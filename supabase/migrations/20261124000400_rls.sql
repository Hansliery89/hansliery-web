-- =====================================================================
-- HANSLIERY ACADEMY · 0004 · Row Level Security y privilegios mínimos
-- Principio: nada es accesible salvo lo que una política permite.
-- El personal (superadmin, admin académico, instructor) requiere sesión aal2.
-- =====================================================================

-- 1. Cerrar todo por defecto
revoke all on all tables in schema public from anon, authenticated;
revoke all on all sequences in schema public from anon, authenticated;
alter default privileges in schema public revoke all on tables from anon, authenticated;
alter default privileges in schema public revoke execute on functions from public, anon, authenticated;

do $$
declare t text;
begin
  for t in select tablename from pg_tables where schemaname = 'public' loop
    execute format('alter table public.%I enable row level security', t);
  end loop;
end $$;

-- 2. Privilegios por tabla (las políticas filtran las filas)
-- Perfiles: el estudiante solo puede cambiar sus datos permitidos.
grant select on public.profiles to authenticated;
grant update (first_name, last_name, phone, country, city, occupation, organization, interest_area,
              avatar_path, public_recognition_consent) on public.profiles to authenticated;

grant select on public.student_accounts to authenticated;
grant update (onboarding_completed, tutorial_seen) on public.student_accounts to authenticated;

grant select, insert, delete on public.user_roles to authenticated;

grant select on public.courses, public.course_modules, public.lessons to anon, authenticated;
grant insert, update, delete on public.courses, public.course_modules, public.lessons to authenticated;

grant select, insert, update on public.enrollments to authenticated;           -- insert/update: solo personal (política)
grant select, insert, delete on public.lesson_progress to authenticated;

grant select, insert, update, delete on public.exams, public.questions, public.answers to authenticated;
grant select on public.exam_attempts to authenticated;                         -- escritura: solo funciones del servidor
grant update (manual_score, score_pct, passed, feedback, graded_by, graded_at, status) on public.exam_attempts to authenticated;

grant select, insert, update, delete on public.assignments to authenticated;
grant select, insert on public.assignment_submissions to authenticated;
grant update (file_path, comment, status, score, feedback, graded_by, graded_at) on public.assignment_submissions to authenticated;

grant select on public.certificates to authenticated;                          -- emisión: solo funciones del servidor
grant update (status, revoked_reason) on public.certificates to authenticated;

grant select, insert, update on public.revenue_categories to authenticated;
grant select, insert, update on public.payments to authenticated;
grant select, insert, update on public.awards, public.scholarships to authenticated;

grant select, insert, update on public.message_threads to authenticated;
grant select, insert on public.messages to authenticated;
grant update (read_at) on public.messages to authenticated;
grant select, insert on public.notifications to authenticated;
grant update (read_at) on public.notifications to authenticated;

grant select on public.activity_logs to authenticated;                         -- inserción: solo funciones internas
grant select, update on public.account_deletion_requests to authenticated;
grant select, insert, update on public.academy_settings to authenticated;

-- 3. Políticas -------------------------------------------------------

-- profiles
create policy profiles_select on public.profiles for select to authenticated using (
  id = (select private.current_profile_id())
  or (select private.is_academic_staff())
  or (select private.instructor_sees_student(profiles.id)));
create policy profiles_update_own on public.profiles for update to authenticated
  using (id = (select private.current_profile_id()))
  with check (id = (select private.current_profile_id()));

-- student_accounts
create policy student_accounts_select on public.student_accounts for select to authenticated using (
  profile_id = (select private.current_profile_id()) or (select private.is_academic_staff()));
create policy student_accounts_update_own on public.student_accounts for update to authenticated
  using (profile_id = (select private.current_profile_id()))
  with check (profile_id = (select private.current_profile_id()));

-- user_roles: cada quien ve los suyos; solo el superadministrador asigna o retira.
create policy user_roles_select on public.user_roles for select to authenticated using (
  profile_id = (select private.current_profile_id()) or (select private.is_superadmin()));
