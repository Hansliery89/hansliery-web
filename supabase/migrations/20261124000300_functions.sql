-- =====================================================================
-- HANSLIERY ACADEMY · 0003 · Funciones de autorización, alta de cuentas,
-- bitácora y operaciones seguras (RPC)
-- Todas las funciones SECURITY DEFINER fijan search_path = ''.
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1. Ayudantes de autorización (usados por las políticas RLS)
-- ---------------------------------------------------------------------

-- ¿La sesión cumple el doble factor? aal2, o el usuario no tiene factores verificados.
create or replace function private.mfa_satisfied()
returns boolean language sql stable security definer set search_path = '' as $$
  select coalesce((auth.jwt() ->> 'aal') = 'aal2', false)
      or not exists (select 1 from auth.mfa_factors f
                     where f.user_id = auth.uid() and f.status = 'verified');
$$;

-- Perfil del usuario autenticado, solo si está activo y cumple 2FA.
create or replace function private.current_profile_id()
returns uuid language sql stable security definer set search_path = '' as $$
  select p.id from public.profiles p
  where p.user_id = auth.uid() and p.status = 'active' and private.mfa_satisfied();
$$;

-- El personal (no estudiantes) debe operar SIEMPRE con sesión aal2.
create or replace function private.staff_session()
returns boolean language sql stable set search_path = '' as $$
  select coalesce((auth.jwt() ->> 'aal') = 'aal2', false);
$$;

create or replace function private.has_role(r public.app_role)
returns boolean language sql stable security definer set search_path = '' as $$
  select exists (
    select 1 from public.user_roles ur
    join public.profiles p on p.id = ur.profile_id
    where p.user_id = auth.uid() and p.status = 'active' and ur.role = r)
  and (r = 'student' or private.staff_session());
$$;

create or replace function private.is_superadmin()
returns boolean language sql stable set search_path = '' as $$
  select private.has_role('superadmin');
$$;

-- Personal académico: superadministrador o administrador académico.
create or replace function private.is_academic_staff()
returns boolean language sql stable set search_path = '' as $$
  select private.has_role('superadmin') or private.has_role('academic_admin');
$$;

-- ¿Puede gestionar este curso? Personal académico o instructor asignado.
create or replace function private.can_manage_course(c uuid)
returns boolean language sql stable security definer set search_path = '' as $$
  select private.is_academic_staff() or (
    private.staff_session() and exists (
      select 1 from public.user_roles ur
      join public.profiles p on p.id = ur.profile_id
      where p.user_id = auth.uid() and p.status = 'active'
        and ur.role = 'instructor' and ur.course_id = c));
$$;

-- ¿El estudiante autenticado está matriculado en el curso?
create or replace function private.is_enrolled(c uuid)
returns boolean language sql stable security definer set search_path = '' as $$
  select exists (select 1 from public.enrollments e
                 where e.course_id = c and e.status <> 'cancelled'
                   and e.profile_id = private.current_profile_id());
$$;

-- ¿Este estudiante pertenece a alguno de los cursos que el instructor gestiona?
create or replace function private.instructor_sees_student(student uuid)
returns boolean language sql stable security definer set search_path = '' as $$
  select private.staff_session() and exists (
    select 1 from public.enrollments e
    join public.user_roles ur on ur.course_id = e.course_id and ur.role = 'instructor'
    join public.profiles p on p.id = ur.profile_id
    where e.profile_id = student and p.user_id = auth.uid() and p.status = 'active');
$$;

-- ---------------------------------------------------------------------
-- 2. Bitácora
-- ---------------------------------------------------------------------
create or replace function private.log(p_action text, p_entity text, p_entity_id text, p_meta jsonb default '{}'::jsonb)
returns void language sql security definer set search_path = '' as $$
  insert into public.activity_logs (actor_user_id, actor_profile_id, action, entity, entity_id, metadata)
  values (auth.uid(),
          (select id from public.profiles where user_id = auth.uid()),
          p_action, p_entity, p_entity_id, coalesce(p_meta, '{}'::jsonb));
