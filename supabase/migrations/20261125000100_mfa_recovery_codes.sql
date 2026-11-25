-- =====================================================================
-- HANSLIERY ACADEMY · 0008 · Códigos de recuperación del doble factor
-- Supabase Auth no ofrece códigos de recuperación: se guardan aquí como
-- hash SHA-256 (nunca en claro) y se consumen desde la función del
-- servidor «mfa-recover», que elimina los factores con la API de admin.
-- =====================================================================
create table private.mfa_recovery_codes (
  id         bigint generated always as identity primary key,
  user_id    uuid not null references auth.users(id) on delete cascade,
  code_hash  text not null,
  created_at timestamptz not null default now(),
  used_at    timestamptz,
  unique (user_id, code_hash)
);
create table private.mfa_recovery_attempts (
  id         bigint generated always as identity primary key,
  user_id    uuid not null references auth.users(id) on delete cascade,
  ok         boolean not null,
  created_at timestamptz not null default now()
);
create index mfa_recovery_attempts_idx on private.mfa_recovery_attempts (user_id, created_at desc);
revoke all on private.mfa_recovery_codes, private.mfa_recovery_attempts from public, anon, authenticated;

create or replace function private.hash_code(p_code text)
returns text language sql immutable set search_path = '' as $$
  select encode(extensions.digest(upper(regexp_replace(coalesce(p_code, ''), '[^A-Za-z0-9]', '', 'g')), 'sha256'), 'hex');
$$;

-- Genera 10 códigos nuevos (invalida los anteriores). Exige sesión con 2FA verificado.
create or replace function public.generate_recovery_codes()
returns setof text language plpgsql volatile security definer set search_path = '' as $$
declare
  v_uid uuid := auth.uid();
  v_alpha text := 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  v_code text; v_bytes bytea; i int; j int;
begin
  if v_uid is null or coalesce(auth.jwt() ->> 'aal', '') <> 'aal2' then
    raise exception 'mfa_required' using errcode = '42501';
  end if;
  update private.mfa_recovery_codes set used_at = now() where user_id = v_uid and used_at is null;  -- invalida los anteriores
  for i in 1..10 loop
    v_bytes := extensions.gen_random_bytes(8);
    v_code := '';
    for j in 0..7 loop
      v_code := v_code || substr(v_alpha, (get_byte(v_bytes, j) % 32) + 1, 1);
      if j = 3 then v_code := v_code || '-'; end if;
    end loop;
    insert into private.mfa_recovery_codes (user_id, code_hash) values (v_uid, private.hash_code(v_code));
    return next v_code;
  end loop;
  perform private.log('mfa.recovery_codes_generated', 'auth.users', v_uid::text);
end $$;

create or replace function public.recovery_codes_remaining()
returns int language sql stable security definer set search_path = '' as $$
  select count(*)::int from private.mfa_recovery_codes where user_id = auth.uid() and used_at is null;
$$;

-- Consumo: solo la función del servidor (service_role). Máximo 5 intentos fallidos en 15 minutos.
create or replace function public.consume_recovery_code(p_user uuid, p_code text)
returns boolean language plpgsql volatile security definer set search_path = '' as $$
declare v_id bigint;
begin
  if (select count(*) from private.mfa_recovery_attempts
      where user_id = p_user and not ok and created_at > now() - interval '15 minutes') >= 5 then
    raise exception 'too_many_attempts' using errcode = '42501';
  end if;
  update private.mfa_recovery_codes set used_at = now()
   where id = (select id from private.mfa_recovery_codes
               where user_id = p_user and used_at is null and code_hash = private.hash_code(p_code)
               limit 1 for update)
  returning id into v_id;
  insert into private.mfa_recovery_attempts (user_id, ok) values (p_user, v_id is not null);
  insert into public.activity_logs (actor_user_id, action, entity, entity_id, metadata)
    values (p_user, case when v_id is null then 'mfa.recovery_failed' else 'mfa.recovery_used' end, 'auth.users', p_user::text, '{}');
  return v_id is not null;
end $$;

revoke execute on function private.hash_code(text) from public, anon, authenticated;
revoke execute on function public.generate_recovery_codes(), public.recovery_codes_remaining(),
  public.consume_recovery_code(uuid, text) from public, anon, authenticated;
grant execute on function public.generate_recovery_codes(), public.recovery_codes_remaining() to authenticated;
grant execute on function public.consume_recovery_code(uuid, text) to service_role;

-- Los 13 cursos ya son gratuitos y públicos en el portal: se publican en la Academy como gratuitos.
update public.courses set status = 'published', is_free = true, published_at = coalesce(published_at, now())
 where status = 'draft';
