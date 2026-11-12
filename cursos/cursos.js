/* =====================================================================
   HANSLIERY SÁNCHEZ · Capacitaciones — interacción de cursos
   - Progreso de lectura y tabla de contenido activa
   - Evaluación con retroalimentación inmediata y resultado final
   - Avance guardado en este navegador (localStorage, si está disponible)
   - Pestañas accesibles para ejemplos por sector
   ===================================================================== */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var KEY = 'hs-cursos-v1';

  /* Almacenamiento tolerante a fallos */
  var store = {
    read: function () { try { return JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { return {}; } },
    write: function (d) { try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) { /* sin almacenamiento */ } }
  };

  /* Barra de progreso de página + volver arriba */
  var bar = $('.progress'), top = $('.to-top'), ticking = false;
  var onScroll = function () {
    var y = window.scrollY, max = document.documentElement.scrollHeight - window.innerHeight;
    if (bar) bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(y / max, 1) : 0) + ')';
    if (top) top.classList.toggle('is-visible', y > 700);
    ticking = false;
  };
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
  if (top) top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });

  /* Aparición suave */
  var revealables = $$('.module, .objectives, .q');
  if ('IntersectionObserver' in window && !reduce) {
    var rio = new IntersectionObserver(function (en) {
      en.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); rio.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    revealables.forEach(function (el) { rio.observe(el); });
  } else { revealables.forEach(function (el) { el.classList.add('is-in'); }); }

  /* Pestañas (patrón WAI-ARIA) */
  $$('.tabs').forEach(function (tabs) {
    var btns = $$('[role="tab"]', tabs), panels = $$('[role="tabpanel"]', tabs);
    var select = function (i, focus) {
      btns.forEach(function (b, k) { b.setAttribute('aria-selected', String(k === i)); b.tabIndex = k === i ? 0 : -1; });
      panels.forEach(function (p, k) { p.hidden = k !== i; });
      if (focus) btns[i].focus();
    };
    btns.forEach(function (b, i) {
      b.addEventListener('click', function () { select(i); });
      b.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight') { e.preventDefault(); select((i + 1) % btns.length, true); }
        if (e.key === 'ArrowLeft') { e.preventDefault(); select((i - 1 + btns.length) % btns.length, true); }
      });
    });
    select(0);
  });

  /* ---------------- Página de curso ---------------- */
  var main = $('main[data-course]');
  if (main) {
    var slug = main.getAttribute('data-course');
    var data = store.read();
    var rec = data[slug] || { read: [], best: null };

    /* Lectura: marcar secciones vistas */
    var sections = $$('[data-section]');
    var links = $$('[data-toc]');
    var ringVal = $('.ring-val'), pctEl = $('[data-pct]');
    var paint = function () {
      var modules = sections.filter(function (s) { return /^modulo-/.test(s.id); });
      var done = modules.filter(function (s) { return rec.read.indexOf(s.id) > -1; }).length;
      var pct = modules.length ? Math.round(done / modules.length * 100) : 0;
      if (ringVal) ringVal.style.strokeDashoffset = String(119.4 * (1 - pct / 100));
      if (pctEl) pctEl.textContent = pct + '%';
      links.forEach(function (a) { a.classList.toggle('is-done', rec.read.indexOf(a.getAttribute('href').slice(1)) > -1); });
    };
    if ('IntersectionObserver' in window) {
      var sio = new IntersectionObserver(function (en) {
        en.forEach(function (e) {
          if (!e.isIntersecting) return;
          var id = e.target.id;
          links.forEach(function (a) { a.classList.toggle('is-active', a.getAttribute('href') === '#' + id); });
          if (rec.read.indexOf(id) === -1) { rec.read.push(id); data[slug] = rec; store.write(data); paint(); }
        });
      }, { rootMargin: '-35% 0px -55% 0px' });
      sections.forEach(function (s) { sio.observe(s); });
    }
    paint();

    var best = $('[data-best]');
    var showBest = function () {
      if (best && rec.best !== null) {
        best.hidden = false;
        best.textContent = (rec.best >= 80 ? '★ Curso aprobado · ' : 'Último intento · ') + 'mejor resultado: ' + rec.best + '%';
      }
    };
    showBest();

    /* Evaluación */
    var form = $('.quiz-form');
    if (form) {
      var qs = $$('.q', form), total = qs.length, answered = 0, correct = 0;
      var qbar = $('.quiz-bar i'), result = $('.result');
      var cheers = ['¡Correcto!', '¡Exacto!', '¡Muy bien!', '¡Así es!', '¡Bien razonado!'];
      var nudges = ['Casi…', 'No exactamente.', 'Revisemos esto.', 'Buen intento.'];

      var finish = function () {
        var pct = Math.round(correct / total * 100);
        var pass = pct >= 80;
        result.hidden = false;
        result.classList.toggle('is-pass', pass);
        $('[data-score]', result).textContent = pct + '%';
        requestAnimationFrame(function () { $('.rs-val', result).style.strokeDashoffset = String(326.7 * (1 - pct / 100)); });
        var t = $('.result-title', result), x = $('.result-text', result);
        if (pct === 100) { t.textContent = '¡Dominio total! Aprobaste con excelencia'; x.textContent = 'Respondiste correctamente ' + correct + ' de ' + total + '. Este conocimiento ya forma parte de tu criterio profesional.'; }
        else if (pass) { t.textContent = '¡Aprobado! Muy buen trabajo'; x.textContent = 'Acertaste ' + correct + ' de ' + total + '. Revisa las explicaciones de las preguntas falladas para cerrar la brecha.'; }
        else if (pct >= 50) { t.textContent = 'Vas por buen camino'; x.textContent = 'Acertaste ' + correct + ' de ' + total + '. Repasa los módulos señalados en las explicaciones y vuelve a intentarlo: necesitas 80 % para aprobar.'; }
        else { t.textContent = 'Cada intento suma'; x.textContent = 'Acertaste ' + correct + ' de ' + total + '. Lee de nuevo los módulos con calma; las explicaciones te muestran dónde está cada respuesta.'; }
        rec.best = Math.max(rec.best || 0, pct); data[slug] = rec; store.write(data); showBest();
        if (pass && !reduce) confetti();
        result.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
      };

      qs.forEach(function (q) {
        var answer = parseInt(q.getAttribute('data-answer'), 10);
        $$('input', q).forEach(function (inp) {
          inp.addEventListener('change', function () {
            if (q.classList.contains('is-answered')) return;
            q.classList.add('is-answered');
            var chosen = parseInt(inp.value, 10), ok = chosen === answer;
            var opts = $$('.opt', q);
            opts[answer].classList.add('is-correct');
            if (!ok) opts[chosen].classList.add('is-wrong');
            $$('input', q).forEach(function (i) { i.disabled = true; });
            var fb = $('.feedback', q);
            fb.hidden = false; fb.className = 'feedback ' + (ok ? 'ok' : 'bad');
            $('.fb-title', fb).textContent = ok ? cheers[Math.floor(Math.random() * cheers.length)] : nudges[Math.floor(Math.random() * nudges.length)] + ' La respuesta correcta es la ' + 'ABCDE'.charAt(answer) + '.';
            answered++; if (ok) correct++;
            if (qbar) qbar.style.width = (answered / total * 100) + '%';
            if (answered === total) setTimeout(finish, 450);
          });
        });
      });

      $('[data-retry]').addEventListener('click', function () {
        answered = 0; correct = 0; result.hidden = true; result.classList.remove('is-pass');
        $('.rs-val', result).style.strokeDashoffset = '326.7';
        if (qbar) qbar.style.width = '0';
        qs.forEach(function (q) {
          q.classList.remove('is-answered');
          $$('.opt', q).forEach(function (o) { o.classList.remove('is-correct', 'is-wrong'); });
          $$('input', q).forEach(function (i) { i.disabled = false; i.checked = false; });
          var fb = $('.feedback', q); fb.hidden = true;
        });
        qs[0].scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
      });
    }
  }

  /* ---------------- Catálogo ---------------- */
  var cards = $$('[data-course-card]');
  if (cards.length) {
    var all = store.read();
    cards.forEach(function (card) {
      var r = all[card.getAttribute('data-course-card')], s = $('[data-status]', card);
      if (!r || !s) return;
      if (r.best !== null && r.best >= 80) { s.hidden = false; s.textContent = '★ Aprobado · ' + r.best + '%'; }
      else if ((r.read && r.read.length) || r.best !== null) { s.hidden = false; s.classList.add('is-progress'); s.textContent = 'En progreso' + (r.best !== null ? ' · mejor ' + r.best + '%' : ''); }
    });
  }

  function confetti() {
    var box = document.createElement('div'); box.className = 'confetti'; box.setAttribute('aria-hidden', 'true');
    var colors = ['#2563EB', '#38BDF8', '#D4AF37', '#123B66', '#0A192F'];
    for (var i = 0; i < 70; i++) {
      var p = document.createElement('i');
      p.style.left = (Math.random() * 100) + 'vw';
      p.style.background = colors[i % colors.length];
      p.style.animationDuration = (2.2 + Math.random() * 1.8) + 's';
      p.style.animationDelay = (Math.random() * .6) + 's';
      p.style.transform = 'rotate(' + (Math.random() * 360) + 'deg)';
      box.appendChild(p);
    }
    document.body.appendChild(box);
    setTimeout(function () { box.remove(); }, 4800);
  }
})();
