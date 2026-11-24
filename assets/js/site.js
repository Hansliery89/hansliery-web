/* =====================================================================
   HANSLIERY SÁNCHEZ · COMPLIANCE & RISK ADVISORY — JavaScript (Vanilla)
   Módulos independientes; cada uno falla de forma aislada sin romper el resto.
   ===================================================================== */
(function () {
  'use strict';

  /* ---------------------------------------------------------------
     CONFIGURACIÓN DE CONTACTO
     Para habilitar nuevos canales, complete los valores. Los vacíos no se muestran.
     - phone: '+1 809 000 0000'
     - whatsapp: solo dígitos con código de país, p. ej. '18090000000'
     - linkedin: URL completa del perfil
     --------------------------------------------------------------- */
  /* Los valores reales se definen en assets/sitio/build.py (bloque SITE) y llegan
     como window.SITE_CONFIG. Estos son solo valores de respaldo. */
  var CFG = window.SITE_CONFIG || {};
  var CONTACT_CONFIG = {
    email: CFG.email || 'sanchezfiguereohansliery@gmail.com',
    phone: CFG.phone || '',
    whatsapp: CFG.whatsapp || '',
    linkedin: CFG.linkedin || '',
    agenda: CFG.agenda || '',
    formEndpoint: CFG.formEndpoint || ''
  };

  var doc = document.documentElement;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
  var $ = function (s, ctx) { return (ctx || document).querySelector(s); };
  var $$ = function (s, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(s)); };
  var safe = function (name, fn) { try { fn(); } catch (err) { if (window.console) console.warn('[' + name + ']', err); } };

  /* Señal de carga para animaciones de entrada del hero */
  var markLoaded = function () { document.body.classList.add('is-loaded'); };
  if (document.readyState === 'complete') { requestAnimationFrame(markLoaded); }
  else { window.addEventListener('load', markLoaded); setTimeout(markLoaded, 1200); }

  /* ---------------------------------------------------------------
     1. Header dinámico + barra de progreso + volver arriba
     --------------------------------------------------------------- */
  safe('scroll', function () {
    var header = $('#header');
    var bar = $('.progress');
    var toTop = $('.to-top');
    var ticking = false;
    var update = function () {
      var y = window.scrollY || window.pageYOffset;
      var max = document.documentElement.scrollHeight - window.innerHeight;
      header.classList.toggle('is-scrolled', y > 24);
      bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(y / max, 1) : 0) + ')';
      toTop.classList.toggle('is-visible', y > window.innerHeight * 0.9);
      ticking = false;
    };
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    window.addEventListener('resize', update);
    update();
    toTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: reduceMotion.matches ? 'auto' : 'smooth' });
      var brand = $('.header .brand'); if (brand) brand.focus({ preventScroll: true });
    });
  });

  /* ---------------------------------------------------------------
     2. Menú móvil (accesible: aria-expanded, Escape, foco atrapado)
     --------------------------------------------------------------- */
  safe('menu', function () {
    var btn = $('.menu-toggle');
    var menu = $('#mobile-menu');
    var focusables = function () { return $$('a, button', menu).concat([btn]); };

    var setOpen = function (open) {
      btn.setAttribute('aria-expanded', String(open));
      btn.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
      menu.classList.toggle('is-open', open);
      menu.setAttribute('aria-hidden', String(!open));
      doc.classList.toggle('menu-open', open);
      if (open) { var first = $('a', menu); if (first) setTimeout(function () { first.focus(); }, 250); }
    };
    btn.addEventListener('click', function () { setOpen(btn.getAttribute('aria-expanded') !== 'true'); });
    $$('a', menu).forEach(function (a) { a.addEventListener('click', function () { setOpen(false); }); });
    document.addEventListener('keydown', function (e) {
      if (!menu.classList.contains('is-open')) return;
      if (e.key === 'Escape') { setOpen(false); btn.focus(); }
      if (e.key === 'Tab') {
        var f = focusables(); var first = f[0]; var last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    window.matchMedia('(min-width: 1101px)').addEventListener('change', function (mq) { if (mq.matches) setOpen(false); });
  });

  /* ---------------------------------------------------------------
     3. Enlace activo en navegación según la sección visible
     --------------------------------------------------------------- */
  safe('activeNav', function () {
    var links = $$('.nav-link, .m-link');
    /* Páginas interiores: el enlace activo lo define <body data-page> */
    var page = document.body.getAttribute('data-page');
    if (page && page !== 'inicio') {
      links.forEach(function (l) {
        if (l.getAttribute('data-nav') === page) { l.classList.add('is-active'); l.setAttribute('aria-current', 'page'); }
      });
      return;
    }
    if (!('IntersectionObserver' in window)) return;
    var map = {};
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var id = map[en.target.id] || en.target.id;
        links.forEach(function (l) {
          var on = l.getAttribute('data-nav') === id;
          l.classList.toggle('is-active', on);
          if (on) l.setAttribute('aria-current', 'true'); else l.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    $$('main section[id]').forEach(function (s) { io.observe(s); });
  });

  /* ---------------------------------------------------------------
     4. Aparición progresiva al desplazarse
     --------------------------------------------------------------- */
  safe('reveal', function () {
    var items = $$('[data-reveal], #method-track, #matrix, .cred-strip');
    if (!('IntersectionObserver' in window) || reduceMotion.matches) {
      items.forEach(function (el) { el.classList.add('is-visible'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-visible'); io.unobserve(en.target); }
      });
    }, { threshold: 0.14, rootMargin: '0px 0px -40px 0px' });
    items.forEach(function (el) { io.observe(el); });
  });

  /* ---------------------------------------------------------------
     5. Escritura progresiva del titular
     --------------------------------------------------------------- */
  safe('typing', function () {
    var lines = $$('.type-line');
    var texts = lines.map(function (l) { return $('.ghost', l).textContent; });
    if (reduceMotion.matches) {
      lines.forEach(function (l, i) { $('.typed', l).textContent = texts[i]; });
      return;
    }
    var li = 0, ci = 0;
    var step = function () {
      if (li >= lines.length) return;
      var line = lines[li], typed = $('.typed', line);
      line.classList.add('is-typing');
      ci++;
      typed.textContent = texts[li].slice(0, ci);
      if (ci < texts[li].length) { setTimeout(step, 34 + Math.random() * 30); }
      else {
        line.classList.remove('is-typing');
        if (li === lines.length - 1) { line.classList.add('is-done'); setTimeout(function () { line.classList.remove('is-done'); }, 4200); return; }
        li++; ci = 0; setTimeout(step, 260);
      }
    };
    setTimeout(step, 550);
  });

  /* ---------------------------------------------------------------
     6. Contadores numéricos animados
     --------------------------------------------------------------- */
  safe('counters', function () {
    var nums = $$('[data-count]');
    var fmt = function (v, d) { return v.toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d }); };
    if (reduceMotion.matches || !('IntersectionObserver' in window)) return; /* conserva el valor final escrito en HTML */
    var run = function (el) {
      var target = parseFloat(el.dataset.count), dec = parseInt(el.dataset.decimals || '0', 10), suf = el.dataset.suffix || '';
      var dur = 1900, t0 = null;
      var frame = function (t) {
        if (!t0) t0 = t;
        var p = Math.min((t - t0) / dur, 1), e = 1 - Math.pow(1 - p, 4);
        el.textContent = fmt(target * e, dec) + suf;
        if (p < 1) requestAnimationFrame(frame); else el.textContent = fmt(target, dec) + suf;
      };
      requestAnimationFrame(frame);
    };
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { run(en.target); io.unobserve(en.target); } });
    }, { threshold: 0.6 });
    nums.forEach(function (el) {
      el.textContent = fmt(0, parseInt(el.dataset.decimals || '0', 10)) + (el.dataset.suffix || '');
      io.observe(el);
    });
  });

  /* ---------------------------------------------------------------
     7. Matriz ilustrativa de probabilidad × impacto
     --------------------------------------------------------------- */
  safe('matrix', function () {
    var m = $('#matrix'); if (!m) return;
    var frag = document.createDocumentFragment();
    for (var r = 5; r >= 1; r--) {
      for (var c = 1; c <= 5; c++) {
        var s = r * c, lvl = s <= 4 ? 1 : s <= 9 ? 2 : s <= 15 ? 3 : 4;
        var cell = document.createElement('span');
        cell.className = 'cell l' + lvl + ((r === 4 && c === 4) || (r === 5 && c === 3) ? ' hot' : '');
        cell.style.setProperty('--cd', (((5 - r) + (c - 1)) * 0.06).toFixed(2) + 's');
        frag.appendChild(cell);
      }
    }
    m.appendChild(frag);
  });

  /* ---------------------------------------------------------------
     8. Red de partículas y conexiones (canvas del hero)
     Se pausa fuera de pantalla y con la pestaña oculta.
     --------------------------------------------------------------- */
  safe('network', function () {
    var canvas = $('#network'); if (!canvas || !canvas.getContext) return;
    var ctx = canvas.getContext('2d');
    var hero = $('.hero');
    var W = 0, H = 0, dpr = 1, pts = [], running = false, visible = true, raf = 0;
    var mouse = { x: -9999, y: -9999 };
    var COLORS = ['37,99,235', '56,189,248', '56,189,248', '37,99,235', '212,175,55'];

    var build = function () {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = canvas.clientWidth; H = canvas.clientHeight;
      canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.round(Math.min(Math.max((W * H) / 17000, 22), W < 640 ? 34 : 82));
      pts = [];
      for (var i = 0; i < n; i++) {
        pts.push({ x: Math.random() * W, y: Math.random() * H, vx: (Math.random() - .5) * .32, vy: (Math.random() - .5) * .32, r: Math.random() * 1.6 + .8, c: COLORS[i % COLORS.length] });
      }
    };
    var LINK = function () { return W < 640 ? 105 : 138; };

    var draw = function (move) {
      ctx.clearRect(0, 0, W, H);
      var L = LINK(), L2 = L * L, i, j, p, q, dx, dy, d2;
      for (i = 0; i < pts.length; i++) {
        p = pts[i];
        if (move) {
          p.x += p.vx; p.y += p.vy;
          if (p.x < -10) p.x = W + 10; else if (p.x > W + 10) p.x = -10;
          if (p.y < -10) p.y = H + 10; else if (p.y > H + 10) p.y = -10;
        }
        for (j = i + 1; j < pts.length; j++) {
          q = pts[j]; dx = p.x - q.x; dy = p.y - q.y; d2 = dx * dx + dy * dy;
          if (d2 < L2) {
            ctx.strokeStyle = 'rgba(56,189,248,' + (0.16 * (1 - d2 / L2)).toFixed(3) + ')';
            ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(q.x, q.y); ctx.stroke();
          }
        }
        dx = p.x - mouse.x; dy = p.y - mouse.y; d2 = dx * dx + dy * dy;
        if (d2 < 32000) {
          ctx.strokeStyle = 'rgba(37,99,235,' + (0.4 * (1 - d2 / 32000)).toFixed(3) + ')';
          ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(mouse.x, mouse.y); ctx.stroke();
        }
      }
      for (i = 0; i < pts.length; i++) {
        p = pts[i];
        ctx.fillStyle = 'rgba(' + p.c + ',.85)';
        ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fill();
      }
    };
    var loop = function () { draw(true); raf = requestAnimationFrame(loop); };
    var start = function () { if (!running && visible && !document.hidden && !reduceMotion.matches) { running = true; raf = requestAnimationFrame(loop); } };
    var stop = function () { running = false; cancelAnimationFrame(raf); };

    build(); draw(false); start();

    var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { build(); draw(false); }, 180); });
    document.addEventListener('visibilitychange', function () { document.hidden ? stop() : start(); });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) { visible = en[0].isIntersecting; visible ? start() : stop(); }).observe(hero);
    }
    if (finePointer.matches) {
      hero.addEventListener('pointermove', function (e) { var r = canvas.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top; });
      hero.addEventListener('pointerleave', function () { mouse.x = mouse.y = -9999; });
    }
    reduceMotion.addEventListener('change', function () { reduceMotion.matches ? (stop(), draw(false)) : start(); });
  });

  /* ---------------------------------------------------------------
     9. Iluminación que sigue al cursor + foco en tarjetas + inclinación 3D
     --------------------------------------------------------------- */
  safe('pointerFx', function () {
    if (!finePointer.matches || reduceMotion.matches) return;
    var glow = $('.cursor-glow'), pending = false, gx = 0, gy = 0;
    window.addEventListener('pointermove', function (e) {
      gx = e.clientX; gy = e.clientY;
      if (!pending) { pending = true; requestAnimationFrame(function () {
        glow.style.setProperty('--cx', gx + 'px'); glow.style.setProperty('--cy', gy + 'px');
        glow.classList.add('is-on'); pending = false;
      }); }
    }, { passive: true });
    document.addEventListener('pointerleave', function () { glow.classList.remove('is-on'); });

    $$('.card').forEach(function (card) {
      var tilt = card.hasAttribute('data-tilt');
      card.addEventListener('pointermove', function (e) {
        var r = card.getBoundingClientRect();
        var x = e.clientX - r.left, y = e.clientY - r.top;
        card.style.setProperty('--mx', x + 'px'); card.style.setProperty('--my', y + 'px');
        if (tilt) {
          var rx = ((y / r.height) - .5) * -7, ry = ((x / r.width) - .5) * 7;
          card.style.transform = 'translateY(-6px) rotateX(' + rx.toFixed(2) + 'deg) rotateY(' + ry.toFixed(2) + 'deg)';
        }
      });
      if (tilt) card.addEventListener('pointerleave', function () { card.style.transform = ''; });
    });
  });

  /* ---------------------------------------------------------------
     10. Botones "Consultar servicio" → preselecciona el servicio
     --------------------------------------------------------------- */
  safe('servicePrefill', function () {
    var select = $('#f-service');
    if (!select) return; /* páginas interiores: el enlace lleva ?svc= a la portada */
    $$('[data-service]').forEach(function (a) {
      a.addEventListener('click', function () {
        var val = a.getAttribute('data-service');
        var opt = Array.prototype.find.call(select.options, function (o) { return o.value === val; });
        if (opt) {
          select.value = val;
          select.dispatchEvent(new Event('change'));
          select.classList.remove('flash'); void select.offsetWidth; select.classList.add('flash');
        }
      });
    });
  });


  /* ---------------------------------------------------------------
     10b. Servicios: pestañas, buscador por necesidad y matriz de riesgo
     --------------------------------------------------------------- */
  safe('serviceTabs', function () {
    var tabs = $$('.sv-tablist [role="tab"]');
    if (!tabs.length) return;
    var panels = tabs.map(function (t) { return document.getElementById(t.getAttribute('aria-controls')); });
    var show = function (i, focus) {
      tabs.forEach(function (t, j) {
        var on = i === j;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        panels[j].hidden = !on;
        panels[j].classList.toggle('is-in', on);
      });
      if (focus) tabs[i].focus();
    };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { show(i); });
      t.addEventListener('keydown', function (e) {
        var k = e.key, n = tabs.length, j = null;
        if (k === 'ArrowRight' || k === 'ArrowDown') j = (i + 1) % n;
        else if (k === 'ArrowLeft' || k === 'ArrowUp') j = (i - 1 + n) % n;
        else if (k === 'Home') j = 0; else if (k === 'End') j = n - 1;
        if (j !== null) { e.preventDefault(); show(j, true); }
      });
    });
    show(0);
    var openSv = function (key) {
      var i = tabs.findIndex(function (t) { return t.getAttribute('data-sv') === key; });
      if (i >= 0) show(i);
      return i;
    };
    $$('.sv-need').forEach(function (b) {
      b.addEventListener('click', function () {
        $$('.sv-need').forEach(function (x) { x.classList.toggle('is-on', x === b); });
        var key = b.getAttribute('data-go');
        var target = key === 'diagnostico' ? (openSv('riesgos'), document.getElementById('diagnostico')) : key === 'saas' ? document.getElementById('compliance-guard-pro') : key === 'lexium' ? document.getElementById('lexium-legal-suite') : key === 'medinovaq' ? document.getElementById('medinovaq') : (openSv(key), document.querySelector('.sv-tabs'));
        if (target) target.scrollIntoView({ behavior: reduceMotion.matches ? 'auto' : 'smooth', block: 'start' });
      });
    });
    $$('[data-open-sv]').forEach(function (a) {
      a.addEventListener('click', function () { openSv(a.getAttribute('data-open-sv')); });
    });
    var dxHash = function () {
      if (location.hash !== '#diagnostico') return;
      openSv('riesgos');
      var c = document.getElementById('diagnostico');
      if (c) setTimeout(function () { c.scrollIntoView({ behavior: reduceMotion.matches ? 'auto' : 'smooth', block: 'center' }); }, 60);
    };
    window.addEventListener('hashchange', dxHash);
    if (location.hash === '#diagnostico') {
      if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
      dxHash();
      /* repetir cuando terminen de cargar fuentes e imágenes, que desplazan el contenido */
      window.addEventListener('load', function () { setTimeout(function () {
        openSv('riesgos');
        var c = document.getElementById('diagnostico');
        if (c) c.scrollIntoView({ behavior: 'auto', block: 'center' });
      }, 350); });
    }
  });

  safe('riskMatrix', function () {
    var sel = $('#mx-row');
    if (!sel) return;
    var D = [["SOF-01", "1. Entidades de intermediación financiera", "Cuenta de ahorro", "Sucursal", "República Dominicana (nacional)", [3, 2, 2, 1, 2], "KYC estándar, monitoreo transaccional", 0.1], ["SOF-02", "1. Entidades de intermediación financiera", "Cuenta corriente", "Sucursal", "República Dominicana (nacional)", [3, 3, 2, 1, 2], "KYC estándar, monitoreo transaccional", 0.1], ["SOF-03", "1. Entidades de intermediación financiera", "Transferencias / SWIFT", "Corresponsal bancario", "Países de Alto Riesgo GAFI (lista negra/gris)", [4, 5, 4, 5, 5], "Monitoreo reforzado, filtrado de listas, EDD", 0.3], ["SOF-04", "1. Entidades de intermediación financiera", "Tarjetas de crédito/débito", "ATM / Móvil", "República Dominicana (nacional)", [3, 3, 3, 1, 3], "Monitoreo transaccional, límites operacionales", 0.15], ["SOF-05", "1. Entidades de intermediación financiera", "Préstamos", "Sucursal", "República Dominicana (nacional)", [3, 3, 2, 1, 2], "Analisis de origen de fondos, KYC", 0.1], ["SOF-06", "1. Entidades de intermediación financiera", "Banca electrónica / banca móvil", "Web / app móvil", "Estados Unidos", [3, 3, 4, 2, 3], "Autenticación reforzada, monitoreo de geolocalización", 0.15], ["SOF-07", "2. Intermediarios de valores", "Corretaje de títulos valores", "Oficina / plataforma electrónica", "Unión Europea / España", [4, 4, 3, 2, 3], "EDD, verificación de origen de fondos", 0.2], ["SOF-08", "2. Intermediarios de valores", "Ventas a futuro (derivados)", "Plataforma electrónica", "Latinoamérica y el Caribe", [4, 5, 4, 3, 4], "Monitoreo reforzado, límites de exposición", 0.2], ["SOF-09", "3. Canje/cambio de divisas y remesas", "Cambio de divisas", "Sucursal", "Estados Unidos", [4, 5, 3, 2, 5], "Monitoreo reforzado, reporte de operaciones en efectivo", 0.25], ["SOF-10", "3. Canje/cambio de divisas y remesas", "Remesas internacionales", "Agente remesador", "Países de Alto Riesgo GAFI (lista negra/gris)", [4, 5, 3, 5, 5], "EDD, filtrado de listas OFAC/ONU, límites por operación", 0.3], ["SOF-11", "4. Banco Central de la República Dominicana", "Operaciones interbancarias / política monetaria", "Directo (interbancario)", "República Dominicana (nacional)", [1, 1, 1, 1, 1], "Supervisión regulatoria propia", 0.05], ["SOF-12", "5. Fiduciarias", "Administración de fideicomisos", "Oficina", "República Dominicana (nacional)", [4, 4, 2, 2, 3], "Verificación de beneficiario final (UBO), EDD", 0.2], ["SOF-13", "5. Fiduciarias", "Fideicomiso de administración inmobiliaria", "Oficina", "Latinoamérica y el Caribe", [4, 4, 2, 3, 3], "Verificación UBO, analisis de origen de fondos", 0.2], ["SOF-14", "6. Cooperativas de ahorro y crédito", "Cuenta de ahorro cooperativa", "Sucursal", "República Dominicana (nacional)", [2, 2, 2, 1, 2], "KYC estándar", 0.1], ["SOF-15", "6. Cooperativas de ahorro y crédito", "Préstamos cooperativos", "Sucursal", "República Dominicana (nacional)", [2, 2, 2, 1, 2], "KYC estándar, analisis de capacidad de pago", 0.1], ["SOF-16", "7. Cías. de seguros, reaseguro y corredores", "Seguro de vida con valor de rescate", "Corredor de seguros", "República Dominicana (nacional)", [3, 4, 3, 2, 3], "KYC, verificación de beneficiarios de póliza", 0.15], ["SOF-17", "7. Cías. de seguros, reaseguro y corredores", "Seguro general (no vida)", "Corredor de seguros", "República Dominicana (nacional)", [2, 2, 3, 1, 2], "KYC estándar", 0.1], ["SOF-18", "7. Cías. de seguros, reaseguro y corredores", "Reaseguro internacional", "Corredor de seguros", "Latinoamérica y el Caribe", [3, 3, 3, 3, 3], "Debida diligencia de contraparte", 0.15], ["SOF-19", "8. Sociedades administradoras de fondos de inversión", "Fondo de inversión abierto", "Oficina / plataforma", "República Dominicana (nacional)", [3, 3, 3, 2, 3], "KYC, monitoreo de aportes y retiros", 0.15], ["SOF-20", "9. Sociedades titularizadoras", "Titularización de activos", "Oficina", "República Dominicana (nacional)", [3, 4, 2, 2, 3], "Verificación de origen de activos titularizados", 0.15], ["SOF-21", "10. Puestos de bolsa e intermediarios de valores", "Operaciones bursátiles", "Puesto de bolsa", "República Dominicana (nacional)", [3, 3, 3, 2, 3], "KYC, monitoreo transaccional", 0.15], ["SOF-22", "11. Depósito centralizado de valores", "Custodia y compensación de valores", "Plataforma electrónica", "República Dominicana (nacional)", [2, 2, 2, 1, 2], "Controles operativos de custodia", 0.1], ["SOF-23", "12. Emisores de valores de oferta pública", "Emisión primaria de valores", "Oficina", "República Dominicana (nacional)", [3, 4, 2, 2, 3], "Verificación de prospecto y origen de fondos", 0.15], ["APNFD-01", "a. Casinos, juegos de azar, bancas de lotería y apuestas", "Compra de fichas", "Presencial", "República Dominicana (nacional)", [4, 5, 2, 1, 5], "EDD, límites de cambio en efectivo", 0.2], ["APNFD-02", "a. Casinos, juegos de azar, bancas de lotería y apuestas", "Pago de premios", "Caja / presencial", "República Dominicana (nacional)", [4, 5, 2, 1, 5], "EDD, verificación de identidad en premios altos", 0.2], ["APNFD-03", "a. Casinos, juegos de azar, bancas de lotería y apuestas", "Apuestas / lotería en línea", "En línea", "Latinoamérica y el Caribe", [4, 5, 4, 3, 5], "Monitoreo reforzado, verificación de origen de fondos", 0.2], ["APNFD-04", "b. Empresas de factoraje", "Factoraje de facturas", "Oficina", "República Dominicana (nacional)", [3, 3, 2, 1, 3], "Verificación de facturas y contraparte", 0.15], ["APNFD-05", "c. Agentes inmobiliarios", "Compra/venta de bienes inmuebles", "Presencial", "Latinoamérica y el Caribe", [4, 4, 2, 3, 4], "Verificación de origen de fondos y UBO", 0.2], ["APNFD-06", "d. Comerciantes de metales preciosos, piedras preciosas y joyas", "Venta de joyas / metales preciosos", "Tienda", "República Dominicana (nacional)", [3, 4, 2, 2, 3], "Limites de operaciones en efectivo", 0.15], ["APNFD-07", "d. Comerciantes de metales preciosos, piedras preciosas y joyas", "Compra/venta de piedras preciosas (alto valor)", "Tienda / comercio internacional", "Centros offshore (paraísos fiscales)", [4, 5, 2, 4, 4], "EDD, verificación de procedencia y certificación", 0.25], ["APNFD-08", "e. Abogados, notarios y contadores", "Compra, venta o remodelación de inmuebles", "Presencial", "Latinoamérica y el Caribe", [4, 4, 2, 3, 4], "Verificación de origen de fondos", 0.2], ["APNFD-09", "e. Abogados, notarios y contadores", "Administración del dinero, valores u otros bienes del cliente", "Oficina", "Unión Europea / España", [4, 4, 2, 3, 4], "Segregación de cuentas de cliente, EDD", 0.25], ["APNFD-10", "e. Abogados, notarios y contadores", "Administración de cuentas bancarias, ahorro o valores", "Oficina", "República Dominicana (nacional)", [4, 4, 2, 2, 4], "EDD, verificación de mandato", 0.2], ["APNFD-11", "e. Abogados, notarios y contadores", "Organización de contribuciones para creación/operación de empresas", "Oficina", "República Dominicana (nacional)", [4, 4, 2, 2, 3], "Verificación de origen de fondos de aportantes", 0.2], ["APNFD-12", "e. Abogados, notarios y contadores", "Creación/administración de personas jurídicas y compraventa de entidades", "Oficina", "Centros offshore (paraísos fiscales)", [5, 5, 2, 4, 4], "Verificación UBO reforzada, EDD", 0.25], ["APNFD-13", "e. Abogados, notarios y contadores", "Constitución de sociedades, fusión/escisión, compraventa de acciones", "Oficina", "Latinoamérica y el Caribe", [4, 4, 2, 3, 4], "Verificación UBO, EDD", 0.2], ["APNFD-14", "e. Abogados, notarios y contadores", "Actuación como agente de creación de personas jurídicas", "Oficina", "Centros offshore (paraísos fiscales)", [5, 5, 2, 4, 4], "Verificación UBO reforzada, EDD", 0.25], ["APNFD-15", "e. Abogados, notarios y contadores", "Actuación como director, apoderado o socio nominal", "Oficina", "Países de Alto Riesgo GAFI (lista negra/gris)", [5, 5, 2, 5, 4], "EDD reforzada, prohibición de estructuras opacas", 0.2], ["APNFD-16", "e. Abogados, notarios y contadores", "Provisión de domicilio registrado, comercial o postal", "Oficina", "Países de Alto Riesgo GAFI (lista negra/gris)", [5, 4, 2, 5, 3], "Verificación de actividad real del cliente", 0.15], ["APNFD-17", "e. Abogados, notarios y contadores", "Actuación o arreglo como accionista nominal para otra persona", "Oficina", "Países de Alto Riesgo GAFI (lista negra/gris)", [5, 5, 2, 5, 4], "EDD reforzada, verificación de titular real", 0.2], ["APNFD-18", "f. Comercio de vehículos, armas de fuego, barcos y aviones", "Venta de vehículos de motor", "Presencial", "República Dominicana (nacional)", [3, 3, 2, 1, 3], "Verificación de origen de fondos en pagos altos", 0.15], ["APNFD-19", "f. Comercio de vehículos, armas de fuego, barcos y aviones", "Venta de armas de fuego", "Presencial", "República Dominicana (nacional)", [4, 5, 2, 2, 4], "Verificación de licencia y antecedentes", 0.2], ["APNFD-20", "f. Comercio de vehículos, armas de fuego, barcos y aviones", "Venta de embarcaciones y aeronaves", "Presencial", "Centros offshore (paraísos fiscales)", [4, 5, 2, 4, 4], "Verificación de origen de fondos y titularidad", 0.2], ["APNFD-21", "g. Casas de empeño", "Préstamo con garantía prendaria", "Sucursal", "República Dominicana (nacional)", [3, 4, 2, 1, 4], "Verificación de identidad y origen del bien", 0.15], ["APNFD-22", "h. Empresas constructoras", "Venta de inmueble (proyecto constructivo)", "Oficina", "República Dominicana (nacional)", [3, 4, 2, 2, 3], "Verificación de origen de fondos", 0.15], ["APNFD-23", "h. Empresas constructoras", "Recepción de pagos en efectivo por construcción", "Oficina", "República Dominicana (nacional)", [3, 4, 2, 1, 4], "Limites de pagos en efectivo, verificación de origen", 0.2]];
    var W = [0.30, 0.20, 0.15, 0.25, 0.10];
    var CATS = [[1.5, 'Muy bajo', 'c1'], [2.5, 'Bajo', 'c2'], [3.5, 'Medio', 'c3'], [4.5, 'Alto', 'c4'], [99, 'Muy alto', 'c5']];
    var cat = function (v) { for (var i = 0; i < CATS.length; i++) if (v < CATS[i][0]) return CATS[i]; };
    var sl = [0, 1, 2, 3, 4].map(function (i) { return $('#mx-s' + i); });
    var ef = $('#mx-ef');
    var paint = function (id, v) {
      var c = cat(v), el = $('#' + id), ce = $('#' + id + '-cat'), bar = $('#' + id + '-bar');
      el.textContent = (Math.round((v + 1e-9) * 100) / 100).toFixed(2);
      ce.textContent = c[1]; ce.className = 'mx-cat ' + c[2];
      bar.className = c[2]; bar.style.background = ''; bar.style.width = (v / 5 * 100) + '%';
    };
    var calc = function () {
      var inh = 0;
      sl.forEach(function (s, i) { var v = +s.value; inh += v * W[i]; $('#mx-o' + i).textContent = v; });
      var e = +ef.value / 100;
      $('#mx-oef').textContent = ef.value + ' %';
      inh = Math.round(inh * 1000) / 1000;
      var res = Math.max(1, inh * (1 - e));
      paint('mx-inh', inh); paint('mx-res', res);
    };
    var load = function () {
      var r = D[+sel.value];
      r[5].forEach(function (v, i) { sl[i].value = v; });
      ef.value = Math.round(r[7] * 100);
      $('#mx-ctx').textContent = r[1].replace(/^[0-9a-h]+\.\s*/, '') + ' · Canal: ' + r[3] + ' · Jurisdicción: ' + r[4];
      var c = $('#mx-ctl'); c.textContent = '';
      var b = document.createElement('b'); b.textContent = 'Controles de referencia: ';
      c.appendChild(b); c.appendChild(document.createTextNode(r[6] + ' (efectividad estimada ' + Math.round(r[7] * 100) + ' %).'));
      calc();
    };
    sel.addEventListener('change', load);
    sl.concat(ef).forEach(function (s) { s.addEventListener('input', calc); });
    load();
  });


  /* ---------------------------------------------------------------
     10c. Costos: moneda, calculadora de factura y planes
     --------------------------------------------------------------- */
  safe('pricing', function () {
    var sec = document.getElementById('costos');
    if (!sec || !sec.querySelector('.pc-switch')) return; /* la portada solo muestra un resumen */
    var fmt = function (n, cur) {
      return (cur === 'usd' ? 'US$' : 'RD$') + Math.round(n).toLocaleString('en-US');
    };
    var fmt2 = function (n) { return 'RD$' + n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); };
    var note = $('#pc-note');
    var setCur = function (cur) {
      $$('.pc-switch [data-cur]', sec).forEach(function (b) { b.setAttribute('aria-checked', b.getAttribute('data-cur') === cur ? 'true' : 'false'); });
      $$('.pc-amt', sec).forEach(function (el) { el.textContent = fmt(+el.getAttribute('data-' + cur), cur); });
      $$('[data-tax]', sec).forEach(function (el) { el.textContent = cur === 'dop' ? '+ ITBIS (18 %)' : 'ITBIS según evaluación'; });
      note.textContent = cur === 'dop'
        ? 'Precios en pesos dominicanos. No incluyen el ITBIS (18 %), que se detalla en la factura electrónica.'
        : 'Precios en dólares para clientes fuera de la República Dominicana, con servicio virtual. Impuestos según la propuesta.';
      var calc = $('#pc-calc'); if (calc) calc.classList.toggle('is-muted', cur !== 'dop');
    };
    $$('.pc-switch [data-cur]', sec).forEach(function (b, i, all) {
      b.addEventListener('click', function () { setCur(b.getAttribute('data-cur')); });
      b.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); var n = all[(i + 1) % all.length]; n.focus(); setCur(n.getAttribute('data-cur')); }
      });
    });
    setCur('dop');

    var svc = $('#pcc-svc'), em = $('#pcc-em'), cl = $('#pcc-cl');
    var calc = function () {
      var sub = +svc.value, itbis = sub * 0.18, tot = sub + itbis, isr = 0, rit = 0, txt;
      if (cl.value === 'pj') {
        if (em.value === 'pf') {
          isr = sub * 0.15; rit = itbis;
          txt = 'Persona física que factura a una empresa: la empresa retiene el 15 % del ISR sobre el subtotal (art. 309 del Código Tributario, modificado por la Ley 30-26, como pago a cuenta) y el 100 % del ITBIS facturado, y los entrega a la DGII.';
        } else {
          rit = itbis * 0.30;
          txt = 'Sociedad que factura a otra sociedad: puede corresponder la retención del 30 % del ITBIS por servicios profesionales liberales (Norma General 02-05). No hay retención de ISR.';
        }
      } else {
        txt = 'Cliente sin RNC: se emite factura de consumo electrónica (E32) y no hay retenciones.';
      }
      $('#pcc-sub').textContent = fmt2(sub);
      $('#pcc-itbis').textContent = fmt2(itbis);
      $('#pcc-tot').textContent = fmt2(tot);
      $('#pcc-isr').textContent = isr ? '− ' + fmt2(isr) : 'No aplica';
      $('#pcc-rit').textContent = rit ? '− ' + fmt2(rit) : 'No aplica';
      $('#pcc-net').textContent = fmt2(tot - isr - rit);
      $('#pcc-note').textContent = txt + ' Cálculo orientativo; confirme con su contador.';
    };
    [svc, em, cl].forEach(function (s) { s.addEventListener('change', calc); });
    calc();

    $$('[data-plan]', sec).forEach(function (a) {
      a.addEventListener('click', function () {
        var msg = $('#f-msg');
        if (msg && !msg.value.trim()) { msg.value = 'Me interesa el ' + a.getAttribute('data-plan') + ' de acompañamiento continuo. '; msg.dispatchEvent(new Event('input')); }
      });
    });
  });

  /* ---------------------------------------------------------------
     10d. Contacto prellenado desde el diagnóstico preliminar
     --------------------------------------------------------------- */
  safe('diagnosticPrefill', function () {
    var q = new URLSearchParams(location.search);
    /* Enlaces desde páginas interiores: index.html?svc=<servicio>&plan=<plan>#contacto */
    if (q.get('svc')) {
      var s = $('#f-service'), mm = $('#f-msg'), want = q.get('svc').slice(0, 80);
      if (s && Array.prototype.some.call(s.options, function (o) { return o.value === want; })) { s.value = want; s.dispatchEvent(new Event('change')); }
      var plan = (q.get('plan') || '').slice(0, 60);
      if (mm && !mm.value.trim() && /^Plan (Esencial|Profesional|Corporativo)$/.test(plan)) {
        mm.value = 'Me interesa el ' + plan + ' de acompañamiento continuo. '; mm.dispatchEvent(new Event('input'));
      }
      return;
    }
    if (q.get('servicio') === 'lexium') {
      var sel = $('#f-service'), m = $('#f-msg');
      if (sel) { sel.value = 'LEXIUM Legal Suite (demostración)'; sel.dispatchEvent(new Event('change')); }
      if (m && !m.value.trim()) { m.value = 'Exploré la demo pública de LEXIUM Legal Suite y me interesa una demostración guiada para mi firma.'; m.dispatchEvent(new Event('input')); }
      return;
    }
    if (q.get('servicio') !== 'riesgos') return;
    var select = $('#f-service'), msg = $('#f-msg');
    if (select) { select.value = 'Gestión de riesgos y debida diligencia'; select.dispatchEvent(new Event('change')); }
    var cats = ['Muy bajo', 'Bajo', 'Medio', 'Alto', 'Muy alto'];
    var c = q.get('dx'), pts = parseInt(q.get('pts'), 10);
    if (msg && !msg.value.trim() && cats.indexOf(c) > -1 && pts >= 0 && pts <= 100) {
      msg.value = 'Completé el diagnóstico preliminar de riesgos LA/FT (riesgo residual estimado: ' + c + ', ' + pts + '/100) y me interesa profundizar en los resultados.';
      msg.dispatchEvent(new Event('input'));
    }
  });


  /* ---------------------------------------------------------------
     11. Utilidades: copiar al portapapeles y aviso temporal
     --------------------------------------------------------------- */
  var toastEl = $('#toast'), toastT;
  var toast = function (msg) {
    toastEl.textContent = msg; toastEl.classList.add('is-on');
    clearTimeout(toastT); toastT = setTimeout(function () { toastEl.classList.remove('is-on'); }, 2600);
  };
  var copyText = function (text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function (res, rej) {
      var ta = document.createElement('textarea');
      ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy') ? res() : rej(new Error('copy')); } catch (e) { rej(e); }
      document.body.removeChild(ta);
    });
  };
  safe('copy', function () {
    $$('[data-copy]').forEach(function (b) {
      b.addEventListener('click', function () {
        copyText(b.getAttribute('data-copy'))
          .then(function () { toast('Dirección de correo copiada'); })
          .catch(function () { toast('No se pudo copiar. Seleccione el correo manualmente.'); });
      });
    });
  });

  /* ---------------------------------------------------------------
     12. Canales de contacto adicionales (arquitectura preparada)
     Se construyen con textContent / atributos: sin inyección de HTML.
     --------------------------------------------------------------- */
  safe('channels', function () {
    var list = $('#channels'); if (!list) return;
    var items = [];
    if (CONTACT_CONFIG.phone) items.push({ label: 'Teléfono: ' + CONTACT_CONFIG.phone, href: 'tel:' + CONTACT_CONFIG.phone.replace(/[^\d+]/g, '') });
    if (CONTACT_CONFIG.whatsapp) items.push({ label: 'Escribir por WhatsApp', href: 'https://wa.me/' + CONTACT_CONFIG.whatsapp.replace(/\D/g, '') + '?text=' + encodeURIComponent('Hola, Hansliery. Le escribo desde su sitio web.'), ext: true });
    if (CONTACT_CONFIG.agenda && /^https:\/\//i.test(CONTACT_CONFIG.agenda)) items.push({ label: 'Agendar una reunión de 30 minutos', href: CONTACT_CONFIG.agenda, ext: true });
    if (CONTACT_CONFIG.linkedin && /^https:\/\/([a-z]+\.)?linkedin\.com\//i.test(CONTACT_CONFIG.linkedin)) items.push({ label: 'LinkedIn', href: CONTACT_CONFIG.linkedin, ext: true });
    if (!items.length) return;
    items.forEach(function (it) {
      var li = document.createElement('li'), a = document.createElement('a');
      a.className = 'channel'; a.href = it.href; a.textContent = it.label;
      if (it.ext) { a.target = '_blank'; a.rel = 'noopener noreferrer'; }
      li.appendChild(a); list.appendChild(li);
    });
    list.hidden = false;
  });

  /* ---------------------------------------------------------------
     13. Formulario: validación + generación de correo (mailto)
     No hay servidor: se abre el cliente de correo del visitante.
     --------------------------------------------------------------- */
  safe('form', function () {
    var form = $('#contact-form'); if (!form) return;
    var f = {
      name: $('#f-name'), email: $('#f-email'), org: $('#f-org'),
      service: $('#f-service'), msg: $('#f-msg'), hp: $('#f-web')
    };
    var status = $('#form-status');
    var counter = $('#c-msg');
    var MAX_MSG = 1500;

    /* Limpieza: elimina caracteres de control y etiquetas, normaliza espacios y limita longitud */
    var clean = function (v, max, multiline) {
      v = String(v || '').normalize('NFC');
      v = multiline ? v.replace(/[\u0000-\u0009\u000B-\u001F\u007F]/g, '') : v.replace(/[\u0000-\u001F\u007F]/g, ' ');
      v = v.replace(/<[^>]*>/g, '');
      v = multiline ? v.replace(/[ \t]+/g, ' ').replace(/\n{3,}/g, '\n\n') : v.replace(/\s+/g, ' ');
      return v.trim().slice(0, max);
    };
    var EMAIL_RE = /^[^\s@<>()[\]\\,;:"]+@[^\s@<>()[\]\\,;:"]+\.[a-z]{2,}$/i;

    var rules = {
      name: function (v) { return v.length < 2 ? 'Escriba su nombre (mínimo 2 caracteres).' : !/[a-záéíóúüñ]/i.test(v) ? 'El nombre debe contener letras.' : ''; },
      email: function (v) { return !v ? 'Escriba su correo electrónico.' : !EMAIL_RE.test(v) ? 'Revise el formato del correo, por ejemplo: nombre@organizacion.com.' : ''; },
      org: function () { return ''; },
      service: function (v) { return !v ? 'Seleccione el servicio de su interés.' : ''; },
      msg: function (v) { return v.length < 20 ? 'Describa su necesidad con al menos 20 caracteres (lleva ' + v.length + ').' : ''; }
    };
    var errorId = { name: 'e-name', email: 'e-email', org: 'e-org', service: 'e-service', msg: 'e-msg' };
    var limits = { name: 80, email: 120, org: 120, service: 80, msg: MAX_MSG };

    var value = function (key) { return clean(f[key].value, limits[key], key === 'msg'); };
    var check = function (key) {
      var err = rules[key](value(key));
      $('#' + errorId[key]).textContent = err;
      if (err) f[key].setAttribute('aria-invalid', 'true'); else f[key].removeAttribute('aria-invalid');
      return !err;
    };

    Object.keys(rules).forEach(function (key) {
      f[key].addEventListener('blur', function () { if (f[key].value || f[key].hasAttribute('aria-invalid')) check(key); });
      f[key].addEventListener(key === 'service' ? 'change' : 'input', function () { if (f[key].hasAttribute('aria-invalid')) check(key); });
    });
    var updateCount = function () { counter.textContent = f.msg.value.length + ' / ' + MAX_MSG; };
    f.msg.addEventListener('input', updateCount); updateCount();

    var showStatus = function (type, nodes) {
      status.className = 'form-status ' + (type === 'ok' ? 'is-ok' : 'is-error');
      status.textContent = '';
      nodes.forEach(function (n) { status.appendChild(n); });
    };
    var el = function (tag, text, attrs) {
      var n = document.createElement(tag); if (text) n.textContent = text;
      if (attrs) Object.keys(attrs).forEach(function (k) { n.setAttribute(k, attrs[k]); });
      return n;
    };

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (f.hp.value) return; /* envío automatizado: se ignora */

      var keys = ['name', 'email', 'org', 'service', 'msg'];
      var invalid = keys.filter(function (k) { return !check(k); });
      if (invalid.length) {
        showStatus('error', [el('strong', 'Revise los campos marcados. '), el('span', invalid.length === 1 ? 'Hay 1 campo por corregir.' : 'Hay ' + invalid.length + ' campos por corregir.')]);
        f[invalid[0]].focus();
        return;
      }

      var data = { name: value('name'), email: value('email'), org: value('org'), service: value('service'), msg: value('msg') };

      /* Envío directo (Formspree u otro servicio compatible) si está configurado */
      if (CONTACT_CONFIG.formEndpoint && window.fetch) {
        var btn = form.querySelector('[type="submit"]');
        btn.disabled = true;
        showStatus('ok', [el('span', 'Enviando su mensaje…')]);
        fetch(CONTACT_CONFIG.formEndpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
          body: JSON.stringify({ nombre: data.name, email: data.email, organizacion: data.org || 'No indicada', servicio: data.service, mensaje: data.msg, _subject: 'Consulta web: ' + data.service })
        }).then(function (r) {
          if (!r.ok) throw new Error('HTTP ' + r.status);
          form.reset(); updateCount();
          showStatus('ok', [el('strong', 'Mensaje enviado. '), el('span', 'Gracias, ' + data.name + '. La respuesta llegará a ' + data.email + '.')]);
          status.focus({ preventScroll: true });
        }).catch(function () {
          showStatus('error', [el('strong', 'No se pudo enviar. '), el('span', 'Escriba directamente a ' + CONTACT_CONFIG.email + ' o inténtelo de nuevo en unos minutos.')]);
        }).then(function () { btn.disabled = false; });
        return;
      }
      var subject = clean('Consulta: ' + data.service + ' — ' + data.name, 140, false);
      var body = [
        'Hola, Hansliery:',
        '',
        data.msg,
        '',
        '— — —',
        'Nombre: ' + data.name,
        'Correo: ' + data.email,
        'Organización: ' + (data.org || 'No indicada'),
        'Servicio de interés: ' + data.service,
        '',
        'Mensaje preparado desde el formulario del sitio web.'
      ].join('\r\n');
      var href = 'mailto:' + CONTACT_CONFIG.email + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      var plain = 'Para: ' + CONTACT_CONFIG.email + '\nAsunto: ' + subject + '\n\n' + body.replace(/\r\n/g, '\n');

      var openLink = el('a', 'Abrir correo de nuevo', { href: href, 'class': 'copy-btn' });
      var copyBtn = el('button', 'Copiar mensaje', { type: 'button', 'class': 'copy-btn' });
      copyBtn.addEventListener('click', function () {
        copyText(plain).then(function () { toast('Mensaje copiado. Péguelo en su correo.'); })
                       .catch(function () { toast('No se pudo copiar el mensaje.'); });
      });
      var actions = el('div', null, { 'class': 'status-actions' });
      actions.appendChild(openLink); actions.appendChild(copyBtn);
      showStatus('ok', [
        el('strong', 'Su mensaje está listo. '),
        el('span', 'Se abrirá su aplicación de correo con el contenido preparado; el envío se completa desde allí. Si no se abre, copie el mensaje y envíelo a ' + CONTACT_CONFIG.email + '.'),
        actions
      ]);
      status.focus({ preventScroll: true });
      window.location.href = href;
    });
  });

  /* ---------------------------------------------------------------
     14. Bloques plegables: abiertos en escritorio, plegados en móvil
     --------------------------------------------------------------- */
  safe('collapsibles', function () {
    var items = $$('details[data-desktop-open]');
    if (!items.length) return;
    var mq = window.matchMedia('(min-width: 861px)');
    var apply = function () { items.forEach(function (d) { d.open = mq.matches; }); };
    apply();
    mq.addEventListener('change', apply);
  });

})();