create policy user_roles_insert on public.user_roles for insert to authenticated
  with check ((select private.is_superadmin()));
create policy user_roles_delete on public.user_roles for delete to authenticated
  using ((select private.is_superadmin()));

-- courses, módulos y lecciones: publicados para todos; gestión por personal o instructor asignado.
create policy courses_select on public.courses for select to anon, authenticated using (
  status = 'published' or (select private.can_manage_course(courses.id)));
create policy courses_insert on public.courses for insert to authenticated with check ((select private.is_academic_staff()));
create policy courses_update on public.courses for update to authenticated
  using ((select private.can_manage_course(courses.id))) with check ((select private.can_manage_course(courses.id)));
create policy courses_delete on public.courses for delete to authenticated using ((select private.is_academic_staff()));

create policy modules_select on public.course_modules for select to anon, authenticated using (
  exists (select 1 from public.courses c where c.id = course_id and c.status = 'published')
  or (select private.can_manage_course(course_id)));
create policy modules_write on public.course_modules for all to authenticated
  using ((select private.can_manage_course(course_id))) with check ((select private.can_manage_course(course_id)));

create policy lessons_select on public.lessons for select to anon, authenticated using (
  exists (select 1 from public.course_modules m join public.courses c on c.id = m.course_id
          where m.id = module_id and (c.status = 'published' or private.can_manage_course(c.id))));
create policy lessons_write on public.lessons for all to authenticated
  using (exists (select 1 from public.course_modules m where m.id = module_id and private.can_manage_course(m.course_id)))
  with check (exists (select 1 from public.course_modules m where m.id = module_id and private.can_manage_course(m.course_id)));

-- enrollments: el estudiante ve las suyas; se matricula vía enroll_in_course(); el personal gestiona.
create policy enrollments_select on public.enrollments for select to authenticated using (
  profile_id = (select private.current_profile_id()) or (select private.can_manage_course(course_id)));
create policy enrollments_insert_staff on public.enrollments for insert to authenticated
  with check ((select private.is_academic_staff()));
create policy enrollments_update_staff on public.enrollments for update to authenticated
  using ((select private.is_academic_staff())) with check ((select private.is_academic_staff()));

-- lesson_progress
create policy progress_select on public.lesson_progress for select to authenticated using (
  exists (select 1 from public.enrollments e where e.id = enrollment_id
          and (e.profile_id = private.current_profile_id() or private.can_manage_course(e.course_id))));
create policy progress_insert_own on public.lesson_progress for insert to authenticated with check (
  exists (select 1 from public.enrollments e where e.id = enrollment_id
          and e.profile_id = private.current_profile_id() and e.status = 'active'));
create policy progress_delete_staff on public.lesson_progress for delete to authenticated using (
  exists (select 1 from public.enrollments e where e.id = enrollment_id and private.is_academic_staff()));

-- exams: el estudiante matriculado ve exámenes publicados; preguntas y claves solo el personal.
create policy exams_select on public.exams for select to authenticated using (
  (status = 'published' and (course_id is null or private.is_enrolled(course_id)))
  or (course_id is not null and private.can_manage_course(course_id))
  or (select private.is_academic_staff()));
create policy exams_write on public.exams for all to authenticated
  using ((select private.is_academic_staff()) or (course_id is not null and private.can_manage_course(course_id)))
  with check ((select private.is_academic_staff()) or (course_id is not null and private.can_manage_course(course_id)));

create policy questions_staff on public.questions for all to authenticated
  using (exists (select 1 from public.exams x where x.id = exam_id
                 and (private.is_academic_staff() or (x.course_id is not null and private.can_manage_course(x.course_id)))))
  with check (exists (select 1 from public.exams x where x.id = exam_id
                 and (private.is_academic_staff() or (x.course_id is not null and private.can_manage_course(x.course_id)))));
