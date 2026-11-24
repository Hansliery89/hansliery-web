#!/usr/bin/env python3
"""
Generador del sitio principal (portada y páginas interiores).

Uso:   python3 assets/sitio/build.py      (desde la raíz del repositorio)

- El contenido de cada página está en assets/sitio/paginas/<nombre>.html
- Encabezado, menú, pie, iconos y metadatos son comunes y se definen aquí,
  así todas las páginas quedan siempre sincronizadas.
- Estilos: assets/css/site.css · Comportamiento: assets/js/site.js
- No requiere dependencias externas (solo Python 3.8+).
"""
import html
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[2]
AQUI = pathlib.Path(__file__).resolve().parent

# =====================================================================
#  CONFIGURACIÓN — edite aquí sus datos. Los valores vacíos no se muestran.
# =====================================================================
SITE = {
    # Dirección pública. Si compra un dominio, cámbiela aquí y vuelva a generar.
    "url": "https://hansliery89.github.io/hansliery-web/",
    # Ruta base en el servidor (para la página 404). Con dominio propio: "/"
    "base_path": "/hansliery-web/",
    # False = oculto para buscadores (noindex). True = visible en Google + sitemap.xml
    "indexable": False,

    "email": "sanchezfiguereohansliery@gmail.com",
    "linkedin": "https://www.linkedin.com/in/hansliery-sanchez-figuereo-mlrm-b49ba254/",
    # Solo dígitos con código de país, p. ej. "18095551234"
    "whatsapp": "",
    "phone": "",
    # Enlace de agenda (Calendly, Google Calendar, Microsoft Bookings…), p. ej. "https://calendly.com/usuario/30min"
    "agenda": "",
    # Envío directo del formulario. Cree un formulario gratis en https://formspree.io
    # y pegue aquí su dirección, p. ej. "https://formspree.io/f/abcdwxyz".
    # Vacío = el formulario prepara el correo en la aplicación del visitante.
    "form_endpoint": "",
    # Analítica sin cookies con Plausible: escriba el dominio registrado en plausible.io
    "plausible_domain": "",
}

# Testimonios: agregue solo testimonios reales y autorizados por escrito.
# La sección aparece en la portada cuando la lista tiene al menos uno.
# Ejemplo:
# {"texto": "…", "nombre": "María Pérez", "cargo": "Oficial de cumplimiento", "organizacion": "Empresa X (con autorización)"}
TESTIMONIOS = []

NAV = [
    ("servicios", "Servicios", "index.html#servicios"),
    ("sobre-mi", "Sobre mí", "sobre-mi.html"),
    ("software", "Software", "software.html"),
    ("cursos", "Cursos", "cursos/index.html"),
    ("costos", "Costos", "costos.html"),
]


def esc(v):
    return html.escape(v, quote=True)


def csp():
    script = ["'self'", "'unsafe-inline'"]
    connect = []
    form = ["'none'"]
    if SITE["form_endpoint"]:
        origin = re.match(r"https://[^/]+", SITE["form_endpoint"]).group(0)
        connect.append(origin)
    if SITE["plausible_domain"]:
        script.append("https://plausible.io")
        connect.append("https://plausible.io")
    return ("default-src 'self'; script-src " + " ".join(script)
            + "; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; "
            "img-src 'self' data:; connect-src " + (" ".join(connect) if connect else "'none'")
            + "; object-src 'none'; base-uri 'self'; form-action " + " ".join(form))


def head(p):
    url = SITE["url"] + ("" if p["out"] == "index.html" else p["out"])
    robots = "index, follow" if SITE["indexable"] else "noindex, nofollow, noarchive, nosnippet"
    og = SITE["url"] + "assets/og-image.jpg"
    base = f'\n  <base href="{esc(SITE["base_path"])}">' if p.get("base") else ""
    cfg = {"email": SITE["email"], "linkedin": SITE["linkedin"], "whatsapp": SITE["whatsapp"],
           "phone": SITE["phone"], "agenda": SITE["agenda"], "formEndpoint": SITE["form_endpoint"]}
    analytics = ""
    if SITE["plausible_domain"]:
        analytics = f'\n  <script defer data-domain="{esc(SITE["plausible_domain"])}" src="https://plausible.io/js/script.js"></script>'
    jsonld = ""
    if p["out"] == "index.html":
        jsonld = "\n  " + (AQUI / "partes" / "jsonld.html").read_text(encoding="utf-8").replace("\n", "\n  ").replace("og-image.png", "og-image.jpg")
    return f"""<!DOCTYPE html>
<html lang="es-DO">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">{base}
  <!-- Página generada por assets/sitio/build.py: edite assets/sitio/paginas/{p['src']} -->
  <title>{esc(p['title'])}</title>
  <meta name="description" content="{esc(p['desc'])}">
  <meta name="author" content="Hansliery Sánchez">
  <meta name="robots" content="{robots}">
  <meta name="googlebot" content="{'index, follow' if SITE['indexable'] else 'noindex, nofollow'}">
  <meta name="theme-color" content="#FFFFFF">
  <meta name="color-scheme" content="light">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <meta http-equiv="Content-Security-Policy" content="{csp()}">
  <link rel="canonical" href="{esc(url)}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="es_DO">
  <meta property="og:site_name" content="HANSLIERY SÁNCHEZ · Compliance &amp; Risk Advisory">
  <meta property="og:title" content="{esc(p['title'])}">
  <meta property="og:description" content="{esc(p['desc'])}">
  <meta property="og:image" content="{og}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="HANSLIERY SÁNCHEZ · Compliance &amp; Risk Advisory">
  <meta property="og:url" content="{esc(url)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(p['title'])}">
  <meta name="twitter:description" content="{esc(p['desc'])}">
  <meta name="twitter:image" content="{og}">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Sora:wght@500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/site.css">
  <script>document.documentElement.classList.add('js');window.SITE_CONFIG={json.dumps(cfg, ensure_ascii=False)};</script>{analytics}{jsonld}
</head>"""


