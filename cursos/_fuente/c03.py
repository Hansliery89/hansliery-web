"""Curso 03 · Enfoque basado en riesgos."""
from fuentes import *  # noqa: F401,F403
from capas import ess, deep

# 1 GAFI40 · 2 LEY · 3 GAFI_RBA · 4 ISO_31000 · 5 DGII_N01 · 6 SIS_NORMA · 7 REG · 8 CNV_NORMA · 9 IDECOOP_NORMA
COURSE = {
"num": 3, "slug": "enfoque-basado-en-riesgos", "tag": "Riesgos", "level": "Intermedio → Profesional", "minutes": 50,
"title": "Enfoque basado en riesgos",
"card": "Cómo concentrar los recursos donde el riesgo es mayor, con criterio y evidencia.",
"summary": "Aprende a aplicar el enfoque basado en riesgos: qué exige la ley, cómo se identifican amenazas y vulnerabilidades, cómo se mide el riesgo inherente, qué controles corresponden y cómo se monitorea el riesgo residual, con ejemplos de la normativa sectorial dominicana.",
"objectives": [
  "Explicar qué exige el enfoque basado en riesgos y por qué es la base del sistema de prevención.",
  "Diferenciar amenaza, vulnerabilidad, consecuencia, riesgo inherente, controles y riesgo residual.",
  "Aplicar los cuatro factores mínimos de riesgo del art. 37 de la Ley 155-17.",
  "Recorrer las etapas de gestión del riesgo: identificación, medición, control y mitigación, y monitoreo.",
  "Vincular el nivel de riesgo con la debida diligencia simplificada, normal o ampliada.",
  "Evitar los errores más comunes al implementar el enfoque.",
],
"sources": [GAFI40, LEY, GAFI_RBA, ISO_31000, DGII_N01, SIS_NORMA, REG, CNV_NORMA, IDECOOP_NORMA],
"modules": [
# 1 ------------------------------------------------------------------------------------------
{"title": "Recursos limitados, riesgos distintos", "html": ess(
"No todos los clientes ni todas las operaciones tienen el mismo peligro de ser usados para lavar dinero. El enfoque basado en riesgos consiste en mirar con más atención donde el peligro es mayor y simplificar donde es menor, dejando por escrito por qué se decidió así.") + """
<p>Ninguna entidad puede revisar con la misma intensidad cada cliente y cada operación. El <strong>enfoque basado en riesgos (EBR)</strong> propone entender dónde está el riesgo y aplicar medidas más intensas donde es mayor y más simples donde es menor. Es la primera de las Recomendaciones del GAFI, que pide a los países y a las entidades identificar, evaluar y entender sus riesgos y asignar recursos en consecuencia.[[1]]</p>
<p>La Ley 155-17 lo adopta en varios niveles:[[2]]</p>
<ul>
<li>El <strong>programa de cumplimiento</strong> debe ser basado en riesgo y adecuado a la organización, estructura, recursos y complejidad de las operaciones (art. 34).</li>
<li>Las políticas deben incluir una <strong>debida diligencia basada en riesgo</strong>, con medidas simplificadas, ampliadas o reforzadas (art. 36).</li>
<li>Los sujetos obligados deben aplicar una <strong>metodología de gestión de riesgos</strong> con, como mínimo, cuatro factores (art. 37).</li>
<li>Los productos, servicios y canales nuevos y existentes, incluidos los que usan nuevas tecnologías, deben evaluarse (art. 45).</li>
</ul>
<div class="callout key"><b>Idea clave</b>El EBR no significa hacer menos: significa hacer lo correcto en el lugar correcto, y poder demostrar por qué.</div>
""" + deep("""
<p><strong>Dos niveles de evaluación.</strong> El GAFI distingue la evaluación de riesgos que hace cada país —la evaluación nacional de riesgos— de la que debe hacer cada entidad sobre su propio negocio; la segunda debe tener en cuenta la primera.[[1]] En la práctica, la evaluación nacional y las tipologías que publican las autoridades son insumos de la matriz de la entidad.</p>
<p><strong>Proporcionalidad.</strong> La ley pide que el programa sea adecuado a la organización, estructura, recursos y complejidad de las operaciones (art. 34).[[2]] Por eso una cooperativa pequeña y un banco no tienen el mismo programa, pero ambos deben poder explicar su lógica de riesgo.</p>
""")},
# 2 ------------------------------------------------------------------------------------------
{"title": "El vocabulario del riesgo", "html": ess(
"Para pensar el riesgo con orden se usan pocas palabras: quién puede causar el daño (amenaza), qué debilidad aprovecharía (vulnerabilidad), qué pasaría si ocurre (consecuencia), cuánto riesgo hay antes de los controles (inherente) y cuánto queda después (residual).") + """
<p>Tres conceptos ayudan a describir un riesgo:[[3]]</p>
<ul>
<li><strong>Amenaza</strong>: personas o actividades que pueden causar daño (organizaciones criminales, sus fondos, sus métodos).</li>
<li><strong>Vulnerabilidad</strong>: debilidades que la amenaza puede aprovechar (un producto que acepta efectivo sin límites, controles manuales, personal sin capacitación).</li>
<li><strong>Consecuencia</strong>: el impacto si ocurre (sanciones, daño reputacional, pérdidas, daño a la sociedad).</li>
</ul>
<p>A partir de ahí se distinguen tres momentos. La norma del sector seguros los define de forma sencilla: el <strong>riesgo inherente</strong> es el propio de la actividad, sin tener en cuenta el efecto de los controles, y el <strong>riesgo residual</strong> es el que resulta luego de aplicarlos.[[6]]</p>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Concepto</th><th>Pregunta que responde</th></tr></thead>
<tbody>
<tr><td>Riesgo inherente</td><td>¿Cuánto riesgo existe por la naturaleza del cliente, producto, zona o canal, antes de aplicar controles?</td></tr>
<tr><td>Controles</td><td>¿Qué medidas lo reducen y qué tan eficaces son en la práctica?</td></tr>
<tr><td>Riesgo residual</td><td>¿Cuánto riesgo queda después de los controles? ¿Está dentro de la tolerancia aprobada?</td></tr>
</tbody></table></div>
<div class="case"><b>Ejemplo</b><p>Un producto que acepta pagos en efectivo de terceros tiene un riesgo inherente alto. Si la entidad limita el efectivo, identifica a quien paga y revisa los pagos de terceros, el riesgo residual baja. Si esos controles existen solo en el manual y nadie los aplica, el residual sigue siendo alto.</p></div>
""" + deep("""
<p><strong>Probabilidad e impacto.</strong> La medición del riesgo combina la posibilidad o probabilidad de que ocurra con el impacto que tendría si se materializa; así lo exige, por ejemplo, la etapa de medición de la norma de seguros.[[6]] ISO 31000 ofrece un marco general de gestión del riesgo —principios, marco de referencia y proceso— que muchas entidades usan para ordenar esa medición, aunque no es una norma específica de prevención de lavado.[[4]]</p>
<p><strong>Tolerancia.</strong> La norma de seguros pide garantizar que el riesgo residual se encuentre en los niveles de tolerancia definidos por el sujeto obligado.[[6]] La Norma 01-2018 de la DGII, al tratar las señales de alerta, pide al sujeto obligado actuar con criterio en cada situación conforme a su apetito y tolerancia de riesgo.[[5]] Es la alta dirección quien debe aprobar esos niveles.</p>
""")},
# 3 ------------------------------------------------------------------------------------------
{"title": "Los cuatro factores mínimos", "html": ess(
"La ley obliga a mirar, como mínimo, cuatro cosas: quién es el cliente, qué producto usa, dónde opera y por qué canal llegó. Además, dos situaciones son siempre de alto riesgo: las personas expuestas políticamente y las operaciones con países señalados por el GAFI.") + """
<p>La metodología de riesgos debe incorporar como mínimo los clientes, los productos o servicios, las áreas geográficas y los canales de distribución (art. 37).[[2]] La norma de seguros detalla qué evaluar en cada uno al segmentar: actividad económica, volumen o frecuencia de las transacciones del cliente; naturaleza, características y mercado objetivo del producto; ubicación geográfica y naturaleza de las transacciones; y naturaleza y características de los canales de comercialización.[[6]]</p>
<div class="grid-2">
<div class="mini"><h4>Clientes</h4><p>Actividad económica, tipo de persona, condición de PEP, estructura de propiedad, antigüedad de la relación, comportamiento transaccional.</p></div>
<div class="mini"><h4>Productos y servicios</h4><p>Uso de efectivo, posibilidad de anonimato, rapidez de movimiento de fondos, pagos de terceros, rescates anticipados.</p></div>
<div class="mini"><h4>Áreas geográficas</h4><p>Jurisdicciones señaladas por el GAFI, zonas fronterizas o con alta incidencia delictiva, origen y destino de transferencias.</p></div>
<div class="mini"><h4>Canales de distribución</h4><p>Presencial, digital sin contacto, intermediarios o agentes, corresponsales.</p></div>
</div>
<p class="note-small">Los ejemplos de cada recuadro son ilustrativos; cada entidad debe elegir y justificar las variables que reflejan su negocio.</p>
<div class="callout warn"><b>Factores de alto riesgo por ley</b>Las personas expuestas políticamente y las transacciones u operaciones que involucren jurisdicciones definidas por el GAFI deben considerarse, como mínimo, factores de alto riesgo (art. 46).[[2]]</div>
""" + deep("""
<p><strong>Ejemplo sectorial: seguros.</strong> La norma de la Superintendencia de Seguros considera, como mínimo, de riesgo alto a las PEP; a los países, jurisdicciones y áreas geográficas de alto riesgo; a las personas incluidas en listas restrictivas; al beneficiario final de seguros de vida y de retiro con componente de ahorro; y al beneficiario de una póliza de riesgos generales que cubra bienes de lujo. Como riesgo bajo menciona, entre otros, las pólizas con prima anual menor a 4 salarios mínimos o primas que en conjunto no superen 10 salarios mínimos, los organismos estatales y las operaciones con organismos internacionales. Lo que no es alto ni bajo es riesgo medio.[[6]]</p>
<p><strong>Ejemplo sectorial: DGII.</strong> La Norma 01-2018 exige debida diligencia ampliada, entre otros supuestos, para relaciones con jurisdicciones de alto riesgo, sociedades «de carpeta» sin actividad económica real, PEP, no residentes con operaciones en efectivo superiores a US$15,000 diarios, estructuras accionarias inusuales o excesivamente complejas y clientes que fueron objeto de un ROS cuando se decidió continuar la relación.[[5]]</p>
""")},
# 4 ------------------------------------------------------------------------------------------
{"title": "Las etapas de la gestión del riesgo", "html": ess(
"Gestionar el riesgo es un ciclo que no termina: primero se identifica qué puede salir mal, luego se mide cuánto, después se ponen controles y, por último, se vigila que funcionen y se vuelve a empezar cuando algo cambia.") + """
<p>La ley pide políticas enfocadas en identificación o diagnóstico; medición y control; y monitoreo y mitigación (art. 36), y una metodología para identificar, medir, controlar, mitigar y monitorear de manera oportuna los eventos potenciales de riesgo (art. 37).[[2]] La norma de seguros lo organiza en cuatro etapas:[[6]]</p>
<ol class="steps">
<li><strong>Identificación o diagnóstico.</strong> Definir la metodología de segmentación de los factores, segmentarlos y, con base en ello, identificar los riesgos dentro de la operación diaria.</li>
<li><strong>Medición.</strong> Medir la probabilidad de ocurrencia y el impacto de cada riesgo, para establecer el perfil de riesgo de la entidad.</li>
<li><strong>Control y mitigación.</strong> Definir y aplicar las medidas de control sobre cada factor y los niveles de exposición, hasta llegar al perfil de riesgo residual.</li>
<li><strong>Monitoreo.</strong> Dar seguimiento a los riesgos inherente y residual, asegurar que el residual esté dentro de la tolerancia y que los controles funcionen de manera efectiva.</li>
</ol>
<p>Es una lógica coherente con el proceso general de ISO 31000, que también recorre la identificación, el análisis, la evaluación, el tratamiento y el seguimiento del riesgo.[[4]]</p>
<div class="callout tip"><b>En la práctica</b>Documenta la metodología y las decisiones. Ante el supervisor, una calificación sin sustento vale poco; un criterio razonado y aplicado de forma consistente vale mucho.</div>
""" + deep("""
<p><strong>Infraestructura.</strong> La misma norma de seguros pide sistemas acordes con el tamaño, riesgo y volumen de negocio, con actualización periódica de los factores de riesgo, automatización de señales de alerta y parametrización de los reportes regulatorios.[[6]]</p>
<p><strong>Revisión periódica.</strong> En el mercado de valores, la matriz de riesgo debe revisarse al menos una vez al año, dejando constancia de la modificación y de su finalidad y conservando la matriz anterior.[[8]] Además, la ley exige mantener actualizados los datos de los clientes según su riesgo, con revisiones que incluyan a las categorías de mayor riesgo (art. 36, párrafo).[[2]]</p>
<p><strong>Nuevos productos.</strong> Los sujetos obligados financieros que introduzcan nuevos productos y servicios deben presentar una evaluación de riesgos junto con un plan de mitigación (art. 45, párrafo).[[2]]</p>
""")},
# 5 ------------------------------------------------------------------------------------------
{"title": "Del nivel de riesgo a la medida de control", "html": ess(
"El nivel de riesgo de un cliente decide cuánto hay que investigarlo: poco si el riesgo es bajo, lo normal si es medio y mucho más si es alto. Pero hay una regla de oro: si hay sospecha, nunca se simplifica.") + """
<p>La ley permite aplicar debida diligencia <strong>simplificada</strong> cuando se identifican riesgos menores y exige debida diligencia <strong>ampliada</strong> cuando se identifican riesgos mayores. Las medidas simplificadas deben ser proporcionales y no son aceptables cuando surge una sospecha o se presentan escenarios específicos de riesgos mayores (art. 42).[[2]]</p>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Nivel</th><th>Tipo de debida diligencia</th><th>Ejemplos de medidas (Norma 01-2018 DGII)</th></tr></thead>
<tbody>
<tr><td>Bajo</td><td>Simplificada</td><td>Reducir la periodicidad de la revisión documental o el seguimiento de operaciones bajo un umbral; inferir el propósito por el tipo de relación.</td></tr>
<tr><td>Medio</td><td>Normal</td><td>Datos de identificación, actividad, dirección y documentación de soporte.</td></tr>
<tr><td>Alto</td><td>Ampliada</td><td>Además de lo normal: información bancaria, evidencia de verificación de lo declarado y referencias comerciales.</td></tr>
</tbody></table></div>
<p class="note-small">Elaborado a partir de la Norma General 01-2018 de la DGII, que exige clasificar a los clientes como mínimo en alto, medio y bajo y aplicar una debida diligencia diferenciada.[[5]]</p>
<p>La Norma 01-2018 define la <strong>matriz de riesgo</strong> como la herramienta que permite clasificar a los clientes, como mínimo, en bajo, medio y alto riesgo, para aplicar una debida diligencia diferenciada.[[5]] El diseño de esa matriz se estudia en el curso 4.</p>
""" + deep("""
<p><strong>Frecuencia de actualización.</strong> El reglamento ordena actualizar la debida diligencia de los clientes actuales conforme a su nivel de riesgo (Decreto 408-17, art. 17).[[7]] Algunas normas fijan plazos concretos: la Norma 01-2018 de la DGII pide actualizar a los clientes habituales cada año y a los ocasionales cada dos años.[[5]]</p>
<p><strong>Clientes institucionales.</strong> La misma norma admite debida diligencia simplificada, entre otros, para clientes de bajo riesgo, entidades financieras que no provengan de países de alto riesgo, el Gobierno Central, el Banco Central y organismos multilaterales de los que el país sea miembro.[[5]]</p>
<p><strong>Cooperativas.</strong> La Norma 001-17 del IDECOOP exige que el manual de las cooperativas defina la matriz de riesgo del asociado, con tipos de asociado, umbrales y factores de productos, ubicaciones geográficas y canales.[[9]]</p>
""")},
# 6 ------------------------------------------------------------------------------------------
{"title": "Errores que conviene evitar", "html": ess(
"Los fallos más comunes son buscar cero riesgo, rechazar grupos enteros de clientes sin analizarlos, tener matrices que nadie actualiza, calificar sin datos y confundir «cliente de alto riesgo» con «cliente sospechoso».") + """
<ul>
<li><strong>Buscar «riesgo cero».</strong> El objetivo es gestionar el riesgo dentro de una tolerancia aprobada, no eliminarlo.</li>
<li><strong>Rechazar categorías completas de clientes sin análisis.</strong> El EBR pide evaluar y gestionar el riesgo; excluir sectores enteros por comodidad no es lo que pide el estándar y puede empujar a las personas hacia canales informales.[[3]]</li>
<li><strong>Matrices que nadie actualiza.</strong> Una evaluación de hace años no refleja productos nuevos ni tipologías emergentes.[[2]]</li>
<li><strong>Calificar sin datos.</strong> Las ponderaciones deben apoyarse en información de la propia entidad y en fuentes externas confiables.</li>
<li><strong>Controles «de papel».</strong> El monitoreo debe asegurar que los controles funcionen de manera efectiva, no solo que existan.[[6]]</li>
<li><strong>Confundir alto riesgo con sospecha.</strong> Un cliente de alto riesgo exige más diligencia, no un reporte automático. El ROS procede cuando, tras el análisis, existe una sospecha.</li>
</ul>
""" + deep("""
<p><strong>Señal para auditores.</strong> Una distribución en la que casi todos los clientes aparecen como de bajo riesgo, o una matriz que nunca cambia aunque la entidad lanza productos, suelen indicar que la metodología no está capturando la realidad. Son puntos que una auditoría independiente debería revisar.</p>
""")},
# 7 ------------------------------------------------------------------------------------------
{"title": "Caso práctico", "html": ess(
"Apliquemos todo a una entidad concreta que lanza un producto nuevo por un canal digital.") + """
<div class="case"><b>Caso · «Seguro de ahorro en línea»</b>
<p>Una aseguradora quiere vender por internet un seguro de vida con componente de ahorro, con pago de primas por transferencia y posibilidad de rescate anticipado.</p>
<ol>
<li><strong>Identificar:</strong> el producto combina ahorro, rescate anticipado y canal no presencial. La norma de seguros considera de riesgo alto al beneficiario final de seguros de vida con componente de ahorro.[[6]]</li>
<li><strong>Medir:</strong> la probabilidad de uso indebido sube por el canal sin contacto y el impacto por la posibilidad de mover fondos rápido.</li>
<li><strong>Controlar:</strong> verificación de identidad del contratante y del beneficiario, límites de prima, revisión de pagos de terceros y de rescates tempranos, alertas automatizadas.</li>
<li><strong>Documentar:</strong> por ser sujeto obligado financiero, presentar la evaluación de riesgos y el plan de mitigación del producto nuevo.[[2]]</li>
<li><strong>Monitorear:</strong> revisar a los seis meses si los controles funcionan y si las alertas se concentran donde se esperaba.</li>
</ol>
<p class="verdict yes"><b>Lección:</b> el EBR no impide lanzar el producto; obliga a lanzarlo con controles proporcionales y con evidencia de que se pensó en el riesgo.</p>
</div>
""" + deep("""
<p><strong>Para discutir.</strong> ¿Qué cambiaría si el mismo producto se vende solo de forma presencial y con primas bajas? ¿Seguiría siendo de alto riesgo el beneficiario final? Recuerda que algunos factores de alto riesgo vienen fijados por la norma y no dependen del puntaje.[[6]]</p>
""")},
],
"glossary": [
("Enfoque basado en riesgos (EBR)", "Aplicar medidas proporcionales al riesgo identificado; Recomendación 1 del GAFI [[1]]."),
("Amenaza", "Persona, grupo o actividad que puede causar daño [[3]]."),
("Vulnerabilidad", "Debilidad que la amenaza puede aprovechar [[3]]."),
("Riesgo inherente", "Riesgo propio de la actividad, sin tener en cuenta los controles [[6]]."),
("Riesgo residual", "Riesgo que resulta después de aplicar los controles [[6]]."),
("Factores de riesgo", "Variables mínimas del art. 37: clientes, productos o servicios, áreas geográficas y canales [[2]]."),
("Segmentación", "Agrupación de los factores de riesgo según criterios definidos por la entidad [[6]]."),
("Debida diligencia simplificada", "Medidas reducidas para riesgos menores; no admisibles si hay sospecha (art. 42) [[2]]."),
("Debida diligencia ampliada", "Medidas adicionales cuando se identifican riesgos mayores (art. 42) [[2]]."),
],
"quiz": [
{"q": "¿Qué describe mejor el enfoque basado en riesgos?", "options": ["Aplicar los mismos controles a todos los clientes", "Concentrar medidas más intensas donde el riesgo es mayor y más simples donde es menor", "Eliminar todo cliente de riesgo", "Revisar solo a los clientes nuevos"], "answer": 1, "explain": "El EBR adapta la intensidad de las medidas al riesgo identificado; es la Recomendación 1 del GAFI [[1]]."},
{"q": "Según la norma del sector seguros, el riesgo propio de la actividad, sin considerar los controles, es el riesgo:", "options": ["Residual", "Inherente", "Reputacional", "Aceptado"], "answer": 1, "explain": "La norma define el riesgo inherente como el propio de la actividad sin tener en cuenta el efecto de los controles [[6]]."},
{"q": "¿Cuáles son los cuatro factores mínimos de riesgo del art. 37 de la Ley 155-17?", "options": ["Clientes, productos y servicios, áreas geográficas y canales de distribución", "Edad, sexo, nacionalidad y profesión", "Monto, moneda, fecha y sucursal", "Auditoría, cumplimiento, riesgo y legal"], "answer": 0, "explain": "El art. 37 exige incorporar como mínimo clientes, productos o servicios, áreas geográficas y canales de distribución [[2]]."},
{"q": "¿Qué dos factores considera la ley, como mínimo, de alto riesgo (art. 46)?", "options": ["Clientes nuevos y clientes jóvenes", "Las PEP y las operaciones con jurisdicciones definidas por el GAFI", "El efectivo y las tarjetas", "Los empleados y los proveedores"], "answer": 1, "explain": "El art. 46 señala a las PEP y a las operaciones con jurisdicciones definidas por el GAFI [[2]]."},
{"q": "¿Cuándo NO es aceptable aplicar debida diligencia simplificada?", "options": ["Cuando el cliente es una entidad estatal", "Cuando surge una sospecha de lavado o financiamiento del terrorismo", "Cuando el riesgo es bajo", "Cuando el cliente es antiguo"], "answer": 1, "explain": "El art. 42 establece que las medidas simplificadas no son aceptables cuando surgen sospechas o escenarios de riesgo mayor [[2]]."},
{"q": "En la norma de seguros, ¿qué etapa establece el perfil de riesgo residual de la entidad?", "options": ["Identificación", "Medición", "Control y mitigación", "Ninguna"], "answer": 2, "explain": "Como resultado de la etapa de control y mitigación se establece el perfil de riesgo residual [[6]]."},
{"q": "Un sujeto obligado financiero lanza un producto nuevo. ¿Qué debe presentar?", "options": ["Nada, solo si el supervisor lo pide", "Una evaluación de riesgos y un plan de mitigación", "Un ROS preventivo", "Un seguro de responsabilidad"], "answer": 1, "explain": "El párrafo del art. 45 exige presentar la evaluación de riesgos junto a un plan de mitigación [[2]]."},
{"q": "Según la Norma 01-2018 de la DGII, ¿con qué frecuencia se actualiza la debida diligencia de los clientes habituales?", "options": ["Cada mes", "Cada año", "Cada cinco años", "Nunca"], "answer": 1, "explain": "La norma pide actualizar a los clientes habituales cada año y a los ocasionales cada dos años [[5]]."},
{"q": "En el mercado de valores, ¿cada cuánto debe revisarse como mínimo la matriz de riesgo?", "options": ["Una vez al año", "Cada tres años", "Solo al crearla", "Cada diez años"], "answer": 0, "explain": "La norma del CNV exige revisarla al menos una vez al año y conservar la versión anterior [[8]]."},
{"q": "Una entidad decide rechazar a todos los clientes de un sector económico sin evaluar casos individuales. Desde el EBR esto es:", "options": ["La mejor práctica", "Un error: el EBR pide evaluar y gestionar, no excluir por categoría sin análisis", "Obligatorio por ley", "Irrelevante"], "answer": 1, "explain": "El EBR busca gestionar el riesgo con análisis; las exclusiones masivas sin evaluación no son lo que pide el estándar [[3]]."},
{"q": "Un cliente fue calificado de alto riesgo. ¿Qué corresponde?", "options": ["Enviar un ROS de inmediato", "Aplicar debida diligencia ampliada y monitoreo reforzado", "Cerrar la relación sin más", "Nada, la calificación es informativa"], "answer": 1, "explain": "Riesgo alto implica diligencia ampliada (art. 42); el reporte procede solo si surge una sospecha tras el análisis [[2]]."},
],
}
