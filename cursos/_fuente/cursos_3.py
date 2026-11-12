"""Curso 08: Reportería (ROS, RAS y RTE). Curso insignia, con ejemplos propios por sector."""
from fuentes import *  # noqa: F401,F403

# Índices de fuentes en este curso:
# 1 LEY · 2 REG · 3 GAFI40 · 4 UAF_ROS · 5 GOAML · 6 TIGA03 · 7 UAF_SEG · 8 UAF_COOP · 9 UAF_CAMB
# 10 UAF_VAL · 11 UAF_CAS · 12 UAF_DGII · 13 LEY_7425 · 14 ESTAFA_7425 · 15 CONCLAFIT_2025_01

SECTORES = """
<div class="tabs">
  <div class="tablist" role="tablist" aria-label="Ejemplos por sector">
    <button type="button" role="tab" id="t-seg" aria-controls="p-seg">Seguros</button>
    <button type="button" role="tab" id="t-coop" aria-controls="p-coop">Cooperativas</button>
    <button type="button" role="tab" id="t-camb" aria-controls="p-camb">Cambio y remesas</button>
    <button type="button" role="tab" id="t-val" aria-controls="p-val">Mercado de valores</button>
    <button type="button" role="tab" id="t-cas" aria-controls="p-cas">Casinos y loterías</button>
    <button type="button" role="tab" id="t-dgii" aria-controls="p-dgii">Supervisados por la DGII</button>
  </div>

  <div class="tabpanel" role="tabpanel" id="p-seg" aria-labelledby="t-seg">
    <h3>Seguros</h3>
    <p><strong>Señales que merecen análisis:</strong> cancelación o rescate anticipado aceptando penalidades sin explicación; primas pagadas con sumas importantes de efectivo sin origen documentado; pagos de pólizas de terceros sin vínculo aparente; cambios frecuentes de beneficiarios; seguros de vida a favor de personas con quienes no se verifica relación; sumas aseguradas desproporcionadas frente a la actividad del cliente.[[7]]</p>
    <div class="case"><b>Caso para analizar</b>
      <p>La Sra. R., que declara trabajar como auxiliar en un colmado, contrata una póliza de vida con prima única elevada. La paga con tres cheques de gerencia emitidos por personas distintas. Seis semanas después solicita el rescate total, acepta perder una parte por penalidad y pide que el reembolso se transfiera a la cuenta de una empresa de importaciones con la que no declaró ninguna relación.</p>
      <p class="verdict yes"><b>¿ROS?</b> Sí, tras el análisis previo. La prima no guarda relación con su perfil, los fondos provienen de terceros, el rescate inmediato con pérdida no tiene lógica económica y el dinero se desvía a un tercero. El patrón es coherente con el uso de la póliza para dar apariencia legítima a fondos.</p>
    </div>
    <div class="case"><b>Caso para comparar</b>
      <p>Un asegurado cambia el beneficiario de su póliza de vida de su excónyuge a sus hijos y presenta la sentencia de divorcio.</p>
      <p class="verdict no"><b>¿ROS?</b> No. El cambio tiene una explicación documentada y coherente.</p>
    </div>
    <div class="callout key"><b>Lo que pide la norma sectorial</b>La norma de prevención de la Superintendencia de Seguros considera de alto riesgo, entre otros, al beneficiario final de los seguros de vida y de retiro con componente de ahorro y a los beneficiarios de pólizas de riesgos generales que cubren bienes de lujo. En los seguros de vida, la aseguradora debe tomar medidas razonables para determinar si los beneficiarios —o el beneficiario final del beneficiario— son PEP, a más tardar al momento del pago.[[16]]</div>
    <div class="callout tip"><b>En goAML</b>Selecciona el nodo correcto, incluye los montos significativos a los que te refieres en el relato y explica la sospecha en detalle; son errores frecuentes del sector.[[7]]</div>
  </div>

  <div class="tabpanel" role="tabpanel" id="p-coop" aria-labelledby="t-coop">
    <h3>Cooperativas</h3>
    <p><strong>Señales que merecen análisis:</strong> depósitos frecuentes en distintas sucursales el mismo día; movimientos fraccionados que se mantienen por debajo de los umbrales; cancelación anticipada de préstamos sin fuente de ingresos que la explique; cuentas abiertas con montos relevantes que se retiran casi de inmediato; uso de la cuenta personal para los flujos de un negocio; empleados o directivos con transacciones fuera de su perfil.[[8]]</p>
    <div class="case"><b>Caso para analizar</b>
      <p>El asociado J., vendedor ambulante con ingresos declarados modestos, realiza en una mañana cuatro depósitos en efectivo en tres sucursales de la misma cooperativa. Cada uno está por debajo de US$15,000, pero en conjunto superan ese monto. Dos días después usa los fondos para saldar por completo un préstamo que vencía en cuatro años y no responde a la solicitud de soportes.</p>
      <p class="verdict yes"><b>¿Qué reportar?</b> Dos cosas distintas: un <strong>RTE</strong>, porque las transacciones en efectivo de un mismo beneficiario en 24 horas se agrupan y superan el umbral (art. 54); y, tras el análisis, un <strong>ROS</strong>, por el fraccionamiento deliberado, la incoherencia con su perfil y la falta de soporte del origen.[[1,8]]</p>
    </div>
    <div class="callout tip"><b>En goAML</b>Explica la sospecha en el campo <em>Razón</em>, no solo en la descripción de la transacción; en <em>Cuenta Mi Cliente</em> registra al signatario de la cuenta, y completa la opción de intermediario solo si realmente lo hubo.[[8]]</div>
  </div>

  <div class="tabpanel" role="tabpanel" id="p-camb" aria-labelledby="t-camb">
    <h3>Agentes de cambio y remesadoras</h3>
    <p><strong>Señales que merecen análisis:</strong> muchos remitentes de distintos lugares hacia un mismo beneficiario sin relación aparente; envíos de montos iguales a varios beneficiarios; clientes que cambian sus datos personales en cada cobro; envíos a países que no son destinos migratorios habituales y sin vínculo con el receptor; canje frecuente de billetes de alta por baja denominación sin relación con la actividad comercial.[[9]]</p>
    <div class="case"><b>Caso para analizar</b>
      <p>En diez días, el Sr. L. cobra remesas de catorce remitentes distintos en tres países, sin relación familiar ni comercial declarada. En cada cobro registra un número de teléfono diferente. Luego envía cerca del 80 % de lo recibido a una persona en un cuarto país, cuya identidad no puede precisar.</p>
      <p class="verdict yes"><b>¿ROS?</b> Sí. La concentración de remitentes sin vínculo, la variación de datos y la redistribución inmediata hacia un tercero apuntan a que podría estar actuando como intermediario de fondos de terceros.</p>
    </div>
    <div class="callout tip"><b>En goAML</b>Completa el monto en moneda extranjera y el origen de la tasa de cambio; indica correctamente país de origen y de destino (no ambos «República Dominicana» en una operación internacional); incluye a todos los involucrados en el flujo multiparte, no solo en el relato, y adjunta los documentos que permitan validar sus nombres.[[9]]</div>
  </div>

  <div class="tabpanel" role="tabpanel" id="p-val" aria-labelledby="t-val">
    <h3>Mercado de valores</h3>
    <p><strong>Señales que merecen análisis:</strong> rescates anticipados de inversiones aceptando penalidades; operaciones repetidas entre las mismas partes con ganancias o pérdidas constantes para una de ellas; precios que no guardan relación con el mercado; clientes sin experiencia que ejecutan operaciones complejas; fondos de terceros sin explicación.[[10]]</p>
    <div class="case"><b>Caso para analizar</b>
      <p>Un inversionista abre una cuenta en un puesto de bolsa y compra cuotas de un fondo con una transferencia proveniente de la cuenta de un tercero. Tres semanas después solicita el rescate anticipado, asume la penalidad y pide que el pago se haga a la cuenta de otra persona distinta. Ante las preguntas, dice que «son amigos que le prestaron».</p>
      <p class="verdict yes"><b>¿ROS?</b> Sí, tras el análisis. El circuito tercero → inversión breve con pérdida → otro tercero no tiene justificación económica y es un patrón típico de estratificación.</p>
    </div>
    <div class="case"><b>Caso para comparar</b>
      <p>Un cliente identificado como PEP invierte en bonos con fondos de su salario y ahorros, documentados y coherentes con su perfil.</p>
      <p class="verdict no"><b>¿ROS?</b> No. Aplica debida diligencia ampliada, pero la condición de PEP no es, por sí sola, motivo de reporte.[[4,10]]</p>
    </div>
    <div class="callout tip"><b>En goAML</b>Identifica la moneda extranjera de la operación, detalla en el campo <em>Razón</em> por qué es sospechosa y anexa los documentos que la sustentan.[[10]]</div>
  </div>

  <div class="tabpanel" role="tabpanel" id="p-cas" aria-labelledby="t-cas">
    <h3>Casinos, juegos de azar y loterías</h3>
    <p><strong>Señales que merecen análisis:</strong> compra de fichas por montos altos para luego apostar cantidades mínimas y pedir el pago; varias personas que cobran boletos premiados comprados por una misma persona; premios significativos repetidos en poco tiempo; billetes de baja denominación en mal estado; clientes que entran y salen reiteradamente sin jugar de forma apreciable.[[11]]</p>
    <div class="case"><b>Caso para analizar</b>
      <p>Un jugador compra fichas con una suma elevada en efectivo, juega veinte minutos con apuestas mínimas y solicita que el saldo se le pague con un cheque a nombre de un familiar, «para tener un comprobante de ganancias».</p>
      <p class="verdict yes"><b>¿Qué reportar?</b> El efectivo recibido supera el umbral especial de los casinos (US$3,000), por lo que se registra para el <strong>RTE</strong>. Además, el patrón de convertir efectivo en un instrumento que aparenta ganancias de juego justifica analizar y remitir un <strong>ROS</strong>.[[1,11]]</p>
    </div>
    <div class="callout tip"><b>En goAML</b>Describe con claridad el contexto: qué compró, cuánto jugó, cómo pidió el pago y por qué no es coherente. Los reportes con poca información son la debilidad más señalada en este sector.[[11]]</div>
  </div>

  <div class="tabpanel" role="tabpanel" id="p-dgii" aria-labelledby="t-dgii">
    <h3>Sujetos obligados supervisados por la DGII</h3>
    <p>Incluye, entre otros, a agentes inmobiliarios, comerciantes de vehículos, joyerías, casas de empeño, abogados, notarios y contadores en las actividades que establece la ley.</p>
    <p><strong>Señales que merecen análisis:</strong> compras pagadas desde múltiples cuentas de terceros; compraventas sucesivas de un mismo bien en poco tiempo con cambios injustificados de valor; vehículos o joyas fuera del perfil del comprador; ventas muy por debajo del precio de mercado; bienes puestos a nombre de parejas, suegros o amigos; cesión de derechos antes de firmar los documentos.[[12]]</p>
    <div class="case"><b>Caso para analizar</b>
      <p>Una persona reserva dos apartamentos en planos. Los pagos iniciales llegan desde cinco cuentas de personas distintas. Antes de firmar el contrato definitivo pide ceder sus derechos a una sociedad constituida hace un mes, cuyo gerente no conoce el proyecto.</p>
      <p class="verdict yes"><b>¿ROS?</b> Sí, tras el análisis: fondos de terceros sin explicación, interposición de una sociedad reciente y posible ocultamiento del beneficiario final.</p>
    </div>
    <div class="case"><b>Caso para comparar</b>
      <p>Un cliente quiere pagar un vehículo en efectivo por encima del límite legal. El vendedor le explica la restricción del art. 64; el cliente paga mediante transferencia desde su propia cuenta y presenta soportes de ingresos coherentes.</p>
      <p class="verdict no"><b>¿ROS?</b> No necesariamente. El desconocimiento de la norma se corrigió y el origen de los fondos está sustentado.[[1,4,15]]</p>
    </div>
    <div class="callout tip"><b>En goAML</b>Anexa contratos de compraventa, matrículas, recibos o facturas: ayudan a validar la sospecha y reducen el tiempo de análisis.[[12]]</div>
  </div>
</div>
"""

