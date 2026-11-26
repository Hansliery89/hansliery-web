-- =================================================================
-- Fases 6 a 9: centro de control, finanzas, reconocimientos y becas,
-- mensajería, avisos y tareas de mantenimiento.
-- Reglas: nada financiero se simula; ningún descuento, beca ni
-- reconocimiento se aplica sin aprobación de la superadministración.
-- =================================================================

alter table public.notifications add column if not exists email_attempts smallint not null default 0;

-- ---------------- Centro de control ----------------
create or replace function public.admin_overview()
returns jsonb language plpgsql stable security definer set search_path = '' as $$
begin
  if not (private.is_academic_staff() or private.has_role('instructor')) or not private.staff_session() then
    raise exception 'not_allowed' using errcode = '42501';
  end if;
  return jsonb_build_object(
    'students', (select count(*) from public.student_accounts sa join public.profiles p on p.id = sa.profile_id where p.status <> 'anonymized'),
    'students_active_30d', (select count(*) from public.student_accounts sa join public.profiles p on p.id = sa.profile_id
                             where p.status = 'active' and p.last_activity_at > now() - interval '30 days'),
    'suspended', (select count(*) from public.profiles where status = 'suspended'),
    'enrollments', (select count(*) from public.enrollments e where e.status <> 'cancelled' and private.can_manage_course(e.course_id)),
    'completed', (select count(*) from public.enrollments e where e.status = 'completed' and private.can_manage_course(e.course_id)),
    'certificates', (select count(*) from public.certificates c where c.status = 'valid' and private.can_manage_course(c.course_id)),
    'certificate_queue', (select count(*) from public.certificate_queue()),
    'attempts_to_grade', (select count(*) from public.exam_attempts a join public.exams x on x.id = a.exam_id
                           where a.status = 'submitted' and (private.is_academic_staff() or private.can_manage_course(x.course_id))),
    'submissions_to_grade', (select count(*) from public.assignment_submissions s join public.assignments a on a.id = s.assignment_id
                              where s.status in ('submitted', 'in_review') and private.can_manage_course(a.course_id)),
    'threads_pending', (select count(*) from public.message_threads t where t.status in ('open', 'pending')
                         and (private.is_academic_staff() or (t.course_id is not null and private.can_manage_course(t.course_id)))),
    'deletion_requests', case when private.is_academic_staff() then (select count(*) from public.account_deletion_requests where status in ('open', 'blocked', 'scheduled')) end,
    'award_candidates', case when private.is_academic_staff() then (select count(*) from public.awards where status = 'candidate') end,
    'scholarships_proposed', case when private.is_academic_staff() then (select count(*) from public.scholarships where status = 'proposed') end,
    'payments_pending', case when private.is_superadmin() then (select count(*) from public.payments where status = 'pending') end);
end $$;

create or replace function public.admin_student_list(p_search text default null)
returns table(profile_id uuid, student_code text, full_name text, email text, status public.account_status, country text,
              organization text, last_activity_at timestamptz, created_at timestamptz, enrollments bigint, completed bigint,
              certificates bigint, roles public.app_role[])
language sql stable security definer set search_path = '' as $$
  select p.id, sa.student_code, btrim(p.first_name || ' ' || p.last_name), p.email::text, p.status, p.country, p.organization,
         p.last_activity_at, p.created_at,
         (select count(*) from public.enrollments e where e.profile_id = p.id and e.status <> 'cancelled'),
         (select count(*) from public.enrollments e where e.profile_id = p.id and e.status = 'completed'),
         (select count(*) from public.certificates c where c.profile_id = p.id and c.status = 'valid'),
         array(select ur.role from public.user_roles ur where ur.profile_id = p.id order by ur.role)
    from public.profiles p left join public.student_accounts sa on sa.profile_id = p.id
   where private.is_academic_staff() and p.status <> 'anonymized'
     and (p_search is null or btrim(p_search) = '' or
          (p.first_name || ' ' || p.last_name || ' ' || p.email || ' ' || coalesce(sa.student_code, '')) ilike '%' || btrim(p_search) || '%')
   order by p.created_at desc
   limit 500;
