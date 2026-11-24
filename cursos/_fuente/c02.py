"""Curso 02 · Marco regulatorio dominicano y Ley 155-17."""
from fuentes import *  # noqa: F401,F403
from capas import ess, deep

# Fuentes: 1 LEY · 2 REG · 3 GAFI40 · 4 DGII_N01 · 5 UAF_ROS · 6 CONCLAFIT_2024 · 7 CONCLAFIT_2025_NOTA
# 8 CONCLAFIT_2025_02 · 9 SIS_NORMA · 10 IDECOOP_NORMA · 11 CNV_NORMA · 12 CASINOS_104 · 13 SIB_DD · 14 DGII_N02 · 15 DEC_407
COURSE = {
"num": 2, "slug": "marco-regulatorio-ley-155-17", "tag": "Regulación", "level": "Básico → Profesional", "minutes": 55,
"title": "Marco regulatorio dominicano y Ley 155-17",
"card": "La ley, su reglamento, los sujetos obligados, sus deberes y el régimen de sanciones.",
"summary": "Recorre la arquitectura normativa dominicana contra el lavado de activos: qué dice la Ley 155-17 y sus reglamentos, quiénes son sujetos obligados, qué programa de cumplimiento deben tener, qué reportes y plazos aplican, cuáles son los límites al efectivo y qué consecuencias tiene incumplir.",
"objectives": [
  "Ubicar la Ley 155-17, sus reglamentos y las normas sectoriales dentro del sistema.",
  "Determinar si una actividad es sujeto obligado financiero o no financiero, y cuándo.",
  "Enumerar los componentes obligatorios del programa de cumplimiento.",
  "Aplicar los reportes, plazos y límites al uso del efectivo que fija la ley.",
  "Clasificar las infracciones administrativas y conocer sus multas vigentes, su gradualidad y su prescripción.",
],
"sources": [LEY, REG, GAFI40, DGII_N01, UAF_ROS, CONCLAFIT_2024, CONCLAFIT_2025_NOTA, CONCLAFIT_2025_02, SIS_NORMA, IDECOOP_NORMA, CNV_NORMA, CASINOS_104, SIB_DD, DGII_N02, DEC_407],
"modules": [
# 1 ------------------------------------------------------------------------------------------
{"title": "La arquitectura normativa", "html": ess(
"Las reglas contra el lavado de activos en el país están en capas: una ley general, decretos que la desarrollan y normas de cada supervisor que la adaptan a su sector. Encima de todo están los estándares internacionales del GAFI. Para cumplir hay que conocer las capas que aplican a tu actividad.") + """
<ul>
<li><strong>Ley 155-17</strong> (1 de junio de 2017): tipifica el lavado y el financiamiento del terrorismo, define a los sujetos obligados y sus deberes, organiza las instituciones y fija las sanciones. Sustituyó a la Ley 72-02.[[1]]</li>
<li><strong>Decreto 408-17</strong>: reglamento de aplicación de la ley; desarrolla, entre otros temas, la debida diligencia, las PEP, el beneficiario final, los medios de pago y el plazo para responder a la UAF.[[2]]</li>
<li><strong>Decreto 407-17</strong>: reglamento sobre el congelamiento preventivo de bienes vinculados al terrorismo y a la proliferación, en aplicación de las listas del Consejo de Seguridad de la ONU.[[15]]</li>
<li><strong>Normas sectoriales</strong> de cada supervisor, que regulan el alcance y la forma de aplicar la ley según las realidades y riesgos de cada sector (Decreto 408-17, art. 3).[[2]]</li>
<li><strong>Resoluciones del CONCLAFIT</strong>, que actualizan multas y umbrales o precisan el alcance de la ley (por ejemplo, las Resoluciones CONCLAFIT-2024-01 y 2025-02).[[6,8]]</li>
<li><strong>Estándares internacionales</strong>: las 40 Recomendaciones del GAFI y sus notas interpretativas, que el reglamento ordena tomar en cuenta al interpretar las normas de prevención (Decreto 408-17, art. 45).[[2,3]]</li>
</ul>
<div class="callout tip"><b>En la práctica</b>Los sujetos obligados deben cumplir a la vez la ley, sus reglamentos y la normativa de su supervisor (Decreto 408-17, art. 2).[[2]] Cuando la norma sectorial pide más que la ley, se cumple lo más exigente.</div>
""" + deep("""
<p><strong>Ejemplos de normativa sectorial en la bibliografía de este curso:</strong></p>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Sector</th><th>Norma</th></tr></thead>
<tbody>
<tr><td>Bancos y fiduciarias</td><td>Instructivo sobre Debida Diligencia de la Superintendencia de Bancos (2.ª versión, Circular SIB 012/17; la SB puso en vigencia una 3.ª versión con la Circular SB 005/22).[[13]]</td></tr>
<tr><td>Seguros</td><td>Norma de la Superintendencia de Seguros para el sector seguros (2 de noviembre de 2017).[[9]]</td></tr>
<tr><td>Mercado de valores</td><td>Norma aprobada por la Primera Resolución del Consejo Nacional de Valores R-CNV-2017-24-MV.[[11]]</td></tr>
<tr><td>Cooperativas</td><td>Norma 001-17 del IDECOOP.[[10]]</td></tr>
<tr><td>Casinos y juegos de azar</td><td>Resolución 104-2017 del Ministerio de Hacienda.[[12]]</td></tr>
<tr><td>No financieros supervisados por la DGII</td><td>Normas Generales 01-2018 (factoraje y profesionales jurídicos y contables) y 02-2018 (vehículos, barcos y aviones), entre otras.[[4,14]]</td></tr>
</tbody></table></div>
<p class="note-small">La lista no es exhaustiva y las normas se actualizan: verifica siempre la versión vigente con tu supervisor.</p>
<p><strong>Interpretación.</strong> El reglamento permite una interpretación analógica o extensiva conforme a las Recomendaciones del GAFI, <em>salvo</em> en los aspectos administrativos sancionatorios (Decreto 408-17, art. 45).[[2]] Las sanciones, por tanto, se aplican de forma estricta.</p>
""")},
# 2 ------------------------------------------------------------------------------------------
{"title": "¿Quiénes están obligados?", "html": ess(
"La ley no obliga a todo el mundo: obliga a las actividades que pueden ser usadas para lavar dinero. Son de dos tipos: las financieras (bancos, aseguradoras, casas de cambio…) y las no financieras (inmobiliarias, joyerías, casinos, abogados en ciertas tareas…). En algunos casos, la obligación depende de qué hace la persona, no de su profesión.") + """
<p>La ley distingue dos grandes grupos.[[1]]</p>
<div class="grid-2">
<div class="mini"><h4>Sujetos obligados financieros (art. 32)</h4><p>Entidades de intermediación financiera; intermediarios de valores; agentes de cambio y remesadoras; el Banco Central; fiduciarias; cooperativas de ahorro y crédito; compañías de seguros, reaseguros y corredores; administradoras de fondos de inversión; titularizadoras; puestos de bolsa; depósito centralizado de valores; y emisores de oferta pública que se reserven la colocación primaria.</p></div>
<div class="mini"><h4>Sujetos obligados no financieros (art. 33)</h4><p>Casinos, juegos de azar, bancas de lotería y apuestas; factoraje; agentes inmobiliarios en compraventas para clientes; comerciantes de metales y piedras preciosas y joyas; abogados, notarios, contadores y otros profesionales jurídicos en ciertas actividades; comerciantes habituales de vehículos, armas, barcos y aviones; casas de empeño; y empresas constructoras.</p></div>
</div>
<h3>Profesionales: obligados por lo que hacen</h3>
<p>Abogados, notarios y contadores son sujetos obligados cuando realizan para sus clientes actividades como compraventa o remodelación de inmuebles, administración de dinero o cuentas, constitución o administración de sociedades, compraventa de acciones, provisión de domicilio o actuación como director o accionista nominal (art. 33, lit. e).[[1]] La DGII precisa que no son sujetos obligados quienes no realicen al menos una de esas actividades, y que en los servicios mixtos la condición se activa en cuanto ofrecen o realizan una de ellas.[[4]]</p>
<div class="callout key"><b>Novedad 2025: empresas constructoras</b>El CONCLAFIT aclaró (Resolución CONCLAFIT-2025-02, 26 de noviembre de 2025) que las constructoras solo son sujetos obligados no financieros cuando intervienen en compraventas de bienes raíces, como compradoras o vendedoras, o cuando promueven y ponen en contacto a compradores y vendedores a cambio de una comisión. La condición no depende del objeto social, sino del riesgo de la actividad concreta.[[8]]</div>
""" + deep("""
<p><strong>Nuevos sujetos obligados.</strong> El Comité Nacional puede, reglamentariamente, incluir como sujetos obligados a quienes realicen otras actividades que presenten riesgos (arts. 32 y 33, párrafos; art. 89, num. 13).[[1]]</p>
<p><strong>Secreto profesional del abogado.</strong> La Norma 01-2018 indica que los abogados no tienen que reportar transacciones sospechosas si la información se obtuvo de un cliente en el desempeño de su tarea de defenderlo o representarlo en procesos judiciales o con respecto a ellos (art. 40, párrafo).[[4]] Fuera de ese supuesto, el secreto profesional no impide cumplir las obligaciones de prevención (Ley 155-17, art. 57).[[1]]</p>
<p><strong>Agentes inmobiliarios y constructoras.</strong> El reglamento les exige debida diligencia cuando intervienen en compraventas de bienes raíces para sus clientes, sean compradores o vendedores (Decreto 408-17, art. 16, párrafo II), criterio que la Resolución CONCLAFIT-2025-02 retoma.[[2,8]]</p>
""")},
# 3 ------------------------------------------------------------------------------------------
{"title": "El programa de cumplimiento", "html": ess(
"Cada sujeto obligado debe tener un programa de cumplimiento: un conjunto de reglas, personas y controles para no ser usado por delincuentes. Debe ser proporcional a su tamaño y a sus riesgos: una joyería pequeña no necesita lo mismo que un banco, pero ambos necesitan lo esencial.") + """
<p>La ley exige un programa de cumplimiento <strong>basado en riesgo</strong>, adecuado a la organización, estructura, recursos y complejidad de las operaciones, que contenga como mínimo (art. 34):[[1]]</p>
<ol class="steps">
<li>Políticas y procedimientos para evaluar y mitigar los riesgos de lavado y financiamiento del terrorismo.</li>
<li>Políticas para altos estándares de contratación y capacitación permanente de funcionarios, empleados y directores.</li>
<li>Un régimen de sanciones disciplinarias.</li>
<li>Un código de ética y buena conducta.</li>
<li>Una auditoría externa que verifique la efectividad del programa.</li>
</ol>
<p>Además, debe designarse un <strong>oficial de cumplimiento</strong>: un ejecutivo de alto nivel, con capacidad técnica, que vigile el programa y sirva de enlace con la UAF y el supervisor (art. 44).[[1]] El programa se aplica también a las filiales locales y subsidiarias en el extranjero (art. 35).[[1]]</p>
<h3>Cómo lo aterrizan las normas sectoriales</h3>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Aspecto</th><th>Ejemplos de la normativa sectorial</th></tr></thead>
<tbody>
<tr><td>Manual</td><td>Seguros: aprobado por la junta directiva y revisado como mínimo cada dos años o ante cambios regulatorios u organizativos.[[9]] DGII: aprobado por la más alta directiva y actualizado ante cambios normativos o de estructura.[[4]]</td></tr>
<tr><td>Capacitación</td><td>DGII: al menos una vez al año para el personal de contacto con clientes y un mínimo de 12 horas anuales de formación especializada para el oficial de cumplimiento.[[4]] Seguros: capacitación especializada anual del oficial y anual para el personal comercial y de nuevo ingreso.[[9]]</td></tr>
<tr><td>Auditoría externa</td><td>Seguros: anual.[[9]] DGII (Norma 01-2018): como mínimo cada dos años.[[4]] Cooperativas con más de RD$5 millones de ingresos brutos anuales: auditoría interna y externa anual.[[10]]</td></tr>
<tr><td>Comité de cumplimiento</td><td>Seguros: integrado al menos por el gerente general, un representante del consejo y el oficial de cumplimiento, con reuniones como mínimo cada tres meses.[[9]] Cooperativas: obligatorio por encima del umbral de RD$5 millones.[[10]]</td></tr>
</tbody></table></div>
""" + deep("""
<p><strong>Auditoría proporcional.</strong> Para sujetos obligados no financieros que sean micro, pequeñas y medianas empresas o personas físicas, la auditoría puede consistir en un dictamen de cumplimiento de un contador público autorizado o de un profesional calificado en prevención, realizado como máximo cada tres años (Decreto 408-17, art. 23, párrafo II).[[2]] Las normas sectoriales pueden fijar plazos más exigentes: por ejemplo, la Norma 02-2018 de la DGII pide auditoría cada dos años a las personas físicas y anual a las demás.[[14]]</p>
<p><strong>Oficial de cumplimiento en sujetos pequeños.</strong> En los sujetos obligados que son personas físicas, sus responsabilidades pueden recaer en la propia persona (Decreto 408-17, art. 28).[[2]] La DGII exige que el oficial se registre en la UAF, que su designación se informe a la DGII dentro de 10 días hábiles, que tenga independencia, jerarquía y acceso irrestricto a la información, y que no sea una persona jurídica.[[4]] En seguros, la función puede recaer en el dueño o administrador general cuando el sujeto obligado tiene menos de 30 empleados.[[9]]</p>
<p><strong>Grupos.</strong> Los grupos financieros y económicos pueden tener un programa de cumplimiento unificado (art. 34, párrafo).[[1]]</p>
""")},
# 4 ------------------------------------------------------------------------------------------
{"title": "Las obligaciones del día a día", "html": ess(
"Además del programa, la ley fija tareas concretas: conocer al cliente, conservar los documentos diez años, reportar el efectivo grande cada mes, reportar lo sospechoso en cinco días hábiles, revisar las listas de la ONU y no contarle nada al cliente. Cada una tiene su artículo y su plazo.") + """
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Obligación</th><th>Lo esencial</th><th>Base</th></tr></thead>
<tbody>
<tr><td>Gestión de riesgos</td><td>Metodología que considere como mínimo clientes, productos y servicios, áreas geográficas y canales.</td><td>Art. 37</td></tr>
<tr><td>Debida diligencia</td><td>Basada en riesgos; identificar y verificar al cliente y al beneficiario final, entender el propósito de la relación y monitorearla.</td><td>Arts. 36 a 42</td></tr>
<tr><td>Factores de alto riesgo</td><td>Como mínimo, las PEP y las operaciones con jurisdicciones definidas por el GAFI.</td><td>Art. 46</td></tr>
<tr><td>Nuevos productos y tecnologías</td><td>Evaluar sus riesgos; los financieros deben presentar una evaluación y un plan de mitigación al lanzarlos.</td><td>Art. 45</td></tr>
<tr><td>Conservación de registros</td><td>Al menos 10 años después de terminada la relación o la transacción ocasional.</td><td>Art. 43</td></tr>
<tr><td>Transacciones en efectivo</td><td>Registrar y reportar las que igualen o superen US$15,000 (US$3,000 en casinos), incluidas las múltiples en 24 horas.</td><td>Arts. 52 a 54</td></tr>
<tr><td>Operaciones sospechosas</td><td>Reportar a la UAF dentro de 5 días hábiles de realizada o intentada la operación.</td><td>Art. 55</td></tr>
<tr><td>Listas de la ONU</td><td>Monitorear clientes y beneficiarios finales; congelar sin demora si hay coincidencia.</td><td>Arts. 82 y 83</td></tr>
<tr><td>Reserva</td><td>No revelar que se reportó o que se examina una operación.</td><td>Art. 63</td></tr>
</tbody></table></div>
<p class="note-small">Elaborado a partir de la Ley 155-17.[[1]] Cada obligación se estudia a fondo en los cursos siguientes.</p>
<h3>Prohibiciones expresas</h3>
<ul>
<li>Relacionarse u operar con <strong>bancos pantalla</strong> (art. 60).</li>
<li>Abrir cuentas u ofrecer servicios con nombres falsos, cifrados o anónimos (art. 61).</li>
<li>Iniciar o mantener una relación, o hacer una transacción, sin poder identificar y verificar al cliente; si el potencial cliente se niega a dar información, debe remitirse un ROS (art. 62).[[1]]</li>
</ul>
""" + deep("""
<p><strong>Respuesta a la UAF.</strong> Cuando la UAF requiere información, el sujeto obligado debe entregarla en un plazo no mayor de 10 días laborables, o menor si la UAF lo dispone por urgencia, especificidad, antigüedad o volumen (Decreto 408-17, art. 25).[[2]] Algunas normas sectoriales fijan plazos propios para solicitudes de información adicional; la de seguros, por ejemplo, prevé 5 días laborables para que el oficial responda a la UAF.[[9]]</p>
<p><strong>Reportes a la DGII.</strong> Los sujetos obligados de la Norma 01-2018 envían a la DGII un reporte <em>estadístico</em> de los ROS remitidos (cantidad, montos, oficinas y fechas, sin información del contenido) dentro de los 15 días hábiles del mes siguiente, y un reporte trimestral de información de riesgo de su cartera de clientes.[[4]]</p>
<p><strong>Formato de los reportes.</strong> La UAF define el formato, la vía y el contenido de los ROS y RTE mediante instructivo publicado en su página web (Decreto 408-17, art. 26).[[2]]</p>
""")},
# 5 ------------------------------------------------------------------------------------------
{"title": "Límites al uso del efectivo (art. 64)", "html": ess(
"Para ciertas compras grandes —una casa, un carro, joyas, acciones de una empresa, premios— la ley prohíbe pagar en efectivo por encima de un monto. Hay que usar transferencias, cheques o tarjetas, que dejan rastro. Los notarios y registradores no deben formalizar esas operaciones si no se demuestra cómo se pagó.") + """
<p>La ley prohíbe a <strong>toda persona</strong> liquidar o pagar, y aceptar el pago, en efectivo o metales preciosos por encima de ciertos montos en operaciones como: inmuebles; vehículos, aeronaves y embarcaciones; relojes, joyas y obras de arte; boletos y premios de juegos y sorteos; participación en casinos y loterías; acciones o partes sociales; y derechos de uso sobre esos bienes (art. 64).[[1]]</p>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Literal</th><th>Operación</th><th>Umbral original de la ley</th></tr></thead>
<tbody>
<tr><td>a)</td><td>Inmuebles</td><td>Más de RD$1,000,000</td></tr>
<tr><td>b)</td><td>Vehículos de motor, aeronaves y embarcaciones</td><td>Más de RD$500,000</td></tr>
<tr><td>c)</td><td>Relojes, joyas y obras de arte</td><td>Más de RD$450,000</td></tr>
<tr><td>d) a g)</td><td>Juegos, sorteos y premios; casinos; acciones; derechos de uso</td><td>Más de RD$250,000</td></tr>
</tbody></table></div>
<div class="callout warn"><b>Los umbrales cambiaron</b>El propio art. 64 permite al CONCLAFIT indexarlos. La Resolución CONCLAFIT-2025-01 los aumentó; su nota aclaratoria del 10 de diciembre de 2025 precisa que para los literales d), e), f) y g) el monto correcto es <strong>RD$400,000</strong>. Antes de aplicar los límites de los literales a), b) y c), consulta el texto completo de esa resolución, que no forma parte de la bibliografía de este curso.[[1,7]]</div>
<p>Los pagos por encima del umbral deben hacerse por depósito a cuenta, cheque, transferencia (incluidas las remesadoras), tarjeta u otro instrumento distinto del efectivo que dé fe del pago (Decreto 408-17, art. 29).[[2]]</p>
""" + deep("""
<p><strong>Notarios y registradores.</strong> Deben abstenerse de instrumentar o registrar las operaciones en efectivo prohibidas salvo que se les entregue constancia fehaciente del medio de pago (art. 64, párrafo II).[[1]] El reglamento aclara que su responsabilidad se limita a exigir esa constancia: no deben hacer debida diligencia del cliente ni pedir prueba del origen de los fondos para registrar; conservan las constancias diez años y solo las entregan a la UAF, a los jueces o al Ministerio Público (Decreto 408-17, arts. 30 y 31).[[2]]</p>
<p><strong>Pagos en cuotas, permutas y daciones.</strong> El reglamento regula cómo acreditar el medio de pago en ventas a plazos, permutas, daciones en pago y suscripción de acciones (Decreto 408-17, art. 29, párrafos II a V).[[2]]</p>
<p><strong>Consecuencias.</strong> Incumplir el art. 64 es infracción administrativa muy grave (art. 69, lit. i) y el notario o registrador que participa sin constancia comete un delito (art. 4, num. 11).[[1]]</p>
""")},
# 6 ------------------------------------------------------------------------------------------
{"title": "Infracciones y multas vigentes", "html": ess(
"Incumplir las obligaciones de prevención trae multas que pueden superar los trece millones de pesos, además de sanciones para los directivos, suspensión de licencias y publicación de la sanción. La gravedad depende de qué se incumplió: no reportar lo sospechoso es de lo más grave.") + """
<p>La ley clasifica las infracciones administrativas en muy graves, graves y leves (art. 68). El órgano que sanciona es el supervisor del sujeto obligado, con respeto al debido proceso de la Ley 107-13 (arts. 66 y 67).[[1]]</p>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Tipo</th><th>Ejemplos (Ley 155-17)</th><th>Sector financiero (art. 74)</th><th>No financiero (art. 75)</th></tr></thead>
<tbody>
<tr><td>Muy grave (art. 69)</td><td>No reportar operaciones sospechosas; no colaborar con la UAF; obstruir la supervisión; incumplir el art. 64 o el congelamiento; fallas en identificación, debida diligencia, monitoreo o conservación de registros</td><td>RD$6,962,014 a RD$13,924,025</td><td>RD$2,784,806 a RD$5,569,610</td></tr>
<tr><td>Grave (art. 70)</td><td>No identificar riesgos; no enviar reportes periódicos; no designar oficial; no tener manual, auditoría externa o capacitación; no aplicar medidas a filiales extranjeras</td><td>RD$3,481,008 a RD$6,962,012</td><td>RD$1,392,404 a RD$2,784,805</td></tr>
<tr><td>Leve (art. 71)</td><td>Retrasos en entregar información o reportes; incumplir normativas sectoriales</td><td>RD$1,392,402 a RD$3,481,006</td><td>RD$417,721 a RD$1,392,402</td></tr>
</tbody></table></div>
<p class="note-small">Montos actualizados por la Resolución CONCLAFIT-2024-01 (3 de julio de 2024), según el Índice de Precios al Consumidor.[[6]] Los montos originales de la ley iban de RD$1,000,000 a RD$10,000,000 (financiero) y de RD$300,000 a RD$4,000,000 (no financiero).[[1]]</p>
<h3>Directivos y otras consecuencias</h3>
<ul>
<li>A quienes ejercen cargos de administración o dirección responsables de una infracción muy grave: multa de <strong>RD$696,201 a RD$4,177,207</strong> cada uno (art. 78, montos actualizados) y separación del cargo con inhabilitación de hasta 10 años.[[1,6]]</li>
<li>Suspensión o revocación de la licencia en faltas muy graves o reincidencia (art. 76).[[1]]</li>
<li>Publicación de las sanciones firmes (art. 77).[[1]]</li>
</ul>
""" + deep("""
<p><strong>Gradualidad.</strong> Las sanciones se gradúan según el monto de la operación o las ganancias obtenidas, la subsanación por iniciativa propia, las sanciones firmes de los últimos cinco años, el ocultamiento o la dilación de información y el daño al sistema de prevención (art. 79).[[1]] El reglamento añade atenuantes: tener un programa de cumplimiento en ejecución, que el empleado haya actuado violando ese programa y haber fortalecido el programa después de la infracción (Decreto 408-17, art. 37).[[2]]</p>
<p><strong>Prescripción.</strong> Las infracciones muy graves prescriben a los 5 años, las graves a los 3 y las leves al año. En debida diligencia el plazo corre desde el fin de la relación de negocios, y en conservación de documentos, desde que vence el plazo de diez años; si hubo maniobras de ocultamiento, desde que el regulador advierte la falta (art. 80).[[1]]</p>
<p><strong>Concurrencia penal-administrativa.</strong> Si los hechos pueden constituir infracción penal, el supervisor debe denunciarlos al Ministerio Público y abstenerse —o suspender— el procedimiento administrativo hasta que se descarte la infracción penal (art. 81).[[1]]</p>
<p><strong>Responsabilidad que sobrevive.</strong> La responsabilidad administrativa es exigible aunque el sujeto obligado haya cesado su actividad; en sociedades disueltas, los antiguos socios responden solidariamente hasta lo recibido en la liquidación (art. 73).[[1]]</p>
<p><strong>Actualización periódica.</strong> La ley prevé la actualización anual de las multas según el IPC, a cargo de la UAF (art. 79, párrafo II), y encarga al CONCLAFIT actualizarlas cada tres años (art. 89, num. 15).[[1]]</p>
""")},
# 7 ------------------------------------------------------------------------------------------
{"title": "Caso integrador", "html": ess(
"Pongamos todo junto con un caso: un pequeño negocio que se convierte en sujeto obligado y debe decidir qué hacer primero.") + """
<div class="case"><b>Caso · «Inversiones Sol del Este»</b>
<p>Una empresa familiar de bienes raíces comienza a intermediar compraventas de apartamentos para clientes a cambio de una comisión. Tiene seis empleados. Nunca ha hecho nada en materia de prevención.</p>
<ol>
<li><strong>¿Es sujeto obligado?</strong> Sí: los agentes inmobiliarios que intervienen en compraventas para sus clientes están en el art. 33, lit. c.[[1]] Al no tener regulador específico, la supervisa la DGII (art. 2, num. 17).[[1]]</li>
<li><strong>Primeros pasos:</strong> designar un oficial de cumplimiento y registrarlo en la UAF; aprobar un manual basado en riesgo; adoptar un código de ética y un régimen disciplinario; capacitar al personal.[[1,4]]</li>
<li><strong>Con cada cliente:</strong> identificarlo y verificarlo, identificar al beneficiario final cuando el comprador es una sociedad, entender el origen de los fondos y conservar el expediente al menos diez años.[[1]]</li>
<li><strong>Con los pagos:</strong> no aceptar ni facilitar pagos en efectivo por encima del umbral del art. 64; registrar y reportar las transacciones en efectivo que alcancen US$15,000.[[1]]</li>
<li><strong>Con lo raro:</strong> si un comprador paga desde múltiples cuentas de terceros y no explica el origen, analizar y, si persiste la sospecha, remitir un ROS dentro de 5 días hábiles, sin advertirle.[[1]]</li>
</ol>
<p class="verdict yes"><b>Lección:</b> el programa de cumplimiento no es un documento para guardar: es la forma de trabajar desde el primer cliente.</p>
</div>
""" + deep("""
<p><strong>¿Y si no lo hace?</strong> No designar oficial de cumplimiento, no tener manual o no capacitar al personal son infracciones graves para un no financiero (RD$1,392,404 a RD$2,784,805); no reportar una operación sospechosa es muy grave (RD$2,784,806 a RD$5,569,610), según los montos de la Resolución CONCLAFIT-2024-01.[[1,6]]</p>
""")},
],
"glossary": [
("Ley 155-17", "Ley contra el lavado de activos y el financiamiento del terrorismo, del 1 de junio de 2017; sustituyó a la Ley 72-02 [[1]]."),
("Decreto 408-17", "Reglamento de aplicación de la Ley 155-17 [[2]]."),
("Decreto 407-17", "Reglamento sobre congelamiento preventivo de bienes vinculados al terrorismo y la proliferación [[15]]."),
("Norma sectorial", "Regulación del supervisor que adapta la ley a las realidades y riesgos de su sector [[2]]."),
("Programa de cumplimiento", "Conjunto de políticas, procedimientos, controles, capacitación, régimen disciplinario, código de ética y auditoría que exige el art. 34 [[1]]."),
("Oficial de cumplimiento", "Ejecutivo de alto nivel que vigila el programa y es enlace con la UAF y el supervisor (art. 44) [[1]]."),
("CONCLAFIT", "Comité Nacional contra el Lavado de Activos y Financiamiento del Terrorismo, órgano de coordinación del sistema [[1]]."),
("Banco pantalla", "Entidad financiera sin presencia física significativa donde se constituyó, con la que está prohibido operar [[1]]."),
("Prescripción", "Pérdida de la facultad de sancionar por el paso del tiempo: 5, 3 o 1 año según la gravedad (art. 80) [[1]]."),
],
"quiz": [
{"q": "¿Qué norma sustituyó la Ley 155-17?", "options": ["La Ley 183-02", "La Ley 72-02", "La Ley 267-08", "El Decreto 408-17"], "answer": 1, "explain": "La Ley 155-17 derogó y sustituyó la Ley 72-02 sobre lavado de activos [[1]]."},
{"q": "Un abogado que solo litiga en tribunales y nunca realiza para sus clientes las actividades del art. 33, lit. e, es:", "options": ["Sujeto obligado no financiero en todo caso", "No sujeto obligado, según la Norma 01-2018 de la DGII", "Sujeto obligado financiero", "Supervisor"], "answer": 1, "explain": "La DGII precisa que no son sujetos obligados los profesionales que no realicen al menos una de las actividades descritas [[4]]."},
{"q": "Según la Resolución CONCLAFIT-2025-02, una empresa constructora es sujeto obligado no financiero cuando:", "options": ["Tiene más de 50 empleados", "Interviene en compraventas de bienes raíces o promueve y pone en contacto a compradores y vendedores a cambio de comisión", "Su objeto social menciona la construcción", "Siempre, sin excepción"], "answer": 1, "explain": "La resolución aclara que la condición depende de la actividad de riesgo concreta, no del objeto social [[8]]."},
{"q": "¿Cuál de estos NO es un componente mínimo del programa de cumplimiento del art. 34?", "options": ["Código de ética y buena conducta", "Auditoría externa", "Régimen de sanciones disciplinarias", "Un seguro contra multas regulatorias"], "answer": 3, "explain": "El art. 34 exige políticas de riesgo, estándares de contratación y capacitación, régimen disciplinario, código de ética y auditoría externa [[1]]."},
{"q": "¿Durante cuánto tiempo, como mínimo, deben conservarse los registros de debida diligencia y transacciones?", "options": ["5 años", "10 años después de terminada la relación o la transacción", "Mientras dure la relación", "2 años"], "answer": 1, "explain": "El art. 43 exige conservar los registros al menos 10 años después de terminada la relación comercial o la transacción ocasional [[1]]."},
{"q": "¿Cuál es el plazo para remitir un Reporte de Operación Sospechosa a la UAF?", "options": ["24 horas", "5 días hábiles después de realizada o intentada la operación", "Los primeros 10 días del mes siguiente", "30 días calendario"], "answer": 1, "explain": "El art. 55 fija 5 días hábiles contados desde que la operación fue realizada o intentada [[1]]."},
{"q": "La UAF solicita información sobre un cliente. Salvo que disponga un plazo menor, ¿en cuánto tiempo debe responder el sujeto obligado?", "options": ["48 horas", "No más de 10 días laborables", "30 días", "Cuando el cliente lo autorice"], "answer": 1, "explain": "El Decreto 408-17 (art. 25) establece un plazo no mayor de 10 días laborables, o menor si la UAF lo dispone [[2]]."},
{"q": "Según la nota aclaratoria de la Resolución CONCLAFIT-2025-01, ¿cuál es el umbral de efectivo para premios, casinos, acciones y derechos de uso (literales d a g del art. 64)?", "options": ["RD$250,000", "RD$400,000", "RD$450,000", "RD$1,000,000"], "answer": 1, "explain": "La nota aclaratoria del 10 de diciembre de 2025 precisa que el monto correcto es RD$400,000 [[7]]."},
{"q": "Para registrar una compraventa sujeta al art. 64, ¿qué debe exigir el registrador según el reglamento?", "options": ["Una debida diligencia completa del comprador", "Solo la constancia fehaciente del medio de pago", "Prueba del origen de los fondos", "Una carta de la UAF"], "answer": 1, "explain": "El Decreto 408-17 (art. 30) limita la responsabilidad del registrador a exigir la constancia del medio de pago [[2]]."},
{"q": "No designar oficial de cumplimiento se clasifica como infracción:", "options": ["Leve", "Grave", "Muy grave", "No es infracción"], "answer": 1, "explain": "El art. 70 incluye entre las infracciones graves no designar oficial de cumplimiento [[1]]."},
{"q": "¿Qué rango de multa vigente aplica a una infracción muy grave de un sujeto obligado no financiero?", "options": ["RD$300,000 a RD$1,000,000", "RD$2,784,806 a RD$5,569,610", "RD$6,962,014 a RD$13,924,025", "RD$50,000 a RD$100,000"], "answer": 1, "explain": "Son los montos del art. 75, lit. a, actualizados por la Resolución CONCLAFIT-2024-01 [[6]]."},
{"q": "¿En cuánto tiempo prescribe una infracción administrativa muy grave?", "options": ["1 año", "3 años", "5 años", "Nunca prescribe"], "answer": 2, "explain": "El art. 80 fija 5 años para las muy graves, 3 para las graves y 1 para las leves [[1]]."},
],
}
