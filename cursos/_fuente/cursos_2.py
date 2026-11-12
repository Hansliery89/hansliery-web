"""Cursos 05 a 07: debida diligencia, beneficiario final y PEP."""
from fuentes import *  # noqa: F401,F403

COURSES = [
# ---------------------------------------------------------------------------------------------
{
"num": 5, "slug": "debida-diligencia-y-conocimiento-del-cliente", "tag": "Debida diligencia", "level": "Intermedio", "minutes": 30,
"title": "Debida diligencia y conocimiento del cliente",
"card": "Identificar, verificar y conocer al cliente según su nivel de riesgo.",
"summary": "Domina el proceso de debida diligencia: qué información obtener, cómo verificarla, cuándo aplicar medidas simplificadas o ampliadas y qué hacer cuando no es posible completarla.",
"objectives": [
  "Describir los componentes de la debida diligencia de personas físicas y jurídicas.",
  "Elegir entre debida diligencia simplificada, estándar y ampliada según el riesgo.",
  "Actuar correctamente cuando el cliente no entrega la información requerida.",
  "Mantener la información actualizada y los registros conservados.",
],
"sources": [LEY, GAFI40, UAF_ROS, GOAML, DGII_GLO],
"modules": [
{"title": "Conocer al cliente no es un formulario", "html": """
<p>La <strong>debida diligencia</strong> es el conjunto de medidas para saber con quién se hace negocio, de dónde vienen sus recursos y si su comportamiento es coherente con lo declarado. La ley la exige para clientes <strong>actuales y potenciales</strong> y la orienta por riesgo (arts. 36 y 38).[[1]]</p>
<p>Sus componentes centrales son:[[1,2]]</p>
<ul>
<li>Identificar al cliente y verificar su identidad con documentos o fuentes confiables e independientes.</li>
<li>Identificar a quien actúa en su nombre y verificar que esté autorizado.</li>
<li>Identificar al <strong>beneficiario final</strong> y tomar medidas razonables para verificarlo.</li>
<li>Entender el propósito y la naturaleza prevista de la relación.</li>
<li>Monitorear la relación y las transacciones de forma continua (art. 39).</li>
</ul>
<div class="callout key"><b>Idea clave</b>El objetivo es construir un <strong>perfil</strong> del cliente —quién es, qué hace, cuánto y cómo opera— contra el cual comparar su actividad futura.</div>
"""},
{"title": "Personas jurídicas y fideicomisos", "html": """
<p>Cuando el cliente es una persona jurídica, además de los datos básicos se debe conocer su <strong>estructura de propiedad y control</strong>. La ley pide verificar, entre otros, la razón social, el número de registro tributario (RNC), la forma jurídica, la dirección y el beneficiario final (art. 40).[[1]]</p>
<p>En los fideicomisos deben identificarse todas las partes, incluidos el fideicomitente y el beneficiario final (art. 41).[[1]]</p>
<div class="callout tip"><b>En la práctica</b>Pide el organigrama de propiedad hasta llegar a personas físicas. Si aparece una sociedad extranjera en la cadena, solicita sus documentos societarios y la identificación de sus propietarios.</div>
"""},
{"title": "Tres intensidades de diligencia", "html": """
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Nivel</th><th>Cuándo</th><th>Qué implica</th></tr></thead>
<tbody>
<tr><td>Simplificada</td><td>Riesgo bajo demostrado</td><td>Medidas reducidas en alcance o frecuencia. <strong>No es aceptable si hay sospecha</strong> de lavado o financiamiento del terrorismo (art. 42).</td></tr>
<tr><td>Estándar</td><td>Riesgo medio o habitual</td><td>Identificación y verificación completas, perfil y monitoreo periódico.</td></tr>
<tr><td>Ampliada</td><td>Riesgo alto: PEP, jurisdicciones señaladas por el GAFI, estructuras complejas, productos de alto riesgo</td><td>Información adicional sobre origen de fondos y patrimonio, aprobación de un nivel superior, monitoreo reforzado y actualización más frecuente.</td></tr>
</tbody></table></div>
<p>La ley también menciona la diligencia reforzada dentro del esquema basado en riesgos (art. 36); lo importante es que la intensidad sea proporcional al riesgo y esté documentada.[[1]]</p>
"""},
{"title": "Cuando el cliente no colabora", "html": """
<p>Si no es posible identificar y verificar al cliente, la entidad <strong>no debe iniciar ni mantener</strong> la relación (art. 62). Además, cuando el cliente <strong>se niega</strong> a suministrar la información de debida diligencia, la ley ordena emitir un Reporte de Operación Sospechosa.[[1,4]]</p>
<div class="callout warn"><b>No confundir</b>Un cliente simplemente <em>ilocalizable</em> o que no completó documentos internos no exigidos por la normativa antilavado no justifica, por sí solo, un reporte. La negativa a entregar información exigida por la ley sí activa el deber de reportar.[[3,4]]</div>
<div class="case"><b>Caso</b><p>Un potencial cliente desea constituir un certificado por un monto alto. Al pedirle la documentación del origen de los fondos responde que «no tiene por qué explicarlo» y se retira.</p>
<p class="verdict yes"><b>Decisión:</b> no se inicia la relación y, al tratarse de una negativa a brindar información de debida diligencia, se evalúa y remite el ROS dentro del plazo legal.</p></div>
"""},
{"title": "Actualizar, conservar y delegar", "html": """
<ul>
<li><strong>Actualización</strong>: los datos deben mantenerse vigentes; la frecuencia depende del riesgo y de eventos que cambien el perfil (nuevo producto, cambio de actividad, alertas).[[1]]</li>
<li><strong>Conservación</strong>: los registros se guardan al menos 10 años después de terminada la relación o la transacción ocasional (art. 43).[[1]]</li>
<li><strong>Delegación</strong>: se puede apoyar en la identificación realizada por otro sujeto obligado, pero la responsabilidad final sigue siendo de quien delega, que debe poder obtener la información y las copias pertinentes (art. 47).[[1]]</li>
</ul>
<div class="callout key"><b>Recuerda</b>La debida diligencia bien hecha es también la mejor defensa ante un falso positivo: permite explicar rápidamente por qué una operación inusual es legítima.</div>
"""},
],
"quiz": [
{"q": "¿A quiénes aplica la debida diligencia según la Ley 155-17?", "options": ["Solo a clientes nuevos", "A clientes actuales y potenciales", "Solo a personas jurídicas", "Solo a clientes de alto riesgo"], "answer": 1, "explain": "El art. 38 extiende la debida diligencia a clientes actuales y potenciales [[1]]."},
{"q": "¿Cuándo NO es aceptable aplicar debida diligencia simplificada?", "options": ["Cuando el cliente es asalariado", "Cuando existe sospecha de lavado o financiamiento del terrorismo", "Cuando el producto es de bajo monto", "Nunca es aceptable"], "answer": 1, "explain": "El art. 42 excluye la simplificada si hay sospecha de LA/FT [[1]]."},
{"q": "Un cliente se niega a entregar información exigida para su debida diligencia. ¿Qué corresponde?", "options": ["Abrir la cuenta igual", "No iniciar la relación y remitir un ROS", "Enviar un RAS opcional", "Esperar a que cambie de opinión"], "answer": 1, "explain": "La ley impide iniciar la relación sin identificación y ordena reportar mediante ROS la negativa a brindar la información [[1,4]]."},
{"q": "Para una persona jurídica, ¿cuál de estos datos exige verificar el art. 40?", "options": ["El color corporativo", "La estructura de propiedad y el beneficiario final", "El número de empleados", "Sus redes sociales"], "answer": 1, "explain": "El art. 40 incluye razón social, RNC, forma jurídica, estructura de propiedad, dirección y beneficiario final [[1]]."},
{"q": "Si una entidad delega la identificación de un cliente en otro sujeto obligado:", "options": ["La responsabilidad pasa al tercero", "La responsabilidad final sigue siendo de quien delega", "No se requiere conservar copias", "Queda exenta de monitorear"], "answer": 1, "explain": "El art. 47 permite delegar, pero mantiene la responsabilidad en quien delega [[1]]."},
{"q": "¿Para qué sirve el perfil del cliente construido en la debida diligencia?", "options": ["Para venderle más productos", "Como referencia para detectar actividad que no sea coherente con lo declarado", "Para cumplir un trámite sin uso posterior", "Para fijar su tasa de interés"], "answer": 1, "explain": "El perfil permite comparar la actividad real con la esperada y detectar inusualidades."},
],
},
# ---------------------------------------------------------------------------------------------
{
"num": 6, "slug": "beneficiario-final", "tag": "Debida diligencia", "level": "Intermedio", "minutes": 25,
"title": "Beneficiario final",
"card": "Llegar a la persona física que realmente posee o controla.",
"summary": "Aprende a identificar a la persona física que posee o controla realmente a un cliente, calcular la propiedad indirecta y reconocer estructuras diseñadas para ocultarla.",
"objectives": [
  "Aplicar la definición legal de beneficiario final.",
  "Calcular participaciones indirectas a través de una cadena societaria.",
  "Seguir la secuencia de identificación cuando no hay un propietario claro.",
  "Reconocer señales de opacidad y el uso de testaferros.",
],
"sources": [LEY, REG, GAFI40, GAFI_BF, DGII_BF],
"modules": [
{"title": "Siempre una persona física", "html": """
<p>La Ley 155-17 define al <strong>beneficiario final</strong> como la persona física que ejerce el <strong>control efectivo final</strong> sobre una persona jurídica o que tiene como mínimo el <strong>20 % de su capital</strong>, incluyendo a la persona física en beneficio de quien se realiza una transacción (art. 2, num. 5).[[1]]</p>
<p>Los estándares internacionales insisten en lo mismo: detrás de cualquier sociedad, fideicomiso o estructura hay personas físicas, y son ellas las que deben conocerse.[[3,4]]</p>
<div class="callout key"><b>Idea clave</b>Una sociedad nunca es beneficiaria final. Si al terminar el análisis el resultado es otra empresa, el trabajo no ha terminado.</div>
"""},
{"title": "Calcular la propiedad indirecta", "html": """
<p>La propiedad puede ser directa o llegar a través de otras sociedades. Para la indirecta se multiplican los porcentajes a lo largo de la cadena.</p>
<div class="case"><b>Ejemplo resuelto</b>
<p>La empresa cliente «Comercial Alfa, SRL» pertenece en 60 % a «Inversiones Beta, SA» y en 40 % a la Sra. Pérez. A su vez, «Inversiones Beta» pertenece en 50 % al Sr. Gómez y en 50 % al Sr. Díaz.</p>
<ul><li>Sra. Pérez: 40 % directo.</li><li>Sr. Gómez: 50 % × 60 % = 30 % indirecto.</li><li>Sr. Díaz: 50 % × 60 % = 30 % indirecto.</li></ul>
<p class="verdict yes"><b>Resultado:</b> los tres superan el 20 % y son beneficiarios finales por propiedad. Aun así, debe verificarse si otra persona ejerce el control por otros medios.</p></div>
"""},
{"title": "La secuencia de identificación", "html": """
<ol class="steps">
<li><strong>Propiedad</strong>: personas físicas con 20 % o más del capital, directa o indirectamente.[[1]]</li>
<li><strong>Control por otros medios</strong>: quien toma las decisiones relevantes aunque no tenga el porcentaje (acuerdos de accionistas, derechos de veto, poderes amplios, influencia familiar o financiera).[[4,5]]</li>
<li><strong>Cargo gerencial</strong>: si no se logra identificar a nadie por los criterios anteriores, el reglamento indica considerar como tal a quienes ocupan el mayor rango gerencial.[[2]]</li>
</ol>
<p>En los fideicomisos deben identificarse todas las partes, incluidos el fideicomitente y los beneficiarios (art. 41).[[1]]</p>
<div class="callout warn"><b>Atención</b>El tercer paso es un último recurso, no un atajo. Documenta qué gestiones hiciste en los dos primeros y por qué no fueron concluyentes.</div>
"""},
{"title": "Señales de opacidad", "html": """
<ul>
<li>Cadenas de sociedades sin una razón comercial que las explique, especialmente con jurisdicciones de baja transparencia.</li>
<li>Socios o administradores que no parecen tener el perfil ni los recursos para el negocio (posibles <strong>testaferros</strong>, figura que la propia ley define y sanciona).[[1]]</li>
<li>Poderes amplios otorgados a terceros sin relación aparente.</li>
<li>Cambios frecuentes de accionistas o administradores sin explicación.</li>
<li>Resistencia a entregar documentos societarios o información de los propietarios.</li>
</ul>
<p>Cuando el beneficiario final resulta ser una persona expuesta políticamente, deben aplicarse los controles propios de las PEP y tratarla como de alto riesgo.[[5]]</p>
"""},
{"title": "Un deber que también es tributario", "html": """
<p>La Ley 155-17 modificó el Código Tributario para obligar a las personas jurídicas y entes sin personalidad jurídica a disponer de información actualizada de sus beneficiarios finales, como deber formal ante la DGII (art. 104).[[5]]</p>
<p>Para el sujeto obligado esto significa que el cliente debería poder entregar esa información. Si no puede o no quiere, es una señal que merece análisis.</p>
<div class="callout tip"><b>En la práctica</b>Contrasta lo que declara el cliente con registros mercantiles, documentos societarios y fuentes públicas. La declaración del cliente es un punto de partida, no una verificación.</div>
"""},
],
"quiz": [
{"q": "Según la Ley 155-17, ¿qué porcentaje mínimo de capital convierte a una persona física en beneficiaria final por propiedad?", "options": ["10 %", "20 %", "25 %", "50 %"], "answer": 1, "explain": "El art. 2, num. 5 establece como mínimo el 20 % del capital, además del control efectivo final [[1]]."},
{"q": "La sociedad X posee 80 % del cliente. El Sr. A posee 30 % de X. ¿Cuál es la participación indirecta del Sr. A en el cliente?", "options": ["30 %", "24 %", "80 %", "10 %"], "answer": 1, "explain": "Se multiplican los porcentajes: 30 % × 80 % = 24 %, por encima del umbral del 20 %."},
{"q": "Una persona tiene solo 5 % del capital, pero por un acuerdo de accionistas decide todas las inversiones. ¿Es beneficiaria final?", "options": ["No, porque no llega al 20 %", "Sí, por ejercer el control efectivo final", "Solo si es PEP", "Depende del monto invertido"], "answer": 1, "explain": "La definición incluye a quien ejerce el control efectivo final, con independencia de su porcentaje [[1,4]]."},
{"q": "Tras agotar los criterios de propiedad y control sin resultado, ¿a quién se considera beneficiario final según el reglamento?", "options": ["A la propia sociedad", "A quienes ocupan el mayor rango gerencial", "Al contador externo", "A nadie"], "answer": 1, "explain": "El Decreto 408-17 indica considerar a las personas que ocupan el mayor rango gerencial cuando no se puede identificar al beneficiario final [[2]]."},
{"q": "El análisis de propiedad termina en «Holding Gamma Ltd.», sociedad extranjera. ¿Qué corresponde?", "options": ["Registrar a Holding Gamma como beneficiaria final", "Continuar el análisis hasta identificar a las personas físicas detrás de Holding Gamma", "Cerrar el expediente", "Pedir solo el logo de la empresa"], "answer": 1, "explain": "El beneficiario final es siempre una persona física; una sociedad no puede serlo."},
{"q": "Si el beneficiario final de un cliente es una PEP, ¿qué medidas se aplican?", "options": ["Ninguna adicional", "Los controles de PEP y tratamiento como alto riesgo", "Un ROS automático", "Rechazo inmediato del cliente"], "answer": 1, "explain": "Deben aplicarse los controles vinculados a las PEP y considerarlas de alto riesgo; ser PEP no implica por sí solo un reporte [[5]]."},
],
},
# ---------------------------------------------------------------------------------------------
{
"num": 7, "slug": "personas-expuestas-politicamente", "tag": "Debida diligencia", "level": "Intermedio", "minutes": 25,
"title": "Personas Expuestas Políticamente (PEP)",
"card": "Quién es PEP, a quién alcanza y qué medidas aplicar sin estigmatizar.",
"summary": "Identifica a las personas expuestas políticamente, sus familiares y asociados cercanos, y aplica las medidas de debida diligencia ampliada que exige la ley sin confundir la condición de PEP con una sospecha.",
"objectives": [
  "Aplicar la definición legal de PEP y su alcance temporal.",
  "Identificar a familiares y asociados cercanos alcanzados por las medidas.",
  "Diseñar las medidas de debida diligencia ampliada para una PEP.",
  "Distinguir entre alto riesgo y operación sospechosa.",
],
"sources": [LEY, GAFI40, GAFI_PEP, UAF_ROS, LEY_311, DGII_GLO, CONCLAFIT_2021_02],
"modules": [
{"title": "¿Quién es PEP?", "html": """
<p>Según la Ley 155-17, una <strong>persona expuesta políticamente</strong> es quien desempeña o ha desempeñado, <strong>durante los últimos tres años</strong>, altas funciones públicas por elección o nombramiento, en el país o en el extranjero, incluidos altos cargos de organismos internacionales (art. 2, num. 19).[[1,6]]</p>
<p>La ley incluye, entre otros, a jefes de Estado o de gobierno, funcionarios gubernamentales, judiciales o militares de alta jerarquía y altos ejecutivos de empresas estatales, y precisa que son PEP <strong>todos los funcionarios obligados a presentar declaración jurada de bienes</strong> (Ley 311-14), además de quienes determine el Comité Nacional.[[1,5]]</p>
<div class="callout tip"><b>Caso particular</b>Mediante la Resolución 02-2021, el CONCLAFIT ratificó la condición de PEP de los <strong>Cónsules Generales Honorarios</strong>, aunque no presenten declaración jurada, por el riesgo asociado a su función.[[7]]</div>
<div class="callout key"><b>Por qué importa</b>Por su posición, una PEP puede tener acceso a recursos públicos o influencia sobre decisiones que la hacen más vulnerable a la corrupción. Las medidas reforzadas existen para gestionar ese riesgo, no para presumir culpa.[[3]]</div>
"""},
{"title": "El círculo cercano", "html": """
<p>El riesgo puede trasladarse a personas cercanas. Por eso la ley extiende la debida diligencia basada en riesgo a:[[1]]</p>
<ul>
<li>Cónyuge, unión libre o concubinato.</li>
<li>Parientes hasta el <strong>segundo grado</strong> de consanguinidad o afinidad.</li>
<li>Asociados cercanos (socios comerciales y personas con relaciones estrechas conocidas).</li>
<li>Quien realice operaciones en nombre de la PEP.</li>
</ul>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Grado</th><th>Consanguinidad</th><th>Afinidad</th></tr></thead>
<tbody>
<tr><td>Primer grado</td><td>Padres e hijos</td><td>Suegros, yernos y nueras</td></tr>
<tr><td>Segundo grado</td><td>Abuelos, nietos y hermanos</td><td>Cuñados</td></tr>
</tbody></table></div>
"""},
{"title": "Medidas de debida diligencia ampliada", "html": """
<p>La ley ordena tratar a las PEP como clientes de <strong>alto riesgo</strong> (art. 46). Siguiendo los estándares internacionales, las medidas típicas son:[[1,2,3]]</p>
<ol class="steps">
<li><strong>Identificar la condición</strong> desde la vinculación (declaración del cliente, consultas y fuentes públicas) y durante la relación.</li>
<li><strong>Aprobación de la alta gerencia</strong> para iniciar o continuar la relación.</li>
<li><strong>Establecer el origen de los fondos y del patrimonio</strong>, con soporte documental proporcional.</li>
<li><strong>Monitoreo reforzado</strong> de la relación y de las transacciones.</li>
</ol>
<div class="callout tip"><b>En la práctica</b>Pregunta por la fuente de riqueza (cómo construyó su patrimonio) y por la fuente de los fondos de la operación concreta. Son preguntas distintas y ambas importan.</div>
"""},
{"title": "Ser PEP no es una sospecha", "html": """
<p>Un error frecuente es reportar a un cliente por el solo hecho de ser PEP. La UAF aclara que las PEP deben clasificarse como de alto riesgo y recibir debida diligencia ampliada, pero <strong>no deben reportarse por pertenecer a esa categoría</strong>, salvo que se identifique una situación sospechosa vinculada a un delito precedente.[[4]]</p>
<div class="case"><b>Caso</b>
<p>Una directora general de una institución pública solicita un préstamo hipotecario. Sus ingresos declarados y su historial bancario son coherentes con la cuota.</p>
<p class="verdict no"><b>Decisión:</b> se aplica debida diligencia ampliada y aprobación superior; no procede ROS. Si luego recibiera depósitos de contratistas del Estado sin explicación, el análisis cambiaría.</p></div>
"""},
{"title": "Después del cargo", "html": """
<p>La definición legal cubre a quien ejerció el cargo en los últimos tres años. Aun así, el enfoque basado en riesgos permite mantener medidas reforzadas más allá de ese plazo cuando la influencia o los riesgos persisten.[[1,3]]</p>
<ul>
<li>Registra la fecha de inicio y de término del cargo.</li>
<li>Programa la revisión de la condición al cumplirse el plazo.</li>
<li>Documenta la decisión de mantener o ajustar las medidas.</li>
</ul>
"""},
],
"quiz": [
{"q": "Según la Ley 155-17, ¿durante qué período posterior al cargo se mantiene la condición de PEP?", "options": ["1 año", "Los últimos 3 años", "5 años", "De por vida"], "answer": 1, "explain": "La definición abarca a quien desempeña o ha desempeñado altas funciones públicas durante los últimos tres años [[1]]."},
{"q": "¿Hasta qué grado de parentesco alcanza el art. 46 a los familiares de una PEP?", "options": ["Primer grado", "Segundo grado", "Cuarto grado", "Solo el cónyuge"], "answer": 1, "explain": "El párrafo del art. 46 incluye a parientes hasta el segundo grado, cónyuges, uniones de hecho y asociados cercanos [[1]]."},
{"q": "El cuñado de un ministro abre una cuenta. ¿Está alcanzado por las medidas?", "options": ["No, la afinidad no cuenta", "Sí, es pariente por afinidad en segundo grado", "Solo si vive con el ministro", "Solo si es funcionario"], "answer": 1, "explain": "El cuñado es pariente por afinidad en segundo grado, dentro del alcance del art. 46."},
{"q": "¿Cuál es una medida típica de debida diligencia ampliada para una PEP?", "options": ["Cobrarle comisiones más altas", "Obtener aprobación de la alta gerencia y establecer el origen de fondos y patrimonio", "Reportarla a la UAF", "Negarle el servicio"], "answer": 1, "explain": "Los estándares internacionales prevén aprobación superior, origen de fondos y patrimonio y monitoreo reforzado [[2,3]]."},
{"q": "Un cliente es identificado como PEP y su operativa es coherente con su perfil. ¿Procede un ROS?", "options": ["Sí, siempre", "No; se aplica debida diligencia ampliada, pero ser PEP no es motivo de reporte por sí solo", "Sí, pero como RTE", "Solo si es extranjero"], "answer": 1, "explain": "La UAF aclara que la condición de PEP no debe reportarse por sí misma, salvo que exista una situación sospechosa [[4]]."},
{"q": "¿Qué diferencia hay entre fuente de riqueza y fuente de fondos?", "options": ["Son lo mismo", "La riqueza explica cómo se formó el patrimonio total; los fondos, de dónde proviene el dinero de una operación concreta", "La riqueza solo aplica a empresas", "Los fondos solo aplican a efectivo"], "answer": 1, "explain": "Ambas se indagan en la diligencia ampliada y responden preguntas distintas [[3]]."},
],
},
]
