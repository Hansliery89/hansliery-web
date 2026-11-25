/* =================================================================
   ACADEMY · Acceso: inicio de sesión, registro, 2FA y contraseñas
   ================================================================= */
(function () {
  'use strict';
  var H = window.HSA; if (!H) return;
  var sb = H.sb, $ = H.$, $$ = H.$$;
  var st = $('#ac-status');
  var PANEL_URL = H.base + 'panel.html';
  var panels = ['p-login', 'p-signup', 'p-mfa', 'p-recovery', 'p-reset', 'p-newpass'];
  var tabs = [$('#tab-login'), $('#tab-signup')];

  function show(id) {
    panels.forEach(function (p) { $('#' + p).hidden = p !== id; });
    var tabbed = id === 'p-login' || id === 'p-signup';
    $('.ac-tabs').hidden = !tabbed;
    tabs.forEach(function (t) {
      var on = t.getAttribute('aria-controls') === id;
      t.setAttribute('aria-selected', on ? 'true' : 'false'); t.tabIndex = on ? 0 : -1;
    });
    var first = $('#' + id + ' input');
    if (first && !tabbed) setTimeout(function () { first.focus(); }, 60);
  }

  // Pestañas accesibles (flechas izquierda/derecha)
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { H.status(st, ''); show(t.getAttribute('aria-controls')); });
    t.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      var n = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length];
      n.focus(); n.click();
    });
  });
  $$('[data-show]').forEach(function (b) { b.addEventListener('click', function () { H.status(st, ''); show(b.dataset.show); }); });
  $$('[data-tab]').forEach(function (b) { b.addEventListener('click', function () { H.status(st, ''); $('#' + b.dataset.tab).click(); }); });
  if (location.hash === '#registro') show('p-signup');

  async function afterLogin() {
    var lv = await H.aal();
    if (lv.nextLevel === 'aal2' && lv.currentLevel !== 'aal2') { show('p-mfa'); return; }
    location.replace(PANEL_URL);
  }

  // ---------------- Google ----------------
  $$('[data-google]').forEach(function (b) {
    b.addEventListener('click', async function () {
      H.busy(b, true, 'Abriendo Google…');
      var r = await sb.auth.signInWithOAuth({ provider: 'google', options: { redirectTo: PANEL_URL, queryParams: { prompt: 'select_account' } } });
      if (r.error) { H.busy(b, false); H.status(st, H.message(r.error), 'error'); }
    });
  });

  // ---------------- Iniciar sesión ----------------
  var fLogin = $('#f-login');
  fLogin.addEventListener('submit', async function (e) {
    e.preventDefault(); H.status(st, '');
    var em = $('#l-email'), pw = $('#l-pass'), email = H.normEmail(em.value);
    var ok = H.fieldError(em, H.validEmail(email) ? '' : 'Escribe un correo válido.');
    ok = H.fieldError(pw, pw.value ? '' : 'Escribe tu contraseña.') && ok;
    if (!ok) return;
    var btn = $('button[type=submit]', fLogin); H.busy(btn, true, 'Verificando…');
    var r = await sb.auth.signInWithPassword({ email: email, password: pw.value });
    H.busy(btn, false);
    if (r.error) { H.status(st, H.message(r.error), 'error'); pw.value = ''; return; }
    afterLogin();
  });

  // ---------------- Registro ----------------
  var fSign = $('#f-signup');
  H.bindPasswordUI(fSign, '#s-pass', '#s-pass2');
  var sending = false;
  fSign.addEventListener('submit', async function (e) {
    e.preventDefault(); H.status(st, '');
    if (sending) return;                                   // evita envíos dobles
    var v = function (id) { return $(id).value.trim(); };
    var email = H.normEmail(v('#s-email'));
    var ok = true;
    [['#s-first', 'Escribe tus nombres.'], ['#s-last', 'Escribe tus apellidos.'], ['#s-country', 'Indica tu país.'],
     ['#s-city', 'Indica tu ciudad.'], ['#s-occ', 'Indica tu profesión u ocupación.'], ['#s-area', 'Selecciona un área.']]
      .forEach(function (r) { ok = H.fieldError($(r[0]), v(r[0]) ? '' : r[1]) && ok; });
    ok = H.fieldError($('#s-email'), H.validEmail(email) ? '' : 'Escribe un correo válido.') && ok;
    ok = H.fieldError($('#s-phone'), /^\+?[0-9 ()-]{7,20}$/.test(v('#s-phone')) ? '' : 'Escribe un teléfono válido (7 a 20 dígitos).') && ok;
    var consent = $('#s-terms').checked && $('#s-privacy').checked;
    $('#s-consent-e').textContent = consent ? '' : 'Debes aceptar los términos y el tratamiento de datos para crear la cuenta.';
    ok = consent && ok;
    var btn = $('button[type=submit]', fSign);
    if (!ok) { H.status(st, 'Revisa los campos marcados.', 'error'); return; }
    sending = true; H.busy(btn, true, 'Validando contraseña…');
    var perr = await H.validatePassword($('#s-pass').value, $('#s-pass2').value, email);
    if (perr) { sending = false; H.busy(btn, false); H.fieldError($('#s-pass'), perr); H.status(st, perr, 'error'); return; }
    H.fieldError($('#s-pass'), '');
    H.busy(btn, true, 'Creando cuenta…');
    var r = await sb.auth.signUp({
      email: email, password: $('#s-pass').value,
      options: {
        emailRedirectTo: PANEL_URL,
        data: {
          first_name: v('#s-first'), last_name: v('#s-last'), phone: v('#s-phone'), country: v('#s-country'),
          city: v('#s-city'), occupation: v('#s-occ'), organization: v('#s-org'), interest_area: v('#s-area'),
          terms_accepted: 'true', terms_version: H.cfg.terms_version, privacy_consent: 'true'
        }
      }
    });
    sending = false; H.busy(btn, false);
    if (r.error && r.error.code !== 'user_already_exists') { H.status(st, H.message(r.error), 'error'); return; }
    if (r.data && r.data.session) { location.replace(PANEL_URL); return; }   // si la verificación por correo estuviera desactivada
    fSign.reset(); H.bindPasswordUI(fSign, '#s-pass', '#s-pass2');
    // Mensaje neutro: no revela si el correo ya tenía cuenta (protección contra enumeración)
    H.status(st, 'Listo. Si el correo no estaba registrado, te enviamos un enlace de verificación a ' + email +
      '. Ábrelo para activar tu cuenta (revisa también la carpeta de spam). Si ya tenías cuenta, inicia sesión o recupera tu contraseña.', 'ok');
  });

  // ---------------- 2FA ----------------
  var fMfa = $('#f-mfa');
  fMfa.addEventListener('submit', async function (e) {
    e.preventDefault(); H.status(st, '');
    var c = $('#m-code'); var code = c.value.replace(/\D/g, '');
    if (!H.fieldError(c, code.length === 6 ? '' : 'El código tiene 6 dígitos.')) return;
    var btn = $('button[type=submit]', fMfa); H.busy(btn, true, 'Verificando…');
    var f = await sb.auth.mfa.listFactors();
    var totp = f.data && f.data.totp && f.data.totp.find(function (x) { return x.status === 'verified'; });
    if (!totp) { H.busy(btn, false); location.replace(PANEL_URL); return; }
    var r = await sb.auth.mfa.challengeAndVerify({ factorId: totp.id, code: code });
    H.busy(btn, false);
    if (r.error) { c.value = ''; H.status(st, H.message(r.error), 'error'); return; }
    location.replace(PANEL_URL);
  });

  var fRec = $('#f-recovery');
  fRec.addEventListener('submit', async function (e) {
    e.preventDefault(); H.status(st, '');
    var c = $('#r-code'); var code = c.value.trim().toUpperCase();
    if (!H.fieldError(c, /^[A-Z0-9]{4}-?[A-Z0-9]{4}$/.test(code) ? '' : 'El código tiene el formato XXXX-XXXX.')) return;
    var btn = $('button[type=submit]', fRec); H.busy(btn, true, 'Validando…');
    var r = await sb.functions.invoke('mfa-recover', { body: { code: code } });
    H.busy(btn, false);
    if (r.error) {
      var ctx = r.error.context, body = null;
      try { body = ctx && ctx.json ? await ctx.json() : null; } catch (x) { /* sin cuerpo */ }
      var err = body && body.error;
      H.status(st, err === 'too_many_attempts' ? 'Demasiados intentos. Espera 15 minutos.' :
        err === 'invalid_code' ? 'El código no es válido o ya fue usado.' : H.message(r.error), 'error');
      return;
    }
    await sb.auth.refreshSession();
    H.status(st, 'Listo: se desactivó la verificación en dos pasos. Vuelve a activarla desde tu perfil.', 'ok');
    setTimeout(function () { location.replace(PANEL_URL + '#seguridad'); }, 1800);
  });

  $$('[data-signout]').forEach(function (b) {
    b.addEventListener('click', async function () { await sb.auth.signOut(); show('p-login'); });
  });

  // ---------------- Recuperación de contraseña ----------------
  var fReset = $('#f-reset');
  fReset.addEventListener('submit', async function (e) {
    e.preventDefault(); H.status(st, '');
    var em = $('#rs-email'), email = H.normEmail(em.value);
    if (!H.fieldError(em, H.validEmail(email) ? '' : 'Escribe un correo válido.')) return;
    var btn = $('button[type=submit]', fReset); H.busy(btn, true, 'Enviando…');
    var r = await sb.auth.resetPasswordForEmail(email, { redirectTo: H.base + 'index.html?nueva=1' });
    H.busy(btn, false);
    if (r.error && !/not found/i.test(r.error.message || '')) { H.status(st, H.message(r.error), 'error'); return; }
    H.status(st, 'Si existe una cuenta con ese correo, recibirás un enlace para crear una contraseña nueva.', 'ok');
  });

  var fNew = $('#f-newpass');
  H.bindPasswordUI(fNew, '#np-pass', '#np-pass2');
  fNew.addEventListener('submit', async function (e) {
    e.preventDefault(); H.status(st, '');
    var btn = $('button[type=submit]', fNew); H.busy(btn, true, 'Validando…');
    var u = await sb.auth.getUser();
    var perr = await H.validatePassword($('#np-pass').value, $('#np-pass2').value, u.data.user && u.data.user.email);
    if (perr) { H.busy(btn, false); H.fieldError($('#np-pass'), perr); return; }
    var r = await sb.auth.updateUser({ password: $('#np-pass').value });
    H.busy(btn, false);
    if (r.error) {
      if (r.error.code === 'insufficient_aal') { show('p-mfa'); H.status(st, 'Verifica tu código de dos pasos y vuelve a guardar la contraseña.', 'info'); return; }
      H.status(st, H.message(r.error), 'error'); return;
    }
    H.status(st, 'Contraseña actualizada. Te llevamos a tu panel…', 'ok');
    setTimeout(afterLogin, 1200);
  });

  // ---------------- Estado inicial ----------------
  var recovering = /[?&]nueva=1/.test(location.search);
  sb.auth.onAuthStateChange(function (event) {
    if (event === 'PASSWORD_RECOVERY') { recovering = true; show('p-newpass'); }
  });

  (async function init() {
    var qs = new URLSearchParams(location.search);
    var errDesc = qs.get('error_description') || new URLSearchParams(location.hash.slice(1)).get('error_description');
    if (errDesc) {
      H.status(st, /expired|invalid/i.test(errDesc)
        ? 'El enlace expiró o ya fue usado. Si verificaste tu correo, inicia sesión; si no, solicita uno nuevo.'
        : 'No se pudo completar el acceso. Inténtalo de nuevo.', 'error');
    }
    var s = await sb.auth.getSession();
    if (!s.data.session) { if (recovering) H.status(st, 'Abre el enlace del correo en este mismo navegador para crear tu nueva contraseña.', 'info'); return; }
    if (recovering) { show('p-newpass'); return; }
    if (qs.get('mfa') === '1') { show('p-mfa'); return; }
    afterLogin();
  })();
})();
