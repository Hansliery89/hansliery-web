"""Curso 01 · Fundamentos de prevención de lavado de activos."""
from fuentes import *  # noqa: F401,F403
from capas import ess, deep

# Fuentes: 1 LEY · 2 GAFI40 · 3 DGII_BRO · 4 REG · 5 UAF_ROS · 6 DEC_407
COURSE = {
"num": 1, "slug": "fundamentos-prevencion-lavado-de-activos", "tag": "Fundamentos", "level": "Básico → Profesional", "minutes": 50,
"title": "Fundamentos de prevención de lavado de activos",
"card": "Qué es el lavado, cómo opera y quiénes participan en su prevención.",
"summary": "Comprende qué es el lavado de activos, cómo se mueve el dinero ilícito, qué conductas castiga la Ley 155-17, en qué se diferencia del financiamiento del terrorismo y qué papel juega cada actor del sistema de prevención dominicano, incluido tú.",
"objectives": [
  "Explicar con tus palabras qué es el lavado de activos y qué es una infracción precedente.",
  "Reconocer las etapas típicas del proceso de lavado en un caso concreto.",
  "Identificar las conductas que la Ley 155-17 sanciona y por qué el desconocimiento deliberado no protege.",
  "Distinguir el lavado de activos del financiamiento del terrorismo y de la proliferación.",
  "Ubicar a los actores del sistema de prevención y tu responsabilidad dentro de él.",
],
"sources": [LEY, GAFI40, DGII_BRO, REG, UAF_ROS, DEC_407],
"modules": [
# 1 ------------------------------------------------------------------------------------------
{"title": "Dinero sucio que busca parecer limpio", "html": ess(
"Quien gana dinero con un delito no puede gastarlo a la vista sin delatarse. Lavar activos es disfrazar ese dinero para que parezca ganado de forma honrada: un negocio, una herencia, un premio. Prevenirlo es tarea de todos, porque el lavado necesita la ayuda —consciente o no— de personas y empresas legítimas.") + """
<p>La Ley 155-17 define el <strong>lavado de activos</strong> como el proceso mediante el cual personas físicas o jurídicas y organizaciones criminales buscan dar <strong>apariencia legítima</strong> a bienes o activos ilícitos provenientes de los delitos precedentes señalados en la propia ley (art. 2, num. 15).[[1]]</p>
<p>La palabra «activos» es amplia: la ley incluye dinero, valores, títulos, bienes muebles e inmuebles, tangibles o intangibles, y los documentos o instrumentos —incluso electrónicos o digitales— que evidencien su titularidad (art. 2, num. 1).[[1]] Se puede lavar con un apartamento, un vehículo, joyas, acciones de una empresa o un saldo digital.</p>
<h3>Sin delito previo no hay lavado</h3>
<p>La ley llama <strong>infracción precedente o determinante</strong> a la que genera los bienes que luego se lavan. Su lista es extensa: tráfico de drogas, terrorismo y su financiamiento, trata y tráfico de personas, secuestro, extorsión, corrupción y soborno, delito tributario, estafa agravada, contrabando, delitos contra la propiedad intelectual y el medio ambiente, testaferrato, sicariato, enriquecimiento no justificado, falsificación de documentos públicos, delitos financieros, crímenes y delitos de alta tecnología y manipulación del mercado, entre otros. Además, incluye una cláusula general: es precedente <strong>toda infracción grave sancionable con pena no menor de tres años</strong> (art. 2, num. 11).[[1]]</p>
<div class="callout key"><b>Idea clave</b>Al evaluar una operación extraña, la pregunta útil no es «¿esto es raro?», sino «¿de qué posible delito podrían provenir estos fondos?». Esa conexión es la que convierte una rareza en una posible sospecha.</div>
<h3>Un delito con vida propia</h3>
<p>El lavado se investiga y juzga como un hecho <strong>autónomo</strong>: no hace falta que el delito precedente haya sido juzgado antes, y no importa que se haya cometido en otro país (art. 6).[[1]] Por eso una entidad dominicana puede ser utilizada para lavar el producto de un delito ocurrido en el extranjero.</p>
""" + deep("""
<p><strong>Infracción grave y pena imponible.</strong> La ley define la infracción grave como la sancionada con pena imponible no menor de tres años que genera recursos susceptibles de lavado (art. 2, num. 12), y precisa que la pena imponible es la establecida en el tipo penal, independiente de la que finalmente imponga el juez (art. 2, num. 18).[[1]] Por tanto, para saber si un delito es precedente se mira la pena prevista en la ley, no la condena concreta.</p>
<p><strong>Delito tributario.</strong> El reglamento fija un umbral: el delito tributario se considera precedente cuando los montos envueltos igualan o superan 700 salarios mínimos promedio del sector privado no sectorizado durante un ejercicio fiscal, salvo reincidencia en la misma conducta después de una auditoría, notificación o advertencia de la DGII (Decreto 408-17, art. 47).[[4]]</p>
<p><strong>Tentativa.</strong> La tentativa de las infracciones de la ley se castiga como la infracción misma; y si la tentativa de un delito precedente genera algún bien, ese bien se reputa susceptible de lavado (art. 11).[[1]]</p>
<p><strong>Irretroactividad.</strong> Los nuevos delitos precedentes y las nuevas infracciones administrativas de la Ley 155-17 solo son perseguibles cuando se cometieron después de su entrada en vigencia (Decreto 408-17, art. 46).[[4]]</p>
""")},
# 2 ------------------------------------------------------------------------------------------
{"title": "Las tres etapas clásicas del proceso", "html": ess(
"Para entender el lavado se suele dividir en tres pasos: meter el dinero al sistema, enredar su rastro y devolverlo a la economía con una explicación que parezca legal. No siempre ocurren en ese orden, pero el modelo ayuda a reconocer qué está pasando.") + """
<p>Las etapas son un modelo didáctico: en la vida real pueden superponerse, repetirse o saltarse.[[3]]</p>
<ol class="steps">
<li><strong>Colocación.</strong> El dinero ilícito entra al sistema económico: depósitos, compra de instrumentos, pago de bienes de alto valor o mezcla con los ingresos de un negocio real. Es la etapa más vulnerable para el delincuente, porque el efectivo todavía está cerca de su origen.</li>
<li><strong>Estratificación (o diversificación).</strong> Se crean capas de transacciones para alejar los fondos de su origen: transferencias entre cuentas y países, compraventas sucesivas, préstamos simulados, sociedades interpuestas.</li>
<li><strong>Integración.</strong> Los fondos regresan a la economía con una explicación aparentemente legal: utilidades de una empresa, venta de un inmueble, premios, herencias o inversiones.</li>
</ol>
<div class="case"><b>Ejemplo ilustrativo</b>
<p>Una red que obtiene efectivo de la extorsión lo deposita en pequeñas sumas en la cuenta de un taller mecánico real (colocación). Desde allí paga «facturas» a tres empresas recién creadas que no tienen empleados ni oficinas (estratificación). Meses después, una de esas empresas compra un apartamento y lo alquila; las rentas aparecen como ingresos de un negocio inmobiliario (integración).</p>
</div>
<h3>¿Dónde se nota cada etapa?</h3>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Etapa</th><th>Lo que podría ver quien atiende al cliente</th></tr></thead>
<tbody>
<tr><td>Colocación</td><td>Efectivo abundante sin explicación; depósitos fraccionados para no llegar a un umbral; pagos en efectivo de bienes caros.</td></tr>
<tr><td>Estratificación</td><td>Transferencias rápidas entre cuentas o países sin propósito claro; terceros que pagan por el cliente; empresas recién creadas que mueven mucho dinero.</td></tr>
<tr><td>Integración</td><td>Ingresos «de negocio» que no cuadran con el tamaño real de la actividad; bienes a nombre de familiares o sociedades; préstamos que se pagan de golpe sin fuente visible.</td></tr>
</tbody></table></div>
<p class="note-small">Ejemplos de elaboración propia. Una señal aislada no prueba nada: abre un análisis.</p>
""" + deep("""
<p>Por eso la ley no define la operación sospechosa por el monto, sino por su naturaleza: transacciones, efectuadas o no, complejas, insólitas o significativas, así como patrones no habituales o transacciones no significativas pero periódicas, que no tengan un fundamento económico o legal evidente o que generen sospecha de vinculación con el lavado, un delito precedente o el financiamiento del terrorismo (art. 2, num. 16).[[1]]</p>
<p>Fíjate en dos matices de esa definición: incluye operaciones <em>no efectuadas</em> (intentadas) y patrones de montos <em>pequeños pero periódicos</em>. Ambas cosas son típicas de la colocación y la estratificación.</p>
""")},
# 3 ------------------------------------------------------------------------------------------
{"title": "Lo que castiga la ley", "html": ess(
"No solo comete lavado quien organiza el esquema. También quien esconde, compra, guarda o usa bienes sabiendo que son de un delito, quien ayuda a otros a escapar de la justicia y quien presta su nombre. Y la ley no acepta como excusa «no quise saber».") + """
<p>El art. 3 de la Ley 155-17 describe varias conductas de lavado y sus penas:[[1]]</p>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Conducta</th><th>Pena de prisión</th></tr></thead>
<tbody>
<tr><td>Convertir, transferir o transportar bienes, a sabiendas de que provienen de un delito precedente, para ocultar o encubrir su origen</td><td>10 a 20 años de prisión mayor</td></tr>
<tr><td>Ocultar, disimular o encubrir la naturaleza, el origen, la ubicación, el movimiento o la propiedad real de esos bienes</td><td>10 a 20 años</td></tr>
<tr><td>Adquirir, poseer, administrar o utilizar bienes sabiendo que provienen de un delito precedente</td><td>10 a 20 años</td></tr>
<tr><td>Asistir, asesorar, ayudar o facilitar a implicados en lavado para que eludan la persecución o la condena</td><td>4 a 10 años</td></tr>
<tr><td>Complicidad, asociación, tentativa o prestación esencial para realizar estas conductas</td><td>4 a 10 años</td></tr>
</tbody></table></div>
<p>A la prisión se suman multas expresadas en salarios mínimos, el decomiso de los bienes e instrumentos y la inhabilitación para trabajar en entidades de intermediación financiera, del mercado de valores y públicas.[[1]]</p>
<h3>«No sabía» no siempre protege</h3>
<p>La ley permite inferir el conocimiento o la intención a partir de las <strong>circunstancias objetivas</strong> del caso, y declara equivalentes el conocimiento, el dolo, la <strong>obligación de conocer</strong> y la <strong>ignorancia deliberada</strong> (art. 7).[[1]] Mirar hacia otro lado ante señales evidentes no es una defensa.</p>
<h3>Delitos asociados que alcanzan al personal</h3>
<p>El art. 4 sanciona, entre otras, estas conductas del personal de los sujetos obligados:[[1]]</p>
<ul>
<li>No cumplir <strong>intencionalmente</strong> con las obligaciones de información o reporte: 3 a 5 años.</li>
<li>Falsear, adulterar, destruir u ocultar documentos, registros o informes exigidos por la ley: 2 a 5 años.</li>
<li><strong>Revelar</strong> a clientes o terceros los reportes de operaciones sospechosas u otra información entregada a la UAF: 2 a 5 años.</li>
</ul>
<p>También castiga a quien presta su nombre para adquirir bienes producto de una infracción grave (persona física: 3 a 6 años; persona jurídica: disolución y multa) y a quien simula o usa la identidad de otra persona para transacciones con bienes de origen ilícito.[[1]]</p>
""" + deep("""
<p><strong>Testaferro.</strong> La ley lo define como la persona física o jurídica que hace aparentar como propios los activos de un tercero procedentes de actividades ilícitas, cuyo propietario real no figura en los documentos de titularidad (art. 2, num. 26).[[1]]</p>
<p><strong>Personas jurídicas.</strong> Cuando la infracción es imputable a una empresa, esta puede ser sancionada —con independencia de la responsabilidad de sus dueños o empleados— con multa no menor de 2,000 salarios mínimos o hasta el valor de los bienes lavados, clausura de locales, prohibición de actividades, cancelación de licencias o disolución (art. 8).[[1]]</p>
<p><strong>Agravantes.</strong> Se aplica el máximo de la pena, entre otros casos, cuando participan grupos criminales organizados, cuando el autor es funcionario público o <strong>director, funcionario o empleado de un sujeto obligado</strong>, en caso de reincidencia o cuando se emplean menores (art. 9).[[1]]</p>
<p><strong>Notarios y registradores.</strong> Quienes, sin constancia fehaciente del medio de pago, instrumenten o registren operaciones en efectivo prohibidas por el art. 64 se sancionan con 6 meses a 1 año de prisión menor; al notario se le revoca su investidura (art. 4, num. 11).[[1]]</p>
<p><strong>Dinero en frontera.</strong> Entrar o salir del país con más de US$10,000 en efectivo o títulos al portador sin declararlo, o declarándolo falsamente, se sanciona con 6 meses a 1 año, decomiso y multa (art. 4, num. 12); la declaración se presenta en el formulario de la Dirección General de Aduanas (art. 65).[[1]]</p>
""")},
# 4 ------------------------------------------------------------------------------------------
{"title": "Financiamiento del terrorismo y de la proliferación", "html": ess(
"El lavado esconde de dónde viene el dinero. El financiamiento del terrorismo esconde a dónde va: puede usar dinero limpio —donaciones, salarios— para pagar actos violentos. Por eso los montos pueden ser pequeños y la señal más importante suele ser quién recibe los fondos.") + """
<p>El <strong>financiamiento del terrorismo (FT)</strong> consiste en proveer, recolectar, ofrecer, facilitar, administrar o entregar bienes o servicios sabiendo, o con la intención de, que se usarán para apoyar a individuos u organizaciones terroristas —aun sin relación directa con un acto concreto— o para cometer actos terroristas. La ley lo sanciona con <strong>20 a 40 años de prisión</strong> y decomiso (art. 5).[[1]]</p>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th></th><th>Lavado de activos</th><th>Financiamiento del terrorismo</th></tr></thead>
<tbody>
<tr><td>Origen de los fondos</td><td>Siempre ilícito</td><td>Puede ser lícito o ilícito</td></tr>
<tr><td>Lo que se oculta</td><td>El origen</td><td>El destino y la finalidad</td></tr>
<tr><td>Montos típicos</td><td>Suelen ser elevados</td><td>Pueden ser pequeños y difíciles de detectar</td></tr>
</tbody></table></div>
<p>El delito existe aunque los actos terroristas no se hayan realizado, aunque la ayuda no se haya brindado o aunque el acto se cometa o intente en otro país (art. 5, párrafo).[[1]]</p>
<p>El <strong>financiamiento de la proliferación de armas de destrucción masiva (FPADM)</strong> se refiere a proveer fondos o servicios financieros para desarrollar, adquirir o transportar armas nucleares, químicas o biológicas. Las Recomendaciones del GAFI exigen aplicar sanciones financieras dirigidas contra personas y entidades designadas por el Consejo de Seguridad de la ONU, tanto por terrorismo como por proliferación (Recomendaciones 6 y 7).[[2]]</p>
<h3>Congelar «sin demora»</h3>
<p>Los sujetos obligados deben monitorear si un cliente, beneficiario final o potencial cliente figura en las listas del Consejo de Seguridad de la ONU y, si es así, <strong>congelar preventivamente sus bienes sin demora</strong> y notificar al Ministerio Público y a la UAF (arts. 82 y 83). Está prohibido a cualquier persona en el país entregar bienes o servicios a personas incluidas en esas listas.[[1]]</p>
""" + deep("""
<p><strong>¿Qué significa «sin demora»?</strong> Para las listas de las Resoluciones 1267, 1988 y 1718, significa de inmediato, en cuestión de horas desde la designación (art. 2, num. 23).[[1]]</p>
<p><strong>Procedimiento del Decreto 407-17.</strong> Los sujetos obligados deben revisar constantemente las actualizaciones de las listas y, de forma autónoma y sin demora: revisar sus bases de datos; si hay un positivo, congelar preventivamente <em>sin notificar a la persona afectada</em>; y comunicar de inmediato la medida a la Procuraduría Especializada Antilavado y a la UAF (arts. 4 y 5). El congelamiento se mantiene hasta que la autoridad judicial lo ratifique o lo levante; puede revocarse, entre otros casos, por homonimia o falso positivo (art. 8).[[6]]</p>
<p>La información entregada a la UAF sobre el congelamiento no sustituye el ROS cuando corresponda (Decreto 407-17, art. 22).[[6]] Incumplir el régimen de congelamiento es una infracción administrativa muy grave (Ley 155-17, art. 87).[[1]]</p>
""")},
# 5 ------------------------------------------------------------------------------------------
{"title": "¿Por qué importa a todos?", "html": ess(
"El lavado no es un problema solo de bancos. Premia al crimen, compite de forma desleal con los negocios honrados y puede dañar la reputación del país entero. Cuando un país no controla el lavado, a sus empresas y ciudadanos les cuesta más acceder al crédito y al sistema financiero internacional.") + """
<p>Los considerandos de la Ley 155-17 explican sus motivos. Entre ellos:[[1]]</p>
<ul>
<li>Proteger las instituciones democráticas, la economía, la balanza de pagos, la estabilidad de precios y la competencia leal en las actividades comerciales y productivas legítimas.</li>
<li>Cumplir los compromisos de las convenciones de Naciones Unidas contra el tráfico de drogas (1988), el terrorismo (1999), la delincuencia organizada transnacional (2000) y la corrupción (2003).</li>
<li>Evitar que el país sea colocado en una lista de países no cooperantes, con consecuencias sobre la reputación, el acceso al crédito del sector público y privado y la asistencia de organismos internacionales.</li>
</ul>
<p>Las Recomendaciones del GAFI son el estándar internacional que inspira la ley; el propio reglamento ordena tomarlas en cuenta, junto con sus notas interpretativas, al interpretar las normas de prevención (Decreto 408-17, art. 45).[[2,4]]</p>
<div class="callout key"><b>Idea clave</b>Cada sujeto obligado que cumple bien protege su propia reputación, pero también la del sistema completo. Una sola entidad débil puede convertirse en la puerta de entrada del dinero ilícito.</div>
""" + deep("""
<p><strong>Transparencia societaria.</strong> La ley también incorporó medidas de transparencia: obligó a convertir las acciones al portador en nominativas (art. 103 y disposición transitoria) y modificó el Código Tributario para que las personas jurídicas dispongan de información actualizada de sus beneficiarios finales (art. 104).[[1]]</p>
<p><strong>Evaluaciones mutuas.</strong> Entre las funciones del Comité Nacional está velar por el cumplimiento y seguimiento de las evaluaciones mutuas que la comunidad internacional hace al país (art. 89, num. 10), y elaborar la estrategia nacional y la metodología de evaluación nacional de riesgos (art. 89, num. 1).[[1]]</p>
""")},
# 6 ------------------------------------------------------------------------------------------
{"title": "Quién hace qué en el sistema dominicano", "html": ess(
"La prevención funciona como una red: unos ponen las reglas, otros vigilan su cumplimiento, otros analizan la información y otros persiguen los delitos. Las empresas obligadas son los ojos de esa red, porque ven las operaciones primero.") + """
<div class="grid-2">
<div class="mini"><h4>GAFI y GAFILAT</h4><p>El GAFI emite las 40 Recomendaciones, el estándar internacional. GAFILAT es el organismo regional que agrupa a países de Latinoamérica y evalúa su cumplimiento.[[2]]</p></div>
<div class="mini"><h4>Comité Nacional (CONCLAFIT)</h4><p>Órgano colegiado de coordinación del sistema. Lo preside el Ministro de Hacienda e integran, entre otros, el Procurador General, el Ministro de Defensa y los superintendentes de Bancos y de Valores (arts. 88 a 90).[[1]]</p></div>
<div class="mini"><h4>Unidad de Análisis Financiero (UAF)</h4><p>Ente técnico que recibe los reportes de operaciones sospechosas y de transacciones en efectivo, los analiza y eleva informes al Ministerio Público; ejerce la secretaría técnica del Comité (art. 91).[[1]]</p></div>
<div class="mini"><h4>Supervisores</h4><p>Regulan, supervisan e inspeccionan a los sujetos obligados con una metodología basada en riesgos y aplican sanciones administrativas (arts. 98 a 100).[[1]]</p></div>
<div class="mini"><h4>Sujetos obligados</h4><p>Entidades financieras y actividades no financieras designadas que deben conocer a sus clientes, detectar operaciones inusuales y reportarlas (arts. 31 a 33).[[1]]</p></div>
<div class="mini"><h4>Ministerio Público y tribunales</h4><p>Investigan, persiguen y juzgan. La UAF no ejerce la acción penal; su producto es inteligencia financiera.[[5]]</p></div>
</div>
<h3>¿Quién supervisa a quién?</h3>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Sujeto obligado</th><th>Supervisor</th></tr></thead>
<tbody>
<tr><td>Intermediación financiera o cambiaria; fiduciarias que sirven a entidades financieras</td><td>Superintendencia de Bancos</td></tr>
<tr><td>Participantes del mercado de valores, incluidas fiduciarias de oferta pública</td><td>Superintendencia de Valores</td></tr>
<tr><td>Sector seguros</td><td>Superintendencia de Seguros</td></tr>
<tr><td>Cooperativas</td><td>IDECOOP</td></tr>
<tr><td>Casinos, juegos de azar, bancas y loterías</td><td>Dirección de Casinos y Juegos de Azar (Ministerio de Hacienda)</td></tr>
<tr><td>Actividades sin regulador específico (por ejemplo, inmobiliarias, joyerías, profesionales)</td><td>Dirección General de Impuestos Internos (DGII)</td></tr>
</tbody></table></div>
<p class="note-small">Según el art. 2, num. 17 de la Ley 155-17.[[1]]</p>
""" + deep("""
<p><strong>La UAF por dentro.</strong> Además de recibir reportes, la UAF puede solicitar información adicional a los sujetos obligados —sin que ello viole el secreto bancario—, hacer análisis estratégico de tendencias y análisis operativo de casos, e intercambiar información con unidades homólogas de otros países (art. 91).[[1]] Cuando la UAF pide información, el sujeto obligado debe entregarla en un plazo no mayor de 10 días laborables, o en uno menor si la UAF lo dispone (Decreto 408-17, art. 25).[[4]]</p>
<p><strong>Reserva hacia el supervisor.</strong> Los supervisores acceden a los registros de los sujetos obligados, <em>excepto</em> a los detalles de inteligencia contenidos en los reportes de operaciones sospechosas (art. 56, párrafo).[[1]] El sujeto obligado tampoco puede revelar al supervisor las solicitudes de la UAF ni el hecho de haberle remitido un ROS; sí puede hacerlo respecto del reporte de transacciones en efectivo (Decreto 408-17, art. 25, párrafo II).[[4]]</p>
""")},
# 7 ------------------------------------------------------------------------------------------
{"title": "Tu papel en la primera línea", "html": ess(
"La mayoría de los casos se detectan gracias a una persona atenta: quien abre la cuenta, emite la póliza, cobra o vende. Tu trabajo no es investigar ni acusar, sino conocer a tu cliente, notar lo que no encaja, avisar por el canal interno y guardar silencio frente al cliente.") + """
<ul>
<li><strong>Conocer al cliente</strong> y entender para qué usará el producto o servicio.</li>
<li><strong>Notar lo que no encaja</strong> con ese perfil: montos, frecuencia, terceros sin relación aparente, prisa injustificada, desinterés por costos.</li>
<li><strong>Escalar internamente</strong> al oficial de cumplimiento, siguiendo el procedimiento de tu entidad, con los hechos documentados.</li>
<li><strong>Guardar reserva</strong>: está prohibido revelar a terceros que se reportó o que se examina una operación (art. 63).[[1]]</li>
</ul>
<div class="callout tip"><b>En la práctica</b>No necesitas probar un delito para escalar una alerta. Basta con describir objetivamente qué observaste y por qué te pareció inusual; el análisis posterior corresponde a cumplimiento.</div>
<div class="case"><b>Caso para pensar</b>
<p>Una cliente nueva quiere comprar al contado un vehículo de lujo. Paga con transferencias desde cuatro cuentas de personas distintas y, cuando el vendedor le pregunta, responde molesta que «son primos que le prestaron». Pide que la factura salga a nombre de una empresa que todavía «está en trámite».</p>
<p class="verdict yes"><b>¿Qué haría la primera línea?</b> Documentar los hechos (pagos de terceros, explicación vaga, titular distinto del pagador) y escalarlos al oficial de cumplimiento sin comentarle nada a la cliente. Cumplimiento decidirá si pide soportes, si aplica medidas adicionales o si reporta.</p>
</div>
<h3>La ley protege a quien reporta de buena fe</h3>
<p>Los sujetos obligados y su personal no incurren en responsabilidad civil, administrativa ni penal cuando, en cumplimiento de la ley, reportan a la UAF o suministran información a las autoridades (art. 58).[[1]] Y si un potencial cliente se niega a dar la información necesaria para identificarlo, la ley prohíbe iniciar la relación y ordena remitir un reporte de operación sospechosa (art. 62).[[1]]</p>
""" + deep("""
<p><strong>Confidencialidad de quien reporta.</strong> No adoptar medidas para mantener la confidencialidad de la identidad de los empleados que hicieron un reporte es una infracción administrativa muy grave para el sujeto obligado (art. 69, lit. h).[[1]]</p>
<p><strong>Secreto profesional.</strong> Las disposiciones sobre secreto bancario, fiduciario o profesional no impiden cumplir las obligaciones de prevención; los sujetos obligados deben entregar la información que requieran la UAF, el Ministerio Público y los tribunales penales (art. 57).[[1]]</p>
<p><strong>Informante.</strong> La ley prevé la figura del informante para quienes voluntariamente aportan información útil a las autoridades, pero aclara que no tienen esa calidad quienes, por su cargo o función, están <em>obligados</em> a denunciar o reportar (art. 14, párrafo II).[[1]] Para el personal de un sujeto obligado, reportar es un deber, no una colaboración opcional.</p>
""")},
],
"glossary": [
("Lavado de activos", "Proceso mediante el cual se busca dar apariencia legítima a bienes provenientes de delitos precedentes (Ley 155-17, art. 2, num. 15) [[1]]."),
("Infracción precedente", "Delito que genera los bienes que luego se lavan; incluye una lista legal y toda infracción grave con pena no menor de tres años [[1]]."),
("Colocación", "Etapa en que el dinero ilícito entra al sistema económico, por ejemplo mediante depósitos o compras de alto valor [[3]]."),
("Estratificación", "Etapa en que se crean capas de transacciones para alejar los fondos de su origen [[3]]."),
("Integración", "Etapa en que los fondos vuelven a la economía con una explicación aparentemente legal [[3]]."),
("Ignorancia deliberada", "Evitar conocer a propósito el origen ilícito de los bienes; la ley la equipara al conocimiento (art. 7) [[1]]."),
("Testaferro", "Persona que aparenta ser dueña de bienes ilícitos de un tercero que no figura en los documentos (art. 2, num. 26) [[1]]."),
("Sujeto obligado", "Persona física o jurídica obligada por la ley a prevenir, detectar, evaluar y mitigar el riesgo de lavado y financiamiento del terrorismo [[1]]."),
("Congelamiento preventivo", "Medida inmediata que impide disponer de los bienes de personas incluidas en listas del Consejo de Seguridad de la ONU [[1,6]]."),
],
"quiz": [
{"q": "¿Qué elemento es indispensable para que exista lavado de activos?", "options": ["Que la operación supere US$15,000", "Que los bienes provengan de una infracción precedente", "Que participe una entidad financiera", "Que el dinero salga del país"], "answer": 1, "explain": "El lavado consiste en dar apariencia legítima a bienes de origen ilícito; sin una infracción precedente que los genere, no hay lavado. El monto o el sector no son requisitos del delito [[1]]."},
{"q": "Además de los delitos enumerados, ¿qué otra infracción puede ser precedente del lavado según la Ley 155-17?", "options": ["Cualquier falta administrativa", "Toda infracción grave sancionable con pena no menor de tres años", "Solo los delitos cometidos en el extranjero", "Únicamente el narcotráfico"], "answer": 1, "explain": "La definición de infracción precedente incluye una cláusula general: toda infracción grave con pena no menor de tres años (art. 2, num. 11) [[1]]."},
{"q": "Una red compra varios inmuebles a nombre de sociedades sin actividad y luego los revende entre ellas. ¿Qué etapa describe mejor esta conducta?", "options": ["Colocación", "Estratificación", "Integración", "Ninguna, es una operación inmobiliaria normal"], "answer": 1, "explain": "Las compraventas sucesivas entre sociedades interpuestas crean capas que alejan los fondos de su origen: es la estratificación [[3]]."},
{"q": "El delito precedente se cometió en otro país y todavía no ha sido juzgado. ¿Puede perseguirse el lavado en la República Dominicana?", "options": ["No, primero debe haber condena por el delito precedente", "Sí, porque el lavado es un delito autónomo, independiente de dónde se cometió el delito previo", "Solo si el monto supera US$10,000", "Solo si el autor es dominicano"], "answer": 1, "explain": "El art. 6 establece que el lavado se investiga, enjuicia y falla como hecho autónomo, aunque el delito precedente se haya cometido en otra jurisdicción [[1]]."},
{"q": "Un empleado nota señales evidentes de que un cliente maneja dinero ilícito, pero decide «no preguntar para no saber». Según el art. 7, esta actitud:", "options": ["Lo protege, porque no tenía conocimiento", "Puede equipararse al conocimiento: la ley trata igual la ignorancia deliberada", "Solo importa si el cliente es condenado", "Es la conducta recomendada"], "answer": 1, "explain": "La ley declara equivalentes el conocimiento, el dolo, la obligación de conocer y la ignorancia deliberada [[1]]."},
{"q": "¿Qué pena prevé la ley para quien revela a un cliente que se envió un ROS sobre sus operaciones?", "options": ["Ninguna, es una falta ética", "Prisión de 2 a 5 años, multa e inhabilitación", "Solo una amonestación interna", "Una multa de US$100"], "answer": 1, "explain": "El art. 4, num. 3 sanciona con 2 a 5 años de prisión mayor, multa e inhabilitación permanente a quien revela los ROS u otra información entregada a la UAF [[1]]."},
{"q": "¿Cuál es una diferencia clave entre el lavado de activos y el financiamiento del terrorismo?", "options": ["El financiamiento del terrorismo siempre usa dinero ilícito", "En el financiamiento del terrorismo los fondos pueden tener origen lícito y lo que se oculta es su destino", "El lavado solo ocurre con montos pequeños", "No existe diferencia práctica"], "answer": 1, "explain": "En el FT el dinero puede venir de fuentes lícitas; lo relevante es su destino y finalidad. En el lavado, el origen siempre es ilícito [[1,2]]."},
{"q": "Un cliente coincide plenamente con una persona de la lista del Consejo de Seguridad de la ONU. ¿Qué corresponde?", "options": ["Avisarle para que aclare su situación", "Congelar preventivamente sus bienes sin demora, sin notificarle, y comunicarlo al Ministerio Público y a la UAF", "Esperar una orden judicial antes de actuar", "Cerrar la cuenta y entregarle el saldo"], "answer": 1, "explain": "Los arts. 82 y 83 de la ley y el Decreto 407-17 exigen congelar sin demora, sin notificar a la persona afectada, y comunicar de inmediato la medida [[1,6]]."},
{"q": "¿Qué institución recibe y analiza los reportes de los sujetos obligados en la República Dominicana?", "options": ["El Ministerio Público", "La Unidad de Análisis Financiero (UAF)", "La Policía Nacional", "El GAFI"], "answer": 1, "explain": "La UAF es el ente técnico que recibe y analiza los reportes y eleva informes al Ministerio Público (art. 91) [[1]]."},
{"q": "Una joyería sin regulador específico es sujeto obligado. ¿Quién la supervisa en materia de prevención?", "options": ["La Superintendencia de Bancos", "La Dirección General de Impuestos Internos (DGII)", "La UAF", "Nadie"], "answer": 1, "explain": "El art. 2, num. 17 asigna a la DGII la supervisión de los sujetos obligados sin un organismo regulador estatal específico [[1]]."},
{"q": "Un cajero nota que un cliente fracciona depósitos en efectivo. ¿Cuál es la actuación correcta?", "options": ["Preguntarle si está lavando dinero", "Escalar internamente al oficial de cumplimiento, con los hechos, y guardar reserva", "Ignorarlo porque cada depósito es pequeño", "Comentarlo en el chat del equipo"], "answer": 1, "explain": "La primera línea documenta y escala por el canal interno. Revelar al cliente o a terceros que se analiza una operación está prohibido (art. 63) [[1]]."},
{"q": "Un empleado reporta de buena fe y el cliente lo amenaza con demandarlo. Según el art. 58:", "options": ["El empleado responde civilmente", "No incurre en responsabilidad civil, administrativa ni penal por reportar en cumplimiento de la ley", "Debe retirar el reporte", "Solo está protegido si el cliente es condenado"], "answer": 1, "explain": "El art. 58 exime de responsabilidad a quienes reportan a la UAF o informan a las autoridades en cumplimiento de la ley [[1]]."},
],
}
