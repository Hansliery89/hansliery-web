/* ACADEMY · Certificado imprimible. Los datos vienen del registro oficial (certificate_public);
   el QR lleva a la página pública de verificación. */
(function () {
  'use strict';
  var H = window.HSA; if (!H) return;
  var $ = H.$, st = $('#ct-status');
  var code = (new URLSearchParams(location.search).get('codigo') || '').trim().toUpperCase();
  $('#ct-print').addEventListener('click', function () { window.print(); });

  function qrSvg(text) {
    var q = window.qrcode(0, 'M'); q.addData(text); q.make();
    var n = q.getModuleCount(), NS = 'http://www.w3.org/2000/svg';
    var svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '0 0 ' + (n + 8) + ' ' + (n + 8)); svg.setAttribute('width', '120'); svg.setAttribute('height', '120');
    var bg = document.createElementNS(NS, 'rect'); bg.setAttribute('width', n + 8); bg.setAttribute('height', n + 8); bg.setAttribute('fill', '#fff'); svg.appendChild(bg);
    var d = '';
    for (var r = 0; r < n; r++) for (var c = 0; c < n; c++) if (q.isDark(r, c)) d += 'M' + (c + 4) + ' ' + (r + 4) + 'h1v1h-1z';
    var p = document.createElementNS(NS, 'path'); p.setAttribute('d', d); p.setAttribute('fill', '#0A192F'); svg.appendChild(p);
    return svg;
  }

  (async function () {
    if (!/^HS-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$/.test(code)) { H.status(st, 'Falta el código del certificado.', 'error'); return; }
    var r = await H.sb.rpc('certificate_public', { p_code: code });
    if (r.error) { H.status(st, H.message(r.error), 'error'); return; }
    var c = (r.data || [])[0];
    if (!c) { H.status(st, 'No existe un certificado con ese código.', 'error'); return; }
    if (c.status !== 'valid') { H.status(st, 'Este certificado fue revocado y no puede imprimirse.', 'error'); return; }
    var url = H.base + 'verificar.html?codigo=' + encodeURIComponent(c.verification_code);
    $('#ct-name').textContent = c.student_name;
    $('#ct-course').textContent = c.course_title;
    $('#ct-detail').textContent = 'Finalizada el ' + H.fmtDate(c.completed_on) +
      (c.academic_hours ? ' · ' + Number(c.academic_hours) + ' horas académicas' : '') +
      (c.grade_pct != null ? ' · Calificación final: ' + Number(c.grade_pct).toFixed(1) + ' %' : '') +
      ' · Emitido el ' + H.fmtDate(c.issued_at) + '.';
    $('#ct-code').textContent = c.verification_code;
    $('#ct-url').textContent = url.replace(/^https?:\/\//, '');
    $('#ct-qr').appendChild(qrSvg(url));
    document.title = 'Certificado ' + c.verification_code + ' | ACADEMY';
    $('#ct-cert').hidden = false;
  })();
})();
