-- =====================================================================
-- HANSLIERY ACADEMY · Pruebas de seguridad (RLS, roles, 2FA, registro,
-- inactividad). Se ejecuta como un único bloque que SIEMPRE revierte:
-- termina con la excepción «TEST_RESULT» que contiene el informe.
-- Uso: ejecutar el archivo completo en el editor SQL de Supabase.
-- =====================================================================
create or replace function pg_temp.act(p_uid uuid, p_aal text) returns void language plpgsql as $$
begin
  perform set_config('request.jwt.claims',
    json_build_object('sub', p_uid, 'role', 'authenticated', 'aal', p_aal)::text, true);
  execute 'set local role authenticated';
end $$;
create or replace function pg_temp.anon() returns void language plpgsql as $$
begin
  perform set_config('request.jwt.claims', json_build_object('role', 'anon')::text, true);
  execute 'set local role anon';
end $$;
create or replace function pg_temp.root() returns void language plpgsql as $$
begin
  execute 'reset role';
  perform set_config('request.jwt.claims', '', true);
end $$;
create or replace function pg_temp.mkuser(p_email text, p_first text) returns uuid language plpgsql as $$
declare v uuid := gen_random_uuid();
begin
  insert into auth.users (id, instance_id, aud, role, email, encrypted_password, email_confirmed_at,
                          raw_app_meta_data, raw_user_meta_data, created_at, updated_at, last_sign_in_at)
  values (v, '00000000-0000-0000-0000-000000000000', 'authenticated', 'authenticated', p_email,
          extensions.crypt('Prueba-Segura-2026!', extensions.gen_salt('bf')), now(),
          '{"provider":"email","providers":["email"]}',
          json_build_object('first_name', p_first, 'last_name', 'Prueba', 'terms_accepted', 'true',
                            'terms_version', '2026-11', 'privacy_consent', 'true', 'phone', '+1 809 555 0101')::jsonb,
          now(), now(), now());
  return v;
end $$;

do $$
declare
  log text := '';
  n int; ok boolean; v_txt text; v_num numeric;
  u_a uuid; u_b uuid; u_i uuid; u_aa uuid; u_sa uuid; u_m uuid;
  p_a uuid; p_b uuid; p_i uuid; p_aa uuid; p_sa uuid; p_m uuid;
  c_pub uuid; c_draft uuid; v_enr uuid; v_cat uuid; v_asg uuid; v_sub uuid;
  procedure_ok int := 0;

  -- registrador
  passed int := 0; failed int := 0;
