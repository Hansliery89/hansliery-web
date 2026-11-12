#!/usr/bin/env python3
"""
Generador de los cursos de HANSLIERY SÁNCHEZ · Compliance & Risk Advisory.

El contenido de cada curso vive en los módulos cursos_*.py (listas COURSES).
Este script produce páginas HTML estáticas (buenas para SEO y legibles sin JavaScript):

    cursos/index.html          -> catálogo
    cursos/<slug>.html         -> una página por curso

Uso:  python3 cursos/_fuente/build.py
Referencias a fuentes dentro del texto: escriba [[n]] y se convierte en un enlace
a la fuente número n del curso.
"""
import hashlib, html, json, random, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
SITE = "https://hansliery89.github.io/hansliery-web/"
REVISION = "Noviembre 2026"
sys.path.insert(0, str(HERE))

from cursos_1 import COURSES as C1  # noqa: E402
from cursos_2 import COURSES as C2  # noqa: E402
from cursos_3 import COURSES as C3  # noqa: E402
from cursos_4 import COURSES as C4  # noqa: E402

COURSES = C1 + C2 + C3 + C4
COURSES.sort(key=lambda c: c["num"])


def shuffle_quiz(c):
    """Mezcla las opciones de cada pregunta (de forma reproducible) para que la
    respuesta correcta no caiga siempre en la misma letra."""
    for k, item in enumerate(c["quiz"]):
        seed = int(hashlib.sha256(f"{c['slug']}-{k}".encode()).hexdigest(), 16)
        rnd = random.Random(seed)
        order = list(range(len(item["options"])))
        rnd.shuffle(order)
        item["options"] = [item["options"][i] for i in order]
        item["answer"] = order.index(item["answer"])


for _c in COURSES:
    shuffle_quiz(_c)

esc = html.escape


def refs(text):
    """[[3]] -> superíndice enlazado a la fuente 3; [[1,4]] -> varias."""
    def rep(m):
        nums = [n.strip() for n in m.group(1).split(",")]
        links = ",".join(f'<a href="#fuente-{n}" aria-label="Fuente {n}">{n}</a>' for n in nums)
        return f'<sup class="ref">[{links}]</sup>'
    return re.sub(r"\[\[([\d,\s]+)\]\]", rep, text)


HEAD = """<!DOCTYPE html>
<html lang="es-DO">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="author" content="Hansliery Sánchez">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#FFFFFF">
  <meta name="color-scheme" content="dark">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'none'; object-src 'none'; base-uri 'self'; form-action 'none'">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="{ogtype}">
  <meta property="og:locale" content="es_DO">
  <meta property="og:site_name" content="HANSLIERY SÁNCHEZ · Compliance &amp; Risk Advisory">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{site}assets/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="../favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Sora:wght@500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="cursos.css">
  <script>document.documentElement.classList.add('js');</script>
  <script type="application/ld+json">{jsonld}</script>
</head>
<body>
  <a class="skip-link" href="#contenido">Saltar al contenido</a>
  <div class="progress" aria-hidden="true"></div>
  <header class="topbar">
    <div class="wrap topbar-inner">
      <a class="brand" href="../index.html" aria-label="HANSLIERY SÁNCHEZ — volver al sitio principal">
        <svg class="brand-mark" viewBox="0 0 48 48" aria-hidden="true">
          <defs><linearGradient id="gm" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2563EB"/><stop offset="1" stop-color="#38BDF8"/></linearGradient></defs>
          <path d="M24 3.5l17.8 10.25v20.5L24 44.5 6.2 34.25v-20.5L24 3.5z" fill="rgba(37,99,235,.08)" stroke="url(#gm)" stroke-width="2"/>
          <path d="M17 18.5v11M17 24h8M25 18.5v11" stroke="#0A192F" stroke-width="2.2" stroke-linecap="round"/>
          <path d="M31.5 19.5c-1-1-2.2-1.2-3.2-.7-1.4.7-1.2 2.6.4 3.2l1.4.5c1.7.6 1.9 2.6.4 3.4-1.1.6-2.5.3-3.5-.7" fill="none" stroke="#D4AF37" stroke-width="1.8" stroke-linecap="round"/>
        </svg>
        <span class="brand-text"><span class="brand-name">HANSLIERY <b>SÁNCHEZ</b></span><span class="brand-tag">CAPACITACIONES PLAFT</span></span>
      </a>
      <nav class="topnav" aria-label="Navegación de cursos">
        <a href="../index.html">Inicio</a>
        <a href="index.html"{cat_current}>Catálogo</a>
        <a class="btn-mini" href="../index.html#contacto">Conversemos</a>
      </nav>
    </div>
  </header>
"""

