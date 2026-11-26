-- =====================================================================
-- HANSLIERY ACADEMY · Pruebas de las fases 4 a 9 (exámenes, certificados,
-- centro de control, finanzas, becas, reconocimientos, mensajería).
-- Un único bloque que SIEMPRE revierte: termina con «TEST_RESULT».
-- =====================================================================
create or replace function pg_temp.act(p_uid uuid, p_aal text) returns void language plpgsql as $$
begin
  perform set_config('request.jwt.claims', json_build_object('sub', p_uid, 'role', 'authenticated', 'aal', p_aal)::text, true);
  execute 'set local role authenticated';
end $$;
create or replace function pg_temp.anon() returns void language plpgsql as $$
begin
  perform set_config('request.jwt.claims', json_build_object('role', 'anon')::text, true);
  execute 'set local role anon';
end $$;
create or replace function pg_temp.root() returns void language plpgsql as $$
begin execute 'reset role'; perform set_config('request.jwt.claims', '', true); end $$;
create or replace function pg_temp.mkuser(p_email text, p_first text) returns uuid language plpgsql as $$
declare v uuid := gen_random_uuid();
begin
  insert into auth.users (id, instance_id, aud, role, email, encrypted_password, email_confirmed_at,
                          raw_app_meta_data, raw_user_meta_data, created_at, updated_at, last_sign_in_at)
  values (v, '00000000-0000-0000-0000-000000000000', 'authenticated', 'authenticated', p_email, 'x', now(),
          '{"provider":"email","providers":["email"]}',
          json_build_object('first_name', p_first, 'last_name', 'Prueba', 'terms_accepted', 'true',
                            'terms_version', '2026-11', 'privacy_consent', 'true')::jsonb, now(), now(), now());
  return v;
end $$;
create temp table res (n serial, name text, ok boolean, info text);
create or replace function pg_temp.t(p_name text, p_ok boolean, p_info text default null) returns void language sql as $$
  insert into res (name, ok, info) values (p_name, coalesce(p_ok, false), p_info);
$$;

do $$
declare
  u_a uuid; u_b uuid; u_i uuid; u_aa uuid; u_sa uuid;
  p_a uuid; p_b uuid; p_i uuid; p_aa uuid; p_sa uuid;
  c1 uuid; c_paid uuid; v_exam uuid; v_enr uuid; v_att uuid; j jsonb; resp jsonb; v_txt text; v_code text; v_cat uuid;
  v_sch uuid; v_aw uuid; v_th uuid; v_asg uuid; v_sub uuid; n int;
