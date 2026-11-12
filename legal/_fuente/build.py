"""Genera las páginas legales del sitio. Uso: python3 legal/_fuente/build.py"""
import os, json, re, html as H
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = "https://hansliery89.github.io/hansliery-web/"
REV = "12 de noviembre de 2026"
MAIL = "sanchezfiguereohansliery@gmail.com"
SRC = os.path.join(ROOT, "cursos", "_fuente", "build.py")
src = open(SRC, encoding="utf-8").read()
HEAD = re.search(r'HEAD = """(.*?)"""', src, re.S).group(1)
HEAD = (HEAD.replace('href="cursos.css"', 'href="../cursos/cursos.css"')
            .replace('aria-label="Navegación de cursos"', 'aria-label="Navegación"')
            .replace('<span class="brand-tag">CAPACITACIONES PLAFT</span>', '<span class="brand-tag">COMPLIANCE &amp; RISK ADVISORY</span>')
            .replace('<a href="index.html"{cat_current}>Catálogo</a>', '<a href="../cursos/index.html">Cursos</a>'))
PAGES = [("terminos-de-uso", "Términos de uso"), ("politica-de-privacidad", "Política de privacidad"),
         ("cookies-y-almacenamiento", "Cookies y almacenamiento"), ("aviso-legal", "Aviso legal"),
         ("accesibilidad", "Accesibilidad")]
def foot(cur):
    links = " · ".join(f'<a href="{s}.html"{" aria-current=\"page\"" if s == cur else ""}>{t}</a>' for s, t in PAGES)
    return f"""
  <footer class="footer">
    <div class="wrap">
      <nav class="legal-links" aria-label="Información legal">{links}</nav>
      <div class="footer-bottom">
        <span>© 2026 HANSLIERY SÁNCHEZ · Compliance &amp; Risk Advisory</span>
        <span>Estrategia. Prevención. Confianza.</span>
      </div>
    </div>
  </footer>
  <button class="to-top" type="button" aria-label="Volver arriba">↑</button>
  <script src="../cursos/cursos.js"></script>
</body>
</html>
"""
def page(slug, title, summary, sections):
    url = f"{SITE}legal/{slug}.html"
    jsonld = json.dumps({"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": url,
                         "inLanguage": "es-DO", "dateModified": "2026-11-12",
                         "isPartOf": {"@type": "WebSite", "name": "HANSLIERY SÁNCHEZ · Compliance & Risk Advisory", "url": SITE}}, ensure_ascii=False)
    h = HEAD.format(title=f"{title} · HANSLIERY SÁNCHEZ", desc=H.escape(summary), canonical=url, ogtype="website", site=SITE, jsonld=jsonld, cat_current="")
    toc = "".join(f'<li><a href="#s{i+1}"><span>{i+1:02d}</span>{H.escape(t)}</a></li>' for i, (t, _) in enumerate(sections))
    body = "".join(f'<section class="module legal-sec" id="s{i+1}"><div class="module-head"><span class="module-n">{i+1:02d}</span><h2>{t}</h2></div><div class="prose">{c}</div></section>' for i, (t, c) in enumerate(sections))
    others = "".join(f'<li><a href="{s}.html">{t}</a></li>' for s, t in PAGES if s != slug)
    return h + f"""
<main id="contenido">
  <section class="hero">
    <div class="wrap">
      <nav class="crumbs" aria-label="Ruta"><a href="../index.html">Inicio</a><span>/</span><span>Legal</span><span>/</span><span aria-current="page">{title}</span></nav>
      <p class="eyebrow"><span class="tag">Legal</span> Última actualización: {REV}</p>
      <h1>{title}</h1>
      <p class="summary">{summary}</p>
    </div>
  </section>
  <div class="wrap layout">
    <aside class="sidebar" aria-label="Contenido de la página">
      <div class="side-card">
        <p class="side-label">En esta página</p>
        <ol class="toc">{toc}</ol>
        <p class="side-label legal-others-label">Otros documentos</p>
        <ul class="legal-others">{others}</ul>
      </div>
    </aside>
    <article class="content legal-body">{body}</article>
  </div>
</main>
""" + foot(slug)

C = f'<a href="mailto:{MAIL}">{MAIL}</a>'
T = "HANSLIERY SÁNCHEZ · Compliance &amp; Risk Advisory"

