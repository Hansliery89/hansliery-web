-- =================================================================
-- Fases 4 y 5: progreso, motor de exámenes y certificados
-- La calificación y la emisión ocurren solo en el servidor.
-- =================================================================

-- Código aleatorio con alfabeto sin caracteres ambiguos (sin I, O, 0, 1)
create or replace function private.random_code(p_groups int default 3)
returns text language plpgsql volatile set search_path = '' as $$
declare
  a text := 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  b bytea := extensions.gen_random_bytes(p_groups * 4);
  r text := ''; i int;
begin
  for i in 0 .. p_groups * 4 - 1 loop
    if i > 0 and i % 4 = 0 then r := r || '-'; end if;
    r := r || substr(a, (get_byte(b, i) % 32) + 1, 1);
  end loop;
  return r;
end $$;

-- Notificación interna (la usan los procesos del servidor)
create or replace function private.notify(p_profile uuid, p_kind text, p_title text, p_body text, p_link text default null)
returns void language sql security definer set search_path = '' as $$
  insert into public.notifications (profile_id, kind, title, body, link, created_by)
  values (p_profile, p_kind, p_title, p_body, p_link, private.current_profile_id());
$$;

-- ---------------- Progreso: al leer todos los módulos, la matrícula se completa ----------------
create or replace function private.recompute_progress()
returns trigger language plpgsql security definer set search_path = '' as $$
declare
  v_enr uuid := coalesce(new.enrollment_id, old.enrollment_id);
  v_total int; v_done int; v_pct numeric;
begin
  select count(*) into v_total from public.course_modules m
    join public.enrollments e on e.course_id = m.course_id where e.id = v_enr;
  select count(*) into v_done from public.lesson_progress lp where lp.enrollment_id = v_enr and lp.module_id is not null;
  v_pct := case when v_total = 0 then 0 else round(least(v_done, v_total) * 100.0 / v_total, 2) end;
  update public.enrollments
     set progress_pct = v_pct,
         status = case when v_pct >= 100 and status = 'active' then 'completed'::public.enrollment_status else status end,
         completed_at = case when v_pct >= 100 and completed_at is null then now() else completed_at end
   where id = v_enr;
  return null;
end $$;

-- ---------------- Motor de exámenes ----------------
-- Preguntas de un intento SIN la respuesta correcta
create or replace function private.attempt_payload(p_attempt uuid)
returns jsonb language sql stable security definer set search_path = '' as $$
  select jsonb_build_object(
    'attempt_id', a.id, 'exam_id', a.exam_id, 'title', x.title, 'description', x.description,
    'attempt_number', a.attempt_number, 'max_attempts', x.max_attempts, 'pass_percentage', x.pass_percentage,
    'started_at', a.started_at, 'expires_at', a.expires_at, 'status', a.status, 'responses', a.responses,
    'questions', coalesce((
      select jsonb_agg(jsonb_build_object(
        'id', q.id, 'type', q.type, 'prompt', q.prompt, 'points', q.points,
        'answers', coalesce((select jsonb_agg(jsonb_build_object('id', an.id, 'label', an.label)
                                      order by case when x.shuffle_questions and q.type <> 'true_false'
                                                    then md5(an.id::text || a.id::text) else lpad(an.position::text, 5, '0') end)
                             from public.answers an where an.question_id = q.id), '[]'::jsonb))
        order by o.n)
      from unnest(a.question_ids) with ordinality o(qid, n) join public.questions q on q.id = o.qid), '[]'::jsonb))
  from public.exam_attempts a join public.exams x on x.id = a.exam_id where a.id = p_attempt;
$$;

-- Califica las preguntas automáticas y cierra el intento
create or replace function private.finalize_attempt(p_attempt uuid)
returns void language plpgsql security definer set search_path = '' as $$
declare
  a public.exam_attempts%rowtype; x public.exams%rowtype;
  q record; v_auto numeric := 0; v_max numeric := 0; v_manual_q int := 0;
  v_sel uuid[]; v_ok uuid[]; v_pct numeric;
