/* Evaluador preliminar de riesgos LA/FT — HANSLIERY SÁNCHEZ
   Todo se calcula en el navegador; no se envía ni se guarda nada. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var CTRL = [['Sí', 1], ['Parcialmente', 0.5], ['No', 0], ['No lo sé', 0]];
  var STEPS = [
    { t: 'Perfil', h: 'Perfil de la organización', d: 'Actividad y tamaño de la operación.', q: [
      { id: 'sector', f: 'p', l: '¿Cuál es la actividad principal de la organización?', group: true, o: [
        ['Sujetos obligados financieros', [['Banca o intermediación financiera', 3], ['Remesas o cambio de divisas', 4], ['Mercado de valores', 3], ['Seguros o intermediación de seguros', 3], ['Cooperativa de ahorro y crédito', 3], ['Otra actividad financiera', 3]]],
        ['Sujetos obligados no financieros', [['Casino, bancas o juegos de azar', 4], ['Inmobiliaria o constructora (compraventa)', 4], ['Comercio de metales o piedras preciosas', 4], ['Comercio de vehículos', 3], ['Abogados, notarios o contadores', 3], ['Casa de empeño o préstamos', 3], ['Otra actividad no financiera', 3]]]] },
      { id: 'clientes', f: 't', l: '¿Cuántos clientes activos atiende aproximadamente?', o: [['Menos de 500', 1], ['Entre 500 y 5,000', 2], ['Entre 5,000 y 50,000', 3], ['Más de 50,000', 4]] },
      { id: 'monto', f: 't', l: '¿Cuál es el monto típico por operación?', o: [['Menos de US$1,000', 1], ['Entre US$1,000 y US$15,000', 2], ['Más de US$15,000', 4], ['Muy variable, sin perfil definido', 5]] }] },
    { t: 'Clientes', h: 'Clientes', d: 'Tipo y perfil de las personas con las que se relaciona.', q: [
      { id: 'pj', f: 'c', l: '¿Qué proporción de sus clientes son personas jurídicas o estructuras societarias?', o: [['Ninguna o casi ninguna', 1], ['Menos del 25 %', 2], ['Entre 25 % y 50 %', 3], ['Más del 50 %', 4]] },
      { id: 'pep', f: 'c', l: '¿Tiene clientes que sean personas expuestas políticamente (PEP) o sus familiares?', o: [['No', 1], ['Pocos casos', 3], ['Varios casos', 4], ['No lo sabemos', 5]] },
      { id: 'nores', f: 'c', l: '¿Qué proporción de sus clientes no reside en la República Dominicana?', o: [['Ninguna', 1], ['Menos del 10 %', 2], ['Entre 10 % y 30 %', 3], ['Más del 30 %', 4]] },
      { id: 'efvo', f: 'c', l: '¿Atiende clientes cuya actividad maneja mucho efectivo?', o: [['No', 1], ['Algunos', 2], ['Muchos', 4], ['No lo sabemos', 4]] }] },
    { t: 'Productos', h: 'Productos y servicios', d: 'Características que facilitan o dificultan su uso indebido.', q: [
      { id: 'cash', f: 'p', l: '¿Recibe pagos en efectivo?', o: [['No', 1], ['Ocasionalmente', 2], ['Con frecuencia', 4], ['Es el medio principal', 5]] },
      { id: 'terc', f: 'p', l: '¿Sus productos permiten pagos a terceros, transferencias o devoluciones y rescates anticipados?', o: [['No', 1], ['Algunos productos', 3], ['La mayoría', 4]] },
      { id: 'virt', f: 'p', l: '¿Opera con activos virtuales o acepta pagos con ellos?', o: [['No', 1], ['De forma indirecta', 3], ['Sí', 5]] }] },
    { t: 'Canales', h: 'Canales y jurisdicciones', d: 'Cómo llega a sus clientes y con qué países opera.', q: [
      { id: 'vinc', f: 'k', l: '¿Cómo vincula a sus clientes?', o: [['Siempre en persona', 1], ['Mixto, en persona y a distancia', 2], ['Mayormente a distancia', 3], ['Totalmente digital', 4]] },
      { id: 'inter', f: 'k', l: '¿Utiliza intermediarios, agentes o corredores para captar clientes?', o: [['No', 1], ['Sí, regulados', 2], ['Sí, no regulados', 4]] },
      { id: 'pais', f: 'j', l: '¿Con qué jurisdicciones operan sus clientes o sus operaciones?', o: [['Solo República Dominicana', 1], ['También Estados Unidos o la Unión Europea', 2], ['También Latinoamérica y el Caribe', 3], ['También centros offshore o países de alto riesgo', 5]] },
      { id: 'gafi', f: 'j', l: '¿Tiene clientes o contrapartes vinculados a países en las listas de alto riesgo o bajo monitoreo del GAFI?', o: [['No', 1], ['No lo sabemos', 4], ['Sí', 5]] }] },
    { t: 'Gobierno', h: 'Controles: gobierno y debida diligencia', d: 'Elementos del programa de cumplimiento que ya tiene implementados.', ctrl: true, q: [
      { id: 'k1', l: '¿Tiene un oficial de cumplimiento designado?' },
      { id: 'k2', l: '¿Tiene un manual de prevención aprobado y actualizado en los últimos 12 meses?' },
      { id: 'k3', l: '¿Tiene una autoevaluación de riesgos documentada?' },
      { id: 'k4', l: '¿Clasifica a sus clientes por nivel de riesgo y aplica debida diligencia según ese nivel?' },
      { id: 'k5', l: '¿Identifica y verifica al beneficiario final de las personas jurídicas?' },
      { id: 'k6', l: '¿Identifica a las PEP y a sus familiares y aplica medidas reforzadas?' }] },
    { t: 'Monitoreo', h: 'Controles: monitoreo, reportes y formación', d: 'Detección, reporte y sostenibilidad del programa.', ctrl: true, q: [
      { id: 'k7', l: '¿Verifica a clientes y contrapartes en listas de sanciones antes de vincularlos?' },
      { id: 'k8', l: '¿Monitorea las operaciones y analiza las alertas de forma documentada?' },
      { id: 'k9', l: '¿Tiene un procedimiento para reportar a la UAF (ROS y RTE) dentro de los plazos legales?' },
      { id: 'k10', l: '¿Capacita a su personal al menos una vez al año y evalúa el aprendizaje?' },
      { id: 'k11', l: '¿El programa se somete a una revisión independiente o auditoría?' },
      { id: 'k12', l: '¿Conserva los registros de clientes y operaciones por al menos 10 años?' }] }
  ];
  var FACT = [
    { k: 'c', n: 'Clientes', w: 0.30, ctl: ['k4', 'k5', 'k6', 'k7'] },
    { k: 'p', n: 'Productos y servicios', w: 0.20, ctl: ['k3', 'k8', 'k9'] },
    { k: 'k', n: 'Canales', w: 0.15, ctl: ['k2', 'k4', 'k10'] },
    { k: 'j', n: 'Jurisdicción', w: 0.25, ctl: ['k3', 'k7', 'k8'] },
    { k: 't', n: 'Transaccionalidad', w: 0.10, ctl: ['k8', 'k9', 'k12'] }
  ];
  var GAP = {
    k1: [1.0, 'Designar un oficial de cumplimiento', 'La Ley 155-17 exige un oficial de cumplimiento y su falta se considera una infracción. Debe contar con independencia, recursos y acceso a la alta gerencia.', '01'],
    k3: [0.95, 'Documentar la autoevaluación de riesgos', 'El programa debe basarse en riesgos (art. 34) y considerar como mínimo clientes, productos y servicios, canales y zona geográfica (art. 37).', '02'],
    k6: [0.9, 'Fortalecer la gestión de PEP', 'Las PEP se tratan como clientes de alto riesgo y la obligación alcanza a sus familiares hasta el segundo grado (art. 46).', '02'],
    k7: [0.9, 'Implementar el screening en listas', 'Las coincidencias con listas de sanciones del Consejo de Seguridad de la ONU exigen aplicar medidas sin demora.', '02'],
    k9: [0.9, 'Formalizar los reportes a la UAF', 'El ROS se remite en un plazo de cinco días hábiles; el RTE aplica desde US$15,000, agrega las operaciones en efectivo de 24 horas (art. 54) y se remite en los primeros 10 días del mes siguiente.', '01'],
    k5: [0.85, 'Identificar al beneficiario final', 'Para personas jurídicas se verifica la razón social, el RNC, la forma jurídica, la dirección y el beneficiario final (art. 40).', '02'],
    k4: [0.85, 'Segmentar clientes por riesgo', 'La debida diligencia debe graduarse según el riesgo de cada cliente (art. 36), con medidas reforzadas para el riesgo alto.', '02'],
    k2: [0.8, 'Actualizar el manual de prevención', 'El manual debe reflejar la normativa vigente y los riesgos reales de la organización (art. 34).', '01'],
    k8: [0.8, 'Monitorear operaciones y alertas', 'La relación con el cliente se monitorea de forma permanente (art. 39), con alertas analizadas y documentadas.', '03'],
    k11: [0.7, 'Programar una revisión independiente', 'Una revisión independiente valida que los controles funcionen y aporta evidencia ante el supervisor.', '03'],
    k10: [0.7, 'Fortalecer la capacitación', 'Un programa anual por audiencias, con evaluación y evidencias, sostiene la aplicación de los controles.', '04'],
    k12: [0.6, 'Asegurar la conservación de registros', 'Los registros de debida diligencia y de operaciones se conservan al menos 10 años (art. 43).', '03']
  };
  var SV = { '01': 'Consultoría y fortalecimiento PLAFT', '02': 'Gestión de riesgos y debida diligencia', '03': 'Controles internos y gobierno', '04': 'Capacitación profesional' };
  var CATS = [[1.5, 'Muy bajo', 1], [2.5, 'Bajo', 2], [3.5, 'Medio', 3], [4.5, 'Alto', 4], [99, 'Muy alto', 5]];
  var cat = function (v) { for (var i = 0; i < CATS.length; i++) if (v < CATS[i][0]) return CATS[i]; };
  var r2 = function (v) { return (Math.round((v + 1e-9) * 100) / 100).toFixed(2); };

  /* ---------- render ---------- */
  var pages = $('#dg-pages'), stepsEl = $('#dg-steps');
  var esc = function (s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML; };
  STEPS.forEach(function (s, si) {
    var st = document.createElement('span');
    st.innerHTML = '<em>' + (si + 1) + '</em>' + esc(s.t);
    stepsEl.appendChild(st);
    var sec = document.createElement('section');
    sec.className = 'dg-page'; sec.hidden = si !== 0;
    var h = '<header class="dg-page-head"><p class="dg-kick">Paso ' + (si + 1) + ' de ' + STEPS.length + '</p><h3 tabindex="-1">' + esc(s.h) + '</h3><p>' + esc(s.d) + '</p></header>';
    if (si === 0) h += '<label class="dg-org-field"><span>Nombre de la organización <small>(opcional, solo para su informe)</small></span><input type="text" id="dg-orgname" maxlength="80" autocomplete="organization" class="control"></label>';
    s.q.forEach(function (q, qi) {
      var name = q.id, opts = '';
      if (q.group) {
        opts = '<select class="control dg-select" name="' + name + '" id="q-' + name + '" aria-describedby="h-' + name + '"><option value="">Seleccione una opción</option>' +
          q.o.map(function (g) { return '<optgroup label="' + esc(g[0]) + '">' + g[1].map(function (o) { return '<option value="' + o[1] + '">' + esc(o[0]) + '</option>'; }).join('') + '</optgroup>'; }).join('') + '</select>';
        h += '<div class="dg-q"><label class="dg-legend" for="q-' + name + '"><span class="dg-qn">' + (qi + 1) + '</span>' + esc(q.l) + '</label><p class="dg-sr" id="h-' + name + '">Obligatorio</p>' + opts + '</div>';
        return;
      }
      var list = s.ctrl ? CTRL : q.o;
      opts = list.map(function (o, oi) {
        var id = 'q-' + name + '-' + oi;
        return '<label class="dg-opt" for="' + id + '"><input type="radio" id="' + id + '" name="' + name + '" value="' + o[1] + '" data-label="' + esc(o[0]) + '"><span>' + esc(o[0]) + '</span></label>';
      }).join('');
      h += '<fieldset class="dg-q' + (s.ctrl ? ' dg-q-ctl' : '') + '"><legend class="dg-legend"><span class="dg-qn">' + (qi + 1) + '</span>' + esc(q.l) + '</legend><div class="dg-opts">' + opts + '</div></fieldset>';
    });
    sec.innerHTML = h;
    pages.appendChild(sec);
  });

  var cur = 0, pageEls = Array.prototype.slice.call(pages.children), stepEls = Array.prototype.slice.call(stepsEl.children);
  var prev = $('#dg-prev'), next = $('#dg-next'), err = $('#dg-error'), bar = $('#dg-bar'), count = $('#dg-count');
  var form = $('#dg-form');
  var answered = function () {
    var n = 0, tot = 0;
    STEPS.forEach(function (s) { s.q.forEach(function (q) { tot++; if (val(q.id) !== null) n++; }); });
    return [n, tot];
  };
  var val = function (id) {
    var el = form.elements[id]; if (!el) return null;
    if (el.tagName === 'SELECT') return el.value === '' ? null : +el.value;
    var c = form.querySelector('input[name="' + id + '"]:checked'); return c ? +c.value : null;
  };
  var label = function (id) {
    var el = form.elements[id];
    if (el && el.tagName === 'SELECT') return el.value === '' ? '—' : el.options[el.selectedIndex].text;
    var c = form.querySelector('input[name="' + id + '"]:checked'); return c ? c.getAttribute('data-label') : '—';
  };
  var update = function () {
    var a = answered(), pct = Math.round(a[0] / a[1] * 100);
    bar.setAttribute('aria-valuenow', pct); bar.firstElementChild.style.width = pct + '%';
    count.textContent = a[0] + ' de ' + a[1] + ' respondidas';
  };
  var show = function (i, focus) {
    pageEls.forEach(function (p, j) { p.hidden = j !== i; p.classList.toggle('is-in', j === i && !reduce); });
    stepEls.forEach(function (s, j) { s.className = j < i ? 'done' : j === i ? 'on' : ''; });
    prev.style.visibility = i === 0 ? 'hidden' : 'visible';
    next.textContent = i === STEPS.length - 1 ? 'Ver mi diagnóstico' : 'Siguiente';
    err.hidden = true; cur = i;
    if (focus) { var h = pageEls[i].querySelector('h3'); h.focus({ preventScroll: true }); $('#evaluador').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' }); }
  };
  form.addEventListener('change', function (e) {
    update();
    var q = e.target.closest('.dg-q'); if (q) q.classList.remove('is-missing');
  });
  next.addEventListener('click', function () {
    var miss = STEPS[cur].q.filter(function (q) { return val(q.id) === null; });
    pageEls[cur].querySelectorAll('.dg-q').forEach(function (el, k) { el.classList.toggle('is-missing', val(STEPS[cur].q[k].id) === null); });
    if (miss.length) {
      err.textContent = miss.length === 1 ? 'Falta 1 pregunta por responder en este paso.' : 'Faltan ' + miss.length + ' preguntas por responder en este paso.';
      err.hidden = false;
      var first = pageEls[cur].querySelector('.is-missing select, .is-missing input'); if (first) first.focus();
      return;
    }
    if (cur < STEPS.length - 1) show(cur + 1, true); else results();
  });
  prev.addEventListener('click', function () { if (cur > 0) show(cur - 1, true); });
  show(0); update();

  /* ---------- resultados ---------- */
  var last = null;
  function results() {
    var by = { c: [], p: [], k: [], j: [], t: [] }, ctl = {};
    STEPS.forEach(function (s) { s.q.forEach(function (q) { if (s.ctrl) ctl[q.id] = val(q.id); else by[q.f].push(val(q.id)); }); });
    var avg = function (a) { return a.reduce(function (x, y) { return x + y; }, 0) / a.length; };
    var keys = Object.keys(ctl), M = avg(keys.map(function (k) { return ctl[k]; }));
    var inh = 0, rows = '';
    FACT.forEach(function (f) {
      var sc = avg(by[f.k]), rd = avg(f.ctl.map(function (k) { return ctl[k]; }));
      var res = Math.max(1, sc * (1 - 0.30 * rd));
      inh += sc * f.w;
      var ce = cat(sc), cr = cat(res), prep = rd >= 0.75 ? ['Alta', 1] : rd >= 0.4 ? ['Media', 3] : ['Baja', 4];
      rows += '<tr><th scope="row">' + f.n + ' <small>' + Math.round(f.w * 100) + ' %</small></th>' +
        '<td data-label="Exposición"><span class="dg-cell lv' + ce[2] + '">' + ce[1] + '</span></td>' +
        '<td data-label="Preparación"><span class="dg-cell lv' + prep[1] + '">' + prep[0] + ' · ' + Math.round(rd * 100) + ' %</span></td>' +
        '<td data-label="Residual"><span class="dg-cell lv' + cr[2] + '">' + cr[1] + '</span></td>' +
        '<td class="dg-num" data-label="Puntaje">' + Math.round((res - 1) / 4 * 100) + '<small>/100</small></td></tr>';
    });
    var res = Math.max(1, inh * (1 - 0.30 * M)), score = Math.round((res - 1) / 4 * 100), c = cat(res);
    $('#dg-heat').innerHTML = rows;
    $('#dg-inh').textContent = r2(inh) + ' · ' + cat(inh)[1];
    $('#dg-mat').textContent = Math.round(M * 100) + ' %';
    $('#dg-res').textContent = r2(res);
    var catEl = $('#dg-cat'); catEl.textContent = c[1]; catEl.className = 'dg-cat-big lv' + c[2];
    var READ = {
      1: 'La exposición estimada es muy baja. Mantenga los controles, revíselos periódicamente y documente la evidencia de su funcionamiento.',
      2: 'La exposición estimada es baja. Conviene cerrar las brechas señaladas para sostener el resultado ante una supervisión.',
      3: 'La exposición estimada es media. Hay factores relevantes que requieren controles más sólidos y documentados.',
      4: 'La exposición estimada es alta. Se recomienda priorizar las brechas señaladas y revisar el programa de cumplimiento a corto plazo.',
      5: 'La exposición estimada es muy alta. Se recomienda una revisión integral del programa de cumplimiento con carácter prioritario.' };
    $('#dg-reading').textContent = READ[c[2]];
    var org = ($('#dg-orgname').value || '').trim();
    $('#dg-org').textContent = org ? 'Organización: ' + org : '';
    $('#dg-date').textContent = new Date().toLocaleDateString('es-DO', { day: 'numeric', month: 'long', year: 'numeric' });
    var gaps = keys.filter(function (k) { return ctl[k] < 1; }).sort(function (a, b) { return (1 - ctl[b]) * GAP[b][0] - (1 - ctl[a]) * GAP[a][0]; }).slice(0, 6);
    $('#dg-gaps').innerHTML = gaps.length ? gaps.map(function (k) {
      var g = GAP[k]; return '<li><div><b>' + g[1] + '</b><span class="dg-gap-st">' + (ctl[k] === 0.5 ? 'Parcial' : 'Pendiente') + '</span></div><p>' + g[2] + '</p><a href="index.html#servicios" class="dg-gap-sv">Servicio ' + g[3] + ' · ' + SV[g[3]] + '</a></li>';
    }).join('') : '<li class="dg-nogap"><div><b>No se identificaron brechas en los controles declarados</b></div><p>Valide periódicamente que los controles funcionen como están documentados y conserve la evidencia.</p></li>';
    var ans = '';
    STEPS.forEach(function (s) {
      ans += '<tr class="dg-ans-h"><th colspan="2">' + esc(s.h) + '</th></tr>';
      s.q.forEach(function (q) { ans += '<tr><td>' + esc(q.l) + '</td><td>' + esc(label(q.id)) + '</td></tr>'; });
    });
    $('#dg-ans').innerHTML = ans;
    last = { cat: c[1], score: score };
    $('#dg-contact').href = 'index.html?servicio=riesgos&dx=' + encodeURIComponent(c[1]) + '&pts=' + score + '#contacto';
    $('#dg-shell').hidden = true;
    var box = $('#dg-result'); box.hidden = false;
    box.classList.toggle('is-in', !reduce);
    var g = $('#dg-gauge'), L = 2 * Math.PI * 52;
    g.style.strokeDasharray = L; g.style.strokeDashoffset = L;
    g.setAttribute('class', 'dg-g-fg lv' + c[2]);
    var n = $('#dg-score');
    if (reduce) { g.style.strokeDashoffset = L * (1 - score / 100); n.textContent = score; }
    else {
      requestAnimationFrame(function () { g.style.strokeDashoffset = L * (1 - score / 100); });
      var t0 = null; (function tick(t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / 1200); n.textContent = Math.round(score * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(tick); })(performance.now());
    }
    box.focus({ preventScroll: true });
    box.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
  }

  $('#dg-pdf').addEventListener('click', function () { var d = $('.dg-answers'); d.open = true; window.print(); });
  window.addEventListener('beforeprint', function () { var d = $('.dg-answers'); if (d) d.open = true; });
  $('#dg-restart').addEventListener('click', function () {
    form.reset(); $('#dg-result').hidden = true; $('#dg-shell').hidden = false;
    pageEls.forEach(function (p) { p.querySelectorAll('.is-missing').forEach(function (x) { x.classList.remove('is-missing'); }); });
    show(0, true); update();
  });
  $('#dg-start-top').addEventListener('click', function (e) {
    e.preventDefault(); $('#evaluador').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    var f = pageEls[cur].querySelector('select, input'); if (f) setTimeout(function () { f.focus({ preventScroll: true }); }, reduce ? 0 : 500);
  });
})();