DOCS = {}
DOCS["terminos-de-uso"] = ("Términos de uso",
 "Condiciones que rigen el acceso y el uso de este sitio web, de sus cursos gratuitos y de los documentos descargables.",
 [("Aceptación", f"<p>Este sitio web es operado por Hansliery Sánchez Figuereo, profesional independiente que ofrece servicios bajo la marca {T} (en adelante, «el titular»). Al acceder o utilizar el sitio, usted acepta estos términos. Si no está de acuerdo con ellos, le pedimos que no utilice el sitio.</p>"),
  ("Objeto del sitio", "<p>El sitio presenta la trayectoria profesional del titular, sus servicios de consultoría, gestión de riesgos, controles internos y capacitación en prevención de lavado de activos, financiamiento del terrorismo y de la proliferación de armas de destrucción masiva, así como contenidos formativos gratuitos y documentos modelo.</p>"),
  ("Uso permitido", "<p>Usted se compromete a utilizar el sitio de forma lícita, de buena fe y conforme a estos términos. En particular, no está permitido:</p><ul><li>Utilizar el sitio para fines ilícitos o que vulneren derechos de terceros.</li><li>Intentar acceder a áreas, sistemas o datos no destinados al público, o afectar el funcionamiento del sitio.</li><li>Extraer contenidos de forma masiva o automatizada con fines de redistribución.</li><li>Presentar los contenidos o documentos del sitio como propios, o retirar las menciones de autoría.</li></ul>"),
  ("Carácter informativo del contenido", "<p>Los textos, cursos, calculadoras, matrices y documentos del sitio tienen fines informativos y formativos. No constituyen asesoría jurídica, tributaria ni contable, ni sustituyen la lectura de la normativa oficial, las instrucciones del ente supervisor o el criterio del oficial de cumplimiento de cada entidad.</p><p>La información normativa se presenta según su estado a la fecha de la última revisión indicada en cada página y puede cambiar. Las herramientas interactivas, como la matriz de riesgo o la calculadora de factura, son ilustrativas y orientativas.</p>"),
  ("Cursos gratuitos", "<p>Los cursos son de acceso libre y gratuito. Las evaluaciones permiten al participante medir su aprendizaje y no constituyen una certificación oficial ni acreditan el cumplimiento de obligaciones de capacitación ante ningún supervisor. El avance se guarda únicamente en el navegador del participante, como se explica en la página de <a href=\"cookies-y-almacenamiento.html\">cookies y almacenamiento</a>.</p>"),
  ("Documentos modelo descargables", "<p>Los documentos en PDF de la sección de servicios son modelos de referencia con datos de ejemplo ficticios. Puede descargarlos y utilizarlos como guía para uso interno de su organización. No está permitido venderlos, redistribuirlos con fines comerciales ni publicarlos como propios. Cada entregable real se elabora a la medida de la organización que lo contrata.</p>"),
  ("Precios y contratación", "<p>Los precios publicados en la sección de costos son referenciales: sirven para planificar un presupuesto y no constituyen una oferta vinculante. La contratación de cualquier servicio se formaliza mediante una propuesta o contrato escrito que define el alcance, los entregables, los plazos, el precio y las condiciones de pago, y que prevalece sobre la información del sitio.</p><p>Los servicios se facturan conforme a la normativa tributaria dominicana vigente, incluido el Impuesto sobre las Transferencias de Bienes Industrializados y Servicios (ITBIS) y el sistema de facturación electrónica de la Dirección General de Impuestos Internos (DGII), cuando correspondan.</p>"),
  ("Compliance Guard Pro", "<p>Compliance Guard Pro es una plataforma en desarrollo. Las funciones descritas en el sitio expresan su diseño previsto y pueden cambiar. Su mención no implica una fecha de lanzamiento, una disponibilidad comercial ni un compromiso de precio.</p>"),
  ("Propiedad intelectual", "<p>Los textos, cursos, evaluaciones, diseños, gráficos, documentos modelo, la metodología de la matriz de riesgo y el código del sitio son obra del titular, salvo que se indique otra autoría, y están protegidos por la Ley núm. 65-00 sobre Derecho de Autor de la República Dominicana y los tratados internacionales aplicables. Las leyes, resoluciones y guías oficiales citadas pertenecen a sus autores institucionales y se enlazan o referencian como fuente.</p><p>Se permite citar fragmentos breves con mención de la fuente y enlace al sitio.</p>"),
  ("Enlaces a sitios de terceros", "<p>El sitio contiene enlaces a fuentes oficiales y a perfiles externos, como LinkedIn. El titular no controla esos sitios ni responde por su contenido, disponibilidad o políticas de privacidad.</p>"),
  ("Limitación de responsabilidad", "<p>El titular procura que la información sea exacta y esté actualizada, pero no garantiza la ausencia de errores ni la disponibilidad ininterrumpida del sitio. En la medida permitida por la ley, no responde por decisiones tomadas exclusivamente con base en la información del sitio ni por daños derivados de su uso. Los servicios profesionales fortalecen el programa de cumplimiento de la organización, pero no sustituyen su responsabilidad ni garantizan el resultado de una inspección o supervisión.</p>"),
  ("Modificaciones", "<p>Estos términos pueden actualizarse para reflejar cambios en el sitio o en la normativa. La versión vigente es la publicada en esta página, con su fecha de actualización.</p>"),
  ("Ley aplicable y jurisdicción", "<p>Estos términos se rigen por las leyes de la República Dominicana. Cualquier controversia se someterá a los tribunales competentes de Santo Domingo, Distrito Nacional, sin perjuicio de los derechos que la Ley núm. 358-05 General de Protección de los Derechos del Consumidor o del Usuario reconozca a quien tenga la condición de consumidor.</p>"),
  ("Contacto", f"<p>Para consultas sobre estos términos, escriba a {C}.</p>")])

