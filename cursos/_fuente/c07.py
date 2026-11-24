"""Curso 07 · Personas expuestas políticamente."""
from fuentes import *  # noqa: F401,F403
from capas import ess, deep

# 1 LEY · 2 GAFI40 · 3 GAFI_PEP_M · 4 UAF_ROS · 5 LEY_311 · 6 REG · 7 CONCLAFIT_2021_02 · 8 SIS_NORMA · 9 DGII_N01
COURSE = {
"num": 7, "slug": "personas-expuestas-politicamente", "tag": "Debida diligencia", "level": "Intermedio → Profesional", "minutes": 50,
"title": "Personas Expuestas Políticamente (PEP)",
"card": "Quién es PEP, a quién alcanza y qué medidas aplicar sin estigmatizar.",
"summary": "Identifica a las personas expuestas políticamente según la ley, el reglamento y el CONCLAFIT; extiende las medidas a familiares y asociados cercanos; aplica la debida diligencia ampliada que exige la normativa y distingue con claridad entre alto riesgo y operación sospechosa.",
"objectives": [
  "Aplicar la definición legal de PEP, su alcance temporal y la lista de cargos del Decreto 408-17.",
  "Conocer las precisiones del CONCLAFIT sobre los funcionarios consulares honorarios.",
  "Identificar a familiares y asociados cercanos alcanzados por las medidas.",
  "Diseñar las medidas de debida diligencia ampliada para una PEP, también cuando es beneficiaria final o beneficiaria de un seguro.",
  "Distinguir entre alto riesgo y operación sospechosa.",
  "Gestionar la condición de PEP en el tiempo.",
],
"sources": [LEY, GAFI40, GAFI_PEP_M, UAF_ROS, LEY_311, REG, CONCLAFIT_2021_02, SIS_NORMA, DGII_N01],
"modules": [
# 1 ------------------------------------------------------------------------------------------
{"title": "¿Quién es PEP?", "html": ess(
"Una PEP es alguien que ocupa o ocupó en los últimos tres años un cargo público importante, aquí o en otro país. Por el poder que tiene, corre más riesgo de que intenten usarlo para la corrupción. Por eso se le aplica más control, no porque se sospeche de ella.") + """
<p>Según la Ley 155-17, una <strong>persona expuesta políticamente</strong> es cualquier individuo que desempeña o ha desempeñado, <strong>durante los últimos tres años</strong>, altas funciones públicas por elección o nombramiento, en el país o en el extranjero, incluidos altos funcionarios de organizaciones internacionales (art. 2, num. 19).[[1]]</p>
<p>La definición incluye, sin limitarse a ellos, a jefes de Estado o de gobierno, funcionarios gubernamentales, judiciales o militares de alta jerarquía y altos ejecutivos de empresas estatales, así como a quienes determine el Comité Nacional. Y fija un criterio práctico: los cargos PEP son <strong>todos los funcionarios obligados a presentar declaración jurada de bienes</strong>; se asimilan quienes ejerzan funciones equivalentes para gobiernos extranjeros.[[1,5]]</p>
<div class="callout key"><b>Por qué importa</b>Por su posición, una PEP puede tener acceso a recursos públicos o influencia sobre decisiones que la hacen más vulnerable a la corrupción. Las medidas reforzadas existen para gestionar ese riesgo, no para presumir culpa.[[3]]</div>
""" + deep("""
<p><strong>Tres tipos de PEP en el estándar internacional.</strong> La guía del GAFI distingue PEP extranjeras, PEP nacionales y personas que tienen o tuvieron funciones prominentes en organizaciones internacionales. Para las extranjeras, la Recomendación 12 exige siempre medidas ampliadas; para las nacionales y de organismos internacionales, las medidas ampliadas se aplican cuando la relación presenta un riesgo mayor.[[2,3]]</p>
<p><strong>La ley dominicana va más allá.</strong> El art. 46 de la Ley 155-17 considera a todas las PEP, sin distinguir su origen, factor de alto riesgo como mínimo, y el reglamento exige debida diligencia ampliada a las PEP (Decreto 408-17, art. 18).[[1,6]]</p>
""")},
# 2 ------------------------------------------------------------------------------------------
{"title": "Los cargos del Decreto 408-17", "html": ess(
"El reglamento trae una lista larga de cargos que se consideran PEP: desde el presidente hasta alcaldes, regidores, jueces, ministros, directores de instituciones, militares y policías de mando, embajadores y encargados de compras públicas.") + """
<p>El Decreto 408-17 considera PEP a todos los funcionarios obligados a presentar declaración jurada de bienes según el art. 2 de la Ley 311-14, y los enumera (art. 19). Algunos grupos:[[6]]</p>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Ámbito</th><th>Ejemplos de cargos</th></tr></thead>
<tbody>
<tr><td>Poderes del Estado</td><td>Presidente y vicepresidente; senadores, diputados y secretarios administrativos de las cámaras; jueces de la Suprema Corte, del Tribunal Constitucional, del Tribunal Superior Electoral y demás jueces del orden judicial; procurador general y miembros del Ministerio Público.</td></tr>
<tr><td>Administración</td><td>Ministros y viceministros; directores nacionales y generales y subdirectores de órganos centralizados y descentralizados; administradores y subadministradores generales; Tesorero Nacional; Contralor General.</td></tr>
<tr><td>Órganos de control y electorales</td><td>Defensor del Pueblo; miembros de la Cámara de Cuentas y de la Junta Central Electoral; Director Nacional de Elecciones; Director Nacional de Registro Civil.</td></tr>
<tr><td>Banca y empresas públicas</td><td>Gobernador, vicegobernador, gerente y contralor del Banco Central; miembros de la Junta Monetaria; administradores y gerentes de bancos estatales; presidentes, superintendentes y administradores de empresas estatales.</td></tr>
<tr><td>Gobiernos locales</td><td>Alcaldes, vicealcaldes, regidores y tesoreros municipales; directores y tesoreros de distritos municipales; gobernadores provinciales.</td></tr>
<tr><td>Seguridad</td><td>Jefes y subjefes de Estado Mayor y oficiales en posiciones de mando operativo o de administración; jefe y subjefe de la Policía Nacional; titulares de cuerpos de seguridad e inteligencia; presidente de la DNCD.</td></tr>
<tr><td>Otros</td><td>Embajadores, cónsules generales y representantes ante organismos internacionales; rector y vicerrectores de la UASD; encargados de compras de las cámaras, la Suprema Corte, ministerios y direcciones generales.</td></tr>
</tbody></table></div>
<p class="note-small">Selección del art. 19 del Decreto 408-17; consulta la lista completa en la norma.[[6]]</p>
""" + deep("""
<p><strong>Quiénes no.</strong> No se consideran PEP quienes, sin ser funcionarios gubernamentales, formen parte de órganos colegiados consultivos o de coordinación, salvo los consejos de administración de órganos autónomos del Estado y el Consejo de Seguridad Social (art. 19, párrafo I).[[6]]</p>
<p><strong>Qué es «funcionario».</strong> El reglamento remite a la Ley 41-08 de Función Pública: funcionarios de libre nombramiento y remoción, de carrera, de estatuto simplificado o empleados temporales (art. 19, párrafo II).[[6]]</p>
<p><strong>Instituciones futuras.</strong> La lista incluye a los funcionarios de cualquier institución autónoma, centralizada o descentralizada que se cree en el futuro y administre fondos públicos (art. 19, lit. ii).[[6]]</p>
""")},
# 3 ------------------------------------------------------------------------------------------
{"title": "Funcionarios consulares honorarios", "html": ess(
"Hubo dudas sobre si los cónsules honorarios —que no cobran salario del Estado ni presentan declaración jurada— son PEP. El CONCLAFIT resolvió que sí: tanto los cónsules generales honorarios como los cónsules y vicecónsules honorarios.") + """
<p>Mediante la Resolución 02-2021, del 15 de diciembre de 2021, el CONCLAFIT:[[7]]</p>
<ul>
<li><strong>Ratificó</strong> la condición de PEP de los <strong>Cónsules Generales Honorarios</strong>, porque en su caso el riesgo no recae en la presentación de una declaración jurada de bienes, sino en su influencia en la toma de decisiones por la prominencia de la función.</li>
<li><strong>Determinó</strong> que los <strong>Cónsules y Vicecónsules Honorarios</strong> también son PEP, por lo que representan en su función como figuras públicas prominentes que representan a un Estado, y que debe dárseles el tratamiento de la Ley 155-17 y su reglamentación.</li>
</ul>
<p>La resolución explica que, aunque estos funcionarios no perciben salario estatal ni pertenecen a la carrera administrativa, su nombramiento no es simbólico: los habilita para ejercer múltiples atribuciones consulares, lo que revela la prominencia de la función.[[7]]</p>
<div class="callout tip"><b>Lección de método</b>El criterio decisivo no es el sueldo ni el formulario, sino la <strong>prominencia de la función</strong> y el riesgo que de ella deriva.</div>
""" + deep("""
<p><strong>Base legal.</strong> La resolución se apoya en la facultad del Comité Nacional de determinar otros PEP, previa consulta con el Ministerio de Administración Pública, prevista en el art. 2, num. 19, de la ley; el expediente recoge las consultas al Ministerio de Relaciones Exteriores y al MAP.[[1,7]]</p>
""")},
# 4 ------------------------------------------------------------------------------------------
{"title": "El círculo cercano", "html": ess(
"El riesgo de una PEP puede pasar a su familia y a sus socios cercanos. Por eso también se revisa, según el riesgo, al cónyuge o pareja, a los parientes hasta el segundo grado, a los asociados cercanos y a quien opera en su nombre.") + """
<p>La ley extiende un enfoque basado en riesgos para la debida diligencia y el monitoreo de (art. 46, párrafo):[[1]]</p>
<ul>
<li>Cónyuge, unión libre o concubinato.</li>
<li>Parientes hasta el <strong>segundo grado</strong> de consanguinidad o afinidad.</li>
<li>Asociados cercanos.</li>
<li>Quien realice operaciones en nombre de la PEP.</li>
</ul>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Grado</th><th>Consanguinidad</th><th>Afinidad</th></tr></thead>
<tbody>
<tr><td>Primer grado</td><td>Padres e hijos</td><td>Suegros, yernos y nueras</td></tr>
<tr><td>Segundo grado</td><td>Abuelos, nietos y hermanos</td><td>Cuñados</td></tr>
</tbody></table></div>
<p>Cuando alguna de esas personas se identifica como cliente de <strong>alto riesgo</strong>, el reglamento exige aplicarle debida diligencia ampliada (Decreto 408-17, art. 18, párrafo).[[6]]</p>
""" + deep("""
<p><strong>Asociados cercanos.</strong> La guía del GAFI incluye entre ellos a personas con relaciones comerciales estrechas con la PEP o que comparten la titularidad de estructuras jurídicas, y a quienes tienen relaciones personales estrechas conocidas.[[3]] Identificarlos requiere información pública y lo que el propio cliente declare.</p>
<p><strong>Seguros.</strong> La norma de seguros reproduce esta regla y precisa que, si la persona resulta de alto riesgo por su relación con una PEP, deben aplicarse todas las medidas de diligencia ampliada previstas para las PEP.[[8]]</p>
""")},
# 5 ------------------------------------------------------------------------------------------
{"title": "Medidas de debida diligencia ampliada", "html": ess(
"Con una PEP hay que hacer cuatro cosas: detectarla a tiempo, que un alto directivo apruebe la relación, entender de dónde vienen su dinero y su patrimonio, y vigilar la relación más de cerca.") + """
<p>El reglamento exige debida diligencia ampliada a las PEP, <strong>aun cuando sean beneficiarias finales</strong> de los clientes, con estas actuaciones (Decreto 408-17, art. 18):[[6]]</p>
<ol class="steps">
<li><strong>Aprobación de la alta gerencia</strong> antes de establecer —o continuar, si ya es cliente— la relación.</li>
<li><strong>Medidas razonables para identificar el origen</strong> de los fondos o activos de los clientes y beneficiarios finales que sean PEP.</li>
<li><strong>Monitoreo intensificado</strong> de la relación de negocios.</li>
</ol>
<p>Antes de todo eso hay que <strong>identificar la condición</strong>: la norma de seguros pide sistemas de gestión de riesgos apropiados para determinar si el cliente es PEP y procedimientos «conozca su cliente» para saber si la operación se hace por o en beneficio de una PEP.[[8]] La DGII exige además aplicar los controles de PEP cuando el beneficiario final de una persona jurídica sea una PEP.[[9]]</p>
<div class="callout tip"><b>En la práctica</b>Pregunta por la fuente de riqueza (cómo construyó su patrimonio) y por la fuente de los fondos de la operación concreta. Son preguntas distintas y ambas importan.[[3]]</div>
""" + deep("""
<p><strong>Variantes sectoriales.</strong> La Norma 01-2018 de la DGII pide la aprobación de la alta gerencia <em>y/o</em> del consejo de administración.[[9]] La norma de seguros habla de <em>notificar</em> a la alta gerencia antes de establecer o continuar la relación, de determinar el origen del patrimonio y de los fondos a invertir y de un monitoreo reforzado de las transacciones en efectivo.[[8]] Como el reglamento exige aprobación, conviene que el procedimiento interno documente una aprobación expresa.</p>
<p><strong>PEP como beneficiaria de un seguro de vida.</strong> Las aseguradoras deben tomar medidas razonables para determinar si los beneficiarios, o el beneficiario final del beneficiario, son PEP, a más tardar en el momento del pago, y reportar cualquier actividad sospechosa.[[8]] La Recomendación 12 del GAFI prevé lo mismo para las pólizas de seguro de vida.[[2]]</p>
""")},
# 6 ------------------------------------------------------------------------------------------
{"title": "Ser PEP no es una sospecha", "html": ess(
"Un error común es reportar a la UAF a un cliente solo por ser PEP. No es así: ser PEP obliga a investigarlo más, pero solo se reporta si aparece algo sospechoso.") + """
<p>La UAF aclara que las PEP deben clasificarse como de alto riesgo y recibir debida diligencia ampliada, pero <strong>no deben reportarse por pertenecer a esa categoría</strong>, salvo que se identifique una situación sospechosa vinculada a un delito precedente.[[4]]</p>
<div class="case"><b>Caso</b>
<p>Una directora general de una institución pública solicita un préstamo hipotecario. Sus ingresos declarados y su historial bancario son coherentes con la cuota.</p>
<p class="verdict no"><b>Decisión:</b> se aplica debida diligencia ampliada y aprobación de la alta gerencia; no procede ROS. Si luego recibiera depósitos de contratistas del Estado sin explicación, el análisis cambiaría.</p></div>
<h3>Señales que sí merecen análisis</h3>
<ul>
<li>Fondos o patrimonio claramente desproporcionados respecto de los ingresos conocidos del cargo.</li>
<li>Pagos de terceros vinculados a contrataciones con la institución que dirige la PEP.</li>
<li>Uso de familiares, asociados o sociedades para mover fondos que parecen pertenecer a la PEP.</li>
<li>Resistencia a explicar el origen de los fondos o del patrimonio.</li>
</ul>
<p class="note-small">Ejemplos ilustrativos coherentes con las situaciones de riesgo que describe la guía del GAFI sobre PEP.[[3]]</p>
""" + deep("""
<p><strong>Rechazo y desbancarización.</strong> La guía del GAFI advierte que las medidas para PEP no deben llevar a rechazar a todas las PEP por el solo hecho de serlo; la decisión debe basarse en la evaluación de riesgo de cada relación.[[3]]</p>
""")},
# 7 ------------------------------------------------------------------------------------------
{"title": "La condición en el tiempo", "html": ess(
"Una persona deja de ser PEP por ley tres años después de dejar el cargo. Pero si su influencia sigue, la entidad puede mantener los controles más tiempo. Lo importante es anotar las fechas y revisar la condición cuando toque.") + """
<p>La definición legal cubre a quien ejerció el cargo en los últimos tres años.[[1]] El enfoque basado en riesgos permite mantener medidas reforzadas más allá de ese plazo cuando la influencia o los riesgos persisten; la guía del GAFI recomienda que esa decisión se base en el riesgo y no solo en el paso del tiempo.[[3]]</p>
<ul>
<li>Registra la fecha de inicio y de término del cargo.</li>
<li>Programa la revisión de la condición al cumplirse el plazo.</li>
<li>Documenta la decisión de mantener o ajustar las medidas.</li>
<li>Revisa periódicamente la cartera contra fuentes de nombramientos y declaraciones juradas, porque un cliente puede <strong>convertirse</strong> en PEP durante la relación; en ese caso se requiere la aprobación para <strong>continuarla</strong>.[[6]]</li>
</ul>
""" + deep("""
<p><strong>Fuentes para identificar PEP.</strong> La declaración del propio cliente (la norma de seguros exige preguntar expresamente si posee la calidad de PEP), las listas de funcionarios obligados a declarar patrimonio, los nombramientos publicados y bases comerciales. Ninguna basta por sí sola.[[5,8]]</p>
""")},
],
"glossary": [
("PEP", "Quien desempeña o desempeñó en los últimos 3 años altas funciones públicas, en el país o en el extranjero (art. 2, num. 19) [[1]]."),
("Declaración jurada de patrimonio", "Obligación de ciertos funcionarios según la Ley 311-14; quienes la tienen son PEP [[1,5]]."),
("Asociado cercano", "Persona con relación comercial o personal estrecha conocida con una PEP [[3]]."),
("Fuente de riqueza", "Origen del patrimonio total de la persona [[3]]."),
("Fuente de fondos", "Origen del dinero usado en una operación concreta [[3]]."),
("Alta gerencia", "Nivel directivo que debe aprobar iniciar o continuar la relación con una PEP [[6]]."),
("Monitoreo intensificado", "Seguimiento más frecuente y profundo de la relación con una PEP [[6]]."),
("Prominencia de la función", "Criterio del CONCLAFIT para considerar PEP a los funcionarios consulares honorarios [[7]]."),
],
"quiz": [
{"q": "Según la Ley 155-17, ¿durante qué período posterior al cargo se mantiene la condición de PEP?", "options": ["1 año", "Los últimos 3 años", "5 años", "De por vida"], "answer": 1, "explain": "La definición abarca a quien desempeña o ha desempeñado altas funciones públicas durante los últimos tres años [[1]]."},
{"q": "¿Qué criterio práctico fija la ley para determinar los cargos PEP?", "options": ["Tener un salario alto", "Ser funcionario obligado a presentar declaración jurada de bienes", "Haber sido candidato", "Tener más de 50 años"], "answer": 1, "explain": "La ley dispone que los cargos PEP son todos los funcionarios obligados a declarar bienes [[1]]."},
{"q": "¿Cuál de estos cargos figura en la lista de PEP del Decreto 408-17?", "options": ["Cajero de un banco privado", "Regidor municipal", "Maestro de escuela privada", "Gerente de una tienda"], "answer": 1, "explain": "El art. 19, lit. p, incluye a alcaldes, vicealcaldes, regidores y tesoreros municipales [[6]]."},
{"q": "Según la Resolución CONCLAFIT 02-2021, los Cónsules y Vicecónsules Honorarios:", "options": ["No son PEP porque no cobran salario", "Son PEP y deben recibir el tratamiento de la Ley 155-17", "Solo son PEP si declaran bienes", "Son PEP solo en su país de residencia"], "answer": 1, "explain": "La resolución determina que son PEP por la prominencia de su función [[7]]."},
{"q": "¿Hasta qué grado de parentesco alcanza el art. 46 a los familiares de una PEP?", "options": ["Primer grado", "Segundo grado", "Cuarto grado", "Solo el cónyuge"], "answer": 1, "explain": "El párrafo del art. 46 incluye a parientes hasta el segundo grado, cónyuges y uniones de hecho [[1]]."},
{"q": "El cuñado de un ministro abre una cuenta. ¿Está alcanzado por las medidas?", "options": ["No, la afinidad no cuenta", "Sí, es pariente por afinidad en segundo grado", "Solo si vive con el ministro", "Solo si es funcionario"], "answer": 1, "explain": "El cuñado es pariente por afinidad en segundo grado, dentro del alcance del art. 46 [[1]]."},
{"q": "¿Qué medidas exige el art. 18 del Decreto 408-17 para una PEP?", "options": ["Cobrarle comisiones más altas", "Aprobación de la alta gerencia, origen de los fondos y monitoreo intensificado", "Reportarla a la UAF", "Negarle el servicio"], "answer": 1, "explain": "Son las tres actuaciones del art. 18 [[6]]."},
{"q": "Un cliente persona jurídica tiene como beneficiario final a una PEP. ¿Aplica la debida diligencia ampliada?", "options": ["No, la PEP no es el cliente", "Sí, el reglamento la exige aun cuando la PEP sea beneficiaria final", "Solo si la PEP es extranjera", "Solo si lo pide la UAF"], "answer": 1, "explain": "El art. 18 del Decreto 408-17 lo establece expresamente [[6]]."},
{"q": "En un seguro de vida, ¿hasta cuándo debe determinarse si el beneficiario es PEP?", "options": ["Nunca", "A más tardar en el momento del pago", "Solo al emitir la póliza", "Cinco años después del pago"], "answer": 1, "explain": "La norma de seguros lo exige a más tardar en el momento del pago [[8]]."},
{"q": "Un cliente es identificado como PEP y su operativa es coherente con su perfil. ¿Procede un ROS?", "options": ["Sí, siempre", "No; se aplica diligencia ampliada, pero ser PEP no es motivo de reporte por sí solo", "Sí, pero como RTE", "Solo si es extranjero"], "answer": 1, "explain": "La UAF aclara que la condición de PEP no debe reportarse por sí misma [[4]]."},
{"q": "¿Qué diferencia hay entre fuente de riqueza y fuente de fondos?", "options": ["Son lo mismo", "La riqueza explica cómo se formó el patrimonio; los fondos, de dónde viene el dinero de una operación concreta", "La riqueza solo aplica a empresas", "Los fondos solo aplican a efectivo"], "answer": 1, "explain": "Ambas se indagan en la diligencia ampliada y responden preguntas distintas [[3]]."},
{"q": "Un cliente existente es nombrado viceministro. ¿Qué corresponde?", "options": ["Nada, ya era cliente", "Obtener la aprobación de la alta gerencia para continuar la relación y aplicar diligencia ampliada", "Cerrar la cuenta", "Esperar tres años"], "answer": 1, "explain": "El art. 18 exige aprobación para establecer o continuar la relación con una PEP [[6]]."},
],
}
