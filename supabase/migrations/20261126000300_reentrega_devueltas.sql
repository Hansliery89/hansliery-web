-- Permite al estudiante reemplazar una entrega devuelta para corrección (vuelve a «submitted»)
alter policy submissions_update_own on public.assignment_submissions
  using (profile_id = (select private.current_profile_id()) and status in ('submitted', 'returned'));