DOCS["politica-de-privacidad"] = ("Política de privacidad",
 "Qué datos personales se tratan cuando usted visita el sitio o se comunica con el titular, para qué se usan y cómo ejercer sus derechos.",
 [("Responsable del tratamiento", f"<p>El responsable del tratamiento de los datos personales es Hansliery Sánchez Figuereo, quien ofrece servicios bajo la marca {T}, con domicilio en la República Dominicana. Correo de contacto: {C}.</p><p>Esta política se ajusta al artículo 44 de la Constitución de la República Dominicana y a la Ley núm. 172-13 sobre Protección de Datos de Carácter Personal.</p>"),
  ("Principio general: el sitio no recoge datos", "<p>Este sitio no tiene base de datos, no registra usuarios y no utiliza herramientas de analítica ni de publicidad. El formulario de contacto no envía ni almacena información en ningún servidor: al pulsar «Preparar correo», abre la aplicación de correo de su dispositivo con el mensaje redactado, y usted decide si lo envía.</p>"),
  ("Datos que se tratan y su origen", "<ul><li><strong>Datos que usted envía por correo electrónico</strong>, ya sea desde el formulario o escribiendo directamente: nombre, correo electrónico, organización (opcional), servicio de interés y la descripción de su necesidad, además de cualquier otro dato que decida incluir.</li><li><strong>Datos de facturación</strong>, si contrata un servicio: nombre o razón social, RNC o cédula, dirección y correo de recepción de comprobantes, necesarios para emitir la factura electrónica.</li><li><strong>Datos técnicos que procesan terceros</strong> al cargar el sitio, como su dirección IP y el tipo de navegador, según se detalla en la sección de proveedores.</li></ul><p>Le pedimos no incluir en sus mensajes información sensible ni datos de clientes de su organización que no sean necesarios para describir su consulta.</p>"),
  ("Finalidades", "<ul><li>Responder sus consultas y preparar propuestas de servicios.</li><li>Ejecutar los servicios contratados y comunicarse durante el proyecto.</li><li>Emitir facturas y cumplir obligaciones tributarias y contables.</li><li>Enviarle información sobre Compliance Guard Pro solo si usted la solicita expresamente.</li></ul><p>Los datos no se utilizan para decisiones automatizadas, perfiles comerciales ni publicidad, y no se venden ni se ceden a terceros.</p>"),
  ("Base del tratamiento", "<p>El tratamiento se basa en su consentimiento, que usted otorga al enviar voluntariamente su mensaje; en la necesidad de atender una relación precontractual o contractual que usted solicita; y en el cumplimiento de obligaciones legales, como las tributarias.</p>"),
  ("Proveedores y transferencias internacionales", "<p>Para funcionar, el sitio y la comunicación por correo se apoyan en proveedores que pueden tratar datos fuera de la República Dominicana, principalmente en los Estados Unidos:</p><ul><li><strong>GitHub Pages</strong> (GitHub, Inc.): aloja el sitio y puede registrar la dirección IP de los visitantes en sus registros técnicos y de seguridad.</li><li><strong>Google Fonts</strong> (Google LLC): sirve las tipografías del sitio; al descargarlas, su navegador comunica a Google su dirección IP y datos técnicos del navegador.</li><li><strong>Gmail</strong> (Google LLC): servicio de correo con el que se reciben y responden los mensajes.</li><li><strong>Proveedor de facturación electrónica</strong> y la DGII, para la emisión y validación de los comprobantes fiscales electrónicos.</li></ul><p>Cada proveedor trata los datos conforme a sus propias políticas de privacidad.</p>"),
  ("Conservación", "<p>Las consultas que no den lugar a una contratación se conservan hasta doce (12) meses después de la última comunicación y luego se eliminan, salvo que usted pida su eliminación antes. Los datos de clientes se conservan durante la relación profesional y, después, por los plazos que exijan las normas tributarias y comerciales.</p>"),
  ("Sus derechos", f"<p>Conforme a la Ley núm. 172-13, usted puede ejercer en cualquier momento sus derechos de:</p><ul><li><strong>Acceso</strong>: saber qué datos suyos se tratan.</li><li><strong>Rectificación</strong>: corregir datos inexactos o incompletos.</li><li><strong>Cancelación o supresión</strong>: pedir que se eliminen sus datos cuando ya no sean necesarios o no exista base para tratarlos.</li><li><strong>Oposición</strong>: oponerse a un tratamiento determinado.</li></ul><p>Para ejercerlos, escriba a {C} indicando el derecho que desea ejercer y un medio que permita verificar su identidad. La solicitud se atenderá dentro de los plazos que establece la ley. Si considera que su solicitud no fue atendida, puede acudir a las vías previstas en la legislación dominicana, incluida la acción de hábeas data.</p>"),
  ("Seguridad", "<p>El sitio se sirve mediante conexión cifrada (HTTPS), aplica una política de seguridad de contenidos que impide el envío de datos a servidores no autorizados y no almacena información de los visitantes. Ningún sistema es completamente infalible; si detecta un problema de seguridad, le agradecemos comunicarlo.</p>"),
  ("Menores de edad", "<p>Los servicios y contenidos están dirigidos a profesionales y organizaciones. El sitio no está destinado a menores de edad ni recoge conscientemente sus datos.</p>"),
  ("Cambios en esta política", "<p>Esta política puede actualizarse cuando cambien el sitio, los proveedores o la normativa. La versión vigente es la publicada en esta página, con su fecha de actualización.</p>")])

