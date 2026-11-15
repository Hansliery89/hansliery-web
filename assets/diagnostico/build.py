"""Genera diagnostico-riesgos.html (Evaluador preliminar de riesgos LA/FT).
Uso: python3 assets/diagnostico/build.py  (desde la raíz del repositorio)"""
import os, re, json
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = "https://hansliery89.github.io/hansliery-web/"
ref = open(os.path.join(ROOT, "legal", "aviso-legal.html"), encoding="utf-8").read()
head = ref[:ref.index('<main id="contenido">')]
TITLE = "Diagnóstico preliminar de riesgos LA/FT · HANSLIERY SÁNCHEZ"
DESC = "Evaluación orientativa y gratuita de la exposición de su organización al riesgo de lavado de activos y financiamiento del terrorismo, con resultados descargables en PDF."
head = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", head)
head = re.sub(r'(<meta name="description" content=")[^"]*', r"\g<1>" + DESC, head)
head = re.sub(r'(<meta property="og:title" content=")[^"]*', r"\g<1>" + TITLE, head)
head = re.sub(r'(<meta property="og:description" content=")[^"]*', r"\g<1>" + DESC, head)
head = head.replace(SITE + "legal/aviso-legal.html", SITE + "diagnostico-riesgos.html")
head = head.replace('href="../', 'href="').replace('src="../', 'src="')
head = re.sub(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "WebApplication", "name": "Diagnóstico preliminar de riesgos LA/FT", "url": SITE + "diagnostico-riesgos.html", "applicationCategory": "BusinessApplication", "operatingSystem": "Web", "inLanguage": "es-DO", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@type": "Person", "name": "Hansliery Sánchez"}}, ensure_ascii=False) + "</script>", head, flags=re.S)
head = head.replace('<div class="progress" aria-hidden="true"></div>\n', '')
head = head.replace('</head>', '  <link rel="stylesheet" href="assets/diagnostico/diagnostico.css">\n</head>')
# nav: Inicio, Cursos, Conversemos -> keep, add "Volver al portal" discreet link in hero
body = open(os.path.join(os.path.dirname(__file__), "body.html"), encoding="utf-8").read()
foot = """
  <footer class="footer">
    <div class="wrap">
      <nav class="legal-links" aria-label="Información legal"><a href="legal/terminos-de-uso.html">Términos de uso</a> · <a href="legal/politica-de-privacidad.html">Política de privacidad</a> · <a href="legal/cookies-y-almacenamiento.html">Cookies y almacenamiento</a> · <a href="legal/aviso-legal.html">Aviso legal</a> · <a href="legal/accesibilidad.html">Accesibilidad</a></nav>
      <div class="footer-bottom">
        <span>© 2026 HANSLIERY SÁNCHEZ · Compliance &amp; Risk Advisory</span>
        <span>Estrategia. Prevención. Confianza.</span>
      </div>
    </div>
  </footer>
  <script src="assets/diagnostico/diagnostico.js"></script>
</body>
</html>
"""
open(os.path.join(ROOT, "diagnostico-riesgos.html"), "w", encoding="utf-8").write(head + body + foot)
print("OK diagnostico-riesgos.html")