begin
  u_a := pg_temp.mkuser('fa@prueba.com', 'Ana'); u_b := pg_temp.mkuser('fb@prueba.com', 'Beto');
  u_i := pg_temp.mkuser('fi@prueba.com', 'Irene'); u_aa := pg_temp.mkuser('faa@prueba.com', 'Alba'); u_sa := pg_temp.mkuser('fsa@prueba.com', 'Saúl');
  select id into p_a from public.profiles where user_id = u_a; select id into p_b from public.profiles where user_id = u_b;
  select id into p_i from public.profiles where user_id = u_i; select id into p_aa from public.profiles where user_id = u_aa;
  select id into p_sa from public.profiles where user_id = u_sa;
  select id into c1 from public.courses where slug = 'beneficiario-final';
  select id into v_exam from public.exams where course_id = c1 and is_certification;
  insert into public.user_roles (profile_id, role, course_id) values (p_i, 'instructor', c1), (p_aa, 'academic_admin', null), (p_sa, 'superadmin', null);
  insert into public.courses (slug, title, status, is_free, price_dop) values ('curso-pago-prueba', 'Curso de pago (prueba)', 'published', false, 5000) returning id into c_paid;
  insert into public.course_modules (course_id, position, title, anchor) values (c_paid, 1, 'Único', 'modulo-1');
  select id into v_cat from public.revenue_categories limit 1;

  -- ---------- Fase 4/5: progreso y examen ----------
  perform pg_temp.act(u_a, 'aal1'); v_enr := public.enroll_in_course(c1); perform pg_temp.root();
  begin perform pg_temp.act(u_a, 'aal1'); perform public.start_exam(v_exam); v_txt := 'ok'; exception when others then v_txt := sqlerrm; end; perform pg_temp.root();
  perform pg_temp.t('examen bloqueado sin completar módulos', v_txt = 'course_not_completed', v_txt);
  insert into public.lesson_progress (enrollment_id, module_id) select v_enr, m.id from public.course_modules m where m.course_id = c1;
  perform pg_temp.t('100 % de módulos completa la matrícula', (select status = 'completed' and progress_pct = 100 and completed_at is not null from public.enrollments where id = v_enr));

  perform pg_temp.act(u_a, 'aal1'); j := public.start_exam(v_exam); perform pg_temp.root();
  v_att := (j ->> 'attempt_id')::uuid;
  perform pg_temp.t('el examen no expone respuestas correctas', position('is_correct' in j::text) = 0 and jsonb_array_length(j -> 'questions') > 5);
  perform pg_temp.act(u_a, 'aal1'); select count(*) into n from public.answers; perform pg_temp.root();
  perform pg_temp.t('el estudiante no lee la tabla de respuestas', n = 0, n::text);
  perform pg_temp.act(u_a, 'aal1'); j := public.start_exam(v_exam); perform pg_temp.root();
  perform pg_temp.t('reabrir devuelve el mismo intento', (j ->> 'attempt_id')::uuid = v_att);

  begin perform pg_temp.act(u_b, 'aal1'); perform public.submit_exam(v_att, '{}'); v_txt := 'ok'; exception when others then v_txt := sqlerrm; end; perform pg_temp.root();
  perform pg_temp.t('otro estudiante no entrega un intento ajeno', v_txt = 'not_allowed', v_txt);

  select jsonb_object_agg(q.id::text, jsonb_build_array(a.id::text)) into resp
    from unnest((select question_ids from public.exam_attempts where id = v_att)) q(id) join public.answers a on a.question_id = q.id and a.is_correct;
  resp := resp || jsonb_build_object('no-es-uuid', 'x');
  perform pg_temp.act(u_a, 'aal1'); j := public.submit_exam(v_att, resp); perform pg_temp.root();
  perform pg_temp.t('calificación en servidor: 100 % y aprobado', (j ->> 'score_pct')::numeric = 100 and (j ->> 'passed')::boolean, j::text);
  perform pg_temp.t('solo se guardan respuestas de preguntas del intento', not ((select responses from public.exam_attempts where id = v_att) ? 'no-es-uuid'));
  begin perform pg_temp.act(u_a, 'aal1'); perform public.start_exam(v_exam); v_txt := 'ok'; exception when others then v_txt := sqlerrm; end; perform pg_temp.root();
  perform pg_temp.t('no se repite un examen aprobado', v_txt = 'exam_already_passed', v_txt);

  -- ---------- Certificados ----------
  begin perform pg_temp.act(u_a, 'aal1'); perform public.issue_certificate(v_enr); v_txt := 'ok'; exception when others then v_txt := sqlerrm; end; perform pg_temp.root();
  perform pg_temp.t('el estudiante no emite certificados', v_txt = 'not_allowed', v_txt);
  perform pg_temp.act(u_aa, 'aal1'); select count(*) into n from public.certificate_queue(); perform pg_temp.root();
  perform pg_temp.t('sin 2FA el personal no ve la cola', n = 0, n::text);
  perform pg_temp.act(u_i, 'aal2'); select count(*) into n from public.certificate_queue() where enrollment_id = v_enr; perform pg_temp.root();
  perform pg_temp.t('el instructor del curso ve la cola', n = 1, n::text);
  perform pg_temp.act(u_i, 'aal2'); v_code := public.issue_certificate(v_enr); perform pg_temp.root();
  perform pg_temp.t('código con formato HS-XXXX-XXXX-XXXX', v_code ~ '^HS-[A-HJ-NP-Z2-9]{4}-[A-HJ-NP-Z2-9]{4}-[A-HJ-NP-Z2-9]{4}$', v_code);
  perform pg_temp.t('emisión notifica al estudiante', exists (select 1 from public.notifications where profile_id = p_a and kind = 'certificate_issued'));
  begin perform pg_temp.act(u_aa, 'aal2'); perform public.issue_certificate(v_enr); v_txt := 'ok'; exception when others then v_txt := sqlerrm; end; perform pg_temp.root();
  perform pg_temp.t('no se emite dos veces', v_txt like 'requirements_not_met%already_issued%', v_txt);
  perform pg_temp.anon(); select count(*) into n from public.certificate_public(v_code) where grade_pct = 100; perform pg_temp.root();
  perform pg_temp.t('verificación pública con calificación', n = 1);
  begin perform pg_temp.act(u_aa, 'aal2'); perform public.revoke_certificate(v_code, 'Prueba de revocación'); v_txt := 'ok'; exception when others then v_txt := sqlerrm; end; perform pg_temp.root();
  perform pg_temp.t('solo superadmin revoca', v_txt = 'not_allowed', v_txt);
  perform pg_temp.act(u_sa, 'aal2'); perform public.revoke_certificate(v_code, 'Prueba de revocación'); perform pg_temp.root();
  perform pg_temp.t('revocación registrada', (select status = 'revoked' from public.certificates where verification_code = v_code));

  -- ---------- Centro de control y finanzas ----------
  begin perform pg_temp.act(u_a, 'aal1'); perform public.admin_overview(); v_txt := 'ok'; exception when others then v_txt := sqlerrm; end; perform pg_temp.root();
  perform pg_temp.t('estudiante sin acceso al resumen', v_txt = 'not_allowed', v_txt);
  begin perform pg_temp.act(u_aa, 'aal1'); perform public.admin_overview(); v_txt := 'ok'; exception when others then v_txt := sqlerrm; end; perform pg_temp.root();
  perform pg_temp.t('personal sin 2FA sin acceso al resumen', v_txt = 'not_allowed', v_txt);
  perform pg_temp.act(u_aa, 'aal2'); j := public.admin_overview(); perform pg_temp.root();
  perform pg_temp.t('admin académico ve el resumen sin datos de pagos', j ? 'students' and (j ->> 'payments_pending') is null);
  begin perform pg_temp.act(u_aa, 'aal2'); perform public.finance_summary('2026-01-01', '2026-12-31'); v_txt := 'ok'; exception when others then v_txt := sqlerrm; end; perform pg_temp.root();
  perform pg_temp.t('finanzas solo para superadmin', v_txt = 'not_allowed', v_txt);
  perform pg_temp.act(u_aa, 'aal2'); select count(*) into n from public.payments; perform pg_temp.root();
  perform pg_temp.t('admin académico no lee pagos', n = 0);

  begin perform pg_temp.act(u_b, 'aal1'); perform public.enroll_in_course(c_paid); v_txt := 'ok'; exception when others then v_txt := sqlerrm; end; perform pg_temp.root();
  perform pg_temp.t('curso de pago no se auto-matricula', v_txt = 'payment_required', v_txt);

  perform pg_temp.act(u_aa, 'aal2'); v_sch := public.propose_scholarship(p_b, null, '2026-S2', 'Prueba', current_date + 30); perform pg_temp.root();
  begin
    perform pg_temp.act(u_sa, 'aal2');
    insert into public.payments (category_id, profile_id, concept, product_type, course_id, occurred_on, amount, currency, method, status, scholarship_id, created_by)
    values (v_cat, p_b, 'Curso de pago', 'course', c_paid, current_date, 2500, 'DOP', 'transfer', 'pending', v_sch, p_sa);
    v_txt := 'ok'; exception when others then v_txt := sqlerrm; end; perform pg_temp.root();
  perform pg_temp.t('beca propuesta (sin aprobar) no se aplica', v_txt = 'scholarship_invalid', v_txt);
  begin perform pg_temp.act(u_aa, 'aal2'); perform public.review_scholarship(v_sch, true); v_txt := 'ok'; exception when others then v_txt := sqlerrm; end; perform pg_temp.root();
  perform pg_temp.t('solo superadmin aprueba becas', v_txt = 'not_allowed', v_txt);
  perform pg_temp.act(u_sa, 'aal2'); perform public.review_scholarship(v_sch, true);
  insert into public.payments (category_id, profile_id, concept, product_type, course_id, occurred_on, amount, discount_amount, currency, method, status, confirmed_at, scholarship_id, created_by)
  values (v_cat, p_b, 'Curso de pago', 'course', c_paid, current_date, 2500, 2500, 'DOP', 'transfer', 'confirmed', now(), v_sch, p_sa);
  j := public.finance_summary(current_date - 1, current_date + 1); perform pg_temp.root();
  perform pg_temp.t('pago confirmado matricula al estudiante', exists (select 1 from public.enrollments where profile_id = p_b and course_id = c_paid and payment_id is not null));
  perform pg_temp.t('beca marcada como utilizada', (select status = 'used' from public.scholarships where id = v_sch));
  perform pg_temp.t('confirmado_por asignado automáticamente', exists (select 1 from public.payments where profile_id = p_b and confirmed_by = p_sa));
  perform pg_temp.t('resumen financiero por moneda', (j -> 'totals' -> 0 ->> 'currency') = 'DOP' and (j -> 'totals' -> 0 ->> 'gross')::numeric >= 2500, j -> 'totals' ->> 0);
  perform pg_temp.act(u_b, 'aal1'); update public.scholarships set status = 'approved' where id = v_sch; get diagnostics n = row_count; perform pg_temp.root();
  perform pg_temp.t('estudiante no modifica becas', n = 0);

  -- ---------- Reconocimientos ----------
  perform pg_temp.act(u_aa, 'aal2'); n := public.compute_award_candidates('2026-PRUEBA', current_date - 1, current_date + 1); perform pg_temp.root();
  select id into v_aw from public.awards where profile_id = p_a and period_label = '2026-PRUEBA';
  perform pg_temp.t('candidato calculado (no aprobado)', v_aw is not null and (select status = 'candidate' from public.awards where id = v_aw), n::text);
  begin perform pg_temp.act(u_aa, 'aal2'); perform public.review_award(v_aw, true); v_txt := 'ok'; exception when others then v_txt := sqlerrm; end; perform pg_temp.root();
  perform pg_temp.t('solo superadmin aprueba reconocimientos', v_txt = 'not_allowed', v_txt);
  perform pg_temp.act(u_sa, 'aal2'); perform public.review_award(v_aw, true); perform pg_temp.root();
  perform pg_temp.t('constancia generada al aprobar', (select constancia_code like 'HSR-%' from public.awards where id = v_aw));

  -- ---------- Mensajería y avisos ----------
  perform pg_temp.act(u_a, 'aal1');
  insert into public.message_threads (profile_id, subject, status) values (p_a, 'Consulta de prueba', 'open') returning id into v_th;
  insert into public.messages (thread_id, sender_profile_id, body) values (v_th, p_a, 'Hola, tengo una duda.');
  perform pg_temp.root();
  perform pg_temp.t('mensaje del estudiante deja la consulta pendiente', (select status = 'pending' from public.message_threads where id = v_th));
  perform pg_temp.act(u_b, 'aal1'); select count(*) into n from public.messages where thread_id = v_th; perform pg_temp.root();
  perform pg_temp.t('otro estudiante no lee la consulta', n = 0);
  perform pg_temp.act(u_aa, 'aal2'); insert into public.messages (thread_id, sender_profile_id, body) values (v_th, p_aa, 'Respuesta.'); perform pg_temp.root();
  perform pg_temp.t('respuesta del personal: respondida y notificada', (select status = 'answered' from public.message_threads where id = v_th)
    and exists (select 1 from public.notifications where profile_id = p_a and kind = 'message_reply'));
  begin perform pg_temp.act(u_i, 'aal2'); perform public.admin_send_announcement(null, 'Aviso general', 'x'); v_txt := 'ok'; exception when others then v_txt := sqlerrm; end; perform pg_temp.root();
  perform pg_temp.t('instructor no envía avisos generales', v_txt = 'not_allowed', v_txt);
  perform pg_temp.act(u_i, 'aal2'); n := public.admin_send_announcement(c1, 'Aviso del curso', 'Contenido'); perform pg_temp.root();
  perform pg_temp.t('aviso a los matriculados del curso', n >= 1 and exists (select 1 from public.notifications where profile_id = p_a and kind = 'announcement'), n::text);
  begin perform pg_temp.act(u_sa, 'aal2'); perform public.job_pending_emails(10); v_txt := 'ok'; exception when others then v_txt := sqlstate; end; perform pg_temp.root();
  perform pg_temp.t('funciones de tareas no accesibles para usuarios', v_txt = '42501', v_txt);

  -- ---------- Asignaciones devueltas ----------
  perform pg_temp.act(u_i, 'aal2');
  insert into public.assignments (course_id, title, max_score, is_published) values (c1, 'Tarea de prueba', 10, true) returning id into v_asg;
  perform pg_temp.root();
  perform pg_temp.act(u_a, 'aal1');
  insert into public.assignment_submissions (assignment_id, profile_id, comment, status) values (v_asg, p_a, 'Mi entrega', 'submitted') returning id into v_sub;
  perform pg_temp.root();
  perform pg_temp.act(u_i, 'aal2'); update public.assignment_submissions set status = 'returned', feedback = 'Corrige', graded_by = p_i, graded_at = now() where id = v_sub; perform pg_temp.root();
  perform pg_temp.act(u_a, 'aal1'); update public.assignment_submissions set status = 'submitted', comment = 'Corregida' where id = v_sub; get diagnostics n = row_count; perform pg_temp.root();
  perform pg_temp.t('el estudiante reentrega una tarea devuelta', n = 1 and exists (select 1 from public.notifications where profile_id = p_a and kind = 'submission_returned'));
  begin perform pg_temp.act(u_a, 'aal1'); update public.assignment_submissions set score = 10 where id = v_sub; v_txt := 'ok'; exception when others then v_txt := sqlstate; end; perform pg_temp.root();
  perform pg_temp.t('el estudiante no se califica', v_txt = '42501' and (select score is null from public.assignment_submissions where id = v_sub), v_txt);

  -- ---------- Cuentas ----------
  begin perform pg_temp.act(u_aa, 'aal2'); perform public.admin_set_account_status(p_b, 'suspended', 'x'); v_txt := 'ok'; exception when others then v_txt := sqlerrm; end; perform pg_temp.root();
  perform pg_temp.t('solo superadmin suspende cuentas', v_txt = 'not_allowed', v_txt);
  perform pg_temp.act(u_sa, 'aal2'); perform public.admin_set_account_status(p_b, 'suspended', 'Prueba'); perform pg_temp.root();
  perform pg_temp.t('suspensión aplicada', (select status = 'suspended' from public.profiles where id = p_b));

  raise exception 'TEST_RESULT passed=% failed=% %', (select count(*) from res where ok), (select count(*) from res where not ok),
    coalesce((select string_agg(r.n || ' ' || r.name || coalesce(' [' || r.info || ']', ''), ' | ') from res r where not r.ok), 'sin fallos');
end $$;
