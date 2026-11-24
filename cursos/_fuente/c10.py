"""Curso 10 · Activos virtuales y riesgos emergentes."""
from fuentes import *  # noqa: F401,F403
from capas import ess, deep

# 1 GAFI40 · 2 GAFI_VA_M · 3 GAFI_VA_RF_M · 4 DGII_CRIPTO · 5 UAF_VAL · 6 LEY
COURSE = {
"num": 10, "slug": "activos-virtuales-y-riesgos-emergentes", "tag": "Riesgos emergentes", "level": "Básico → Profesional", "minutes": 50,
"title": "Activos virtuales y riesgos emergentes",
"card": "Criptoactivos, proveedores de servicios y señales de alerta.",
"summary": "Entiende qué son los activos virtuales y sus proveedores de servicios, cómo funcionan las billeteras y la cadena de bloques, cuál es la situación en la República Dominicana, qué exigen las Recomendaciones 15 y 16 del GAFI, qué señales de alerta publicó el GAFI y cómo aplicar debida diligencia a clientes vinculados a criptoactivos.",
"objectives": [
  "Explicar qué es un activo virtual y qué actividades convierten a alguien en proveedor de servicios de activos virtuales.",
  "Distinguir billeteras custodiadas y no custodiadas y comprender la trazabilidad de la cadena de bloques.",
  "Describir la posición oficial dominicana sobre las criptomonedas.",
  "Identificar los requisitos del GAFI para este sector, incluida la regla de viaje.",
  "Reconocer las categorías de señales de alerta del GAFI.",
  "Aplicar debida diligencia a clientes vinculados a criptoactivos.",
],
"sources": [GAFI40, GAFI_VA_M, GAFI_VA_RF_M, DGII_CRIPTO, UAF_VAL, LEY],
"notice": "Este es un ámbito que cambia con rapidez. Verifica si existe normativa dominicana nueva sobre activos virtuales antes de aplicar este contenido.",
"modules": [
# 1 ------------------------------------------------------------------------------------------
{"title": "Conceptos básicos", "html": ess(
"Un activo virtual —como el bitcoin— es valor que existe solo en forma digital y que se puede vender, transferir o usar para pagar o invertir. No es lo mismo que el dinero electrónico de un banco, que representa pesos o dólares.") + """
<p>Para el GAFI, un <strong>activo virtual</strong> es una representación digital de valor que puede comercializarse o transferirse digitalmente y usarse para pagos o inversiones. No incluye las representaciones digitales de monedas de curso legal ni los valores y otros activos financieros ya cubiertos por otras Recomendaciones.[[1,2]]</p>
<p>Un <strong>proveedor de servicios de activos virtuales (PSAV)</strong> es quien, como negocio y por cuenta de otros, realiza una o más de estas actividades:[[1,2]]</p>
<ol class="steps">
<li>Intercambio entre activos virtuales y monedas de curso legal.</li>
<li>Intercambio entre una o más formas de activos virtuales.</li>
<li>Transferencia de activos virtuales.</li>
<li>Custodia o administración de activos virtuales o de instrumentos que permiten controlarlos.</li>
<li>Participación y provisión de servicios financieros relacionados con la oferta o venta de un activo virtual por un emisor.</li>
</ol>
""" + deep("""
<p><strong>Función, no nombre.</strong> La guía del GAFI insiste en que lo que importa es la actividad que se realiza y no la etiqueta o la tecnología: un mismo servicio puede llamarse plataforma, billetera o protocolo y ser un PSAV si realiza alguna de esas actividades por cuenta de otros.[[2]]</p>
<p><strong>Casos frontera.</strong> La guía de 2021 analiza, entre otros, las monedas estables (<em>stablecoins</em>), los tokens no fungibles (NFT), que en general no se consideran activos virtuales salvo que se usen para pagos o inversiones, y las finanzas descentralizadas (DeFi), donde los creadores, propietarios u operadores que mantienen control o influencia suficiente pueden ser PSAV.[[2]]</p>
""")},
# 2 ------------------------------------------------------------------------------------------
{"title": "Billeteras y cadena de bloques", "html": ess(
"Los activos virtuales se guardan en «billeteras». Si las claves las tiene una empresa, la billetera es custodiada; si las tiene el propio usuario, no lo es. Las transacciones quedan registradas en una cadena de bloques: se pueden rastrear, aunque no siempre se sabe quién está detrás.") + """
<ul>
<li><strong>Billetera custodiada:</strong> un tercero —normalmente un PSAV— controla las claves privadas en nombre del usuario.</li>
<li><strong>Billetera no custodiada</strong> (o «no alojada»): el propio usuario controla sus claves, sin intermediario.[[2]]</li>
<li><strong>Cadena de bloques:</strong> registro distribuido en el que quedan las transacciones; es <strong>seudónimo</strong>, no necesariamente anónimo, porque las direcciones pueden vincularse a personas mediante análisis.</li>
<li><strong>Transacciones entre pares (P2P):</strong> transferencias directas entre billeteras sin la intervención de un PSAV; la guía del GAFI las identifica como un riesgo, porque no pasan por un sujeto obligado que aplique medidas preventivas.[[2]]</li>
</ul>
<div class="callout key"><b>Por qué importa</b>Cuando los fondos llegan al sistema financiero tradicional, casi siempre pasan antes por un PSAV que los convierte a moneda de curso legal. Ese es el punto donde el sujeto obligado puede pedir trazabilidad.</div>
""" + deep("""
<p><strong>Herramientas de análisis.</strong> Existen servicios de análisis de cadena de bloques que asignan puntuaciones de riesgo a direcciones según su vínculo con fraudes, mercados ilícitos o servicios de mezcla. Úsalos como insumo, no como conclusión, y documenta qué herramienta se consultó y cuándo.</p>
<p><strong>Mejoras de anonimato.</strong> La guía de señales de alerta del GAFI menciona las monedas que refuerzan el anonimato y los servicios de mezcla («mixers» o «tumblers») como factores que dificultan rastrear el origen de los fondos.[[3]]</p>
""")},
# 3 ------------------------------------------------------------------------------------------
{"title": "Situación en la República Dominicana", "html": ess(
"En el país, las criptomonedas no son dinero oficial: el Banco Central advirtió que no tienen respaldo ni están autorizadas como medio de pago. Tampoco están prohibidas. Para un sujeto obligado, eso significa que el riesgo existe y hay que gestionarlo.") + """
<p>El Banco Central advirtió en 2017, en cumplimiento de una resolución de la Junta Monetaria, que los activos virtuales <strong>no son moneda de curso legal</strong>, no tienen fuerza liberatoria y no están respaldados ni autorizados como medio de pago. La DGII ha reiterado en sus consultas que no están regulados ni supervisados, aunque tampoco prohibidos.[[4]]</p>
<div class="callout warn"><b>Para el sujeto obligado</b>Que no haya una regulación específica no elimina el riesgo. Los clientes que obtienen ingresos de criptoactivos y los convierten a moneda de curso legal deben poder justificar el origen de esos fondos, igual que cualquier otro.[[4]] La UAF incluye la participación en actividades como las criptomonedas entre las señales de alerta del mercado de valores.[[5]]</div>
<p>La Ley 155-17 obliga a identificar y evaluar los riesgos de los productos, servicios y canales nuevos y existentes, <strong>incluidos los que utilizan nuevas tecnologías</strong>, y a adoptar medidas para mitigarlos (art. 45).[[6]]</p>
""" + deep("""
<p><strong>Ámbito cambiante.</strong> La Recomendación 15 pide a los países regular a los PSAV; varios países de la región han adoptado o están adoptando marcos de registro o licencia. Antes de aplicar este curso, verifica si se ha emitido normativa dominicana nueva y si hay pronunciamientos recientes de la UAF, el Banco Central o los supervisores.[[1]]</p>
""")},
# 4 ------------------------------------------------------------------------------------------
{"title": "Lo que exige el GAFI", "html": ess(
"El GAFI pide que los países regulen y supervisen a quienes prestan servicios con criptoactivos, y que esos proveedores conozcan a sus clientes y envíen con cada transferencia los datos de quien envía y de quien recibe, como hacen los bancos.") + """
<p>La <strong>Recomendación 15</strong> pide a los países y a las entidades identificar y evaluar los riesgos de las nuevas tecnologías y, en particular, que los PSAV estén regulados con fines antilavado, tengan licencia o registro y estén sujetos a supervisión eficaz.[[1]]</p>
<p>Los PSAV deben aplicar las medidas preventivas generales —debida diligencia, conservación de registros, reporte de operaciones sospechosas— y la llamada <strong>«regla de viaje»</strong>: obtener, conservar y transmitir información del originador y del beneficiario en las transferencias de activos virtuales, de forma análoga a las transferencias electrónicas (Recomendación 16).[[1,2]]</p>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Medida</th><th>Qué implica para un PSAV</th></tr></thead>
<tbody>
<tr><td>Licencia o registro</td><td>Estar autorizado o registrado donde fue creado y supervisado.</td></tr>
<tr><td>Debida diligencia</td><td>Identificar y verificar a sus clientes y beneficiarios finales según el riesgo.</td></tr>
<tr><td>Regla de viaje</td><td>Acompañar las transferencias con los datos del originador y del beneficiario.</td></tr>
<tr><td>Sanciones financieras</td><td>Aplicar las sanciones financieras dirigidas de la ONU.</td></tr>
</tbody></table></div>
<p class="note-small">Síntesis de las Recomendaciones 15 y 16 y de la guía del GAFI de 2021.[[1,2]]</p>
""" + deep("""
<p><strong>Analogía con las transferencias.</strong> La Ley 155-17 ya exige a los sujetos obligados financieros identificar al remitente y al beneficiario de las transferencias internacionales y nacionales (arts. 48 y 49).[[6]] La regla de viaje traslada esa lógica a los activos virtuales.</p>
<p><strong>Billeteras no custodiadas.</strong> La guía de 2021 indica que, cuando un PSAV transfiere a o recibe de una billetera no custodiada, debe obtener la información del originador o beneficiario de su cliente y aplicar medidas de mitigación según el riesgo.[[2]]</p>
""")},
# 5 ------------------------------------------------------------------------------------------
{"title": "Señales de alerta", "html": ess(
"El GAFI publicó una lista de señales para criptoactivos: fraccionar montos, mover fondos de inmediato a muchos lugares, usar servicios que borran el rastro, perfiles que no encajan con lo que mueven y fondos ligados a estafas o secuestros de datos.") + """
<p>La guía del GAFI de 2020 organiza los indicadores en categorías como el tamaño y la frecuencia de las transacciones, los patrones de transacción, el anonimato, los remitentes o destinatarios, el origen de los fondos y los riesgos geográficos. Entre ellos:[[3]]</p>
<ul>
<li>Fraccionar operaciones en montos pequeños o justo por debajo de los umbrales de reporte.</li>
<li>Transferir fondos inmediatamente a múltiples PSAV o a jurisdicciones sin regulación adecuada.</li>
<li>Usar servicios de mezcla y monedas que refuerzan el anonimato.</li>
<li>Depositar activos virtuales y retirarlos de inmediato sin actividad intermedia, aceptando comisiones elevadas.</li>
<li>Perfiles de clientes que no son coherentes con el volumen operado (por ejemplo, adultos mayores o estudiantes con grandes movimientos).</li>
<li>Fondos provenientes de direcciones vinculadas a fraudes, ransomware o mercados ilícitos.</li>
</ul>
<div class="callout tip"><b>Recuerda</b>Como en cualquier sector, una señal abre el análisis. La guía advierte que la presencia de un indicador no implica por sí sola actividad delictiva.[[3]]</div>
""" + deep("""
<p><strong>Indicadores geográficos.</strong> Entre ellos, el uso de PSAV ubicados en jurisdicciones sin regulación adecuada o con deficiencias antilavado, o el cambio frecuente de la ubicación declarada.[[3]]</p>
<p><strong>Indicadores del perfil.</strong> La guía también menciona clientes que usan información de identificación falsa o de terceros, cuentas abiertas por personas que parecen actuar bajo instrucciones de otros y la creación de múltiples cuentas por una misma persona.[[3]]</p>
""")},
# 6 ------------------------------------------------------------------------------------------
{"title": "Debida diligencia en la práctica", "html": ess(
"Si un cliente dice que su dinero viene de criptomonedas, hay que pedirle pruebas: de qué plataforma viene, cuándo compró y con qué dinero empezó. Si no puede demostrarlo, se evalúa un reporte.") + """
<div class="case"><b>Caso</b>
<p>Un cliente de un banco empieza a recibir transferencias internacionales frecuentes desde una plataforma de intercambio de criptoactivos. Dice que son «ganancias de trading», pero su perfil es de empleado con ingresos bajos y nunca declaró esa actividad.</p>
<p class="verdict yes"><b>Qué hacer:</b> actualizar su debida diligencia; pedir estados de la plataforma, historial de compras y prueba del capital inicial invertido; recalcular su riesgo. Si no puede sustentar el origen o aparecen otras señales, evaluar un ROS.</p></div>
<ul>
<li>Pregunta por la actividad con criptoactivos desde la vinculación.</li>
<li>Pide evidencia que conecte el capital inicial con fuentes lícitas.</li>
<li>Valora el riesgo de las plataformas y jurisdicciones involucradas.</li>
<li>Recuerda que la reserva sobre cualquier análisis se mantiene (art. 63).[[6]]</li>
</ul>
""" + deep("""
<p><strong>Qué documentos pedir.</strong> Estados de cuenta de la plataforma con la identificación del titular; historial de compras y ventas; comprobantes de los depósitos iniciales en moneda de curso legal desde cuentas propias; y, si declara minería, evidencia de los equipos, el consumo y las recompensas recibidas. Contrasta la identidad del titular de la plataforma con la del cliente.</p>
<p><strong>Y si la entidad quiere ofrecer servicios con criptoactivos.</strong> Para un sujeto obligado financiero, un producto así es un producto nuevo que exige evaluación de riesgos y plan de mitigación antes de lanzarse (art. 45, párrafo).[[6]]</p>
""")},
# 7 ------------------------------------------------------------------------------------------
{"title": "Caso integrador", "html": ess(
"Un caso con varias señales a la vez: dinero de muchas personas que entra, se convierte en criptoactivos y sale enseguida hacia otro país.") + """
<div class="case"><b>Caso · «La cuenta puente»</b>
<p>Una cuenta de ahorro de una persona sin actividad declarada recibe en dos semanas 60 transferencias pequeñas de personas distintas. Cada día, la titular transfiere el saldo a una plataforma de intercambio extranjera. Al consultar, dice que «invierte para un grupo de amigos».</p>
<ol>
<li><strong>Señales:</strong> muchos remitentes sin relación (remitentes), conversión inmediata (patrón), plataforma extranjera (geografía), perfil que no encaja (perfil).[[3]]</li>
<li><strong>Hipótesis:</strong> recaudación de fondos de víctimas de un fraude o de una captación ilegal, canalizada a criptoactivos para dificultar el rastreo.</li>
<li><strong>Acciones:</strong> solicitar soportes y la identificación de los «amigos», revisar si los remitentes reportaron fraudes y actualizar el riesgo.</li>
<li><strong>Decisión:</strong> sin explicación sustentada, ROS dentro de 5 días hábiles. Si hubiera indicios de estafa, recuerda que hoy es delito precedente (curso 8).[[6]]</li>
</ol>
<p class="verdict yes"><b>Lección:</b> el criptoactivo es el medio; la sospecha se construye con las mismas señales de siempre.</p>
</div>
"""},
],
"glossary": [
("Activo virtual", "Representación digital de valor que puede comercializarse o transferirse digitalmente y usarse para pagos o inversiones [[1]]."),
("PSAV", "Proveedor de servicios de activos virtuales: quien, como negocio y por cuenta de otros, intercambia, transfiere o custodia activos virtuales [[1]]."),
("Billetera custodiada", "Billetera cuyas claves controla un tercero en nombre del usuario [[2]]."),
("Billetera no custodiada", "Billetera cuyas claves controla el propio usuario, sin intermediario [[2]]."),
("Cadena de bloques", "Registro distribuido de transacciones; seudónimo, no necesariamente anónimo."),
("Regla de viaje", "Obligación de transmitir los datos del originador y del beneficiario en las transferencias de activos virtuales (R. 16) [[1]]."),
("Mezclador (mixer)", "Servicio que combina fondos de muchos usuarios para dificultar el rastreo [[3]]."),
("Transacción P2P", "Transferencia directa entre billeteras sin intervención de un PSAV [[2]]."),
],
"quiz": [
{"q": "Según el GAFI, ¿qué es un activo virtual?", "options": ["Cualquier depósito bancario digital", "Una representación digital de valor que puede comercializarse o transferirse digitalmente y usarse para pagos o inversiones", "Una moneda de curso legal electrónica", "Un bono del Estado"], "answer": 1, "explain": "Es la definición del GAFI; excluye las representaciones digitales de moneda de curso legal [[1,2]]."},
{"q": "¿Cuál de estas actividades, realizada como negocio por cuenta de otros, convierte a alguien en PSAV?", "options": ["Comprar bitcoin para uno mismo", "Custodiar activos virtuales de clientes", "Leer noticias sobre criptomonedas", "Pagar con tarjeta"], "answer": 1, "explain": "La custodia o administración de activos virtuales por cuenta de otros es una de las actividades de un PSAV [[1]]."},
{"q": "Una billetera no custodiada es aquella en la que:", "options": ["Un banco controla las claves", "El propio usuario controla sus claves sin intermediario", "No se pueden recibir fondos", "El Banco Central guarda los fondos"], "answer": 1, "explain": "En la billetera no custodiada el usuario controla sus claves [[2]]."},
{"q": "¿Cuál es la posición del Banco Central sobre las criptomonedas?", "options": ["Son moneda de curso legal", "No son moneda de curso legal ni están respaldadas o autorizadas como medio de pago", "Están prohibidas con pena de prisión", "Son supervisadas por la UAF"], "answer": 1, "explain": "El aviso de 2017, reiterado por la DGII, señala que no tienen curso legal ni respaldo [[4]]."},
{"q": "¿Qué artículo de la Ley 155-17 obliga a evaluar los riesgos de productos que usan nuevas tecnologías?", "options": ["Art. 2", "Art. 45", "Art. 64", "Art. 80"], "answer": 1, "explain": "El art. 45 exige identificar y evaluar esos riesgos y adoptar medidas para mitigarlos [[6]]."},
{"q": "¿Qué es la «regla de viaje»?", "options": ["Un límite para viajar con criptoactivos", "La obligación de obtener, conservar y transmitir información del originador y del beneficiario en las transferencias de activos virtuales", "Una tasa de cambio", "Un tipo de billetera"], "answer": 1, "explain": "Es la aplicación de la Recomendación 16 a las transferencias de activos virtuales [[1,2]]."},
{"q": "¿Cuál de estas es una señal de alerta del GAFI para activos virtuales?", "options": ["Mantener activos durante años", "Usar servicios de mezcla para ocultar el rastro de los fondos", "Comprar en una plataforma regulada con cuenta verificada", "Declarar las ganancias"], "answer": 1, "explain": "Los mezcladores y las monedas que refuerzan el anonimato figuran entre los indicadores del GAFI [[3]]."},
{"q": "La presencia de un indicador de la guía del GAFI:", "options": ["Prueba un delito", "Abre el análisis, pero no implica por sí sola actividad delictiva", "Obliga a cerrar la cuenta", "Se ignora"], "answer": 1, "explain": "La guía advierte que los indicadores deben analizarse en contexto [[3]]."},
{"q": "Un cliente justifica sus depósitos como ganancias de criptoactivos, pero no aporta evidencia del capital inicial. ¿Qué corresponde?", "options": ["Aceptar la explicación verbal", "Solicitar soportes, actualizar la debida diligencia y evaluar un ROS si no se sustenta", "Cerrar la cuenta sin análisis", "Enviar un RTE"], "answer": 1, "explain": "El origen de los fondos debe justificarse; la falta de soporte, sumada al perfil, puede llevar a un ROS [[4]]."},
{"q": "Que los criptoactivos no estén regulados específicamente en el país significa que:", "options": ["No hay riesgo de lavado", "El sujeto obligado debe igualmente gestionar el riesgo y exigir justificación del origen de fondos", "Están prohibidos", "Solo el Banco Central debe actuar"], "answer": 1, "explain": "La falta de regulación específica no elimina el riesgo; el art. 45 y el enfoque basado en riesgos siguen aplicando [[6]]."},
],
}
