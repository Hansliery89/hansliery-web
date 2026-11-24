"""Curso 09 · Señales de alerta y análisis de casos."""
from fuentes import *  # noqa: F401,F403
from capas import ess, deep

# 1 UAF_ROS · 2 UAF_SEG · 3 UAF_COOP · 4 UAF_CAMB · 5 UAF_VAL · 6 UAF_DGII · 7 LEY · 8 GAFI40 · 9 SIS_NORMA · 10 DGII_N01 · 11 UAF_CAS
COURSE = {
"num": 9, "slug": "senales-de-alerta-y-analisis-de-casos", "tag": "Tipologías", "level": "Básico → Profesional", "minutes": 50,
"title": "Señales de alerta y análisis de casos",
"card": "De la alerta a la decisión: un método para analizar y documentar.",
"summary": "Aprende a reconocer señales de alerta de la normativa y de las subguías de la UAF, a convertirlas en decisiones fundamentadas mediante un método de análisis en cinco pasos y a documentar el resultado, incluida la decisión de no reportar, con casos resueltos de varios sectores.",
"objectives": [
  "Explicar qué es una señal de alerta y por qué no equivale a una sospecha.",
  "Reconocer las señales de alerta que recogen la ley, las normas sectoriales y las subguías de la UAF.",
  "Clasificar señales de alerta por categoría.",
  "Aplicar un método de análisis en cinco pasos y combinar señales.",
  "Resolver casos y documentar la decisión, incluida la de no reportar.",
],
"sources": [UAF_ROS, UAF_SEG, UAF_COOP, UAF_CAMB, UAF_VAL, UAF_DGII, LEY, GAFI40, SIS_NORMA, DGII_N01, UAF_CAS],
"modules": [
# 1 ------------------------------------------------------------------------------------------
{"title": "Alerta no es sospecha", "html": ess(
"Una señal de alerta es algo raro que llama la atención: un depósito grande de quien gana poco, prisa sin motivo, papeles que no cuadran. No prueba nada; es una invitación a mirar mejor antes de decidir.") + """
<p>Una <strong>señal de alerta</strong> es un comportamiento, situación o característica atípica que podría indicar que se está encubriendo una operación ilícita. Es un aviso para mirar con más atención, no una conclusión.[[1,2]]</p>
<p>La UAF insiste en que, ante una señal de alerta, el sujeto obligado debe hacer un <strong>análisis previo</strong> para validar si corresponde reportar. Lo inusual, por sí solo, puede no bastar: necesita complementarse con otros motivos de sospecha.[[1]]</p>
<p>La ley ofrece la referencia: una operación sospechosa es la compleja, insólita o significativa, o el patrón no habitual, sin fundamento económico o legal evidente, o que genera sospecha de vinculación con el lavado, un delito precedente o el financiamiento del terrorismo (art. 2, num. 16).[[7]]</p>
<div class="callout key"><b>Idea clave</b>Una alerta bien analizada termina en una de tres decisiones: hay explicación razonable (se archiva), hay dudas (se monitorea o se pide más información) o hay sospecha (se reporta).</div>
""" + deep("""
<p><strong>Inusual frente a sospechoso.</strong> Lo inusual se define por comparación con el perfil del cliente y de sus pares; lo sospechoso exige, además, que no haya una explicación razonable o que existan indicios de vínculo con una actividad ilícita. La Norma 01-2018 pide prestar especial atención a las operaciones complejas, insólitas y significativas que exceden los patrones habituales del cliente.[[10]]</p>
<p><strong>Listas no limitativas.</strong> Tanto la DGII como la Superintendencia de Seguros advierten que sus señales son explicativas y no limitativas; la DGII pide actuar con criterio en cada situación conforme al apetito y tolerancia de riesgo, y la de seguros, mantenerse actualizado en tendencias y tipologías.[[9,10]]</p>
""")},
# 2 ------------------------------------------------------------------------------------------
{"title": "Señales en la normativa", "html": ess(
"Las normas de los supervisores traen listas de señales. Se repiten ideas: operaciones que no encajan con lo que el cliente hace, negarse a dar información, fraccionar para no llegar al umbral, despreocupación por los costos y países de alto riesgo.") + """
<div class="grid-2">
<div class="mini"><h4>Seguros (Anexo I de la norma)</h4><p>Montos, frecuencia o naturaleza sin relación con la actividad del cliente; montos inusualmente elevados o modalidades no habituales; operaciones que parecen fraccionadas; negativa a dar datos o información alterada; indicios de origen o destino ilegal sin explicación razonable; inusual despreocupación por riesgos o costos; jurisdicciones de alto riesgo o no cooperantes; un mismo domicilio para varias personas jurídicas o los mismos apoderados en diferentes empresas sin razón económica.[[9]]</p></div>
<div class="mini"><h4>DGII (Norma 01-2018, art. 38)</h4><p>Transacciones sin relación con el perfil económico; intento de evadir los requisitos de información; información insuficiente o falsa; operaciones a nombre de terceros que las desconocen; participación de múltiples organizaciones sin fines de lucro, cooperativas o fundaciones con recursos cuantiosos; clientes con informaciones públicas negativas vinculadas al lavado o sus delitos precedentes.[[10]]</p></div>
</div>
<p class="note-small">Síntesis de las listas oficiales; consulta el texto completo en cada norma.</p>
""" + deep("""
<p><strong>Subguías sectoriales de la UAF.</strong> Además de las normas, la UAF publicó subguías de calidad de los ROS para seguros, cooperativas, agentes de cambio y remesadoras, mercado de valores, casinos y sujetos obligados supervisados por la DGII. Cada una recoge señales propias del sector y errores frecuentes de reporte; el curso 8 incluye casos por sector construidos a partir de ellas.[[2,3,4,5,6,11]]</p>
""")},
# 3 ------------------------------------------------------------------------------------------
{"title": "Categorías de señales", "html": ess(
"Para recordar las señales es útil agruparlas en seis familias: identidad, origen y destino del dinero, comportamiento, patrón de operaciones, terceros y geografía.") + """
<p>Las subguías sectoriales de la UAF comparten señales que se repiten en todos los sectores. Agruparlas ayuda a recordarlas:[[2,3,4,5,6]]</p>
<div class="grid-2">
<div class="mini"><h4>Identidad y documentos</h4><p>Documentos en mal estado o con apariencia alterada; datos personales que cambian entre una operación y otra; negativa a identificar al verdadero beneficiario.</p></div>
<div class="mini"><h4>Origen y destino de fondos</h4><p>Se menciona un origen pero no se documenta; el soporte entregado corresponde a otra fuente o a otro monto; se evita explicar el destino.</p></div>
<div class="mini"><h4>Comportamiento</h4><p>Prisa inusual; desinterés por costos, penalidades o rentabilidad; nerviosismo o confusión sobre la propia operación.</p></div>
<div class="mini"><h4>Patrón transaccional</h4><p>Movimientos fuera del perfil; fraccionamiento para no alcanzar umbrales; cambios bruscos de volumen sin justificación.</p></div>
<div class="mini"><h4>Terceros</h4><p>Pagos o beneficios a personas sin relación aparente; muchos remitentes hacia un mismo receptor; bienes a nombre de familiares o amigos.</p></div>
<div class="mini"><h4>Geografía</h4><p>Jurisdicciones de alto riesgo o no cooperantes; operaciones en zonas que no se corresponden con la actividad declarada.</p></div>
</div>
""" + deep("""
<p><strong>Señales que se refuerzan.</strong> Una señal aislada suele tener explicación; varias de distintas familias, juntas, rara vez. Un depósito alto (patrón) puede ser una venta; pero un depósito alto de terceros sin relación (terceros), con soporte que no coincide (origen) y prisa por retirarlo (comportamiento) apunta a otra cosa.</p>
<p><strong>Jurisdicciones.</strong> Las operaciones con jurisdicciones definidas por el GAFI son factor de alto riesgo por ley (art. 46) y figuran entre las señales de la norma de seguros.[[7,9]] Revisa periódicamente las listas públicas del GAFI, que cambian.[[8]]</p>
""")},
# 4 ------------------------------------------------------------------------------------------
{"title": "Un método de análisis en cinco pasos", "html": ess(
"Para analizar una alerta: conoce al cliente, compara la operación con lo que suele hacer, pide una explicación, pregúntate con qué delito podría relacionarse y, al final, decide y escríbelo.") + """
<ol class="steps">
<li><strong>Contexto:</strong> ¿quién es el cliente, qué declaró, qué productos tiene, cuál es su calificación de riesgo?</li>
<li><strong>Comparación:</strong> ¿la operación encaja con su perfil y con el de clientes similares?</li>
<li><strong>Explicación:</strong> ¿existe una razón económica o legal razonable? Pídela y documéntala, cuidando no revelar que se examina la operación.</li>
<li><strong>Vínculo:</strong> si no hay explicación, ¿con qué posible delito precedente o con qué tipología podría relacionarse?</li>
<li><strong>Decisión y registro:</strong> archivar, monitorear o reportar, dejando por escrito los hechos, las fuentes consultadas y el razonamiento.</li>
</ol>
<p>Este método es coherente con lo que la UAF espera encontrar en un buen ROS: personas, productos, razonabilidad de los hechos, origen y destino de los fondos y relación con el delito.[[1]]</p>
""" + deep("""
<p><strong>El reloj corre.</strong> El ROS debe remitirse dentro de 5 días hábiles de realizada o intentada la operación (art. 55).[[7]] Diseña el flujo de análisis para que las alertas se revisen con prioridad según su riesgo y no se acumulen.</p>
<p><strong>Monitoreo con parámetros.</strong> La norma de seguros pide parámetros de alertas, manuales o automatizados, según la organización, estructura y complejidad, para analizar si las operaciones corresponden al perfil del cliente.[[9]] El curso 12 trata cómo automatizarlo.</p>
""")},
# 5 ------------------------------------------------------------------------------------------
{"title": "Casos para practicar", "html": ess(
"Tres casos cortos: en dos hay que reportar y en uno no. Fíjate en qué cambia la decisión: casi siempre, la existencia o no de una explicación con respaldo.") + """
<div class="case"><b>Caso 1 · Joven con alto movimiento</b>
<p>Un estudiante de 22 años, sin empleo declarado, recibe en un mes más de cuarenta transferencias de distintas personas por montos similares y las retira en efectivo el mismo día. Ante la consulta, responde que «vende por internet», pero no presenta facturas ni publicaciones.</p>
<p class="verdict yes"><b>Análisis:</b> fuera de perfil, sin soporte, con dispersión de remitentes y retiro inmediato. Posible uso de su cuenta como «mula». Corresponde ROS.</p></div>
<div class="case"><b>Caso 2 · Comerciante en temporada</b>
<p>Una tienda de juguetes triplica sus depósitos en efectivo en diciembre. Sus estados de los años anteriores muestran el mismo comportamiento estacional y presenta reportes de ventas.</p>
<p class="verdict no"><b>Análisis:</b> inusual frente al resto del año, pero con explicación documentada y coherente con su historia. Se archiva con nota y se mantiene el monitoreo.</p></div>
<div class="case"><b>Caso 3 · Pago anticipado sin explicación</b>
<p>Un cliente con ingresos medios cancela en efectivo un préstamo de vehículo a los tres meses de otorgado. Al pedirle el origen, dice que «fue un regalo» y no aporta más datos.</p>
<p class="verdict yes"><b>Análisis:</b> la cancelación anticipada sin fuente de ingresos verificable es una señal recogida por la UAF. Se insiste en el soporte; si no se aclara, procede ROS.[[3]]</p></div>
""" + deep("""
<p><strong>Para discutir.</strong> En el caso 1, ¿cambiaría la decisión si el estudiante mostrara una tienda en línea con publicaciones, pedidos y entregas verificables? En el caso 3, ¿qué documento aceptarías como soporte de un regalo (por ejemplo, la transferencia del donante desde su propia cuenta y la identificación de este)?</p>
""")},
# 6 ------------------------------------------------------------------------------------------
{"title": "Casos de seguros y sector no financiero", "html": ess(
"Dos casos más, de seguros y de una empresa con los mismos apoderados en varias sociedades. Aplica el método antes de leer la decisión.") + """
<div class="case"><b>Caso 4 · Póliza pagada por muchos</b>
<p>Una póliza de vida con componente de ahorro se paga durante seis meses con aportes de cinco personas distintas, sin relación declarada con el asegurado. El contratante muestra desinterés por la rentabilidad y pregunta reiteradamente por el rescate anticipado.</p>
<p class="verdict yes"><b>Análisis:</b> concurren pagos de terceros sin vínculo, despreocupación por costos y riesgos y foco en el rescate: señales del Anexo I de la norma de seguros y de la subguía del sector. Se pide explicación; si no se sustenta, ROS.[[2,9]]</p></div>
<div class="case"><b>Caso 5 · Los mismos apoderados</b>
<p>Tres sociedades recién constituidas, clientes de un agente inmobiliario, comparten domicilio y tienen a la misma persona como apoderada. Compran locales en efectivo por debajo del umbral, en fechas cercanas.</p>
<p class="verdict yes"><b>Análisis:</b> el mismo domicilio y apoderado en varias personas jurídicas sin razón económica es una señal expresa de la norma de seguros, y las compras escalonadas sugieren fraccionamiento. Corresponde identificar a los beneficiarios finales, pedir el origen de los fondos y, si no se aclara, ROS.[[6,9]]</p></div>
""" + deep("""
<p><strong>Efectivo y límites legales.</strong> En el caso 5, recuerda también los límites del art. 64 para pagos en efectivo de inmuebles, que el CONCLAFIT ha actualizado.[[7]] Una operación que intenta esquivar esos límites mediante varias compras puede constituir, además, una infracción administrativa.</p>
""")},
# 7 ------------------------------------------------------------------------------------------
{"title": "Documentar también lo que no se reporta", "html": ess(
"Si una alerta se cierra sin explicación escrita, parece que nadie la revisó. Anotar qué se revisó, qué se pidió y por qué se decidió protege a la entidad y al analista.") + """
<p>Una alerta archivada sin explicación es una debilidad ante cualquier revisión. Documentar el análisis protege a la entidad y al analista, y alimenta la calibración de las alertas.</p>
<ul>
<li>Qué disparó la alerta y cuándo.</li>
<li>Qué información se revisó y qué se pidió al cliente.</li>
<li>Cuál fue la explicación y qué la sustenta.</li>
<li>Qué se decidió, quién lo decidió y por qué.</li>
</ul>
<p>Los resultados de los análisis forman parte de los registros que deben conservarse al menos 10 años (art. 43).[[7]]</p>
<div class="callout warn"><b>Reserva</b>Todo este proceso es confidencial: no se puede revelar al cliente ni a terceros que su operación está siendo examinada (art. 63).[[7]]</div>
""" + deep("""
<p><strong>Aprender de las alertas.</strong> Mide cuántas alertas de cada regla terminan en ROS. Una regla que nunca produce hallazgos quizá deba recalibrarse; una que produce muchos ROS quizá merezca un umbral más bajo. Esa revisión periódica es parte del monitoreo que exige la gestión de riesgos.[[9]]</p>
""")},
],
"glossary": [
("Señal de alerta", "Comportamiento o situación atípica que amerita un análisis más profundo [[1]]."),
("Análisis previo", "Revisión que se hace antes de decidir si reportar: perfil, explicación, soportes [[1]]."),
("Operación inusual", "La que se aparta del perfil del cliente o de sus pares; puede tener explicación."),
("Fraccionamiento", "División de operaciones para evitar umbrales de detección o reporte [[9]]."),
("Mula de dinero", "Persona que presta su cuenta para recibir y mover fondos de terceros."),
("Jurisdicción no cooperante", "País o territorio identificado por el GAFI como de alto riesgo o con deficiencias [[8,9]]."),
("Archivo justificado", "Cierre documentado de una alerta con explicación razonable y soportes."),
("Tipología", "Forma o patrón conocido de lavado de activos o de financiamiento del terrorismo."),
],
"quiz": [
{"q": "¿Qué es una señal de alerta?", "options": ["Una prueba de que el cliente cometió un delito", "Un comportamiento o situación atípica que amerita un análisis más profundo", "Una orden de la UAF", "Un tipo de reporte"], "answer": 1, "explain": "La señal de alerta activa el análisis previo; no es una conclusión [[1]]."},
{"q": "Según la UAF, la inusualidad de una transacción:", "options": ["Siempre basta para reportar", "Por sí sola puede no bastar y necesita complementarse con otros motivos de sospecha", "Nunca es relevante", "Solo importa en efectivo"], "answer": 1, "explain": "La guía de calidad señala que la inusualidad, aislada, puede no ser suficiente [[1]]."},
{"q": "¿Cuál de estas es una señal del Anexo I de la norma de seguros?", "options": ["Pagar la prima a tiempo", "Inusual despreocupación por los riesgos o costos de las transacciones", "Tener una sola póliza", "Vivir en Santo Domingo"], "answer": 1, "explain": "El Anexo I incluye la inusual despreocupación respecto de riesgos o costos [[9]]."},
{"q": "Según la Norma 01-2018 de la DGII, ¿cuál puede considerarse operación sospechosa?", "options": ["Una compra coherente con el perfil", "Operaciones a nombre de terceros que desconocen de las mismas", "Pagar con transferencia", "Pedir factura"], "answer": 1, "explain": "Es uno de los supuestos del art. 38 de la Norma 01-2018 [[10]]."},
{"q": "En el Caso 2 (tienda de juguetes en diciembre), ¿por qué no se reporta?", "options": ["Porque el monto es bajo", "Porque existe una explicación documentada y coherente con su historia", "Porque es una empresa", "Porque diciembre está exento"], "answer": 1, "explain": "La estacionalidad documentada explica la variación; se archiva con nota y se mantiene el monitoreo."},
{"q": "¿En qué paso del método se busca una razón económica o legal para la operación?", "options": ["Contexto", "Explicación", "Geografía", "Archivo"], "answer": 1, "explain": "El tercer paso consiste en buscar y documentar una explicación razonable."},
{"q": "Un cliente entrega como soporte una factura por un monto distinto al de la operación. Esto es:", "options": ["Irrelevante", "Una señal de alerta recogida por la UAF en varios sectores", "Un motivo de RTE", "Prueba de lavado"], "answer": 1, "explain": "Las subguías incluyen como señal que el soporte corresponda a otra fuente o no coincida con el monto [[2,6]]."},
{"q": "Tres sociedades nuevas comparten domicilio y apoderado sin razón económica. Según la norma de seguros, esto es:", "options": ["Normal", "Una señal de alerta", "Un motivo de RTE", "Una prueba de delito"], "answer": 1, "explain": "El Anexo I incluye el mismo domicilio o los mismos apoderados en distintas personas jurídicas sin razón económica [[9]]."},
{"q": "¿Por qué conviene documentar las alertas que se archivan?", "options": ["No conviene", "Porque demuestra el análisis, protege a la entidad y ayuda a calibrar las alertas", "Para enviarlas al cliente", "Para cobrar una comisión"], "answer": 1, "explain": "La documentación sustenta la decisión y mejora el sistema de alertas; además, los análisis se conservan 10 años [[7]]."},
{"q": "Durante el análisis de una alerta, ¿qué no se debe hacer?", "options": ["Pedir soportes", "Revelar al cliente que su operación está siendo examinada por sospecha", "Revisar su perfil", "Consultar al área de negocio"], "answer": 1, "explain": "El art. 63 prohíbe revelar que se examina una operación [[7]]."},
{"q": "Un depósito alto aislado, con factura coherente, frente a un depósito alto de terceros sin vínculo, con soporte que no coincide y prisa por retirarlo:", "options": ["Son igual de sospechosos", "El segundo combina señales de varias familias y merece mucho más análisis", "Ninguno es relevante", "El primero es más grave"], "answer": 1, "explain": "La combinación de señales de distintas categorías aumenta la probabilidad de que no exista una explicación legítima."},
],
}
