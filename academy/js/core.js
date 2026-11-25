/* =================================================================
   ACADEMY · núcleo común (cliente de Supabase y utilidades)
   La seguridad real está en el servidor (RLS y funciones). Aquí solo se
   valida para dar mensajes claros y evitar envíos inútiles.
   ================================================================= */
(function () {
  'use strict';
  var cfg = (window.SITE_CONFIG || {}).academy;
  if (!cfg || !window.supabase) { console.error('[academy] configuración no disponible'); return; }

  var sb = window.supabase.createClient(cfg.supabase_url, cfg.supabase_key, {
    auth: { flowType: 'pkce', persistSession: true, autoRefreshToken: true, detectSessionInUrl: true }
  });

  // Dirección base de la Academy (funciona en github.io y con dominio propio)
  var base = new URL('academy/', document.baseURI).href;

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  function esc(v) {
    return String(v == null ? '' : v).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function normEmail(v) { return String(v || '').trim().toLowerCase(); }
  function validEmail(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) && v.length <= 254; }

  // Mensajes comprensibles para los errores más comunes
  var MSG = {
    invalid_credentials: 'Correo o contraseña incorrectos.',
    email_not_confirmed: 'Aún no has verificado tu correo. Revisa tu bandeja de entrada (y la carpeta de spam).',
    user_already_exists: 'Si el correo no estaba registrado, recibirás un enlace de verificación. Si ya tienes cuenta, inicia sesión o recupera tu contraseña.',
    weak_password: 'La contraseña no cumple la política de seguridad. Usa al menos 12 caracteres y evita contraseñas comunes.',
    same_password: 'La nueva contraseña debe ser distinta de la anterior.',
    over_email_send_rate_limit: 'Se enviaron demasiados correos en poco tiempo. Espera unos minutos e inténtalo de nuevo.',
    over_request_rate_limit: 'Demasiados intentos. Espera unos minutos e inténtalo de nuevo.',
    mfa_verification_failed: 'El código no es correcto o ya expiró. Inténtalo de nuevo.',
    mfa_challenge_expired: 'El código expiró. Escribe el código actual de tu aplicación.',
    insufficient_aal: 'Necesitas completar la verificación en dos pasos para hacer este cambio.',
    reauthentication_needed: 'Por seguridad, vuelve a iniciar sesión para hacer este cambio.',
    session_not_found: 'Tu sesión expiró. Inicia sesión de nuevo.',
    provider_disabled: 'El acceso con Google aún no está habilitado. Usa tu correo y contraseña.',
    validation_failed: 'Revisa los datos ingresados.',
    signup_disabled: 'El registro está temporalmente deshabilitado.',
    email_address_not_authorized: 'Por ahora no es posible enviar correos a esa dirección. Inténtalo más tarde o escríbenos.',
    consent_required: 'Debes aceptar los términos y la política de privacidad.',
    course_full: 'El curso ya no tiene cupos disponibles.',
    payment_required: 'Este curso requiere pago. Escríbenos para inscribirte.',
    course_not_available: 'El curso no está disponible.',
    not_enrolled: 'Primero debes matricularte en el curso.',
    not_allowed: 'No tienes permiso para esta acción. Vuelve a iniciar sesión.',
    mfa_required: 'Completa la verificación en dos pasos para continuar.'
  };
  function message(err) {
    if (!err) return 'Ocurrió un error inesperado. Inténtalo de nuevo.';
    var code = err.code || err.error_code || '';
    if (MSG[code]) return MSG[code];
    var m = String(err.message || err.msg || err);
    for (var k in MSG) { if (m.indexOf(k) > -1) return MSG[k]; }
    if (/provider is not enabled/i.test(m)) return MSG.provider_disabled;
    if (/rate limit/i.test(m)) return MSG.over_request_rate_limit;
    if (/Failed to fetch|NetworkError|Load failed/i.test(m)) return 'No hay conexión con el servidor. Revisa tu internet e inténtalo de nuevo.';
    return 'No se pudo completar la operación. Inténtalo de nuevo en unos minutos.';
  }

  function status(el, text, kind) {
    if (!el) return;
    el.className = 'ac-status' + (text ? ' is-' + (kind || 'info') : '');
    el.textContent = text || '';
    if (text && kind === 'error') el.setAttribute('role', 'alert'); else el.setAttribute('role', 'status');
  }

  function busy(btn, on, label) {
    if (!btn) return;
    if (on) { btn.dataset.label = btn.innerHTML; btn.disabled = true; btn.setAttribute('aria-busy', 'true'); btn.textContent = label || 'Procesando…'; }
    else { btn.disabled = false; btn.removeAttribute('aria-busy'); if (btn.dataset.label) btn.innerHTML = btn.dataset.label; }
  }

  function fieldError(input, text) {
    var box = input.closest('.field');
    var e = box ? $('.error', box) : null;
    input.setAttribute('aria-invalid', text ? 'true' : 'false');
    if (e) { if (!e.id) e.id = input.id + '-e'; e.textContent = text || ''; input.setAttribute('aria-describedby', e.id); }
    return !text;
  }

  // ---------------- Contraseñas ----------------
  var COMMON = ['123456789012', 'password1234', 'contraseña123', 'qwertyuiop12', '000000000000', '111111111111',
    'abcdefghijkl', 'administrador', 'iloveyou1234', 'republicadominicana', 'passwordpassword', 'hansliery123'];

  function passwordChecks(p, p2) {
    var len = p.length >= 12 && p.length <= 128;
    var mix = /[A-Za-zÁÉÍÓÚÑáéíóúñ]/.test(p) && /[^A-Za-zÁÉÍÓÚÑáéíóúñ]/.test(p);
    var match = !!p && p === p2;
    var level = (len ? 1 : 0) + (mix ? 1 : 0) + (p.length >= 16 ? 1 : 0);
    return { len: len, mix: mix, match: match, level: len ? Math.max(1, level) : 0 };
  }

  function bindPasswordUI(form, passSel, pass2Sel) {
    var p = $(passSel, form), p2 = $(pass2Sel, form), meter = $('[data-meter]', form), rules = $('[data-rules]', form);
    function paint() {
      var c = passwordChecks(p.value, p2.value);
      if (meter) { meter.dataset.level = String(c.level); $('i', meter).style.width = (c.level / 3 * 100) + '%'; }
      if (rules) ['len', 'mix', 'match'].forEach(function (k) { var li = $('[data-rule="' + k + '"]', rules); if (li) li.classList.toggle('is-ok', c[k]); });
    }
    p.addEventListener('input', paint); p2.addEventListener('input', paint); paint();
  }

  // Comprueba si la contraseña aparece en filtraciones conocidas (Have I Been Pwned, k-anonimato:
  // solo se envían los 5 primeros caracteres del hash SHA-1, nunca la contraseña).
  async function pwnedCount(p) {
    try {
      var buf = await crypto.subtle.digest('SHA-1', new TextEncoder().encode(p));
      var hex = Array.prototype.map.call(new Uint8Array(buf), function (b) { return ('0' + b.toString(16)).slice(-2); }).join('').toUpperCase();
      var ctrl = new AbortController(); var t = setTimeout(function () { ctrl.abort(); }, 4000);
      var res = await fetch('https://api.pwnedpasswords.com/range/' + hex.slice(0, 5), { headers: { 'Add-Padding': 'true' }, signal: ctrl.signal });
      clearTimeout(t);
      if (!res.ok) return -1;
      var body = await res.text(), suffix = hex.slice(5);
      var line = body.split('\n').find(function (l) { return l.split(':')[0] === suffix; });
      return line ? parseInt(line.split(':')[1], 10) || 0 : 0;
    } catch (e) { return -1; }  // si el servicio no responde, no se bloquea el registro
  }

  async function validatePassword(p, p2, email) {
    var c = passwordChecks(p, p2);
    if (!c.len) return 'La contraseña debe tener entre 12 y 128 caracteres.';
    if (!c.mix) return 'Combina letras con números, símbolos o espacios.';
    if (!c.match) return 'Las contraseñas no coinciden.';
    var lower = p.toLowerCase();
    if (email && lower.indexOf(email.split('@')[0]) > -1 && email.split('@')[0].length >= 4) return 'La contraseña no debe contener tu correo.';
    if (COMMON.indexOf(lower) > -1 || /^(.)\1+$/.test(p)) return 'Esa contraseña es demasiado común. Elige otra.';
    var n = await pwnedCount(p);
    if (n > 0) return 'Esa contraseña aparece en filtraciones de datos conocidas. Elige una distinta.';
    return '';
  }

  // ---------------- Sesión ----------------
  async function aal() {
    var r = await sb.auth.mfa.getAuthenticatorAssuranceLevel();
    return r.data || { currentLevel: null, nextLevel: null };
  }

  function fmtDate(v, withTime) {
    if (!v) return '—';
    var d = new Date(v);
    return d.toLocaleDateString('es-DO', { year: 'numeric', month: 'short', day: 'numeric' }) +
      (withTime ? ' · ' + d.toLocaleTimeString('es-DO', { hour: '2-digit', minute: '2-digit' }) : '');
  }

  window.HSA = {
    sb: sb, cfg: cfg, base: base, $: $, $$: $$, esc: esc, normEmail: normEmail, validEmail: validEmail,
    message: message, status: status, busy: busy, fieldError: fieldError,
    bindPasswordUI: bindPasswordUI, validatePassword: validatePassword, aal: aal, fmtDate: fmtDate
  };
})();