FOOT = """
  <footer class="footer">
    <div class="wrap">
      <p class="disclaimer"><strong>Aviso.</strong> Contenido formativo elaborado por Hansliery Sánchez a partir de las fuentes citadas en cada curso. No sustituye la lectura de la normativa oficial, las instrucciones de su ente supervisor ni la asesoría jurídica especializada. Los casos son hipotéticos y cualquier parecido con hechos reales es coincidencia. Última revisión: {rev}.</p>
      <div class="footer-bottom">
        <span>© 2026 HANSLIERY SÁNCHEZ · Compliance &amp; Risk Advisory</span>
        <span>Estrategia. Prevención. Confianza.</span>
      </div>
    </div>
  </footer>
  <button class="to-top" type="button" aria-label="Volver arriba">↑</button>
  <script src="cursos.js"></script>
</body>
</html>
"""


def course_page(c, prev_c, next_c):
    n = len(c["modules"])
    q = len(c["quiz"])
    url = f"{SITE}cursos/{c['slug']}.html"
    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Course",
        "name": c["title"],
        "description": c["summary"],
        "inLanguage": "es",
        "url": url,
        "educationalLevel": c["level"],
        "provider": {"@type": "Person", "name": "Hansliery Sánchez", "url": SITE},
        "isAccessibleForFree": True,
        "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "online", "courseWorkload": f"PT{c['minutes']}M"},
    }, ensure_ascii=False)

    out = [HEAD.format(title=esc(f"{c['title']} | Curso gratuito · Hansliery Sánchez"),
                       desc=esc(c["summary"]), canonical=url, site=SITE, ogtype="article",
                       jsonld=jsonld, cat_current="")]
    out.append(f'<main id="contenido" data-course="{c["slug"]}">')
    # HERO
    out.append(f"""
  <section class="hero">
    <div class="wrap">
      <nav class="crumbs" aria-label="Ruta"><a href="../index.html">Inicio</a><span>/</span><a href="index.html">Capacitaciones</a><span>/</span><span aria-current="page">Curso {c['num']:02d}</span></nav>
      <p class="eyebrow"><span class="tag">{esc(c['tag'])}</span> Curso {c['num']:02d}</p>
      <h1>{esc(c['title'])}</h1>
      <p class="summary">{esc(c['summary'])}</p>
      {f'<a class="notice" href="#nota-codigo-penal"><b>Nota aclaratoria</b><span>{esc(c["notice"])}</span><em>Leer la nota →</em></a>' if c.get('notice') else ''}
      <ul class="meta">
        <li><b>Nivel</b>{esc(c['level'])}</li>
        <li><b>Duración</b>≈ {c['minutes']} min</li>
        <li><b>Módulos</b>{n}</li>
        <li><b>Evaluación</b>{q} preguntas</li>
      </ul>
      <div class="hero-actions">
        <a class="btn btn-primary" href="#modulo-1">Comenzar el curso <span aria-hidden="true">→</span></a>
        <a class="btn btn-ghost" href="#evaluacion">Ir a la evaluación</a>
      </div>
      <p class="best" data-best hidden></p>
    </div>
  </section>
""")
    # BODY
    toc = "".join(f'<li><a href="#modulo-{i+1}" data-toc><span>{i+1:02d}</span>{esc(m["title"])}</a></li>' for i, m in enumerate(c["modules"]))
    out.append(f"""
  <div class="wrap layout">
    <aside class="sidebar" aria-label="Contenido del curso">
      <div class="side-card">
        <div class="ring" aria-hidden="true"><svg viewBox="0 0 44 44"><circle cx="22" cy="22" r="19" class="ring-track"/><circle cx="22" cy="22" r="19" class="ring-val"/></svg><span data-pct>0%</span></div>
        <p class="side-label">Tu avance de lectura</p>
        <ol class="toc">{toc}
          <li><a href="#evaluacion" data-toc><span>✓</span>Evaluación</a></li>
          <li><a href="#fuentes" data-toc><span>§</span>Fuentes</a></li>
        </ol>
      </div>
    </aside>

    <article class="content">
      <section class="objectives" aria-labelledby="obj-title">
        <h2 id="obj-title">Al finalizar podrás</h2>
        <ul>{''.join(f'<li>{esc(o)}</li>' for o in c['objectives'])}</ul>
      </section>
""")
    for i, m in enumerate(c["modules"]):
        out.append(f"""
      <section class="module" id="modulo-{i+1}" data-section>
        <header class="module-head"><span class="module-n">{i+1:02d}</span><h2>{esc(m['title'])}</h2></header>
        <div class="prose">{refs(m['html'])}</div>
      </section>
""")
    # QUIZ
    qs = []
    for k, item in enumerate(c["quiz"]):
        opts = "".join(
            f'<label class="opt"><input type="radio" name="q{k}" value="{j}"><span class="opt-letter">{"ABCDE"[j]}</span><span class="opt-text">{esc(o)}</span></label>'
            for j, o in enumerate(item["options"]))
        qs.append(f"""
        <fieldset class="q" data-answer="{item['answer']}">
          <legend><span class="q-n">Pregunta {k+1} de {q}</span>{esc(item['q'])}</legend>
          <div class="opts">{opts}</div>
          <div class="feedback" role="status" aria-live="polite" hidden>
            <p class="fb-title"></p>
            <p class="fb-text">{refs(esc(item['explain']))}</p>
          </div>
        </fieldset>""")
    out.append(f"""
      <section class="quiz" id="evaluacion" data-section aria-labelledby="quiz-title">
        <header class="module-head"><span class="module-n">✓</span><h2 id="quiz-title">Evaluación del aprendizaje</h2></header>
        <p class="quiz-intro">Responde cada pregunta: verás de inmediato si acertaste y por qué. Con 80&nbsp;% o más apruebas el curso. Puedes repetirla cuantas veces quieras.</p>
        <div class="quiz-bar" aria-hidden="true"><i></i></div>
        <form class="quiz-form" novalidate>{''.join(qs)}
        </form>
        <div class="result" role="status" aria-live="polite" hidden>
          <div class="result-score"><svg viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="52" class="rs-track"/><circle cx="60" cy="60" r="52" class="rs-val"/></svg><strong data-score>0%</strong></div>
          <div>
            <h3 class="result-title"></h3>
            <p class="result-text"></p>
            <div class="result-actions">
              <button type="button" class="btn btn-ghost" data-retry>Repetir evaluación</button>
              {f'<a class="btn btn-primary" href="{next_c["slug"]}.html">Siguiente curso <span aria-hidden="true">→</span></a>' if next_c else '<a class="btn btn-primary" href="index.html">Volver al catálogo</a>'}
            </div>
          </div>
        </div>
      </section>
""")
    # SOURCES
    src = "".join(
        f'<li id="fuente-{i+1}">{esc(s["text"])}' + (f' <a href="{esc(s["url"])}" target="_blank" rel="noopener noreferrer">Ver fuente</a>' if s.get("url") else "") + "</li>"
        for i, s in enumerate(c["sources"]))
    out.append(f"""
      <section class="sources" id="fuentes" data-section aria-labelledby="src-title">
        <header class="module-head"><span class="module-n">§</span><h2 id="src-title">Fuentes consultadas</h2></header>
        <p class="src-intro">Todo el contenido de este curso se sustenta en las siguientes fuentes oficiales y de referencia. Las cifras y artículos citados pueden actualizarse; verifique siempre la versión vigente.</p>
        <ol class="src-list">{src}</ol>
      </section>

      <nav class="pager" aria-label="Otros cursos">
        {f'<a class="pager-prev" href="{prev_c["slug"]}.html"><small>← Curso anterior</small>{esc(prev_c["title"])}</a>' if prev_c else '<span></span>'}
        {f'<a class="pager-next" href="{next_c["slug"]}.html"><small>Curso siguiente →</small>{esc(next_c["title"])}</a>' if next_c else '<a class="pager-next" href="index.html"><small>Has llegado al final →</small>Ver el catálogo completo</a>'}
      </nav>
    </article>
  </div>
</main>""")
    out.append(FOOT.format(rev=REVISION))
    return "".join(out)