$$;

create or replace function public.admin_course_stats()
returns table(course_id uuid, title text, status public.course_status, enrollments bigint, completed bigint,
              avg_progress numeric, certificates bigint, exams bigint, pass_rate numeric)
language sql stable security definer set search_path = '' as $$
  select c.id, c.title, c.status,
         (select count(*) from public.enrollments e where e.course_id = c.id and e.status <> 'cancelled'),
         (select count(*) from public.enrollments e where e.course_id = c.id and e.status = 'completed'),
         (select round(avg(e.progress_pct), 1) from public.enrollments e where e.course_id = c.id and e.status <> 'cancelled'),
         (select count(*) from public.certificates x where x.course_id = c.id and x.status = 'valid'),
         (select count(*) from public.exams x where x.course_id = c.id),
         (select round(100.0 * count(*) filter (where a.passed) / nullif(count(*) filter (where a.status = 'graded'), 0), 1)
            from public.exam_attempts a join public.exams x on x.id = a.exam_id where x.course_id = c.id)
    from public.courses c
   where private.can_manage_course(c.id)
   order by c.title;
$$;

create or replace function public.admin_set_account_status(p_profile uuid, p_status public.account_status, p_reason text default null)
returns void language plpgsql security definer set search_path = '' as $$
begin
  if not private.is_superadmin() then raise exception 'not_allowed' using errcode = '42501'; end if;
  if p_status not in ('active', 'suspended') then raise exception 'validation_failed'; end if;
  if p_profile = private.current_profile_id() then raise exception 'cannot_change_own_status'; end if;
  update public.profiles set status = p_status where id = p_profile and status in ('active', 'suspended');
  if not found then raise exception 'not_found'; end if;
  update public.student_accounts set suspended_at = case when p_status = 'suspended' then now() end,
         inactivity_warning_level = case when p_status = 'active' then 0 else inactivity_warning_level end
   where profile_id = p_profile;
  if p_status = 'active' then
    update public.account_deletion_requests set status = 'cancelled', processed_by = private.current_profile_id()
     where profile_id = p_profile and reason = 'inactivity' and status in ('open', 'blocked', 'scheduled');
  end if;
  perform private.notify(p_profile, 'account_status',
          case when p_status = 'active' then 'Tu cuenta fue reactivada' else 'Tu cuenta fue suspendida' end,
          coalesce(nullif(btrim(p_reason), ''), case when p_status = 'active' then 'Ya puedes volver a usar el aula virtual.' else 'Escríbenos si necesitas más información.' end));
  perform private.log('account.status_changed', 'profiles', p_profile::text, jsonb_build_object('status', p_status, 'reason', p_reason));
end $$;

-- Atención de solicitudes de baja: anonimizar (si nada lo impide) o cancelar
create or replace function public.admin_process_deletion(p_request uuid, p_action text)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare d public.account_deletion_requests%rowtype; v_blk text[];
begin
  if not private.is_superadmin() then raise exception 'not_allowed' using errcode = '42501'; end if;
  select * into d from public.account_deletion_requests where id = p_request for update;
  if not found or d.status in ('completed', 'cancelled') then raise exception 'not_found'; end if;
  if p_action = 'cancel' then
    update public.account_deletion_requests set status = 'cancelled', processed_by = private.current_profile_id() where id = p_request;
    return jsonb_build_object('status', 'cancelled');
  elsif p_action = 'anonymize' then
    v_blk := private.deletion_blockers(d.profile_id);
    if cardinality(v_blk) > 0 then
      update public.account_deletion_requests set status = 'blocked', blocking_reasons = v_blk where id = p_request;
      return jsonb_build_object('status', 'blocked', 'blocking_reasons', v_blk);
    end if;
    perform private.anonymize_profile(d.profile_id);
    update public.account_deletion_requests set status = 'completed', completed_at = now(), blocking_reasons = '{}',
           processed_by = private.current_profile_id() where id = p_request;
    return jsonb_build_object('status', 'completed');
  end if;
  raise exception 'validation_failed';
end $$;

