"""Curso 05 · Debida diligencia y conocimiento del cliente."""
from fuentes import *  # noqa: F401,F403
from capas import ess, deep

# 1 LEY · 2 REG · 3 GAFI40 · 4 SIS_NORMA · 5 DGII_N01 · 6 SB_ONBOARD · 7 SIB_DD · 8 UAF_ROS
COURSE = {
"num": 5, "slug": "debida-diligencia-y-conocimiento-del-cliente", "tag": "Debida diligencia", "level": "Básico → Profesional", "minutes": 55,
"title": "Debida diligencia y conocimiento del cliente",
"card": "Identificar, verificar y conocer al cliente según su nivel de riesgo.",
"summary": "Domina el proceso de debida diligencia: cuándo es obligatoria, qué información obtener de personas físicas y jurídicas, cómo verificarla también en canales digitales, cuándo aplicar medidas simplificadas o ampliadas, qué hacer cuando el cliente no colabora y cómo mantener, conservar y delegar la información.",
"objectives": [
  "Identificar cuándo es obligatorio aplicar debida diligencia, incluidos los umbrales para clientes ocasionales.",
  "Describir los componentes de la debida diligencia de personas físicas, jurídicas y fideicomisos.",
  "Elegir entre debida diligencia simplificada, normal y ampliada según el riesgo.",
  "Conocer los lineamientos de verificación no presencial (onboarding digital).",
  "Actuar correctamente cuando el cliente no entrega la información o cuando la diligencia lo alertaría.",
  "Mantener la información actualizada, los registros conservados y la delegación bajo control.",
],
"sources": [LEY, REG, GAFI40, SIS_NORMA, DGII_N01, SB_ONBOARD, SIB_DD, UAF_ROS],
"modules": [
# 1 ------------------------------------------------------------------------------------------
{"title": "Conocer al cliente no es un formulario", "html": ess(
"Hacer debida diligencia es saber con quién se hace negocio: quién es de verdad, quién está detrás, para qué quiere el producto y de dónde sale su dinero. Con eso se arma un «perfil» que luego sirve para notar si algo no cuadra.") + """
<p>La <strong>debida diligencia</strong> es el conjunto de medidas para saber con quién se hace negocio, de dónde vienen sus recursos y si su comportamiento es coherente con lo declarado. La ley la exige para clientes <strong>actuales y potenciales</strong>, con el fin de (art. 38):[[1]]</p>
<ol class="steps">
<li>Identificar al cliente, persona física o jurídica, y verificar su identidad con documentos, datos o información de fuentes fiables e independientes.</li>
<li>Identificar y verificar a quien dice actuar en nombre del cliente y que esté autorizado.</li>
<li>Identificar al <strong>beneficiario final</strong> y tomar medidas razonables para verificarlo.</li>
<li>Entender y, cuando corresponda, obtener información sobre el propósito y el carácter de la relación.</li>
<li>Completar la verificación de acuerdo con el nivel de riesgo definido por el sujeto obligado.</li>
</ol>
<p>A eso se suma el <strong>monitoreo continuo</strong>: examinar las transacciones a lo largo de la relación para asegurar que sean consistentes con el conocimiento del cliente, su actividad y su perfil de riesgo, incluyendo, cuando sea necesario, la documentación del origen y el destino de los fondos (art. 39).[[1]]</p>
<div class="callout key"><b>Idea clave</b>El objetivo es construir un <strong>perfil</strong> del cliente —quién es, qué hace, cuánto y cómo opera— contra el cual comparar su actividad futura.</div>
""" + deep("""
<p><strong>Listas.</strong> Varias normas sectoriales añaden al art. 38 la verificación en listas. La Norma 01-2018 de la DGII incluye verificar que el cliente no figure en las listas del Consejo de Seguridad de la ONU.[[5]] La norma de seguros pide verificar las listas de la ONU, la de la OFAC y otras listas criminales oficiales nacionales e internacionales públicas (por ejemplo, Policía Nacional, Interpol y DNCD).[[4]] La verificación en las listas de la ONU es, además, una obligación expresa de la ley (art. 82).[[1]]</p>
<p><strong>Estándar internacional.</strong> Estas medidas reproducen las de la Recomendación 10 del GAFI sobre debida diligencia del cliente.[[3]]</p>
""")},
# 2 ------------------------------------------------------------------------------------------
{"title": "¿Cuándo es obligatoria?", "html": ess(
"La debida diligencia se hace siempre al empezar una relación, cuando hay sospecha, cuando se duda de los datos del cliente y cuando alguien que no es cliente fijo hace operaciones grandes. En casinos y joyerías hay reglas propias.") + """
<p>El reglamento fija los momentos en que es obligatoria (Decreto 408-17, arts. 15 y 16):[[2]]</p>
<ul>
<li>Cuando se pretende establecer o se establece una relación comercial o profesional.</li>
<li>Cuando hay <strong>sospecha</strong> de lavado o financiamiento del terrorismo, con independencia de exenciones o umbrales.</li>
<li>Cuando hay <strong>dudas</strong> sobre la veracidad de los datos de identificación.</li>
<li>Cuando un cliente realiza <strong>transacciones ocasionales</strong> por encima de US$15,000 en una sola operación o en varias durante 24 horas.</li>
</ul>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Sector</th><th>Regla particular (Decreto 408-17)</th></tr></thead>
<tbody>
<tr><td>Seguros, reaseguros y corredores</td><td>La debida diligencia se aplica solo a los seguros de vida y a los que contemplen una inversión (art. 15, lit. e).</td></tr>
<tr><td>Casinos y juegos de azar</td><td>Operaciones iguales o superiores a US$3,000, en varias operaciones en 24 horas (art. 16, párrafo I).</td></tr>
<tr><td>Agentes inmobiliarios y constructoras</td><td>Cuando intervienen en compraventas de bienes raíces para sus clientes, compradores o vendedores (art. 16, párrafo II).</td></tr>
<tr><td>Joyas, metales y piedras preciosas</td><td>Transacciones iguales o superiores a US$15,000, en una o varias operaciones en 24 horas o que parezcan relacionadas (art. 16, párrafo III).</td></tr>
</tbody></table></div>
<p class="note-small">Elaborado a partir del Decreto 408-17.[[2]]</p>
""" + deep("""
<p><strong>Clientes existentes.</strong> El reglamento ordena actualizar la debida diligencia de los clientes actuales conforme a su nivel de riesgo (art. 17).[[2]] La ley exige que los datos se mantengan actualizados y relevantes según el riesgo, con revisiones que incluyan a las categorías de mayor riesgo (art. 36, párrafo).[[1]]</p>
<p><strong>Seguros: momentos adicionales.</strong> La norma de seguros pide actualizar los datos cuando se detecten operaciones inusuales, cuando cambie de forma relevante la manera de operar del cliente o cuando haya sospechas; y, para clientes ocasionales, si reinciden después de más de 12 meses de la última transacción.[[4]]</p>
""")},
# 3 ------------------------------------------------------------------------------------------
{"title": "Qué información pedir", "html": ess(
"De una persona se piden sus datos básicos, su documento, a qué se dedica y dónde vive. De una empresa, además de sus datos legales, hay que entender quién es su dueño real y quién la controla. En los fideicomisos hay que identificar a todas las partes.") + """
<div class="grid-2">
<div class="mini"><h4>Personas físicas (ejemplo DGII)</h4><p>Nombre completo; cédula o pasaporte; nacionalidad; país de residencia; dirección; teléfonos; profesión u ocupación; documentación que sustente lo declarado (por ejemplo, recibos de servicios).[[5]]</p></div>
<div class="mini"><h4>Personas jurídicas (art. 40 de la ley)</h4><p>Razón social, número de identificación tributaria, forma jurídica y prueba de existencia; estructura de titularidad, propiedad y control; nombres de la alta gerencia; dirección principal; beneficiario final.[[1]]</p></div>
</div>
<p>La norma de seguros pide además a las personas físicas, entre otros datos, fecha y lugar de nacimiento, correo electrónico, lugar de trabajo, la <strong>declaración expresa de si es PEP</strong> y la forma de pago.[[4]]</p>
<h3>Fideicomisos</h3>
<p>Las fiduciarias deben identificar y verificar a todas las partes del fideicomiso, incluidos el fideicomitente y el beneficiario final, y mantener esa información actualizada (art. 41).[[1]] La norma de seguros añade determinar el origen de los bienes fideicomitidos y de los fondos de los beneficiarios.[[4]]</p>
<div class="callout tip"><b>En la práctica</b>Pide el organigrama de propiedad hasta llegar a personas físicas. Si aparece una sociedad extranjera en la cadena, solicita sus documentos societarios y la identificación de sus propietarios. El curso 6 desarrolla el beneficiario final.</div>
""" + deep("""
<p><strong>Expediente.</strong> En seguros, el expediente debe contener las constancias del cumplimiento de los requisitos de debida diligencia y todos los datos intercambiados con el cliente, por medios físicos o electrónicos, que contribuyan a reflejar su perfil.[[4]]</p>
<p><strong>Banca.</strong> Las entidades de intermediación financiera siguen además el Instructivo sobre Debida Diligencia de la Superintendencia de Bancos, cuya versión vigente es la tercera, puesta en vigencia con la Circular SB 005/22. La versión incluida en la bibliografía de este curso es la segunda (Circular SIB 012/17), por lo que sus detalles deben contrastarse con la vigente.[[7]]</p>
""")},
# 4 ------------------------------------------------------------------------------------------
{"title": "Tres intensidades de diligencia", "html": ess(
"Según el riesgo, la debida diligencia puede ser más ligera (simplificada), la habitual (normal) o más profunda (ampliada). La ampliada pide, entre otras cosas, saber de dónde vienen los fondos y que un jefe apruebe la relación.") + """
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Nivel</th><th>Cuándo</th><th>Qué implica</th></tr></thead>
<tbody>
<tr><td>Simplificada</td><td>Riesgo bajo identificado</td><td>Medidas reducidas y proporcionales. <strong>No es aceptable si hay sospecha</strong> o escenarios de riesgo mayor (art. 42).[[1]]</td></tr>
<tr><td>Normal</td><td>Riesgo medio o habitual</td><td>Identificación y verificación completas, perfil y monitoreo periódico.[[5]]</td></tr>
<tr><td>Ampliada</td><td>Riesgo alto: PEP, jurisdicciones señaladas por el GAFI, estructuras complejas, productos de alto riesgo</td><td>Niveles de aprobación para iniciar o continuar la relación, medidas para determinar el origen del patrimonio o de los fondos y monitoreo permanente y más exhaustivo.[[4]]</td></tr>
</tbody></table></div>
<p>La Norma 01-2018 de la DGII añade a la ampliada información bancaria, evidencia de verificación de lo declarado y referencias comerciales.[[5]]</p>
<div class="callout warn"><b>Supuestos fijos de diligencia ampliada (DGII)</b>Entre otros: clientes de alto riesgo según la matriz; relaciones con jurisdicciones de alto riesgo; entidades con participaciones en sociedades «de carpeta» sin actividad económica real; PEP; no residentes con operaciones en efectivo mayores de US$15,000 diarios; estructuras accionarias inusuales o excesivamente complejas; y clientes que fueron objeto de un ROS cuando se decidió continuar la relación.[[5]]</div>
""" + deep("""
<p><strong>Seguros: beneficiarios de pólizas.</strong> Las aseguradoras deben aplicar debida diligencia ampliada respecto del beneficiario de las pólizas y fianzas calificadas de alto riesgo.[[4]] En seguros de vida, deben adoptar medidas razonables para determinar si los beneficiarios, o el beneficiario final del beneficiario, son PEP, a más tardar en el momento del pago.[[4]]</p>
<p><strong>Simplificada en seguros.</strong> La norma de seguros considera factores de bajo riesgo, entre otros, las pólizas con prima anual menor a 4 salarios mínimos (o primas que en conjunto no superen 10), los organismos estatales y las operaciones con organismos internacionales, y en esos casos prevé debida diligencia simplificada.[[4]]</p>
""")},
# 5 ------------------------------------------------------------------------------------------
{"title": "Verificar a distancia: onboarding digital", "html": ess(
"Hoy muchos clientes se vinculan por una app, sin ir a una oficina. Eso está permitido en la banca, pero la verificación debe dar la misma confianza que en persona: comprobar el documento, hacer una prueba de vida y guardar la evidencia diez años.") + """
<p>La Superintendencia de Bancos permite a las entidades de intermediación financiera vincular personas físicas y jurídicas por mecanismos automatizados o semiautomatizados, sin interacción presencial, siempre que la identificación, verificación y autenticación generen una <strong>confianza equivalente a un proceso presencial</strong> (Circular CSB-REG-2026000013).[[6]]</p>
<p>Entre los objetivos mínimos de la verificación no presencial figuran:[[6]]</p>
<ul>
<li>Un proceso técnicamente seguro que asegure con alta fiabilidad la autenticidad del documento de identidad (cédula o pasaporte).</li>
<li>Garantizar que la persona es quien dice ser, verificando su fecha de nacimiento y con una <strong>prueba de vida</strong>.</li>
<li>Capacitación y revisiones de calidad del personal que verifica, y asignación impredecible de ese personal.</li>
<li>Resguardar la evidencia del proceso de verificación por un mínimo de <strong>10 años</strong> desde la vinculación.</li>
<li>Mecanismos continuos de actualización y monitoreo de la debida diligencia.</li>
</ul>
<p>El proceso debe permitir conocer el <strong>origen de los fondos</strong> (la actividad, negocio, ocupación o empleo que los genera) y ejecutar chequeos antifraude como geolocalización, verificación de correo y teléfono y detección de identidades suplantadas o manipuladas, con autorización previa del usuario.[[6]]</p>
""" + deep("""
<p><strong>Riesgo del canal.</strong> El canal no presencial es uno de los factores de riesgo que la ley obliga a evaluar (art. 37) y, si es nuevo, debe evaluarse antes de ofrecerse (art. 45).[[1]] La circular no elimina esas obligaciones: las entidades deben contar con políticas y procedimientos que incluyan controles de validación de identidad y conocimiento del cliente.[[6]]</p>
<p><strong>Otros sectores.</strong> La circular está dirigida a las entidades de intermediación financiera. Otros sujetos obligados que vinculen clientes a distancia deben aplicar los principios de su propia norma sectorial y del art. 38 de la ley.</p>
""")},
# 6 ------------------------------------------------------------------------------------------
{"title": "Cuando el cliente no colabora", "html": ess(
"Si no se puede saber quién es el cliente, no se hace el negocio. Si el cliente se niega a dar la información que exige la ley, además se reporta a la UAF. Y si hacer preguntas lo pondría en alerta, se reporta sin seguir preguntando.") + """
<p>Si no es posible identificar y verificar al cliente, la entidad <strong>no debe iniciar ni mantener</strong> la relación ni realizar la transacción, y cuando el potencial cliente <strong>se niega</strong> a aportar la información, debe remitirse un Reporte de Operación Sospechosa (art. 62).[[1]]</p>
<div class="callout warn"><b>No confundir</b>Un cliente simplemente ilocalizable o que no completó documentos internos no exigidos por la normativa antilavado no justifica, por sí solo, un reporte. La negativa a entregar información exigida por la ley sí activa el deber de reportar.[[1,8]]</div>
<div class="callout key"><b>Diligencia que alertaría al cliente</b>La norma de seguros prevé que, si la entidad tiene sospechas y considera que efectuar la debida diligencia alertaría al cliente, debe reportar la operación como sospechosa sin realizarla.[[4]] Es coherente con la prohibición de revelar que se reporta o se examina una operación (art. 63 de la ley).[[1]]</div>
<div class="case"><b>Caso</b><p>Un potencial cliente desea contratar un seguro de vida con inversión por un monto alto. Al pedirle la documentación del origen de los fondos responde que «no tiene por qué explicarlo» y se retira.</p>
<p class="verdict yes"><b>Decisión:</b> no se inicia la relación y, al tratarse de una negativa a brindar información de debida diligencia, se analiza y remite el ROS dentro del plazo legal de 5 días hábiles.[[1]]</p></div>
""" + deep("""
<p><strong>Calidad del reporte.</strong> La guía de calidad de la UAF insiste en que el ROS explique con claridad los hechos y el análisis que llevaron a la sospecha; en estos casos, conviene documentar qué información se pidió, por qué era exigible y cómo respondió el cliente.[[8]] El curso 8 desarrolla la redacción del reporte.</p>
""")},
# 7 ------------------------------------------------------------------------------------------
{"title": "Actualizar, conservar y delegar", "html": ess(
"La información del cliente envejece: hay que actualizarla según su riesgo. Los documentos se guardan diez años. Y se puede pedir a otra entidad que identifique al cliente, pero la responsabilidad sigue siendo propia.") + """
<ul>
<li><strong>Actualización</strong>: los datos deben mantenerse vigentes según el riesgo (art. 36, párrafo). La DGII fija una actualización anual para clientes habituales y cada dos años para ocasionales.[[1,5]]</li>
<li><strong>Conservación</strong>: los registros de transacciones, debida diligencia, archivos, correspondencia y resultados de análisis se guardan al menos 10 años después de terminada la relación o la transacción ocasional, en cualquier medio de reproducción (art. 43).[[1]]</li>
<li><strong>Delegación</strong>: se puede delegar en otro sujeto obligado la identificación del cliente y del beneficiario final y la comprensión de la actividad, pero la responsabilidad final sigue siendo de quien delega, que debe obtener inmediatamente la información y las copias (art. 47).[[1]]</li>
</ul>
<p>El reglamento limita lo que puede delegarse a la identificación y verificación del cliente y del beneficiario final y al entendimiento del propósito de la relación; si el tercero reside en otro país, debe considerarse el riesgo de ese país (Decreto 408-17, art. 22).[[2]]</p>
""" + deep("""
<p><strong>Condiciones para tercerizar (seguros).</strong> La norma de seguros solo permite tercerizar esos mismos elementos si la entidad tiene acceso inmediato a la información del tercero, se asegura de que el tercero entregará copias sin demora, verifica que el tercero cuenta con controles adecuados y la UAF puede acceder a la información en su poder.[[4]]</p>
<p><strong>Delegación dentro del grupo (DGII).</strong> La Norma 01-2018 permite delegar solo en otro sujeto obligado del mismo grupo financiero o económico y recuerda que la delegación no exime de responsabilidad.[[5]]</p>
<div class="callout key"><b>Recuerda</b>La debida diligencia bien hecha es también la mejor defensa ante un falso positivo: permite explicar rápidamente por qué una operación inusual es legítima.</div>
""")},
],
"glossary": [
("Debida diligencia del cliente", "Medidas para identificar, verificar y conocer al cliente y monitorear la relación (arts. 38 y 39) [[1]]."),
("Cliente ocasional", "Quien realiza transacciones sin relación permanente; requiere debida diligencia por encima de US$15,000 [[2]]."),
("Perfil del cliente", "Conocimiento de quién es el cliente, su actividad y su comportamiento esperado, contra el cual se compara su actividad [[1]]."),
("Debida diligencia ampliada", "Medidas adicionales para riesgos mayores: aprobaciones, origen de fondos y monitoreo más exhaustivo [[4]]."),
("Prueba de vida", "Verificación de que la persona está presente y es quien dice ser en un proceso no presencial [[6]]."),
("Onboarding digital", "Vinculación de clientes por canales automatizados o semiautomatizados, sin interacción presencial [[6]]."),
("Delegación", "Encargar a otro sujeto obligado ciertos elementos de la debida diligencia, manteniendo la responsabilidad (art. 47) [[1]]."),
("Revelación (tipping-off)", "Advertir al cliente de que se reporta o examina una operación; está prohibido (art. 63) [[1]]."),
],
"quiz": [
{"q": "¿A quiénes aplica la debida diligencia según la Ley 155-17?", "options": ["Solo a clientes nuevos", "A clientes actuales y potenciales", "Solo a personas jurídicas", "Solo a clientes de alto riesgo"], "answer": 1, "explain": "El art. 38 extiende la debida diligencia a clientes actuales y potenciales [[1]]."},
{"q": "Un cliente ocasional realiza tres operaciones en 24 horas que suman US$16,000. Según el Decreto 408-17:", "options": ["No se requiere debida diligencia", "Debe aplicarse debida diligencia", "Solo se registra el nombre", "Se rechaza la operación"], "answer": 1, "explain": "Los arts. 15 y 16 exigen debida diligencia en transacciones ocasionales por encima de US$15,000 en una o varias operaciones en 24 horas [[2]]."},
{"q": "En el sector seguros, el reglamento limita la debida diligencia del cliente a:", "options": ["Todos los seguros sin excepción", "Los seguros de vida y los que contemplen una inversión", "Solo los seguros de autos", "Ningún seguro"], "answer": 1, "explain": "El art. 15, lit. e, del Decreto 408-17 la limita a seguros de vida y a los que contemplen inversión [[2]]."},
{"q": "¿Cuándo NO es aceptable aplicar debida diligencia simplificada?", "options": ["Cuando el cliente es asalariado", "Cuando existe sospecha de lavado o financiamiento del terrorismo", "Cuando el producto es de bajo monto", "Nunca es aceptable"], "answer": 1, "explain": "El art. 42 excluye la simplificada si hay sospecha o escenarios de riesgo mayor [[1]]."},
{"q": "Para una persona jurídica, ¿qué exige entender el art. 40 de la ley?", "options": ["Su color corporativo", "Su estructura de titularidad, propiedad y control", "Su número de empleados", "Sus redes sociales"], "answer": 1, "explain": "El art. 40 incluye razón social, identificación tributaria, forma jurídica, estructura de propiedad y control, dirección y beneficiario final [[1]]."},
{"q": "Según la circular de onboarding digital de la SB, la verificación no presencial debe:", "options": ["Ser más laxa que la presencial", "Generar una confianza equivalente a un proceso presencial", "Evitar pedir documentos", "Hacerse solo por correo"], "answer": 1, "explain": "La circular exige mecanismos cuyos resultados generen una confianza equivalente a la vinculación presencial [[6]]."},
{"q": "¿Por cuánto tiempo debe resguardarse la evidencia de la verificación de identidad en el onboarding digital bancario?", "options": ["1 año", "5 años", "Mínimo 10 años desde la vinculación", "No se guarda"], "answer": 2, "explain": "La circular exige resguardarla por un mínimo de 10 años a partir de la vinculación [[6]]."},
{"q": "Un cliente se niega a entregar información exigida para su debida diligencia. ¿Qué corresponde?", "options": ["Abrir la cuenta igual", "No iniciar la relación y remitir un ROS", "Esperar a que cambie de opinión", "Pedirle una carta de disculpa"], "answer": 1, "explain": "El art. 62 impide iniciar la relación y ordena remitir un ROS ante la negativa [[1]]."},
{"q": "Según la norma de seguros, si hacer la debida diligencia alertaría a un cliente sospechoso, la entidad debe:", "options": ["Hacerla de todos modos y contarle al cliente", "Reportar la operación como sospechosa sin realizar la debida diligencia", "Cerrar el caso", "Esperar un año"], "answer": 1, "explain": "La norma de seguros lo prevé expresamente para no alertar al cliente [[4]]."},
{"q": "En seguros de vida, ¿hasta cuándo debe determinarse si el beneficiario es PEP?", "options": ["Al emitir la póliza, sin excepción", "A más tardar en el momento del pago", "Nunca", "Solo si lo pide la UAF"], "answer": 1, "explain": "La norma de seguros pide medidas razonables a más tardar en el momento del pago [[4]]."},
{"q": "Si una entidad delega la identificación de un cliente en otro sujeto obligado:", "options": ["La responsabilidad pasa al tercero", "La responsabilidad final sigue siendo de quien delega", "No se requiere conservar copias", "Queda exenta de monitorear"], "answer": 1, "explain": "El art. 47 permite delegar, pero mantiene la responsabilidad en quien delega [[1]]."},
{"q": "¿Durante cuánto tiempo deben conservarse los registros de debida diligencia?", "options": ["5 años", "Al menos 10 años después de terminada la relación o la transacción ocasional", "Mientras el cliente lo autorice", "2 años"], "answer": 1, "explain": "Lo fija el art. 43 de la ley [[1]]."},
],
}
