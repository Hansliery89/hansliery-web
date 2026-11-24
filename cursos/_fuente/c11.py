"""Curso 11 · Fraude digital y delitos financieros tecnológicos."""
from fuentes import *  # noqa: F401,F403
from capas import ess, deep

# 1 GAFI_CEF_M · 2 LEY_5307 · 3 LEY_7425 · 4 ESTAFA_7425 · 5 UAF_ROS · 6 LEY · 7 LEY_4426 · 8 LEY_7425_TXT
# 9 SB_ONBOARD · 10 SB_VERIF
COURSE = {
"num": 11, "slug": "fraude-digital-y-delitos-financieros-tecnologicos", "tag": "Riesgos emergentes", "level": "Básico → Profesional", "minutes": 50,
"title": "Fraude digital y delitos financieros tecnológicos",
"card": "Ciberfraude, mulas de dinero y su vínculo con el lavado.",
"summary": "Conoce las modalidades más comunes de fraude habilitado por la tecnología, el marco penal dominicano aplicable con el Código Penal vigente, el papel de las «mulas» de dinero, los controles antifraude en la vinculación digital y la verificación de documentos, y cómo responder desde cumplimiento.",
"objectives": [
  "Describir las modalidades frecuentes de fraude digital y cómo se lava su producto.",
  "Ubicar el marco penal dominicano aplicable (Ley 53-07 y Código Penal vigente) y su efecto en el deber de reportar.",
  "Reconocer a las «mulas» de dinero y sus señales.",
  "Conocer controles antifraude en la vinculación digital y la verificación de documentos bancarios.",
  "Coordinar la respuesta entre prevención de fraude y cumplimiento.",
],
"sources": [GAFI_CEF_M, LEY_5307, LEY_7425, ESTAFA_7425, UAF_ROS, LEY, LEY_4426, LEY_7425_TXT, SB_ONBOARD, SB_VERIF],
"notice": "Este curso aplica el nuevo Código Penal (Ley 74-25), vigente desde agosto de 2026: la estafa es ahora delito precedente del lavado de activos.",
"modules": [
# 1 ------------------------------------------------------------------------------------------
{"title": "Un delito global y veloz", "html": ess(
"Hoy muchas estafas se hacen por internet o por teléfono: mensajes que imitan al banco, falsas inversiones, ventas que nunca se entregan. El dinero robado se mueve muy rápido entre cuentas y países para que no se pueda recuperar.") + """
<p>El GAFI, INTERPOL y el Grupo Egmont describen el fraude habilitado por la tecnología como una amenaza transnacional en crecimiento: los delincuentes aprovechan la digitalización para operar a mayor escala y velocidad, y mueven los fondos rápidamente entre jurisdicciones.[[1]]</p>
<h3>Modalidades frecuentes</h3>
<ul>
<li><strong>Suplantación (phishing, smishing, vishing):</strong> correos, mensajes o llamadas que imitan a una entidad para obtener claves o datos.</li>
<li><strong>Compromiso de correo empresarial:</strong> se suplanta a un proveedor o ejecutivo para desviar pagos.</li>
<li><strong>Fraudes de inversión:</strong> promesas de rentabilidad alta y segura, a menudo con criptoactivos.</li>
<li><strong>Fraudes románticos o de confianza:</strong> relaciones construidas en línea para pedir dinero.</li>
<li><strong>Ventas falsas en redes sociales:</strong> se cobra por artículos que nunca se entregan.</li>
</ul>
<p class="note-small">Categorías coherentes con las que describe el informe conjunto de 2023.[[1]]</p>
""" + deep("""
<p><strong>Por qué es un problema de lavado.</strong> El informe conjunto destaca que el producto del fraude se canaliza rápidamente a través de redes de cuentas —muchas de mulas—, a menudo con conversión a activos virtuales y salida a otras jurisdicciones, lo que dificulta la recuperación. Recomienda fortalecer la cooperación entre el sector público y el privado y la capacidad de actuar con rapidez para detener los pagos.[[1]]</p>
<p><strong>Ingeniería social.</strong> La mayoría de las modalidades no rompe sistemas: convence a la víctima de que autorice la transferencia o entregue sus claves. Por eso la capacitación de clientes y empleados es tan importante como la tecnología.</p>
""")},
# 2 ------------------------------------------------------------------------------------------
{"title": "Marco penal dominicano", "html": ess(
"En el país hay una ley especial para los delitos de alta tecnología (Ley 53-07) y un nuevo Código Penal vigente desde agosto de 2026. Con este código, toda estafa tiene una pena de al menos tres años, lo que la convierte en delito precedente del lavado.") + """
<ul>
<li><strong>Ley 53-07 sobre Crímenes y Delitos de Alta Tecnología:</strong> tipifica, entre otros, la obtención ilícita de fondos (art. 14), la estafa cometida por medios electrónicos (art. 15) y el robo de identidad (art. 17).[[2]]</li>
<li><strong>Nuevo Código Penal (Ley Orgánica 74-25, con las modificaciones de la Ley 44-26):</strong> vigente desde agosto de 2026. La estafa simple (art. 237) se sanciona con tres a cinco años de prisión; la estafa agravada, la colectiva y la piramidal (arts. 238 a 242), con cinco a diez años.[[3,4,7]]</li>
</ul>
<div class="callout warn" id="nota-codigo-penal"><b>Nota aclaratoria para los participantes · Nuevo Código Penal</b>
<p>La Ley 155-17 considera infracción precedente toda infracción grave con pena no menor de tres años (art. 2, num. 11).[[6]] Con el código vigente, <strong>toda estafa es delito precedente del lavado de activos</strong>.[[3,4,8]] Además, la misma lista del art. 2, num. 11 menciona expresamente los <strong>crímenes y delitos de alta tecnología</strong>, como la estafa por medios electrónicos de la Ley 53-07.[[2,6]]</p>
<p>Distinto es el caso de la falsificación de un documento privado: el art. 348 del código vigente la sanciona con 1 a 2 años, por lo que, aislada, no es delito precedente; sí lo es cuando el documento falso sirve para cometer una estafa.[[8]]</p>
<p>En consecuencia, cuando una operación realizada o intentada genere sospecha de estar vinculada a una estafa, corresponde remitir un <strong>ROS</strong> a la UAF, sin perjuicio de orientar a las víctimas a denunciar. El criterio anterior de la Guía de Calidad de la UAF (2024), según el cual la estafa simple no era precedente, se basaba en el Código Penal de 1884 y ya no aplica.[[5]]</p>
</div>
""" + deep("""
<p><strong>Estafa piramidal y captación.</strong> El código vigente contempla la estafa colectiva y la piramidal entre las modalidades sancionadas con cinco a diez años (arts. 238 a 242).[[4,8]] Los esquemas de «inversión» que pagan rendimientos con el dinero de nuevos participantes, frecuentes en redes sociales y con criptoactivos, encajan con esta descripción y deben analizarse con especial cuidado.</p>
<p><strong>Calificación jurídica.</strong> Al sujeto obligado no le corresponde calificar el delito: basta con que la operación genere sospecha de vinculación con un delito precedente. Indicar el posible delito en el ROS ayuda, pero no es requisito.[[5]]</p>
""")},
# 3 ------------------------------------------------------------------------------------------
{"title": "Las «mulas» de dinero", "html": ess(
"Una «mula» es una persona que presta su cuenta para recibir dinero de un fraude y pasarlo a otros, a veces sin saber que está cometiendo un delito. Se les recluta con falsos trabajos, préstamos fáciles o relaciones por internet.") + """
<p>Una <strong>mula</strong> es una persona que recibe en su cuenta fondos de origen ilícito y los transfiere o retira por cuenta de otros, a veces sin saber que participa en un delito. Son una pieza clave para sacar el dinero del fraude.[[1]]</p>
<p>Se recluta con ofertas de «trabajo desde casa», préstamos fáciles o relaciones en línea. Señales frecuentes:</p>
<ul>
<li>Cuentas nuevas o poco usadas que de pronto reciben muchas transferencias de desconocidos.</li>
<li>Retiro o reenvío casi inmediato de lo recibido.</li>
<li>Titulares jóvenes o sin ingresos que no pueden explicar los movimientos.</li>
<li>Varias cuentas que comparten dispositivo, dirección IP o datos de contacto.</li>
</ul>
""" + deep("""
<p><strong>Mulas conscientes y no conscientes.</strong> Algunas saben lo que hacen y cobran una comisión; otras creen que tienen un empleo legítimo. Para el sujeto obligado la respuesta operativa es similar —analizar, escalar, reportar—, pero la comunicación con el cliente debe cuidar la reserva del art. 63.[[6]]</p>
<p><strong>Responsabilidad.</strong> La ley considera lavado convertir o transferir bienes a sabiendas de su origen ilícito, y el art. 2 define las «circunstancias objetivas» que permiten inferir ese conocimiento.[[6]] Prestar la cuenta «sin preguntar» no es una defensa segura.</p>
""")},
# 4 ------------------------------------------------------------------------------------------
{"title": "Controles en la vinculación digital", "html": ess(
"Muchas cuentas de mulas se abren por internet con identidades robadas. Por eso la banca debe hacer chequeos antifraude al vincular clientes: ubicación, correo, teléfono y detección de identidades falsas.") + """
<p>La circular de la Superintendencia de Bancos sobre onboarding digital exige a las entidades de intermediación financiera ejecutar <strong>chequeos antifraude</strong> al vincular clientes no presenciales, con autorización previa del usuario. Entre los mecanismos que menciona:[[9]]</p>
<ul>
<li><strong>Geolocalización:</strong> validar las coordenadas del potencial cliente mediante la reputación de su dirección IP o de su proveedor de telecomunicaciones.</li>
<li><strong>Verificación del correo electrónico:</strong> que no sea de alto riesgo y que su servidor no haya sufrido una brecha reciente.</li>
<li><strong>Verificación del teléfono móvil:</strong> tipo de número, de teléfono y operador, y coherencia de su geolocalización con la del cliente.</li>
<li><strong>Detección de identidades suplantadas, manipuladas o robadas.</strong></li>
</ul>
<p>La verificación debe incluir, además, la autenticidad del documento de identidad y una <strong>prueba de vida</strong>.[[9]]</p>
""" + deep("""
<p><strong>De la vinculación al monitoreo.</strong> La misma circular pide mecanismos continuos de actualización y monitoreo de la debida diligencia.[[9]] Los datos del onboarding (dispositivo, IP, teléfono) son valiosos para detectar después redes de cuentas relacionadas, siempre con base legal y con el consentimiento que exige la circular.</p>
""")},
# 5 ------------------------------------------------------------------------------------------
{"title": "Documentos falsos y verificación digital", "html": ess(
"Un recurso común del fraude es presentar estados de cuenta o cartas bancarias falsas. Los bancos deben ofrecer una forma de verificar en línea que sus documentos son auténticos, y quien los recibe puede comprobarlo por sí mismo.") + """
<p>La Superintendencia de Bancos requiere a las entidades de intermediación financiera establecer <strong>mecanismos de verificación digital</strong> que aseguren la autenticidad, integridad y validez de los documentos que emiten a solicitud de sus clientes, como cartas de referencia bancaria y estados de cuenta (Circular CSB-REG-202400010, del 9 de julio de 2024).[[10]]</p>
<ul>
<li>Cada entidad elige el mecanismo según su tamaño, complejidad y capacidad, garantizando que el documento no ha sido alterado, manipulado o falsificado.</li>
<li>Debe informar a usuarios y receptores cómo verificar el documento, de modo que puedan hacerlo <strong>por sí mismos</strong>.</li>
</ul>
<p class="note-small">Síntesis de la circular.[[10]]</p>
<div class="callout tip"><b>Para cualquier sujeto obligado</b>Si un cliente entrega un estado de cuenta o una referencia bancaria como soporte del origen de fondos, verifica su autenticidad con el mecanismo de la entidad emisora. Un documento falso usado para justificar fondos u obtener un crédito puede indicar una estafa, que es delito precedente.[[8]]</div>
""" + deep("""
<p><strong>Falsedad aislada vs. falsedad instrumental.</strong> Recuerda la regla del curso 8: la falsificación de un documento privado, aislada, se sanciona con 1 a 2 años y no es delito precedente; cuando sirve para cometer una estafa, la conducta relevante es la estafa.[[8]]</p>
""")},
# 6 ------------------------------------------------------------------------------------------
{"title": "Respuesta desde cumplimiento", "html": ess(
"Ante un fraude hay que actuar rápido: el equipo de fraude bloquea o escala, cumplimiento analiza y reporta a la UAF, y a la víctima se le orienta a denunciar a la Policía o a la Procuraduría.") + """
<ol class="steps">
<li><strong>Coordinar fraude y cumplimiento:</strong> los indicadores de fraude alimentan el monitoreo antilavado y viceversa.[[1]]</li>
<li><strong>Actuar rápido:</strong> la velocidad del fraude exige procesos ágiles de bloqueo y escalamiento, según las políticas de la entidad.</li>
<li><strong>Orientar a las víctimas:</strong> la UAF recuerda los canales de denuncia de la Policía Nacional (incluida su plataforma en línea), la Procuraduría General de la República y la línea 311.[[5]]</li>
<li><strong>Reportar:</strong> como la estafa es delito precedente con el código vigente, la operación sospechosa vinculada a un fraude se reporta mediante ROS dentro de los 5 días hábiles.[[3,6]]</li>
</ol>
<div class="callout warn"><b>Reserva</b>Orientar a la víctima a denunciar no significa contarle que se envió un ROS. La prohibición del art. 63 se mantiene frente a clientes y terceros.[[6]]</div>
""" + deep("""
<p><strong>Lecciones del informe conjunto.</strong> El GAFI, INTERPOL y Egmont recomiendan mecanismos que permitan detener pagos con rapidez, compartir información entre entidades dentro del marco legal y coordinar a las unidades de inteligencia financiera con la policía y el sector privado.[[1]]</p>
""")},
# 7 ------------------------------------------------------------------------------------------
{"title": "Casos integradores", "html": ess(
"Dos casos: uno de ventas falsas en redes sociales y otro de correo empresarial suplantado.") + """
<div class="case"><b>Caso 1 · Ventas que nunca llegan</b><p>Varios clientes denuncian que pagaron artículos anunciados en redes sociales a la cuenta de la Sra. T. y nunca los recibieron. La cuenta recibió en un mes decenas de transferencias similares, retiradas en cajeros el mismo día.</p>
<p class="verdict yes"><b>Decisión:</b> escalar a fraude para las medidas inmediatas, orientar a los afectados a denunciar y remitir el ROS: el patrón apunta a una estafa, que es delito precedente con el código vigente.[[3,6]]</p></div>
<div class="case"><b>Caso 2 · El proveedor que cambió de cuenta</b><p>Una empresa cliente recibe un correo, aparentemente de su proveedor habitual, que informa un «cambio de cuenta bancaria» en el extranjero. Transfiere el pago mensual. Días después, el proveedor real reclama que no ha cobrado.</p>
<p class="verdict yes"><b>Decisión:</b> es un compromiso de correo empresarial. La entidad del cliente debe intentar detener o recuperar la transferencia con la entidad receptora; la entidad que recibió los fondos debe analizar la cuenta beneficiaria —que puede ser de una mula— y, si confirma la sospecha, remitir el ROS.[[1,6]]</p></div>
""" + deep("""
<p><strong>Prevención con el cliente empresarial.</strong> Recomienda confirmar por un canal distinto (por ejemplo, una llamada a un número ya conocido) cualquier cambio de datos bancarios de un proveedor. Es un control sencillo que evita la mayoría de estos fraudes.</p>
""")},
],
"glossary": [
("Fraude habilitado por la tecnología", "Fraude cometido a gran escala y velocidad mediante medios digitales [[1]]."),
("Phishing, smishing, vishing", "Suplantación por correo, mensaje de texto o llamada para obtener datos o claves."),
("Compromiso de correo empresarial", "Suplantación de un proveedor o ejecutivo para desviar pagos."),
("Mula de dinero", "Persona que recibe y mueve fondos ilícitos por cuenta de otros [[1]]."),
("Estafa", "Delito sancionado con 3 a 5 años (simple) y 5 a 10 años (agravada, colectiva o piramidal) en el Código Penal vigente [[4,8]]."),
("Ley 53-07", "Ley sobre Crímenes y Delitos de Alta Tecnología [[2]]."),
("Prueba de vida", "Verificación de que la persona está presente en un proceso no presencial [[9]]."),
("Verificación digital de documentos", "Mecanismo para comprobar la autenticidad de documentos bancarios [[10]]."),
],
"quiz": [
{"q": "¿Qué caracteriza al fraude habilitado por la tecnología según el GAFI, INTERPOL y Egmont?", "options": ["Es local y lento", "Es transnacional, crece rápido y mueve los fondos con velocidad entre jurisdicciones", "Solo afecta a bancos grandes", "No tiene relación con el lavado"], "answer": 1, "explain": "El informe de 2023 lo describe como una amenaza transnacional en crecimiento ligada al lavado [[1]]."},
{"q": "¿Qué ley dominicana tipifica la estafa cometida por medios electrónicos?", "options": ["Ley 172-13", "Ley 53-07 sobre Crímenes y Delitos de Alta Tecnología", "Ley 183-02", "Ley 311-14"], "answer": 1, "explain": "El art. 15 de la Ley 53-07 sanciona la estafa realizada por medios electrónicos [[2]]."},
{"q": "Con el Código Penal vigente (Ley 74-25), ¿cómo se trata la estafa en materia de lavado de activos?", "options": ["Sigue sin ser delito precedente", "Es delito precedente, porque su pena (3 a 5 años) alcanza el umbral de la Ley 155-17", "Solo es precedente si la comete un funcionario", "Solo la investiga la UAF"], "answer": 1, "explain": "La estafa simple (art. 237) se castiga con 3 a 5 años; la Ley 155-17 considera precedente toda infracción grave con pena no menor de tres años [[3,4,6]]."},
{"q": "¿Qué es una «mula» de dinero?", "options": ["Un sistema de pago", "Una persona que recibe y mueve fondos ilícitos por cuenta de otros", "Una billetera digital", "Un tipo de reporte"], "answer": 1, "explain": "Las mulas permiten sacar y dispersar el dinero del fraude [[1]]."},
{"q": "¿Cuál es una señal típica de una cuenta usada como mula?", "options": ["Pago puntual de la nómina", "Muchas transferencias de desconocidos retiradas o reenviadas casi de inmediato", "Ahorro mensual constante", "Uso de tarjeta en supermercados"], "answer": 1, "explain": "La recepción masiva y el retiro inmediato son indicadores frecuentes."},
{"q": "¿Cuál de estos es un chequeo antifraude previsto en la circular de onboarding digital de la SB?", "options": ["Preguntar el color favorito", "Verificar la geolocalización mediante la reputación de la dirección IP", "Pedir una foto de la mascota", "No hacer ninguno"], "answer": 1, "explain": "La circular menciona geolocalización, verificación de correo y teléfono y detección de identidades suplantadas [[9]]."},
{"q": "Según la Circular CSB-REG-202400010, las entidades de intermediación financiera deben:", "options": ["Dejar de emitir estados de cuenta", "Establecer mecanismos de verificación digital de los documentos que emiten", "Enviar los documentos solo por fax", "Cobrar por cada verificación"], "answer": 1, "explain": "La circular exige mecanismos que aseguren la autenticidad, integridad y validez de esos documentos [[10]]."},
{"q": "Un cliente presenta un estado de cuenta falso para obtener un préstamo. ¿Cómo se analiza?", "options": ["Es solo una falsedad privada sin relevancia", "Puede constituir una estafa, que es delito precedente; se analiza y, si hay sospecha, se reporta", "Se ignora", "Se le devuelve el documento"], "answer": 1, "explain": "Aislada, la falsedad privada no es precedente; usada para obtener un crédito, puede ser una estafa [[8]]."},
{"q": "Una víctima de fraude acude a la entidad. ¿Qué orientación es correcta?", "options": ["Decirle que no hay nada que hacer", "Orientarla a denunciar ante la Policía Nacional, la Procuraduría o la línea 311, sin revelar análisis internos", "Mostrarle los ROS enviados", "Contactar al presunto estafador"], "answer": 1, "explain": "La UAF recuerda esos canales de denuncia; la reserva sobre los reportes se mantiene [[5,6]]."},
{"q": "En un compromiso de correo empresarial, ¿qué control sencillo previene el fraude?", "options": ["Responder rápido al correo", "Confirmar por un canal distinto y conocido cualquier cambio de cuenta del proveedor", "Pagar siempre en efectivo", "Desactivar el correo"], "answer": 1, "explain": "La confirmación por un canal independiente evita la mayoría de estos fraudes."},
],
}
