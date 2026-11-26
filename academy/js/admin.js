/* =================================================================
   ACADEMY · Centro de control (personal académico y administración)
   El servidor decide qué puede ver y hacer cada rol (RLS y funciones);
   esta interfaz solo oculta lo que el rol no puede usar.
   ================================================================= */
(function () {
  'use strict';
  var H = window.HSA; if (!H) return;
  var sb = H.sb, $ = H.$, $$ = H.$$, esc = H.esc;
  var st = $('#ad-status');
  var ME = null, IS_SUPER = false, IS_ACAD = false, COURSES = [], LOADED = {};
  var ROLE = { superadmin: 'Superadministrador', academic_admin: 'Administrador académico', instructor: 'Instructor', student: 'Estudiante' };

  // ---------------- Utilidades ----------------
  var ERR = {
    requirements_not_met: 'El estudiante aún no cumple los requisitos (módulos completos y evaluación final aprobada).',
    scholarship_cap_reached: 'Ya se alcanzó el número máximo de becas aprobadas para ese período.',
    award_not_approved: 'La beca debe vincularse a un reconocimiento aprobado de ese estudiante.',
    scholarship_invalid: 'La beca seleccionada no está aprobada, venció o no pertenece al estudiante.',
    invalid_score: 'La puntuación manual está fuera del rango permitido.',
    reason_required: 'Indica el motivo (mínimo 5 caracteres).',
    cannot_change_own_status: 'No puedes cambiar el estado de tu propia cuenta.',
    last_superadmin: 'Debe quedar al menos un superadministrador.',
    account_not_active: 'La cuenta del estudiante no está activa.',
    duplicate: 'Ya existe un registro con esos datos.',
    payments_refund_le_amount: 'El reembolso más la comisión no puede superar el monto.',
    payments_party: 'Indica el estudiante o el nombre del cliente.'
  };
  function msg(e) {
    var m = String((e && (e.message || e.details)) || '');
    for (var k in ERR) if (m.indexOf(k) > -1) return ERR[k];
    if (e && e.code === '23505') return ERR.duplicate;
    return H.message(e);
  }
  function fail(e, box) { H.status(box || st, msg(e), 'error'); }
  function ok(text, box) { H.status(box || st, text, 'ok'); }
  function empty(t) { return '<p class="ac-empty">' + esc(t) + '</p>'; }
  function d(v, time) { return v ? H.fmtDate(v, time) : '—'; }
  function n(v, dec) { return v == null ? '—' : Number(v).toLocaleString('es-DO', { minimumFractionDigits: dec || 0, maximumFractionDigits: dec == null ? 1 : dec }); }
  function money(v, cur) { return v == null ? '—' : esc(cur || '') + ' ' + Number(v).toLocaleString('es-DO', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
  function tag(t, kind) { return '<span class="ac-tag' + (kind ? ' is-' + kind : '') + '">' + esc(t) + '</span>'; }
  function btn(label, attrs, ghost) { return '<button class="btn ' + (ghost === false ? 'btn-primary' : 'btn-ghost') + ' btn-sm" type="button" ' + attrs + '>' + esc(label) + '</button>'; }
  function table(head, rows, emptyText) {
    if (!rows.length) return empty(emptyText || 'Sin registros.');
    return '<div class="ac-table-wrap"><table class="ac-table"><thead><tr>' + head.map(function (h) { return '<th scope="col">' + esc(h) + '</th>'; }).join('') +
      '</tr></thead><tbody>' + rows.map(function (r) { return '<tr>' + r.map(function (c) { return '<td>' + (c == null ? '—' : c) + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody></table></div>';
  }
  function card(title, body, extra) {
    return '<div class="ac-card"><div class="ac-section-title"><h2>' + esc(title) + '</h2>' + (extra || '') + '</div>' + body + '</div>';
  }
  function options(list, val, blank) {
    return (blank != null ? '<option value="">' + esc(blank) + '</option>' : '') + list.map(function (o) {
      var v = Array.isArray(o) ? o[0] : o, l = Array.isArray(o) ? o[1] : o;
      return '<option value="' + esc(v) + '"' + (String(val) === String(v) ? ' selected' : '') + '>' + esc(l) + '</option>';
    }).join('');
  }
  function field(id, label, input, full) { return '<div class="field' + (full ? ' full' : '') + '"><label for="' + id + '">' + esc(label) + '</label>' + input + '<span class="error"></span></div>'; }
  function inp(id, val, attrs) { return '<input class="control" id="' + id + '" value="' + esc(val == null ? '' : val) + '" ' + (attrs || '') + '>'; }
  function area(id, val, rows) { return '<textarea class="control" id="' + id + '" rows="' + (rows || 3) + '">' + esc(val || '') + '</textarea>'; }
  function chk(id, label, on) { return '<label class="ac-check"><input type="checkbox" id="' + id + '"' + (on ? ' checked' : '') + '> <span>' + esc(label) + '</span></label>'; }
  function val(id) { var e = $('#' + id); return e ? e.value.trim() : ''; }
  function numOrNull(id) { var v = val(id); return v === '' ? null : Number(v); }
  function isoLocal(v) { if (!v) return ''; var x = new Date(v); x.setMinutes(x.getMinutes() - x.getTimezoneOffset()); return x.toISOString().slice(0, 16); }
  function csv(name, head, rows) {
    var q = function (v) { v = v == null ? '' : String(v); if (/^[=+\-@]/.test(v)) v = "'" + v; return '"' + v.replace(/"/g, '""') + '"'; };
    var blob = new Blob(['﻿' + [head].concat(rows).map(function (r) { return r.map(q).join(','); }).join('\r\n')], { type: 'text/csv;charset=utf-8' });
    var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  }
  function on(root, sel, fn) { $$(sel, root).forEach(function (b) { b.addEventListener('click', function (e) { fn(b.dataset, b, e); }); }); }
  function fullName(p) { return p ? esc(((p.first_name || '') + ' ' + (p.last_name || '')).trim()) : '—'; }
  async function signed(bucket, path) {
    var u = await sb.storage.from(bucket).createSignedUrl(path, 300);
    if (u.error) { fail(u.error); return; } window.open(u.data.signedUrl, '_blank', 'noopener');
  }
  function safeName(f) { return f.name.normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^\w.\-]+/g, '_').slice(-80); }

  // Diálogo genérico
  var dlg = $('#dlg-admin'), dlBody = $('#dl-body'), dlSt = $('#dl-status');
  function openDlg(title, html) { $('#dl-title').textContent = title; dlBody.innerHTML = html; H.status(dlSt, ''); if (!dlg.open) dlg.showModal(); return dlBody; }
  function closeDlg() { dlg.close(); }
  $('#dl-close').addEventListener('click', closeDlg);

  // ---------------- Navegación ----------------
  var tabs = [];
  function go(sec, focus) {
    tabs.forEach(function (t) {
      var onp = t.dataset.sec === sec;
      t.setAttribute('aria-selected', onp ? 'true' : 'false'); t.tabIndex = onp ? 0 : -1;
      $('#sec-' + t.dataset.sec).hidden = !onp;
      if (onp && focus) t.focus();
    });
    if (history.replaceState) history.replaceState(null, '', '#' + sec);
    H.status(st, '');
    if (LOAD[sec]) LOAD[sec]($('#sec-' + sec));
  }

  // ---------------- Arranque ----------------
  (async function init() {
    var s = await sb.auth.getSession();
    if (!s.data.session) { location.replace(H.base + 'index.html'); return; }
    var lv = await H.aal();
    var acc = await sb.rpc('my_account');
    $('#ad-loading').hidden = true;
    if (acc.error || !acc.data || !acc.data.length) { fail(acc.error); return; }
    ME = acc.data[0];
    var roles = (ME.roles || []).filter(function (r) { return r !== 'student'; });
    if (!roles.length) { H.status(st, 'Tu cuenta no tiene acceso al centro de control.', 'error'); return; }
    if (lv.currentLevel !== 'aal2') {
      H.status(st, 'Para entrar al centro de control debes activar y usar la verificación en dos pasos. Actívala en «Seguridad» de tu panel y vuelve a iniciar sesión.', 'error'); return;
    }
    IS_SUPER = roles.indexOf('superadmin') > -1;
    IS_ACAD = IS_SUPER || roles.indexOf('academic_admin') > -1;
    $('#ad-role').textContent = (ME.first_name ? ME.first_name + ' · ' : '') + roles.map(function (r) { return ROLE[r]; }).join(', ');
    $$('.ac-nav [role=tab]').forEach(function (t) {
      var need = t.dataset.need;
      if ((need === 'super' && !IS_SUPER) || (need === 'academic' && !IS_ACAD)) { t.remove(); $('#sec-' + t.dataset.sec).remove(); }
    });
    tabs = $$('.ac-nav [role=tab]');
    tabs.forEach(function (t, i) {
      t.id = 'tab-' + t.dataset.sec; $('#sec-' + t.dataset.sec).setAttribute('aria-labelledby', t.id);
      t.addEventListener('click', function () { go(t.dataset.sec); });
      t.addEventListener('keydown', function (e) {
        var k = e.key, x = null;
        if (k === 'ArrowDown' || k === 'ArrowRight') x = tabs[(i + 1) % tabs.length];
        if (k === 'ArrowUp' || k === 'ArrowLeft') x = tabs[(i - 1 + tabs.length) % tabs.length];
        if (x) { e.preventDefault(); go(x.dataset.sec, true); }
      });
    });
    var c = await sb.from('courses').select('id,title,slug,status').order('title');
    COURSES = c.data || [];
    $('#ad-app').hidden = false;
    var initial = (location.hash || '').slice(1);
    go(tabs.some(function (t) { return t.dataset.sec === initial; }) ? initial : 'resumen');
  })();
  sb.auth.onAuthStateChange(function (ev) { if (ev === 'SIGNED_OUT') location.replace(H.base + 'index.html'); });
  $('#ad-signout').addEventListener('click', function () { sb.auth.signOut(); });

  function courseOpts(val, blank) { return options(COURSES.map(function (c) { return [c.id, c.title]; }), val, blank); }

  async function runJobs(btnEl, box) {
    H.busy(btnEl, true, 'Ejecutando…');
    var r = await sb.functions.invoke('academy-jobs', { body: { tasks: ['cleanup', 'email'] } });
    H.busy(btnEl, false);
    if (r.error) { fail(r.error, box); return; }
    var x = r.data || {}, cl = x.cleanup || {}, em = x.email || {};
    ok('Mantenimiento ejecutado. Archivos eliminados: ' + (cl.files_removed || 0) + '; usuarios eliminados de Auth: ' + (cl.auth_users_deleted || 0) +
      '; correo: ' + (em.status === 'disabled' ? 'desactivado (se habilita con el dominio y el proveedor de correo)' : (em.sent || 0) + ' enviados') + '.', box);
  }

  // ================= SECCIONES =================
  var LOAD = {};

  // ---------- Resumen ----------
  LOAD.resumen = async function (root) {
    root.innerHTML = '<div class="ac-loading">Cargando…</div>';
    var o = await sb.rpc('admin_overview'), cs = await sb.rpc('admin_course_stats');
    if (o.error) { root.innerHTML = ''; fail(o.error); return; }
    var k = o.data || {};
    var kpi = function (v, l, sec) { return v == null ? '' : '<button type="button" class="ac-kpi ac-kpi-btn"' + (sec ? ' data-go="' + sec + '"' : ' disabled') + '><b>' + n(v, 0) + '</b><span>' + esc(l) + '</span></button>'; };
    root.innerHTML =
      '<div class="ac-kpis ac-kpis-6">' + kpi(k.students, 'Estudiantes', IS_ACAD && 'estudiantes') + kpi(k.students_active_30d, 'Activos (30 días)', IS_ACAD && 'estudiantes') +
      kpi(k.enrollments, 'Matrículas') + kpi(k.completed, 'Cursos finalizados') + kpi(k.certificates, 'Certificados vigentes', 'certificados') + kpi(k.suspended, 'Cuentas suspendidas', IS_ACAD && 'estudiantes') + '</div>' +
      card('Pendientes', '<div class="ac-kpis ac-kpis-6" style="margin-top:1rem">' +
        kpi(k.certificate_queue, 'Certificados por emitir', 'certificados') + kpi(k.attempts_to_grade, 'Exámenes por calificar', 'evaluaciones') +
        kpi(k.submissions_to_grade, 'Entregas por calificar', 'asignaciones') + kpi(k.threads_pending, 'Consultas sin responder', 'mensajes') +
        kpi(k.award_candidates, 'Candidatos a reconocimiento', IS_ACAD && 'reconocimientos') + kpi(k.scholarships_proposed, 'Becas propuestas', IS_ACAD && 'reconocimientos') +
        kpi(k.payments_pending, 'Pagos por confirmar', IS_SUPER && 'finanzas') + kpi(k.deletion_requests, 'Solicitudes de baja', IS_SUPER && 'cuentas') + '</div>') +
      card('Rendimiento por curso', table(['Curso', 'Estado', 'Matrículas', 'Finalizados', 'Avance promedio', 'Aprobación de exámenes', 'Certificados'],
        (cs.data || []).map(function (c) {
          return [esc(c.title), tag(c.status === 'published' ? 'Publicado' : c.status === 'draft' ? 'Borrador' : 'Archivado', c.status === 'published' ? 'ok' : ''),
            n(c.enrollments, 0), n(c.completed, 0), c.avg_progress == null ? '—' : n(c.avg_progress) + ' %', c.pass_rate == null ? '—' : n(c.pass_rate) + ' %', n(c.certificates, 0)];
        }), 'No hay cursos a tu cargo.'),
        '<button class="btn btn-ghost btn-sm" type="button" id="rs-csv">Exportar CSV</button>') +
      (IS_SUPER ? card('Mantenimiento', '<p class="ac-muted" style="margin-top:.5rem">Se ejecuta solo cada 15 minutos: borra archivos de cuentas anonimizadas, elimina sus usuarios de Auth y envía los correos pendientes cuando el proveedor de correo esté configurado.</p><div class="ac-actions">' +
        btn('Ejecutar ahora', 'id="rs-jobs"') + '</div><div class="ac-status" id="rs-jobs-st" aria-live="polite"></div>') : '');
    on(root, '[data-go]', function (ds) { go(ds.go, true); });
    var cb = $('#rs-csv', root); if (cb) cb.addEventListener('click', function () {
      csv('cursos.csv', ['Curso', 'Estado', 'Matrículas', 'Finalizados', 'Avance promedio', 'Aprobación', 'Certificados'],
        (cs.data || []).map(function (c) { return [c.title, c.status, c.enrollments, c.completed, c.avg_progress, c.pass_rate, c.certificates]; }));
    });
    var jb = $('#rs-jobs', root); if (jb) jb.addEventListener('click', function () { runJobs(jb, $('#rs-jobs-st')); });
  };

  // ---------- Estudiantes ----------
  var STATUS = { active: 'Activa', suspended: 'Suspendida', pending_deletion: 'Baja en curso', anonymized: 'Anonimizada' };
  LOAD.estudiantes = async function (root) {
    if (!LOADED.est) {
      root.innerHTML = card('Estudiantes', '<form class="ac-inline" id="es-f" role="search"><label class="sr-only" for="es-q">Buscar estudiante</label>' +
        inp('es-q', '', 'placeholder="Nombre, correo o código" maxlength="80"') + '<button class="btn btn-primary btn-sm" type="submit">Buscar</button>' +
        btn('Exportar CSV', 'id="es-csv"') + '</form><div id="es-list"></div>');
      $('#es-f').addEventListener('submit', function (e) { e.preventDefault(); listStudents(); });
      $('#es-csv').addEventListener('click', function () {
        csv('estudiantes.csv', ['Código', 'Nombre', 'Correo', 'Estado', 'País', 'Institución', 'Matrículas', 'Finalizados', 'Certificados', 'Última actividad', 'Registro'],
          (LOADED.students || []).map(function (s) { return [s.student_code, s.full_name, s.email, s.status, s.country, s.organization, s.enrollments, s.completed, s.certificates, s.last_activity_at, s.created_at]; }));
      });
      LOADED.est = true;
    }
    listStudents();
  };
  async function listStudents() {
    var r = await sb.rpc('admin_student_list', { p_search: val('es-q') || null });
    if (r.error) { fail(r.error); return; }
    LOADED.students = r.data || [];
    var box = $('#es-list');
    box.innerHTML = table(['Código', 'Nombre', 'Correo', 'Estado', 'Cursos', 'Finalizados', 'Certificados', 'Última actividad', ''],
      LOADED.students.map(function (s) {
        return [esc(s.student_code || 'Personal'), esc(s.full_name), esc(s.email), tag(STATUS[s.status] || s.status, s.status === 'active' ? 'ok' : ''),
          n(s.enrollments, 0), n(s.completed, 0), n(s.certificates, 0), d(s.last_activity_at), btn('Ver', 'data-st="' + esc(s.profile_id) + '"')];
      }), 'No se encontraron personas.');
    on(box, '[data-st]', function (ds) { studentDetail(ds.st); });
  }
  async function studentDetail(id) {
    var s = (LOADED.students || []).find(function (x) { return x.profile_id === id; }) || {};
    var p = await sb.from('profiles').select('first_name,last_name,email,phone,country,city,occupation,organization,interest_area,status,created_at,terms_accepted_at').eq('id', id).single();
    var e = await sb.from('enrollments').select('id,status,progress_pct,enrolled_at,completed_at,courses(title)').eq('profile_id', id).order('enrolled_at', { ascending: false });
    if (p.error) { fail(p.error); return; }
    var x = p.data;
    var body = openDlg(((x.first_name || '') + ' ' + (x.last_name || '')).trim() || 'Estudiante',
      '<table class="ac-table"><tbody>' + [['Código', s.student_code || '—'], ['Correo', x.email], ['Teléfono', x.phone], ['País / ciudad', [x.country, x.city].filter(Boolean).join(' · ')],
        ['Ocupación', x.occupation], ['Institución', x.organization], ['Interés', x.interest_area], ['Estado', STATUS[x.status]], ['Registro', d(x.created_at)], ['Términos aceptados', d(x.terms_accepted_at)]]
        .map(function (r) { return '<tr><th scope="row">' + esc(r[0]) + '</th><td>' + esc(r[1] || '—') + '</td></tr>'; }).join('') + '</tbody></table>' +
      '<h3 style="margin-top:1.2rem">Matrículas</h3>' + table(['Curso', 'Estado', 'Avance', 'Matrícula', 'Finalización', ''], (e.data || []).map(function (m) {
        return [esc(m.courses ? m.courses.title : ''), esc({ active: 'Activa', completed: 'Finalizada', cancelled: 'Cancelada' }[m.status]), n(m.progress_pct) + ' %', d(m.enrolled_at), d(m.completed_at),
          m.status !== 'cancelled' ? btn('Cancelar', 'data-cancel="' + esc(m.id) + '"') : btn('Reactivar', 'data-react="' + esc(m.id) + '"')];
      }), 'Sin matrículas.') +
      '<form class="ac-inline" id="sd-enr" style="margin-top:1rem"><label class="sr-only" for="sd-course">Curso</label><select class="control" id="sd-course">' + courseOpts('', 'Matricular en…') + '</select>' +
      '<button class="btn btn-primary btn-sm" type="submit">Matricular</button></form>' +
      (IS_SUPER && x.status !== 'anonymized' && id !== ME.profile_id ? '<div class="ac-actions">' + (x.status === 'active' ? btn('Suspender cuenta', 'id="sd-susp"') : btn('Reactivar cuenta', 'id="sd-act"', false)) + '</div>' : ''));
    on(body, '[data-cancel]', async function (ds) {
      if (!confirm('¿Cancelar esta matrícula? El avance se conserva.')) return;
      var r = await sb.from('enrollments').update({ status: 'cancelled' }).eq('id', ds.cancel); if (r.error) { fail(r.error, dlSt); return; } studentDetail(id);
    });
    on(body, '[data-react]', async function (ds) {
      var r = await sb.from('enrollments').update({ status: 'active' }).eq('id', ds.react); if (r.error) { fail(r.error, dlSt); return; } studentDetail(id);
    });
    $('#sd-enr').addEventListener('submit', async function (ev) {
      ev.preventDefault(); var c = val('sd-course'); if (!c) return;
      var r = await sb.from('enrollments').insert({ profile_id: id, course_id: c }); if (r.error) { fail(r.error, dlSt); return; } studentDetail(id);
    });
    var setStatus = async function (status) {
      var reason = prompt(status === 'suspended' ? 'Motivo de la suspensión (se notificará al estudiante):' : 'Mensaje para el estudiante (opcional):', '');
      if (reason === null) return;
      var r = await sb.rpc('admin_set_account_status', { p_profile: id, p_status: status, p_reason: reason });
      if (r.error) { fail(r.error, dlSt); return; } listStudents(); studentDetail(id);
    };
    if ($('#sd-susp')) $('#sd-susp').addEventListener('click', function () { setStatus('suspended'); });
    if ($('#sd-act')) $('#sd-act').addEventListener('click', function () { setStatus('active'); });
  }

  // ---------- Cursos ----------
  LOAD.cursos = async function (root) {
    var r = await sb.rpc('admin_course_stats');
    if (r.error) { fail(r.error); return; }
    root.innerHTML = card('Cursos', table(['Curso', 'Estado', 'Matrículas', 'Finalizados', 'Avance promedio', 'Evaluaciones', ''], (r.data || []).map(function (c) {
      return [esc(c.title), tag({ published: 'Publicado', draft: 'Borrador', archived: 'Archivado' }[c.status], c.status === 'published' ? 'ok' : ''), n(c.enrollments, 0), n(c.completed, 0),
        c.avg_progress == null ? '—' : n(c.avg_progress) + ' %', n(c.exams, 0), btn('Editar', 'data-ed="' + esc(c.course_id) + '"') + ' ' + btn('Módulos y materiales', 'data-mod="' + esc(c.course_id) + '"')];
    }), 'No hay cursos a tu cargo.'), IS_ACAD ? btn('Nuevo curso', 'id="cu-new"', false) : '');
    on(root, '[data-ed]', function (ds) { courseForm(ds.ed); });
    on(root, '[data-mod]', function (ds) { courseModules(ds.mod); });
    if ($('#cu-new')) $('#cu-new').addEventListener('click', function () { courseForm(null); });
  };
  async function courseForm(id) {
    var c = {};
    if (id) { var r = await sb.from('courses').select('*').eq('id', id).single(); if (r.error) { fail(r.error); return; } c = r.data; }
    var body = openDlg(id ? 'Editar curso' : 'Nuevo curso',
      '<form class="ac-form" id="cf" novalidate><div class="form-grid">' +
      field('cf-title', 'Título', inp('cf-title', c.title, 'maxlength="160" required'), true) +
      (id ? '' : field('cf-slug', 'Identificador (slug)', inp('cf-slug', '', 'maxlength="80" pattern="[a-z0-9-]+" placeholder="mi-curso"'))) +
      field('cf-status', 'Estado', '<select class="control" id="cf-status">' + options([['draft', 'Borrador'], ['published', 'Publicado'], ['archived', 'Archivado']], c.status || 'draft') + '</select>') +
      field('cf-summary', 'Resumen', area('cf-summary', c.summary, 3), true) +
      field('cf-level', 'Nivel', inp('cf-level', c.level, 'maxlength="60"')) + field('cf-tag', 'Etiqueta', inp('cf-tag', c.tag, 'maxlength="60"')) +
      field('cf-min', 'Duración (minutos)', inp('cf-min', c.duration_minutes, 'type="number" min="0"')) + field('cf-hours', 'Horas académicas (certificado)', inp('cf-hours', c.academic_hours, 'type="number" min="0" step="0.5"')) +
      field('cf-url', 'Página pública del curso', inp('cf-url', c.public_url, 'maxlength="300" placeholder="cursos/mi-curso.html"'), true) +
      field('cf-cap', 'Cupo (vacío = sin límite)', inp('cf-cap', c.capacity, 'type="number" min="1"')) + field('cf-pass', 'Aprobación (%)', inp('cf-pass', c.pass_percentage == null ? 80 : c.pass_percentage, 'type="number" min="1" max="100"')) +
      field('cf-dop', 'Precio RD$', inp('cf-dop', c.price_dop || 0, 'type="number" min="0" step="0.01"')) + field('cf-usd', 'Precio US$', inp('cf-usd', c.price_usd || 0, 'type="number" min="0" step="0.01"')) +
      '</div><div class="ac-stack" style="margin-top:1rem">' + chk('cf-free', 'Gratuito (los estudiantes se matriculan solos)', c.is_free !== false) +
      chk('cf-exam', 'El certificado exige aprobar la evaluación final', c.requires_exam !== false) + '</div>' +
      '<p class="ac-small" style="margin-top:.6rem">Un curso de pago solo se matricula cuando la administración confirma el pago. No hay cobro en línea hasta conectar la pasarela.</p>' +
      '<div class="ac-actions"><button class="btn btn-primary" type="submit">Guardar</button></div></form>');
    $('#cf', body).addEventListener('submit', async function (e) {
      e.preventDefault();
      var row = { title: val('cf-title'), status: val('cf-status'), summary: val('cf-summary') || null, level: val('cf-level') || null, tag: val('cf-tag') || null,
        duration_minutes: numOrNull('cf-min'), academic_hours: numOrNull('cf-hours'), public_url: val('cf-url') || null, capacity: numOrNull('cf-cap'),
        pass_percentage: numOrNull('cf-pass') || 80, price_dop: numOrNull('cf-dop') || 0, price_usd: numOrNull('cf-usd') || 0,
        is_free: $('#cf-free').checked, requires_exam: $('#cf-exam').checked };
      if (!H.fieldError($('#cf-title'), row.title.length < 3 ? 'Escribe el título.' : '')) return;
      if (row.status === 'published' && !c.published_at) row.published_at = new Date().toISOString();
      var r;
      if (id) r = await sb.from('courses').update(row).eq('id', id);
      else {
        row.slug = val('cf-slug');
        if (!H.fieldError($('#cf-slug'), /^[a-z0-9]+(-[a-z0-9]+)*$/.test(row.slug) ? '' : 'Solo minúsculas, números y guiones.')) return;
        row.created_by = ME.profile_id; r = await sb.from('courses').insert(row);
      }
      if (r.error) { fail(r.error, dlSt); return; }
      closeDlg(); ok('Curso guardado.');
      var cc = await sb.from('courses').select('id,title,slug,status').order('title'); COURSES = cc.data || COURSES;
      LOAD.cursos($('#sec-cursos'));
    });
  }
  async function courseModules(id) {
    var c = COURSES.find(function (x) { return x.id === id; }) || {};
    var m = await sb.from('course_modules').select('id,position,title,anchor,lessons(id,title,kind,storage_path,content_url,position)').eq('course_id', id).order('position');
    if (m.error) { fail(m.error); return; }
    var mods = m.data || [];
    var body = openDlg('Módulos y materiales · ' + (c.title || ''),
      '<p class="ac-small">El avance se calcula con los módulos (anclas <code>modulo-N</code> de la página del curso). Agrega materiales descargables o enlaces a cada módulo.</p>' +
      table(['#', 'Módulo', 'Ancla', 'Materiales', ''], mods.map(function (x) {
        return [x.position, esc(x.title), '<code>' + esc(x.anchor) + '</code>', (x.lessons || []).sort(function (a, b) { return a.position - b.position; }).map(function (l) {
          return esc(l.title) + ' <span class="ac-small">(' + esc(l.kind) + ')</span> ' + (l.storage_path ? btn('Abrir', 'data-open="' + esc(l.storage_path) + '"') : '') + ' ' + btn('Quitar', 'data-dl="' + esc(l.id) + '" data-path="' + esc(l.storage_path || '') + '"');
        }).join('<br>') || '—', btn('Renombrar', 'data-ren="' + esc(x.id) + '" data-title="' + esc(x.title) + '"')];
      }), 'Este curso no tiene módulos.') +
      '<h3 style="margin-top:1.2rem">Agregar módulo</h3><form class="ac-inline" id="mm-add">' + '<label class="sr-only" for="mm-title">Título del módulo</label>' + inp('mm-title', '', 'maxlength="160" placeholder="Título del módulo"') +
      '<button class="btn btn-primary btn-sm" type="submit">Agregar</button></form>' +
      (mods.length ? '<h3 style="margin-top:1.2rem">Agregar material</h3><form class="ac-form" id="mm-mat" novalidate><div class="form-grid">' +
        field('mm-mod', 'Módulo', '<select class="control" id="mm-mod">' + options(mods.map(function (x) { return [x.id, x.position + '. ' + x.title]; }), mods[0].id) + '</select>') +
        field('mm-kind', 'Tipo', '<select class="control" id="mm-kind">' + options([['pdf', 'Documento (archivo)'], ['link', 'Enlace'], ['video', 'Video (enlace)']], 'pdf') + '</select>') +
        field('mm-ltitle', 'Título', inp('mm-ltitle', '', 'maxlength="160"'), true) +
        field('mm-file', 'Archivo (máx. 20 MB)', '<input class="control" id="mm-file" type="file">') + field('mm-url', 'Enlace (https://…)', inp('mm-url', '', 'type="url" maxlength="500"')) +
        '</div><div class="ac-actions"><button class="btn btn-primary btn-sm" type="submit">Agregar material</button></div></form>' : ''));
    on(body, '[data-open]', function (ds) { signed('course-materials', ds.open); });
    on(body, '[data-dl]', async function (ds) {
      if (!confirm('¿Quitar este material?')) return;
      if (ds.path) await sb.storage.from('course-materials').remove([ds.path]);
      var r = await sb.from('lessons').delete().eq('id', ds.dl); if (r.error) { fail(r.error, dlSt); return; } courseModules(id);
    });
    on(body, '[data-ren]', async function (ds) {
      var t = prompt('Nuevo título del módulo:', ds.title); if (!t || t.trim().length < 3) return;
      var r = await sb.from('course_modules').update({ title: t.trim().slice(0, 160) }).eq('id', ds.ren); if (r.error) { fail(r.error, dlSt); return; } courseModules(id);
    });
    $('#mm-add', body).addEventListener('submit', async function (e) {
      e.preventDefault(); var t = val('mm-title'); if (t.length < 3) return;
      var pos = mods.reduce(function (a, x) { return Math.max(a, x.position); }, 0) + 1;
      var r = await sb.from('course_modules').insert({ course_id: id, position: pos, title: t, anchor: 'modulo-' + pos });
      if (r.error) { fail(r.error, dlSt); return; } courseModules(id);
    });
    var mf = $('#mm-mat', body);
    if (mf) mf.addEventListener('submit', async function (e) {
      e.preventDefault();
      var kind = val('mm-kind'), title = val('mm-ltitle'), file = $('#mm-file').files[0], url = val('mm-url'), b = $('button[type=submit]', mf);
      if (!H.fieldError($('#mm-ltitle'), title.length < 3 ? 'Escribe el título.' : '')) return;
      var row = { module_id: val('mm-mod'), title: title, kind: kind === 'pdf' ? 'pdf' : kind, position: 1 };
      if (kind === 'pdf') {
        if (!file) { H.fieldError($('#mm-file'), 'Selecciona un archivo.'); return; }
        if (file.size > 20 * 1024 * 1024) { H.fieldError($('#mm-file'), 'Máximo 20 MB.'); return; }
        H.busy(b, true, 'Subiendo…');
        var path = id + '/' + Date.now() + '-' + safeName(file);
        var up = await sb.storage.from('course-materials').upload(path, file, { contentType: file.type || 'application/octet-stream' });
        if (up.error) { H.busy(b, false); fail(up.error, dlSt); return; }
        row.storage_path = path;
      } else {
        if (!H.fieldError($('#mm-url'), /^https:\/\/\S+$/.test(url) ? '' : 'Escribe un enlace https://')) return;
        row.content_url = url;
      }
      var mod = mods.find(function (x) { return x.id === row.module_id; });
      row.position = ((mod && mod.lessons) || []).length + 1;
      var r = await sb.from('lessons').insert(row); H.busy(b, false);
      if (r.error) { fail(r.error, dlSt); return; } courseModules(id);
    });
  }

  // ---------- Evaluaciones ----------
  var QT = { single: 'Opción única', multiple: 'Opción múltiple', true_false: 'Verdadero / falso', open: 'Abierta', case: 'Caso práctico' };
  LOAD.evaluaciones = async function (root) {
    var ex = await sb.from('exams').select('id,title,status,course_id,is_certification,pass_percentage,max_attempts,time_limit_minutes,courses(title),questions(count)').order('title');
    var q = await sb.from('exam_attempts').select('id,attempt_number,submitted_at,auto_score,max_score,exams(title),who:profiles!exam_attempts_profile_id_fkey(first_name,last_name)').eq('status', 'submitted').order('submitted_at');
    var g = await sb.from('exam_attempts').select('id,attempt_number,submitted_at,score_pct,passed,status,exams(title),who:profiles!exam_attempts_profile_id_fkey(first_name,last_name)').in('status', ['graded']).order('submitted_at', { ascending: false }).limit(50);
    if (ex.error) { fail(ex.error); return; }
    root.innerHTML =
      card('Por calificar', table(['Estudiante', 'Evaluación', 'Intento', 'Entrega', 'Puntos automáticos', ''], (q.data || []).map(function (a) {
        return [fullName(a.who), esc(a.exams ? a.exams.title : ''), a.attempt_number, d(a.submitted_at, true), n(a.auto_score) + ' / ' + n(a.max_score), btn('Revisar y calificar', 'data-rev="' + esc(a.id) + '"', false)];
      }), 'No hay intentos pendientes de calificación manual.')) +
      card('Evaluaciones', table(['Evaluación', 'Curso', 'Tipo', 'Estado', 'Preguntas', 'Aprobación', 'Intentos', 'Tiempo', ''], (ex.data || []).map(function (x) {
        return [esc(x.title), esc(x.courses ? x.courses.title : 'Independiente'), x.is_certification ? 'Certificación' : 'Práctica',
          tag({ published: 'Publicada', draft: 'Borrador', archived: 'Archivada' }[x.status], x.status === 'published' ? 'ok' : ''),
          n(x.questions && x.questions[0] ? x.questions[0].count : 0, 0), n(x.pass_percentage) + ' %', x.max_attempts, x.time_limit_minutes ? x.time_limit_minutes + ' min' : 'Sin límite',
          btn('Editar', 'data-ex="' + esc(x.id) + '"') + ' ' + btn('Preguntas', 'data-qs="' + esc(x.id) + '"')];
      }), 'No hay evaluaciones.'), btn('Nueva evaluación', 'id="ex-new"', false)) +
      card('Resultados recientes', table(['Estudiante', 'Evaluación', 'Intento', 'Fecha', 'Calificación', 'Resultado', ''], (g.data || []).map(function (a) {
        return [fullName(a.who), esc(a.exams ? a.exams.title : ''), a.attempt_number, d(a.submitted_at, true), n(a.score_pct) + ' %', a.passed ? tag('Aprobado', 'ok') : tag('No aprobado'), btn('Ver', 'data-rev="' + esc(a.id) + '"')];
      }), 'Sin resultados todavía.'));
    on(root, '[data-rev]', function (ds) { reviewAttempt(ds.rev); });
    on(root, '[data-ex]', function (ds) { examForm(ds.ex); });
    on(root, '[data-qs]', function (ds) { examQuestions(ds.qs); });
    $('#ex-new').addEventListener('click', function () { examForm(null); });
  };
  async function reviewAttempt(id) {
    var r = await sb.rpc('attempt_review', { p_attempt: id });
    if (r.error) { fail(r.error); return; }
    var x = r.data, a = x.attempt, manualMax = 0;
    var qs = (x.questions || []).map(function (q, i) {
      var resp = q.response, manual = q.type === 'open' || q.type === 'case';
      if (manual) manualMax += Number(q.points);
      var detail = manual ? '<p style="white-space:pre-line" class="ac-answer">' + esc(resp || '(sin respuesta)') + '</p>'
        : '<ul class="ac-opts">' + (q.answers || []).map(function (o) {
          var chosen = [].concat(resp || []).indexOf(o.id) > -1;
          return '<li class="' + (o.is_correct ? 'is-correct' : '') + (chosen ? ' is-chosen' : '') + '">' + (chosen ? '☑ ' : '☐ ') + esc(o.label) + (o.is_correct ? ' <b>(correcta)</b>' : '') + '</li>';
        }).join('') + '</ul>';
      return '<div class="ac-q"><p><b>' + (i + 1) + '.</b> ' + esc(q.prompt) + ' <span class="ac-small">' + esc(QT[q.type]) + ' · ' + n(q.points) + ' pts</span></p>' + detail + '</div>';
    }).join('');
    var body = openDlg('Intento de ' + x.student + ' · ' + x.exam,
      '<p class="ac-small">Intento ' + a.attempt_number + ' · Entregado ' + d(a.submitted_at, true) + ' · Puntos automáticos: ' + n(a.auto_score) + ' de ' + n(a.max_score) +
      (a.score_pct != null ? ' · Calificación: ' + n(a.score_pct) + ' %' : '') + '</p>' + qs +
      (manualMax > 0 ? '<form class="ac-form" id="gr-f" novalidate><div class="form-grid">' +
        field('gr-score', 'Puntos de las preguntas abiertas (0 a ' + manualMax + ')', inp('gr-score', a.manual_score, 'type="number" min="0" max="' + manualMax + '" step="0.5" required')) +
        field('gr-fb', 'Retroalimentación para el estudiante', area('gr-fb', a.feedback, 3), true) +
        '</div><div class="ac-actions"><button class="btn btn-primary" type="submit">Guardar calificación</button></div></form>' : ''));
    var f = $('#gr-f', body);
    if (f) f.addEventListener('submit', async function (e) {
      e.preventDefault();
      var r2 = await sb.rpc('grade_exam_attempt', { p_attempt: id, p_manual_score: numOrNull('gr-score'), p_feedback: val('gr-fb') });
      if (r2.error) { fail(r2.error, dlSt); return; }
      closeDlg(); ok('Calificación guardada: ' + n(r2.data.score_pct) + ' %.'); LOAD.evaluaciones($('#sec-evaluaciones'));
    });
  }
  async function examForm(id) {
    var x = { status: 'draft', max_attempts: 3, pass_percentage: 80, is_free: true, shuffle_questions: true, is_certification: true };
    if (id) { var r = await sb.from('exams').select('*').eq('id', id).single(); if (r.error) { fail(r.error); return; } x = r.data; }
    var body = openDlg(id ? 'Editar evaluación' : 'Nueva evaluación', '<form class="ac-form" id="xf" novalidate><div class="form-grid">' +
      field('xf-title', 'Título', inp('xf-title', x.title, 'maxlength="160"'), true) +
      field('xf-course', 'Curso', '<select class="control" id="xf-course">' + courseOpts(x.course_id || '', IS_ACAD ? 'Independiente (sin curso)' : null) + '</select>') +
      field('xf-status', 'Estado', '<select class="control" id="xf-status">' + options([['draft', 'Borrador'], ['published', 'Publicada'], ['archived', 'Archivada']], x.status) + '</select>') +
      field('xf-desc', 'Instrucciones', area('xf-desc', x.description, 3), true) +
      field('xf-time', 'Tiempo límite (min, vacío = sin límite)', inp('xf-time', x.time_limit_minutes, 'type="number" min="1"')) +
      field('xf-att', 'Intentos permitidos', inp('xf-att', x.max_attempts, 'type="number" min="1" max="20"')) +
      field('xf-pass', 'Aprobación (%)', inp('xf-pass', x.pass_percentage, 'type="number" min="1" max="100"')) +
      field('xf-qpa', 'Preguntas por intento (vacío = todas)', inp('xf-qpa', x.questions_per_attempt, 'type="number" min="1"')) +
      field('xf-from', 'Disponible desde', inp('xf-from', isoLocal(x.available_from), 'type="datetime-local"')) +
      field('xf-until', 'Disponible hasta', inp('xf-until', isoLocal(x.available_until), 'type="datetime-local"')) +
      field('xf-dop', 'Precio RD$ (si no es gratuita)', inp('xf-dop', x.price_dop || 0, 'type="number" min="0" step="0.01"')) +
      field('xf-usd', 'Precio US$', inp('xf-usd', x.price_usd || 0, 'type="number" min="0" step="0.01"')) +
      '</div><div class="ac-stack" style="margin-top:1rem">' + chk('xf-cert', 'Es la evaluación de certificación del curso', x.is_certification) +
      chk('xf-shuffle', 'Mezclar preguntas y opciones', x.shuffle_questions) + chk('xf-free', 'Gratuita', x.is_free) + '</div>' +
      '<div class="ac-actions"><button class="btn btn-primary" type="submit">Guardar</button></div></form>');
    $('#xf', body).addEventListener('submit', async function (e) {
      e.preventDefault();
      var row = { title: val('xf-title'), course_id: val('xf-course') || null, status: val('xf-status'), description: val('xf-desc') || null,
        time_limit_minutes: numOrNull('xf-time'), max_attempts: numOrNull('xf-att') || 1, pass_percentage: numOrNull('xf-pass') || 80,
        questions_per_attempt: numOrNull('xf-qpa'), available_from: val('xf-from') ? new Date(val('xf-from')).toISOString() : null,
        available_until: val('xf-until') ? new Date(val('xf-until')).toISOString() : null, price_dop: numOrNull('xf-dop') || 0, price_usd: numOrNull('xf-usd') || 0,
        is_certification: $('#xf-cert').checked, shuffle_questions: $('#xf-shuffle').checked, is_free: $('#xf-free').checked };
      if (!H.fieldError($('#xf-title'), row.title.length < 3 ? 'Escribe el título.' : '')) return;
      var r = id ? await sb.from('exams').update(row).eq('id', id) : await sb.from('exams').insert(Object.assign({ created_by: ME.profile_id }, row));
      if (r.error) { fail(r.error, dlSt); return; }
      closeDlg(); ok('Evaluación guardada.'); LOAD.evaluaciones($('#sec-evaluaciones'));
    });
  }
  async function examQuestions(id) {
    var r = await sb.from('questions').select('id,type,prompt,points,explanation,position,is_active,answers(id,label,is_correct,position)').eq('exam_id', id).order('position');
    var used = await sb.from('exam_attempts').select('id', { count: 'exact', head: true }).eq('exam_id', id);
    if (r.error) { fail(r.error); return; }
    var locked = (used.count || 0) > 0, qs = r.data || [];
    var body = openDlg('Banco de preguntas (' + qs.length + ')',
      (locked ? '<p class="ac-info">Esta evaluación ya tiene intentos: para no alterar resultados emitidos, las preguntas existentes no se editan. Puedes desactivarlas y agregar nuevas.</p>' : '') +
      qs.map(function (q, i) {
        return '<div class="ac-q' + (q.is_active ? '' : ' is-off') + '"><p><b>' + (i + 1) + '.</b> ' + esc(q.prompt) + ' <span class="ac-small">' + esc(QT[q.type]) + ' · ' + n(q.points) + ' pts' + (q.is_active ? '' : ' · desactivada') + '</span></p>' +
          ((q.answers || []).length ? '<ul class="ac-opts">' + q.answers.sort(function (a, b) { return a.position - b.position; }).map(function (a) { return '<li class="' + (a.is_correct ? 'is-correct' : '') + '">' + esc(a.label) + (a.is_correct ? ' <b>(correcta)</b>' : '') + '</li>'; }).join('') + '</ul>' : '') +
          '<div class="ac-actions" style="margin-top:.4rem">' + btn(q.is_active ? 'Desactivar' : 'Activar', 'data-tog="' + esc(q.id) + '" data-on="' + (q.is_active ? '1' : '0') + '"') +
          (locked ? '' : ' ' + btn('Eliminar', 'data-del="' + esc(q.id) + '"')) + '</div></div>';
      }).join('') +
      '<h3 style="margin-top:1.2rem">Agregar pregunta</h3><form class="ac-form" id="qf" novalidate><div class="form-grid">' +
      field('qf-type', 'Tipo', '<select class="control" id="qf-type">' + options(Object.keys(QT).map(function (k) { return [k, QT[k]]; }), 'single') + '</select>') +
      field('qf-pts', 'Puntos', inp('qf-pts', 1, 'type="number" min="0.5" step="0.5"')) +
      field('qf-prompt', 'Enunciado', area('qf-prompt', '', 3), true) +
      '<div class="field full" id="qf-opts"><span class="ac-label">Opciones (marca la o las correctas)</span>' + [1, 2, 3, 4, 5, 6].map(function (k) {
        return '<div class="ac-inline"><input type="checkbox" id="qf-ok' + k + '" aria-label="Opción ' + k + ' correcta"><label class="sr-only" for="qf-o' + k + '">Opción ' + k + '</label>' + inp('qf-o' + k, '', 'maxlength="300" placeholder="Opción ' + k + '"') + '</div>';
      }).join('') + '<span class="error" id="qf-opts-e"></span></div>' +
      field('qf-exp', 'Explicación (se usa en la revisión)', area('qf-exp', '', 2), true) +
      '</div><div class="ac-actions"><button class="btn btn-primary" type="submit">Agregar pregunta</button></div></form>');
    var syncType = function () {
      var t = val('qf-type'); $('#qf-opts').hidden = t === 'open' || t === 'case';
      if (t === 'true_false') { $('#qf-o1').value = 'Verdadero'; $('#qf-o2').value = 'Falso'; for (var k = 3; k <= 6; k++) $('#qf-o' + k).value = ''; }
    };
    $('#qf-type').addEventListener('change', syncType);
    on(body, '[data-tog]', async function (ds) { var x = await sb.from('questions').update({ is_active: ds.on !== '1' }).eq('id', ds.tog); if (x.error) { fail(x.error, dlSt); return; } examQuestions(id); });
    on(body, '[data-del]', async function (ds) { if (!confirm('¿Eliminar la pregunta?')) return; var x = await sb.from('questions').delete().eq('id', ds.del); if (x.error) { fail(x.error, dlSt); return; } examQuestions(id); });
    $('#qf', body).addEventListener('submit', async function (e) {
      e.preventDefault();
      var t = val('qf-type'), prompt_ = val('qf-prompt'), opts = [];
      for (var k = 1; k <= 6; k++) { var l = val('qf-o' + k); if (l) opts.push({ label: l, is_correct: $('#qf-ok' + k).checked, position: opts.length + 1 }); }
      if (!H.fieldError($('#qf-prompt'), prompt_.length < 5 ? 'Escribe el enunciado.' : '')) return;
      var nOk = opts.filter(function (o) { return o.is_correct; }).length, err = '';
      if (t !== 'open' && t !== 'case') {
        if (opts.length < 2) err = 'Agrega al menos dos opciones.';
        else if ((t === 'single' || t === 'true_false') && nOk !== 1) err = 'Marca exactamente una opción correcta.';
        else if (t === 'multiple' && nOk < 1) err = 'Marca al menos una opción correcta.';
      }
      $('#qf-opts-e').textContent = err; if (err) return;
      var ins = await sb.from('questions').insert({ exam_id: id, type: t, prompt: prompt_, points: numOrNull('qf-pts') || 1, explanation: val('qf-exp') || null, position: qs.length + 1 }).select('id').single();
      if (ins.error) { fail(ins.error, dlSt); return; }
      if (t !== 'open' && t !== 'case') {
        var a = await sb.from('answers').insert(opts.map(function (o) { return Object.assign({ question_id: ins.data.id }, o); }));
        if (a.error) { fail(a.error, dlSt); return; }
      }
      examQuestions(id);
    });
  }

  // ---------- Asignaciones ----------
  LOAD.asignaciones = async function (root) {
    var a = await sb.from('assignments').select('id,title,due_at,max_score,is_published,course_id,courses(title)').order('created_at', { ascending: false });
    var s = await sb.from('assignment_submissions').select('id,status,submitted_at,file_path,comment,score,feedback,assignments(title,max_score),who:profiles!assignment_submissions_profile_id_fkey(first_name,last_name)').in('status', ['submitted', 'in_review']).order('submitted_at');
    if (a.error) { fail(a.error); return; }
    root.innerHTML =
      card('Entregas por calificar', table(['Estudiante', 'Asignación', 'Entrega', 'Estado', ''], (s.data || []).map(function (x) {
        return [fullName(x.who), esc(x.assignments ? x.assignments.title : ''), d(x.submitted_at, true), x.status === 'in_review' ? 'En revisión' : 'Entregada', btn('Calificar', 'data-gr="' + esc(x.id) + '"', false)];
      }), 'No hay entregas pendientes.')) +
      card('Asignaciones', table(['Asignación', 'Curso', 'Fecha límite', 'Puntaje', 'Estado', ''], (a.data || []).map(function (x) {
        return [esc(x.title), esc(x.courses ? x.courses.title : ''), d(x.due_at, true), n(x.max_score), x.is_published ? tag('Publicada', 'ok') : tag('Borrador'), btn('Editar', 'data-as="' + esc(x.id) + '"')];
      }), 'No hay asignaciones.'), btn('Nueva asignación', 'id="as-new"', false));
    LOADED.subs = s.data || [];
    on(root, '[data-gr]', function (ds) { gradeSubmission(LOADED.subs.find(function (x) { return x.id === ds.gr; })); });
    on(root, '[data-as]', function (ds) { assignmentForm(ds.as); });
    $('#as-new').addEventListener('click', function () { assignmentForm(null); });
  };
  async function assignmentForm(id) {
    var x = { max_score: 100, is_published: false };
    if (id) { var r = await sb.from('assignments').select('*').eq('id', id).single(); if (r.error) { fail(r.error); return; } x = r.data; }
    var body = openDlg(id ? 'Editar asignación' : 'Nueva asignación', '<form class="ac-form" id="af" novalidate><div class="form-grid">' +
      field('af-title', 'Título', inp('af-title', x.title, 'maxlength="160"'), true) +
      field('af-course', 'Curso', '<select class="control" id="af-course">' + courseOpts(x.course_id || '', 'Selecciona…') + '</select>') +
      field('af-due', 'Fecha límite', inp('af-due', isoLocal(x.due_at), 'type="datetime-local"')) +
      field('af-max', 'Puntaje máximo', inp('af-max', x.max_score, 'type="number" min="1"')) +
      field('af-ins', 'Instrucciones', area('af-ins', x.instructions, 5), true) +
      '</div><div class="ac-stack" style="margin-top:1rem">' + chk('af-pub', 'Publicada (visible para los matriculados)', x.is_published) + '</div>' +
      '<div class="ac-actions"><button class="btn btn-primary" type="submit">Guardar</button></div></form>');
    $('#af', body).addEventListener('submit', async function (e) {
      e.preventDefault();
      var row = { title: val('af-title'), course_id: val('af-course'), due_at: val('af-due') ? new Date(val('af-due')).toISOString() : null,
        max_score: numOrNull('af-max') || 100, instructions: val('af-ins') || null, is_published: $('#af-pub').checked };
      if (!H.fieldError($('#af-title'), row.title.length < 3 ? 'Escribe el título.' : '')) return;
      if (!H.fieldError($('#af-course'), row.course_id ? '' : 'Elige el curso.')) return;
      var r = id ? await sb.from('assignments').update(row).eq('id', id) : await sb.from('assignments').insert(Object.assign({ created_by: ME.profile_id }, row));
      if (r.error) { fail(r.error, dlSt); return; }
      closeDlg(); ok('Asignación guardada.'); LOAD.asignaciones($('#sec-asignaciones'));
    });
  }
  function gradeSubmission(x) {
    if (!x) return;
    var max = x.assignments ? Number(x.assignments.max_score) : 100;
    var body = openDlg('Calificar · ' + (x.assignments ? x.assignments.title : ''),
      '<p class="ac-small">' + fullName(x.who) + ' · entregado ' + d(x.submitted_at, true) + '</p>' +
      (x.comment ? '<p class="ac-answer" style="white-space:pre-line">' + esc(x.comment) + '</p>' : '') +
      (x.file_path ? '<div class="ac-actions">' + btn('Abrir el archivo entregado', 'id="gs-file"') + '</div>' : '') +
      '<form class="ac-form" id="gs" novalidate><div class="form-grid">' +
      field('gs-score', 'Puntaje (0 a ' + max + ')', inp('gs-score', x.score, 'type="number" min="0" max="' + max + '" step="0.5"')) +
      field('gs-status', 'Resultado', '<select class="control" id="gs-status">' + options([['graded', 'Calificada'], ['returned', 'Devolver para corrección'], ['in_review', 'Marcar en revisión']], 'graded') + '</select>') +
      field('gs-fb', 'Comentarios para el estudiante', area('gs-fb', x.feedback, 4), true) +
      '</div><div class="ac-actions"><button class="btn btn-primary" type="submit">Guardar</button></div></form>');
    if ($('#gs-file')) $('#gs-file').addEventListener('click', function () { signed('submissions', x.file_path); });
    $('#gs', body).addEventListener('submit', async function (e) {
      e.preventDefault();
      var stt = val('gs-status'), score = numOrNull('gs-score');
      if (stt === 'graded' && !H.fieldError($('#gs-score'), score == null || score < 0 || score > max ? 'Indica un puntaje entre 0 y ' + max + '.' : '')) return;
      var r = await sb.from('assignment_submissions').update({ status: stt, score: stt === 'graded' ? score : null, feedback: val('gs-fb') || null,
        graded_by: ME.profile_id, graded_at: new Date().toISOString() }).eq('id', x.id);
      if (r.error) { fail(r.error, dlSt); return; }
      closeDlg(); ok('Entrega actualizada.'); LOAD.asignaciones($('#sec-asignaciones'));
    });
  }

  // ---------- Certificados ----------
  LOAD.certificados = async function (root) {
    var q = await sb.rpc('certificate_queue');
    var c = await sb.from('certificates').select('verification_code,student_name,course_title,grade_pct,status,issued_at,revoked_reason').order('issued_at', { ascending: false }).limit(300);
    if (q.error) { fail(q.error); return; }
    root.innerHTML =
      card('Listos para emitir', '<p class="ac-muted" style="margin-top:.5rem">Solo aparecen estudiantes que completaron todos los módulos y, si el curso lo exige, aprobaron la evaluación final. La emisión no es automática: revisa y confirma.</p>' +
        table(['Estudiante', 'Correo', 'Curso', 'Mejor calificación', 'Finalización', ''], (q.data || []).map(function (x) {
          return [esc(x.student_name), esc(x.email), esc(x.course_title), x.best_score == null ? '—' : n(x.best_score) + ' %', d(x.completed_at), btn('Emitir certificado', 'data-iss="' + esc(x.enrollment_id) + '"', false)];
        }), 'No hay certificados pendientes de emisión.')) +
      card('Certificados emitidos', '<div class="ac-inline"><label class="sr-only" for="ce-q">Filtrar</label>' + inp('ce-q', '', 'placeholder="Filtrar por nombre, curso o código"') + '</div><div id="ce-list"></div>');
    var rows = c.data || [];
    var paint = function () {
      var f = val('ce-q').toLowerCase();
      var list = rows.filter(function (x) { return !f || (x.student_name + ' ' + x.course_title + ' ' + x.verification_code).toLowerCase().indexOf(f) > -1; });
      $('#ce-list').innerHTML = table(['Código', 'Estudiante', 'Curso', 'Calificación', 'Emisión', 'Estado', ''], list.map(function (x) {
        var code = encodeURIComponent(x.verification_code);
        return ['<code>' + esc(x.verification_code) + '</code>', esc(x.student_name), esc(x.course_title), x.grade_pct == null ? '—' : n(x.grade_pct) + ' %', d(x.issued_at),
          x.status === 'valid' ? tag('Vigente', 'ok') : tag('Revocado') + '<br><span class="ac-small">' + esc(x.revoked_reason || '') + '</span>',
          (x.status === 'valid' ? '<a class="btn btn-ghost btn-sm" href="' + H.base + 'certificado.html?codigo=' + code + '" target="_blank" rel="noopener">Ver</a>' : '') +
          (IS_SUPER && x.status === 'valid' ? ' ' + btn('Revocar', 'data-rv="' + esc(x.verification_code) + '"') : '')];
      }), 'Sin certificados emitidos.');
      on($('#ce-list'), '[data-rv]', async function (ds) {
        var reason = prompt('Motivo de la revocación (queda registrado y se muestra en la verificación pública):');
        if (reason === null) return;
        var r = await sb.rpc('revoke_certificate', { p_code: ds.rv, p_reason: reason });
        if (r.error) { fail(r.error); return; } ok('Certificado revocado.'); LOAD.certificados(root);
      });
    };
    $('#ce-q').addEventListener('input', paint); paint();
    on(root, '[data-iss]', async function (ds, b) {
      if (!confirm('¿Emitir el certificado? Se notificará al estudiante.')) return;
      H.busy(b, true, 'Emitiendo…');
      var r = await sb.rpc('issue_certificate', { p_enrollment: ds.iss });
      H.busy(b, false);
      if (r.error) { fail(r.error); return; } ok('Certificado emitido: ' + r.data + '.'); LOAD.certificados(root);
    });
  };

  // ---------- Mensajes y avisos ----------
  var TH = { open: 'Nueva', pending: 'Esperando respuesta', answered: 'Respondida', archived: 'Archivada' };
  LOAD.mensajes = async function (root) {
    if (!LOADED.msg) {
      root.innerHTML = card('Consultas de estudiantes', '<div class="ac-filters" role="group" aria-label="Filtrar consultas">' +
        [['active', 'Sin responder'], ['answered', 'Respondidas'], ['archived', 'Archivadas'], ['all', 'Todas']].map(function (f, i) {
          return '<button type="button" data-tf="' + f[0] + '" aria-pressed="' + (i === 0) + '">' + f[1] + '</button>';
        }).join('') + '</div><div id="ms-list"></div>') +
        card('Enviar un aviso', '<p class="ac-muted" style="margin-top:.5rem">El aviso llega a las notificaciones de los estudiantes (y por correo cuando el envío esté habilitado).</p>' +
          '<form class="ac-form" id="an-f" novalidate><div class="form-grid">' +
          field('an-course', 'Destinatarios', '<select class="control" id="an-course">' + (IS_ACAD ? '<option value="">Todos los estudiantes activos</option>' : '') + courseOpts('', null) + '</select>') +
          field('an-title', 'Título', inp('an-title', '', 'maxlength="140"')) + field('an-body', 'Mensaje', area('an-body', '', 4), true) +
          '</div><div class="ac-actions"><button class="btn btn-primary" type="submit">Enviar aviso</button></div></form>');
      on(root, '[data-tf]', function (ds, b) { $$('[data-tf]', root).forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); LOADED.tf = ds.tf; listThreads(); });
      $('#an-f').addEventListener('submit', async function (e) {
        e.preventDefault();
        var t = val('an-title'); if (!H.fieldError($('#an-title'), t.length < 3 ? 'Escribe el título.' : '')) return;
        if (!confirm('¿Enviar el aviso?')) return;
        var r = await sb.rpc('admin_send_announcement', { p_course: val('an-course') || null, p_title: t, p_body: val('an-body') });
        if (r.error) { fail(r.error); return; } ok('Aviso enviado a ' + r.data + ' estudiante(s).'); $('#an-title').value = ''; $('#an-body').value = '';
      });
      LOADED.msg = true; LOADED.tf = 'active';
    }
    listThreads();
  };
  async function listThreads() {
    var q = sb.from('message_threads').select('id,profile_id,subject,status,updated_at,courses(title),who:profiles!message_threads_profile_id_fkey(first_name,last_name,email)').order('updated_at', { ascending: false }).limit(200);
    if (LOADED.tf === 'active') q = q.in('status', ['open', 'pending']); else if (LOADED.tf !== 'all') q = q.eq('status', LOADED.tf);
    var r = await q; if (r.error) { fail(r.error); return; }
    var box = $('#ms-list');
    box.innerHTML = table(['Estudiante', 'Asunto', 'Curso', 'Estado', 'Actualizada', ''], (r.data || []).map(function (t) {
      return [fullName(t.who) + '<br><span class="ac-small">' + esc(t.who ? t.who.email : '') + '</span>', esc(t.subject), esc(t.courses ? t.courses.title : '—'),
        tag(TH[t.status], t.status === 'answered' ? 'ok' : t.status === 'archived' ? '' : 'run'), d(t.updated_at, true), btn('Abrir', 'data-th="' + esc(t.id) + '"', false)];
    }), 'No hay consultas en esta vista.');
    LOADED.threads = r.data || [];
    on(box, '[data-th]', function (ds) { openThread(LOADED.threads.find(function (t) { return t.id === ds.th; })); });
  }
  async function openThread(t) {
    var m = await sb.from('messages').select('id,body,created_at,sender_profile_id,read_at').eq('thread_id', t.id).order('created_at');
    if (m.error) { fail(m.error); return; }
    var msgs = m.data || [];
    var body = openDlg(t.subject, '<p class="ac-small">' + fullName(t.who) + ' · ' + esc(t.who ? t.who.email : '') + (t.courses ? ' · ' + esc(t.courses.title) : '') + '</p><div class="ac-thread">' +
      msgs.map(function (x) {
        var mine = x.sender_profile_id === ME.profile_id, student = x.sender_profile_id === t.profile_id;
        return '<div class="ac-msg' + (mine ? ' is-me' : '') + '"><p class="ac-small"><b>' + (mine ? 'Tú' : student ? fullName(t.who) : 'Equipo Academy') + '</b> · ' + d(x.created_at, true) + '</p><p style="white-space:pre-line">' + esc(x.body) + '</p></div>';
      }).join('') + '</div>' +
      (t.status !== 'archived' ? '<form class="ac-form" id="rp-f" novalidate>' + field('rp-body', 'Respuesta', area('rp-body', '', 4), true) +
        '<div class="ac-actions"><button class="btn btn-primary" type="submit">Responder</button>' + btn('Archivar consulta', 'id="rp-arch"') + '</div></form>' : ''));
    var unread = msgs.filter(function (x) { return x.sender_profile_id === t.profile_id && !x.read_at; }).map(function (x) { return x.id; });
    if (unread.length) await sb.from('messages').update({ read_at: new Date().toISOString() }).in('id', unread);
    var f = $('#rp-f', body);
    if (f) {
      f.addEventListener('submit', async function (e) {
        e.preventDefault(); var txt = val('rp-body');
        if (!H.fieldError($('#rp-body'), txt.length < 2 ? 'Escribe la respuesta.' : '')) return;
        var r = await sb.from('messages').insert({ thread_id: t.id, sender_profile_id: ME.profile_id, body: txt.slice(0, 4000) });
        if (r.error) { fail(r.error, dlSt); return; } t.status = 'answered'; openThread(t); listThreads();
      });
      $('#rp-arch').addEventListener('click', async function () {
        var r = await sb.from('message_threads').update({ status: 'archived' }).eq('id', t.id); if (r.error) { fail(r.error, dlSt); return; } closeDlg(); listThreads();
      });
    }
  }

  // ---------- Finanzas ----------
  var PST = { pending: 'Pendiente', confirmed: 'Confirmado', rejected: 'Rechazado', refunded: 'Reembolsado', partially_refunded: 'Reembolso parcial' };
  var PMETHOD = { transfer: 'Transferencia', deposit: 'Depósito', card: 'Tarjeta', cash: 'Efectivo', paypal: 'PayPal', gateway: 'Pasarela', other: 'Otro' };
  var PTYPE = { course: 'Curso', workshop: 'Taller', corporate_training: 'Capacitación corporativa', exam: 'Examen', software: 'Software', service: 'Servicio', other: 'Otro' };
  var GRP = { training: 'Capacitación', software: 'Software', evaluation: 'Evaluación', other: 'Otros' };
  LOAD.finanzas = async function (root) {
    if (!LOADED.fin) {
      var y = new Date().getFullYear();
      root.innerHTML = '<p class="ac-info">Registro manual de cobros reales (transferencias, depósitos, efectivo, etc.). No hay pasarela de pago conectada: el cobro en línea se activará con el dominio propio. Las cifras en RD$ y US$ nunca se suman entre sí.</p>' +
        card('Período', '<form class="ac-inline" id="fi-f"><label for="fi-from">Desde</label>' + inp('fi-from', y + '-01-01', 'type="date"') + '<label for="fi-to">Hasta</label>' + inp('fi-to', y + '-12-31', 'type="date"') +
          '<button class="btn btn-primary btn-sm" type="submit">Actualizar</button>' + btn('Registrar pago', 'id="fi-new"', false) + btn('Categorías', 'id="fi-cat"') + '</form>') +
        '<div id="fi-sum"></div>' +
        card('Pagos del período', '<div class="ac-filters" role="group" aria-label="Filtrar pagos">' + [['all', 'Todos'], ['pending', 'Pendientes'], ['confirmed', 'Confirmados'], ['rejected', 'Rechazados'], ['refunded', 'Reembolsados']].map(function (f, i) {
          return '<button type="button" data-pf="' + f[0] + '" aria-pressed="' + (i === 0) + '">' + f[1] + '</button>'; }).join('') + '</div><div id="fi-list"></div>', btn('Exportar CSV', 'id="fi-csv"'));
      $('#fi-f').addEventListener('submit', function (e) { e.preventDefault(); finLoad(); });
      $('#fi-new').addEventListener('click', function () { paymentForm(); });
      $('#fi-cat').addEventListener('click', categoriesDlg);
      $('#fi-csv').addEventListener('click', function () {
        csv('pagos.csv', ['Fecha', 'Estudiante/cliente', 'Concepto', 'Categoría', 'Tipo', 'Moneda', 'Monto', 'Descuento', 'Comisión', 'Reembolso', 'Neto', 'Método', 'Referencia', 'Estado'],
          (LOADED.pays || []).map(function (p) { return [p.occurred_on, p.who ? (p.who.first_name + ' ' + p.who.last_name) : p.client_name, p.concept, p.cat ? p.cat.name : '', p.product_type, p.currency, p.amount, p.discount_amount, p.fee_amount, p.refunded_amount, p.net_amount, p.method, p.reference, p.status]; }));
      });
      on(root, '[data-pf]', function (ds, b) { $$('[data-pf]', root).forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); LOADED.pf = ds.pf; paintPays(); });
      LOADED.fin = true; LOADED.pf = 'all';
    }
    finLoad();
  };
  async function finLoad() {
    var from = val('fi-from'), to = val('fi-to');
    var s = await sb.rpc('finance_summary', { p_from: from, p_to: to });
    var p = await sb.from('payments').select('*,cat:revenue_categories(name),who:profiles!payments_profile_id_fkey(first_name,last_name,email)').gte('occurred_on', from).lte('occurred_on', to).order('occurred_on', { ascending: false }).limit(1000);
    if (s.error) { fail(s.error); return; }
    var x = s.data || {};
    var tot = (x.totals || []).map(function (t) {
      return '<div class="ac-card ac-fin"><h3>' + esc(t.currency) + '</h3><dl class="ac-dl">' +
        [['Ingresos brutos', t.gross], ['Descuentos y becas', t.discounts], ['Comisiones', t.fees], ['Reembolsos', t.refunds], ['Ingreso neto', t.net]].map(function (r) {
          return '<dt>' + r[0] + '</dt><dd>' + money(r[1], t.currency) + '</dd>'; }).join('') + '<dt>Pagos</dt><dd>' + n(t.payments, 0) + '</dd></dl></div>';
    }).join('');
    var pend = (x.pending || []).map(function (t) { return n(t.payments, 0) + ' pendiente(s) por ' + money(t.amount, t.currency); }).join(' · ');
    $('#fi-sum').innerHTML = '<div class="ac-grid-2">' + (tot || '<div class="ac-card">' + empty('Sin pagos confirmados en el período.') + '</div>') + '</div>' +
      (pend ? '<p class="ac-info">Por confirmar: ' + pend + '</p>' : '') +
      card('Ingreso neto por categoría', table(['Moneda', 'Categoría', 'Grupo', 'Pagos', 'Neto'], (x.by_category || []).map(function (r) { return [esc(r.currency), esc(r.category), esc(GRP[r.grp] || r.grp), n(r.payments, 0), money(r.net, r.currency)]; }), 'Sin datos.')) +
      card('Evolución mensual', table(['Mes', 'Moneda', 'Pagos', 'Neto'], (x.by_month || []).map(function (r) { return [esc(r.month), esc(r.currency), n(r.payments, 0), money(r.net, r.currency)]; }), 'Sin datos.')) +
      card('Por método y por producto', table(['Moneda', 'Método', 'Pagos', 'Neto'], (x.by_method || []).map(function (r) { return [esc(r.currency), esc(PMETHOD[r.method] || r.method), n(r.payments, 0), money(r.net, r.currency)]; }), 'Sin datos.') +
        table(['Moneda', 'Tipo', 'Producto', 'Pagos', 'Neto'], (x.by_product || []).map(function (r) { return [esc(r.currency), esc(PTYPE[r.product_type] || r.product_type), esc(r.product), n(r.payments, 0), money(r.net, r.currency)]; }), ''));
    LOADED.pays = p.data || []; paintPays();
  }
  function paintPays() {
    var list = (LOADED.pays || []).filter(function (p) { return LOADED.pf === 'all' || p.status === LOADED.pf || (LOADED.pf === 'refunded' && p.status === 'partially_refunded'); });
    var box = $('#fi-list');
    box.innerHTML = table(['Fecha', 'Estudiante / cliente', 'Concepto', 'Monto', 'Neto', 'Método', 'Estado', ''], list.map(function (p) {
      return [d(p.occurred_on), p.who ? fullName(p.who) : esc(p.client_name || ''), esc(p.concept) + '<br><span class="ac-small">' + esc(p.cat ? p.cat.name : '') + (p.reference ? ' · Ref. ' + esc(p.reference) : '') + '</span>',
        money(p.amount, p.currency) + (Number(p.discount_amount) ? '<br><span class="ac-small">Desc. ' + money(p.discount_amount, p.currency) + '</span>' : ''), money(p.net_amount, p.currency),
        esc(PMETHOD[p.method] || p.method), tag(PST[p.status], p.status === 'confirmed' ? 'ok' : p.status === 'pending' ? 'run' : ''),
        (p.status === 'pending' ? btn('Confirmar', 'data-pc="' + esc(p.id) + '"', false) + ' ' + btn('Rechazar', 'data-pr="' + esc(p.id) + '"') : '') +
        (p.status === 'confirmed' || p.status === 'partially_refunded' ? btn('Reembolso', 'data-pu="' + esc(p.id) + '"') : '') +
        (p.evidence_path ? ' ' + btn('Comprobante', 'data-pe="' + esc(p.evidence_path) + '"') : '')];
    }), 'Sin pagos en esta vista.');
    on(box, '[data-pc]', async function (ds) {
      if (!confirm('¿Confirmar que el pago fue recibido? Si corresponde a un curso, el estudiante quedará matriculado.')) return;
      var r = await sb.from('payments').update({ status: 'confirmed', confirmed_by: ME.profile_id, confirmed_at: new Date().toISOString() }).eq('id', ds.pc);
      if (r.error) { fail(r.error); return; } ok('Pago confirmado.'); finLoad();
    });
    on(box, '[data-pr]', async function (ds) {
      var note = prompt('Motivo del rechazo:'); if (note === null) return;
      var r = await sb.from('payments').update({ status: 'rejected', notes: note.slice(0, 500) }).eq('id', ds.pr);
      if (r.error) { fail(r.error); return; } finLoad();
    });
    on(box, '[data-pu]', async function (ds) {
      var p = LOADED.pays.find(function (x) { return x.id === ds.pu; });
      var max = Number(p.amount) - Number(p.fee_amount);
      var v = prompt('Monto total reembolsado (' + p.currency + ', máximo ' + max.toFixed(2) + '):', p.refunded_amount || ''); if (v === null) return;
      var amt = Number(String(v).replace(',', '.'));
      if (!(amt > 0) || amt > max) { H.status(st, 'Monto de reembolso no válido.', 'error'); return; }
      var r = await sb.from('payments').update({ refunded_amount: amt, status: amt >= max ? 'refunded' : 'partially_refunded' }).eq('id', p.id);
      if (r.error) { fail(r.error); return; } ok('Reembolso registrado.'); finLoad();
    });
    on(box, '[data-pe]', function (ds) { signed('payment-evidence', ds.pe); });
  }
  async function paymentForm() {
    var c = await sb.from('revenue_categories').select('id,name,grp,is_active').eq('is_active', true).order('name');
    var ex = await sb.from('exams').select('id,title').order('title');
    var today = new Date().toISOString().slice(0, 10);
    var body = openDlg('Registrar pago', '<form class="ac-form" id="pf" novalidate><div class="form-grid">' +
      field('pf-who', 'Estudiante (buscar por nombre, correo o código)', '<div class="ac-inline">' + inp('pf-q', '', 'aria-label="Buscar estudiante" placeholder="Buscar…"') + btn('Buscar', 'id="pf-find"') + '</div><select class="control" id="pf-who"><option value="">— Cliente sin cuenta —</option></select>', true) +
      field('pf-client', 'Nombre del cliente (si no tiene cuenta)', inp('pf-client', '', 'maxlength="160"')) +
      field('pf-cat', 'Categoría', '<select class="control" id="pf-cat">' + options((c.data || []).map(function (x) { return [x.id, x.name]; }), '', 'Selecciona…') + '</select>') +
      field('pf-concept', 'Concepto', inp('pf-concept', '', 'maxlength="200"'), true) +
      field('pf-type', 'Tipo de producto', '<select class="control" id="pf-type">' + options(Object.keys(PTYPE).map(function (k) { return [k, PTYPE[k]]; }), 'course') + '</select>') +
      field('pf-course', 'Curso (se matricula al confirmar)', '<select class="control" id="pf-course">' + courseOpts('', 'Ninguno') + '</select>') +
      field('pf-exam', 'Examen', '<select class="control" id="pf-exam">' + options((ex.data || []).map(function (x) { return [x.id, x.title]; }), '', 'Ninguno') + '</select>') +
      field('pf-pname', 'Producto (descripción)', inp('pf-pname', '', 'maxlength="160"')) +
      field('pf-date', 'Fecha del pago', inp('pf-date', today, 'type="date"')) +
      field('pf-cur', 'Moneda', '<select class="control" id="pf-cur">' + options([['DOP', 'RD$ (DOP)'], ['USD', 'US$ (USD)']], 'DOP') + '</select>') +
      field('pf-amount', 'Monto cobrado', inp('pf-amount', '', 'type="number" min="0.01" step="0.01"')) +
      field('pf-disc', 'Descuento aplicado', inp('pf-disc', 0, 'type="number" min="0" step="0.01"')) +
      field('pf-fee', 'Comisión bancaria', inp('pf-fee', 0, 'type="number" min="0" step="0.01"')) +
      field('pf-sch', 'Media beca aprobada (opcional)', '<select class="control" id="pf-sch"><option value="">Ninguna</option></select>') +
      field('pf-method', 'Método', '<select class="control" id="pf-method">' + options(Object.keys(PMETHOD).filter(function (k) { return k !== 'gateway'; }).map(function (k) { return [k, PMETHOD[k]]; }), 'transfer') + '</select>') +
      field('pf-ref', 'Referencia / número de transacción', inp('pf-ref', '', 'maxlength="120"')) +
      field('pf-status', 'Estado', '<select class="control" id="pf-status">' + options([['pending', 'Pendiente de verificar'], ['confirmed', 'Confirmado (dinero recibido)']], 'pending') + '</select>') +
      field('pf-file', 'Comprobante (PDF o imagen, máx. 5 MB)', '<input class="control" id="pf-file" type="file" accept=".pdf,.png,.jpg,.jpeg,.webp">') +
      field('pf-notes', 'Notas internas', area('pf-notes', '', 2), true) +
      '</div><div class="ac-actions"><button class="btn btn-primary" type="submit">Registrar</button></div></form>');
    var loadSch = async function () {
      var pid = val('pf-who'); var opt = '<option value="">Ninguna</option>';
      if (pid) {
        var s = await sb.from('scholarships').select('id,percentage,period_label,expires_on').eq('profile_id', pid).eq('status', 'approved');
        opt += (s.data || []).map(function (x) { return '<option value="' + esc(x.id) + '">' + n(x.percentage) + ' % · ' + esc(x.period_label) + (x.expires_on ? ' · hasta ' + d(x.expires_on) : '') + '</option>'; }).join('');
      }
      $('#pf-sch').innerHTML = opt;
    };
    $('#pf-find').addEventListener('click', async function () {
      var r = await sb.rpc('admin_student_list', { p_search: val('pf-q') || null });
      if (r.error) { fail(r.error, dlSt); return; }
      $('#pf-who').innerHTML = '<option value="">— Cliente sin cuenta —</option>' + (r.data || []).slice(0, 50).map(function (s) {
        return '<option value="' + esc(s.profile_id) + '">' + esc(s.full_name + ' · ' + s.email + (s.student_code ? ' · ' + s.student_code : '')) + '</option>'; }).join('');
      loadSch();
    });
    $('#pf-who').addEventListener('change', loadSch);
    $('#pf', body).addEventListener('submit', async function (e) {
      e.preventDefault();
      var b = $('button[type=submit]', this), stt = val('pf-status');
      var row = { profile_id: val('pf-who') || null, client_name: val('pf-client') || null, category_id: val('pf-cat'), concept: val('pf-concept'),
        product_type: val('pf-type'), course_id: val('pf-course') || null, exam_id: val('pf-exam') || null, product_name: val('pf-pname') || null,
        occurred_on: val('pf-date'), currency: val('pf-cur'), amount: numOrNull('pf-amount'), discount_amount: numOrNull('pf-disc') || 0, fee_amount: numOrNull('pf-fee') || 0,
        scholarship_id: val('pf-sch') || null, method: val('pf-method'), reference: val('pf-ref') || null, status: stt, notes: val('pf-notes') || null, created_by: ME.profile_id };
      var errs = [['pf-cat', !row.category_id && 'Elige la categoría.'], ['pf-concept', row.concept.length < 3 && 'Escribe el concepto.'], ['pf-amount', !(row.amount > 0) && 'Indica el monto.'],
        ['pf-client', !row.profile_id && !row.client_name && 'Elige un estudiante o escribe el nombre del cliente.'], ['pf-fee', row.fee_amount > (row.amount || 0) && 'La comisión no puede superar el monto.']];
      var bad = false; errs.forEach(function (x) { if (!H.fieldError($('#' + x[0]), x[1] || '')) bad = true; }); if (bad) return;
      if (stt === 'confirmed') { row.confirmed_by = ME.profile_id; row.confirmed_at = new Date().toISOString(); }
      H.busy(b, true, 'Guardando…');
      var f = $('#pf-file').files[0];
      if (f) {
        if (f.size > 5 * 1024 * 1024) { H.busy(b, false); H.fieldError($('#pf-file'), 'Máximo 5 MB.'); return; }
        var path = row.occurred_on.slice(0, 4) + '/' + Date.now() + '-' + safeName(f);
        var up = await sb.storage.from('payment-evidence').upload(path, f, { contentType: f.type || 'application/octet-stream' });
        if (up.error) { H.busy(b, false); fail(up.error, dlSt); return; }
        row.evidence_path = path;
      }
      var r = await sb.from('payments').insert(row); H.busy(b, false);
      if (r.error) { fail(r.error, dlSt); return; }
      closeDlg(); ok('Pago registrado.'); finLoad();
    });
  }
  async function categoriesDlg() {
    var c = await sb.from('revenue_categories').select('id,code,name,grp,is_active').order('grp').order('name');
    var body = openDlg('Categorías de ingreso', table(['Código', 'Nombre', 'Grupo', 'Estado', ''], (c.data || []).map(function (x) {
      return ['<code>' + esc(x.code) + '</code>', esc(x.name), esc(GRP[x.grp]), x.is_active ? tag('Activa', 'ok') : tag('Inactiva'), btn(x.is_active ? 'Desactivar' : 'Activar', 'data-ct="' + esc(x.id) + '" data-on="' + (x.is_active ? 1 : 0) + '"')];
    })) + '<h3 style="margin-top:1rem">Nueva categoría</h3><form class="ac-inline" id="ct-f">' + '<label class="sr-only" for="ct-code">Código</label>' + inp('ct-code', '', 'placeholder="codigo_corto" maxlength="40"') +
      '<label class="sr-only" for="ct-name">Nombre</label>' + inp('ct-name', '', 'placeholder="Nombre" maxlength="120"') + '<label class="sr-only" for="ct-grp">Grupo</label><select class="control" id="ct-grp">' +
      options(Object.keys(GRP).map(function (k) { return [k, GRP[k]]; }), 'training') + '</select><button class="btn btn-primary btn-sm" type="submit">Agregar</button></form>');
    on(body, '[data-ct]', async function (ds) { var r = await sb.from('revenue_categories').update({ is_active: ds.on !== '1' }).eq('id', ds.ct); if (r.error) { fail(r.error, dlSt); return; } categoriesDlg(); });
    $('#ct-f', body).addEventListener('submit', async function (e) {
      e.preventDefault(); var code = val('ct-code').toLowerCase(), name = val('ct-name');
      if (!/^[a-z0-9_]{3,40}$/.test(code) || name.length < 3) { H.status(dlSt, 'Código en minúsculas (letras, números y _), nombre de al menos 3 caracteres.', 'error'); return; }
      var r = await sb.from('revenue_categories').insert({ code: code, name: name, grp: val('ct-grp') }); if (r.error) { fail(r.error, dlSt); return; } categoriesDlg();
    });
  }

  // ---------- Reconocimientos y becas ----------
  var LV = { excelencia_academica: 'Excelencia Académica', alto_rendimiento: 'Alto Rendimiento', merito_compromiso: 'Mérito y Compromiso' };
  var AST = { candidate: 'Candidato', approved: 'Aprobado', rejected: 'No aprobado' };
  var SST = { proposed: 'Propuesta', approved: 'Aprobada', used: 'Utilizada', expired: 'Vencida', rejected: 'No aprobada', revoked: 'Revocada' };
  LOAD.reconocimientos = async function (root) {
    var a = await sb.from('awards').select('id,period_label,level,score,score_breakdown,status,constancia_code,created_at,profile_id,who:profiles!awards_profile_id_fkey(first_name,last_name,public_recognition_consent)').order('created_at', { ascending: false }).limit(300);
    var s = await sb.from('scholarships').select('id,period_label,percentage,status,expires_on,conditions,created_at,who:profiles!scholarships_profile_id_fkey(first_name,last_name)').order('created_at', { ascending: false }).limit(300);
    if (a.error) { fail(a.error); return; }
    var y = new Date().getFullYear();
    root.innerHTML =
      card('Calcular candidatos', '<p class="ac-muted" style="margin-top:.5rem">Se calculan con los pesos configurados (calificaciones, finalización, evaluaciones, asignaciones y participación) y la nota mínima. El cálculo solo propone candidatos: la superadministración aprueba o rechaza cada uno.</p>' +
        '<form class="ac-inline" id="aw-f"><label for="aw-p">Período</label>' + inp('aw-p', y + '-S' + (new Date().getMonth() < 6 ? 1 : 2), 'maxlength="40"') +
        '<label for="aw-from">Desde</label>' + inp('aw-from', y + '-01-01', 'type="date"') + '<label for="aw-to">Hasta</label>' + inp('aw-to', y + '-12-31', 'type="date"') +
        '<button class="btn btn-primary btn-sm" type="submit">Calcular</button></form>') +
      card('Academy Excellence Awards', table(['Estudiante', 'Período', 'Nivel', 'Puntuación', 'Estado', 'Constancia', ''], (a.data || []).map(function (x) {
        var comp = (x.score_breakdown && x.score_breakdown.components) || {};
        return [fullName(x.who) + (x.who && x.who.public_recognition_consent ? '' : '<br><span class="ac-small">Sin autorización de publicación</span>'), esc(x.period_label), esc(LV[x.level]),
          n(x.score) + '<br><span class="ac-small">' + Object.keys(comp).map(function (k) { return esc(k) + ': ' + n(comp[k]); }).join(' · ') + '</span>',
          tag(AST[x.status], x.status === 'approved' ? 'ok' : x.status === 'candidate' ? 'run' : ''), esc(x.constancia_code || '—'),
          (x.status === 'candidate' && IS_SUPER ? btn('Aprobar', 'data-aa="' + esc(x.id) + '"', false) + ' ' + btn('Rechazar', 'data-ar="' + esc(x.id) + '"') : '') +
          (x.status === 'approved' ? btn('Proponer media beca', 'data-sp="' + esc(x.id) + '" data-pid="' + esc(x.profile_id) + '" data-per="' + esc(x.period_label) + '"') : '')];
      }), 'No hay reconocimientos calculados.')) +
      card('Medias becas', table(['Estudiante', 'Período', '%', 'Estado', 'Vence', 'Condiciones', ''], (s.data || []).map(function (x) {
        return [fullName(x.who), esc(x.period_label), n(x.percentage) + ' %', tag(SST[x.status], x.status === 'approved' ? 'ok' : x.status === 'proposed' ? 'run' : ''), d(x.expires_on), esc(x.conditions || '—'),
          x.status === 'proposed' && IS_SUPER ? btn('Aprobar', 'data-sa="' + esc(x.id) + '"', false) + ' ' + btn('Rechazar', 'data-sr="' + esc(x.id) + '"') : ''];
      }), 'No hay becas.'));
    $('#aw-f').addEventListener('submit', async function (e) {
      e.preventDefault();
      var r = await sb.rpc('compute_award_candidates', { p_period: val('aw-p'), p_from: val('aw-from'), p_to: val('aw-to') });
      if (r.error) { fail(r.error); return; } ok('Nuevos candidatos: ' + r.data + '.'); LOAD.reconocimientos(root);
    });
    var review = function (fnName, idKey, approve) { return async function (ds) {
      if (!confirm(approve ? '¿Aprobar? Se notificará al estudiante.' : '¿Rechazar?')) return;
      var args = {}; args[idKey] = ds.aa || ds.ar || ds.sa || ds.sr; args.p_approve = approve;
      var r = await sb.rpc(fnName, args); if (r.error) { fail(r.error); return; } LOAD.reconocimientos(root);
    }; };
    on(root, '[data-aa]', review('review_award', 'p_award', true));
    on(root, '[data-ar]', review('review_award', 'p_award', false));
    on(root, '[data-sa]', review('review_scholarship', 'p_id', true));
    on(root, '[data-sr]', review('review_scholarship', 'p_id', false));
    on(root, '[data-sp]', function (ds) {
      var body = openDlg('Proponer media beca', '<form class="ac-form" id="sp-f" novalidate><div class="form-grid">' +
        field('sp-per', 'Período', inp('sp-per', ds.per, 'maxlength="40"')) + field('sp-exp', 'Válida hasta', inp('sp-exp', '', 'type="date"')) +
        field('sp-cond', 'Condiciones', area('sp-cond', 'Aplicable a una capacitación de pago de la Academy dentro del período de vigencia.', 3), true) +
        '</div><p class="ac-small">El porcentaje sale de la configuración. La beca queda «propuesta» hasta que la superadministración la apruebe; nunca se aplica sola.</p><div class="ac-actions"><button class="btn btn-primary" type="submit">Proponer</button></div></form>');
      $('#sp-f', body).addEventListener('submit', async function (e) {
        e.preventDefault();
        var r = await sb.rpc('propose_scholarship', { p_profile: ds.pid, p_award: ds.sp, p_period: val('sp-per'), p_conditions: val('sp-cond'), p_expires: val('sp-exp') || null });
        if (r.error) { fail(r.error, dlSt); return; } closeDlg(); ok('Beca propuesta.'); LOAD.reconocimientos(root);
      });
    });
  };

  // ---------- Cuentas y roles ----------
  var DST = { open: 'Abierta', blocked: 'Bloqueada', scheduled: 'Programada', completed: 'Completada', cancelled: 'Cancelada' };
  var DBLK = { pending_payment: 'pago pendiente', submission_in_review: 'entrega en revisión', exam_pending_grading: 'examen por calificar', active_scholarship: 'beca vigente', open_conversation: 'consulta abierta' };
  LOAD.cuentas = async function (root) {
    var del = await sb.from('account_deletion_requests').select('id,reason,status,blocking_reasons,requested_at,scheduled_for,who:profiles!account_deletion_requests_profile_id_fkey(first_name,last_name,email)').order('requested_at', { ascending: false }).limit(200);
    var ro = await sb.from('user_roles').select('id,role,course_id,granted_at,courses(title),who:profiles!user_roles_profile_id_fkey(id,first_name,last_name,email)').neq('role', 'student').order('granted_at');
    if (del.error) { fail(del.error); return; }
    root.innerHTML =
      card('Solicitudes de baja y anonimización', '<p class="ac-muted" style="margin-top:.5rem">La anonimización borra los datos personales y es irreversible. Se bloquea si hay pagos, entregas, exámenes, becas o consultas pendientes.</p>' +
        table(['Persona', 'Motivo', 'Estado', 'Solicitud', 'Programada', ''], (del.data || []).map(function (x) {
          return [fullName(x.who) + '<br><span class="ac-small">' + esc(x.who ? x.who.email : '') + '</span>', esc({ inactivity: 'Inactividad', user_request: 'Pedido del titular', admin: 'Administración' }[x.reason]),
            tag(DST[x.status]) + ((x.blocking_reasons || []).length ? '<br><span class="ac-small">Bloqueos: ' + x.blocking_reasons.map(function (b) { return esc(DBLK[b] || b); }).join(', ') + '</span>' : ''),
            d(x.requested_at), d(x.scheduled_for),
            ['open', 'blocked', 'scheduled'].indexOf(x.status) > -1 ? btn('Anonimizar ahora', 'data-dz="' + esc(x.id) + '"') + ' ' + btn('Cancelar', 'data-dc="' + esc(x.id) + '"') : ''];
        }), 'Sin solicitudes.')) +
      card('Roles del personal', table(['Persona', 'Rol', 'Curso', 'Desde', ''], (ro.data || []).map(function (x) {
        return [fullName(x.who) + '<br><span class="ac-small">' + esc(x.who ? x.who.email : '') + '</span>', esc(ROLE[x.role]), esc(x.courses ? x.courses.title : '—'), d(x.granted_at),
          btn('Quitar', 'data-rr="' + esc(x.id) + '"')];
      })) + '<h3 style="margin-top:1.2rem">Asignar un rol</h3><p class="ac-small">La persona debe tener cuenta y, para usar el centro de control, activar la verificación en dos pasos.</p>' +
        '<form class="ac-form" id="rl-f" novalidate><div class="form-grid">' +
        field('rl-who', 'Persona', '<div class="ac-inline">' + inp('rl-q', '', 'aria-label="Buscar persona" placeholder="Nombre o correo"') + btn('Buscar', 'id="rl-find"') + '</div><select class="control" id="rl-who"><option value="">Busca primero…</option></select>', true) +
        field('rl-role', 'Rol', '<select class="control" id="rl-role">' + options([['instructor', 'Instructor (de un curso)'], ['academic_admin', 'Administrador académico'], ['superadmin', 'Superadministrador']], 'instructor') + '</select>') +
        field('rl-course', 'Curso (solo instructor)', '<select class="control" id="rl-course">' + courseOpts('', 'Selecciona…') + '</select>') +
        '</div><div class="ac-actions"><button class="btn btn-primary" type="submit">Asignar</button></div></form>') +
      card('Mantenimiento', '<p class="ac-muted" style="margin-top:.5rem">Limpieza de archivos y usuarios anonimizados, y envío de correos pendientes.</p><div class="ac-actions">' + btn('Ejecutar ahora', 'id="cu-jobs"') + '</div><div class="ac-status" id="cu-jobs-st" aria-live="polite"></div>');
    on(root, '[data-dz]', async function (ds) {
      if (!confirm('La anonimización es IRREVERSIBLE: se borran nombre, correo, teléfono, fotografía y notificaciones. ¿Continuar?')) return;
      var r = await sb.rpc('admin_process_deletion', { p_request: ds.dz, p_action: 'anonymize' });
      if (r.error) { fail(r.error); return; }
      if (r.data.status === 'blocked') H.status(st, 'No se puede anonimizar todavía: hay obligaciones pendientes (' + r.data.blocking_reasons.map(function (b) { return DBLK[b] || b; }).join(', ') + ').', 'error');
      else ok('Cuenta anonimizada. El usuario se eliminará de Auth en la próxima ejecución del mantenimiento.');
      LOAD.cuentas(root);
    });
    on(root, '[data-dc]', async function (ds) { var r = await sb.rpc('admin_process_deletion', { p_request: ds.dc, p_action: 'cancel' }); if (r.error) { fail(r.error); return; } LOAD.cuentas(root); });
    on(root, '[data-rr]', async function (ds) { if (!confirm('¿Quitar este rol?')) return; var r = await sb.from('user_roles').delete().eq('id', ds.rr); if (r.error) { fail(r.error); return; } LOAD.cuentas(root); });
    $('#rl-find').addEventListener('click', async function () {
      var r = await sb.rpc('admin_student_list', { p_search: val('rl-q') || null }); if (r.error) { fail(r.error); return; }
      $('#rl-who').innerHTML = (r.data || []).slice(0, 50).map(function (s) { return '<option value="' + esc(s.profile_id) + '">' + esc(s.full_name + ' · ' + s.email) + '</option>'; }).join('') || '<option value="">Sin resultados</option>';
    });
    $('#rl-f').addEventListener('submit', async function (e) {
      e.preventDefault();
      var who = val('rl-who'), role = val('rl-role'), course = val('rl-course') || null;
      if (!who) { H.fieldError($('#rl-who'), 'Elige la persona.'); return; }
      if (role === 'instructor' && !course) { H.fieldError($('#rl-course'), 'El instructor necesita un curso.'); return; }
      if (!confirm('¿Asignar el rol de ' + ROLE[role] + '?')) return;
      var r = await sb.from('user_roles').insert({ profile_id: who, role: role, course_id: role === 'instructor' ? course : null, granted_by: ME.profile_id });
      if (r.error) { fail(r.error); return; } ok('Rol asignado.'); LOAD.cuentas(root);
    });
    $('#cu-jobs').addEventListener('click', function () { runJobs($('#cu-jobs'), $('#cu-jobs-st')); });
  };

  // ---------- Configuración ----------
  var SETTINGS = {
    inactivity_days: 'Días de inactividad antes de suspender una cuenta de estudiante.',
    inactivity_warning_days: 'Días en los que se envían avisos preventivos (lista JSON, p. ej. [70,85,95]).',
    anonymization_grace_days: 'Días entre la suspensión por inactividad y la anonimización.',
    terms_version: 'Versión vigente de términos y privacidad (texto entre comillas).',
    award_weights: 'Pesos del cálculo de reconocimientos (JSON).',
    award_min_grade: 'Nota mínima para ser candidato a reconocimiento.',
    scholarship_percentage: 'Porcentaje de las medias becas.',
    scholarships_per_period: 'Máximo de becas aprobadas por período.'
  };
  LOAD.configuracion = async function (root) {
    var r = await sb.from('academy_settings').select('key,value,updated_at').order('key');
    if (r.error) { fail(r.error); return; }
    root.innerHTML = card('Configuración de la Academy', '<p class="ac-muted" style="margin-top:.5rem">Los valores se guardan como JSON. Cada cambio queda en la auditoría.</p>' +
      (r.data || []).map(function (x) {
        return '<form class="ac-form ac-setting" data-key="' + esc(x.key) + '" novalidate>' + field('set-' + x.key, x.key, area('set-' + x.key, JSON.stringify(x.value), 2), true) +
          '<p class="ac-small">' + esc(SETTINGS[x.key] || '') + ' · Actualizado ' + d(x.updated_at, true) + '</p><div class="ac-actions" style="margin-top:.4rem"><button class="btn btn-ghost btn-sm" type="submit">Guardar</button></div></form>';
      }).join(''));
    $$('.ac-setting', root).forEach(function (f) {
      f.addEventListener('submit', async function (e) {
        e.preventDefault();
        var k = f.dataset.key, ta = $('#set-' + k), v;
        try { v = JSON.parse(ta.value); } catch (x) { H.fieldError(ta, 'JSON no válido.'); return; }
        H.fieldError(ta, '');
        var u = await sb.from('academy_settings').update({ value: v, updated_by: ME.profile_id, updated_at: new Date().toISOString() }).eq('key', k);
        if (u.error) { fail(u.error); return; } ok('«' + k + '» guardado.');
      });
    });
  };

  // ---------- Auditoría ----------
  LOAD.auditoria = async function (root) {
    if (!LOADED.aud) {
      root.innerHTML = card('Registro de actividad', '<form class="ac-inline" id="au-f" role="search"><label class="sr-only" for="au-q">Filtrar por acción</label>' + inp('au-q', '', 'placeholder="Acción (p. ej. certificate, payments, account)"') +
        '<button class="btn btn-primary btn-sm" type="submit">Filtrar</button>' + btn('Exportar CSV', 'id="au-csv"') + '</form><div id="au-list"></div>');
      $('#au-f').addEventListener('submit', function (e) { e.preventDefault(); LOAD.auditoria(root); });
      $('#au-csv').addEventListener('click', function () {
        csv('auditoria.csv', ['Fecha', 'Acción', 'Entidad', 'Registro', 'Actor', 'Detalle'], (LOADED.logs || []).map(function (l) { return [l.created_at, l.action, l.entity, l.entity_id, l.actor_profile_id, JSON.stringify(l.metadata)]; }));
      });
      LOADED.aud = true;
    }
    var q = sb.from('activity_logs').select('id,action,entity,entity_id,metadata,actor_profile_id,created_at').order('id', { ascending: false }).limit(300);
    if (val('au-q')) q = q.ilike('action', '%' + val('au-q').replace(/[%_]/g, '') + '%');
    var r = await q; if (r.error) { fail(r.error); return; }
    LOADED.logs = r.data || [];
    var ids = Array.from(new Set(LOADED.logs.map(function (l) { return l.actor_profile_id; }).filter(Boolean)));
    var names = {};
    if (ids.length) { var p = await sb.from('profiles').select('id,first_name,last_name').in('id', ids); (p.data || []).forEach(function (x) { names[x.id] = fullName(x); }); }
    $('#au-list').innerHTML = table(['Fecha', 'Acción', 'Entidad', 'Registro', 'Actor', 'Detalle'], LOADED.logs.map(function (l) {
      var meta = JSON.stringify(l.metadata || {}); if (meta.length > 160) meta = meta.slice(0, 160) + '…';
      return [d(l.created_at, true), '<code>' + esc(l.action) + '</code>', esc(l.entity || ''), '<span class="ac-small">' + esc(l.entity_id || '') + '</span>', names[l.actor_profile_id] || (l.actor_profile_id ? '—' : 'Sistema'), '<span class="ac-small">' + esc(meta) + '</span>'];
    }), 'Sin registros.');
  };
})();