def header(active):
    links = "\n".join(
        f'          <li><a class="nav-link" data-nav="{k}" href="{h}">{t}</a></li>' for k, t, h in NAV)
    mlinks = "\n".join(
        f'        <li><a class="m-link" data-nav="{k}" href="{h}">{t}</a></li>' for k, t, h in NAV)
    sprite = (AQUI / "partes" / "sprite.svg").read_text(encoding="utf-8")
    return f"""
<body data-page="{active}">
  <a class="skip-link" href="#main">Saltar al contenido</a>
  <div class="progress" aria-hidden="true"></div>
  <div class="cursor-glow" aria-hidden="true"></div>

{sprite}
  <header class="header" id="header">
    <div class="container header-inner">
      <a class="brand" href="index.html" aria-label="HANSLIERY SÁNCHEZ · Compliance & Risk Advisory — ir al inicio">
        <svg class="brand-mark" aria-hidden="true"><use href="#logo-mark"/></svg>
        <span class="brand-text">
          <span class="brand-name">HANSLIERY <b>SÁNCHEZ</b></span>
          <span class="brand-tag">COMPLIANCE &amp; RISK ADVISORY</span>
        </span>
      </a>
      <nav class="nav" aria-label="Navegación principal">
        <ul class="nav-list">
{links}
        </ul>
        <a class="btn btn-primary btn-sm" href="index.html#contacto">Conversemos <svg aria-hidden="true"><use href="#i-arrow"/></svg></a>
      </nav>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="Abrir menú">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>

  <div class="mobile-menu" id="mobile-menu" aria-hidden="true">
    <nav aria-label="Navegación móvil">
      <ol>
{mlinks}
      </ol>
    </nav>
    <div class="mobile-menu-foot">
      <a class="btn btn-primary" href="index.html#contacto">Conversemos <svg aria-hidden="true"><use href="#i-arrow"/></svg></a>
      <a class="mail" href="mailto:{esc(SITE['email'])}">{esc(SITE['email'])}</a>
      <a class="mail" href="{esc(SITE['linkedin'])}" target="_blank" rel="noopener noreferrer">LinkedIn</a>
    </div>
  </div>
"""


def footer():
    nav = "\n".join(f'            <li><a href="{h}">{t}</a></li>' for _, t, h in NAV)
    return f"""
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a class="brand" href="index.html" aria-label="Hansliery Sánchez — volver al inicio">
            <svg class="brand-mark" aria-hidden="true"><use href="#logo-mark"/></svg>
            <span class="brand-text">
              <span class="brand-name">HANSLIERY <b>SÁNCHEZ</b></span>
              <span class="brand-tag">COMPLIANCE &amp; RISK ADVISORY</span>
            </span>
          </a>
          <p class="slogan">Estrategia. <span class="grad">Prevención.</span> <span class="grad-gold">Confianza.</span></p>
        </div>
        <nav aria-label="Navegación del pie de página">
          <h4>Navegación</h4>
          <ul class="footer-nav">
            <li><a href="index.html">Inicio</a></li>
{nav}
            <li><a href="diagnostico-riesgos.html">Diagnóstico gratuito</a></li>
            <li><a href="index.html#contacto">Contacto</a></li>
          </ul>
        </nav>
        <nav aria-label="Información legal">
          <h4>Legal</h4>
          <ul class="footer-nav">
            <li><a href="legal/terminos-de-uso.html">Términos de uso</a></li>
            <li><a href="legal/politica-de-privacidad.html">Política de privacidad</a></li>
            <li><a href="legal/cookies-y-almacenamiento.html">Cookies y almacenamiento</a></li>
            <li><a href="legal/aviso-legal.html">Aviso legal</a></li>
            <li><a href="legal/accesibilidad.html">Accesibilidad</a></li>
          </ul>
        </nav>
        <div>
          <h4>Contacto</h4>
          <a class="footer-mail" href="mailto:{esc(SITE['email'])}">{esc(SITE['email'])}</a>
          <a class="footer-li" href="{esc(SITE['linkedin'])}" target="_blank" rel="noopener noreferrer"><svg aria-hidden="true"><use href="#i-linkedin"/></svg>LinkedIn</a>
          <p class="footer-region">República Dominicana · Latinoamérica · Proyección internacional</p>
        </div>
      </div>
      <p class="disclaimer"><strong>Aviso profesional.</strong> El contenido de este sitio tiene fines informativos y formativos. Los servicios se ofrecen a título personal y no constituyen representación de empleadores, autoridades u organismos públicos. La información no sustituye asesoría jurídica especializada ni la evaluación independiente que corresponda a cada organización.</p>
      <div class="footer-bottom">
        <span>© 2026 HANSLIERY SÁNCHEZ · Compliance &amp; Risk Advisory · Todos los derechos reservados</span>
        <span class="footer-legal-mini"><a href="legal/politica-de-privacidad.html">Privacidad</a> · <a href="legal/terminos-de-uso.html">Términos</a> · <a href="legal/cookies-y-almacenamiento.html">Cookies</a></span>
      </div>
    </div>
  </footer>

  <button class="to-top" type="button" aria-label="Volver arriba"><svg aria-hidden="true"><use href="#i-up"/></svg></button>
  <div class="toast" id="toast" role="status" aria-live="polite"></div>
  <script src="assets/js/site.js"></script>
</body>
</html>
"""


