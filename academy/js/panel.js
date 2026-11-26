/* =================================================================
   ACADEMY · Panel del estudiante
   Toda lectura y escritura pasa por las políticas RLS del servidor.
   ================================================================= */
(function () {
  'use strict';
  var H = window.HSA; if (!H) return;
  var sb = H.sb, $ = H.$, $$ = H.$$, esc = H.esc;
  var st = $('#pn-status');
  var ME = null, PROFILE = null, COURSES = [], ENROLL = {}, CERTS = [];
  var ROLE_NAMES = { superadmin: 'Superadministrador', academic_admin: 'Administrador académico', instructor: 'Instructor', student: 'Estudiante' };

  function empty(text) { return '<p class="ac-empty">' + esc(text) + '</p>'; }
  function toLogin(extra) { location.replace(H.base + 'index.html' + (extra || '')); }
  function fail(e) { H.status(st, H.message(e), 'error'); }

  // ---------------- Navegación por secciones ----------------
  var tabs = $$('.ac-nav [role=tab]');
  function go(sec, focus) {
    tabs.forEach(function (t) {
      var on = t.dataset.sec === sec;
      t.setAttribute('aria-selected', on ? 'true' : 'false'); t.tabIndex = on ? 0 : -1;
      $('#sec-' + t.dataset.sec).hidden = !on;
      if (on && focus) t.focus();
    });
    if (history.replaceState) history.replaceState(null, '', '#' + sec);
    if (sec === 'seguridad') { renderMfa(); loadSessions(); }
  }
  tabs.forEach(function (t, i) {
    t.id = 'tab-' + t.dataset.sec; $('#sec-' + t.dataset.sec).setAttribute('aria-labelledby', t.id);
    t.addEventListener('click', function () { go(t.dataset.sec); });
    t.addEventListener('keydown', function (e) {
      var k = e.key, n = null;
      if (k === 'ArrowDown' || k === 'ArrowRight') n = tabs[(i + 1) % tabs.length];
      if (k === 'ArrowUp' || k === 'ArrowLeft') n = tabs[(i - 1 + tabs.length) % tabs.length];
      if (n) { e.preventDefault(); go(n.dataset.sec, true); }
    });
  });
  $$('[data-go]').forEach(function (b) { b.addEventListener('click', function () { go(b.dataset.go, true); }); });

  // ---------------- Arranque ----------------
  (async function init() {
    var s = await sb.auth.getSession();
    if (!s.data.session) { toLogin(); return; }
    var lv = await H.aal();
    if (lv.nextLevel === 'aal2' && lv.currentLevel !== 'aal2') { toLogin('?mfa=1'); return; }

    var r = await sb.rpc('touch_activity');
    if (r.error && /profile_not_found/.test(r.error.message || '')) {
      H.status(st, 'No encontramos tu perfil. Si acabas de registrarte, espera unos segundos y recarga la página.', 'error');
      $('#pn-loading').hidden = true; return;
    }
    var acc = await sb.rpc('my_account');
    if (acc.error || !acc.data || !acc.data.length) { fail(acc.error); $('#pn-loading').hidden = true; return; }
    ME = acc.data[0];
    if (ME.status !== 'active') {
      $('#pn-loading').hidden = true;
      H.status(st, ME.status === 'anonymized' ? 'Esta cuenta fue dada de baja.' : 'Tu cuenta está suspendida. Escríbenos para reactivarla.', 'error');
      return;
    }
    $('#pn-name').textContent = ME.first_name ? ', ' + ME.first_name : '';
    if (ME.student_code) { $('#pn-code').hidden = false; $('#pn-code').textContent = ME.student_code; }
    var mail = (window.SITE_CONFIG || {}).email || '';
    $$('[data-mail]').forEach(function (a) { a.textContent = mail; a.href = 'mailto:' + mail; });

    var staff = (ME.roles || []).filter(function (x) { return x !== 'student'; });
    if (staff.length) {
      var b = $('#pn-staff-banner'); b.hidden = false;
      if (lv.currentLevel === 'aal2') {
        b.innerHTML = 'Tu cuenta tiene el rol de ' + esc(staff.map(function (x) { return ROLE_NAMES[x]; }).join(', ')) +
          '. <a class="btn btn-primary btn-sm" href="' + H.base + 'admin.html" style="margin-left:.6rem">Abrir el centro de control</a>';
      } else {
        b.textContent = 'Tu cuenta tiene un rol administrativo. Activa la verificación en dos pasos en «Seguridad»: sin ella, el sistema no te mostrará datos administrativos.';
      }
    }

    $('#pn-loading').hidden = true; $('#pn-app').hidden = false;
    var initial = (location.hash || '').slice(1);
    go(tabs.some(function (t) { return t.dataset.sec === initial; }) ? initial : 'resumen');

    await Promise.all([loadProfile(), loadCourses(), loadCerts(), loadNotifs()]);
    await syncLocal(true);
    renderCourses(); renderSummary();
    loadExams(); loadAssignments(); loadMaterials(); loadAwards(); loadPayments(); loadThreads();

    if (ME.consent_pending) openConsent();
    else maybeTour();
  })();

  sb.auth.onAuthStateChange(function (event) { if (event === 'SIGNED_OUT') toLogin(); });
  $('#pn-signout').addEventListener('click', async function () { await sb.auth.signOut(); });
  $('#pn-signout-all').addEventListener('click', async function () {
    if (!confirm('¿Cerrar la sesión en todos los dispositivos, incluido este?')) return;
    await sb.auth.signOut({ scope: 'global' });
  });

  // ---------------- Perfil ----------------
  var FIELDS = { first_name: '#pf-first', last_name: '#pf-last', phone: '#pf-phone', country: '#pf-country', city: '#pf-city',
    occupation: '#pf-occ', organization: '#pf-org', interest_area: '#pf-area' };

  async function loadProfile() {
    var r = await sb.from('profiles').select('id,email,first_name,last_name,phone,country,city,occupation,organization,interest_area,avatar_path,public_recognition_consent').eq('id', ME.profile_id).single();
    if (r.error) { fail(r.error); return; }
    PROFILE = r.data;
    Object.keys(FIELDS).forEach(function (k) { $(FIELDS[k]).value = PROFILE[k] || ''; });
    $('#pf-email').value = PROFILE.email; $('#pf-public').checked = !!PROFILE.public_recognition_consent;
    paintAvatar();
  }

  async function paintAvatar() {
    var initials = ((PROFILE.first_name || ' ')[0] + (PROFILE.last_name || ' ')[0]).trim().toUpperCase() || '·';
    var html = esc(initials);
    if (PROFILE.avatar_path) {
      var u = await sb.storage.from('avatars').createSignedUrl(PROFILE.avatar_path, 3600);
      if (!u.error) html = '<img src="' + esc(u.data.signedUrl) + '" alt="">';
    }
    $('#pn-avatar').innerHTML = html; $('#pf-avatar').innerHTML = html;
    $('#pf-remove').hidden = !PROFILE.avatar_path;
  }

  $('#f-profile').addEventListener('submit', async function (e) {
    e.preventDefault(); H.status(st, '');
    var data = {}, ok = true;
    Object.keys(FIELDS).forEach(function (k) { data[k] = $(FIELDS[k]).value.trim() || null; });
    ok = H.fieldError($('#pf-first'), data.first_name ? '' : 'Obligatorio.') && ok;
    ok = H.fieldError($('#pf-last'), data.last_name ? '' : 'Obligatorio.') && ok;
    ok = H.fieldError($('#pf-phone'), !data.phone || /^\+?[0-9 ()-]{7,20}$/.test(data.phone) ? '' : 'Teléfono no válido.') && ok;
    if (!ok) return;
    data.public_recognition_consent = $('#pf-public').checked;
    var btn = $('button[type=submit]', this); H.busy(btn, true, 'Guardando…');
    var r = await sb.from('profiles').update(data).eq('id', ME.profile_id);
    H.busy(btn, false);
    if (r.error) { fail(r.error); return; }
    Object.assign(PROFILE, data); $('#pn-name').textContent = ', ' + data.first_name; paintAvatar();
    H.status(st, 'Perfil actualizado.', 'ok');
  });

  $('#pf-file').addEventListener('change', async function () {
    var f = this.files[0]; this.value = '';
    if (!f) return;
    if (['image/jpeg', 'image/png', 'image/webp'].indexOf(f.type) < 0) { H.status(st, 'Formato no permitido. Usa JPG, PNG o WEBP.', 'error'); return; }
    if (f.size > 2 * 1024 * 1024) { H.status(st, 'La imagen supera 2 MB.', 'error'); return; }
    H.status(st, 'Subiendo fotografía…', 'info');
    var ext = { 'image/jpeg': 'jpg', 'image/png': 'png', 'image/webp': 'webp' }[f.type];
    var path = ME.profile_id + '/avatar-' + Date.now() + '.' + ext;
    var up = await sb.storage.from('avatars').upload(path, f, { contentType: f.type, upsert: false });
    if (up.error) { fail(up.error); return; }
    var old = PROFILE.avatar_path;
    var r = await sb.from('profiles').update({ avatar_path: path }).eq('id', ME.profile_id);
    if (r.error) { fail(r.error); return; }
    if (old) await sb.storage.from('avatars').remove([old]);
    PROFILE.avatar_path = path; paintAvatar(); H.status(st, 'Fotografía actualizada.', 'ok');
  });
  $('#pf-remove').addEventListener('click', async function () {
    var old = PROFILE.avatar_path; if (!old) return;
    var r = await sb.from('profiles').update({ avatar_path: null }).eq('id', ME.profile_id);
    if (r.error) { fail(r.error); return; }
    await sb.storage.from('avatars').remove([old]);
    PROFILE.avatar_path = null; paintAvatar();
  });

  // ---------------- Cursos ----------------
  async function loadCourses() {
    var c = await sb.from('courses').select('id,slug,title,level,tag,duration_minutes,public_url,is_free').eq('status', 'published').order('title');
    var e = await sb.from('enrollments').select('id,course_id,status,progress_pct,enrolled_at,completed_at').eq('profile_id', ME.profile_id);
    if (c.error) { fail(c.error); return; }
    COURSES = c.data || [];
    ENROLL = {};
    (e.data || []).forEach(function (x) { ENROLL[x.course_id] = x; });
  }

  function courseState(c) {
    var en = ENROLL[c.id];
    if (!en || en.status === 'cancelled') return 'available';
    if (en.status === 'completed') return 'done';
    return Number(en.progress_pct) > 0 ? 'progress' : 'enrolled';
  }

  var filter = 'all';
  $$('[data-filter]').forEach(function (b) {
    b.addEventListener('click', function () {
      filter = b.dataset.filter;
      $$('[data-filter]').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      renderCourses();
    });
  });

  function courseItem(c, compact) {
    var en = ENROLL[c.id], state = courseState(c), pct = en ? Number(en.progress_pct) : 0;
    var tag = { available: '<span class="ac-tag">Disponible</span>', enrolled: '<span class="ac-tag is-run">Inscrito</span>',
      progress: '<span class="ac-tag is-run">En progreso · ' + pct.toFixed(0) + ' %</span>', done: '<span class="ac-tag is-ok">Finalizado</span>' }[state];
    if (state === 'progress' && pct >= 100) tag = '<span class="ac-tag is-ok">Lectura completa</span>';
    var action = state === 'available'
      ? '<button class="btn btn-primary btn-sm" type="button" data-enroll="' + esc(c.id) + '">Matricularme</button>'
      : '<a class="btn btn-ghost btn-sm" href="' + esc(c.public_url || ('cursos/' + c.slug + '.html')) + '">' + (pct > 0 ? 'Continuar' : 'Empezar') + '</a>';
    return '<article class="ac-item"><div><h3>' + esc(c.title) + '</h3>' +
      '<p class="ac-meta">' + [c.tag, c.level, c.duration_minutes ? c.duration_minutes + ' min' : '', c.is_free ? 'Gratuito' : ''].filter(Boolean).map(esc).join(' · ') + '</p>' +
      (en ? '<div class="ac-progress" role="progressbar" aria-label="Avance" aria-valuemin="0" aria-valuemax="100" aria-valuenow="' + pct + '"><i style="width:' + pct + '%"></i></div>' : '') +
      (compact ? '' : '<p style="margin-top:.5rem">' + tag + '</p>') + '</div><div>' + action + '</div></article>';
  }

  function renderCourses() {
    var list = COURSES.filter(function (c) {
      var s = courseState(c);
      return filter === 'all' || s === filter || (filter === 'enrolled' && s !== 'available');
    });
    $('#pn-courses').innerHTML = list.length ? list.map(function (c) { return courseItem(c); }).join('') : empty('No hay cursos en esta categoría.');
    bindEnroll($('#pn-courses'));
  }

  function renderSummary() {
    var states = COURSES.map(courseState);
    $('#k-enrolled').textContent = states.filter(function (s) { return s !== 'available'; }).length;
    $('#k-progress').textContent = states.filter(function (s) { return s === 'progress'; }).length;
    $('#k-done').textContent = states.filter(function (s) { return s === 'done'; }).length;
    $('#k-certs').textContent = CERTS.filter(function (c) { return c.status === 'valid'; }).length;
    var mine = COURSES.filter(function (c) { return courseState(c) === 'progress' || courseState(c) === 'enrolled'; })
      .sort(function (a, b) { return Number(ENROLL[b.id].progress_pct) - Number(ENROLL[a.id].progress_pct); }).slice(0, 3);
    $('#pn-continue').innerHTML = mine.length ? mine.map(function (c) { return courseItem(c, true); }).join('')
      : empty('Aún no te has matriculado en ningún curso. Ve a «Mis capacitaciones» para elegir el primero.');
  }

  function bindEnroll(root) {
    $$('[data-enroll]', root).forEach(function (b) {
      b.addEventListener('click', async function () {
        H.busy(b, true, 'Matriculando…');
        var r = await sb.rpc('enroll_in_course', { p_course: b.dataset.enroll });
        if (r.error) { H.busy(b, false); fail(r.error); return; }
        await loadCourses(); await syncLocal(true); renderCourses(); renderSummary(); loadExams(); loadAssignments(); loadMaterials();
        H.status(st, 'Matrícula realizada. Tu avance en ese curso se registrará en tu cuenta.', 'ok');
      });
    });
  }

  // Trae el avance guardado en este navegador por las páginas de los cursos (clave hs-cursos-v1)
  async function syncLocal(quiet) {
    var local = {};
    try { local = JSON.parse(localStorage.getItem('hs-cursos-v1') || '{}'); } catch (e) { local = {}; }
    var n = 0;
    for (var i = 0; i < COURSES.length; i++) {
      var c = COURSES[i], en = ENROLL[c.id];
      if (!en || en.status === 'cancelled' || !local[c.slug] || !Array.isArray(local[c.slug].read)) continue;
      var ids = local[c.slug].read.filter(function (x) { return /^modulo-\d{1,2}$/.test(x); });
      for (var j = 0; j < ids.length; j++) {
        var r = await sb.rpc('mark_module_read', { p_course_slug: c.slug, p_anchor: ids[j] });
        if (!r.error) { en.progress_pct = r.data; n++; }
      }
    }
    if (!quiet) H.status(st, n ? 'Avance sincronizado.' : 'No hay avance nuevo en este navegador para tus cursos matriculados.', n ? 'ok' : 'info');
  }
  $('#pn-sync').addEventListener('click', async function () {
    var b = this; H.busy(b, true, 'Sincronizando…');
    await syncLocal(false); await loadCourses(); renderCourses(); renderSummary(); H.busy(b, false);
  });

  async function loadMaterials() {
    var ids = Object.keys(ENROLL);
    if (!ids.length) { $('#pn-materials').innerHTML = empty('Los materiales aparecen al matricularte en un curso.'); return; }
    var r = await sb.from('lessons').select('id,title,kind,storage_path,content_url,course_modules!inner(course_id,title)').in('course_modules.course_id', ids);
    var rows = (r.data || []).filter(function (l) { return l.storage_path || l.content_url; });
    if (!rows.length) { $('#pn-materials').innerHTML = empty('Tus cursos aún no tienen materiales descargables adicionales. El contenido completo está en la página de cada curso.'); return; }
    $('#pn-materials').innerHTML = '<div class="ac-list">' + rows.map(function (l) {
      return '<article class="ac-item"><div><h3>' + esc(l.title) + '</h3><p class="ac-meta">' + esc(l.course_modules.title) + '</p></div><div>' +
        (l.storage_path ? '<button class="btn btn-ghost btn-sm" type="button" data-file="' + esc(l.storage_path) + '">Descargar</button>'
          : '<a class="btn btn-ghost btn-sm" href="' + esc(l.content_url) + '" target="_blank" rel="noopener">Abrir</a>') + '</div></article>';
    }).join('') + '</div>';
    $$('[data-file]').forEach(function (b) {
      b.addEventListener('click', async function () {
        var u = await sb.storage.from('course-materials').createSignedUrl(b.dataset.file, 300);
        if (u.error) { fail(u.error); return; }
        location.href = u.data.signedUrl;
      });
    });
  }

  // ---------------- Evaluaciones ----------------
  var EXAM_MSG = {
    exam_not_available: 'La evaluación no está disponible.', exam_out_of_window: 'La evaluación está fuera del período habilitado.',
    course_not_completed: 'Completa todos los módulos del curso antes de presentar la evaluación final.',
    exam_already_passed: 'Ya aprobaste esta evaluación.', exam_pending_grading: 'Tu intento anterior está en revisión.',
    no_attempts_left: 'Ya usaste todos los intentos disponibles.', attempt_closed: 'El tiempo de la evaluación terminó.'
  };
  function examFail(e, box) {
    var m = String((e && e.message) || ''), k = Object.keys(EXAM_MSG).find(function (x) { return m.indexOf(x) > -1; });
    H.status(box || st, k ? EXAM_MSG[k] : H.message(e), 'error');
  }

  async function loadExams() {
    var ex = await sb.from('exams').select('id,title,course_id,is_certification,max_attempts,pass_percentage,time_limit_minutes,available_until,courses(title)').eq('status', 'published');
    var at = await sb.from('exam_attempts').select('id,exam_id,attempt_number,status,score_pct,passed,submitted_at,feedback,exams(title)').eq('profile_id', ME.profile_id).order('started_at', { ascending: false });
    var attempts = at.data || [];
    var exams = (ex.data || []).filter(function (x) { return !x.course_id || ENROLL[x.course_id]; });
    $('#pn-exams').innerHTML = exams.length ? '<div class="ac-list">' + exams.map(function (x) {
      var mine = attempts.filter(function (a) { return a.exam_id === x.id; });
      var passed = mine.some(function (a) { return a.passed; });
      var open = mine.some(function (a) { return a.status === 'in_progress'; });
      var review = mine.some(function (a) { return a.status === 'submitted'; });
      var left = x.max_attempts - mine.length;
      var en = ENROLL[x.course_id];
      var locked = x.is_certification && en && Number(en.progress_pct) < 100;
      var action = passed ? '<span class="ac-tag is-ok">Aprobada</span>'
        : review ? '<span class="ac-tag">En revisión</span>'
        : open ? '<button class="btn btn-primary btn-sm" type="button" data-exam="' + esc(x.id) + '">Continuar</button>'
        : left <= 0 ? '<span class="ac-tag">Sin intentos</span>'
        : locked ? '<span class="ac-tag" title="Completa los módulos del curso">Bloqueada</span>'
        : '<button class="btn btn-primary btn-sm" type="button" data-exam="' + esc(x.id) + '">Presentar</button>';
      return '<article class="ac-item"><div><h3>' + esc(x.title) + '</h3><p class="ac-meta">Intentos: ' + mine.length + ' de ' + x.max_attempts +
        ' · Aprobación: ' + Number(x.pass_percentage) + ' %' + (x.time_limit_minutes ? ' · ' + x.time_limit_minutes + ' min' : '') +
        (x.available_until ? ' · Hasta ' + H.fmtDate(x.available_until) : '') +
        (locked ? ' · Se habilita al completar el 100 % de los módulos (llevas ' + Math.round(Number(en.progress_pct)) + ' %)' : '') + '</p></div><div>' + action + '</div></article>';
    }).join('') + '</div>' : empty('No tienes evaluaciones disponibles. Matricúlate en un curso para ver su evaluación final.');
    $$('[data-exam]', $('#pn-exams')).forEach(function (b) { b.addEventListener('click', function () { openExam(b.dataset.exam, b); }); });
    var done = attempts.filter(function (a) { return a.status !== 'in_progress'; });
    $('#pn-attempts').innerHTML = done.length ? '<div class="ac-table-wrap"><table class="ac-table"><thead><tr><th>Evaluación</th><th>Intento</th><th>Fecha</th><th>Calificación</th><th>Resultado</th><th>Retroalimentación</th></tr></thead><tbody>' +
      done.map(function (a) {
        return '<tr><td>' + esc(a.exams ? a.exams.title : '') + '</td><td>' + a.attempt_number + '</td><td>' + H.fmtDate(a.submitted_at) + '</td><td>' +
          (a.score_pct == null ? '—' : Number(a.score_pct).toFixed(1) + ' %') + '</td><td>' +
          (a.status === 'submitted' ? 'En revisión' : a.passed ? 'Aprobado' : a.passed === false ? 'No aprobado' : '—') + '</td><td>' + esc(a.feedback || '—') + '</td></tr>';
      }).join('') + '</tbody></table></div>' : empty('Aún no has presentado evaluaciones.');
  }

  // Examen: preguntas sin respuestas correctas (las entrega el servidor), autoguardado y temporizador
  var EXAM = null, examTimer = null, saveTimer = null;
  var dExam = $('#dlg-exam'), exSt = $('#ex-status');
  function collect() {
    var out = {};
    (EXAM.questions || []).forEach(function (q) {
      if (q.type === 'open' || q.type === 'case') { var t = $('#q-' + q.id); if (t && t.value.trim()) out[q.id] = t.value.trim().slice(0, 4000); return; }
      var sel = $$('input[name="q-' + q.id + '"]:checked', dExam).map(function (i) { return i.value; });
      if (sel.length) out[q.id] = sel;
    });
    return out;
  }
  async function saveExam(quiet) {
    if (!EXAM) return;
    var r = await sb.rpc('save_exam_progress', { p_attempt: EXAM.attempt_id, p_responses: collect() });
    if (r.error) { if (!quiet) examFail(r.error, exSt); return false; }
    if (!quiet) H.status(exSt, 'Respuestas guardadas.', 'ok');
    return true;
  }
  function tick() {
    if (!EXAM || !EXAM.expires_at) { $('#ex-timer').textContent = ''; return; }
    var s = Math.max(0, Math.floor((new Date(EXAM.expires_at) - Date.now()) / 1000));
    $('#ex-timer').textContent = 'Tiempo restante: ' + Math.floor(s / 60) + ':' + ('0' + (s % 60)).slice(-2);
    if (s === 60) H.status(exSt, 'Queda 1 minuto. Tus respuestas se entregarán automáticamente al terminar el tiempo.', 'info');
    if (s <= 0) { clearInterval(examTimer); submitExam(true); }
  }
  async function openExam(id, btn) {
    H.busy(btn, true, 'Preparando…');
    var r = await sb.rpc('start_exam', { p_exam: id });
    H.busy(btn, false);
    if (r.error) { examFail(r.error); return; }
    EXAM = r.data;
    $('#ex-title').textContent = EXAM.title;
    $('#ex-meta').textContent = 'Intento ' + EXAM.attempt_number + ' de ' + EXAM.max_attempts + ' · Se aprueba con ' + Number(EXAM.pass_percentage) + ' % · ' + EXAM.questions.length + ' preguntas. Tus respuestas se guardan solas.';
    var saved = EXAM.responses || {};
    $('#ex-body').innerHTML = EXAM.questions.map(function (q, i) {
      var head = '<legend><b>' + (i + 1) + '.</b> ' + esc(q.prompt) + ' <span class="ac-small">(' + Number(q.points) + ' pt' + (Number(q.points) === 1 ? '' : 's') + ')</span></legend>';
      if (q.type === 'open' || q.type === 'case') {
        return '<fieldset class="ac-q">' + head + '<label class="sr-only" for="q-' + esc(q.id) + '">Respuesta</label><textarea class="control" id="q-' + esc(q.id) + '" rows="4" maxlength="4000">' + esc(saved[q.id] || '') + '</textarea></fieldset>';
      }
      var multi = q.type === 'multiple', chosen = [].concat(saved[q.id] || []);
      return '<fieldset class="ac-q">' + head + (multi ? '<p class="ac-small">Puedes marcar varias opciones.</p>' : '') + q.answers.map(function (a) {
        return '<label class="ac-check"><input type="' + (multi ? 'checkbox' : 'radio') + '" name="q-' + esc(q.id) + '" value="' + esc(a.id) + '"' +
          (chosen.indexOf(a.id) > -1 ? ' checked' : '') + '> <span>' + esc(a.label) + '</span></label>';
      }).join('') + '</fieldset>';
    }).join('');
    H.status(exSt, '');
    $('#ex-submit').disabled = false;
    dExam.showModal();
    clearInterval(examTimer); examTimer = setInterval(tick, 1000); tick();
  }
  $('#f-exam').addEventListener('change', function () { clearTimeout(saveTimer); saveTimer = setTimeout(function () { saveExam(true); }, 800); });
  $('#f-exam').addEventListener('input', function (e) { if (e.target.tagName === 'TEXTAREA') { clearTimeout(saveTimer); saveTimer = setTimeout(function () { saveExam(true); }, 2000); } });
  async function submitExam(auto) {
    if (!EXAM) return;
    var answers = collect(), missing = EXAM.questions.length - Object.keys(answers).length;
    if (!auto && missing > 0 && !confirm('Tienes ' + missing + ' pregunta(s) sin responder. ¿Entregar de todos modos?')) return;
    var b = $('#ex-submit'); H.busy(b, true, 'Entregando…');
    var r = await sb.rpc('submit_exam', { p_attempt: EXAM.attempt_id, p_responses: answers });
    H.busy(b, false);
    if (r.error) { examFail(r.error, exSt); return; }
    clearInterval(examTimer); b.disabled = true;
    var d = r.data || {};
    $('#ex-body').innerHTML = d.status === 'submitted'
      ? '<p class="ac-status is-info">Entregaste tu evaluación. Tiene preguntas que califica el equipo académico; te avisaremos cuando esté lista.</p>'
      : '<p class="ac-status ' + (d.passed ? 'is-ok' : 'is-error') + '">Calificación: <b>' + Number(d.score_pct).toFixed(1) + ' %</b>. ' +
        (d.passed ? '¡Aprobaste! Tu certificado se emitirá después de la revisión académica.' : 'No alcanzaste el mínimo. Repasa los módulos y vuelve a intentarlo si te quedan intentos.') + '</p>';
    H.status(exSt, '');
    $('#ex-close').textContent = 'Cerrar';
    EXAM = null; loadExams();
  }
  $('#f-exam').addEventListener('submit', function (e) { e.preventDefault(); submitExam(false); });
  $('#ex-close').addEventListener('click', async function () {
    if (EXAM) await saveExam(true);
    clearInterval(examTimer); EXAM = null; dExam.close(); $('#ex-close').textContent = 'Guardar y salir'; loadExams();
  });
  dExam.addEventListener('cancel', function (e) { e.preventDefault(); $('#ex-close').click(); });

  // ---------------- Asignaciones ----------------
  var SUB_STATE = { submitted: 'Entregada', in_review: 'En revisión', graded: 'Calificada', returned: 'Devuelta para corrección' };
  async function loadAssignments() {
    var ids = Object.keys(ENROLL);
    if (!ids.length) { $('#pn-assignments').innerHTML = empty('Las asignaciones aparecen al matricularte en un curso.'); return; }
    var a = await sb.from('assignments').select('id,title,instructions,due_at,max_score,courses(title)').eq('is_published', true).in('course_id', ids).order('due_at', { ascending: true });
    var s = await sb.from('assignment_submissions').select('id,assignment_id,status,submitted_at,score,feedback,file_path').eq('profile_id', ME.profile_id);
    var subs = {}; (s.data || []).forEach(function (x) { subs[x.assignment_id] = x; });
    var rows = a.data || [];
    $('#pn-assignments').innerHTML = rows.length ? '<div class="ac-list">' + rows.map(function (x) {
      var sub = subs[x.id];
      var late = x.due_at && new Date(x.due_at) < new Date();
      var can = !sub || sub.status === 'submitted' || sub.status === 'returned';
      return '<article class="ac-item"><div><h3>' + esc(x.title) + '</h3><p class="ac-meta">' + esc(x.courses ? x.courses.title : '') +
        (x.due_at ? ' · Fecha límite: ' + H.fmtDate(x.due_at, true) + (late ? ' (vencida)' : '') : '') +
        ' · Estado: ' + (sub ? SUB_STATE[sub.status] : 'Pendiente') +
        (sub && sub.score != null ? ' · Calificación: ' + Number(sub.score) + ' / ' + Number(x.max_score) : '') + '</p>' +
        (x.instructions ? '<p class="ac-small" style="margin-top:.4rem;white-space:pre-line">' + esc(x.instructions) + '</p>' : '') +
        (sub && sub.feedback ? '<p class="ac-small" style="margin-top:.4rem"><b>Comentarios:</b> ' + esc(sub.feedback) + '</p>' : '') +
        '</div><div class="ac-actions" style="margin:0">' +
        (can ? '<button class="btn btn-primary btn-sm" type="button" data-submit="' + esc(x.id) + '">' + (sub ? 'Reemplazar entrega' : 'Entregar') + '</button>' : '') +
        (sub && sub.file_path ? '<button class="btn btn-ghost btn-sm" type="button" data-myfile="' + esc(sub.file_path) + '">Ver mi archivo</button>' : '') +
        '</div></article>';
    }).join('') + '</div>' : empty('No tienes asignaciones por ahora.');
    $$('[data-submit]').forEach(function (b) {
      b.addEventListener('click', function () { var x = rows.find(function (r) { return r.id === b.dataset.submit; }); openSubmit(x, subs[x.id]); });
    });
    $$('[data-myfile]').forEach(function (b) {
      b.addEventListener('click', async function () {
        var u = await sb.storage.from('submissions').createSignedUrl(b.dataset.myfile, 300);
        if (u.error) { fail(u.error); return; } window.open(u.data.signedUrl, '_blank', 'noopener');
      });
    });
  }
  var SUB = null, dSub = $('#dlg-submit');
  function openSubmit(x, sub) {
    SUB = { a: x, sub: sub };
    $('#sb-title').textContent = 'Entregar: ' + x.title;
    $('#sb-meta').textContent = (x.courses ? x.courses.title : '') + (x.due_at ? ' · Fecha límite: ' + H.fmtDate(x.due_at, true) : '');
    $('#sb-file').value = ''; $('#sb-comment').value = sub && sub.comment || ''; H.status($('#sb-status'), '');
    dSub.showModal();
  }
  $('#sb-cancel').addEventListener('click', function () { dSub.close(); });
  $('#f-submit').addEventListener('submit', async function (e) {
    e.preventDefault();
    var f = $('#sb-file').files[0], comment = $('#sb-comment').value.trim(), box = $('#sb-status'), btn = e.submitter || $('button[type=submit]', this);
    if (!f && !(SUB.sub && SUB.sub.file_path) && !comment) { H.fieldError($('#sb-file'), 'Adjunta un archivo o escribe un comentario.'); return; }
    if (f && f.size > 10 * 1024 * 1024) { H.fieldError($('#sb-file'), 'El archivo supera 10 MB.'); return; }
    H.fieldError($('#sb-file'), '');
    H.busy(btn, true, 'Enviando…');
    var path = SUB.sub ? SUB.sub.file_path : null;
    if (f) {
      var clean = f.name.normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^\w.\-]+/g, '_').slice(-80);
      path = ME.profile_id + '/' + SUB.a.id + '/' + Date.now() + '-' + clean;
      var up = await sb.storage.from('submissions').upload(path, f, { upsert: false, contentType: f.type || 'application/octet-stream' });
      if (up.error) { H.busy(btn, false); H.status(box, H.message(up.error), 'error'); return; }
    }
    var row = { file_path: path, comment: comment || null, status: 'submitted' };
    var r = SUB.sub
      ? await sb.from('assignment_submissions').update(row).eq('id', SUB.sub.id)
      : await sb.from('assignment_submissions').insert(Object.assign({ assignment_id: SUB.a.id, profile_id: ME.profile_id }, row));
    H.busy(btn, false);
    if (r.error) { H.status(box, H.message(r.error), 'error'); return; }
    dSub.close(); H.status(st, 'Entrega enviada.', 'ok'); loadAssignments();
  });

  // ---------------- Certificados, reconocimientos y becas ----------------
  async function loadCerts() {
    var r = await sb.from('certificates').select('id,verification_code,course_title,academic_hours,completed_on,grade_pct,status,issued_at').eq('profile_id', ME.profile_id).order('issued_at', { ascending: false });
    CERTS = r.data || [];
    $('#pn-certs').innerHTML = CERTS.length ? '<div class="ac-list">' + CERTS.map(function (c) {
      var q = encodeURIComponent(c.verification_code);
      return '<article class="ac-item"><div><h3>' + esc(c.course_title) + '</h3><p class="ac-meta">Emitido el ' + H.fmtDate(c.issued_at) +
        (c.academic_hours ? ' · ' + Number(c.academic_hours) + ' horas' : '') + (c.grade_pct != null ? ' · Calificación ' + Number(c.grade_pct) + ' %' : '') +
        ' · Código <b>' + esc(c.verification_code) + '</b>' + (c.status === 'revoked' ? ' · <b>Revocado</b>' : '') + '</p></div><div class="ac-actions" style="margin:0">' +
        (c.status === 'valid' ? '<a class="btn btn-primary btn-sm" href="' + H.base + 'certificado.html?codigo=' + q + '" target="_blank" rel="noopener">Ver e imprimir</a>' : '') +
        '<a class="btn btn-ghost btn-sm" href="' + H.base + 'verificar.html?codigo=' + q + '">Verificar</a></div></article>';
    }).join('') + '</div>' : empty('Aún no tienes certificados. Se emiten al completar los módulos y aprobar la evaluación final, tras la revisión académica.');
  }
  var LEVELS = { excelencia_academica: 'Excelencia Académica', alto_rendimiento: 'Alto Rendimiento', merito_compromiso: 'Mérito y Compromiso' };
  var SCH = { proposed: 'En evaluación', approved: 'Aprobada', used: 'Utilizada', expired: 'Vencida', rejected: 'No aprobada', revoked: 'Revocada' };
  async function loadAwards() {
    var a = await sb.from('awards').select('period_label,level,score,status,constancia_code').eq('profile_id', ME.profile_id).eq('status', 'approved');
    var s = await sb.from('scholarships').select('period_label,percentage,status,expires_on,conditions').eq('profile_id', ME.profile_id).neq('status', 'proposed');
    var items = (a.data || []).map(function (x) {
      return '<article class="ac-item"><div><h3>Academy Excellence Awards · ' + esc(LEVELS[x.level] || x.level) + '</h3><p class="ac-meta">Período ' + esc(x.period_label) +
        ' · Puntuación ' + Number(x.score).toFixed(1) + ' · Constancia <b>' + esc(x.constancia_code || '') + '</b></p></div></article>';
    }).concat((s.data || []).map(function (x) {
      return '<article class="ac-item"><div><h3>Media beca (' + Number(x.percentage) + ' %)</h3><p class="ac-meta">Período ' + esc(x.period_label) + ' · ' + (SCH[x.status] || x.status) +
        (x.expires_on ? ' · Válida hasta ' + H.fmtDate(x.expires_on) : '') + '</p>' + (x.conditions ? '<p class="ac-small">' + esc(x.conditions) + '</p>' : '') + '</div></article>';
    }));
    $('#pn-awards').innerHTML = items.length ? '<div class="ac-list">' + items.join('') + '</div>' : empty('Aún no tienes reconocimientos ni becas.');
  }
  var PM = { pending: 'Pendiente', confirmed: 'Confirmado', rejected: 'Rechazado', refunded: 'Reembolsado', partially_refunded: 'Reembolso parcial' };
  async function loadPayments() {
    var r = await sb.from('payments').select('occurred_on,concept,amount,discount_amount,currency,status,reference').eq('profile_id', ME.profile_id).order('occurred_on', { ascending: false });
    var rows = r.data || [];
    $('#pn-payments').innerHTML = rows.length ? '<div class="ac-table-wrap"><table class="ac-table"><thead><tr><th>Fecha</th><th>Concepto</th><th>Monto</th><th>Descuento</th><th>Estado</th><th>Referencia</th></tr></thead><tbody>' +
      rows.map(function (p) {
        return '<tr><td>' + H.fmtDate(p.occurred_on) + '</td><td>' + esc(p.concept) + '</td><td>' + esc(p.currency) + ' ' + Number(p.amount).toLocaleString('es-DO', { minimumFractionDigits: 2 }) +
          '</td><td>' + (Number(p.discount_amount) ? esc(p.currency) + ' ' + Number(p.discount_amount).toLocaleString('es-DO', { minimumFractionDigits: 2 }) : '—') + '</td><td>' + (PM[p.status] || p.status) + '</td><td>' + esc(p.reference || '—') + '</td></tr>';
      }).join('') + '</tbody></table></div>' : empty('No hay pagos registrados a tu nombre.');
  }

  // ---------------- Consultas ----------------
  var TH = { open: 'Abierta', pending: 'Esperando respuesta', answered: 'Respondida', archived: 'Archivada' };
  var THREAD = null, dTh = $('#dlg-thread');
  async function loadThreads() {
    var r = await sb.from('message_threads').select('id,subject,status,updated_at,courses(title)').eq('profile_id', ME.profile_id).order('updated_at', { ascending: false });
    var rows = r.data || [];
    $('#pn-threads').innerHTML = rows.length ? '<div class="ac-list">' + rows.map(function (t) {
      return '<article class="ac-item"><div><h3>' + esc(t.subject) + '</h3><p class="ac-meta">' + (TH[t.status] || t.status) + ' · ' + H.fmtDate(t.updated_at, true) +
        (t.courses ? ' · ' + esc(t.courses.title) : '') + '</p></div><div><button class="btn btn-ghost btn-sm" type="button" data-thread="' + esc(t.id) + '">Abrir</button></div></article>';
    }).join('') + '</div>' : empty('No tienes consultas.');
    $$('[data-thread]').forEach(function (b) { b.addEventListener('click', function () { openThread(rows.find(function (t) { return t.id === b.dataset.thread; })); }); });
  }
  async function openThread(t) {
    THREAD = t || null;
    H.status($('#th-status'), ''); $('#th-msg').value = '';
    $('#th-subject-f').hidden = !!t; $('#th-course-f').hidden = !!t;
    $('#th-title').textContent = t ? t.subject : 'Nueva consulta';
    $('#th-send').textContent = t ? 'Responder' : 'Enviar consulta';
    if (!t) {
      $('#th-subject').value = '';
      $('#th-course').innerHTML = '<option value="">Ninguna</option>' + COURSES.filter(function (c) { return ENROLL[c.id]; })
        .map(function (c) { return '<option value="' + esc(c.id) + '">' + esc(c.title) + '</option>'; }).join('');
      $('#th-body').innerHTML = ''; $('#f-thread').hidden = false;
    } else {
      var m = await sb.from('messages').select('id,body,created_at,sender_profile_id,read_at').eq('thread_id', t.id).order('created_at');
      var msgs = m.data || [];
      $('#th-body').innerHTML = '<div class="ac-thread">' + msgs.map(function (x) {
        var me = x.sender_profile_id === ME.profile_id;
        return '<div class="ac-msg' + (me ? ' is-me' : '') + '"><p class="ac-small"><b>' + (me ? 'Tú' : 'Equipo Academy') + '</b> · ' + H.fmtDate(x.created_at, true) + '</p><p style="white-space:pre-line">' + esc(x.body) + '</p></div>';
      }).join('') + '</div>';
      $('#f-thread').hidden = t.status === 'archived';
      var unread = msgs.filter(function (x) { return x.sender_profile_id !== ME.profile_id && !x.read_at; }).map(function (x) { return x.id; });
      if (unread.length) await sb.from('messages').update({ read_at: new Date().toISOString() }).in('id', unread);
    }
    if (!dTh.open) dTh.showModal();
  }
  $('#pn-newthread').addEventListener('click', function () { openThread(null); });
  $('#th-close').addEventListener('click', function () { dTh.close(); loadThreads(); });
  $('#f-thread').addEventListener('submit', async function (e) {
    e.preventDefault();
    var body = $('#th-msg').value.trim(), box = $('#th-status'), btn = $('#th-send');
    if (!H.fieldError($('#th-msg'), body.length < 5 ? 'Escribe tu mensaje (mínimo 5 caracteres).' : '')) return;
    var t = THREAD;
    H.busy(btn, true, 'Enviando…');
    if (!t) {
      var subj = $('#th-subject').value.trim();
      if (!H.fieldError($('#th-subject'), subj.length < 3 ? 'Escribe un asunto.' : '')) { H.busy(btn, false); return; }
      var nt = await sb.from('message_threads').insert({ profile_id: ME.profile_id, subject: subj, course_id: $('#th-course').value || null, status: 'open' }).select('id,subject,status,updated_at').single();
      if (nt.error) { H.busy(btn, false); H.status(box, H.message(nt.error), 'error'); return; }
      t = nt.data;
    }
    var r = await sb.from('messages').insert({ thread_id: t.id, sender_profile_id: ME.profile_id, body: body.slice(0, 4000) });
    H.busy(btn, false);
    if (r.error) { H.status(box, H.message(r.error), 'error'); return; }
    t.status = 'pending'; openThread(t); loadThreads();
  });

  // ---------------- Notificaciones ----------------
  async function loadNotifs() {
    var r = await sb.from('notifications').select('id,kind,title,body,link,read_at,created_at').eq('profile_id', ME.profile_id).order('created_at', { ascending: false }).limit(50);
    var rows = r.data || [];
    var unread = rows.filter(function (n) { return !n.read_at; }).length;
    $('#pn-unread').textContent = unread ? String(unread) : '';
    $('#pn-notifs').innerHTML = rows.length ? '<div class="ac-list">' + rows.map(function (n) {
      return '<article class="ac-item"' + (n.read_at ? '' : ' style="border-color:var(--teal)"') + '><div><h3>' + esc(n.title) + '</h3><p class="ac-meta">' + H.fmtDate(n.created_at, true) + '</p>' +
        (n.body ? '<p style="margin-top:.4rem;font-size:.9rem">' + esc(n.body) + '</p>' : '') + '</div><div>' +
        (n.read_at ? '<span class="ac-tag">Leída</span>' : '<button class="ac-link" type="button" data-read="' + esc(n.id) + '">Marcar como leída</button>') + '</div></article>';
    }).join('') + '</div>' : empty('No tienes notificaciones.');
    $$('[data-read]').forEach(function (b) {
      b.addEventListener('click', async function () { await sb.from('notifications').update({ read_at: new Date().toISOString() }).eq('id', b.dataset.read); loadNotifs(); });
    });
  }
  $('#pn-readall').addEventListener('click', async function () {
    await sb.from('notifications').update({ read_at: new Date().toISOString() }).is('read_at', null).eq('profile_id', ME.profile_id); loadNotifs();
  });

  // ---------------- Seguridad: 2FA ----------------
  async function renderMfa() {
    var box = $('#mfa-box');
    var f = await sb.auth.mfa.listFactors();
    var totp = (f.data && f.data.all || []).filter(function (x) { return x.factor_type === 'totp'; });
    var verified = totp.filter(function (x) { return x.status === 'verified'; });
    // Limpia intentos de activación que quedaron sin terminar
    for (var i = 0; i < totp.length; i++) if (totp[i].status !== 'verified') await sb.auth.mfa.unenroll({ factorId: totp[i].id });

    if (!verified.length) {
      box.innerHTML = '<p class="ac-muted">Protege tu cuenta con un código de una aplicación de autenticación (Google Authenticator, Microsoft Authenticator u otra compatible con TOTP), además de tu contraseña.</p>' +
        '<div class="ac-actions"><button class="btn btn-primary" type="button" id="mfa-start">Activar verificación en dos pasos</button></div>';
      $('#mfa-start').addEventListener('click', startEnroll);
      return;
    }
    var left = await sb.rpc('recovery_codes_remaining');
    box.innerHTML = '<p class="ac-status is-ok" style="margin-top:0">La verificación en dos pasos está activa desde el ' + H.fmtDate(verified[0].created_at) + '.</p>' +
      '<p class="ac-muted" style="margin-top:.8rem">Códigos de recuperación disponibles: <b>' + (left.error ? '—' : left.data) + '</b> de 10.</p>' +
      '<div class="ac-actions"><button class="btn btn-ghost btn-sm" type="button" id="mfa-codes">Generar nuevos códigos de recuperación</button>' +
      '<button class="btn btn-ghost btn-sm" type="button" id="mfa-off">Desactivar</button></div><div id="mfa-out"></div>';
    $('#mfa-codes').addEventListener('click', function () { showCodes($('#mfa-out')); });
    $('#mfa-off').addEventListener('click', async function () {
      if (!confirm('¿Desactivar la verificación en dos pasos? Tu cuenta quedará protegida solo con la contraseña.')) return;
      var r = await sb.auth.mfa.unenroll({ factorId: verified[0].id });
      if (r.error) { fail(r.error); return; }
      await sb.auth.refreshSession(); H.status(st, 'Verificación en dos pasos desactivada.', 'info'); renderMfa();
    });
  }

  async function startEnroll() {
    var box = $('#mfa-box');
    var r = await sb.auth.mfa.enroll({ factorType: 'totp', friendlyName: 'Autenticador ' + new Date().toISOString().slice(0, 10) });
    if (r.error) { fail(r.error); return; }
    var id = r.data.id;
    box.innerHTML = '<ol class="ac-stack" style="list-style:decimal;padding-left:1.2rem"><li>Abre tu aplicación de autenticación y escanea este código QR.</li><li>Escribe el código de 6 dígitos que aparece en la aplicación.</li></ol>' +
      '<div class="ac-qr"><img id="mfa-qr" alt="Código QR para configurar la verificación en dos pasos"><div><p class="ac-small">¿No puedes escanear? Escribe esta clave en la aplicación:</p><p class="ac-secret" id="mfa-secret"></p></div></div>' +
      '<form class="ac-form ac-stack" id="f-mfa-enroll" novalidate style="margin-top:1rem"><div class="field"><label for="mfa-code">Código de 6 dígitos</label>' +
      '<input class="control ac-code" id="mfa-code" inputmode="numeric" autocomplete="one-time-code" maxlength="6" required><span class="error"></span></div>' +
      '<div class="ac-actions"><button class="btn btn-primary" type="submit">Confirmar y activar</button><button class="ac-link" type="button" id="mfa-cancel">Cancelar</button></div></form><div id="mfa-out"></div>';
    $('#mfa-qr').src = r.data.totp.qr_code;            // data:image/svg+xml generado por Supabase
    $('#mfa-secret').textContent = r.data.totp.secret;
    $('#mfa-cancel').addEventListener('click', async function () { await sb.auth.mfa.unenroll({ factorId: id }); renderMfa(); });
    $('#f-mfa-enroll').addEventListener('submit', async function (e) {
      e.preventDefault();
      var c = $('#mfa-code'), code = c.value.replace(/\D/g, '');
      if (!H.fieldError(c, code.length === 6 ? '' : 'El código tiene 6 dígitos.')) return;
      var btn = $('button[type=submit]', this); H.busy(btn, true, 'Verificando…');
      var v = await sb.auth.mfa.challengeAndVerify({ factorId: id, code: code });
      H.busy(btn, false);
      if (v.error) { c.value = ''; fail(v.error); return; }
      H.status(st, 'Verificación en dos pasos activada. Guarda ahora tus códigos de recuperación.', 'ok');
      box.innerHTML = '<div id="mfa-out"></div>';
      await showCodes($('#mfa-out'), true);
    });
  }

  async function showCodes(out, fresh) {
    if (!fresh && !confirm('Los códigos anteriores dejarán de funcionar. ¿Generar nuevos?')) return;
    var r = await sb.rpc('generate_recovery_codes');
    if (r.error) { fail(r.error); return; }
    var codes = r.data || [];
    out.innerHTML = '<div class="ac-note"><strong>Guarda estos códigos en un lugar seguro.</strong> Cada uno sirve una sola vez si pierdes tu aplicación de autenticación. No volverán a mostrarse.</div>' +
      '<ul class="ac-codes">' + codes.map(function (c) { return '<li>' + esc(c) + '</li>'; }).join('') + '</ul>' +
      '<div class="ac-actions"><button class="btn btn-ghost btn-sm" type="button" id="codes-copy">Copiar</button><button class="btn btn-ghost btn-sm" type="button" id="codes-dl">Descargar .txt</button>' +
      '<button class="btn btn-primary btn-sm" type="button" id="codes-done">Ya los guardé</button></div>';
    var text = 'HANSLIERY ACADEMY · Códigos de recuperación\n' + new Date().toLocaleString('es-DO') + '\n\n' + codes.join('\n') + '\n\nCada código sirve una sola vez.\n';
    $('#codes-copy').addEventListener('click', function () { navigator.clipboard && navigator.clipboard.writeText(text); H.status(st, 'Códigos copiados.', 'ok'); });
    $('#codes-dl').addEventListener('click', function () {
      var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([text], { type: 'text/plain' }));
      a.download = 'academy-codigos-recuperacion.txt'; document.body.appendChild(a); a.click(); a.remove();
    });
    $('#codes-done').addEventListener('click', renderMfa);
  }

  // ---------------- Seguridad: contraseña, sesiones y baja ----------------
  H.bindPasswordUI($('#f-pass'), '#pw-new', '#pw-new2');
  $('#f-pass').addEventListener('submit', async function (e) {
    e.preventDefault(); H.status(st, '');
    var btn = $('button[type=submit]', this); H.busy(btn, true, 'Validando…');
    var perr = await H.validatePassword($('#pw-new').value, $('#pw-new2').value, PROFILE && PROFILE.email);
    if (perr) { H.busy(btn, false); H.fieldError($('#pw-new'), perr); return; }
    H.fieldError($('#pw-new'), '');
    var r = await sb.auth.updateUser({ password: $('#pw-new').value });
    H.busy(btn, false);
    if (r.error) { fail(r.error); return; }
    this.reset(); H.bindPasswordUI($('#f-pass'), '#pw-new', '#pw-new2');
    H.status(st, 'Contraseña actualizada.', 'ok');
  });

  async function loadSessions() {
    var r = await sb.rpc('my_access_history');
    var rows = r.data || [];
    $('#pn-sessions').innerHTML = rows.length ? rows.map(function (s) {
      var ua = String(s.user_agent || '');
      var dev = /Mobile|Android|iPhone/i.test(ua) ? 'Móvil' : 'Computadora';
      var br = /Edg\//.test(ua) ? 'Edge' : /Chrome\//.test(ua) ? 'Chrome' : /Firefox\//.test(ua) ? 'Firefox' : /Safari\//.test(ua) ? 'Safari' : 'Navegador';
      return '<tr><td>' + H.fmtDate(s.started_at, true) + '</td><td>' + H.fmtDate(s.last_seen_at, true) + '</td><td>' + esc(dev + ' · ' + br) + '</td><td>' + esc(s.ip || '—') + '</td><td>' + (s.aal === 'aal2' ? 'Con 2FA' : 'Contraseña') + '</td></tr>';
    }).join('') : '<tr><td colspan="5">Sin registros.</td></tr>';
  }

  $('#pn-delete').addEventListener('click', async function () {
    if (!confirm('¿Solicitar la baja de tu cuenta? Se revisará que no tengas obligaciones pendientes antes de anonimizar tus datos.')) return;
    var r = await sb.rpc('request_account_deletion');
    if (r.error) { fail(r.error); return; }
    H.status(st, 'Solicitud de baja registrada. Te avisaremos por esta vía.', 'ok');
  });

  // ---------------- Consentimiento (Google) ----------------
  function openConsent() {
    var d = $('#dlg-consent'); d.showModal();
    d.addEventListener('cancel', function (e) { e.preventDefault(); });
    $('#dc-cancel').addEventListener('click', async function () { await sb.auth.signOut(); });
    $('#f-consent').addEventListener('submit', async function (e) {
      e.preventDefault();
      if (!$('#dc-terms').checked || !$('#dc-privacy').checked) { H.status($('#dc-status'), 'Debes marcar ambas casillas para continuar.', 'error'); return; }
      var r = await sb.rpc('accept_terms', { p_version: H.cfg.terms_version, p_privacy: true });
      if (r.error) { H.status($('#dc-status'), H.message(r.error), 'error'); return; }
      d.close(); ME.consent_pending = false;
      H.status(st, 'Gracias. Completa tus datos en «Mi perfil» (teléfono, país, ciudad y ocupación).', 'info');
      maybeTour();
    });
  }

  // ---------------- Tutorial inicial ----------------
  var TOUR = [
    'Desde <b>Mis capacitaciones</b> te matriculas en los cursos. Tu avance se guarda en tu cuenta mientras lees cada módulo.',
    'En <b>Mis evaluaciones</b> y <b>Mis asignaciones</b> verás lo pendiente, tus calificaciones y la retroalimentación.',
    'En <b>Mis certificados</b> descargas tus certificados con su código de verificación.',
    'En <b>Seguridad</b> te recomendamos activar la verificación en dos pasos. Recuerda: tras 100 días sin actividad, la cuenta se suspende.'
  ];
  async function maybeTour() {
    var r = await sb.from('student_accounts').select('tutorial_seen').eq('profile_id', ME.profile_id).maybeSingle();
    if (r.error || !r.data || r.data.tutorial_seen) return;
    var d = $('#dlg-tour'), i = 0;
    var paint = function () {
      $('#dt-body').innerHTML = TOUR[i];
      $$('.ac-steps i', d).forEach(function (x, k) { x.classList.toggle('is-on', k <= i); });
      $('#dt-next').textContent = i === TOUR.length - 1 ? 'Empezar' : 'Siguiente';
    };
    var done = async function () { d.close(); await sb.from('student_accounts').update({ tutorial_seen: true }).eq('profile_id', ME.profile_id); };
    $('#dt-next').addEventListener('click', function () { if (i < TOUR.length - 1) { i++; paint(); } else done(); });
    $('#dt-skip').addEventListener('click', done);
    paint(); d.showModal();
  }
})();
