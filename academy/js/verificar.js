/* ACADEMY · Verificación pública de certificados (sin sesión) */
(function () {
  'use strict';
  var H = window.HSA; if (!H) return;
  var $ = H.$, st = $('#vf-status'), out = $('#vf-result'), input = $('#vf-code');

  async function verify(code) {
    H.status(st, ''); out.innerHTML = '';
    code = code.trim().toUpperCase();
    if (!H.fieldError(input, /^HS-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$/.test(code) ? '' : 'El código tiene el formato HS-XXXX-XXXX-XXXX.')) return;
    var btn = $('#f-verify button[type=submit]'); H.busy(btn, true, 'Verificando…');
    var r = await H.sb.rpc('verify_certificate', { p_code: code });
    H.busy(btn, false);
    if (r.error) { H.status(st, H.message(r.error), 'error'); return; }
    var c = (r.data || [])[0];
    if (!c) { H.status(st, 'No existe un certificado con ese código. Revisa que esté bien escrito.', 'error'); return; }
    var valid = c.status === 'valid';
    H.status(st, valid ? 'Certificado auténtico y vigente.' : 'Este certificado fue revocado y no es válido.', valid ? 'ok' : 'error');
    out.innerHTML = '<table class="ac-table"><tbody>' +
      '<tr><th>Estudiante</th><td>' + H.esc(c.student_name) + '</td></tr>' +
      '<tr><th>Capacitación</th><td>' + H.esc(c.course_title) + '</td></tr>' +
      (c.academic_hours ? '<tr><th>Horas académicas</th><td>' + Number(c.academic_hours) + '</td></tr>' : '') +
      '<tr><th>Finalización</th><td>' + H.fmtDate(c.completed_on) + '</td></tr>' +
      '<tr><th>Emisión</th><td>' + H.fmtDate(c.issued_at) + '</td></tr>' +
      '<tr><th>Código</th><td>' + H.esc(code) + '</td></tr></tbody></table>' +
      (valid ? '<div class="ac-actions"><a class="btn btn-ghost btn-sm" href="' + H.base + 'certificado.html?codigo=' + encodeURIComponent(code) + '">Ver el certificado</a></div>' : '');
  }

  $('#f-verify').addEventListener('submit', function (e) { e.preventDefault(); verify(input.value); });
  var q = new URLSearchParams(location.search).get('codigo');
  if (q) { input.value = q; verify(q); }
})();