$$;

-- Auditoría genérica: registra operación y columnas modificadas (sin copiar valores personales).
create or replace function private.audit_row()
returns trigger language plpgsql security definer set search_path = '' as $$
declare
  v_id text;
  v_changed text[];
begin
  if tg_op = 'DELETE' then
    v_id := (to_jsonb(old) ->> 'id');
  else
    v_id := coalesce(to_jsonb(new) ->> 'id', to_jsonb(new) ->> 'key', to_jsonb(new) ->> 'profile_id');
  end if;
  if tg_op = 'UPDATE' then
    select array_agg(n.key order by n.key) into v_changed
    from jsonb_each(to_jsonb(new)) n
    where n.value is distinct from (to_jsonb(old) -> n.key) and n.key not in ('updated_at');
    if v_changed is null then return new; end if;
  end if;
  perform private.log(lower(tg_table_name || '.' || tg_op), tg_table_name, v_id,
                      case when v_changed is null then '{}'::jsonb else jsonb_build_object('changed', v_changed) end);
  return coalesce(new, old);
end $$;

do $$
declare t text;
begin
  foreach t in array array['profiles','user_roles','courses','course_modules','lessons','exams','questions','answers',
                           'payments','revenue_categories','scholarships','awards','certificates','academy_settings',
                           'account_deletion_requests','enrollments'] loop
    execute format('create trigger %I_audit after insert or update or delete on public.%I
                    for each row execute function private.audit_row()', t, t);
  end loop;
end $$;

-- ---------------------------------------------------------------------
-- 3. Alta de cuentas: perfil, cuenta de estudiante y rol, en la misma transacción
-- ---------------------------------------------------------------------
create sequence if not exists private.student_code_seq;

create or replace function private.new_student_code()
returns text language sql volatile set search_path = '' as $$
  select 'HSA-' || to_char(now(), 'YYYY') || '-' || lpad(nextval('private.student_code_seq')::text, 6, '0');
$$;

create or replace function private.clean_text(v text, maxlen int)
returns text language sql immutable set search_path = '' as $$
  select nullif(left(btrim(regexp_replace(coalesce(v, ''), '[[:cntrl:]<>]', '', 'g')), maxlen), '');
$$;

create or replace function private.handle_new_user()
returns trigger language plpgsql security definer set search_path = '' as $$
declare
  v_email   text := lower(btrim(new.email));
  m         jsonb := coalesce(new.raw_user_meta_data, '{}'::jsonb);
  v_full    text := coalesce(m ->> 'full_name', m ->> 'name', '');
  v_first   text;
  v_last    text;
  v_phone   text;
  v_profile uuid;
  v_terms   boolean := (m ->> 'terms_accepted') = 'true';
  v_privacy boolean := (m ->> 'privacy_consent') = 'true';
begin
  if v_email is null or v_email = '' then
    raise exception 'email_required' using errcode = '23502';
  end if;
  -- Prevención de duplicados (además del índice UNIQUE, que resuelve las carreras)
  if exists (select 1 from public.profiles where email = v_email) then
    raise exception 'email_already_registered' using errcode = '23505';
  end if;

  v_first := coalesce(private.clean_text(m ->> 'first_name', 80), private.clean_text(m ->> 'given_name', 80),
                      private.clean_text(split_part(v_full, ' ', 1), 80), '');
  v_last  := coalesce(private.clean_text(m ->> 'last_name', 80), private.clean_text(m ->> 'family_name', 80),
                      private.clean_text(regexp_replace(v_full, '^\S+\s*', ''), 80), '');
  v_phone := private.clean_text(m ->> 'phone', 20);
  if v_phone is not null and v_phone !~ '^\+?[0-9 ()-]{7,20}$' then v_phone := null; end if;

  insert into public.profiles (user_id, email, first_name, last_name, phone, country, city, occupation,
                               organization, interest_area, terms_version, terms_accepted_at, privacy_consent_at)
  values (new.id, v_email, v_first, v_last, v_phone,
          private.clean_text(m ->> 'country', 60), private.clean_text(m ->> 'city', 80),
          private.clean_text(m ->> 'occupation', 120), private.clean_text(m ->> 'organization', 120),
          private.clean_text(m ->> 'interest_area', 120),
          case when v_terms then private.clean_text(m ->> 'terms_version', 20) end,
          case when v_terms then now() end,
          case when v_privacy then now() end)
  returning id into v_profile;

  insert into public.student_accounts (profile_id, student_code) values (v_profile, private.new_student_code());
  insert into public.user_roles (profile_id, role) values (v_profile, 'student');

  insert into public.activity_logs (actor_user_id, actor_profile_id, action, entity, entity_id, metadata)
  values (new.id, v_profile, 'account.created', 'profiles', v_profile::text,
          jsonb_build_object('provider', coalesce(new.raw_app_meta_data ->> 'provider', 'email'),
                             'terms', v_terms, 'privacy', v_privacy));
  return new;
end $$;

create trigger on_auth_user_created
  after insert on auth.users for each row execute function private.handle_new_user();

-- Cambio de correo en Auth (ya verificado por Auth) → perfil
create or replace function private.handle_user_email_change()
returns trigger language plpgsql security definer set search_path = '' as $$
begin
  if new.email is distinct from old.email and new.email is not null then
    update public.profiles set email = lower(btrim(new.email)) where user_id = new.id;
  end if;
  return new;
end $$;

create trigger on_auth_user_email_changed
  after update of email on auth.users for each row execute function private.handle_user_email_change();

-- Impide quitar el último superadministrador.
create or replace function private.protect_last_superadmin()
returns trigger language plpgsql security definer set search_path = '' as $$
begin
  if old.role = 'superadmin' and (tg_op = 'DELETE' or new.role <> 'superadmin')
     and (select count(*) from public.user_roles where role = 'superadmin') <= 1 then
    raise exception 'cannot_remove_last_superadmin';
  end if;
  return coalesce(new, old);
end $$;
create trigger user_roles_protect_superadmin before update or delete on public.user_roles
  for each row execute function private.protect_last_superadmin();

-- Recalcula el avance de la matrícula a partir de los módulos completados.
create or replace function private.recompute_progress()
returns trigger language plpgsql security definer set search_path = '' as $$
declare
  v_enr uuid := coalesce(new.enrollment_id, old.enrollment_id);
  v_total int; v_done int;
begin
  select count(*) into v_total from public.course_modules m
    join public.enrollments e on e.course_id = m.course_id where e.id = v_enr;
  select count(*) into v_done from public.lesson_progress lp where lp.enrollment_id = v_enr and lp.module_id is not null;
  update public.enrollments
     set progress_pct = case when v_total = 0 then 0 else round(least(v_done, v_total) * 100.0 / v_total, 2) end
   where id = v_enr;
  return null;
end $$;
create trigger lesson_progress_recompute after insert or delete on public.lesson_progress
  for each row execute function private.recompute_progress();

-- ---------------------------------------------------------------------
-- 4. Operaciones expuestas (RPC) — validan en el servidor
-- ---------------------------------------------------------------------

-- Registra actividad autenticada (política de inactividad) y reactiva la cuenta
-- si estaba suspendida solo por inactividad.
create or replace function public.touch_activity()
returns text language plpgsql security definer set search_path = '' as $$
declare v_p public.profiles%rowtype;
begin
  if auth.uid() is null then raise exception 'not_authenticated' using errcode = '42501'; end if;
  select * into v_p from public.profiles where user_id = auth.uid() for update;
  if not found then raise exception 'profile_not_found'; end if;

  if v_p.status = 'suspended' and exists (
       select 1 from public.account_deletion_requests r
       where r.profile_id = v_p.id and r.reason = 'inactivity' and r.status in ('open','blocked','scheduled')) then
    update public.profiles set status = 'active', last_activity_at = now() where id = v_p.id;
    update public.student_accounts set suspended_at = null, inactivity_warning_level = 0 where profile_id = v_p.id;
    update public.account_deletion_requests set status = 'cancelled', completed_at = now()
      where profile_id = v_p.id and status in ('open','blocked','scheduled');
    perform private.log('account.reactivated', 'profiles', v_p.id::text);
    return 'active';
  end if;

  if v_p.status = 'active' and v_p.last_activity_at < now() - interval '5 minutes' then
    update public.profiles set last_activity_at = now() where id = v_p.id;
    update public.student_accounts set inactivity_warning_level = 0 where profile_id = v_p.id;
  end if;
  return v_p.status::text;
end $$;

-- Aceptación de términos y consentimiento (p. ej., tras registrarse con Google).
create or replace function public.accept_terms(p_version text, p_privacy boolean)
returns void language plpgsql security definer set search_path = '' as $$
declare v_id uuid := private.current_profile_id();
begin
  if v_id is null then raise exception 'not_allowed' using errcode = '42501'; end if;
  if p_version !~ '^[0-9A-Za-z.\-]{1,20}$' or not p_privacy then raise exception 'consent_required'; end if;
  update public.profiles set terms_version = p_version, terms_accepted_at = now(), privacy_consent_at = now()
   where id = v_id;
  perform private.log('consent.accepted', 'profiles', v_id::text, jsonb_build_object('terms_version', p_version));
end $$;

-- Matrícula en un curso gratuito publicado, con control de cupo atómico.
create or replace function public.enroll_in_course(p_course uuid)
returns uuid language plpgsql security definer set search_path = '' as $$
declare
  v_profile uuid := private.current_profile_id();
  v_c public.courses%rowtype;
  v_taken int;
  v_id uuid;
begin
  if v_profile is null then raise exception 'not_allowed' using errcode = '42501'; end if;
  if not exists (select 1 from public.profiles where id = v_profile and terms_accepted_at is not null and privacy_consent_at is not null) then
    raise exception 'consent_required';
  end if;
  select * into v_c from public.courses where id = p_course for update;
  if not found or v_c.status <> 'published' then raise exception 'course_not_available'; end if;
  if not v_c.is_free then raise exception 'payment_required'; end if;
  select id into v_id from public.enrollments where profile_id = v_profile and course_id = p_course;
  if v_id is not null then return v_id; end if;
  if v_c.capacity is not null then
    select count(*) into v_taken from public.enrollments where course_id = p_course and status <> 'cancelled';
    if v_taken >= v_c.capacity then raise exception 'course_full'; end if;
  end if;
  insert into public.enrollments (profile_id, course_id) values (v_profile, p_course) returning id into v_id;
  return v_id;
end $$;

-- Marca como leído un módulo de un curso matriculado (sincroniza con las páginas públicas).
create or replace function public.mark_module_read(p_course_slug text, p_anchor text)
returns numeric language plpgsql security definer set search_path = '' as $$
declare
  v_profile uuid := private.current_profile_id();
  v_enr uuid; v_mod uuid; v_pct numeric;
begin
  if v_profile is null then raise exception 'not_allowed' using errcode = '42501'; end if;
  select e.id into v_enr from public.enrollments e join public.courses c on c.id = e.course_id
   where c.slug = p_course_slug and e.profile_id = v_profile and e.status <> 'cancelled';
  if v_enr is null then raise exception 'not_enrolled'; end if;
  select m.id into v_mod from public.course_modules m join public.courses c on c.id = m.course_id
   where c.slug = p_course_slug and m.anchor = p_anchor;
  if v_mod is null then raise exception 'module_not_found'; end if;
  insert into public.lesson_progress (enrollment_id, module_id) values (v_enr, v_mod)
    on conflict (enrollment_id, module_id) do nothing;
  select progress_pct into v_pct from public.enrollments where id = v_enr;
  return v_pct;
end $$;

-- Historial de acceso del propio usuario (sesiones registradas por Auth).
create or replace function public.my_access_history()
returns table (started_at timestamptz, last_seen_at timestamptz, user_agent text, ip text, aal text)
language sql stable security definer set search_path = '' as $$
  select s.created_at, coalesce(s.refreshed_at::timestamptz, s.updated_at), s.user_agent, host(s.ip), s.aal::text
  from auth.sessions s where s.user_id = auth.uid()
  order by s.created_at desc limit 50;
$$;

-- Solicitud de baja por el propio estudiante.
create or replace function public.request_account_deletion()
returns uuid language plpgsql security definer set search_path = '' as $$
declare v_profile uuid := private.current_profile_id(); v_id uuid;
begin
  if v_profile is null then raise exception 'not_allowed' using errcode = '42501'; end if;
  insert into public.account_deletion_requests (profile_id, reason) values (v_profile, 'user_request')
  on conflict do nothing returning id into v_id;
  return v_id;
end $$;

-- Verificación pública de certificados: solo datos mínimos.
create or replace function public.verify_certificate(p_code text)
returns table (student_name text, course_title text, academic_hours numeric, completed_on date,
               issued_at timestamptz, status public.certificate_status)
language sql stable security definer set search_path = '' as $$
  select c.student_name, c.course_title, c.academic_hours, c.completed_on, c.issued_at, c.status
  from public.certificates c
  where c.verification_code = upper(btrim(p_code)) and length(p_code) <= 20;
$$;

-- Reconocimientos públicos: solo premios aprobados de estudiantes que lo autorizaron.
create or replace function public.public_recognitions()
returns table (student_name text, level public.award_level, period_label text)
language sql stable security definer set search_path = '' as $$
  select btrim(p.first_name || ' ' || p.last_name), a.level, a.period_label
  from public.awards a join public.profiles p on p.id = a.profile_id
  where a.status = 'approved' and p.public_recognition_consent and p.status = 'active'
  order by a.period_label desc, a.level, a.score desc;
$$;

-- Lectura de la propia cuenta, incluso antes de completar el 2FA o estando suspendido.
create or replace function public.my_account()
returns table (profile_id uuid, email text, first_name text, last_name text, status public.account_status,
               student_code text, roles public.app_role[], mfa_required boolean, consent_pending boolean)
language sql stable security definer set search_path = '' as $$
  select p.id, p.email::text, p.first_name, p.last_name, p.status, sa.student_code,
         array(select ur.role from public.user_roles ur where ur.profile_id = p.id order by ur.role),
         not private.mfa_satisfied()
           or (exists (select 1 from public.user_roles ur where ur.profile_id = p.id and ur.role <> 'student')
               and not private.staff_session()),
         p.terms_accepted_at is null or p.privacy_consent_at is null
  from public.profiles p left join public.student_accounts sa on sa.profile_id = p.id
  where p.user_id = auth.uid();
$$;

-- Permisos de ejecución
revoke execute on all functions in schema public from public, anon;
grant execute on function public.touch_activity(), public.accept_terms(text, boolean),
  public.enroll_in_course(uuid), public.mark_module_read(text, text), public.my_access_history(),
  public.request_account_deletion(), public.my_account() to authenticated;
grant execute on function public.verify_certificate(text), public.public_recognitions() to anon, authenticated;

revoke execute on all functions in schema private from public, anon, authenticated;
grant execute on function private.mfa_satisfied(), private.current_profile_id(), private.staff_session(),
  private.has_role(public.app_role), private.is_superadmin(), private.is_academic_staff(),
  private.can_manage_course(uuid), private.is_enrolled(uuid), private.instructor_sees_student(uuid)
  to authenticated;
