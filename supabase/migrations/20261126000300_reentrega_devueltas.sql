-- Permite al estudiante reemplazar una entrega devuelta para corrección (vuelve a «submitted»)
alter policy submissions_update_own on public.assignment_submissions
  using (profile_id = (select private.current_profile_id()) and status in ('submitted', 'returned'));

-- Al reentregar, se limpian los datos de la corrección anterior (la política exige graded_by nulo)
create or replace function private.submission_resubmit()
returns trigger language plpgsql security definer set search_path = '' as $$
begin
  if old.status = 'returned' and new.status = 'submitted' and new.profile_id = private.current_profile_id() then
    new.graded_by := null; new.graded_at := null; new.score := null; new.submitted_at := now();
  end if;
  return new;
end $$;
revoke all on function private.submission_resubmit() from public, anon, authenticated;
create trigger submissions_resubmit before update on public.assignment_submissions
  for each row execute function private.submission_resubmit();