def testimonios_html():
    if not TESTIMONIOS:
        return ""
    cards = "\n".join(
        f'''          <figure class="card quote" data-reveal>
            <blockquote><p>{esc(t["texto"])}</p></blockquote>
            <figcaption><b>{esc(t["nombre"])}</b><span>{esc(t["cargo"])} · {esc(t["organizacion"])}</span></figcaption>
          </figure>''' for t in TESTIMONIOS)
    return f'''
    <section class="section quotes" id="testimonios" aria-labelledby="test-title">
      <div class="container">
        <header class="section-head center">
          <p class="eyebrow" data-reveal>Testimonios</p>
          <h2 class="h2" id="test-title" data-reveal>Lo que dicen quienes han trabajado conmigo.</h2>
        </header>
        <div class="quote-grid">
{cards}
        </div>
      </div>
    </section>
'''


META_RE = re.compile(r"^<!--\s*(.*?)\s*-->\s*\n", re.S)


def leer(src):
    raw = (AQUI / "paginas" / src).read_text(encoding="utf-8")
    m = META_RE.match(raw)
    if not m:
        sys.exit(f"{src}: falta el bloque de metadatos inicial")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    meta["src"] = src
    meta["base"] = meta.get("base") == "si"
    return meta, raw[m.end():]


def main():
    salidas = []
    for src in sorted(p.name for p in (AQUI / "paginas").glob("*.html")):
        meta, cuerpo = leer(src)
        cuerpo = cuerpo.replace("{{TESTIMONIOS}}", testimonios_html())
        if SITE["form_endpoint"]:
            how = ("El formulario envía su mensaje directamente a mi correo mediante Formspree. "
                   "Solo se usan los datos que usted escribe, para responder a su consulta.")
            helptext = "Al enviar, sus datos se usan solo para responder a su consulta."
            btn = "Enviar mensaje"
        else:
            how = ("El formulario no almacena ni transmite información a ningún servidor. Al pulsar «Preparar correo», "
                   "se abrirá su aplicación de correo con el mensaje redactado, y usted decide si lo envía.")
            helptext = "El envío se realiza mediante el cliente de correo de su dispositivo. Este sitio no guarda sus datos."
            btn = "Preparar correo"
        cuerpo = cuerpo.replace("{{FORM_HOW}}", f'''<div class="how" data-reveal style="--d:.26s">
            <strong><svg aria-hidden="true"><use href="#i-lock"/></svg>¿Cómo se envía el formulario?</strong>
            <p>{how}</p>
          </div>''')
        cuerpo = cuerpo.replace("{{FORM_HELP}}", f'<p id="form-help"><svg aria-hidden="true"><use href="#i-info"/></svg>{helptext} <a href="legal/politica-de-privacidad.html">Política de privacidad</a>.</p>')
        cuerpo = cuerpo.replace("{{FORM_BTN}}", btn)
        cuerpo = cuerpo.replace("{{EMAIL}}", esc(SITE["email"]))
        out = head(meta) + header(meta["active"]) + '\n  <main id="main">\n' + cuerpo.rstrip() + "\n  </main>\n" + footer()
        if "{{" in out:
            sys.exit(f"{src}: marcador sin reemplazar")
        (RAIZ / meta["out"]).write_text(out, encoding="utf-8")
        salidas.append(meta["out"])

    if SITE["indexable"]:
        urls = "\n".join(f"  <url><loc>{SITE['url']}{'' if o == 'index.html' else o}</loc></url>"
                         for o in salidas if o != "404.html")
        (RAIZ / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + urls + "\n</urlset>\n", encoding="utf-8")
    print("Generadas:", ", ".join(salidas))


if __name__ == "__main__":
    main()
