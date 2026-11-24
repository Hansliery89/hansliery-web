"""Curso 13 · Inteligencia artificial aplicada a PLAFT."""
from fuentes import *  # noqa: F401,F403
from capas import ess, deep

# 1 GAFI_TECH_M · 2 NIST_AI_DOC · 3 ISO_42001 · 4 LEY · 5 LEY_17213 · 6 UAF_ROS
COURSE = {
"num": 13, "slug": "inteligencia-artificial-aplicada-a-plaft", "tag": "Tecnología", "level": "Intermedio → Profesional", "minutes": 50,
"title": "Inteligencia artificial aplicada a PLAFT",
"card": "Usos, riesgos y gobierno responsable de la IA en cumplimiento.",
"summary": "Explora cómo la inteligencia artificial puede apoyar la prevención del lavado de activos, qué tipos de IA existen y para qué sirve cada uno, cuáles son sus riesgos y qué marco de gobierno —NIST AI RMF e ISO/IEC 42001— permite usarla de forma responsable, supervisada y compatible con la confidencialidad que exige la ley.",
"objectives": [
  "Diferenciar los principales tipos de IA y sus aplicaciones en PLAFT.",
  "Identificar casos de uso con valor real en monitoreo, debida diligencia y listas.",
  "Reconocer riesgos: sesgos, falta de explicabilidad, errores, confidencialidad y dependencia.",
  "Aplicar las funciones y características de confianza del NIST AI RMF y el enfoque de ISO/IEC 42001.",
  "Usar herramientas de IA generativa sin comprometer información reservada.",
  "Evaluar un caso de uso de IA antes de ponerlo en producción.",
],
"sources": [GAFI_TECH_M, NIST_AI_DOC, ISO_42001, LEY, LEY_17213, UAF_ROS],
"modules": [
# 1 ------------------------------------------------------------------------------------------
{"title": "Qué es (y qué no es) la IA en cumplimiento", "html": ess(
"La inteligencia artificial son programas que aprenden de datos para encontrar patrones o producir textos. Pueden ayudar mucho, pero no conocen la ley ni son responsables de nada: quien decide y responde sigue siendo la entidad.") + """
<ul>
<li><strong>Aprendizaje automático supervisado:</strong> aprende de casos etiquetados (por ejemplo, alertas confirmadas o descartadas) para priorizar nuevas alertas.</li>
<li><strong>No supervisado:</strong> encuentra grupos o anomalías sin etiquetas previas; útil para segmentar y detectar comportamientos atípicos.</li>
<li><strong>Procesamiento del lenguaje:</strong> analiza textos, como noticias o documentos, para extraer información relevante.</li>
<li><strong>IA generativa:</strong> produce textos o resúmenes; útil para borradores, nunca como fuente de verdad sin verificación.</li>
</ul>
<div class="callout key"><b>Idea clave</b>La IA estima probabilidades a partir de datos. No conoce la ley ni asume responsabilidad: esa sigue siendo de la entidad y de sus profesionales.</div>
""" + deep("""
<p><strong>Reglas frente a modelos.</strong> Los sistemas tradicionales de monitoreo usan reglas fijas («alertar si el efectivo supera X»). Los modelos aprenden combinaciones de variables que una regla no capta, pero son más difíciles de explicar. En la práctica, muchas entidades combinan ambos: reglas para lo que exige la norma y modelos para priorizar.</p>
<p><strong>Visión del GAFI.</strong> El GAFI identifica la IA y el aprendizaje automático, junto con la identidad digital y el análisis de grandes datos, entre las tecnologías con mayor potencial para mejorar la eficacia, y advierte que su adopción debe ser responsable y basada en riesgo.[[1]]</p>
""")},
# 2 ------------------------------------------------------------------------------------------
{"title": "Casos de uso", "html": ess(
"La IA es útil para ordenar alertas por importancia, reconocer nombres escritos de formas distintas en listas, clasificar noticias negativas, resumir expedientes y descubrir redes de cuentas relacionadas.") + """
<p>El GAFI identifica oportunidades en el monitoreo de transacciones, la debida diligencia y la evaluación de riesgos de clientes, así como en el análisis de grandes volúmenes de datos.[[1]]</p>
<ul>
<li><strong>Priorizar alertas</strong> y reducir falsos positivos, para que el analista revise primero lo más relevante.</li>
<li><strong>Mejorar la coincidencia en listas</strong> con nombres escritos de forma distinta o transliterados.</li>
<li><strong>Clasificar noticias adversas</strong> por relevancia y por tipo de delito.</li>
<li><strong>Resumir expedientes</strong> extensos para acelerar la revisión.</li>
<li><strong>Detectar redes</strong> de cuentas relacionadas (mismo dispositivo, contactos o contrapartes).</li>
<li><strong>Segmentar clientes</strong> con técnicas de agrupamiento, como insumo de la matriz (curso 4).</li>
</ul>
""" + deep("""
<p><strong>Valor medible.</strong> Antes de adoptar un caso de uso, define qué mejora esperas y cómo lo medirás: menos falsos positivos sin perder casos relevantes, menos tiempo por expediente o más coincidencias verdaderas en listas. Si no se puede medir, no se puede justificar ante la dirección ni ante el supervisor.</p>
""")},
# 3 ------------------------------------------------------------------------------------------
{"title": "Riesgos que hay que gestionar", "html": ess(
"La IA puede repetir prejuicios de los datos, dar respuestas que nadie sabe explicar, inventar información con mucha seguridad y exponer datos confidenciales si se usa en herramientas no autorizadas.") + """
<ul>
<li><strong>Sesgo:</strong> si los datos históricos están sesgados, el modelo reproduce el sesgo.</li>
<li><strong>Explicabilidad:</strong> el supervisor y la propia entidad deben poder entender por qué el modelo prioriza o descarta un caso.[[1]]</li>
<li><strong>Errores y «alucinaciones»:</strong> la IA generativa puede inventar datos, artículos o fuentes con apariencia convincente.</li>
<li><strong>Confidencialidad:</strong> subir información de clientes o de reportes a herramientas externas puede violar el art. 63 de la Ley 155-17 y la Ley 172-13.[[4,5]]</li>
<li><strong>Dependencia:</strong> perder la capacidad de análisis propio por confiar ciegamente en el sistema.</li>
<li><strong>Deriva:</strong> un modelo que funcionaba puede degradarse cuando cambian los clientes, los productos o las tipologías.</li>
</ul>
""" + deep("""
<p><strong>Calidad de los datos.</strong> La Ley 172-13 exige que los datos personales sean ciertos, adecuados, pertinentes, exactos y actualizados (art. 5), y que se conserven con seguridad y acceso limitado (art. 13).[[5]] Un modelo entrenado con datos que no cumplen ese estándar hereda sus defectos.</p>
<p><strong>Un falso negativo cuesta más.</strong> Si un modelo descarta automáticamente alertas que habrían terminado en ROS, la entidad podría incumplir el deber de reportar, que es una infracción muy grave (art. 69).[[4]] Por eso la supervisión humana debe cubrir también lo que el modelo descarta.</p>
""")},
# 4 ------------------------------------------------------------------------------------------
{"title": "Gobierno responsable: NIST AI RMF", "html": ess(
"Un marco muy usado para gobernar la IA es el del NIST de Estados Unidos. Organiza el trabajo en cuatro funciones: gobernar, mapear, medir y gestionar, y describe qué características debe tener una IA confiable.") + """
<p>El <strong>NIST AI RMF 1.0</strong> (NIST AI 100-1, 2023) organiza la gestión del riesgo de la IA en cuatro funciones:[[2]]</p>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Función</th><th>Aplicación en PLAFT</th></tr></thead>
<tbody>
<tr><td><strong>Gobernar</strong></td><td>Políticas, roles y responsabilidades; quién aprueba un modelo y quién responde por él.</td></tr>
<tr><td><strong>Mapear</strong></td><td>Contexto del uso: qué decisión apoya, qué datos usa, a quién puede afectar.</td></tr>
<tr><td><strong>Medir</strong></td><td>Métricas de desempeño, sesgo y estabilidad; pruebas antes y después de implementar.</td></tr>
<tr><td><strong>Gestionar</strong></td><td>Priorizar y tratar los riesgos identificados; planes de respuesta y retiro del modelo si falla.</td></tr>
</tbody></table></div>
<p class="note-small">La columna de aplicación es de elaboración propia.</p>
<p>El marco describe como características de una IA confiable que sea válida y fiable; segura; protegida y resiliente; responsable y transparente; explicable e interpretable; respetuosa de la privacidad; y justa, con los sesgos perjudiciales gestionados.[[2]]</p>
""" + deep("""
<p><strong>Gobernar es transversal.</strong> El NIST presenta la función de gobernar como transversal a las otras tres: sin roles, políticas y cultura de gestión del riesgo, las mediciones no se traducen en decisiones.[[2]]</p>
<p><strong>Voluntario y adaptable.</strong> El AI RMF es un marco voluntario, pensado para adaptarse a organizaciones de cualquier tamaño y sector.[[2]]</p>
""")},
# 5 ------------------------------------------------------------------------------------------
{"title": "Gobierno responsable: ISO/IEC 42001 y pasos prácticos", "html": ess(
"La norma ISO/IEC 42001 dice cómo montar un sistema de gestión de la IA en una organización, como otras normas ISO lo hacen para la calidad o la seguridad. En la práctica, todo se resume en cinco pasos.") + """
<p>La norma <strong>ISO/IEC 42001:2023</strong> establece requisitos para establecer, implementar, mantener y mejorar continuamente un sistema de gestión de la IA dentro de la organización.[[3]]</p>
<ol class="steps">
<li>Definir responsables y casos de uso autorizados.</li>
<li>Documentar datos, supuestos y limitaciones de cada modelo.</li>
<li>Validar antes de usar y monitorear el desempeño después.</li>
<li>Mantener supervisión humana en toda decisión con efectos sobre clientes o reportes.</li>
<li>Revisar periódicamente sesgos y desempeño.</li>
</ol>
""" + deep("""
<p><strong>Ficha del modelo.</strong> Una práctica útil es mantener, para cada modelo, una ficha con su propósito, los datos de entrenamiento y su período, las variables usadas, las métricas de validación, las limitaciones conocidas, el responsable y la fecha de la próxima revisión. Facilita la auditoría y responde a la pregunta del supervisor: «¿por qué el sistema hizo esto?».</p>
<p><strong>Conservación.</strong> Si el modelo influyó en una decisión de debida diligencia o de reporte, conserva la versión, los datos y la salida junto con el expediente, porque los resultados de los análisis se guardan al menos 10 años (art. 43).[[4]]</p>
""")},
# 6 ------------------------------------------------------------------------------------------
{"title": "Uso responsable de la IA generativa", "html": ess(
"Los asistentes de IA sirven para escribir borradores de políticas o materiales de capacitación y para resumir normas públicas. Nunca se les debe dar datos de clientes o de reportes, ni copiar lo que digan sin comprobarlo en la fuente oficial.") + """
<div class="grid-2">
<div class="mini"><h4>Sí</h4><p>Borradores de políticas, guías de capacitación o correos genéricos; resúmenes de normativa pública que luego verificas en la fuente oficial; ideas para estructurar un análisis.</p></div>
<div class="mini"><h4>No</h4><p>Datos de clientes o de reportes en herramientas no autorizadas; citar artículos o cifras sin verificarlos; delegar la decisión de reportar.</p></div>
</div>
<div class="callout warn"><b>Regla de oro</b>La tecnología complementa el criterio profesional; no sustituye la evaluación humana.</div>
<div class="case"><b>Ejemplo</b><p>Un analista pide a un asistente de IA «el artículo de la Ley 155-17 sobre el plazo del ROS». La respuesta cita un plazo y un número de artículo. Antes de usarla, verifica en el texto oficial: el art. 55 fija 5 días hábiles desde que la operación fue realizada o intentada.[[4]]</p></div>
""" + deep("""
<p><strong>Redacción de ROS.</strong> Una herramienta autorizada e interna puede ayudar a ordenar los hechos según el método de las 5W, pero el razonamiento de la sospecha debe ser del analista. La UAF valora los reportes que explican con claridad por qué la operación es sospechosa, algo que solo puede hacer quien analizó el caso.[[6]]</p>
""")},
# 7 ------------------------------------------------------------------------------------------
{"title": "Evaluar un caso de uso", "html": ess(
"Antes de usar un modelo en la operación hay que responder unas pocas preguntas: para qué sirve, con qué datos se entrenó, cómo se mide, quién lo supervisa y qué pasa si falla.") + """
<div class="case"><b>Caso · «El modelo que descarta alertas»</b>
<p>Un proveedor ofrece un modelo que, según promete, «elimina el 70 % de los falsos positivos» cerrando automáticamente las alertas de menor puntaje.</p>
<ol>
<li><strong>Mapear:</strong> el modelo afecta una obligación legal (detectar y reportar operaciones sospechosas).[[4]]</li>
<li><strong>Medir:</strong> pedir pruebas con datos propios: ¿cuántas alertas que terminaron en ROS habría cerrado?</li>
<li><strong>Gobernar:</strong> definir quién aprueba, quién monitorea y con qué periodicidad; documentarlo en una ficha del modelo.[[2,3]]</li>
<li><strong>Gestionar:</strong> en lugar de cierre automático, usarlo para priorizar, con muestreo humano de las alertas de bajo puntaje.</li>
<li><strong>Proteger:</strong> verificar dónde procesa los datos el proveedor y cómo se cumplen el art. 63 y la Ley 172-13.[[4,5]]</li>
</ol>
<p class="verdict yes"><b>Lección:</b> un modelo útil puede adoptarse, pero con supervisión humana, evidencia propia y responsabilidades claras.</p>
</div>
"""},
],
"glossary": [
("Aprendizaje supervisado", "Técnica que aprende de ejemplos etiquetados para predecir o clasificar."),
("Aprendizaje no supervisado", "Técnica que encuentra grupos o anomalías sin etiquetas previas."),
("IA generativa", "Sistemas que producen textos, imágenes u otros contenidos a partir de instrucciones."),
("Alucinación", "Contenido falso generado por una IA con apariencia convincente."),
("Explicabilidad", "Capacidad de entender y explicar por qué un modelo produjo un resultado [[2]]."),
("Deriva del modelo", "Pérdida de desempeño cuando cambian los datos o el contexto."),
("NIST AI RMF", "Marco de gestión de riesgos de IA del NIST: gobernar, mapear, medir y gestionar [[2]]."),
("ISO/IEC 42001", "Norma con requisitos para un sistema de gestión de la IA [[3]]."),
],
"quiz": [
{"q": "¿Qué tipo de IA aprende de casos etiquetados, como alertas confirmadas o descartadas?", "options": ["No supervisada", "Aprendizaje automático supervisado", "IA generativa", "Ninguna"], "answer": 1, "explain": "El aprendizaje supervisado usa ejemplos etiquetados para aprender."},
{"q": "¿Cuál es un riesgo propio de la IA generativa?", "options": ["Que sea demasiado lenta", "Que produzca datos o fuentes inventados con apariencia convincente", "Que no funcione en español", "Que reduzca costos"], "answer": 1, "explain": "Las «alucinaciones» exigen verificar siempre en fuentes oficiales."},
{"q": "¿Por qué no se deben subir datos de un ROS a una herramienta de IA externa no autorizada?", "options": ["Porque es lento", "Porque puede violar la confidencialidad del art. 63 y la protección de datos", "Porque la IA no entiende reportes", "No hay ningún problema"], "answer": 1, "explain": "La reserva de los reportes y la protección de datos personales son obligaciones legales [[4,5]]."},
{"q": "¿Cuáles son las cuatro funciones del NIST AI RMF 1.0?", "options": ["Planear, hacer, verificar, actuar", "Gobernar, mapear, medir y gestionar", "Identificar, proteger, detectar, responder", "Analizar, diseñar, construir, probar"], "answer": 1, "explain": "El marco del NIST organiza la gestión de riesgos de la IA en esas cuatro funciones [[2]]."},
{"q": "¿Cuál de estas es una característica de una IA confiable según el NIST?", "options": ["Ser la más barata", "Ser explicable e interpretable", "Ser secreta", "No tener supervisión"], "answer": 1, "explain": "El AI RMF incluye la explicabilidad e interpretabilidad entre las características de confianza [[2]]."},
{"q": "¿Qué establece la norma ISO/IEC 42001:2023?", "options": ["Las 40 Recomendaciones del GAFI", "Requisitos para un sistema de gestión de la IA en la organización", "El formato del ROS", "Las multas por lavado"], "answer": 1, "explain": "Es la norma de sistemas de gestión de la IA [[3]]."},
{"q": "Un modelo cierra automáticamente alertas de bajo puntaje. ¿Cuál es el principal riesgo?", "options": ["Que el tablero se vea mal", "Que descarte casos que debían reportarse, con riesgo de incumplir el deber de reportar", "Que consuma electricidad", "Ninguno"], "answer": 1, "explain": "No reportar una operación sospechosa es infracción muy grave (art. 69); por eso se requiere supervisión humana [[4]]."},
{"q": "¿Quién conserva la responsabilidad por las decisiones apoyadas en IA?", "options": ["El proveedor del software", "La entidad y sus profesionales", "El modelo", "Nadie"], "answer": 1, "explain": "La IA apoya; la responsabilidad sigue en la organización y en quienes deciden [[1]]."},
{"q": "¿Qué uso de la IA generativa es apropiado?", "options": ["Decidir si enviar un ROS", "Redactar un borrador de guía de capacitación que luego se verifica", "Cargar la base de clientes en una herramienta gratuita", "Citar artículos de ley sin revisarlos"], "answer": 1, "explain": "Es útil para borradores, siempre con verificación y sin datos reservados."},
{"q": "Un asistente de IA indica el plazo del ROS. ¿Qué debe hacer el analista?", "options": ["Usarlo sin revisar", "Verificarlo en el texto oficial de la ley (art. 55: 5 días hábiles)", "Preguntar a otro asistente", "Ignorar la ley"], "answer": 1, "explain": "La información generada debe verificarse en la fuente oficial [[4]]."},
],
}
