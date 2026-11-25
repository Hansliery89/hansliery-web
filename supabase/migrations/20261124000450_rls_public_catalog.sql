-- =====================================================================
-- HANSLIERY ACADEMY · 0004b · Catálogo público
-- El rol anónimo no ejecuta funciones privadas: las políticas con
-- funciones quedan solo para usuarios autenticados y los visitantes
-- tienen políticas propias que solo muestran lo publicado.
-- =====================================================================
alter policy courses_select on public.courses to authenticated;
alter policy modules_select on public.course_modules to authenticated;
alter policy lessons_select on public.lessons to authenticated;

create policy courses_select_public on public.courses for select to anon using (status = 'published');
create policy modules_select_public on public.course_modules for select to anon using (
  exists (select 1 from public.courses c where c.id = course_id and c.status = 'published'));
create policy lessons_select_public on public.lessons for select to anon using (
  exists (select 1 from public.course_modules m join public.courses c on c.id = m.course_id
          where m.id = module_id and c.status = 'published'));
