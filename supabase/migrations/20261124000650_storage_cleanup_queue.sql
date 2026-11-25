-- =====================================================================
-- HANSLIERY ACADEMY · 0006b · Limpieza de archivos por cola
-- Supabase prohíbe borrar archivos de Storage con SQL (protect_delete).
-- La anonimización encola la ruta y una función del servidor la borra
-- con la API de Storage.
-- =====================================================================
create table private.storage_cleanup_queue (
  id          bigint generated always as identity primary key,
  bucket_id   text not null,
  prefix      text not null,
  reason      text not null,
  created_at  timestamptz not null default now(),
  processed_at timestamptz
);
revoke all on private.storage_cleanup_queue from public, anon, authenticated;

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
  insert into private.storage_cleanup_queue (bucket_id, prefix, reason)
    values ('avatars', p_profile::text || '/', 'anonymization');
  insert into public.activity_logs (action, entity, entity_id) values ('account.anonymized', 'profiles', p_profile::text);
end $$;
revoke execute on function private.anonymize_profile(uuid) from public, anon, authenticated;