DOCS["cookies-y-almacenamiento"] = ("Cookies y almacenamiento",
 "El sitio no utiliza cookies de seguimiento. Aquí se explica el único almacenamiento local que usan los cursos y cómo borrarlo.",
 [("¿Usa cookies este sitio?", "<p>No. El sitio no instala cookies propias y no utiliza herramientas de analítica, publicidad, redes sociales integradas ni seguimiento entre sitios. Por eso no muestra un aviso de consentimiento de cookies.</p>"),
  ("Almacenamiento local de los cursos", "<p>Las páginas de cursos guardan su avance de lectura y los resultados de las evaluaciones en el almacenamiento local de su navegador (<code>localStorage</code>), bajo la clave <code>hs-cursos-v1</code>. Esta información:</p><ul><li>Se queda en su dispositivo y no se envía a ningún servidor.</li><li>No identifica a la persona ni se comparte con terceros.</li><li>Solo sirve para mostrarle su progreso cuando vuelve a un curso.</li></ul><p>Si su navegador bloquea este almacenamiento, los cursos funcionan igual, pero el avance no se recuerda entre visitas.</p>"),
  ("Servicios de terceros", "<p>Al cargar el sitio, su navegador descarga las tipografías desde Google Fonts y el sitio se sirve desde GitHub Pages. Estos servicios reciben datos técnicos como la dirección IP, como se explica en la <a href=\"politica-de-privacidad.html\">política de privacidad</a>. Al pulsar el enlace a LinkedIn, se aplican las políticas de ese sitio.</p>"),
  ("Cómo borrar los datos guardados", "<p>Puede eliminar el avance de los cursos en cualquier momento desde la configuración de su navegador, en la opción de borrar los datos de sitios o del historial para este dominio. También se elimina al usar la navegación privada, que no conserva datos al cerrar la ventana.</p>")])