create policy answers_staff on public.answers for all to authenticated
  using (exists (select 1 from public.questions q join public.exams x on x.id = q.exam_id where q.id = question_id
                 and (private.is_academic_staff() or (x.course_id is not null and private.can_manage_course(x.course_id)))))
  with check (exists (select 1 from public.questions q join public.exams x on x.id = q.exam_id where q.id = question_id
                 and (private.is_academic_staff() or (x.course_id is not null and private.can_manage_course(x.course_id)))));

-- exam_attempts: lectura propia o del personal del curso; calificación manual por el personal.
create policy attempts_select on public.exam_attempts for select to authenticated using (
  profile_id = (select private.current_profile_id())
  or exists (select 1 from public.exams x where x.id = exam_id
             and (private.is_academic_staff() or (x.course_id is not null and private.can_manage_course(x.course_id)))));
create policy attempts_grade on public.exam_attempts for update to authenticated
  using (status in ('submitted','graded') and exists (select 1 from public.exams x where x.id = exam_id
         and (private.is_academic_staff() or (x.course_id is not null and private.can_manage_course(x.course_id)))))
  with check (graded_by = private.current_profile_id() and exists (select 1 from public.exams x where x.id = exam_id
         and (private.is_academic_staff() or (x.course_id is not null and private.can_manage_course(x.course_id)))));

-- assignments
create policy assignments_select on public.assignments for select to authenticated using (
  (is_published and private.is_enrolled(course_id)) or private.can_manage_course(course_id));
create policy assignments_write on public.assignments for all to authenticated
  using (private.can_manage_course(course_id)) with check (private.can_manage_course(course_id));

-- assignment_submissions: el estudiante entrega y corrige mientras no esté en revisión; el personal califica.
create policy submissions_select on public.assignment_submissions for select to authenticated using (
  profile_id = (select private.current_profile_id())
  or exists (select 1 from public.assignments a where a.id = assignment_id and private.can_manage_course(a.course_id)));
create policy submissions_insert_own on public.assignment_submissions for insert to authenticated with check (
  profile_id = (select private.current_profile_id()) and status = 'submitted' and score is null and graded_by is null
  and exists (select 1 from public.assignments a where a.id = assignment_id and a.is_published and private.is_enrolled(a.course_id)));
create policy submissions_update_own on public.assignment_submissions for update to authenticated
  using (profile_id = (select private.current_profile_id()) and status = 'submitted')
  with check (profile_id = (select private.current_profile_id()) and status = 'submitted' and score is null and graded_by is null);
create policy submissions_grade on public.assignment_submissions for update to authenticated
  using (exists (select 1 from public.assignments a where a.id = assignment_id and private.can_manage_course(a.course_id)))
  with check (graded_by = private.current_profile_id()
              and exists (select 1 from public.assignments a where a.id = assignment_id and private.can_manage_course(a.course_id)));

-- certificates: propios o personal académico (revocación). Emisión solo por el servidor.
create policy certificates_select on public.certificates for select to authenticated using (
  profile_id = (select private.current_profile_id()) or (select private.is_academic_staff()));
create policy certificates_revoke on public.certificates for update to authenticated
  using ((select private.is_superadmin())) with check ((select private.is_superadmin()));

-- Finanzas: solo superadministrador. El estudiante ve únicamente sus propios pagos.
create policy revenue_categories_admin on public.revenue_categories for all to authenticated
  using ((select private.is_superadmin())) with check ((select private.is_superadmin()));
create policy payments_select on public.payments for select to authenticated using (
  (select private.is_superadmin()) or profile_id = (select private.current_profile_id()));
create policy payments_insert on public.payments for insert to authenticated with check (
  (select private.is_superadmin()) and created_by = private.current_profile_id()
  and (status = 'pending' or confirmed_by = private.current_profile_id()));
create policy payments_update on public.payments for update to authenticated
  using ((select private.is_superadmin())) with check ((select private.is_superadmin()));