COURSES = [
{
"num": 8, "slug": "reporteria-ros-ras-rte", "tag": "Reportería", "level": "Avanzado", "minutes": 50, "featured": True,
"title": "Reportería: ROS, RAS y RTE",
"card": "Cuándo y cómo reportar a la UAF, con ejemplos por sector y uso de goAML.",
"summary": "Aprende a decidir qué reportar a la UAF y cómo hacerlo bien: el Reporte de Transacciones en Efectivo, el Reporte de Operación Sospechosa y el Reporte de Actividad Sospechosa, con ejemplos propios para seis sectores y buenas prácticas en goAML.",
"objectives": [
  "Diferenciar con precisión el RTE, el ROS y el RAS: disparador, plazo y obligatoriedad.",
  "Realizar el análisis previo y redactar un ROS claro con el método de las 5W.",
  "Reconocer situaciones que, por sí solas, no justifican un ROS.",
  "Aplicar lo aprendido a casos de seis sectores de sujetos obligados.",
  "Evitar los errores de llenado más frecuentes en goAML.",
],
"sources": [LEY, REG, GAFI40, UAF_ROS, GOAML, TIGA03, UAF_SEG, UAF_COOP, UAF_CAMB, UAF_VAL, UAF_CAS, UAF_DGII, LEY_7425, ESTAFA_7425, CONCLAFIT_2025_01, SIS_NORMA, LEY_4426, LEY_7425_TXT],
"notice": "Este curso aplica el nuevo Código Penal (Ley 74-25), vigente desde agosto de 2026: la estafa es ahora delito precedente del lavado de activos.",
"modules": [
{"title": "Tres reportes, tres lógicas", "html": """
<p>La reportería es el punto donde el trabajo del sujeto obligado se convierte en inteligencia financiera. Cada reporte responde a una lógica distinta:</p>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th></th><th>RTE</th><th>ROS</th><th>RAS</th></tr></thead>
<tbody>
<tr><td>¿Qué lo activa?</td><td>Un hecho objetivo: transacciones en efectivo que igualan o superan el umbral</td><td>Una operación, realizada o intentada, que genera sospecha tras el análisis</td><td>Información que vincula a un cliente con posibles actividades ilícitas, sin que exista operación</td></tr>
<tr><td>Base</td><td>Arts. 52 a 54, Ley 155-17</td><td>Art. 55, Ley 155-17; Recomendación 20 del GAFI</td><td>No está en la ley; lo habilita la UAF</td></tr>
<tr><td>Plazo</td><td>Los del mes anterior, dentro de los primeros 10 días calendario del mes</td><td>Dentro de 5 días hábiles de realizada o intentada la operación</td><td>Sin plazo legal</td></tr>
<tr><td>¿Obligatorio?</td><td>Sí</td><td>Sí, sin importar el monto</td><td>Opcional</td></tr>
<tr><td>¿Requiere sospecha?</td><td>No</td><td>Sí</td><td>Requiere un vínculo identificado con actividad ilícita</td></tr>
</tbody></table></div>
<p class="note-small">Elaborado a partir de la Ley 155-17, las Recomendaciones del GAFI, la Guía de Calidad ROS y el Manual de goAML.[[1,3,4,5]]</p>
<div class="callout key"><b>Idea clave</b>El RTE se envía porque ocurrió algo medible; el ROS, porque alguien analizó y sospecha; el RAS, porque se conoce algo relevante de un cliente aunque no haya transacción.</div>
"""},
{"title": "El Reporte de Transacciones en Efectivo (RTE)", "html": """
<ul>
<li><strong>Umbral general:</strong> transacciones en efectivo que igualen o superen <strong>US$15,000</strong> o su equivalente.[[1]]</li>
<li><strong>Casinos:</strong> el umbral es de <strong>US$3,000</strong> e incluye transacciones en efectivo, múltiples en efectivo y financieras.[[1]]</li>
<li><strong>Transacciones múltiples:</strong> las realizadas en una misma entidad, en beneficio de una misma persona y dentro de <strong>24 horas</strong>, se suman y se consideran una sola si alcanzan el umbral.[[1]]</li>
<li><strong>Remisión:</strong> las del mes anterior se envían a la UAF dentro de los <strong>primeros diez días calendario</strong>, y se conserva copia al menos diez años.[[1]]</li>
<li><strong>Canal:</strong> la plataforma goAML.[[5]]</li>
</ul>
<div class="callout warn"><b>El fraccionamiento es otra cosa</b>Si un cliente divide operaciones para quedar por debajo del umbral, el RTE puede no activarse, pero la conducta en sí puede ser motivo de un ROS. Un reporte no sustituye al otro.</div>
"""},
{"title": "El Reporte de Operación Sospechosa (ROS)", "html": """
<p>La ley describe las operaciones sospechosas como transacciones, efectuadas o no, complejas, insólitas o significativas, así como patrones no habituales o periódicos, que no tienen un fundamento económico o legal evidente o que generan sospecha de vinculación con el lavado, un delito precedente o el financiamiento del terrorismo.[[1]]</p>
<h3>Lo que no hace falta</h3>
<ul>
<li><strong>Certeza:</strong> no se exige probar el delito ni identificar el tipo penal, aunque, si se tienen elementos, conviene indicarlo.[[4]]</li>
<li><strong>Un monto mínimo:</strong> el deber existe con independencia de la cuantía.[[4]]</li>
<li><strong>Que la operación se concrete:</strong> también se reportan las operaciones intentadas.[[1]]</li>
</ul>
<h3>Lo que sí hace falta: el análisis previo</h3>
<ol class="steps">
<li>Contrastar la operación con el perfil y la debida diligencia del cliente, y actualizarla si hace falta.</li>
<li>Revisar con el área de negocio cómo ha operado el cliente.</li>
<li>Pedir al cliente la documentación que podría justificar la operación.</li>
<li>Decidir y documentar: archivar con justificación, monitorear o reportar.</li>
</ol>
<p>Este análisis evita reportes que no aportan y fortalece los que sí.[[4]]</p>
<h3>Redactar con el método de las 5W</h3>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Pregunta</th><th>Qué debe quedar claro</th></tr></thead>
<tbody>
<tr><td>¿Quién?</td><td>Todas las personas involucradas, con nombre completo, identificación y rol (titular, remitente, beneficiario, apoderado).</td></tr>
<tr><td>¿Qué?</td><td>La operación o el patrón: producto, montos, moneda, frecuencia.</td></tr>
<tr><td>¿Cuándo?</td><td>Fechas o períodos, en orden cronológico.</td></tr>
<tr><td>¿Dónde?</td><td>Sucursal o localidad específica, países de origen y destino.</td></tr>
<tr><td>¿Por qué?</td><td>Las razones concretas de la sospecha: qué no encaja con el perfil, qué explicación faltó, con qué posible delito precedente se relaciona.</td></tr>
</tbody></table></div>
<p>Además, conviene describir el origen y destino de los fondos, la razonabilidad de los hechos frente a la realidad económica del cliente y adjuntar soportes: identificación, documentos de debida diligencia, estados de cuenta, contratos o comprobantes de pago.[[4]]</p>
"""},
{"title": "Lo que, por sí solo, no justifica un ROS", "html": """
<p>Una parte importante de los reportes que recibe la UAF no aporta inteligencia porque describe situaciones que, aisladas, no indican un delito precedente. Algunos ejemplos, a partir de los criterios de la UAF:[[4]]</p>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Situación</th><th>Criterio</th></tr></thead>
<tbody>
<tr><td>El cliente incumplió una política interna o no completó documentos que no exige la normativa antilavado</td><td>No es, por sí sola, un riesgo de LA/FT. Sí sería relevante si busca ocultar al beneficiario final.</td></tr>
<tr><td>El cliente es ilocalizable</td><td>No amerita reporte por sí solo.[[5]]</td></tr>
<tr><td>El cliente es PEP</td><td>Se aplica debida diligencia ampliada; no se reporta por la condición.</td></tr>
<tr><td>Noticia negativa antigua, sin operación actual</td><td>No es un ROS. Si se confirma el vínculo con actividad ilícita, puede enviarse un RAS.</td></tr>
<tr><td>Estafa (simple o agravada)</td><td><strong>Criterio actualizado:</strong> desde agosto de 2026 es delito precedente. Si hay una operación sospechosa vinculada, procede ROS (ver la nota aclaratoria).</td></tr>
<tr><td>Falsificación de un documento privado (por ejemplo, una carta laboral)</td><td><strong>Criterio actualizado:</strong> con el Código Penal vigente, la falsedad se sanciona con 1 a 2 años (art. 348) y no figura en la lista del art. 2, num. 11 de la Ley 155-17; por sí sola no es delito precedente y se denuncia por la vía penal. Excepciones: la falsedad documental agravada (art. 351: habitual o para facilitar una infracción grave o muy grave, 10 a 20 años) y los casos en que el documento falso se usa para cometer otro delito precedente, como una estafa. La falsificación de documentos <strong>públicos</strong> (cédula, pasaporte, actas) sí es delito precedente, porque la ley la menciona expresamente.[[1,17]]</td></tr>
</tbody></table></div>
<div class="callout warn" id="nota-codigo-penal"><b>Nota aclaratoria para los participantes · Nuevo Código Penal</b>
<p>Desde agosto de 2026 está vigente el nuevo Código Penal de la República Dominicana (Ley Orgánica 74-25, con las modificaciones de la Ley 44-26). Este curso aplica el código vigente.[[13,16]]</p>
<ul>
<li>La <strong>estafa simple</strong> (art. 237) se sanciona con <strong>tres a cinco años</strong> de prisión; la estafa agravada, la colectiva y la piramidal (arts. 238 a 242), con cinco a diez años.[[14]]</li>
<li>Como la Ley 155-17 considera infracción precedente toda infracción grave con pena no menor de tres años (art. 2, num. 11), <strong>toda estafa es hoy delito precedente del lavado de activos</strong>.[[1]]</li>
<li>Por tanto, una operación realizada o intentada que genere sospecha de estar vinculada a una estafa <strong>debe reportarse mediante ROS</strong>, además de orientar a las víctimas a denunciar.</li>
</ul>
<p><strong>Falsificación de documentos privados:</strong> la falsedad simple del art. 348 se castiga con 1 a 2 años, por lo que, aislada, sigue sin ser delito precedente. Pero si una carta laboral o un estado de cuenta falsos se usan para obtener un préstamo o un pago, la conducta puede constituir una estafa, y esta sí lo es. Analiza siempre para qué se usó el documento.[[17]]</p>
<p>La Guía de Calidad de la UAF (enero 2024) indicaba lo contrario para la estafa simple porque se basaba en el Código Penal de 1884, que la castigaba con menos de tres años. Ese criterio quedó superado por el nuevo código. Si encuentras material anterior con esa indicación, aplica la norma vigente.[[4]]</p>
</div>
"""},
{"title": "El Reporte de Actividad Sospechosa (RAS)", "html": """
<p>El RAS permite comunicar a la UAF situaciones en las que <strong>no hubo transacción ni intento</strong>, pero se identificó un posible vínculo de un cliente con lavado, delitos precedentes, financiamiento del terrorismo o de la proliferación. Sus rasgos:[[4,5]]</p>
<ul>
<li>No está contemplado en la Ley 155-17; es <strong>opcional</strong>.</li>
<li>No requiere una operación realizada o intentada.</li>
<li>Puede basarse en información reputacional (noticias negativas) o en coincidencias en listas como las de sanciones.</li>
<li>Ayuda a la entidad a gestionar su riesgo reputacional y aporta a las labores de inteligencia de la UAF.</li>
</ul>
<div class="callout warn"><b>Excepción que no es RAS</b>Si un cliente o potencial cliente <strong>se niega</strong> a entregar información de debida diligencia, la ley exige un <strong>ROS</strong> (art. 62), no un RAS.[[1,5]]</div>
<div class="case"><b>Caso</b><p>Durante la revisión periódica, se encuentra que un cliente aparece en la prensa reciente como investigado por contrabando. No ha realizado transacciones inusuales.</p>
<p class="verdict no"><b>Decisión:</b> RAS opcional (y revisión de su calificación de riesgo). Si luego realiza operaciones incoherentes con su perfil, el análisis puede derivar en un ROS.</p></div>
"""},
{"title": "Confidencialidad, protección y consecuencias", "html": """
<ul>
<li><strong>Reserva absoluta:</strong> ni la entidad ni sus directores o empleados pueden revelar a terceros que se remitió información a la UAF o que se examina una operación (art. 63; Recomendación 21 del GAFI). La UAF incluye en «terceros» a los auditores internos y externos.[[1,3,4]]</li>
<li><strong>Protección:</strong> reportar de buena fe no genera responsabilidad civil, administrativa ni penal (art. 58).[[1]]</li>
<li><strong>Consecuencias de no reportar:</strong> es una infracción administrativa muy grave (art. 69); el retraso en remitir información es una infracción leve (art. 71).[[1]]</li>
<li><strong>Naturaleza del ROS:</strong> no es una denuncia penal ni una prueba. La UAF analiza y, si corresponde, comparte inteligencia con las autoridades; no ejerce la acción penal.[[4]]</li>
<li><strong>Revelar la identidad</strong> de quien elaboró el reporte también está sancionado.[[4]]</li>
</ul>
"""},
{"title": "goAML en la práctica", "html": """
<p>goAML es la plataforma de la UAF para recibir los reportes de los sujetos obligados.[[5]]</p>
<h3>Registro</h3>
<ol class="steps">
<li>Desde el portal de goAML, elegir «Regístrese» y la opción <em>Entidad que reporta</em>.</li>
<li>Completar las secciones de <strong>Organización</strong>, <strong>Administrador</strong> (normalmente el oficial de cumplimiento, que luego gestiona usuarios y permisos) y <strong>Archivos adjuntos</strong> en PDF que acrediten la designación.</li>
<li>Revisar la vista previa y enviar; la confirmación llega por correo y luego pueden añadirse usuarios adicionales.</li>
</ol>
<p>Los campos numéricos (RNC, cédula, teléfono) se digitan <strong>sin guiones, espacios ni paréntesis</strong>. Todo sujeto obligado debe estar registrado aunque aún no haya tenido nada que reportar.[[4,6]]</p>
<h3>Errores que provocan rechazos</h3>
<ul>
<li>Campo de razón o motivo sin una explicación real de la sospecha.</li>
<li>Identificaciones con dígitos incorrectos o con guiones; fechas equivocadas.</li>
<li>Moneda no identificada; países de origen y destino vacíos o ambos «República Dominicana» en operaciones internacionales.</li>
<li>Estructura de flujo equivocada (por ejemplo, registrar un retiro como depósito).</li>
<li>Involucrados mencionados solo en el relato y no en las partes de la transacción.</li>
<li>Omitir el beneficiario final o la identificación del reportado.</li>
<li>Sucursal: indicar la localidad donde ocurrió la operación, no la oficina principal.</li>
</ul>
<p>Si un reporte es rechazado, el usuario puede ver el motivo, revertirlo, corregirlo desde «Reportes redactados» y reenviarlo.[[4,5]]</p>
"""},
{"title": "Ejemplos por sector", "html": """
<p>Los siguientes casos son <strong>hipotéticos y de elaboración propia</strong>, construidos a partir de las señales de alerta que la UAF ha identificado para cada sector. Recuerda: una señal de alerta abre el análisis, no lo cierra.</p>
""" + SECTORES},
],
"quiz": [
{"q": "Un cliente deposita en efectivo US$9,000 por la mañana y US$7,000 por la tarde en la misma entidad, a su favor. ¿Qué corresponde según la ley?", "options": ["Nada, ninguna supera el umbral", "Agruparlas como una sola transacción y reportarla en el RTE", "Solo un RAS", "Esperar al día siguiente"], "answer": 1, "explain": "El art. 54 agrupa las transacciones múltiples en efectivo de una misma persona en 24 horas que, sumadas, alcanzan US$15,000 [[1]]."},
{"q": "¿Cuál es el umbral del RTE para los casinos?", "options": ["US$15,000", "US$10,000", "US$3,000", "No reportan RTE"], "answer": 2, "explain": "El párrafo del art. 52 fija US$3,000 para los casinos [[1]]."},
{"q": "¿Cuándo deben remitirse los RTE a la UAF?", "options": ["Dentro de 5 días hábiles", "Los del mes anterior, dentro de los primeros 10 días calendario", "Una vez al año", "Solo cuando hay sospecha"], "answer": 1, "explain": "El art. 53 establece la remisión dentro de los primeros diez días calendario del mes siguiente [[1]]."},
{"q": "Un cliente intentó una operación sospechosa, pero desistió al pedírsele documentos. ¿Procede ROS?", "options": ["No, porque no se concretó", "Sí, el ROS abarca operaciones realizadas o intentadas", "Solo si superó US$15,000", "Solo un RAS"], "answer": 1, "explain": "El art. 55 cuenta el plazo desde que la operación fue realizada o intentada [[1]]."},
{"q": "¿Cuál afirmación sobre el ROS es correcta?", "options": ["Hay que probar el delito antes de reportar", "No se requiere certeza del delito, pero sí un análisis previo que sustente la sospecha", "Solo se reportan montos altos", "Es una denuncia penal"], "answer": 1, "explain": "La UAF aclara que no se requiere certeza ni identificar el tipo penal, pero sí analizar antes de reportar [[4]]."},
{"q": "Un cliente aparece en una noticia de hace diez años por un delito ya juzgado y no tiene operaciones inusuales. ¿Qué reporte corresponde?", "options": ["ROS obligatorio", "No es un ROS; si se confirma un vínculo relevante, un RAS opcional", "RTE", "Ninguno nunca"], "answer": 1, "explain": "Sin operación ni intento, una noticia negativa no genera ROS; puede valorarse un RAS [[4]]."},
{"q": "Un potencial cliente se niega a entregar información para su identificación. ¿Qué exige la ley?", "options": ["Un RAS", "Un ROS", "Nada si no abrió cuenta", "Un RTE"], "answer": 1, "explain": "El art. 62 ordena realizar un ROS cuando el potencial cliente se niega a aportar información para su identificación [[1,5]]."},
{"q": "El auditor externo pide la lista de ROS enviados para su revisión. Según la UAF y el art. 63:", "options": ["Se le entrega sin restricción", "La prohibición de revelar alcanza también a auditores internos y externos", "Solo si firma un acuerdo", "Se le entrega una copia parcial"], "answer": 1, "explain": "La UAF incluye a los auditores internos y externos dentro de «terceros» a quienes no se debe revelar la existencia de un ROS [[1,4]]."},
{"q": "En una remesa internacional, ¿qué error de goAML provoca rechazos con frecuencia?", "options": ["Incluir el monto en moneda extranjera", "Dejar vacíos los países de origen y destino o poner ambos como República Dominicana", "Adjuntar documentos", "Detallar la razón de la sospecha"], "answer": 1, "explain": "Es uno de los errores identificados por la UAF en reportes de transacciones internacionales [[4,9]]."},
{"q": "Una cliente recibe decenas de pagos por ventas en redes sociales que nunca entrega, y el análisis confirma el patrón. Con el Código Penal vigente, ¿qué corresponde?", "options": ["Nada: la estafa simple no es delito precedente", "Remitir un ROS, porque la estafa (art. 237, 3 a 5 años) es hoy delito precedente, y orientar a las víctimas a denunciar", "Enviar solo un RTE", "Esperar una sentencia condenatoria"], "answer": 1, "explain": "Con la Ley 74-25 la estafa simple se sanciona con 3 a 5 años, por lo que alcanza el umbral de infracción precedente del art. 2, num. 11 de la Ley 155-17; el criterio contrario de la guía de 2024 se basaba en el código de 1884 [[1,4,13,14]]."},
],
},
]
