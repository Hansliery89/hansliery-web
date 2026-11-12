"""Cursos 09 a 13: señales de alerta, activos virtuales, fraude digital, automatización e IA."""
from fuentes import *  # noqa: F401,F403

COURSES = [
# ---------------------------------------------------------------------------------------------
{
"num": 9, "slug": "senales-de-alerta-y-analisis-de-casos", "tag": "Tipologías", "level": "Intermedio", "minutes": 30,
"title": "Señales de alerta y análisis de casos",
"card": "De la alerta a la decisión: un método para analizar y documentar.",
"summary": "Aprende a reconocer señales de alerta transversales y a convertirlas en decisiones fundamentadas mediante un método de análisis que se puede documentar y defender.",
"objectives": [
  "Explicar qué es una señal de alerta y por qué no equivale a una sospecha.",
  "Clasificar señales de alerta por categoría.",
  "Aplicar un método de análisis en cinco pasos.",
  "Documentar la decisión, incluida la de no reportar.",
],
"sources": [UAF_ROS, UAF_SEG, UAF_COOP, UAF_CAMB, UAF_VAL, UAF_DGII, LEY, GAFI40],
"modules": [
{"title": "Alerta no es sospecha", "html": """
<p>Una <strong>señal de alerta</strong> es un comportamiento, situación o característica atípica que podría indicar que se está encubriendo una operación ilícita. Es un aviso para mirar con más atención, no una conclusión.[[1,2]]</p>
<p>La UAF insiste en que, ante una señal de alerta, el sujeto obligado debe hacer un <strong>análisis previo</strong> para validar si corresponde reportar. Lo inusual, por sí solo, puede no bastar: necesita complementarse con otros motivos de sospecha.[[1]]</p>
<div class="callout key"><b>Idea clave</b>Una alerta bien analizada termina en una de tres decisiones: hay explicación razonable (se archiva), hay dudas (se monitorea o se pide más información) o hay sospecha (se reporta).</div>
"""},
{"title": "Categorías de señales", "html": """
<p>Las subguías sectoriales de la UAF comparten señales que se repiten en todos los sectores. Agruparlas ayuda a recordarlas:[[2,3,4,5,6]]</p>
<div class="grid-2">
<div class="mini"><h4>Identidad y documentos</h4><p>Documentos en mal estado o con apariencia alterada; datos personales que cambian entre una operación y otra; negativa a identificar al verdadero beneficiario.</p></div>
<div class="mini"><h4>Origen y destino de fondos</h4><p>Se menciona un origen pero no se documenta; el soporte entregado corresponde a otra fuente o a otro monto; se evita explicar el destino.</p></div>
<div class="mini"><h4>Comportamiento</h4><p>Prisa inusual; desinterés por costos, penalidades o rentabilidad; nerviosismo o confusión sobre la propia operación.</p></div>
<div class="mini"><h4>Patrón transaccional</h4><p>Movimientos fuera del perfil; fraccionamiento para no alcanzar umbrales; cambios bruscos de volumen sin justificación.</p></div>
<div class="mini"><h4>Terceros</h4><p>Pagos o beneficios a personas sin relación aparente; muchos remitentes hacia un mismo receptor; bienes a nombre de familiares o amigos.</p></div>
<div class="mini"><h4>Geografía</h4><p>Jurisdicciones de alto riesgo o no cooperantes; operaciones en zonas que no se corresponden con la actividad declarada.</p></div>
</div>
"""},
{"title": "Un método de análisis en cinco pasos", "html": """
<ol class="steps">
<li><strong>Contexto:</strong> ¿quién es el cliente, qué declaró, qué productos tiene, cuál es su calificación de riesgo?</li>
<li><strong>Comparación:</strong> ¿la operación encaja con su perfil y con el de clientes similares?</li>
<li><strong>Explicación:</strong> ¿existe una razón económica o legal razonable? Pídela y documéntala.</li>
<li><strong>Vínculo:</strong> si no hay explicación, ¿con qué posible delito precedente o con qué tipología podría relacionarse?</li>
<li><strong>Decisión y registro:</strong> archivar, monitorear o reportar, dejando por escrito los hechos, las fuentes consultadas y el razonamiento.</li>
</ol>
<p>Este método es coherente con lo que la UAF espera encontrar en un buen ROS: personas, productos, razonabilidad de los hechos, origen y destino de los fondos y relación con el delito.[[1]]</p>
"""},
{"title": "Casos para practicar", "html": """
<div class="case"><b>Caso 1 · Joven con alto movimiento</b>
<p>Un estudiante de 22 años, sin empleo declarado, recibe en un mes más de cuarenta transferencias de distintas personas por montos similares y las retira en efectivo el mismo día. Ante la consulta, responde que «vende por internet», pero no presenta facturas ni publicaciones.</p>
<p class="verdict yes"><b>Análisis:</b> fuera de perfil, sin soporte, con dispersión de remitentes y retiro inmediato. Posible uso de su cuenta como «mula». Corresponde ROS.</p></div>
<div class="case"><b>Caso 2 · Comerciante en temporada</b>
<p>Una tienda de juguetes triplica sus depósitos en efectivo en diciembre. Sus estados de los años anteriores muestran el mismo comportamiento estacional y presenta reportes de ventas.</p>
<p class="verdict no"><b>Análisis:</b> inusual frente al resto del año, pero con explicación documentada y coherente con su historia. Se archiva con nota y se mantiene el monitoreo.</p></div>
<div class="case"><b>Caso 3 · Pago anticipado sin explicación</b>
<p>Un cliente con ingresos medios cancela en efectivo un préstamo de vehículo a los tres meses de otorgado. Al pedirle el origen, dice que «fue un regalo» y no aporta más datos.</p>
<p class="verdict yes"><b>Análisis:</b> la cancelación anticipada sin fuente de ingresos verificable es una señal recogida por la UAF. Se insiste en el soporte; si no se aclara, procede ROS.[[3]]</p></div>
"""},
{"title": "Documentar también lo que no se reporta", "html": """
<p>Una alerta archivada sin explicación es una debilidad ante cualquier revisión. Documentar el análisis protege a la entidad y al analista, y alimenta la calibración de las alertas.</p>
<ul>
<li>Qué disparó la alerta y cuándo.</li>
<li>Qué información se revisó y qué se pidió al cliente.</li>
<li>Cuál fue la explicación y qué la sustenta.</li>
<li>Qué se decidió, quién lo decidió y por qué.</li>
</ul>
<div class="callout warn"><b>Reserva</b>Todo este proceso es confidencial: no se puede revelar al cliente ni a terceros que su operación está siendo examinada.[[7]]</div>
"""},
],
"quiz": [
{"q": "¿Qué es una señal de alerta?", "options": ["Una prueba de que el cliente cometió un delito", "Un comportamiento o situación atípica que amerita un análisis más profundo", "Una orden de la UAF", "Un tipo de reporte"], "answer": 1, "explain": "La señal de alerta es un aviso que activa el análisis previo; no es una conclusión [[1]]."},
{"q": "Según la UAF, la inusualidad de una transacción:", "options": ["Siempre basta para reportar", "Por sí sola puede no bastar y necesita complementarse con otros motivos de sospecha", "Nunca es relevante", "Solo importa en efectivo"], "answer": 1, "explain": "La guía de calidad señala que la inusualidad, aislada, puede no ser suficiente [[1]]."},
{"q": "En el Caso 2 (tienda de juguetes en diciembre), ¿por qué no se reporta?", "options": ["Porque el monto es bajo", "Porque existe una explicación documentada y coherente con su historia", "Porque es una empresa", "Porque diciembre está exento"], "answer": 1, "explain": "La estacionalidad documentada explica la variación; se archiva con nota y se mantiene el monitoreo."},
{"q": "¿Cuál es el paso del método en el que se busca una razón económica o legal para la operación?", "options": ["Contexto", "Explicación", "Geografía", "Archivo"], "answer": 1, "explain": "El tercer paso consiste en buscar y documentar una explicación razonable."},
{"q": "Un cliente entrega como soporte una factura por un monto distinto al de la operación. Esto es:", "options": ["Irrelevante", "Una señal de alerta recogida por la UAF en varios sectores", "Un motivo de RTE", "Prueba de lavado"], "answer": 1, "explain": "Las subguías incluyen como señal que el soporte corresponda a otra fuente o no coincida con el monto [[2,6]]."},
{"q": "¿Por qué conviene documentar las alertas que se archivan?", "options": ["No conviene", "Porque demuestra el análisis realizado, protege a la entidad y ayuda a calibrar las alertas", "Para enviarlas al cliente", "Para cobrar una comisión"], "answer": 1, "explain": "La documentación sustenta la decisión ante auditorías y supervisión y mejora el sistema de alertas."},
],
},
# ---------------------------------------------------------------------------------------------
{
"num": 10, "slug": "activos-virtuales-y-riesgos-emergentes", "tag": "Riesgos emergentes", "level": "Intermedio", "minutes": 30,
"title": "Activos virtuales y riesgos emergentes",
"card": "Criptoactivos, proveedores de servicios y señales de alerta.",
"summary": "Entiende qué son los activos virtuales, cuál es su situación en la República Dominicana, qué exigen los estándares del GAFI y qué señales de alerta deben vigilar los sujetos obligados.",
"objectives": [
  "Explicar qué es un activo virtual y qué es un proveedor de servicios de activos virtuales.",
  "Describir la posición oficial dominicana sobre las criptomonedas.",
  "Identificar los requisitos del GAFI para este sector.",
  "Reconocer señales de alerta y aplicar debida diligencia a clientes vinculados a criptoactivos.",
],
"sources": [GAFI40, GAFI_VA, GAFI_VA_RF, DGII_CRIPTO, UAF_VAL, LEY],
"modules": [
{"title": "Conceptos básicos", "html": """
<p>Para el GAFI, un <strong>activo virtual</strong> es una representación digital de valor que puede comercializarse o transferirse digitalmente y usarse para pagos o inversiones. No incluye las representaciones digitales de monedas de curso legal ni los valores ya cubiertos por otras Recomendaciones.[[1,2]]</p>
<ul>
<li><strong>Proveedor de servicios de activos virtuales (PSAV):</strong> quien, como negocio y por cuenta de otros, intercambia activos virtuales por dinero o por otros activos virtuales, los transfiere, los custodia o participa en servicios financieros relacionados con su emisión.[[1,2]]</li>
<li><strong>Billetera custodiada:</strong> un tercero controla las claves. <strong>Billetera no custodiada:</strong> el propio usuario controla sus claves, sin intermediario.</li>
<li><strong>Cadena de bloques:</strong> registro distribuido en el que quedan las transacciones; es seudónimo, no necesariamente anónimo.</li>
</ul>
"""},
{"title": "Situación en la República Dominicana", "html": """
<p>El Banco Central advirtió en 2017, en cumplimiento de una resolución de la Junta Monetaria, que los activos virtuales <strong>no son moneda de curso legal</strong>, no tienen fuerza liberatoria y no están respaldados ni autorizados como medio de pago. La DGII ha reiterado en sus consultas que no están regulados ni supervisados, aunque tampoco prohibidos.[[4]]</p>
<div class="callout warn"><b>Para el sujeto obligado</b>Que no haya una regulación específica no elimina el riesgo. Los clientes que obtienen ingresos de criptoactivos y los convierten a moneda de curso legal deben poder justificar el origen de esos fondos, igual que cualquier otro.[[4]] De hecho, la UAF incluye la participación en actividades como las criptomonedas entre las señales de alerta del mercado de valores.[[5]]</div>
<p>Este es un ámbito que cambia con rapidez. Verifica si existe normativa nueva antes de aplicar este contenido.</p>
"""},
{"title": "Lo que exige el GAFI", "html": """
<p>La <strong>Recomendación 15</strong> pide a los países identificar y evaluar los riesgos de las nuevas tecnologías y, en particular, que los PSAV estén regulados con fines antilavado, tengan licencia o registro y estén supervisados.[[1]]</p>
<p>Además, los PSAV deben aplicar las medidas preventivas generales y la llamada <strong>«regla de viaje»</strong>: obtener, conservar y transmitir información del originador y del beneficiario en las transferencias de activos virtuales, de forma análoga a las transferencias electrónicas (Recomendación 16).[[1,2]]</p>
"""},
{"title": "Señales de alerta", "html": """
<p>El GAFI publicó indicadores específicos para este sector. Entre ellos:[[3]]</p>
<ul>
<li>Fraccionar operaciones en montos pequeños o justo por debajo de los umbrales de reporte.</li>
<li>Transferir fondos inmediatamente a múltiples PSAV o a jurisdicciones sin regulación adecuada.</li>
<li>Usar servicios de mezcla o «tumblers» y monedas que refuerzan el anonimato.</li>
<li>Depositar activos virtuales y retirarlos de inmediato sin actividad intermedia, aceptando comisiones elevadas.</li>
<li>Perfiles de clientes que no son coherentes con el volumen operado (por ejemplo, adultos mayores o estudiantes con grandes movimientos).</li>
<li>Fondos provenientes de direcciones vinculadas a fraudes, ransomware o mercados ilícitos.</li>
</ul>
"""},
{"title": "Debida diligencia en la práctica", "html": """
<div class="case"><b>Caso</b>
<p>Un cliente de un banco empieza a recibir transferencias internacionales frecuentes desde una plataforma de intercambio de criptoactivos. Dice que son «ganancias de trading», pero su perfil es de empleado con ingresos bajos y nunca declaró esa actividad.</p>
<p class="verdict yes"><b>Qué hacer:</b> actualizar su debida diligencia; pedir estados de la plataforma, historial de compras y prueba del capital inicial invertido; recalcular su riesgo. Si no puede sustentar el origen o aparecen otras señales, evaluar un ROS.</p></div>
<ul>
<li>Pregunta por la actividad con criptoactivos desde la vinculación.</li>
<li>Pide evidencia que conecte el capital inicial con fuentes lícitas.</li>
<li>Valora el riesgo de las plataformas y jurisdicciones involucradas.</li>
<li>Recuerda que la reserva sobre cualquier análisis se mantiene (art. 63).[[6]]</li>
</ul>
"""},
],
"quiz": [
{"q": "Según el GAFI, ¿qué es un activo virtual?", "options": ["Cualquier depósito bancario digital", "Una representación digital de valor que puede comercializarse o transferirse digitalmente y usarse para pagos o inversiones", "Una moneda de curso legal electrónica", "Un bono del Estado"], "answer": 1, "explain": "Es la definición del glosario del GAFI; excluye las representaciones digitales de moneda de curso legal [[1,2]]."},
{"q": "¿Cuál es la posición del Banco Central sobre las criptomonedas?", "options": ["Son moneda de curso legal", "No son moneda de curso legal ni están respaldadas o autorizadas como medio de pago", "Están prohibidas con pena de prisión", "Son supervisadas por la UAF"], "answer": 1, "explain": "El aviso de 2017, reiterado por la DGII en sus consultas, señala que no tienen curso legal ni respaldo [[4]]."},
{"q": "¿Qué es la «regla de viaje»?", "options": ["Un límite para viajar con criptoactivos", "La obligación de obtener, conservar y transmitir información del originador y del beneficiario en las transferencias de activos virtuales", "Una tasa de cambio", "Un tipo de billetera"], "answer": 1, "explain": "Es la aplicación de la Recomendación 16 a las transferencias de activos virtuales [[1,2]]."},
{"q": "¿Cuál de estas es una señal de alerta del GAFI para activos virtuales?", "options": ["Mantener activos durante años", "Usar servicios de mezcla para ocultar el rastro de los fondos", "Comprar en una plataforma regulada con cuenta verificada", "Declarar las ganancias"], "answer": 1, "explain": "Los mezcladores y las monedas que refuerzan el anonimato figuran entre los indicadores del GAFI [[3]]."},
{"q": "Un cliente justifica sus depósitos como ganancias de criptoactivos, pero no aporta evidencia del capital inicial. ¿Qué corresponde?", "options": ["Aceptar la explicación verbal", "Solicitar soportes, actualizar la debida diligencia y evaluar un ROS si no se sustenta", "Cerrar la cuenta sin análisis", "Enviar un RTE"], "answer": 1, "explain": "El origen de los fondos debe justificarse; la falta de soporte, sumada al perfil, puede llevar a un ROS [[4]]."},
{"q": "Que los criptoactivos no estén regulados específicamente en el país significa que:", "options": ["No hay riesgo de lavado", "El sujeto obligado debe igualmente gestionar el riesgo y exigir justificación del origen de fondos", "Están prohibidos", "Solo el Banco Central debe actuar"], "answer": 1, "explain": "La falta de regulación específica no elimina el riesgo; el enfoque basado en riesgos sigue aplicando."},
],
},
# ---------------------------------------------------------------------------------------------
{
"num": 11, "slug": "fraude-digital-y-delitos-financieros-tecnologicos", "tag": "Riesgos emergentes", "level": "Intermedio", "minutes": 25,
"title": "Fraude digital y delitos financieros tecnológicos",
"card": "Ciberfraude, mulas de dinero y su vínculo con el lavado.",
"summary": "Conoce las modalidades más comunes de fraude habilitado por la tecnología, el marco penal dominicano aplicable, el papel de las «mulas» de dinero y cómo responder desde cumplimiento.",
"objectives": [
  "Describir las modalidades frecuentes de fraude digital.",
  "Ubicar el marco penal dominicano aplicable (Ley 53-07 y nuevo Código Penal).",
  "Reconocer a las «mulas» de dinero y sus señales.",
  "Coordinar la respuesta entre prevención de fraude y cumplimiento.",
],
"sources": [GAFI_CEF, LEY_5307, LEY_7425, ESTAFA_7425, UAF_ROS, LEY],
"modules": [
{"title": "Un delito global y veloz", "html": """
<p>El GAFI, INTERPOL y el Grupo Egmont describen el fraude habilitado por la tecnología como una amenaza transnacional en crecimiento: los delincuentes aprovechan la digitalización para operar a mayor escala y velocidad, y mueven los fondos rápidamente entre jurisdicciones.[[1]]</p>
<h3>Modalidades frecuentes</h3>
<ul>
<li><strong>Suplantación (phishing, smishing, vishing):</strong> correos, mensajes o llamadas que imitan a una entidad para obtener claves o datos.</li>
<li><strong>Compromiso de correo empresarial:</strong> se suplanta a un proveedor o ejecutivo para desviar pagos.</li>
<li><strong>Fraudes de inversión:</strong> promesas de rentabilidad alta y segura, a menudo con criptoactivos.</li>
<li><strong>Fraudes románticos o de confianza:</strong> relaciones construidas en línea para pedir dinero.</li>
<li><strong>Ventas falsas en redes sociales:</strong> se cobra por artículos que nunca se entregan.</li>
</ul>
"""},
{"title": "Marco penal dominicano", "html": """
<ul>
<li><strong>Ley 53-07 sobre Crímenes y Delitos de Alta Tecnología:</strong> tipifica, entre otros, la obtención ilícita de fondos (art. 14), la estafa cometida por medios electrónicos (art. 15) y el robo de identidad (art. 17).[[2]]</li>
<li><strong>Nuevo Código Penal (Ley 74-25):</strong> vigente desde el 3 de agosto de 2026, actualiza los delitos contra el patrimonio. Según los análisis publicados, la estafa pasa a sancionarse con tres a cinco años y la agravada con cinco a diez.[[3,4]]</li>
</ul>
<div class="callout key"><b>Conexión con el lavado</b>La Ley 155-17 considera infracción precedente toda infracción grave con pena no menor de tres años.[[6]] Con las nuevas penas, los fraudes que antes podían quedar fuera de ese umbral podrían ahora considerarse precedentes. Consulta el criterio vigente de la UAF.</div>
"""},
{"title": "Las «mulas» de dinero", "html": """
<p>Una <strong>mula</strong> es una persona que recibe en su cuenta fondos de origen ilícito y los transfiere o retira por cuenta de otros, a veces sin saber que participa en un delito. Son una pieza clave para sacar el dinero del fraude.[[1]]</p>
<p>Se recluta con ofertas de «trabajo desde casa», préstamos fáciles o relaciones en línea. Señales frecuentes:</p>
<ul>
<li>Cuentas nuevas o poco usadas que de pronto reciben muchas transferencias de desconocidos.</li>
<li>Retiro o reenvío casi inmediato de lo recibido.</li>
<li>Titulares jóvenes o sin ingresos que no pueden explicar los movimientos.</li>
<li>Varias cuentas que comparten dispositivo, dirección IP o datos de contacto.</li>
</ul>
"""},
{"title": "Respuesta desde cumplimiento", "html": """
<ol class="steps">
<li><strong>Coordinar fraude y cumplimiento:</strong> los indicadores de fraude alimentan el monitoreo antilavado y viceversa.[[1]]</li>
<li><strong>Actuar rápido:</strong> la velocidad del fraude exige procesos ágiles de bloqueo y escalamiento, según las políticas de la entidad.</li>
<li><strong>Orientar a las víctimas:</strong> la UAF recuerda los canales de denuncia de la Policía Nacional (incluida su plataforma en línea), la Procuraduría General de la República y la línea 311.[[5]]</li>
<li><strong>Reportar cuando corresponda:</strong> si el análisis apunta a un delito precedente o a una red que mueve fondos ilícitos, se remite el ROS dentro del plazo legal.[[5,6]]</li>
</ol>
<div class="case"><b>Caso</b><p>Varios clientes denuncian que pagaron artículos anunciados en redes sociales a la cuenta de la Sra. T. y nunca los recibieron. La cuenta recibió en un mes decenas de transferencias similares, retiradas en cajeros el mismo día.</p>
<p class="verdict yes"><b>Decisión:</b> escalar a fraude para las medidas inmediatas, orientar a los afectados a denunciar y analizar la remisión de un ROS por el patrón de captación y retiro de fondos.</p></div>
"""},
],
"quiz": [
{"q": "¿Qué caracteriza al fraude habilitado por la tecnología según el GAFI, INTERPOL y Egmont?", "options": ["Es local y lento", "Es transnacional, crece rápido y mueve los fondos con velocidad entre jurisdicciones", "Solo afecta a bancos grandes", "No tiene relación con el lavado"], "answer": 1, "explain": "El informe de 2023 lo describe como una amenaza transnacional en crecimiento ligada al lavado [[1]]."},
{"q": "¿Qué ley dominicana tipifica la estafa cometida por medios electrónicos?", "options": ["Ley 172-13", "Ley 53-07 sobre Crímenes y Delitos de Alta Tecnología", "Ley 183-02", "Ley 311-14"], "answer": 1, "explain": "El art. 15 de la Ley 53-07 sanciona la estafa realizada por medios electrónicos [[2]]."},
{"q": "¿Qué es una «mula» de dinero?", "options": ["Un sistema de pago", "Una persona que recibe y mueve fondos ilícitos por cuenta de otros", "Una billetera digital", "Un tipo de reporte"], "answer": 1, "explain": "Las mulas permiten sacar y dispersar el dinero del fraude [[1]]."},
{"q": "¿Cuál es una señal típica de una cuenta usada como mula?", "options": ["Pago puntual de la nómina", "Muchas transferencias de desconocidos retiradas o reenviadas casi de inmediato", "Ahorro mensual constante", "Uso de tarjeta en supermercados"], "answer": 1, "explain": "La recepción masiva y el retiro inmediato son indicadores frecuentes."},
{"q": "Con el nuevo Código Penal, ¿por qué podría cambiar el tratamiento de la estafa en materia de lavado?", "options": ["Porque se despenalizó", "Porque su pena pasaría a 3-5 años y alcanzaría el umbral de infracción precedente", "Porque ahora la investiga la UAF", "No cambia nada"], "answer": 1, "explain": "La Ley 155-17 considera precedente toda infracción grave con pena no menor de tres años [[3,4,6]]."},
{"q": "Una víctima de fraude acude a la entidad. ¿Qué orientación es correcta?", "options": ["Decirle que no hay nada que hacer", "Orientarla a denunciar ante la Policía Nacional, la Procuraduría o la línea 311, sin revelar análisis internos", "Mostrarle los ROS enviados", "Contactar al presunto estafador"], "answer": 1, "explain": "La UAF recuerda esos canales de denuncia; la reserva sobre los reportes se mantiene [[5,6]]."},
],
},
# ---------------------------------------------------------------------------------------------
{
"num": 12, "slug": "automatizacion-de-procesos-de-cumplimiento", "tag": "Tecnología", "level": "Intermedio", "minutes": 25,
"title": "Automatización de procesos de cumplimiento",
"card": "Qué automatizar, con qué herramientas y con qué controles.",
"summary": "Descubre qué procesos de cumplimiento conviene automatizar, qué herramientas accesibles existen y qué controles de gobierno, calidad de datos y confidencialidad deben acompañarlos.",
"objectives": [
  "Identificar procesos de cumplimiento con alto potencial de automatización.",
  "Distinguir lo que se puede automatizar de lo que exige juicio humano.",
  "Aplicar controles de calidad de datos, trazabilidad y confidencialidad.",
  "Construir una hoja de ruta de automatización con indicadores.",
],
"sources": [GAFI_TECH, LEY, LEY_17213, GAFI40, UAF_ROS],
"modules": [
{"title": "Por qué automatizar", "html": """
<p>Las obligaciones de cumplimiento son continuas: la ley exige monitorear permanentemente la relación con los clientes (art. 39) y conservar registros durante al menos diez años (art. 43).[[2]] Con volúmenes crecientes, los procesos manuales se vuelven lentos, inconsistentes y difíciles de auditar.</p>
<p>El GAFI reconoce que las nuevas tecnologías pueden hacer más eficiente y eficaz la prevención, siempre que se gestionen sus riesgos.[[1]]</p>
<div class="callout key"><b>Idea clave</b>Automatizar no es reemplazar al analista: es liberarlo de tareas repetitivas para que dedique su tiempo al juicio profesional.</div>
"""},
{"title": "Qué automatizar y qué no", "html": """
<div class="grid-2">
<div class="mini"><h4>Buenas candidatas</h4><p>Consulta en listas y medios; cálculo del riesgo con la matriz; recordatorios de actualización de expedientes; consolidación de transacciones en efectivo para el RTE; generación de alertas por reglas; tableros de indicadores; bitácoras de revisión.</p></div>
<div class="mini"><h4>Requieren juicio humano</h4><p>Decidir si una operación es sospechosa; redactar el razonamiento del ROS; aprobar relaciones de alto riesgo; resolver coincidencias dudosas en listas; interpretar normativa nueva.</p></div>
</div>
"""},
{"title": "Herramientas accesibles", "html": """
<ul>
<li><strong>Hojas de cálculo con reglas:</strong> validaciones de datos, fórmulas de ponderación y formato condicional para matrices de riesgo.</li>
<li><strong>Flujos automatizados</strong> (por ejemplo, Power Automate): solicitudes de aprobación, recordatorios y registro de evidencias.</li>
<li><strong>Tableros</strong> (por ejemplo, Power BI): indicadores de alertas, tiempos de atención y distribución del riesgo.</li>
<li><strong>Bases de datos y scripts:</strong> cuando el volumen exige consultas reproducibles y control de versiones.</li>
</ul>
<p>La herramienta importa menos que el diseño: un proceso confuso automatizado sigue siendo confuso, solo que más rápido.</p>
"""},
{"title": "Controles que no pueden faltar", "html": """
<ul>
<li><strong>Calidad de datos:</strong> campos obligatorios, formatos validados (cédula, RNC) y conciliación con las fuentes.</li>
<li><strong>Trazabilidad:</strong> registro de quién hizo qué y cuándo; versiones de reglas y parámetros.</li>
<li><strong>Control de cambios y pruebas:</strong> ninguna regla se modifica en producción sin probarla y aprobarla.</li>
<li><strong>Protección de datos personales:</strong> tratamiento conforme a la Ley 172-13 y acceso según el principio de mínimo privilegio.[[3]]</li>
<li><strong>Confidencialidad reforzada:</strong> la información de reportes y análisis está protegida por el art. 63; limita accesos y evita herramientas externas no autorizadas.[[2]]</li>
</ul>
"""},
{"title": "Hoja de ruta", "html": """
<ol class="steps">
<li><strong>Mapear</strong> el proceso actual: pasos, tiempos, responsables y puntos de error.</li>
<li><strong>Medir</strong> una línea base: horas dedicadas, alertas por analista, errores de llenado, rechazos.</li>
<li><strong>Priorizar</strong> por impacto y facilidad.</li>
<li><strong>Pilotear</strong> en pequeño, con usuarios reales y criterios de éxito definidos.</li>
<li><strong>Escalar y mejorar</strong> con indicadores: tiempo de cierre de alertas, falsos positivos, rechazos de reportes, expedientes vencidos.</li>
</ol>
"""},
],
"quiz": [
{"q": "¿Cuál es el propósito principal de automatizar en cumplimiento?", "options": ["Eliminar al oficial de cumplimiento", "Liberar tiempo de tareas repetitivas para dedicarlo al juicio profesional", "Reportar todo automáticamente", "Evitar la supervisión"], "answer": 1, "explain": "La automatización apoya, no sustituye, el criterio humano [[1]]."},
{"q": "¿Cuál de estas tareas requiere juicio humano y no debe automatizarse por completo?", "options": ["Recordatorios de actualización", "Decidir si una operación es sospechosa", "Consolidar transacciones para el RTE", "Calcular puntajes de la matriz"], "answer": 1, "explain": "La decisión de reportar exige análisis y criterio profesional."},
{"q": "¿Qué ley dominicana regula la protección de datos personales?", "options": ["Ley 53-07", "Ley 172-13", "Ley 155-17", "Ley 249-17"], "answer": 1, "explain": "La Ley 172-13 regula la protección integral de los datos personales [[3]]."},
{"q": "¿Por qué hay que restringir el acceso a la información de reportes en las herramientas automatizadas?", "options": ["Por estética", "Porque el art. 63 prohíbe revelar que se reportó o se examina una operación", "Para ahorrar licencias", "No es necesario"], "answer": 1, "explain": "La confidencialidad de los reportes es una obligación legal [[2]]."},
{"q": "¿Qué indicador sirve para medir el éxito de una automatización de alertas?", "options": ["Número de colores del tablero", "Reducción de falsos positivos y del tiempo de cierre de alertas", "Cantidad de correos enviados", "Tamaño del archivo"], "answer": 1, "explain": "Los indicadores deben reflejar eficacia y eficiencia del proceso."},
{"q": "Antes de modificar una regla de alertas en producción se debe:", "options": ["Hacerlo directamente para ganar tiempo", "Probarla, aprobarla y documentar la versión", "Avisar al cliente", "Desactivar todas las alertas"], "answer": 1, "explain": "El control de cambios evita errores y mantiene la trazabilidad."},
],
},
# ---------------------------------------------------------------------------------------------
{
"num": 13, "slug": "inteligencia-artificial-aplicada-a-plaft", "tag": "Tecnología", "level": "Avanzado", "minutes": 25,
"title": "Inteligencia artificial aplicada a PLAFT",
"card": "Usos, riesgos y gobierno responsable de la IA en cumplimiento.",
"summary": "Explora cómo la inteligencia artificial puede apoyar la prevención del lavado de activos, cuáles son sus riesgos y qué marco de gobierno permite usarla de forma responsable y supervisada.",
"objectives": [
  "Diferenciar los principales tipos de IA y sus aplicaciones en PLAFT.",
  "Identificar riesgos: sesgos, falta de explicabilidad, errores y confidencialidad.",
  "Aplicar principios de gobierno basados en marcos reconocidos.",
  "Usar herramientas de IA generativa sin comprometer información reservada.",
],
"sources": [GAFI_TECH, NIST_AI, ISO_42001, LEY, LEY_17213],
"modules": [
{"title": "Qué es (y qué no es) la IA en cumplimiento", "html": """
<ul>
<li><strong>Aprendizaje automático supervisado:</strong> aprende de casos etiquetados (por ejemplo, alertas confirmadas o descartadas) para priorizar nuevas alertas.</li>
<li><strong>No supervisado:</strong> encuentra grupos o anomalías sin etiquetas previas; útil para segmentar y detectar comportamientos atípicos.</li>
<li><strong>Procesamiento del lenguaje:</strong> analiza textos, como noticias o documentos, para extraer información relevante.</li>
<li><strong>IA generativa:</strong> produce textos o resúmenes; útil para borradores, nunca como fuente de verdad sin verificación.</li>
</ul>
<div class="callout key"><b>Idea clave</b>La IA estima probabilidades a partir de datos. No conoce la ley ni asume responsabilidad: esa sigue siendo de la entidad y de sus profesionales.</div>
"""},
{"title": "Casos de uso", "html": """
<p>El GAFI identifica oportunidades en el monitoreo de transacciones, la debida diligencia y la evaluación de riesgos de clientes, así como en el análisis de grandes volúmenes de datos.[[1]]</p>
<ul>
<li>Priorizar alertas y reducir falsos positivos.</li>
<li>Mejorar la coincidencia en listas con nombres escritos de forma distinta.</li>
<li>Clasificar noticias adversas por relevancia.</li>
<li>Resumir expedientes extensos para acelerar la revisión.</li>
<li>Detectar redes de cuentas relacionadas.</li>
</ul>
"""},
{"title": "Riesgos que hay que gestionar", "html": """
<ul>
<li><strong>Sesgo:</strong> si los datos históricos están sesgados, el modelo reproduce el sesgo.</li>
<li><strong>Explicabilidad:</strong> el supervisor y la propia entidad deben poder entender por qué el modelo prioriza o descarta un caso.[[1]]</li>
<li><strong>Errores y «alucinaciones»:</strong> la IA generativa puede inventar datos, artículos o fuentes con apariencia convincente.</li>
<li><strong>Confidencialidad:</strong> subir información de clientes o de reportes a herramientas externas puede violar el art. 63 de la Ley 155-17 y la Ley 172-13.[[4,5]]</li>
<li><strong>Dependencia:</strong> perder la capacidad de análisis propio por confiar ciegamente en el sistema.</li>
</ul>
"""},
{"title": "Gobierno responsable", "html": """
<p>Dos referencias reconocidas orientan el gobierno de la IA:</p>
<ul>
<li><strong>NIST AI RMF 1.0</strong> organiza la gestión en cuatro funciones: <em>gobernar</em>, <em>mapear</em>, <em>medir</em> y <em>gestionar</em> los riesgos de la IA.[[2]]</li>
<li><strong>ISO/IEC 42001:2023</strong> establece requisitos para un sistema de gestión de la IA dentro de la organización.[[3]]</li>
</ul>
<ol class="steps">
<li>Definir responsables y casos de uso autorizados.</li>
<li>Documentar datos, supuestos y limitaciones de cada modelo.</li>
<li>Validar antes de usar y monitorear el desempeño después.</li>
<li>Mantener supervisión humana en toda decisión con efectos sobre clientes o reportes.</li>
<li>Revisar periódicamente sesgos y desempeño.</li>
</ol>
"""},
{"title": "Uso responsable de la IA generativa", "html": """
<div class="grid-2">
<div class="mini"><h4>Sí</h4><p>Borradores de políticas, guías de capacitación o correos genéricos; resúmenes de normativa pública que luego verificas en la fuente oficial; ideas para estructurar un análisis.</p></div>
<div class="mini"><h4>No</h4><p>Datos de clientes o de reportes en herramientas no autorizadas; citar artículos o cifras sin verificarlos; delegar la decisión de reportar.</p></div>
</div>
<div class="callout warn"><b>Regla de oro</b>La tecnología complementa el criterio profesional; no sustituye la evaluación humana.</div>
"""},
],
"quiz": [
{"q": "¿Qué tipo de IA aprende de casos etiquetados, como alertas confirmadas o descartadas?", "options": ["No supervisada", "Aprendizaje automático supervisado", "IA generativa", "Ninguna"], "answer": 1, "explain": "El aprendizaje supervisado usa ejemplos etiquetados para aprender."},
{"q": "¿Cuál es un riesgo propio de la IA generativa?", "options": ["Que sea demasiado lenta", "Que produzca datos o fuentes inventados con apariencia convincente", "Que no funcione en español", "Que reduzca costos"], "answer": 1, "explain": "Las «alucinaciones» exigen verificar siempre en fuentes oficiales."},
{"q": "¿Por qué no se deben subir datos de un ROS a una herramienta de IA externa no autorizada?", "options": ["Porque es lento", "Porque puede violar la confidencialidad del art. 63 y la protección de datos", "Porque la IA no entiende reportes", "No hay ningún problema"], "answer": 1, "explain": "La reserva de los reportes y la protección de datos personales son obligaciones legales [[4,5]]."},
{"q": "¿Cuáles son las cuatro funciones del NIST AI RMF 1.0?", "options": ["Planear, hacer, verificar, actuar", "Gobernar, mapear, medir y gestionar", "Identificar, proteger, detectar, responder", "Analizar, diseñar, construir, probar"], "answer": 1, "explain": "El marco del NIST organiza la gestión de riesgos de la IA en esas cuatro funciones [[2]]."},
{"q": "¿Quién conserva la responsabilidad por las decisiones apoyadas en IA?", "options": ["El proveedor del software", "La entidad y sus profesionales", "El modelo", "Nadie"], "answer": 1, "explain": "La IA apoya; la responsabilidad sigue en la organización y en quienes deciden [[1]]."},
{"q": "¿Qué uso de la IA generativa es apropiado?", "options": ["Decidir si enviar un ROS", "Redactar un borrador de guía de capacitación que luego se verifica", "Cargar la base de clientes en una herramienta gratuita", "Citar artículos de ley sin revisarlos"], "answer": 1, "explain": "Es útil para borradores, siempre con verificación y sin datos reservados."},
],
},
]