-- Reconocimientos: el admin académico propone; solo el superadministrador aprueba.
create policy awards_select on public.awards for select to authenticated using (
  profile_id = (select private.current_profile_id()) or (select private.is_academic_staff()));
create policy awards_insert on public.awards for insert to authenticated with check (
  (select private.is_academic_staff()) and status = 'candidate');
create policy awards_update on public.awards for update to authenticated
  using ((select private.is_academic_staff()))
  with check ((select private.is_superadmin()) or status = 'candidate');

create policy scholarships_select on public.scholarships for select to authenticated using (
  profile_id = (select private.current_profile_id()) or (select private.is_academic_staff()));
create policy scholarships_insert on public.scholarships for insert to authenticated with check (
  (select private.is_academic_staff()) and status = 'proposed' and approved_by is null);
create policy scholarships_update on public.scholarships for update to authenticated
  using ((select private.is_superadmin())) with check ((select private.is_superadmin()));

-- Mensajería: cada estudiante solo sus conversaciones; personal académico todas; instructor las de su curso.
create policy threads_select on public.message_threads for select to authenticated using (
  profile_id = (select private.current_profile_id()) or (select private.is_academic_staff())
  or (course_id is not null and private.can_manage_course(course_id)));
create policy threads_insert_own on public.message_threads for insert to authenticated with check (
  profile_id = (select private.current_profile_id()) and status = 'open');
create policy threads_update_staff on public.message_threads for update to authenticated
  using ((select private.is_academic_staff()) or (course_id is not null and private.can_manage_course(course_id)))
  with check ((select private.is_academic_staff()) or (course_id is not null and private.can_manage_course(course_id)));

create policy messages_select on public.messages for select to authenticated using (
  exists (select 1 from public.message_threads t where t.id = thread_id and (
    t.profile_id = private.current_profile_id() or private.is_academic_staff()
    or (t.course_id is not null and private.can_manage_course(t.course_id)))));
create policy messages_insert on public.messages for insert to authenticated with check (
  sender_profile_id = (select private.current_profile_id())
  and exists (select 1 from public.message_threads t where t.id = thread_id and t.status <> 'archived' and (
    t.profile_id = private.current_profile_id() or private.is_academic_staff()
    or (t.course_id is not null and private.can_manage_course(t.course_id)))));
create policy messages_mark_read on public.messages for update to authenticated using (
  exists (select 1 from public.message_threads t where t.id = thread_id and (
    t.profile_id = private.current_profile_id() or private.is_academic_staff()
    or (t.course_id is not null and private.can_manage_course(t.course_id)))));

-- Notificaciones: propias; el personal académico puede emitir.
create policy notifications_select on public.notifications for select to authenticated using (
  profile_id = (select private.current_profile_id()) or (select private.is_academic_staff()));
create policy notifications_insert_staff on public.notifications for insert to authenticated with check (
  (select private.is_academic_staff()) and created_by = private.current_profile_id());
create policy notifications_mark_read on public.notifications for update to authenticated
  using (profile_id = (select private.current_profile_id()))
  with check (profile_id = (select private.current_profile_id()));

-- Bitácora: solo superadministrador (el estudiante ve su historial con my_access_history()).
create policy activity_logs_select on public.activity_logs for select to authenticated using ((select private.is_superadmin()));

-- Bajas
create policy deletion_select on public.account_deletion_requests for select to authenticated using (
  profile_id = (select private.current_profile_id()) or (select private.is_academic_staff()));
create policy deletion_update_admin on public.account_deletion_requests for update to authenticated
  using ((select private.is_superadmin())) with check ((select private.is_superadmin()));

-- Configuración: personal académico lee; superadministrador modifica.
create policy settings_select on public.academy_settings for select to authenticated using ((select private.is_academic_staff()));
create policy settings_write on public.academy_settings for insert to authenticated with check ((select private.is_superadmin()));
create policy settings_update on public.academy_settings for update to authenticated
  using ((select private.is_superadmin())) with check ((select private.is_superadmin()));