-- ---------------- Finanzas (solo superadministración) ----------------
create or replace function public.finance_summary(p_from date, p_to date)
returns jsonb language plpgsql stable security definer set search_path = '' as $$
begin
  if not private.is_superadmin() then raise exception 'not_allowed' using errcode = '42501'; end if;
  return (
    with base as (
      select p.*, rc.name as category, rc.grp
        from public.payments p join public.revenue_categories rc on rc.id = p.category_id
       where p.occurred_on between p_from and p_to),
    ok as (select * from base where status in ('confirmed', 'partially_refunded', 'refunded'))
    select jsonb_build_object(
      'totals', coalesce((select jsonb_agg(t) from (
          select currency, count(*) as payments, sum(amount) as gross, sum(discount_amount) as discounts, sum(fee_amount) as fees,
                 sum(refunded_amount) as refunds, sum(net_amount) as net
            from ok group by currency order by currency) t), '[]'),
      'pending', coalesce((select jsonb_agg(t) from (
          select currency, count(*) as payments, sum(amount) as amount from base where status = 'pending' group by currency) t), '[]'),
      'by_category', coalesce((select jsonb_agg(t) from (
          select currency, category, grp, count(*) as payments, sum(net_amount) as net
            from ok group by currency, category, grp order by currency, sum(net_amount) desc) t), '[]'),
      'by_month', coalesce((select jsonb_agg(t) from (
          select to_char(occurred_on, 'YYYY-MM') as month, currency, sum(net_amount) as net, count(*) as payments
            from ok group by 1, 2 order by 1, 2) t), '[]'),
      'by_method', coalesce((select jsonb_agg(t) from (
          select currency, method, count(*) as payments, sum(net_amount) as net from ok group by 1, 2 order by 1, 4 desc) t), '[]'),
      'by_product', coalesce((select jsonb_agg(t) from (
          select currency, product_type, coalesce(product_name, concept) as product, count(*) as payments, sum(net_amount) as net
            from ok group by 1, 2, 3 order by 1, 5 desc limit 30) t), '[]'));
  end;
$$;

-- Validación de becas usadas en un pago (antes de guardar)
create or replace function private.payment_validate()
returns trigger language plpgsql security definer set search_path = '' as $$
begin
  if new.scholarship_id is not null and (tg_op = 'INSERT' or new.scholarship_id is distinct from old.scholarship_id) then
    if not exists (select 1 from public.scholarships s
                    where s.id = new.scholarship_id and s.profile_id = new.profile_id and s.status = 'approved'
                      and (s.expires_on is null or s.expires_on >= current_date)) then
      raise exception 'scholarship_invalid';
    end if;
  end if;
  if new.status in ('confirmed', 'partially_refunded', 'refunded') and new.confirmed_by is null then
    new.confirmed_by := private.current_profile_id();
  end if;
  return new;
end $$;

-- Pago confirmado: matrícula del curso pagado, beca marcada como usada y aviso al estudiante
create or replace function private.payment_confirmed()
returns trigger language plpgsql security definer set search_path = '' as $$
declare v_enr uuid;
begin
  if new.status = 'confirmed' and (tg_op = 'INSERT' or old.status is distinct from 'confirmed') then
    if new.profile_id is not null and new.course_id is not null then
      insert into public.enrollments (profile_id, course_id, payment_id, scholarship_id)
      values (new.profile_id, new.course_id, new.id, new.scholarship_id)
      on conflict (profile_id, course_id) do update
        set payment_id = coalesce(public.enrollments.payment_id, excluded.payment_id),
            scholarship_id = coalesce(public.enrollments.scholarship_id, excluded.scholarship_id),
            status = case when public.enrollments.status = 'cancelled' then 'active'::public.enrollment_status else public.enrollments.status end
      returning id into v_enr;
    end if;
    if new.scholarship_id is not null then
      update public.scholarships set status = 'used', used_at = now(), used_enrollment_id = v_enr
       where id = new.scholarship_id and status = 'approved';
    end if;
    if new.profile_id is not null then
      perform private.notify(new.profile_id, 'payment_confirmed', 'Pago confirmado',
              format('Registramos tu pago de %s %s por «%s».', new.currency, to_char(new.amount, 'FM999,999,990.00'), new.concept),
              'panel.html#perfil');
    end if;
  end if;
  return null;
end $$;

create trigger payments_validate before insert or update on public.payments
  for each row execute function private.payment_validate();
create trigger payments_confirmed after insert or update of status on public.payments
  for each row execute function private.payment_confirmed();

-- ---------------- Reconocimientos y medias becas ----------------
create or replace function public.compute_award_candidates(p_period text, p_from date, p_to date)
returns int language plpgsql security definer set search_path = '' as $$
declare
  w jsonb := coalesce((select value from public.academy_settings where key = 'award_weights'),
                      '{"calificaciones":50,"finalizacion":20,"evaluaciones":15,"asignaciones":10,"participacion":5}');
  v_min numeric := coalesce(private.setting_int('award_min_grade', 85), 85);
  r record; comp jsonb; v_score numeric; v_wsum numeric; k text; n int := 0;
begin
  if not private.is_academic_staff() then raise exception 'not_allowed' using errcode = '42501'; end if;
  if p_from is null or p_to is null or p_from > p_to or char_length(btrim(coalesce(p_period, ''))) < 4 then raise exception 'validation_failed'; end if;
  for r in
    select p.id,
      (select round(avg(best), 2) from (select max(a.score_pct) best from public.exam_attempts a
          where a.profile_id = p.id and a.status = 'graded' and a.graded_at::date between p_from and p_to group by a.exam_id) b) as calificaciones,
      (select round(100.0 * count(distinct a.exam_id) filter (where a.passed) / nullif(count(distinct a.exam_id), 0), 2)
         from public.exam_attempts a where a.profile_id = p.id and a.status = 'graded' and a.graded_at::date between p_from and p_to) as evaluaciones,
      (select round(100.0 * count(*) filter (where e.completed_at::date <= p_to) / nullif(count(*), 0), 2)
         from public.enrollments e where e.profile_id = p.id and e.status <> 'cancelled' and e.enrolled_at::date <= p_to) as finalizacion,
      (select round(avg(least(100, s.score * 100 / nullif(x.max_score, 0))), 2)
         from public.assignment_submissions s join public.assignments x on x.id = s.assignment_id
        where s.profile_id = p.id and s.status = 'graded' and s.graded_at::date between p_from and p_to) as asignaciones,
      (select round(least(100, 100.0 * count(lp.*) / nullif((select count(*) from public.course_modules m join public.enrollments e2
                  on e2.course_id = m.course_id where e2.profile_id = p.id and e2.status <> 'cancelled'), 0)), 2)
         from public.lesson_progress lp join public.enrollments e on e.id = lp.enrollment_id
        where e.profile_id = p.id and lp.completed_at::date between p_from and p_to) as participacion
    from public.profiles p join public.student_accounts sa on sa.profile_id = p.id
    where p.status = 'active'
  loop
    continue when r.calificaciones is null or r.calificaciones < v_min;
    comp := jsonb_strip_nulls(jsonb_build_object('calificaciones', r.calificaciones, 'evaluaciones', r.evaluaciones,
              'finalizacion', r.finalizacion, 'asignaciones', r.asignaciones, 'participacion', r.participacion));
    v_score := 0; v_wsum := 0;
    for k in select jsonb_object_keys(comp) loop
      v_score := v_score + (comp ->> k)::numeric * coalesce((w ->> k)::numeric, 0);
      v_wsum := v_wsum + coalesce((w ->> k)::numeric, 0);
    end loop;
    v_score := case when v_wsum > 0 then round(v_score / v_wsum, 2) else 0 end;
    continue when v_score < v_min;
    insert into public.awards (profile_id, period_label, level, score, score_breakdown)
    values (r.id, btrim(p_period),
            case when v_score >= 95 then 'excelencia_academica'::public.award_level
                 when v_score >= 90 then 'alto_rendimiento'::public.award_level else 'merito_compromiso'::public.award_level end,
            v_score, jsonb_build_object('components', comp, 'weights', w, 'from', p_from, 'to', p_to))
    on conflict (profile_id, period_label) do nothing;
    if found then n := n + 1; end if;
  end loop;
  perform private.log('awards.computed', 'awards', btrim(p_period), jsonb_build_object('candidates', n, 'from', p_from, 'to', p_to));
  return n;
end $$;

create or replace function public.review_award(p_award uuid, p_approve boolean)
returns void language plpgsql security definer set search_path = '' as $$
declare a public.awards%rowtype; v_code text;
begin
  if not private.is_superadmin() then raise exception 'not_allowed' using errcode = '42501'; end if;
  select * into a from public.awards where id = p_award for update;
  if not found or a.status <> 'candidate' then raise exception 'not_found'; end if;
  if p_approve then
    loop v_code := 'HSR-' || private.random_code(3); exit when not exists (select 1 from public.awards where constancia_code = v_code); end loop;
  end if;
  update public.awards set status = case when p_approve then 'approved'::public.award_status else 'rejected'::public.award_status end,
         constancia_code = v_code, reviewed_by = private.current_profile_id(), reviewed_at = now()
   where id = p_award;
  if p_approve then
    perform private.notify(a.profile_id, 'award_approved', 'Recibiste un reconocimiento académico',
            format('Período %s. Código de constancia: %s.', a.period_label, v_code), 'panel.html#certificados');
  end if;
  perform private.log(case when p_approve then 'award.approved' else 'award.rejected' end, 'awards', p_award::text);
end $$;

create or replace function public.propose_scholarship(p_profile uuid, p_award uuid, p_period text, p_conditions text, p_expires date)
returns uuid language plpgsql security definer set search_path = '' as $$
declare v_id uuid; v_pct numeric := coalesce(private.setting_int('scholarship_percentage', 50), 50);
begin
  if not private.is_academic_staff() then raise exception 'not_allowed' using errcode = '42501'; end if;
  if p_award is not null and not exists (select 1 from public.awards where id = p_award and profile_id = p_profile and status = 'approved') then
    raise exception 'award_not_approved';
  end if;
  if char_length(btrim(coalesce(p_period, ''))) < 4 or (p_expires is not null and p_expires < current_date) then raise exception 'validation_failed'; end if;
  insert into public.scholarships (profile_id, award_id, percentage, period_label, conditions, expires_on, proposed_by)
  values (p_profile, p_award, v_pct, btrim(p_period), left(nullif(btrim(p_conditions), ''), 1000), p_expires, private.current_profile_id())
  returning id into v_id;
  perform private.log('scholarship.proposed', 'scholarships', v_id::text);
  return v_id;
end $$;

create or replace function public.review_scholarship(p_id uuid, p_approve boolean)
returns void language plpgsql security definer set search_path = '' as $$
declare s public.scholarships%rowtype; v_cap int := coalesce(private.setting_int('scholarships_per_period', 3), 3);
begin
  if not private.is_superadmin() then raise exception 'not_allowed' using errcode = '42501'; end if;
  select * into s from public.scholarships where id = p_id for update;
  if not found or s.status <> 'proposed' then raise exception 'not_found'; end if;
  if p_approve and (select count(*) from public.scholarships where period_label = s.period_label and status in ('approved', 'used')) >= v_cap then
    raise exception 'scholarship_cap_reached';
  end if;
  update public.scholarships
     set status = case when p_approve then 'approved'::public.scholarship_status else 'rejected'::public.scholarship_status end,
         approved_by = case when p_approve then private.current_profile_id() end,
         approved_at = case when p_approve then now() end
   where id = p_id;
  if p_approve then
    perform private.notify(s.profile_id, 'scholarship_approved', 'Se te otorgó una media beca',
            format('Beca de %s %% (período %s)%s. Se aplica cuando te inscribas en una capacitación de pago.', s.percentage, s.period_label,
                   case when s.expires_on is not null then ', válida hasta el ' || to_char(s.expires_on, 'DD/MM/YYYY') else '' end), 'panel.html#certificados');
  end if;
  perform private.log(case when p_approve then 'scholarship.approved' else 'scholarship.rejected' end, 'scholarships', p_id::text);
end $$;

-- ---------------- Mensajería y avisos ----------------
create or replace function private.message_posted()
returns trigger language plpgsql security definer set search_path = '' as $$
declare t public.message_threads%rowtype;
begin
  select * into t from public.message_threads where id = new.thread_id;
  if new.sender_profile_id = t.profile_id then
    update public.message_threads set status = 'pending', updated_at = now() where id = t.id;
  else
    update public.message_threads set status = 'answered', updated_at = now() where id = t.id;
    perform private.notify(t.profile_id, 'message_reply', 'Respondimos tu consulta', format('«%s»', t.subject), 'panel.html#comunicaciones');
  end if;
  return null;
end $$;
create trigger messages_posted after insert on public.messages for each row execute function private.message_posted();

create or replace function private.submission_graded()
returns trigger language plpgsql security definer set search_path = '' as $$
declare v_title text;
begin
  if new.status in ('graded', 'returned') and old.status is distinct from new.status then
    select title into v_title from public.assignments where id = new.assignment_id;
    perform private.notify(new.profile_id, 'submission_' || new.status::text,
            case when new.status = 'graded' then 'Tu asignación fue calificada' else 'Tu asignación fue devuelta para corrección' end,
            format('«%s»%s', v_title, case when new.score is not null then ': ' || new.score else '' end), 'panel.html#asignaciones');
  end if;
  return null;
end $$;
create trigger submissions_graded after update of status on public.assignment_submissions
  for each row execute function private.submission_graded();

create or replace function public.admin_send_announcement(p_course uuid, p_title text, p_body text)
returns int language plpgsql security definer set search_path = '' as $$
declare n int;
begin
  if p_course is null and not private.is_academic_staff() then raise exception 'not_allowed' using errcode = '42501'; end if;
  if p_course is not null and not private.can_manage_course(p_course) then raise exception 'not_allowed' using errcode = '42501'; end if;
  if char_length(btrim(coalesce(p_title, ''))) < 3 or char_length(p_title) > 140 or char_length(coalesce(p_body, '')) > 2000 then
    raise exception 'validation_failed';
  end if;
  insert into public.notifications (profile_id, kind, title, body, link, created_by)
  select distinct p.id, 'announcement', btrim(p_title), nullif(btrim(p_body), ''), 'panel.html#comunicaciones', private.current_profile_id()
    from public.profiles p
   where p.status = 'active' and exists (select 1 from public.student_accounts sa where sa.profile_id = p.id)
     and (p_course is null or exists (select 1 from public.enrollments e where e.profile_id = p.id and e.course_id = p_course and e.status <> 'cancelled'));
  get diagnostics n = row_count;
  perform private.log('announcement.sent', 'notifications', coalesce(p_course::text, 'all'), jsonb_build_object('recipients', n, 'title', p_title));
  return n;
end $$;

-- ---------------- Tareas programadas (función Edge academy-jobs) ----------------
select vault.create_secret(encode(extensions.gen_random_bytes(32), 'hex'), 'academy_job_secret', 'Secreto compartido entre pg_cron y la función academy-jobs')
 where not exists (select 1 from vault.secrets where name = 'academy_job_secret');

create or replace function public.job_secret_ok(p_secret text)
returns boolean language sql stable security definer set search_path = '' as $$
  select coalesce(length(p_secret) = 64 and p_secret = (select decrypted_secret from vault.decrypted_secrets where name = 'academy_job_secret'), false);
$$;

create or replace function public.job_caller_is_admin()
returns boolean language sql stable security definer set search_path = '' as $$
  select private.is_superadmin();
$$;

create or replace function public.job_pending_emails(p_limit int default 50)
returns table(id uuid, email text, first_name text, title text, body text, link text)
language sql stable security definer set search_path = '' as $$
  select n.id, p.email::text, p.first_name, n.title, n.body, n.link
    from public.notifications n join public.profiles p on p.id = n.profile_id
   where n.email_sent_at is null and n.email_attempts < 3 and n.created_at > now() - interval '3 days'
     and p.status = 'active' and p.email not like '%@academy.invalid'
   order by n.created_at limit least(greatest(p_limit, 1), 200);
$$;

create or replace function public.job_mark_emails(p_sent uuid[], p_failed uuid[])
returns void language sql security definer set search_path = '' as $$
  update public.notifications set email_sent_at = now() where id = any(coalesce(p_sent, '{}'));
  update public.notifications set email_attempts = email_attempts + 1 where id = any(coalesce(p_failed, '{}'));
$$;

create or replace function public.job_cleanup_batch()
returns jsonb language sql stable security definer set search_path = '' as $$
  select jsonb_build_object(
    'storage', coalesce((select jsonb_agg(jsonb_build_object('id', id, 'bucket', bucket_id, 'prefix', prefix))
                           from (select * from private.storage_cleanup_queue where processed_at is null order by id limit 100) q), '[]'),
    'users', coalesce((select jsonb_agg(user_id) from (select user_id from public.profiles
                         where status = 'anonymized' and user_id is not null limit 100) u), '[]'));
$$;

create or replace function public.job_cleanup_done(p_queue bigint[], p_users uuid[])
returns void language plpgsql security definer set search_path = '' as $$
begin
  update private.storage_cleanup_queue set processed_at = now() where id = any(coalesce(p_queue, '{}'));
  if cardinality(coalesce(p_users, '{}')) > 0 then
    insert into public.activity_logs (action, entity, metadata)
    values ('auth.users_deleted', 'auth.users', jsonb_build_object('count', cardinality(p_users)));
  end if;
end $$;

-- Vencimiento de becas aprobadas y no usadas
create or replace function private.expire_scholarships()
returns int language sql security definer set search_path = '' as $$
  with u as (update public.scholarships set status = 'expired'
              where status = 'approved' and expires_on is not null and expires_on < current_date returning 1)
  select count(*)::int from u;
$$;

-- ---------------- Permisos ----------------
revoke all on function public.admin_overview(), public.admin_student_list(text), public.admin_course_stats(),
  public.admin_set_account_status(uuid, public.account_status, text), public.admin_process_deletion(uuid, text),
  public.finance_summary(date, date), public.compute_award_candidates(text, date, date), public.review_award(uuid, boolean),
  public.propose_scholarship(uuid, uuid, text, text, date), public.review_scholarship(uuid, boolean),
  public.admin_send_announcement(uuid, text, text), public.job_caller_is_admin(),
  public.job_secret_ok(text), public.job_pending_emails(int), public.job_mark_emails(uuid[], uuid[]),
  public.job_cleanup_batch(), public.job_cleanup_done(bigint[], uuid[]) from public, anon, authenticated;
grant execute on function public.admin_overview(), public.admin_student_list(text), public.admin_course_stats(),
  public.admin_set_account_status(uuid, public.account_status, text), public.admin_process_deletion(uuid, text),
  public.finance_summary(date, date), public.compute_award_candidates(text, date, date), public.review_award(uuid, boolean),
  public.propose_scholarship(uuid, uuid, text, text, date), public.review_scholarship(uuid, boolean),
  public.admin_send_announcement(uuid, text, text), public.job_caller_is_admin() to authenticated;
grant execute on function public.job_secret_ok(text), public.job_pending_emails(int), public.job_mark_emails(uuid[], uuid[]),
  public.job_cleanup_batch(), public.job_cleanup_done(bigint[], uuid[]) to service_role;
revoke all on function private.payment_validate(), private.payment_confirmed(), private.message_posted(),
  private.submission_graded(), private.expire_scholarships() from public, anon, authenticated;

select cron.schedule('academy-expire-scholarships', '30 6 * * *', $$select private.expire_scholarships()$$);
select cron.schedule('academy-jobs', '*/15 * * * *', $$
  select net.http_post(
    url := 'https://vbodazonicfzfovlighm.supabase.co/functions/v1/academy-jobs',
    headers := jsonb_build_object('Content-Type', 'application/json',
                 'x-job-secret', (select decrypted_secret from vault.decrypted_secrets where name = 'academy_job_secret')),
    body := '{"tasks":["cleanup","email"]}'::jsonb,
    timeout_milliseconds := 30000)
$$);
