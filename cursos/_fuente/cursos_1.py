"""Cursos 01 a 04: fundamentos, marco regulatorio, enfoque basado en riesgos y matrices."""
from fuentes import *  # noqa: F401,F403

COURSES = [
# ---------------------------------------------------------------------------------------------
{
"num": 1, "slug": "fundamentos-prevencion-lavado-de-activos", "tag": "Fundamentos", "level": "Básico", "minutes": 20,
"title": "Fundamentos de prevención de lavado de activos",
"card": "Qué es el lavado, cómo opera y quiénes participan en su prevención.",
"summary": "Comprende qué es el lavado de activos, cómo se mueve el dinero ilícito, en qué se diferencia del financiamiento del terrorismo y qué papel juega cada actor del sistema de prevención dominicano.",
"objectives": [
  "Explicar con tus palabras qué es el lavado de activos y qué es una infracción precedente.",
  "Reconocer las etapas típicas del proceso de lavado en un caso concreto.",
  "Distinguir el lavado de activos del financiamiento del terrorismo y de la proliferación.",
  "Identificar a los actores del sistema de prevención y tu responsabilidad dentro de él.",
],
"sources": [LEY, GAFI40, DGII_BRO, REG, UAF_ROS],
"modules": [
{"title": "Dinero sucio que busca parecer limpio", "html": """
<p>Quien obtiene dinero de un delito enfrenta un problema práctico: no puede usarlo abiertamente sin delatar su origen. El <strong>lavado de activos</strong> es, precisamente, el conjunto de maniobras con las que personas u organizaciones intentan dar apariencia legítima a bienes que provienen de actividades ilícitas.[[1,3]]</p>
<p>La Ley 155-17 no limita el lavado al narcotráfico. Define como <strong>infracción precedente o determinante</strong> aquella que genera bienes susceptibles de ser lavados, enumera una lista amplia —tráfico de drogas, trata de personas, corrupción, delitos tributarios, entre otros— y añade una regla general: también lo es <strong>toda infracción grave sancionable con pena no menor de tres años</strong>.[[1]]</p>
<div class="callout key"><b>Idea clave</b>Sin un delito previo que genere bienes, no hay lavado. Por eso, al evaluar una operación sospechosa siempre conviene preguntarse: ¿de qué posible delito podrían provenir estos fondos?</div>
<p>Este delito es autónomo: la ley lo castiga con penas de hasta 20 años de prisión mayor para quien convierte, transfiere u oculta bienes sabiendo, o debiendo saber, su origen ilícito.[[1]]</p>
"""},
{"title": "Las tres etapas clásicas del proceso", "html": """
<p>Para estudiar el lavado se suele dividir en tres etapas. Son un modelo didáctico: en la vida real pueden superponerse, repetirse o saltarse.[[3]]</p>
<ol class="steps">
<li><strong>Colocación.</strong> El dinero ilícito entra al sistema económico: depósitos, compra de instrumentos, pago de bienes de alto valor o mezcla con ingresos de un negocio real. Es la etapa más vulnerable para el delincuente porque el efectivo todavía está cerca de su origen.</li>
<li><strong>Estratificación (o diversificación).</strong> Se crean capas de transacciones para alejar los fondos de su origen: transferencias entre cuentas y países, compraventas sucesivas, préstamos simulados, sociedades interpuestas.</li>
<li><strong>Integración.</strong> Los fondos regresan a la economía con una explicación aparentemente legal: utilidades de una empresa, venta de un inmueble, premios, herencias o inversiones.</li>
</ol>
<div class="case"><b>Ejemplo ilustrativo</b>
<p>Una red que obtiene efectivo de la extorsión lo deposita en pequeñas sumas en la cuenta de un taller mecánico real (colocación). Desde allí paga «facturas» a tres empresas recién creadas que no tienen empleados ni oficinas (estratificación). Meses después, una de esas empresas compra un local comercial y lo alquila: las rentas parecen un ingreso legítimo (integración).</p>
</div>
"""},
{"title": "Financiamiento del terrorismo y de la proliferación", "html": """
<p>El <strong>financiamiento del terrorismo (FT)</strong> consiste en proveer, recolectar o facilitar fondos o bienes para personas u organizaciones terroristas o para la comisión de actos terroristas. La diferencia esencial con el lavado está en la dirección del dinero:[[1,2]]</p>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th></th><th>Lavado de activos</th><th>Financiamiento del terrorismo</th></tr></thead>
<tbody>
<tr><td>Origen de los fondos</td><td>Siempre ilícito</td><td>Puede ser lícito (donaciones, salarios, negocios) o ilícito</td></tr>
<tr><td>Objetivo</td><td>Ocultar el origen</td><td>Ocultar el destino y la finalidad</td></tr>
<tr><td>Montos típicos</td><td>Suelen ser elevados</td><td>Pueden ser pequeños y difíciles de detectar</td></tr>
</tbody></table></div>
<p>El <strong>financiamiento de la proliferación de armas de destrucción masiva (FPADM)</strong> se refiere a proveer fondos o servicios financieros para desarrollar, adquirir o transportar armas nucleares, químicas o biológicas. Los estándares internacionales exigen, entre otras medidas, aplicar sin demora las sanciones financieras dirigidas que dicta el Consejo de Seguridad de la ONU.[[2]]</p>
"""},
{"title": "Quién hace qué en el sistema dominicano", "html": """
<p>La prevención funciona como una red en la que cada actor cumple un papel distinto:</p>
<div class="grid-2">
<div class="mini"><h4>GAFI y GAFILAT</h4><p>El GAFI emite las 40 Recomendaciones, el estándar internacional en la materia. GAFILAT es el organismo regional que evalúa a los países de Latinoamérica, entre ellos la República Dominicana.[[2]]</p></div>
<div class="mini"><h4>Comité Nacional</h4><p>Órgano de coordinación de las políticas nacionales contra el lavado y el financiamiento del terrorismo.[[1,3]]</p></div>
<div class="mini"><h4>Unidad de Análisis Financiero</h4><p>Ente técnico que recibe y analiza los reportes de los sujetos obligados y produce inteligencia financiera; ejerce además la secretaría técnica del Comité Nacional (art. 91).[[1]]</p></div>
<div class="mini"><h4>Supervisores</h4><p>Regulan y fiscalizan a los sujetos obligados de su sector con una metodología basada en riesgos (por ejemplo, la DGII para los no financieros que le corresponden).[[1,3]]</p></div>
<div class="mini"><h4>Sujetos obligados</h4><p>Entidades financieras y actividades no financieras designadas que deben conocer a sus clientes, detectar operaciones inusuales y reportarlas.[[1]]</p></div>
<div class="mini"><h4>Ministerio Público y tribunales</h4><p>Investigan, persiguen y juzgan. La UAF no tiene facultades punitivas ni pone en movimiento la acción penal.[[5]]</p></div>
</div>
"""},
{"title": "Tu papel en la primera línea", "html": """
<p>La mayoría de los casos se detectan gracias a una persona atenta en el lugar correcto: quien abre la cuenta, emite la póliza, recibe el pago o tramita la venta. Tu aporte concreto es:</p>
<ul>
<li><strong>Conocer al cliente</strong> y entender para qué usará el producto o servicio.</li>
<li><strong>Notar lo que no encaja</strong> con ese perfil: montos, frecuencia, terceros sin relación aparente, prisa injustificada.</li>
<li><strong>Escalar internamente</strong> al oficial de cumplimiento siguiendo el procedimiento de tu entidad, con los hechos documentados.</li>
<li><strong>Guardar reserva</strong>: está prohibido advertir al cliente o a terceros que una operación está siendo analizada o fue reportada.[[1]]</li>
</ul>
<div class="callout tip"><b>En la práctica</b>No necesitas probar un delito para escalar una alerta. Basta con describir objetivamente qué observaste y por qué te pareció inusual; el análisis posterior corresponde a cumplimiento.</div>
"""},
],
"quiz": [
{"q": "¿Qué elemento es indispensable para que exista lavado de activos?", "options": ["Que la operación supere US$15,000", "Que los bienes provengan de una infracción precedente", "Que participe una entidad financiera", "Que el dinero salga del país"], "answer": 1, "explain": "El lavado consiste en dar apariencia legítima a bienes de origen ilícito; sin una infracción precedente que los genere, no hay lavado. El monto o el sector no son requisitos del delito [[1]]."},
{"q": "Según la Ley 155-17, además de los delitos enumerados, ¿qué otra infracción puede ser precedente del lavado?", "options": ["Cualquier falta administrativa", "Toda infracción grave sancionable con pena no menor de tres años", "Solo los delitos cometidos en el extranjero", "Únicamente el narcotráfico"], "answer": 1, "explain": "La definición de infracción precedente incluye una cláusula general: toda infracción grave con pena no menor de tres años [[1]]."},
{"q": "Una red compra varios inmuebles a nombre de sociedades sin actividad y luego los revende entre ellas. ¿Qué etapa describe mejor esta conducta?", "options": ["Colocación", "Estratificación", "Integración", "Ninguna, es una operación inmobiliaria normal"], "answer": 1, "explain": "Las compraventas sucesivas entre sociedades interpuestas crean capas que alejan los fondos de su origen: es la estratificación."},
{"q": "¿Cuál es una diferencia clave entre el lavado de activos y el financiamiento del terrorismo?", "options": ["El financiamiento del terrorismo siempre usa dinero ilícito", "En el financiamiento del terrorismo los fondos pueden tener origen lícito y lo que se oculta es su destino", "El lavado solo ocurre con montos pequeños", "No existe diferencia práctica"], "answer": 1, "explain": "En el FT el dinero puede venir de fuentes lícitas; lo relevante es su destino y finalidad. En el lavado, el origen siempre es ilícito [[2]]."},
{"q": "¿Qué institución recibe y analiza los reportes de los sujetos obligados en la República Dominicana?", "options": ["El Ministerio Público", "La Unidad de Análisis Financiero (UAF)", "La Policía Nacional", "El GAFI"], "answer": 1, "explain": "La UAF es el ente técnico que recibe y analiza los reportes y produce inteligencia financiera (art. 91 de la Ley 155-17) [[1]]."},
{"q": "Un cajero nota que un cliente fracciona depósitos en efectivo. ¿Cuál es la actuación correcta?", "options": ["Preguntarle si está lavando dinero", "Escalar internamente al oficial de cumplimiento, con los hechos, y guardar reserva", "Ignorarlo porque cada depósito es pequeño", "Publicarlo en el chat del equipo"], "answer": 1, "explain": "La primera línea documenta y escala por el canal interno. Revelar al cliente o a terceros que se analiza una operación está prohibido [[1]]."},
],
},
# ---------------------------------------------------------------------------------------------
{
"num": 2, "slug": "marco-regulatorio-ley-155-17", "tag": "Regulación", "level": "Intermedio", "minutes": 30,
"title": "Marco regulatorio dominicano y Ley 155-17",
"card": "La ley, su reglamento, los sujetos obligados, sus deberes y el régimen de sanciones.",
"summary": "Recorre la arquitectura normativa dominicana contra el lavado de activos: quiénes son sujetos obligados, qué deben hacer, qué plazos y umbrales aplican y qué consecuencias tiene incumplir.",
"objectives": [
  "Ubicar la Ley 155-17, su reglamento y las normas sectoriales dentro del sistema.",
  "Identificar si una actividad es sujeto obligado financiero o no financiero.",
  "Enumerar las obligaciones centrales del programa de cumplimiento.",
  "Reconocer los tipos de infracciones administrativas y sus rangos de sanción.",
],
"sources": [LEY, REG, GAFI40, DGII_N01, UAF_ROS, DGII_BRO, CONCLAFIT_2024, CONCLAFIT_2025_01, CONCLAFIT_2025_02],
"modules": [
{"title": "La arquitectura normativa", "html": """
<p>El marco dominicano se construye en capas que se complementan:</p>
<ul>
<li><strong>Ley 155-17</strong> (1 de junio de 2017): tipifica el lavado y el financiamiento del terrorismo, define a los sujetos obligados y sus deberes, y fija las sanciones. Sustituyó a la Ley 72-02.[[1]]</li>
<li><strong>Decreto 408-17</strong>: reglamento de aplicación que desarrolla aspectos como la información mínima del beneficiario final, la forma de los reportes y el plazo para responder requerimientos de la UAF.[[2,5]]</li>
<li><strong>Normas sectoriales</strong> de cada supervisor, que adaptan las obligaciones al sector (por ejemplo, la Norma General 01-2018 de la DGII para ciertos no financieros).[[4]]</li>
<li><strong>Estándares internacionales</strong>: las 40 Recomendaciones del GAFI, que inspiran la legislación y sirven de referencia en las evaluaciones del país.[[3]]</li>
</ul>
<div class="callout tip"><b>En la práctica</b>Cuando una norma sectorial es más exigente que la ley, el sujeto obligado debe cumplir ambas. Mantén siempre a mano la normativa de tu supervisor.</div>
"""},
{"title": "¿Quiénes están obligados?", "html": """
<p>La ley distingue dos grandes grupos.[[1]]</p>
<div class="grid-2">
<div class="mini"><h4>Sujetos obligados financieros (art. 32)</h4><p>Entidades de intermediación financiera, intermediarios de valores y puestos de bolsa, agentes de cambio y remesadoras, fiduciarias, cooperativas de ahorro y crédito, compañías de seguros y corredores, administradoras de fondos, titularizadoras, depósito centralizado de valores, entre otros.</p></div>
<div class="mini"><h4>Sujetos obligados no financieros (art. 33)</h4><p>Casinos, juegos de azar, loterías y apuestas; factoraje; agentes inmobiliarios en compraventa; comerciantes de metales y piedras preciosas; abogados, notarios y contadores en ciertas actividades; comerciantes habituales de vehículos, armas, barcos y aviones; casas de empeño; y empresas constructoras.</p></div>
</div>
<div class="callout warn"><b>Atención</b>Para abogados, notarios y contadores la obligación aplica cuando realizan determinadas actividades por cuenta de clientes (compraventa de inmuebles, administración de fondos, creación de sociedades, entre otras), no a toda su práctica profesional.</div>
<div class="callout key"><b>Novedad 2025: empresas constructoras</b>El CONCLAFIT aclaró, mediante la Resolución CONCLAFIT-2025-02 (26 de noviembre de 2025), que las empresas constructoras del literal h) del art. 33 solo son sujetos obligados no financieros cuando intervienen en operaciones de compra y venta de bienes raíces, como compradoras o vendedoras, en línea con el enfoque basado en riesgos.[[9]]</div>
"""},
{"title": "Las obligaciones que no pueden faltar", "html": """
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Obligación</th><th>Lo esencial</th><th>Base</th></tr></thead>
<tbody>
<tr><td>Programa de cumplimiento</td><td>Basado en riesgos; incluye políticas de evaluación y mitigación, estándares de contratación y capacitación del personal, régimen disciplinario, código de ética y auditoría externa.</td><td>Art. 34</td></tr>
<tr><td>Oficial de cumplimiento</td><td>Ejecutivo de alto nivel con capacidad técnica; vigila el programa y es enlace con la UAF y el supervisor.</td><td>Art. 44</td></tr>
<tr><td>Debida diligencia</td><td>Basada en riesgos; identificar y verificar al cliente y al beneficiario final y monitorear la relación.</td><td>Arts. 36 a 42</td></tr>
<tr><td>Conservación de registros</td><td>Al menos 10 años después de terminada la relación o la transacción ocasional.</td><td>Art. 43</td></tr>
<tr><td>Transacciones en efectivo</td><td>Registrar y reportar las que igualen o superen US$15,000 (US$3,000 en casinos).</td><td>Arts. 52 a 54</td></tr>
<tr><td>Operaciones sospechosas</td><td>Reportar a la UAF dentro de 5 días hábiles de realizada o intentada la operación.</td><td>Art. 55</td></tr>
<tr><td>Reserva</td><td>No revelar a terceros que se reportó o se examina una operación.</td><td>Art. 63</td></tr>
</tbody></table></div>
<p>Además, cuando la UAF solicita información, el sujeto obligado debe entregarla en un plazo no mayor de <strong>10 días laborables</strong>, o en uno menor si la UAF lo dispone por urgencia.[[2,5]]</p>
"""},
{"title": "Límites al uso del efectivo (art. 64)", "html": """
<p>La ley prohíbe liquidar o aceptar en efectivo, por encima de ciertos montos, operaciones como la compra de inmuebles, vehículos, joyas y obras de arte, juegos de azar o participaciones societarias. Los notarios y registradores deben abstenerse de instrumentar esas operaciones si no se acredita el medio de pago.[[1]]</p>
<div class="callout warn"><b>Los umbrales cambiaron</b>El texto original de la ley fijaba los montos en pesos, pero el propio artículo permite que el Comité Nacional (CONCLAFIT) los actualice. La Resolución CONCLAFIT-2025-01 los aumentó; por ejemplo, para premios y demás operaciones de los literales d) a g), su nota aclaratoria del 10 de diciembre de 2025 precisa que el límite es de <strong>RD$400,000</strong>. Antes de aplicar cualquier límite, consulta el texto completo de esa resolución.[[1,8]]</div>
<p>Incumplir el art. 64 es una infracción administrativa <strong>muy grave</strong>.[[1]]</p>
"""},
{"title": "Consecuencias del incumplimiento", "html": """
<p>La ley prevé dos vías de responsabilidad que pueden coexistir.[[1]]</p>
<h3>Responsabilidad penal</h3>
<p>El lavado de activos se sanciona con penas que llegan hasta 10 a 20 años de prisión mayor, multas de 200 a 400 salarios mínimos, decomiso e inhabilitación, según la conducta.[[1]]</p>
<h3>Responsabilidad administrativa del sujeto obligado</h3>
<p>La ley ordena al CONCLAFIT actualizar las multas cada tres años según el Índice de Precios al Consumidor (art. 89, num. 15). Los montos vigentes son los de la <strong>Resolución CONCLAFIT-2024-01</strong> (3 de julio de 2024):[[1,7]]</p>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Tipo de infracción</th><th>Ejemplos</th><th>Sector financiero (art. 74)</th><th>No financiero (art. 75)</th></tr></thead>
<tbody>
<tr><td>Muy grave (art. 69)</td><td>No reportar operaciones sospechosas; no colaborar con la UAF; incumplir el art. 64; fallas graves de debida diligencia o de registros</td><td>RD$6,962,014 a RD$13,924,025</td><td>RD$2,784,806 a RD$5,569,610</td></tr>
<tr><td>Grave (art. 70)</td><td>No enviar reportes periódicos; no designar oficial de cumplimiento; no tener manual, auditoría o capacitación</td><td>RD$3,481,008 a RD$6,962,012</td><td>RD$1,392,404 a RD$2,784,805</td></tr>
<tr><td>Leve (art. 71)</td><td>Retrasos en entregar información o reportes</td><td>RD$1,392,402 a RD$3,481,006</td><td>RD$417,721 a RD$1,392,402</td></tr>
</tbody></table></div>
<p class="note-small">Montos originales de la ley: de RD$1,000,000 a RD$10,000,000 (financiero) y de RD$300,000 a RD$4,000,000 (no financiero), según la gravedad.</p>
<div class="callout key"><b>Protección al que cumple</b>Los sujetos obligados y su personal no incurren en responsabilidad civil, administrativa ni penal por reportar de buena fe a la UAF o informar a las autoridades competentes (art. 58).[[1]]</div>
"""},
],
"quiz": [
{"q": "¿Qué norma sustituyó la Ley 155-17?", "options": ["La Ley 183-02", "La Ley 72-02", "La Ley 267-08", "El Decreto 408-17"], "answer": 1, "explain": "La Ley 155-17 derogó y sustituyó la Ley 72-02 sobre lavado de activos [[1]]."},
{"q": "Un notario que instrumenta compraventas de inmuebles por cuenta de clientes es:", "options": ["Sujeto obligado financiero", "Sujeto obligado no financiero, en esas actividades", "No es sujeto obligado", "Supervisor"], "answer": 1, "explain": "El art. 33 incluye a abogados, notarios y contadores cuando realizan actividades como la compraventa de inmuebles por cuenta de clientes [[1]]."},
{"q": "¿Durante cuánto tiempo, como mínimo, deben conservarse los registros de debida diligencia y transacciones?", "options": ["5 años", "10 años después de terminada la relación o transacción", "Mientras dure la relación", "2 años"], "answer": 1, "explain": "El art. 43 exige conservar los registros al menos 10 años después de terminada la relación comercial o la transacción ocasional [[1]]."},
{"q": "¿Cuál es el plazo para remitir un Reporte de Operación Sospechosa a la UAF?", "options": ["24 horas", "5 días hábiles después de realizada o intentada la operación", "Los primeros 10 días del mes siguiente", "30 días calendario"], "answer": 1, "explain": "El art. 55 fija 5 días hábiles contados desde que la operación fue realizada o intentada [[1]]."},
{"q": "No designar oficial de cumplimiento se clasifica como infracción:", "options": ["Leve", "Grave", "Muy grave", "No es infracción"], "answer": 1, "explain": "El art. 70 incluye entre las infracciones graves no designar oficial de cumplimiento [[1]]."},
{"q": "La UAF solicita información sobre un cliente. Salvo que disponga un plazo menor, ¿en cuánto tiempo debe responder el sujeto obligado?", "options": ["48 horas", "No mayor de 10 días laborables", "30 días", "Cuando el cliente lo autorice"], "answer": 1, "explain": "El reglamento establece un plazo no mayor de 10 días laborables, o menor si la UAF lo dispone por urgencia [[2]]."},
{"q": "¿Qué instrumento actualizó en 2024 los montos de las multas administrativas de los arts. 74 y 75?", "options": ["Un decreto presidencial", "La Resolución CONCLAFIT-2024-01, indexando por el Índice de Precios al Consumidor", "Una circular de la UAF", "No se han actualizado"], "answer": 1, "explain": "La ley encarga al CONCLAFIT actualizar las multas cada tres años según el IPC; la Resolución CONCLAFIT-2024-01 fijó los montos vigentes [[1,7]]."},
{"q": "Un empleado reporta de buena fe una operación sospechosa y luego el cliente lo amenaza con demandarlo. Según la ley:", "options": ["El empleado responde civilmente", "La ley lo exime de responsabilidad civil, administrativa y penal por reportar", "Debe retirar el reporte", "Solo está protegido si el cliente es condenado"], "answer": 1, "explain": "El art. 58 exime de responsabilidad a quienes reportan a la UAF o informan a las autoridades en cumplimiento de la ley [[1]]."},
],
},
# ---------------------------------------------------------------------------------------------
{
"num": 3, "slug": "enfoque-basado-en-riesgos", "tag": "Riesgos", "level": "Intermedio", "minutes": 25,
"title": "Enfoque basado en riesgos",
"card": "Cómo concentrar los recursos donde el riesgo es mayor, con criterio y evidencia.",
"summary": "Aprende a aplicar el enfoque basado en riesgos: identificar amenazas y vulnerabilidades, medir el riesgo inherente, aplicar controles proporcionales y monitorear el riesgo residual.",
"objectives": [
  "Explicar qué exige el enfoque basado en riesgos y por qué es la base del sistema.",
  "Diferenciar riesgo inherente, controles y riesgo residual.",
  "Aplicar los cuatro factores mínimos de riesgo previstos en la ley.",
  "Evitar los errores más comunes al implementar el enfoque.",
],
"sources": [GAFI40, LEY, GAFI_RBA, ISO_31000, DGII_N01],
"modules": [
{"title": "Recursos limitados, riesgos distintos", "html": """
<p>Ninguna entidad puede revisar con la misma intensidad cada cliente y cada operación. El <strong>enfoque basado en riesgos (EBR)</strong> propone algo sensato: entender dónde está el riesgo y aplicar medidas más intensas donde es mayor y más simples donde es menor.[[1]]</p>
<p>Es la primera de las Recomendaciones del GAFI y la Ley 155-17 lo adopta en varios niveles: el programa de cumplimiento debe ser basado en riesgos (art. 34), la debida diligencia también (art. 36), y los supervisores deben supervisar con esa misma metodología.[[1,2]]</p>
<div class="callout key"><b>Idea clave</b>El EBR no significa hacer menos: significa hacer lo correcto en el lugar correcto, y poder demostrar por qué.</div>
"""},
{"title": "Amenaza, vulnerabilidad y consecuencia", "html": """
<p>Tres conceptos ayudan a pensar el riesgo con orden:[[3]]</p>
<ul>
<li><strong>Amenaza</strong>: personas o actividades que pueden causar daño (organizaciones criminales, sus fondos, sus métodos).</li>
<li><strong>Vulnerabilidad</strong>: debilidades que la amenaza puede aprovechar (un producto que acepta efectivo sin límites, controles manuales, personal sin capacitación).</li>
<li><strong>Consecuencia</strong>: el impacto si ocurre (sanciones, daño reputacional, pérdidas, daño a la sociedad).</li>
</ul>
<p>A partir de ahí se distinguen:</p>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Concepto</th><th>Pregunta que responde</th></tr></thead>
<tbody>
<tr><td>Riesgo inherente</td><td>¿Cuánto riesgo existe por la naturaleza del cliente, producto, zona o canal, antes de aplicar controles?</td></tr>
<tr><td>Controles</td><td>¿Qué medidas lo reducen y qué tan eficaces son en la práctica?</td></tr>
<tr><td>Riesgo residual</td><td>¿Cuánto riesgo queda después de los controles? ¿Está dentro del apetito de riesgo aprobado?</td></tr>
</tbody></table></div>
"""},
{"title": "Los cuatro factores mínimos", "html": """
<p>La ley exige considerar, como mínimo, cuatro factores de riesgo (art. 37).[[2]] Algunos ejemplos de lo que cada uno puede incluir:</p>
<div class="grid-2">
<div class="mini"><h4>Clientes</h4><p>Actividad económica, tipo de persona, condición de PEP, estructura de propiedad, antigüedad de la relación, comportamiento transaccional.</p></div>
<div class="mini"><h4>Productos y servicios</h4><p>Uso de efectivo, posibilidad de anonimato, rapidez de movimiento de fondos, pagos de terceros, rescates anticipados.</p></div>
<div class="mini"><h4>Áreas geográficas</h4><p>Jurisdicciones señaladas por el GAFI, zonas fronterizas o con alta incidencia delictiva, origen y destino de transferencias.</p></div>
<div class="mini"><h4>Canales de distribución</h4><p>Presencial, digital sin contacto, intermediarios o agentes, corresponsales.</p></div>
</div>
<p>Las personas expuestas políticamente y las transacciones con jurisdicciones identificadas por el GAFI son, por mandato de ley, factores de alto riesgo (art. 46).[[2]]</p>
"""},
{"title": "El ciclo de gestión", "html": """
<p>La ley describe la gestión del riesgo en fases de identificación, medición, monitoreo y mitigación (art. 36), una lógica coherente con las directrices generales de la norma ISO 31000.[[2,4]]</p>
<ol class="steps">
<li><strong>Identificar</strong> los eventos de riesgo de la entidad: cómo podrían usarla para lavar dinero o financiar el terrorismo.</li>
<li><strong>Medir</strong> su probabilidad e impacto con una escala definida y documentada.</li>
<li><strong>Mitigar</strong> con controles proporcionales: debida diligencia ampliada, límites, aprobaciones, monitoreo reforzado.</li>
<li><strong>Monitorear</strong> que los controles funcionen y que la evaluación siga vigente; actualizarla ante nuevos productos, canales o tipologías.</li>
</ol>
<div class="callout tip"><b>En la práctica</b>Documenta la metodología y las decisiones. Ante el supervisor, una calificación sin sustento vale poco; un criterio razonado y aplicado de forma consistente vale mucho.</div>
"""},
{"title": "Errores que conviene evitar", "html": """
<ul>
<li><strong>Buscar «riesgo cero».</strong> El objetivo es gestionar el riesgo dentro de un apetito aprobado, no eliminarlo.</li>
<li><strong>Rechazar categorías completas de clientes sin análisis.</strong> El EBR pide evaluar caso a caso; excluir sectores enteros por comodidad puede empujar a personas hacia canales informales.[[3]]</li>
<li><strong>Matrices que nadie actualiza.</strong> Una evaluación de hace años no refleja productos nuevos ni tipologías emergentes.</li>
<li><strong>Calificar sin datos.</strong> Las ponderaciones deben apoyarse en información de la propia entidad y en fuentes externas confiables.</li>
<li><strong>Confundir alto riesgo con sospecha.</strong> Un cliente de alto riesgo exige más diligencia, no un reporte automático.</li>
</ul>
"""},
],
"quiz": [
{"q": "¿Qué describe mejor el enfoque basado en riesgos?", "options": ["Aplicar los mismos controles a todos los clientes", "Concentrar medidas más intensas donde el riesgo es mayor y más simples donde es menor", "Eliminar todo cliente de riesgo", "Revisar solo a los clientes nuevos"], "answer": 1, "explain": "El EBR adapta la intensidad de las medidas al nivel de riesgo identificado; es la Recomendación 1 del GAFI [[1]]."},
{"q": "El riesgo que existe antes de aplicar cualquier control se denomina:", "options": ["Residual", "Inherente", "Aceptado", "Reputacional"], "answer": 1, "explain": "El riesgo inherente es el que se deriva de la naturaleza del cliente, producto, zona o canal, antes de los controles."},
{"q": "¿Cuáles son los cuatro factores mínimos de riesgo previstos en el art. 37 de la Ley 155-17?", "options": ["Clientes, productos y servicios, áreas geográficas y canales de distribución", "Edad, sexo, nacionalidad y profesión", "Monto, moneda, fecha y sucursal", "Auditoría, cumplimiento, riesgo y legal"], "answer": 0, "explain": "La ley exige considerar clientes, productos y servicios, áreas geográficas y canales de distribución [[2]]."},
{"q": "Una entidad decide no aceptar a ningún cliente de un sector económico completo sin evaluar casos individuales. Desde el EBR esto es:", "options": ["La mejor práctica", "Un error frecuente: el EBR pide evaluar y gestionar, no excluir por categoría sin análisis", "Obligatorio por ley", "Irrelevante"], "answer": 1, "explain": "El EBR busca gestionar el riesgo con análisis; las exclusiones masivas sin evaluación no son lo que pide el estándar [[3]]."},
{"q": "Un cliente fue calificado de alto riesgo. ¿Qué corresponde?", "options": ["Enviar un ROS de inmediato", "Aplicar medidas de debida diligencia más intensas y monitoreo reforzado", "Cerrar la cuenta sin más", "Nada, la calificación es informativa"], "answer": 1, "explain": "Alto riesgo implica mayor diligencia; el reporte procede solo si, tras el análisis, surge una sospecha."},
{"q": "¿Qué ocurre con la evaluación de riesgos cuando la entidad lanza un nuevo producto digital?", "options": ["Nada, se revisa cada cinco años", "Debe actualizarse para identificar y mitigar los nuevos riesgos", "Solo se informa al cliente", "Se transfiere el riesgo al proveedor tecnológico"], "answer": 1, "explain": "El ciclo de gestión incluye monitorear y actualizar la evaluación ante cambios relevantes como nuevos productos o canales [[2,4]]."},
],
},
# ---------------------------------------------------------------------------------------------
{
"num": 4, "slug": "matrices-de-evaluacion-y-segmentacion", "tag": "Riesgos", "level": "Avanzado", "minutes": 30,
"title": "Matrices de evaluación y segmentación",
"card": "Diseño de matrices de riesgo de clientes, ponderaciones y segmentación.",
"summary": "Diseña y aplica una matriz de riesgo de clientes: variables, escalas, ponderaciones, niveles de riesgo y segmentación, con un ejemplo resuelto paso a paso.",
"objectives": [
  "Diferenciar la autoevaluación de riesgos de la entidad de la matriz de riesgo de clientes.",
  "Construir una matriz con variables, escalas y ponderaciones justificadas.",
  "Calcular el nivel de riesgo de un cliente y vincularlo a medidas de debida diligencia.",
  "Usar la segmentación para definir perfiles y umbrales de monitoreo.",
],
"sources": [LEY, GAFI40, GAFI_RBA, ISO_31000],
"modules": [
{"title": "Dos matrices, dos propósitos", "html": """
<p>En la práctica se habla de «la matriz», pero conviene distinguir dos herramientas:</p>
<div class="grid-2">
<div class="mini"><h4>Autoevaluación de riesgos de la entidad</h4><p>Identifica cómo podría la entidad ser utilizada para lavar activos, mide esos eventos y evalúa sus controles. Orienta el programa de cumplimiento completo.</p></div>
<div class="mini"><h4>Matriz de riesgo de clientes</h4><p>Asigna a cada cliente un nivel de riesgo a partir de sus características. Decide el tipo de debida diligencia y la intensidad del monitoreo.</p></div>
</div>
<p>Ambas responden al mandato de gestionar el riesgo considerando, como mínimo, clientes, productos y servicios, áreas geográficas y canales (art. 37).[[1]]</p>
"""},
{"title": "Cómo se construye una matriz de clientes", "html": """
<ol class="steps">
<li><strong>Elegir variables por factor.</strong> Por ejemplo: actividad económica y condición de PEP (cliente); producto contratado (producto); país y provincia (geografía); canal de vinculación (canal).</li>
<li><strong>Definir una escala</strong> para cada variable, por ejemplo de 1 (bajo) a 5 (alto), con criterios escritos para asignar cada valor.</li>
<li><strong>Asignar ponderaciones</strong> que reflejen el peso relativo de cada factor según la realidad de la entidad.</li>
<li><strong>Calcular el puntaje</strong> como promedio ponderado y traducirlo a niveles (bajo, medio, alto).</li>
<li><strong>Vincular cada nivel a medidas</strong>: tipo de debida diligencia, frecuencia de actualización y umbrales de monitoreo.</li>
</ol>
<div class="callout warn"><b>Reglas que prevalecen</b>Algunas condiciones fijan el nivel con independencia del puntaje. Por ejemplo, la ley ordena tratar a las PEP como clientes de alto riesgo (art. 46); la matriz debe reflejarlo con una regla de prevalencia.[[1]]</div>
"""},
{"title": "Ejemplo resuelto", "html": """
<p>Las cifras siguientes son <strong>ilustrativas</strong>: cada entidad debe definir y justificar las suyas.</p>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Factor</th><th>Variable del cliente</th><th>Valor (1-5)</th><th>Peso</th><th>Aporte</th></tr></thead>
<tbody>
<tr><td>Cliente</td><td>Comercio de vehículos usados, persona jurídica con 2 socios</td><td>4</td><td>40 %</td><td>1.60</td></tr>
<tr><td>Producto</td><td>Cuenta corriente con alto uso de efectivo</td><td>4</td><td>25 %</td><td>1.00</td></tr>
<tr><td>Geografía</td><td>Opera en una provincia fronteriza</td><td>3</td><td>20 %</td><td>0.60</td></tr>
<tr><td>Canal</td><td>Vinculación presencial</td><td>1</td><td>15 %</td><td>0.15</td></tr>
<tr><td colspan="4"><strong>Puntaje total</strong></td><td><strong>3.35</strong></td></tr>
</tbody></table></div>
<p>Si la política define <em>bajo</em> hasta 2.00, <em>medio</em> de 2.01 a 3.20 y <em>alto</em> desde 3.21, este cliente es de <strong>riesgo alto</strong>: corresponde debida diligencia ampliada, identificar a los beneficiarios finales, documentar el origen de los fondos y actualizar su información con mayor frecuencia.</p>
"""},
{"title": "Segmentación: comparar con iguales", "html": """
<p>Una alerta tiene sentido cuando se compara con lo esperado. La <strong>segmentación</strong> agrupa a los clientes con características similares (actividad, ingresos, volumen transaccional, zona) para definir qué es «normal» en cada grupo y detectar desviaciones.[[3]]</p>
<ul>
<li><strong>Por reglas</strong>: segmentos definidos por criterios de negocio (por ejemplo, asalariados con ingresos hasta cierto monto).</li>
<li><strong>Estadística</strong>: percentiles o desviaciones respecto al promedio del segmento.</li>
<li><strong>Analítica avanzada</strong>: técnicas de agrupamiento que descubren segmentos a partir de los datos; requieren validación y explicación.</li>
</ul>
<div class="case"><b>Ejemplo</b><p>En el segmento «empleados privados con ingresos hasta RD$40,000», casi nadie recibe más de diez transferencias de terceros al mes. Un cliente de ese segmento que recibe sesenta merece revisión, aunque cada transferencia sea pequeña.</p></div>
"""},
{"title": "Gobierno de la matriz", "html": """
<ul>
<li><strong>Metodología escrita y aprobada</strong> por la instancia que corresponda, con la justificación de variables y ponderaciones.</li>
<li><strong>Calibración</strong>: revisar si la distribución de clientes por nivel es razonable y si los niveles altos concentran las alertas relevantes.</li>
<li><strong>Pruebas retrospectivas</strong>: verificar si los clientes reportados o con hallazgos estaban bien calificados.</li>
<li><strong>Actualización</strong> ante nuevos productos, cambios normativos o tipologías, y recálculo cuando cambian los datos del cliente.</li>
<li><strong>Trazabilidad</strong>: poder reconstruir por qué un cliente obtuvo su calificación en una fecha dada.[[4]]</li>
</ul>
"""},
],
"quiz": [
{"q": "¿Para qué sirve principalmente la matriz de riesgo de clientes?", "options": ["Para calcular comisiones", "Para asignar a cada cliente un nivel de riesgo que determina su debida diligencia y monitoreo", "Para reemplazar la evaluación de la entidad", "Para decidir qué reportar a la UAF sin análisis"], "answer": 1, "explain": "La matriz de clientes traduce características en un nivel de riesgo que define medidas de debida diligencia y monitoreo."},
{"q": "En el ejemplo resuelto, ¿por qué el cliente resultó de riesgo alto?", "options": ["Porque usa el canal presencial", "Porque su puntaje ponderado (3.35) superó el umbral definido para alto (3.21)", "Porque es persona jurídica", "Porque todos los clientes con cuenta corriente son de alto riesgo"], "answer": 1, "explain": "El nivel se obtiene comparando el puntaje ponderado con los rangos definidos en la política."},
{"q": "Un cliente obtiene puntaje bajo, pero es PEP. ¿Qué nivel de riesgo corresponde?", "options": ["Bajo, porque manda el puntaje", "Alto, por la regla de prevalencia que refleja el art. 46", "Medio, como promedio", "No se califica"], "answer": 1, "explain": "La ley ordena tratar a las PEP como clientes de alto riesgo; la matriz debe incorporar esa regla [[1]]."},
{"q": "¿Qué aporta la segmentación al monitoreo?", "options": ["Permite definir lo esperado en grupos similares y detectar desviaciones", "Reemplaza la debida diligencia", "Sirve solo para mercadeo", "Elimina las alertas"], "answer": 0, "explain": "Comparar a un cliente con sus pares permite identificar comportamientos fuera de lo normal [[3]]."},
{"q": "¿Qué es una prueba retrospectiva de la matriz?", "options": ["Repetir el cálculo con otra calculadora", "Verificar si los clientes con hallazgos o reportes estaban bien calificados", "Eliminar clientes antiguos", "Enviar la matriz al cliente"], "answer": 1, "explain": "La revisión retrospectiva ayuda a calibrar variables y ponderaciones con evidencia de la propia entidad."},
{"q": "¿Qué práctica fortalece la trazabilidad de la matriz?", "options": ["Cambiar ponderaciones sin documentarlo", "Poder reconstruir por qué un cliente obtuvo su calificación en una fecha determinada", "Guardar solo el resultado final", "Usar criterios distintos en cada sucursal"], "answer": 1, "explain": "La trazabilidad permite explicar y defender las calificaciones ante auditoría y supervisión [[4]]."},
],
},
]
