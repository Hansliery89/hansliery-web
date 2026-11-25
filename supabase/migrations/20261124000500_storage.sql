-- =====================================================================
-- HANSLIERY ACADEMY · 0005 · Almacenamiento privado con validación de
-- tamaño y tipo. Ruta: <propietario>/<...>. Ningún bucket es público.
-- =====================================================================
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types) values
  ('avatars',             'avatars',             false, 2097152,  array['image/jpeg','image/png','image/webp']),
  ('submissions',         'submissions',         false, 20971520, array['application/pdf','image/jpeg','image/png',
                            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']),
  ('course-materials',    'course-materials',    false, 52428800, array['application/pdf','image/jpeg','image/png','video/mp4',
                            'application/vnd.openxmlformats-officedocument.presentationml.presentation']),
  ('message-attachments', 'message-attachments', false, 10485760, array['application/pdf','image/jpeg','image/png']),
  ('certificates',        'certificates',        false, 5242880,  array['application/pdf']),
  ('payment-evidence',    'payment-evidence',    false, 10485760, array['application/pdf','image/jpeg','image/png'])
on conflict (id) do nothing;

-- Primer segmento de la ruta como uuid (o null si no lo es)
create or replace function private.path_uuid(p_name text, p_pos int)
returns uuid language plpgsql immutable set search_path = '' as $$
begin
  return (storage.foldername(p_name))[p_pos]::uuid;
exception when others then
  return null;
end $$;
grant execute on function private.path_uuid(text, int) to authenticated;

-- avatars/<profile_id>/archivo
create policy avatars_read on storage.objects for select to authenticated using (
  bucket_id = 'avatars' and (private.path_uuid(name, 1) = private.current_profile_id() or private.is_academic_staff()));
create policy avatars_write on storage.objects for insert to authenticated with check (
  bucket_id = 'avatars' and private.path_uuid(name, 1) = private.current_profile_id());
create policy avatars_update on storage.objects for update to authenticated using (
  bucket_id = 'avatars' and private.path_uuid(name, 1) = private.current_profile_id());
create policy avatars_delete on storage.objects for delete to authenticated using (
  bucket_id = 'avatars' and private.path_uuid(name, 1) = private.current_profile_id());

-- submissions/<profile_id>/<assignment_id>/archivo
create policy submissions_read on storage.objects for select to authenticated using (
  bucket_id = 'submissions' and (
    private.path_uuid(name, 1) = private.current_profile_id()
    or exists (select 1 from public.assignments a where a.id = private.path_uuid(name, 2) and private.can_manage_course(a.course_id))));
create policy submissions_write on storage.objects for insert to authenticated with check (
  bucket_id = 'submissions' and private.path_uuid(name, 1) = private.current_profile_id()
  and exists (select 1 from public.assignments a where a.id = private.path_uuid(name, 2) and a.is_published and private.is_enrolled(a.course_id)));

-- course-materials/<course_id>/archivo
create policy materials_read on storage.objects for select to authenticated using (
  bucket_id = 'course-materials' and (private.is_enrolled(private.path_uuid(name, 1)) or private.can_manage_course(private.path_uuid(name, 1))));
create policy materials_write on storage.objects for insert to authenticated with check (
  bucket_id = 'course-materials' and private.can_manage_course(private.path_uuid(name, 1)));
create policy materials_delete on storage.objects for delete to authenticated using (
  bucket_id = 'course-materials' and private.can_manage_course(private.path_uuid(name, 1)));

-- message-attachments/<thread_id>/archivo
create policy msg_files_read on storage.objects for select to authenticated using (
  bucket_id = 'message-attachments' and exists (select 1 from public.message_threads t where t.id = private.path_uuid(name, 1) and (
    t.profile_id = private.current_profile_id() or private.is_academic_staff()
    or (t.course_id is not null and private.can_manage_course(t.course_id)))));
create policy msg_files_write on storage.objects for insert to authenticated with check (
  bucket_id = 'message-attachments' and exists (select 1 from public.message_threads t where t.id = private.path_uuid(name, 1)
    and t.status <> 'archived' and (t.profile_id = private.current_profile_id() or private.is_academic_staff()
    or (t.course_id is not null and private.can_manage_course(t.course_id)))));

-- certificates/<profile_id>/archivo.pdf — escritura solo por funciones del servidor
create policy certificates_read on storage.objects for select to authenticated using (
  bucket_id = 'certificates' and (private.path_uuid(name, 1) = private.current_profile_id() or private.is_academic_staff()));

-- payment-evidence — solo superadministrador
create policy evidence_all on storage.objects for all to authenticated
  using (bucket_id = 'payment-evidence' and private.is_superadmin())
  with check (bucket_id = 'payment-evidence' and private.is_superadmin());