begin
  -- ---------------- Preparación (como postgres) ----------------
  u_a  := pg_temp.mkuser('Estudiante.A@Prueba.com', 'Ana');
  u_b  := pg_temp.mkuser('estudiante.b@prueba.com', 'Beto');
  u_i  := pg_temp.mkuser('instructor@prueba.com', 'Irene');
  u_aa := pg_temp.mkuser('academico@prueba.com', 'Alba');
  u_sa := pg_temp.mkuser('super@prueba.com', 'Saúl');
  u_m  := pg_temp.mkuser('conmfa@prueba.com', 'Mía');
  select id into p_a  from public.profiles where user_id = u_a;
  select id into p_b  from public.profiles where user_id = u_b;
  select id into p_i  from public.profiles where user_id = u_i;
  select id into p_aa from public.profiles where user_id = u_aa;
  select id into p_sa from public.profiles where user_id = u_sa;
  select id into p_m  from public.profiles where user_id = u_m;

  select id into c_pub from public.courses where slug = 'fundamentos-prevencion-lavado-de-activos';
  select id into c_draft from public.courses where slug = 'beneficiario-final';
  update public.courses set status = 'published', published_at = now() where id = c_pub;
  insert into public.user_roles (profile_id, role, course_id) values (p_i, 'instructor', c_pub);
  insert into public.user_roles (profile_id, role) values (p_aa, 'academic_admin'), (p_sa, 'superadmin');
  insert into auth.mfa_factors (id, user_id, friendly_name, factor_type, status, created_at, updated_at, secret)
    values (gen_random_uuid(), u_m, 'app', 'totp', 'verified', now(), now(), 'JBSWY3DPEHPK3PXP');
  select id into v_cat from public.revenue_categories where code = 'cap_curso_pago';
  insert into public.payments (category_id, profile_id, concept, product_type, amount, currency, fee_amount, method, status, reference, confirmed_at)
    values (v_cat, p_b, 'Curso pago de prueba', 'course', 1000, 'DOP', 50, 'transfer', 'confirmed', 'TRX-001', now());

  -- T01 registro: perfil, código y rol creados; correo normalizado
  select count(*) into n from public.profiles p join public.student_accounts s on s.profile_id = p.id
   join public.user_roles r on r.profile_id = p.id and r.role = 'student'
   where p.id = p_a and p.email = 'estudiante.a@prueba.com' and s.student_code like 'HSA-%' and p.terms_accepted_at is not null;
  if n = 1 then passed := passed + 1; log := log || E'\nOK  T01 alta automática de perfil, código de estudiante, rol y consentimiento';
  else failed := failed + 1; log := log || E'\nERR T01 alta automática'; end if;

  -- T02 duplicado con otra capitalización y espacios
  begin
    perform pg_temp.mkuser(' ESTUDIANTE.a@prueba.COM', 'Copia');
    failed := failed + 1; log := log || E'\nERR T02 se permitió un registro duplicado';
  exception when others then
    passed := passed + 1; log := log || E'\nOK  T02 registro duplicado rechazado (' || sqlerrm || ')';
  end;

  -- T03 el estudiante solo ve su perfil
  perform pg_temp.act(u_a, 'aal1');
  select count(*) into n from public.profiles;
  perform pg_temp.root();
  if n = 1 then passed := passed + 1; log := log || E'\nOK  T03 estudiante ve solo su perfil';
  else failed := failed + 1; log := log || E'\nERR T03 estudiante ve ' || n || ' perfiles'; end if;

  -- T04 el estudiante no puede cambiar su estado ni su correo
  begin
    perform pg_temp.act(u_a, 'aal1');
    update public.profiles set status = 'active', email = 'otro@prueba.com' where id = p_a;
    perform pg_temp.root();
    failed := failed + 1; log := log || E'\nERR T04 el estudiante modificó estado/correo';
  exception when insufficient_privilege then
    passed := passed + 1; log := log || E'\nOK  T04 estado y correo no modificables por el estudiante';
  end;

  -- T05 sí puede cambiar sus datos permitidos
  perform pg_temp.act(u_a, 'aal1');
  update public.profiles set city = 'Santiago' where id = p_a;
  get diagnostics n = row_count;
  perform pg_temp.root();
  if n = 1 then passed := passed + 1; log := log || E'\nOK  T05 estudiante actualiza sus datos permitidos';
  else failed := failed + 1; log := log || E'\nERR T05'; end if;

  -- T06 escalada de privilegios: asignarse superadmin
  begin
    perform pg_temp.act(u_a, 'aal2');
    insert into public.user_roles (profile_id, role) values (p_a, 'superadmin');
    perform pg_temp.root();
    failed := failed + 1; log := log || E'\nERR T06 el estudiante se asignó superadmin';
  exception when others then
    passed := passed + 1; log := log || E'\nOK  T06 autoasignación de roles bloqueada';
  end;

  -- T07 el estudiante no ve finanzas, bitácora, preguntas ni claves de respuesta
  perform pg_temp.act(u_a, 'aal2');
  select (select count(*) from public.payments) + (select count(*) from public.activity_logs)
       + (select count(*) from public.questions) + (select count(*) from public.answers)
       + (select count(*) from public.academy_settings) into n;
  perform pg_temp.root();
  if n = 0 then passed := passed + 1; log := log || E'\nOK  T07 sin acceso a pagos ajenos, bitácora, banco de preguntas ni configuración';
  else failed := failed + 1; log := log || E'\nERR T07 ve ' || n || ' filas restringidas'; end if;

  -- T08 matrícula en curso publicado gratuito y progreso por módulo
  perform pg_temp.act(u_a, 'aal1');
  v_enr := public.enroll_in_course(c_pub);
  v_num := public.mark_module_read('fundamentos-prevencion-lavado-de-activos', 'modulo-1');
  perform pg_temp.root();
  if v_enr is not null and v_num = 14.29 then passed := passed + 1; log := log || E'\nOK  T08 matrícula y avance (1/7 = 14.29 %)';
  else failed := failed + 1; log := log || E'\nERR T08 avance ' || coalesce(v_num::text, 'null'); end if;

  -- T09 no puede matricularse en un curso en borrador
  begin
    perform pg_temp.act(u_a, 'aal1');
    perform public.enroll_in_course(c_draft);
    perform pg_temp.root();
    failed := failed + 1; log := log || E'\nERR T09 matrícula en borrador';
  exception when others then
    passed := passed + 1; log := log || E'\nOK  T09 matrícula en curso no publicado rechazada';
  end;

  -- T10 otro estudiante no ve la matrícula ni el progreso de A
  perform pg_temp.act(u_b, 'aal1');
  select (select count(*) from public.enrollments) + (select count(*) from public.lesson_progress) into n;
  perform pg_temp.root();
  if n = 0 then passed := passed + 1; log := log || E'\nOK  T10 aislamiento entre estudiantes';
  else failed := failed + 1; log := log || E'\nERR T10'; end if;

  -- T11 el estudiante ve solo sus propios pagos
  perform pg_temp.act(u_b, 'aal1');
  select count(*), max(net_amount) into n, v_num from public.payments;
  perform pg_temp.root();
  if n = 1 and v_num = 950 then passed := passed + 1; log := log || E'\nOK  T11 estudiante ve su pago; neto = monto - comisión (950.00)';
  else failed := failed + 1; log := log || E'\nERR T11'; end if;

  -- T12 instructor sin 2FA (aal1) no ve estudiantes
  perform pg_temp.act(u_i, 'aal1');
  select count(*) into n from public.profiles where id <> p_i;
  perform pg_temp.root();
  if n = 0 then passed := passed + 1; log := log || E'\nOK  T12 instructor sin 2FA no accede a datos de estudiantes';
  else failed := failed + 1; log := log || E'\nERR T12'; end if;

  -- T13 instructor con 2FA ve solo a los estudiantes de su curso y ningún pago
  perform pg_temp.act(u_i, 'aal2');
  select count(*) into n from public.profiles where id in (p_a, p_b);
  select count(*) into procedure_ok from public.payments;
  perform pg_temp.root();
  if n = 1 and procedure_ok = 0 then passed := passed + 1; log := log || E'\nOK  T13 instructor ve solo a sus estudiantes y no ve finanzas';
  else failed := failed + 1; log := log || E'\nERR T13 perfiles=' || n || ' pagos=' || procedure_ok; end if;

  -- T14 administrador académico: todos los perfiles, ninguna finanza
  perform pg_temp.act(u_aa, 'aal2');
  select count(*) into n from public.profiles;
  select count(*) into procedure_ok from public.payments;
  perform pg_temp.root();
  if n >= 6 and procedure_ok = 0 then passed := passed + 1; log := log || E'\nOK  T14 admin académico sin privilegios financieros';
  else failed := failed + 1; log := log || E'\nERR T14'; end if;

  begin
    perform pg_temp.act(u_aa, 'aal2');
    insert into public.payments (category_id, client_name, concept, product_type, amount, currency, method, created_by)
      values (v_cat, 'Cliente', 'Intento no autorizado', 'course', 10, 'USD', 'cash', p_aa);
    perform pg_temp.root();
    failed := failed + 1; log := log || E'\nERR T15 admin académico registró un pago';
  exception when others then
    passed := passed + 1; log := log || E'\nOK  T15 admin académico no puede registrar pagos';
  end;

  -- T16 superadmin sin 2FA no ve finanzas; con 2FA sí
  perform pg_temp.act(u_sa, 'aal1');
  select count(*) into n from public.payments;
  perform pg_temp.act(u_sa, 'aal2');
  select count(*) into procedure_ok from public.payments;
  perform pg_temp.root();
  if n = 0 and procedure_ok = 1 then passed := passed + 1; log := log || E'\nOK  T16 finanzas exigen superadmin con 2FA (aal2)';
  else failed := failed + 1; log := log || E'\nERR T16 aal1=' || n || ' aal2=' || procedure_ok; end if;

  -- T17 estudiante con 2FA activado: sin verificar en la sesión no accede ni a su perfil
  perform pg_temp.act(u_m, 'aal1');
  select count(*) into n from public.profiles;
  perform pg_temp.act(u_m, 'aal2');
  select count(*) into procedure_ok from public.profiles;
  perform pg_temp.root();
  if n = 0 and procedure_ok = 1 then passed := passed + 1; log := log || E'\nOK  T17 2FA obligatorio en la sesión cuando el usuario lo activó';
  else failed := failed + 1; log := log || E'\nERR T17 aal1=' || n || ' aal2=' || procedure_ok; end if;

  -- T18 visitante anónimo: ve solo cursos publicados y no accede a perfiles
  perform pg_temp.anon();
  select count(*) into n from public.courses;
  select count(*) into procedure_ok from public.course_modules;
  perform pg_temp.root();
  if n = 1 and procedure_ok = 7 then passed := passed + 1; log := log || E'\nOK  T18 catálogo público: 1 curso publicado y sus 7 módulos';
  else failed := failed + 1; log := log || E'\nERR T18 cursos=' || n || ' modulos=' || procedure_ok; end if;
  begin
    perform pg_temp.anon();
    select count(*) into n from public.profiles;
    perform pg_temp.root();
    failed := failed + 1; log := log || E'\nERR T19 el visitante leyó perfiles';
  exception when insufficient_privilege then
    passed := passed + 1; log := log || E'\nOK  T19 visitante sin acceso a perfiles';
  end;

  -- T20 manipulación de calificación de una tarea propia
  insert into public.assignments (course_id, title, is_published, due_at) values (c_pub, 'Tarea 1', true, now() + interval '7 days') returning id into v_asg;
  perform pg_temp.act(u_a, 'aal1');
  insert into public.assignment_submissions (assignment_id, profile_id, comment) values (v_asg, p_a, 'Mi entrega') returning id into v_sub;
  begin
    update public.assignment_submissions set score = 100, graded_by = p_a, status = 'graded' where id = v_sub;
    get diagnostics n = row_count;
    perform pg_temp.root();
    if n = 0 then passed := passed + 1; log := log || E'\nOK  T20 el estudiante no puede calificarse';
    else failed := failed + 1; log := log || E'\nERR T20 el estudiante se calificó'; end if;
  exception when others then
    perform pg_temp.root();
    passed := passed + 1; log := log || E'\nOK  T20 el estudiante no puede calificarse (' || sqlerrm || ')';
  end;

  -- T21 verificación pública de certificados (datos mínimos)
  insert into public.certificates (verification_code, profile_id, course_id, student_name, course_title, completed_on)
    values ('HS-ABCD-EFGH-JKLM', p_a, c_pub, 'Ana Prueba', 'Fundamentos', current_date);
  perform pg_temp.anon();
  select count(*) into n from public.verify_certificate('hs-abcd-efgh-jklm');
  select count(*) into procedure_ok from public.verify_certificate('HS-0000-0000-0000');
  perform pg_temp.root();
  if n = 1 and procedure_ok = 0 then passed := passed + 1; log := log || E'\nOK  T21 verificador público de certificados';
  else failed := failed + 1; log := log || E'\nERR T21'; end if;

  -- T22 inactividad: aviso a los 71 días y suspensión a los 101
  update public.profiles set last_activity_at = now() - interval '71 days' where id = p_a;
  update auth.users set last_sign_in_at = now() - interval '71 days' where id = u_a;
  update public.profiles set last_activity_at = now() - interval '101 days' where id = p_b;
  update auth.users set last_sign_in_at = now() - interval '101 days' where id = u_b;
  v_txt := private.run_inactivity_policy()::text;
  select count(*) into n from public.profiles where id = p_b and status = 'suspended';
  select count(*) into procedure_ok from public.notifications where profile_id = p_a and kind = 'inactivity_warning';
  if n = 1 and procedure_ok = 1 then passed := passed + 1; log := log || E'\nOK  T22 aviso preventivo y suspensión a los 100 días ' || v_txt;
  else failed := failed + 1; log := log || E'\nERR T22 ' || v_txt; end if;

  -- T23 el suspendido no accede a datos; al volver se reactiva
  perform pg_temp.act(u_b, 'aal1');
  select count(*) into n from public.payments;
  v_txt := public.touch_activity();
  select count(*) into procedure_ok from public.payments;
  perform pg_temp.root();
  if n = 0 and v_txt = 'active' and procedure_ok = 1 then passed := passed + 1; log := log || E'\nOK  T23 cuenta suspendida bloqueada y reactivada al iniciar sesión';
  else failed := failed + 1; log := log || E'\nERR T23 ' || n || '/' || v_txt || '/' || procedure_ok; end if;

  -- T24 baja con obligaciones pendientes: bloqueada (A tiene una tarea en revisión)
  update public.profiles set last_activity_at = now() - interval '101 days' where id = p_a;
  update auth.users set last_sign_in_at = now() - interval '101 days' where id = u_a;
  perform private.run_inactivity_policy();
  update public.account_deletion_requests set scheduled_for = now() - interval '1 minute' where profile_id = p_a;
  perform private.run_inactivity_policy();
  select count(*) into n from public.account_deletion_requests where profile_id = p_a and status = 'blocked' and 'submission_in_review' = any(blocking_reasons);
  if n = 1 then passed := passed + 1; log := log || E'\nOK  T24 anonimización bloqueada por obligación académica pendiente';
  else failed := failed + 1; log := log || E'\nERR T24'; end if;

  -- T25 sin obligaciones: anonimiza y conserva el certificado
  update public.assignment_submissions set status = 'graded', score = 90, graded_at = now() where id = v_sub;
  perform private.run_inactivity_policy();
  select count(*) into n from public.profiles where id = p_a and status = 'anonymized' and first_name = 'Estudiante' and phone is null;
  select count(*) into procedure_ok from public.certificates where profile_id = p_a and status = 'valid';
  if n = 1 and procedure_ok = 1 then passed := passed + 1; log := log || E'\nOK  T25 datos anonimizados; certificado y registros conservados';
  else failed := failed + 1; log := log || E'\nERR T25 anon=' || n || ' cert=' || procedure_ok; end if;

  -- T26 no se puede retirar el último superadministrador
  begin
    delete from public.user_roles where profile_id = p_sa and role = 'superadmin';
    failed := failed + 1; log := log || E'\nERR T26 se eliminó el último superadmin';
  exception when others then
    passed := passed + 1; log := log || E'\nOK  T26 último superadministrador protegido';
  end;

  -- T27 bitácora registró operaciones
  select count(*) into n from public.activity_logs where action in ('account.created','payments.insert','user_roles.insert','account.suspended_inactivity','account.reactivated','account.anonymized');
  if n >= 10 then passed := passed + 1; log := log || E'\nOK  T27 bitácora con ' || n || ' eventos de auditoría';
  else failed := failed + 1; log := log || E'\nERR T27 ' || n; end if;

  raise exception 'TEST_RESULT passed=% failed=% %', passed, failed, log;
end $$;