begin
  select * into a from public.exam_attempts where id = p_attempt for update;
  if a.status <> 'in_progress' then return; end if;
  select * into x from public.exams where id = a.exam_id;
  for q in select qq.* from public.questions qq where qq.id = any(a.question_ids) loop
    v_max := v_max + q.points;
    if q.type in ('open', 'case') then v_manual_q := v_manual_q + 1; continue; end if;
    select coalesce(array_agg(distinct e::uuid), '{}') into v_sel
      from jsonb_array_elements_text(case when jsonb_typeof(a.responses -> q.id::text) = 'array'
                                          then a.responses -> q.id::text else '[]'::jsonb end) e
     where e ~ '^[0-9a-f-]{36}$';
    select coalesce(array_agg(id), '{}') into v_ok from public.answers where question_id = q.id and is_correct;
    if cardinality(v_ok) > 0 and v_sel @> v_ok and v_ok @> v_sel then v_auto := v_auto + q.points; end if;
  end loop;
  if v_manual_q = 0 then
    v_pct := case when v_max = 0 then 0 else round(v_auto * 100 / v_max, 2) end;
    update public.exam_attempts set status = 'graded', submitted_at = coalesce(submitted_at, now()), graded_at = now(),
           auto_score = v_auto, max_score = v_max, score_pct = v_pct, passed = v_pct >= x.pass_percentage
     where id = p_attempt;
  else
    update public.exam_attempts set status = 'submitted', submitted_at = coalesce(submitted_at, now()),
           auto_score = v_auto, max_score = v_max
     where id = p_attempt;
  end if;
end $$;

-- Cierra los intentos cuyo tiempo venció (con lo guardado hasta ese momento)
create or replace function private.close_expired_attempts(p_profile uuid default null)
returns int language plpgsql security definer set search_path = '' as $$
declare r record; n int := 0;
begin
  for r in select id from public.exam_attempts
            where status = 'in_progress' and expires_at is not null and expires_at + interval '2 minutes' < now()
              and (p_profile is null or profile_id = p_profile) loop
    perform private.finalize_attempt(r.id); n := n + 1;
  end loop;
  return n;
end $$;

create or replace function public.start_exam(p_exam uuid)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare
  v_profile uuid := private.current_profile_id();
  x public.exams%rowtype; v_used int; v_open uuid; v_qs uuid[]; v_id uuid; v_prog numeric;
begin
  if v_profile is null or not private.mfa_satisfied() then raise exception 'not_allowed' using errcode = '42501'; end if;
  perform private.close_expired_attempts(v_profile);
  select * into x from public.exams where id = p_exam;
  if not found or x.status <> 'published' then raise exception 'exam_not_available'; end if;
  if (x.available_from is not null and now() < x.available_from) or (x.available_until is not null and now() > x.available_until) then
    raise exception 'exam_out_of_window';
  end if;
  if x.course_id is not null then
    select progress_pct into v_prog from public.enrollments
     where profile_id = v_profile and course_id = x.course_id and status <> 'cancelled';
    if not found then raise exception 'not_enrolled'; end if;
    if x.is_certification and v_prog < 100 then raise exception 'course_not_completed'; end if;
  end if;
  if not x.is_free and not exists (select 1 from public.payments
       where profile_id = v_profile and exam_id = x.id and status in ('confirmed', 'partially_refunded')) then
    raise exception 'payment_required';
  end if;

  select id into v_open from public.exam_attempts
   where exam_id = x.id and profile_id = v_profile and status = 'in_progress' limit 1;
  if v_open is not null then return private.attempt_payload(v_open); end if;

  if exists (select 1 from public.exam_attempts where exam_id = x.id and profile_id = v_profile and passed) then
    raise exception 'exam_already_passed';
  end if;
  if exists (select 1 from public.exam_attempts where exam_id = x.id and profile_id = v_profile and status = 'submitted') then
    raise exception 'exam_pending_grading';
  end if;
  select count(*) into v_used from public.exam_attempts where exam_id = x.id and profile_id = v_profile;
  if v_used >= x.max_attempts then raise exception 'no_attempts_left'; end if;

  select coalesce(array_agg(id), '{}') into v_qs from (
    select id from public.questions where exam_id = x.id and is_active
     order by case when x.shuffle_questions then random() else position end
     limit coalesce(x.questions_per_attempt, 1000)) s;
  if cardinality(v_qs) = 0 then raise exception 'exam_not_available'; end if;

  insert into public.exam_attempts (exam_id, profile_id, attempt_number, question_ids, expires_at)
  values (x.id, v_profile, v_used + 1, v_qs,
          case when x.time_limit_minutes is not null then now() + make_interval(mins => x.time_limit_minutes) end)
  returning id into v_id;
  perform private.log('exam.started', 'exam_attempts', v_id::text, jsonb_build_object('exam', x.id));
  return private.attempt_payload(v_id);
