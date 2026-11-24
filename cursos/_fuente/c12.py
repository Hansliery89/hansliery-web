"""Curso 12 · Automatización de procesos de cumplimiento."""
from fuentes import *  # noqa: F401,F403
from capas import ess, deep

# 1 GAFI_TECH_M · 2 LEY · 3 LEY_17213 · 4 GAFI40 · 5 UAF_ROS · 6 SIS_NORMA · 7 DGII_N01 · 8 IDECOOP_NORMA · 9 SB_ONBOARD
COURSE = {
"num": 12, "slug": "automatizacion-de-procesos-de-cumplimiento", "tag": "Tecnología", "level": "Básico → Profesional", "minutes": 50,
"title": "Automatización de procesos de cumplimiento",
"card": "Qué automatizar, con qué herramientas y con qué controles.",
"summary": "Descubre qué exige la normativa en materia de infraestructura tecnológica, qué procesos de cumplimiento conviene automatizar, qué herramientas accesibles existen y qué controles de calidad de datos, trazabilidad, protección de datos personales y confidencialidad deben acompañarlos, con una hoja de ruta medible.",
"objectives": [
  "Identificar lo que piden las normas sectoriales sobre sistemas y plataforma tecnológica.",
  "Distinguir lo que se puede automatizar de lo que exige juicio humano.",
  "Elegir herramientas accesibles según el problema y el volumen.",
  "Aplicar controles de calidad de datos, trazabilidad, conservación y confidencialidad.",
  "Cumplir los principios de la Ley 172-13 al tratar datos personales.",
  "Construir una hoja de ruta de automatización con indicadores.",
],
"sources": [GAFI_TECH_M, LEY, LEY_17213, GAFI40, UAF_ROS, SIS_NORMA, DGII_N01, IDECOOP_NORMA, SB_ONBOARD],
"modules": [
# 1 ------------------------------------------------------------------------------------------
{"title": "Por qué automatizar", "html": ess(
"Cumplimiento es trabajo que no se acaba: revisar clientes, vigilar operaciones, guardar papeles diez años, enviar reportes cada mes. Hacerlo todo a mano es lento y da errores. Automatizar libera tiempo para lo que sí necesita a una persona: pensar y decidir.") + """
<p>Las obligaciones de cumplimiento son continuas: la ley exige monitorear permanentemente la relación con los clientes (art. 39), remitir los reportes de efectivo cada mes (art. 53) y conservar registros durante al menos diez años (art. 43).[[2]] Con volúmenes crecientes, los procesos manuales se vuelven lentos, inconsistentes y difíciles de auditar.</p>
<p>El GAFI reconoce que las nuevas tecnologías pueden hacer más eficiente y eficaz la prevención —en identificación digital, monitoreo de transacciones o análisis de datos—, siempre que se gestionen sus riesgos y se superen obstáculos como la calidad de los datos y los sistemas heredados.[[1]]</p>
<div class="callout key"><b>Idea clave</b>Automatizar no es reemplazar al analista: es liberarlo de tareas repetitivas para que dedique su tiempo al juicio profesional.</div>
""" + deep("""
<p><strong>Obligación, no solo eficiencia.</strong> El GAFI advierte que la tecnología no sustituye las obligaciones ni la responsabilidad de la entidad; la decisión de adoptarla debe basarse en riesgo y en una comprensión clara de sus limitaciones.[[1]]</p>
""")},
# 2 ------------------------------------------------------------------------------------------
{"title": "Lo que piden las normas", "html": ess(
"Algunas normas ya exigen tecnología: la de seguros pide sistemas que actualicen los factores de riesgo, automaticen las alertas y preparen los reportes a la UAF. La de cooperativas pide describir la plataforma tecnológica en el manual.") + """
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Norma</th><th>Requisito tecnológico</th></tr></thead>
<tbody>
<tr><td>Seguros (art. 6.4)</td><td>Sistemas acordes con el tamaño, riesgo y volumen de negocio, con, como mínimo, actualización periódica de los factores de riesgo, <strong>automatización de señales de alerta</strong> y <strong>parametrización de los reportes regulatorios</strong> a la UAF.[[6]]</td></tr>
<tr><td>Seguros (monitoreo)</td><td>Parámetros de alertas, manuales o automatizados, que permitan analizar si las operaciones corresponden al perfil del cliente.[[6]]</td></tr>
<tr><td>Cooperativas</td><td>El manual debe describir, si aplica, la plataforma tecnológica: conozca a su asociado, actualización de información, monitoreo, reportes internos y reportes a las autoridades.[[8]]</td></tr>
<tr><td>DGII</td><td>Los registros digitales deben permitir reconstruir transacciones individuales con suficiente rapidez y estar a disposición del supervisor.[[7]]</td></tr>
<tr><td>Banca (onboarding digital)</td><td>Mecanismos tecnológicos seguros de identificación, verificación y autenticación, con resguardo de la evidencia por 10 años.[[9]]</td></tr>
</tbody></table></div>
""" + deep("""
<p><strong>Reportes tabulados.</strong> La DGII pide a sus sujetos obligados un reporte trimestral de información acumulada y tabulada: volumen y montos por categoría de cliente, cantidad de clientes por tipo, nacionalidad y residencia, número de clientes por categoría de riesgo y operaciones con extranjeros.[[7]] Es un ejemplo típico de reporte que conviene generar automáticamente desde la base de clientes.</p>
""")},
# 3 ------------------------------------------------------------------------------------------
{"title": "Qué automatizar y qué no", "html": ess(
"Las máquinas son buenas para tareas repetitivas: revisar listas, calcular puntajes, recordar vencimientos, sumar efectivo para el RTE. Las personas deben decidir lo importante: si algo es sospechoso, qué escribir en el ROS o si se acepta un cliente de alto riesgo.") + """
<div class="grid-2">
<div class="mini"><h4>Buenas candidatas</h4><p>Consulta en listas y medios; cálculo del riesgo con la matriz; recordatorios de actualización de expedientes; consolidación de transacciones en efectivo para el RTE (incluida la suma de las múltiples en 24 horas del art. 54); generación de alertas por reglas; tableros de indicadores; bitácoras de revisión.[[2]]</p></div>
<div class="mini"><h4>Requieren juicio humano</h4><p>Decidir si una operación es sospechosa; redactar el razonamiento del ROS; aprobar relaciones de alto riesgo y con PEP; resolver coincidencias dudosas en listas; interpretar normativa nueva.</p></div>
</div>
<div class="callout warn"><b>Coincidencias en listas de la ONU</b>Un sistema puede detectar la coincidencia, pero confirmarla, congelar sin demora y notificar al Ministerio Público y a la UAF son decisiones que deben quedar a cargo de personas responsables (art. 83).[[2]]</div>
""" + deep("""
<p><strong>Calidad del ROS.</strong> La UAF insiste en que el reporte explique el razonamiento y los hechos; un texto generado automáticamente a partir de plantillas, sin análisis, es precisamente el tipo de reporte que no aporta inteligencia.[[5]] La automatización puede preparar los datos del reporte, no la conclusión.</p>
""")},
# 4 ------------------------------------------------------------------------------------------
{"title": "Herramientas accesibles", "html": ess(
"No hace falta un gran sistema para empezar. Una hoja de cálculo bien hecha, un flujo de aprobaciones y un tablero de indicadores ya cambian mucho. Lo que más importa es diseñar bien el proceso antes de automatizarlo.") + """
<ul>
<li><strong>Hojas de cálculo con reglas:</strong> validaciones de datos, fórmulas de ponderación y formato condicional para matrices de riesgo.</li>
<li><strong>Flujos automatizados</strong> (por ejemplo, Power Automate): solicitudes de aprobación, recordatorios y registro de evidencias.</li>
<li><strong>Tableros</strong> (por ejemplo, Power BI): indicadores de alertas, tiempos de atención y distribución del riesgo.</li>
<li><strong>Bases de datos y scripts</strong> (por ejemplo, SQL o Python): cuando el volumen exige consultas reproducibles y control de versiones.</li>
<li><strong>Interfaces de programación (API)</strong> con fuentes oficiales o proveedores de listas, cuando estén disponibles y autorizadas.</li>
</ul>
<p>La herramienta importa menos que el diseño: un proceso confuso automatizado sigue siendo confuso, solo que más rápido.</p>
""" + deep("""
<p><strong>Cuándo cambiar de herramienta.</strong> Señales de que una hoja de cálculo ya no alcanza: varias personas la editan a la vez, no hay forma de saber quién cambió qué, los cálculos tardan o se copian datos a mano entre archivos. En ese punto conviene una base de datos con control de acceso y bitácora.</p>
<p><strong>Proveedores externos.</strong> Si se contrata un sistema, el sujeto obligado sigue siendo responsable del cumplimiento; evalúa la seguridad del proveedor, el lugar donde se almacenan los datos y las condiciones de acceso, a la luz de la reserva del art. 63 y de la Ley 172-13.[[2,3]]</p>
""")},
# 5 ------------------------------------------------------------------------------------------
{"title": "Datos personales y confidencialidad", "html": ess(
"Automatizar significa mover muchos datos de personas. La Ley 172-13 exige que esos datos sean ciertos, estén al día, se protejan y solo los vea quien debe. Y lo relativo a los reportes a la UAF es todavía más reservado.") + """
<p>La Ley 172-13 fija, entre otros, estos principios y deberes:[[3]]</p>
<ul>
<li><strong>Calidad de los datos:</strong> ciertos, adecuados y pertinentes a la finalidad; exactos y actualizados; los inexactos o incompletos deben corregirse (art. 5).</li>
<li><strong>Seguridad:</strong> conservar la información en condiciones que impidan su adulteración, pérdida, consulta o acceso no autorizado (art. 13).</li>
<li><strong>Acceso limitado:</strong> permitir el acceso solo a las personas que tengan derecho a ella (art. 13).</li>
<li><strong>Manual interno</strong> de políticas y procedimientos para cumplir la ley y atender consultas y reclamos (art. 13).</li>
</ul>
<p>La ley exceptúa del consentimiento, entre otros casos, los datos recabados en virtud de una <strong>obligación legal</strong> o derivados de una relación comercial y necesarios para su cumplimiento (art. 27).[[3]] Esa excepción no elimina los deberes de calidad y seguridad.</p>
<div class="callout warn"><b>Confidencialidad reforzada</b>La información de reportes y análisis está protegida por el art. 63 de la Ley 155-17: limita accesos y evita herramientas externas no autorizadas.[[2]]</div>
""" + deep("""
<p><strong>Mínimo privilegio.</strong> Diseña perfiles de acceso: el área comercial puede ver la calificación de riesgo de un cliente, pero no la existencia de un ROS; el equipo de cumplimiento ve los expedientes de análisis; solo administradores autorizados gestionan permisos. Registra los accesos.</p>
<p><strong>Ambientes de prueba.</strong> No uses datos reales de clientes en pruebas sin anonimizarlos; la propia Ley 172-13 reconoce la disociación de datos como forma de que los titulares no sean identificables (art. 27).[[3]]</p>
""")},
# 6 ------------------------------------------------------------------------------------------
{"title": "Controles que no pueden faltar", "html": ess(
"Todo lo automatizado necesita controles: datos validados, registro de quién hizo qué, pruebas antes de cambiar una regla y copias que permitan reconstruir lo que pasó durante diez años.") + """
<ul>
<li><strong>Calidad de datos:</strong> campos obligatorios, formatos validados (cédula, RNC) y conciliación con las fuentes.</li>
<li><strong>Trazabilidad:</strong> registro de quién hizo qué y cuándo; versiones de reglas y parámetros.</li>
<li><strong>Control de cambios y pruebas:</strong> ninguna regla se modifica en producción sin probarla y aprobarla.</li>
<li><strong>Conservación:</strong> registros por al menos 10 años, en medios que permitan reconstruir transacciones individuales con rapidez.[[2,7]]</li>
<li><strong>Protección de datos personales:</strong> tratamiento conforme a la Ley 172-13 y acceso según el principio de mínimo privilegio.[[3]]</li>
<li><strong>Confidencialidad:</strong> segregar la información de reportes y análisis (art. 63).[[2]]</li>
</ul>
""" + deep("""
<p><strong>Validación de reglas.</strong> Antes de activar una regla nueva, pruébala con datos históricos: ¿cuántas alertas habría generado?, ¿cuántas habrían terminado en ROS?, ¿habría detectado los casos ya conocidos? Documenta los resultados y la aprobación. Es la misma lógica de calibración de la matriz del curso 4.</p>
""")},
# 7 ------------------------------------------------------------------------------------------
{"title": "Hoja de ruta y caso", "html": ess(
"Para automatizar con éxito: dibuja el proceso actual, mide cuánto tarda, elige por dónde empezar, prueba en pequeño y mide el resultado.") + """
<ol class="steps">
<li><strong>Mapear</strong> el proceso actual: pasos, tiempos, responsables y puntos de error.</li>
<li><strong>Medir</strong> una línea base: horas dedicadas, alertas por analista, errores de llenado, rechazos.</li>
<li><strong>Priorizar</strong> por impacto y facilidad.</li>
<li><strong>Pilotear</strong> en pequeño, con usuarios reales y criterios de éxito definidos.</li>
<li><strong>Escalar y mejorar</strong> con indicadores: tiempo de cierre de alertas, falsos positivos, rechazos de reportes, expedientes vencidos.</li>
</ol>
<div class="case"><b>Caso · «El RTE de cada mes»</b>
<p>Un analista dedica dos días al mes a consolidar a mano los depósitos en efectivo de varias sucursales para preparar el RTE, y en ocasiones no suma las operaciones múltiples de un mismo cliente en 24 horas.</p>
<p><strong>Solución:</strong> una consulta automática que agrupa por cliente y por ventana de 24 horas, marca las que alcanzan US$15,000 (art. 54), genera el archivo para revisión y deja bitácora. El analista revisa excepciones y envía dentro de los primeros 10 días calendario (art. 53).[[2]]</p>
<p class="verdict yes"><b>Resultado esperado:</b> menos horas, cero omisiones de operaciones múltiples y evidencia de cada envío.</p>
</div>
""" + deep("""
<p><strong>Indicadores útiles.</strong> Tiempo promedio de cierre de alertas; porcentaje de alertas que terminan en ROS por regla; reportes rechazados en goAML; expedientes con debida diligencia vencida; clientes de alto riesgo sin revisión en el plazo. Presentarlos a la alta dirección ayuda a justificar nuevas inversiones.</p>
""")},
],
"glossary": [
("Automatización", "Uso de herramientas para ejecutar tareas repetitivas sin intervención manual en cada paso."),
("Regla de alerta", "Condición parametrizada que genera una alerta para revisión [[6]]."),
("Falso positivo", "Alerta que, tras el análisis, no corresponde a una situación de riesgo."),
("Trazabilidad", "Registro que permite saber quién hizo qué, cuándo y con qué versión de reglas."),
("Control de cambios", "Procedimiento para probar, aprobar y documentar las modificaciones."),
("Mínimo privilegio", "Dar a cada usuario solo el acceso que necesita para su función."),
("Calidad de los datos", "Principio de la Ley 172-13: datos ciertos, adecuados, pertinentes, exactos y actualizados [[3]]."),
("Disociación", "Tratamiento que impide identificar a los titulares de los datos [[3]]."),
],
"quiz": [
{"q": "¿Cuál es el propósito principal de automatizar en cumplimiento?", "options": ["Eliminar al oficial de cumplimiento", "Liberar tiempo de tareas repetitivas para dedicarlo al juicio profesional", "Reportar todo automáticamente", "Evitar la supervisión"], "answer": 1, "explain": "La automatización apoya, no sustituye, el criterio humano [[1]]."},
{"q": "Según la norma de seguros, ¿qué debe incluir como mínimo el soporte tecnológico?", "options": ["Un sitio web", "Actualización de factores de riesgo, automatización de alertas y parametrización de reportes regulatorios", "Redes sociales", "Un chat con clientes"], "answer": 1, "explain": "Así lo exige el art. 6.4 de la norma de seguros [[6]]."},
{"q": "¿Cuál de estas tareas requiere juicio humano y no debe automatizarse por completo?", "options": ["Recordatorios de actualización", "Decidir si una operación es sospechosa", "Consolidar transacciones para el RTE", "Calcular puntajes de la matriz"], "answer": 1, "explain": "La decisión de reportar exige análisis y criterio profesional [[5]]."},
{"q": "Un sistema detecta una coincidencia con las listas del Consejo de Seguridad. ¿Qué corresponde?", "options": ["Que el sistema la cierre solo", "Que una persona responsable la confirme y, si procede, congele sin demora y notifique", "Ignorarla", "Enviarla al cliente"], "answer": 1, "explain": "El art. 83 exige congelar sin demora y notificar al Ministerio Público y a la UAF [[2]]."},
{"q": "¿Qué ley dominicana regula la protección de datos personales?", "options": ["Ley 53-07", "Ley 172-13", "Ley 155-17", "Ley 249-17"], "answer": 1, "explain": "La Ley 172-13 regula la protección integral de los datos personales [[3]]."},
{"q": "Según la Ley 172-13, los datos personales deben ser:", "options": ["Muchos, aunque no sean necesarios", "Ciertos, adecuados, pertinentes, exactos y actualizados", "Públicos", "Borrados cada mes"], "answer": 1, "explain": "Es el principio de calidad de los datos del art. 5 [[3]]."},
{"q": "¿Por qué hay que restringir el acceso a la información de reportes en las herramientas automatizadas?", "options": ["Por estética", "Porque el art. 63 prohíbe revelar que se reportó o se examina una operación", "Para ahorrar licencias", "No es necesario"], "answer": 1, "explain": "La confidencialidad de los reportes es una obligación legal [[2]]."},
{"q": "Según la DGII, los registros digitales deben:", "options": ["Borrarse al año", "Permitir reconstruir transacciones individuales con rapidez y estar disponibles para el supervisor", "Estar solo en papel", "Enviarse al cliente"], "answer": 1, "explain": "Así lo establece la Norma 01-2018 [[7]]."},
{"q": "¿Qué indicador sirve para medir el éxito de una automatización de alertas?", "options": ["Número de colores del tablero", "Reducción de falsos positivos y del tiempo de cierre de alertas", "Cantidad de correos enviados", "Tamaño del archivo"], "answer": 1, "explain": "Los indicadores deben reflejar eficacia y eficiencia del proceso."},
{"q": "Antes de modificar una regla de alertas en producción se debe:", "options": ["Hacerlo directamente para ganar tiempo", "Probarla, aprobarla y documentar la versión", "Avisar al cliente", "Desactivar todas las alertas"], "answer": 1, "explain": "El control de cambios evita errores y mantiene la trazabilidad."},
],
}
