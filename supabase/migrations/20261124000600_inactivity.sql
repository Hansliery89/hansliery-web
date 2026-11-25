-- =====================================================================
-- HANSLIERY ACADEMY · 0006 · Política de inactividad (100 días)
-- Avisos → suspensión → solicitud de baja → anonimización (si no hay
-- obligaciones pendientes). Nunca borra certificados, pagos ni registros
-- académicos: quedan vinculados a un perfil anonimizado.
-- =====================================================================
create extension if not exists pg_cron;

-- Motivos que impiden anonimizar una cuenta
create or replace function private.deletion_blockers(p_profile uuid)
returns text[] language sql stable security definer set search_path = '' as $$
  select array_remove(array[
    case when exists (select 1 from public.payments where profile_id = p_profile and status = 'pending') then 'pending_payment' end,
    case when exists (select 1 from public.assignment_submissions where profile_id = p_profile and status in ('submitted','in_review')) then 'submission_in_review' end,
    case when exists (select 1 from public.exam_attempts where profile_id = p_profile and status = 'submitted') then 'exam_pending_grading' end,
    case when exists (select 1 from public.scholarships where profile_id = p_profile and status = 'approved'
                      and (expires_on is null or expires_on >= current_date)) then 'active_scholarship' end,
    case when exists (select 1 from public.message_threads where profile_id = p_profile and status in ('open','pending')) then 'open_conversation' end
  ], null);
$$;

-- Anonimiza los datos personales; conserva registros académicos y financieros.
create or replace function private.anonymize_profile(p_profile uuid)
returns void language plpgsql security definer set search_path = '' as $$
begin
  update public.profiles set
    email = ('anonimo+' || replace(p_profile::text, '-', '') || '@academy.invalid'),
    first_name = 'Estudiante', last_name = 'anonimizado', phone = null, country = null, city = null,
    occupation = null, organization = null, interest_area = null, avatar_path = null,
    public_recognition_consent = false, status = 'anonymized', anonymized_at = now()
  where id = p_profile;
  update public.message_threads set status = 'archived' where profile_id = p_profile;
  delete from public.notifications where profile_id = p_profile;
  delete from storage.objects where bucket_id = 'avatars' and (storage.foldername(name))[1] = p_profile::text;
  -- La cuenta de acceso (auth.users) se elimina después con la función administrativa del servidor.
  insert into public.activity_logs (action, entity, entity_id) values ('account.anonymized', 'profiles', p_profile::text);
end $$;

create or replace function private.setting_int(p_key text, p_default int)
returns int language sql stable security definer set search_path = '' as $$
  select coalesce((select (value #>> '{}')::int from public.academy_settings where key = p_key), p_default);
$$;

create or replace function private.run_inactivity_policy()
returns jsonb language plpgsql security definer set search_path = '' as $$
declare
  v_limit  int := private.setting_int('inactivity_days', 100);
  v_grace  int := private.setting_int('anonymization_grace_days', 30);
  v_warn   int[] := coalesce((select array(select jsonb_array_elements_text(value)::int)
                              from public.academy_settings where key = 'inactivity_warning_days'), array[70,85,95]);
  r record; v_lvl int; v_blk text[];
  n_warn int := 0; n_susp int := 0; n_anon int := 0; n_block int := 0;
begin
  -- Solo estudiantes (cuentas sin rol de personal)
  for r in
    select p.id, p.status, sa.inactivity_warning_level,
           extract(day from now() - greatest(p.last_activity_at, coalesce(u.last_sign_in_at, p.last_activity_at)))::int as days
    from public.profiles p
    join public.student_accounts sa on sa.profile_id = p.id
    left join auth.users u on u.id = p.user_id
    where p.status in ('active','suspended')
      and not exists (select 1 from public.user_roles ur where ur.profile_id = p.id and ur.role <> 'student')
  loop
    if r.status = 'active' and r.days >= v_limit then
      update public.profiles set status = 'suspended' where id = r.id;
      update public.student_accounts set suspended_at = now() where profile_id = r.id;
      insert into public.account_deletion_requests (profile_id, reason, scheduled_for)
        values (r.id, 'inactivity', now() + make_interval(days => v_grace)) on conflict do nothing;
      insert into public.notifications (profile_id, kind, title, body)
        values (r.id, 'account_suspended', 'Tu cuenta fue suspendida por inactividad',
                'Inicia sesión para reactivarla antes de la fecha programada para la anonimización de tus datos.');
      insert into public.activity_logs (action, entity, entity_id, metadata)
        values ('account.suspended_inactivity', 'profiles', r.id::text, jsonb_build_object('days', r.days));
      n_susp := n_susp + 1;
    elsif r.status = 'active' then
      select coalesce(max(i), 0) into v_lvl from generate_subscripts(v_warn, 1) i where r.days >= v_warn[i];
      if v_lvl > r.inactivity_warning_level then
        update public.student_accounts set inactivity_warning_level = v_lvl where profile_id = r.id;
        insert into public.notifications (profile_id, kind, title, body)
          values (r.id, 'inactivity_warning', 'Aviso de inactividad',
                  format('Llevas %s días sin actividad. Al llegar a %s días tu cuenta será suspendida. Inicia sesión para mantenerla activa.', r.days, v_limit));
        n_warn := n_warn + 1;
      end if;
    end if;
  end loop;

  -- Anonimización de solicitudes vencidas sin obligaciones pendientes
  for r in
    select d.id, d.profile_id from public.account_deletion_requests d
    join public.profiles p on p.id = d.profile_id
    where d.status in ('open','blocked','scheduled') and d.scheduled_for <= now() and p.status = 'suspended'
  loop
    v_blk := private.deletion_blockers(r.profile_id);
    if cardinality(v_blk) > 0 then
      update public.account_deletion_requests set status = 'blocked', blocking_reasons = v_blk where id = r.id;
      n_block := n_block + 1;
    else
      perform private.anonymize_profile(r.profile_id);
      update public.account_deletion_requests set status = 'completed', completed_at = now(), blocking_reasons = '{}' where id = r.id;
      n_anon := n_anon + 1;
    end if;
  end loop;

  return jsonb_build_object('warned', n_warn, 'suspended', n_susp, 'anonymized', n_anon, 'blocked', n_block);
end $$;

revoke execute on function private.deletion_blockers(uuid), private.anonymize_profile(uuid),
  private.setting_int(text, int), private.run_inactivity_policy() from public, anon, authenticated;

-- Todos los días a las 06:15 UTC (02:15 en RD)
select cron.schedule('academy-inactivity-policy', '15 6 * * *', $$select private.run_inactivity_policy()$$);