def catalog_page():
    url = f"{SITE}cursos/"
    cards = []
    for c in COURSES:
        cards.append(f"""
      <li class="cat-card{' cat-featured' if c.get('featured') else ''}" data-course-card="{c['slug']}">
        <div class="cat-top"><span class="cat-n">{c['num']:02d}</span><span class="tag">{esc(c['tag'])}</span></div>
        <h2><a href="{c['slug']}.html">{esc(c['title'])}</a></h2>
        <p>{esc(c['summary'])}</p>
        <ul class="cat-meta"><li>{esc(c['level'])}</li><li>≈ {c['minutes']} min</li><li>{len(c['modules'])} módulos</li><li>{len(c['quiz'])} preguntas</li></ul>
        <span class="cat-status" data-status hidden></span>
      </li>""")
    jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "ItemList", "name": "Capacitaciones PLAFT",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}cursos/{c['slug']}.html", "name": c["title"]} for i, c in enumerate(COURSES)],
    }, ensure_ascii=False)
    return (HEAD.format(title="Capacitaciones PLAFT gratuitas | HANSLIERY SÁNCHEZ",
                        desc="Cursos gratuitos de prevención de lavado de activos, Ley 155-17, debida diligencia, reportería ROS/RAS/RTE y más, con evaluaciones y fuentes oficiales.",
                        canonical=url, site=SITE, ogtype="website", jsonld=jsonld, cat_current=' aria-current="page"')
            + f"""<main id="contenido">
  <section class="hero hero-cat">
    <div class="wrap">
      <nav class="crumbs" aria-label="Ruta"><a href="../index.html">Inicio</a><span>/</span><span aria-current="page">Capacitaciones</span></nav>
      <p class="eyebrow"><span class="tag">Catálogo</span> {len(COURSES)} cursos</p>
      <h1>Conocimiento que se transforma en <span class="grad-gold">criterio</span>.</h1>
      <p class="summary">Cursos breves y gratuitos sobre prevención de lavado de activos y cumplimiento, con evaluación interactiva y fuentes oficiales al final de cada uno. Tu avance se guarda en este navegador.</p>
    </div>
  </section>
  <div class="wrap">
    <ol class="catalog">{''.join(cards)}
    </ol>
  </div>
</main>""" + FOOT.format(rev=REVISION))