end $$;

-- Guarda respuestas parciales (autoguardado)
create or replace function public.save_exam_progress(p_attempt uuid, p_responses jsonb)
returns void language plpgsql security definer set search_path = '' as $$
declare a public.exam_attempts%rowtype;
begin
  select * into a from public.exam_attempts where id = p_attempt for update;
  if not found or a.profile_id is distinct from private.current_profile_id() then raise exception 'not_allowed' using errcode = '42501'; end if;
  if a.status <> 'in_progress' or (a.expires_at is not null and now() > a.expires_at + interval '30 seconds') then
    raise exception 'attempt_closed';
  end if;
  if jsonb_typeof(p_responses) <> 'object' or length(p_responses::text) > 60000 then raise exception 'validation_failed'; end if;
  -- Solo se guardan respuestas de preguntas de este intento
  update public.exam_attempts
     set responses = (select coalesce(jsonb_object_agg(k, v), '{}'::jsonb) from jsonb_each(p_responses) e(k, v)
                       where case when k ~ '^[0-9a-f-]{36}$' then k::uuid = any(a.question_ids) else false end)
   where id = p_attempt;
end $$;

create or replace function public.submit_exam(p_attempt uuid, p_responses jsonb)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare a public.exam_attempts%rowtype;
begin
  select * into a from public.exam_attempts where id = p_attempt;
  if not found or a.profile_id is distinct from private.current_profile_id() then raise exception 'not_allowed' using errcode = '42501'; end if;
  if a.status = 'in_progress' then
    if p_responses is not null and (a.expires_at is null or now() <= a.expires_at + interval '30 seconds') then
      perform public.save_exam_progress(p_attempt, p_responses);
    end if;
    perform private.finalize_attempt(p_attempt);
    perform private.log('exam.submitted', 'exam_attempts', p_attempt::text);
  end if;
  return (select jsonb_build_object('status', status, 'score_pct', score_pct, 'passed', passed, 'attempt_number', attempt_number)
            from public.exam_attempts where id = p_attempt);
end $$;

-- Calificación manual de preguntas abiertas o de caso
create or replace function public.grade_exam_attempt(p_attempt uuid, p_manual_score numeric, p_feedback text)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare a public.exam_attempts%rowtype; x public.exams%rowtype; v_manual_max numeric; v_pct numeric;
begin
  select * into a from public.exam_attempts where id = p_attempt for update;
  if not found then raise exception 'not_found'; end if;
  select * into x from public.exams where id = a.exam_id;
  if not (private.is_academic_staff() or (x.course_id is not null and private.can_manage_course(x.course_id))) then
    raise exception 'not_allowed' using errcode = '42501';
  end if;
  if a.status not in ('submitted', 'graded') then raise exception 'attempt_not_submitted'; end if;
  select coalesce(sum(points), 0) into v_manual_max from public.questions where id = any(a.question_ids) and type in ('open', 'case');
  if p_manual_score is null or p_manual_score < 0 or p_manual_score > v_manual_max then raise exception 'invalid_score'; end if;
  v_pct := case when a.max_score > 0 then round((coalesce(a.auto_score, 0) + p_manual_score) * 100 / a.max_score, 2) else 0 end;
  update public.exam_attempts set manual_score = p_manual_score, feedback = left(nullif(btrim(p_feedback), ''), 2000),
         score_pct = v_pct, passed = v_pct >= x.pass_percentage, status = 'graded',
         graded_by = private.current_profile_id(), graded_at = now()
   where id = p_attempt;
  perform private.notify(a.profile_id, 'exam_graded', 'Tu evaluación fue calificada',
          format('«%s»: %s %% (%s).', x.title, v_pct, case when v_pct >= x.pass_percentage then 'aprobada' else 'no aprobada' end), 'panel.html#evaluaciones');
  perform private.log('exam.graded', 'exam_attempts', p_attempt::text, jsonb_build_object('score_pct', v_pct));
  return jsonb_build_object('score_pct', v_pct, 'passed', v_pct >= x.pass_percentage);
