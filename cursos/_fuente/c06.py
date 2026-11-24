"""Curso 06 · Beneficiario final."""
from fuentes import *  # noqa: F401,F403
from capas import ess, deep

# 1 LEY · 2 REG · 3 GAFI40 · 4 GAFI_BF_M · 5 DGII_BF · 6 DGII_N01 · 7 SIS_NORMA
COURSE = {
"num": 6, "slug": "beneficiario-final", "tag": "Debida diligencia", "level": "Intermedio → Profesional", "minutes": 50,
"title": "Beneficiario final",
"card": "Llegar a la persona física que realmente posee o controla.",
"summary": "Aprende a identificar a la persona física que posee o controla realmente a un cliente: la definición legal y tributaria, el umbral del 20 %, el cálculo de la propiedad indirecta, la secuencia cuando no hay un propietario claro, los fideicomisos, la información mínima que debe obtenerse y las señales de estructuras diseñadas para ocultarla.",
"objectives": [
  "Aplicar la definición de beneficiario final de la Ley 155-17 y del Código Tributario modificado por ella.",
  "Calcular participaciones indirectas a través de una cadena societaria.",
  "Seguir la secuencia propiedad → control por otros medios → mayor rango gerencial.",
  "Identificar al beneficiario final en fideicomisos y entes sin personalidad jurídica.",
  "Conocer la información mínima, su conservación y su actualización.",
  "Reconocer señales de opacidad y el uso de testaferros.",
],
"sources": [LEY, REG, GAFI40, GAFI_BF_M, DGII_BF, DGII_N01, SIS_NORMA],
"modules": [
# 1 ------------------------------------------------------------------------------------------
{"title": "Siempre una persona física", "html": ess(
"Detrás de toda empresa hay personas. El beneficiario final es la persona de carne y hueso que es dueña de verdad o que manda en una empresa, aunque su nombre no aparezca en los papeles. Una empresa nunca puede ser beneficiaria final.") + """
<p>La Ley 155-17 define al <strong>beneficiario final</strong> como la persona física que ejerce el <strong>control efectivo final</strong> sobre una persona jurídica o que tiene como mínimo el <strong>20 % de su capital</strong>, incluyendo a la persona física en beneficio de quien se realiza una transacción (art. 2, num. 5).[[1]]</p>
<p>La misma ley, al modificar el Código Tributario, amplía la idea: beneficiario final es la persona física que ejerce el control efectivo final o es propietaria última de una persona jurídica o ente sin personalidad jurídica, y también aquella en cuyo beneficio se realiza una transacción <strong>aunque no aparezca como titular</strong> ni como quien formalmente la controla (art. 104).[[1]]</p>
<p>Los estándares internacionales insisten en lo mismo: las Recomendaciones 24 y 25 del GAFI exigen que exista información adecuada, precisa y actualizada sobre los beneficiarios finales de personas y estructuras jurídicas, accesible a las autoridades.[[3,4]]</p>
<div class="callout key"><b>Idea clave</b>Una sociedad nunca es beneficiaria final. Si al terminar el análisis el resultado es otra empresa, el trabajo no ha terminado.</div>
""" + deep("""
<p><strong>Por qué importa.</strong> La prohibición de abrir cuentas u ofrecer servicios con nombres falsos, cifrados, anónimos o por cualquier modalidad que encubra la identidad del titular y del <em>beneficiario final</em> (art. 61) muestra que la ley busca evitar que la persona real quede oculta.[[1]] El beneficiario final también es objeto de la verificación en listas de la ONU y del congelamiento preventivo (arts. 82 y 83).[[1]]</p>
<p><strong>Doble función.</strong> La información de beneficiario final sirve a la prevención del lavado (debida diligencia del sujeto obligado) y a la transparencia fiscal (deber formal ante la DGII). Las dos se refuerzan: la UAF y el Ministerio Público pueden solicitar administrativamente la información que esté en poder de los sujetos obligados o de la DGII (Decreto 408-17, art. 44).[[2]]</p>
""")},
# 2 ------------------------------------------------------------------------------------------
{"title": "Calcular la propiedad indirecta", "html": ess(
"La propiedad puede ser directa (tengo acciones de la empresa) o indirecta (tengo acciones de otra empresa que a su vez es dueña). Para saber cuánto tiene alguien de forma indirecta se multiplican los porcentajes de la cadena.") + """
<p>El reglamento ordena identificar y verificar a las personas físicas con participación igual o superior al 20 % de una persona o estructura jurídica (Decreto 408-17, art. 4), y el Código Tributario modificado precisa que la titularidad puede alcanzarse <strong>directa o indirectamente</strong>, a través de una cadena de titularidad u otro medio de control (art. 104).[[1,2]]</p>
<div class="case"><b>Ejemplo resuelto</b>
<p>La empresa cliente «Comercial Alfa, SRL» pertenece en 60 % a «Inversiones Beta, SA» y en 40 % a la Sra. Pérez. A su vez, «Inversiones Beta» pertenece en 50 % al Sr. Gómez y en 50 % al Sr. Díaz.</p>
<ul><li>Sra. Pérez: 40 % directo.</li><li>Sr. Gómez: 50 % × 60 % = 30 % indirecto.</li><li>Sr. Díaz: 50 % × 60 % = 30 % indirecto.</li></ul>
<p class="verdict yes"><b>Resultado:</b> los tres superan el 20 % y son beneficiarios finales por propiedad. Aun así, debe verificarse si otra persona ejerce el control por otros medios.</p></div>
<h3>Familias que suman</h3>
<p>Para fines tributarios, la ley considera que también posee el control efectivo final un <strong>conjunto de personas físicas</strong> unidas por matrimonio, consanguinidad o afinidad hasta el segundo grado, en línea directa o colateral (art. 104).[[1]]</p>
<div class="case"><b>Ejemplo</b><p>Dos hermanos tienen cada uno el 12 % de una sociedad. Ninguno llega al 20 % por separado, pero juntos suman 24 %. Bajo ese criterio, el conjunto familiar alcanza el umbral y conviene identificarlos a ambos.</p></div>
""" + deep("""
<p><strong>Varias cadenas.</strong> Si una misma persona participa por varias vías (directamente y a través de una o más sociedades), se suman sus participaciones de cada cadena. Por ejemplo, 10 % directo más 30 % × 50 % indirecto da 25 %.</p>
<p><strong>Votos y capital.</strong> El Código Tributario modificado habla de «acciones o derechos de voto».[[1]] Cuando una sociedad tiene clases de acciones con votos distintos, analiza ambos: alguien con poco capital y muchos votos puede controlar.</p>
""")},
# 3 ------------------------------------------------------------------------------------------
{"title": "La secuencia de identificación", "html": ess(
"Primero se busca a quien tenga 20 % o más. Si no hay nadie claro, se busca a quien manda por otras vías. Si tampoco aparece, se registra a la persona de mayor cargo gerencial, como último recurso y dejando constancia de lo que se intentó.") + """
<ol class="steps">
<li><strong>Propiedad</strong>: personas físicas con 20 % o más del capital, directa o indirectamente.[[1,2]]</li>
<li><strong>Control por otros medios</strong>: si no es posible determinar con claridad si quien tiene la participación mayoritaria es el beneficiario final, o nadie llega al 20 %, se identifica a quien ejerce el control por otros medios. El reglamento incluye, sin limitarse a ellos, a los controlantes por disposición estatutaria, de hecho o que hayan revelado poder en la toma de decisiones (Decreto 408-17, art. 4, párrafos I y II).[[2]] El Código Tributario lo describe como quien se beneficia del capital o los activos o toma las decisiones relevantes o estratégicas y consigue su ejecución.[[1]]</li>
<li><strong>Mayor rango gerencial</strong>: cuando no se identifica a ninguna persona física por los criterios anteriores, se considera beneficiario final a quien ocupa el puesto de mayor rango gerencial (Decreto 408-17, art. 4, párrafo I).[[2]]</li>
</ol>
<div class="callout warn"><b>Atención</b>El tercer paso es un último recurso, no un atajo. Documenta qué gestiones hiciste en los dos primeros y por qué no fueron concluyentes.</div>
""" + deep("""
<p><strong>Ejemplos de control por otros medios.</strong> Acuerdos de accionistas que otorgan derechos de veto o de nombramiento, poderes generales amplios, financiamiento que condiciona las decisiones, o influencia familiar sobre los socios formales. La guía del GAFI sobre la Recomendación 24 describe este enfoque escalonado y advierte que los porcentajes son un indicio, no el único criterio.[[4]]</p>
<p><strong>Excepciones tributarias.</strong> El Código Tributario modificado exceptúa del deber de información, entre otras, a las sociedades cotizadas en la Bolsa de Valores de la República Dominicana cuando factores como el reducido porcentaje de participación o la existencia de inversores institucionales no justifiquen el costo (art. 104, párrafo IV).[[1]] Esa excepción es tributaria: el sujeto obligado debe seguir aplicando su propio enfoque basado en riesgo.</p>
""")},
# 4 ------------------------------------------------------------------------------------------
{"title": "Fideicomisos y entes sin personalidad jurídica", "html": ess(
"En un fideicomiso no hay «dueños» como en una empresa, sino personas que aportan bienes, que los administran y que se benefician. Hay que identificarlas a todas y saber de dónde salen los bienes.") + """
<p>Las fiduciarias deben identificar y verificar a <strong>todas las partes</strong> del fideicomiso, incluidos el fideicomitente y el beneficiario final, y mantener la información actualizada (art. 41).[[1]] La norma de seguros añade, para los fideicomisos, determinar el origen de los bienes fideicomitidos y de los fondos de los beneficiarios.[[7]]</p>
<p>Para fines tributarios, en fideicomisos, fondos de inversión y entes similares, el beneficiario final es (art. 104, párrafo III, lit. b):[[1]]</p>
<ul>
<li>Si ya se designaron los futuros titulares, la persona física titular del <strong>20 % o más</strong> de los bienes o derechos.</li>
<li>Si los beneficiarios están por designar, la <strong>categoría de personas</strong> en cuyo beneficio se creó o actúa el ente.</li>
<li>Quien ejerce por otros medios el control efectivo final; se incluyen expresamente los residentes en el país que sean fiduciarios (<em>trustees</em>), fideicomitentes (<em>settlors</em>) o beneficiarios de <em>trusts</em> o fideicomisos extranjeros.</li>
</ul>
""" + deep("""
<p><strong>Productos de oferta pública.</strong> El reglamento exceptúa a los fondos de inversión, fideicomisos de oferta pública y patrimonios separados de titularización respecto de los tenedores de sus valores, aunque las autoridades pueden acceder a esa información a través de los sujetos obligados del mercado de valores (Decreto 408-17, art. 41, párrafo).[[2]]</p>
<p><strong>Recomendación 25.</strong> El GAFI exige que los fiduciarios de fideicomisos expresos tengan información adecuada, precisa y actualizada sobre el fideicomitente, los fiduciarios, el protector, los beneficiarios o la clase de beneficiarios y cualquier persona que ejerza el control efectivo final.[[3]]</p>
""")},
# 5 ------------------------------------------------------------------------------------------
{"title": "Información mínima, conservación y actualización", "html": ess(
"De cada beneficiario final se necesita su identificación, su número tributario, su domicilio y cuánto controla. Esa documentación se guarda diez años y, si cambia el beneficiario, la DGII debe saberlo en seis meses.") + """
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Aspecto</th><th>Regla (Decreto 408-17)</th></tr></thead>
<tbody>
<tr><td>Datos mínimos (art. 39)</td><td>Cédula, documento de identidad o pasaporte vigentes; número de identificación tributaria del país de residencia fiscal; nombre completo; domicilio; porcentaje de participación o control efectivo.</td></tr>
<tr><td>Cadenas (art. 39, párrafo)</td><td>Identificación de cada entidad de la cadena de titularidad o control, con su identificación tributaria, domicilio y porcentaje.</td></tr>
<tr><td>Conservación (art. 40)</td><td>La documentación de soporte debe estar disponible para las autoridades durante 10 años; la conservación digital es válida.</td></tr>
<tr><td>Actualización (art. 42)</td><td>Se informa a la DGII cada año en la declaración jurada del Impuesto sobre la Renta u otro medio que disponga, y cualquier cambio debe notificarse en un plazo no mayor de 6 meses.</td></tr>
</tbody></table></div>
<p class="note-small">Elaborado a partir del Decreto 408-17.[[2]]</p>
<p>La Ley 155-17, al modificar el Código Tributario, convirtió en deber formal de las personas jurídicas y entes sin personalidad jurídica disponer de información actualizada de sus beneficiarios finales.[[1,5]] Para el sujeto obligado esto significa que el cliente <strong>debería poder entregar</strong> esa información; si no puede o no quiere, es una señal que merece análisis.</p>
""" + deep("""
<p><strong>Verificar, no solo recibir.</strong> El art. 38 exige tomar medidas razonables para verificar la identidad del beneficiario final con información o datos de fuentes confiables.[[1]] Contrasta lo declarado con el registro mercantil, actas de asamblea, libros de accionistas y fuentes públicas.</p>
<p><strong>Si el beneficiario final es PEP.</strong> El reglamento exige debida diligencia ampliada a las PEP aun cuando sean beneficiarias finales de los clientes (Decreto 408-17, art. 18), y la DGII lo reitera para sus sujetos obligados.[[2,6]]</p>
""")},
# 6 ------------------------------------------------------------------------------------------
{"title": "Señales de opacidad y testaferros", "html": ess(
"Hay estructuras armadas para esconder al verdadero dueño: muchas empresas en cadena sin motivo, socios que no parecen tener dinero para el negocio, poderes amplios a desconocidos o cambios frecuentes de dueños. Cuando aparecen, hay que profundizar.") + """
<p>La ley define al <strong>testaferro</strong> como la persona física o jurídica que hace aparentar como propios los activos y bienes de un tercero procedentes de actividades ilícitas, cuyo propietario real no figura en los documentos de titularidad (art. 2, num. 26).[[1]]</p>
<ul>
<li>Cadenas de sociedades sin una razón comercial que las explique, especialmente con jurisdicciones de baja transparencia.</li>
<li>Socios o administradores que no parecen tener el perfil ni los recursos para el negocio.</li>
<li>Poderes amplios otorgados a terceros sin relación aparente.</li>
<li>Cambios frecuentes de accionistas o administradores sin explicación.</li>
<li>Resistencia a entregar documentos societarios o información de los propietarios.</li>
</ul>
<div class="callout warn"><b>Diligencia ampliada obligatoria (DGII)</b>La Norma 01-2018 exige diligencia ampliada para sociedades con estructura accionaria y de control inusual o excesivamente compleja, y para operaciones en beneficio de entidades con participaciones en sociedades «de carpeta», formadas sin actividad económica real para su posterior transmisión a terceros.[[6]]</div>
""" + deep("""
<p><strong>Acciones al portador y nominatarios.</strong> La guía del GAFI identifica como riesgos típicos las acciones al portador, los accionistas y directores nominales y el uso de intermediarios profesionales para crear estructuras complejas.[[4]] Entre las actividades que convierten a abogados y contadores en sujetos obligados está, precisamente, actuar o disponer que otra persona actúe como director o accionista nominal (Ley 155-17, art. 33, lit. e).[[1]]</p>
""")},
# 7 ------------------------------------------------------------------------------------------
{"title": "Caso integrador", "html": ess(
"Un caso con una cadena de empresas, un socio extranjero y un administrador con poderes amplios.") + """
<div class="case"><b>Caso · «Agroexport Delta, SRL»</b>
<p>Delta solicita abrir una cuenta para exportar productos agrícolas. Sus socios son «Holding Gamma Ltd.» (70 %), constituida en el extranjero, y el Sr. Ramírez (30 %). El gerente general, Sr. Núñez, tiene un poder general amplio otorgado por Gamma.</p>
<ol>
<li><strong>Propiedad:</strong> el Sr. Ramírez es beneficiario final (30 %). Gamma no puede serlo: se piden sus documentos societarios y la identificación de sus propietarios.</li>
<li><strong>Hallazgo:</strong> Gamma pertenece en partes iguales a dos personas físicas extranjeras (35 % indirecto cada una). Ambas son beneficiarias finales.</li>
<li><strong>Control:</strong> el poder del Sr. Núñez se revisa; si toma las decisiones estratégicas por cuenta propia, también podría ejercer control por otros medios.[[2]]</li>
<li><strong>Riesgo:</strong> la estructura con una sociedad extranjera y poderes amplios aconseja diligencia ampliada; se verifica en listas a todos los beneficiarios finales.[[1,6]]</li>
<li><strong>Registro:</strong> se documenta la cadena completa con porcentajes, identificaciones y fuentes de verificación.[[2]]</li>
</ol>
<p class="verdict yes"><b>Lección:</b> el resultado no es «Gamma Ltd.», sino tres o cuatro personas con nombre, documento y porcentaje.</p>
</div>
"""},
],
"glossary": [
("Beneficiario final", "Persona física que ejerce el control efectivo final o tiene como mínimo el 20 % del capital, o en cuyo beneficio se realiza la transacción [[1]]."),
("Propiedad indirecta", "Participación que se obtiene a través de otras sociedades; se calcula multiplicando los porcentajes de la cadena."),
("Control por otros medios", "Control sin participación suficiente: por estatutos, de hecho o por poder revelado en las decisiones [[2]]."),
("Cadena de titularidad", "Sucesión de entidades entre el cliente y sus beneficiarios finales [[2]]."),
("Fideicomitente (settlor)", "Quien aporta los bienes a un fideicomiso [[1]]."),
("Fiduciario (trustee)", "Quien administra los bienes del fideicomiso [[1]]."),
("Testaferro", "Quien aparenta como propios bienes ilícitos de un tercero que no figura como titular (art. 2, num. 26) [[1]]."),
("Sociedad de carpeta", "Sociedad formada sin actividad económica real para su posterior transmisión a terceros [[6]]."),
],
"quiz": [
{"q": "Según la Ley 155-17, ¿qué porcentaje mínimo de capital convierte a una persona física en beneficiaria final por propiedad?", "options": ["10 %", "20 %", "25 %", "50 %"], "answer": 1, "explain": "El art. 2, num. 5 establece como mínimo el 20 % del capital, además del control efectivo final [[1]]."},
{"q": "La sociedad X posee 80 % del cliente. El Sr. A posee 30 % de X. ¿Cuál es la participación indirecta del Sr. A?", "options": ["30 %", "24 %", "80 %", "10 %"], "answer": 1, "explain": "Se multiplican los porcentajes: 30 % × 80 % = 24 %, por encima del umbral."},
{"q": "Una persona tiene solo 5 % del capital, pero por un acuerdo de accionistas decide todas las inversiones. ¿Es beneficiaria final?", "options": ["No, porque no llega al 20 %", "Sí, por ejercer el control por otros medios", "Solo si es PEP", "Depende del monto invertido"], "answer": 1, "explain": "La definición incluye a quien ejerce el control efectivo final, con independencia de su porcentaje [[1,2]]."},
{"q": "Tras agotar los criterios de propiedad y control sin resultado, ¿a quién se considera beneficiario final?", "options": ["A la propia sociedad", "A quien ocupa el puesto de mayor rango gerencial", "Al contador externo", "A nadie"], "answer": 1, "explain": "El Decreto 408-17, art. 4, lo indica como último recurso [[2]]."},
{"q": "El análisis de propiedad termina en «Holding Gamma Ltd.», sociedad extranjera. ¿Qué corresponde?", "options": ["Registrar a Gamma como beneficiaria final", "Continuar hasta identificar a las personas físicas detrás de Gamma", "Cerrar el expediente", "Pedir solo el logo de la empresa"], "answer": 1, "explain": "El beneficiario final es siempre una persona física [[1]]."},
{"q": "Para fines tributarios, dos hermanos con 12 % cada uno de una sociedad:", "options": ["Nunca se consideran", "Pueden considerarse como un conjunto que alcanza el umbral del 20 %", "Solo cuenta el mayor", "Deben ser PEP"], "answer": 1, "explain": "El art. 104 considera el conjunto de personas unidas por parentesco hasta el segundo grado [[1]]."},
{"q": "En un fideicomiso cuyos beneficiarios aún no se han designado, ¿quién se considera beneficiario final para fines tributarios?", "options": ["Nadie", "La categoría de personas en cuyo beneficio se creó o actúa el ente", "El notario", "El banco depositario"], "answer": 1, "explain": "Así lo establece el art. 104, párrafo III, lit. b, num. 2 [[1]]."},
{"q": "¿Cuál de estos datos forma parte de la información mínima del beneficiario final del art. 39 del Decreto 408-17?", "options": ["Su color favorito", "Su número de identificación tributaria del país de residencia fiscal", "Su historial médico", "Su religión"], "answer": 1, "explain": "El art. 39 incluye identificación, número tributario, nombre, domicilio y porcentaje de participación o control [[2]]."},
{"q": "Si cambia el beneficiario final de una entidad, ¿en qué plazo debe notificarse a la DGII?", "options": ["Un mes", "No mayor de 6 meses", "Dos años", "No se notifica"], "answer": 1, "explain": "El Decreto 408-17, art. 42, fija un plazo no mayor de 6 meses desde el cambio [[2]]."},
{"q": "Según la ley, un testaferro es:", "options": ["Un tipo de fideicomiso", "Quien aparenta como propios bienes ilícitos de un tercero que no figura como titular", "Un auditor externo", "Un beneficiario de seguro"], "answer": 1, "explain": "Es la definición del art. 2, num. 26 [[1]]."},
{"q": "Si el beneficiario final de un cliente es una PEP, ¿qué corresponde?", "options": ["Ninguna medida adicional", "Debida diligencia ampliada, aunque la PEP no sea el cliente directo", "Un ROS automático", "Rechazo inmediato"], "answer": 1, "explain": "El Decreto 408-17, art. 18, exige diligencia ampliada a las PEP aun cuando sean beneficiarias finales [[2]]."},
],
}