def main():
    slugs = [c["slug"] for c in COURSES]
    assert len(slugs) == len(set(slugs)), "slugs duplicados"
    for c in COURSES:
        for item in c["quiz"]:
            assert 0 <= item["answer"] < len(item["options"]), (c["slug"], item["q"])
        used = {int(x) for m in c["modules"] for grp in re.findall(r"\[\[([\d,\s]+)\]\]", m["html"]) for x in grp.split(",")}
        used |= {int(x) for it in c["quiz"] for grp in re.findall(r"\[\[([\d,\s]+)\]\]", it["explain"]) for x in grp.split(",")}
        assert max(used, default=0) <= len(c["sources"]), (c["slug"], "referencia a fuente inexistente", max(used))
    for i, c in enumerate(COURSES):
        prev_c = COURSES[i - 1] if i > 0 else None
        next_c = COURSES[i + 1] if i + 1 < len(COURSES) else None
        (OUT / f"{c['slug']}.html").write_text(course_page(c, prev_c, next_c), encoding="utf-8")
    (OUT / "index.html").write_text(catalog_page(), encoding="utf-8")
    # Lista para la portada (enlaces) y el sitemap
    (HERE / "indice.json").write_text(json.dumps([{"num": c["num"], "slug": c["slug"], "title": c["title"], "tag": c["tag"], "card": c["card"]} for c in COURSES], ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"OK: {len(COURSES)} cursos generados en {OUT}")


if __name__ == "__main__":
    main()