end $$;

-- Detalle de un intento para quien califica (incluye respuestas correctas)
create or replace function public.attempt_review(p_attempt uuid)
returns jsonb language plpgsql stable security definer set search_path = '' as $$
declare a public.exam_attempts%rowtype; x public.exams%rowtype;
begin
  select * into a from public.exam_attempts where id = p_attempt;
  if not found then raise exception 'not_found'; end if;
  select * into x from public.exams where id = a.exam_id;
  if not (private.is_academic_staff() or (x.course_id is not null and private.can_manage_course(x.course_id))) then
    raise exception 'not_allowed' using errcode = '42501';
  end if;
  return jsonb_build_object('attempt', to_jsonb(a) - 'question_ids', 'exam', x.title,
    'student', (select btrim(first_name || ' ' || last_name) from public.profiles where id = a.profile_id),
    'questions', (select jsonb_agg(jsonb_build_object('id', q.id, 'type', q.type, 'prompt', q.prompt, 'points', q.points,
        'response', a.responses -> q.id::text,
        'answers', (select jsonb_agg(jsonb_build_object('id', an.id, 'label', an.label, 'is_correct', an.is_correct) order by an.position)
                      from public.answers an where an.question_id = q.id)) order by o.n)
      from unnest(a.question_ids) with ordinality o(qid, n) join public.questions q on q.id = o.qid));
end $$;

-- ---------------- Certificados ----------------
-- Requisitos: módulos completos y, si el curso lo exige, examen de certificación aprobado.
create or replace function private.certificate_check(p_enrollment uuid)
returns jsonb language plpgsql stable security definer set search_path = '' as $$
declare e public.enrollments%rowtype; c public.courses%rowtype; v_best numeric; v_attempt uuid; v_miss text[] := '{}';
begin
  select * into e from public.enrollments where id = p_enrollment;
  if not found then return jsonb_build_object('ok', false, 'missing', array['not_found']); end if;
  select * into c from public.courses where id = e.course_id;
  if e.status = 'cancelled' then v_miss := v_miss || 'enrollment_cancelled'::text; end if;
  if e.progress_pct < 100 then v_miss := v_miss || 'modules_incomplete'::text; end if;
  select a.score_pct, a.id into v_best, v_attempt from public.exam_attempts a join public.exams x on x.id = a.exam_id
   where a.profile_id = e.profile_id and x.course_id = c.id and x.is_certification and a.passed
   order by a.score_pct desc limit 1;
  if c.requires_exam and v_attempt is null then v_miss := v_miss || 'exam_not_passed'::text; end if;
  if exists (select 1 from public.certificates where profile_id = e.profile_id and course_id = c.id and status = 'valid') then
    v_miss := v_miss || 'already_issued'::text;
  end if;
  return jsonb_build_object('ok', cardinality(v_miss) = 0, 'missing', v_miss, 'best_score', v_best, 'attempt_id', v_attempt);
end $$;

create or replace function public.issue_certificate(p_enrollment uuid)
returns text language plpgsql security definer set search_path = '' as $$
declare e public.enrollments%rowtype; c public.courses%rowtype; p public.profiles%rowtype; chk jsonb; v_code text; v_try int := 0;
begin
  select * into e from public.enrollments where id = p_enrollment;
  if not found then raise exception 'not_found'; end if;
  if not private.can_manage_course(e.course_id) then raise exception 'not_allowed' using errcode = '42501'; end if;
  chk := private.certificate_check(p_enrollment);
  if not (chk ->> 'ok')::boolean then
    raise exception 'requirements_not_met: %', array_to_string(array(select jsonb_array_elements_text(chk -> 'missing')), ', ');
  end if;
  select * into c from public.courses where id = e.course_id;
  select * into p from public.profiles where id = e.profile_id;
  if p.status <> 'active' then raise exception 'account_not_active'; end if;
  loop
    v_try := v_try + 1;
    v_code := 'HS-' || private.random_code(3);
    exit when not exists (select 1 from public.certificates where verification_code = v_code) or v_try > 5;
  end loop;
  insert into public.certificates (verification_code, profile_id, course_id, enrollment_id, exam_attempt_id, student_name,
         course_title, academic_hours, completed_on, grade_pct, issued_by)
  values (v_code, p.id, c.id, e.id, nullif(chk ->> 'attempt_id', '')::uuid, btrim(p.first_name || ' ' || p.last_name),
          c.title, c.academic_hours, coalesce(e.completed_at, now())::date, nullif(chk ->> 'best_score', '')::numeric,
          private.current_profile_id());
  perform private.notify(p.id, 'certificate_issued', 'Tu certificado está disponible',
          format('Ya puedes ver e imprimir el certificado de «%s». Código de verificación: %s.', c.title, v_code), 'panel.html#certificados');
  perform private.log('certificate.issued', 'certificates', v_code, jsonb_build_object('enrollment', e.id));
  return v_code;