DOCS["aviso-legal"] = ("Aviso legal",
 "Identificación del titular, naturaleza de los servicios y alcance de la información publicada en el sitio.",
 [("Titular del sitio", f"<ul><li><strong>Titular:</strong> Hansliery Sánchez Figuereo, profesional independiente.</li><li><strong>Marca:</strong> {T}.</li><li><strong>País:</strong> República Dominicana.</li><li><strong>Contacto:</strong> {C}.</li></ul>"),
  ("Naturaleza de los servicios", "<p>Los servicios de consultoría, gestión de riesgos, controles internos, capacitación y el desarrollo de Compliance Guard Pro se ofrecen a título personal e independiente. No constituyen representación de empleadores actuales o anteriores, de autoridades ni de organismos públicos, y las opiniones expresadas en el sitio son del titular.</p>"),
  ("Referencias institucionales", "<p>Las menciones a instituciones como la Unidad de Análisis Financiero, el Comité Nacional contra el Lavado de Activos y Financiamiento del Terrorismo (CONCLAFIT), la DGII, el Grupo de Acción Financiera Internacional (GAFI), el Basel Institute on Governance, la Organization of Risk Management Certification (ORMC) u otras se hacen con fines informativos, para describir la trayectoria profesional o citar fuentes. No implican patrocinio, aval ni relación comercial con esas instituciones.</p>"),
  ("Credenciales y experiencia", "<p>La formación, las certificaciones y la experiencia descritas en el perfil corresponden a la trayectoria del titular. Los indicadores de experiencia formativa, como la cantidad de participantes capacitados, describen actividad formativa y no constituyen resultados comerciales ni garantías de desempeño.</p>"),
  ("Alcance de la información", "<p>El contenido del sitio es general y no sustituye la asesoría profesional específica ni la evaluación independiente que corresponda a cada organización. Las referencias normativas se citan según su vigencia a la fecha de revisión de cada página.</p>"),
  ("Documentos relacionados", "<p>Consulte también los <a href=\"terminos-de-uso.html\">términos de uso</a>, la <a href=\"politica-de-privacidad.html\">política de privacidad</a> y la página de <a href=\"cookies-y-almacenamiento.html\">cookies y almacenamiento</a>.</p>")])

DOCS["accesibilidad"] = ("Accesibilidad",
 "Compromiso con un sitio usable por todas las personas, medidas aplicadas, limitaciones conocidas y cómo reportar barreras.",
 [("Compromiso", "<p>El objetivo es que el sitio pueda ser usado por el mayor número posible de personas, incluidas las que utilizan lectores de pantalla, navegación por teclado o ampliación. Como referencia se toman las Pautas de Accesibilidad para el Contenido Web (WCAG) 2.2 del W3C, nivel AA.</p>"),
  ("Medidas aplicadas", "<ul><li>Estructura semántica con encabezados ordenados y regiones identificadas.</li><li>Enlace «Saltar al contenido» y estados de foco visibles.</li><li>Menús, pestañas, selectores y evaluaciones operables con teclado.</li><li>Respeto de la preferencia del sistema de reducir el movimiento: las animaciones se detienen y el contenido se muestra completo.</li><li>Textos alternativos en imágenes y elementos gráficos decorativos ocultos a los lectores de pantalla.</li><li>Revisión del contraste de color de los textos sobre sus fondos.</li><li>Diseño adaptable a pantallas de escritorio, tableta y móvil, y ampliación del texto sin pérdida de contenido.</li></ul>"),
  ("Limitaciones conocidas", "<ul><li>Algunas leyendas decorativas de tamaño pequeño tienen un contraste ligeramente inferior al recomendado.</li><li>Los documentos modelo en PDF pueden no estar plenamente optimizados para lectores de pantalla. Si necesita un formato alternativo, puede solicitarlo.</li><li>Las visualizaciones ilustrativas, como el panel del inicio o la matriz de probabilidad e impacto, se describen en el texto que las acompaña y no aportan información adicional.</li></ul>"),
  ("Reportar una barrera", f"<p>Si encuentra una dificultad para acceder a algún contenido, escriba a {C} indicando la página y el problema. Se procurará corregirlo o facilitarle la información en un formato accesible.</p>")])

for slug, (title, summary, secs) in DOCS.items():
    open(os.path.join(ROOT, "legal", slug + ".html"), "w", encoding="utf-8").write(page(slug, title, summary, secs))
print("OK:", len(DOCS), "páginas legales")