end $$;

-- Cola de personal: matrículas con requisitos cumplidos y sin certificado vigente
create or replace function public.certificate_queue()
returns table(enrollment_id uuid, profile_id uuid, student_name text, email text, course_id uuid, course_title text,
              progress_pct numeric, best_score numeric, completed_at timestamptz)
language sql stable security definer set search_path = '' as $$
  select e.id, p.id, btrim(p.first_name || ' ' || p.last_name), p.email::text, c.id, c.title, e.progress_pct,
         (private.certificate_check(e.id) ->> 'best_score')::numeric, e.completed_at
    from public.enrollments e join public.profiles p on p.id = e.profile_id join public.courses c on c.id = e.course_id
   where private.can_manage_course(c.id) and p.status = 'active' and e.progress_pct >= 100
     and (private.certificate_check(e.id) ->> 'ok')::boolean
   order by e.completed_at nulls last;
$$;

-- Revocación con motivo obligatorio (solo superadministración)
create or replace function public.revoke_certificate(p_code text, p_reason text)
returns void language plpgsql security definer set search_path = '' as $$
begin
  if not private.is_superadmin() then raise exception 'not_allowed' using errcode = '42501'; end if;
  if char_length(btrim(coalesce(p_reason, ''))) < 5 then raise exception 'reason_required'; end if;
  update public.certificates set status = 'revoked', revoked_reason = left(btrim(p_reason), 500)
   where verification_code = upper(btrim(p_code)) and status = 'valid';
  if not found then raise exception 'not_found'; end if;
  perform private.log('certificate.revoked', 'certificates', upper(btrim(p_code)), jsonb_build_object('reason', p_reason));
end $$;

-- Datos públicos de un certificado para la página imprimible y el verificador (incluye la calificación)
create or replace function public.certificate_public(p_code text)
returns table(student_name text, course_title text, academic_hours numeric, completed_on date, issued_at timestamptz,
              status public.certificate_status, grade_pct numeric, verification_code text)
language sql stable security definer set search_path = '' as $$
  select c.student_name, c.course_title, c.academic_hours, c.completed_on, c.issued_at, c.status, c.grade_pct, c.verification_code
  from public.certificates c
  where length(p_code) <= 20 and c.verification_code = upper(btrim(p_code));
$$;

-- ---------------- Permisos de ejecución ----------------
revoke all on function public.start_exam(uuid), public.save_exam_progress(uuid, jsonb), public.submit_exam(uuid, jsonb),
  public.grade_exam_attempt(uuid, numeric, text), public.attempt_review(uuid), public.issue_certificate(uuid),
  public.certificate_queue(), public.revoke_certificate(text, text), public.certificate_public(text) from public, anon;
grant execute on function public.start_exam(uuid), public.save_exam_progress(uuid, jsonb), public.submit_exam(uuid, jsonb),
  public.grade_exam_attempt(uuid, numeric, text), public.attempt_review(uuid), public.issue_certificate(uuid),
  public.certificate_queue(), public.revoke_certificate(text, text) to authenticated;
grant execute on function public.certificate_public(text) to anon, authenticated;
revoke all on function private.random_code(int), private.notify(uuid, text, text, text, text), private.attempt_payload(uuid),
  private.finalize_attempt(uuid), private.close_expired_attempts(uuid), private.certificate_check(uuid) from public, anon, authenticated;

-- Cierre periódico de intentos vencidos
select cron.schedule('academy-close-expired-attempts', '*/10 * * * *', $$select private.close_expired_attempts()$$);
