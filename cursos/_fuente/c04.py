"""Curso 04 · Matrices de evaluación y segmentación."""
from fuentes import *  # noqa: F401,F403
from capas import ess, deep

# 1 LEY · 2 GAFI40 · 3 GAFI_RBA · 4 ISO_31000 · 5 DGII_N01 · 6 CNV_NORMA · 7 SIS_NORMA · 8 IDECOOP_NORMA · 9 CASINOS_104 · 10 REG
COURSE = {
"num": 4, "slug": "matrices-de-evaluacion-y-segmentacion", "tag": "Riesgos", "level": "Intermedio → Profesional", "minutes": 55,
"title": "Matrices de evaluación y segmentación",
"card": "Diseño de matrices de riesgo de clientes, ponderaciones y segmentación.",
"summary": "Diseña y aplica una matriz de riesgo de clientes: qué exigen las normas, qué variables elegir, cómo construir escalas y ponderaciones, cómo convertir el puntaje en niveles de riesgo y medidas de debida diligencia, y cómo segmentar y gobernar la matriz, con un ejemplo resuelto.",
"objectives": [
  "Diferenciar la autoevaluación de riesgos de la entidad de la matriz de riesgo de clientes.",
  "Identificar los requisitos mínimos que piden las normas sectoriales a una matriz.",
  "Construir una matriz con variables, escalas y ponderaciones justificadas, y reglas de prevalencia.",
  "Calcular el nivel de riesgo de un cliente y vincularlo a medidas de debida diligencia.",
  "Usar la segmentación para definir perfiles y umbrales de monitoreo.",
  "Gobernar la matriz: aprobación, calibración, actualización y trazabilidad.",
],
"sources": [LEY, GAFI40, GAFI_RBA, ISO_31000, DGII_N01, CNV_NORMA, SIS_NORMA, IDECOOP_NORMA, CASINOS_104, REG],
"modules": [
# 1 ------------------------------------------------------------------------------------------
{"title": "Dos matrices, dos propósitos", "html": ess(
"Se suele hablar de «la matriz», pero hay dos: una mide los riesgos de la empresa completa (cómo podrían usarla para lavar dinero) y otra califica a cada cliente. La primera orienta el programa; la segunda decide cuánto investigar a cada persona.") + """
<div class="grid-2">
<div class="mini"><h4>Autoevaluación de riesgos de la entidad</h4><p>Identifica cómo podría la entidad ser utilizada para lavar activos o financiar el terrorismo, mide esos eventos y evalúa sus controles. Orienta el programa de cumplimiento completo.</p></div>
<div class="mini"><h4>Matriz de riesgo de clientes</h4><p>Asigna a cada cliente un nivel de riesgo a partir de sus características. Decide el tipo de debida diligencia y la intensidad del monitoreo.</p></div>
</div>
<p>Ambas responden al mandato de gestionar el riesgo considerando, como mínimo, clientes, productos y servicios, áreas geográficas y canales (art. 37).[[1]] Las normas las definen así:</p>
<ul>
<li><strong>DGII (Norma 01-2018):</strong> la matriz de riesgo es la herramienta o sistema que permite clasificar a los clientes, como mínimo, en bajo, medio y alto riesgo, para aplicar una debida diligencia diferenciada.[[5]]</li>
<li><strong>Mercado de valores:</strong> la matriz es una herramienta analítica que los sujetos obligados deben elaborar y actualizar periódicamente para determinar su grado de exposición al riesgo y las brechas de su programa frente a los requerimientos regulatorios.[[6]]</li>
</ul>
<p>En seguros y casinos, elaborar la matriz de riesgo según los factores de la norma es una función expresa del oficial de cumplimiento.[[7,9]]</p>
""" + deep("""
<p><strong>Por qué importa la diferencia.</strong> Una entidad puede tener muchos clientes de riesgo bajo y, aun así, un riesgo alto como institución si sus controles son débiles o si ofrece un producto muy expuesto. La autoevaluación captura esa visión de conjunto; la matriz de clientes, no. Por eso la norma de seguros pide seguir la evolución del perfil de riesgo inherente y residual de la entidad, no solo de cada cliente.[[7]]</p>
<p><strong>Autoevaluación del programa.</strong> En el mercado de valores, el oficial de cumplimiento debe realizar una autoevaluación anual del nivel de cumplimiento del programa, dirigida al consejo de administración a través del comité de cumplimiento. Debe cubrir, como mínimo, los pilares del programa y el ambiente de trabajo del oficial, las acciones disciplinarias impuestas por incumplimientos, el número de ROS presentados, la cantidad de empleados capacitados, los hallazgos del supervisor y de las auditorías y los resultados de la propia autoevaluación.[[6]]</p>
<h3>Cómo se arma la autoevaluación de la entidad</h3>
<ol class="steps">
<li><strong>Listar los eventos de riesgo</strong>: formas concretas en que cada producto, canal o tipo de cliente podría ser usado (por ejemplo, «pago de primas en efectivo por terceros»).</li>
<li><strong>Medir el riesgo inherente</strong> de cada evento por probabilidad e impacto, con una escala escrita.[[7]]</li>
<li><strong>Identificar y probar los controles</strong> que mitigan cada evento y calificar su eficacia real.</li>
<li><strong>Obtener el riesgo residual</strong> y compararlo con la tolerancia aprobada.[[7]]</li>
<li><strong>Definir planes de acción</strong> para los eventos que quedan fuera de tolerancia, con responsable y fecha.</li>
</ol>
""")},
# 2 ------------------------------------------------------------------------------------------
{"title": "Lo que piden las normas", "html": ess(
"Las normas no imponen una fórmula, pero sí piden que la matriz contenga ciertos datos y que deje claro qué tipo de debida diligencia corresponde a cada cliente. Un buen punto de partida es la lista del mercado de valores.") + """
<p>La norma del Consejo Nacional de Valores (art. 44) es la más detallada de la bibliografía. La matriz, que elabora el comité de cumplimiento, debe incluir como mínimo:[[6]]</p>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Grupo</th><th>Requisitos mínimos</th></tr></thead>
<tbody>
<tr><td>Identificación</td><td>Nombre y código del cliente; datos geográficos; tipo de cliente; tipo de negocio, ocupación y naturaleza del negocio; productos utilizados; duración de la relación.</td></tr>
<tr><td>Resultado</td><td>Calificación y categoría de riesgo; responsable de la preparación, fecha y hora; clasificación del riesgo tomando como herramienta las listas del Consejo de Seguridad de la ONU, la OFAC, entre otras.</td></tr>
<tr><td>Consecuencias</td><td>Tipo de debida diligencia a aplicar según los niveles de escalamiento; controles para gestionar el riesgo; intensidad del monitoreo para detectar operaciones sospechosas.</td></tr>
<tr><td>Insumos</td><td>Guías, tipologías y pautas de las autoridades, experiencia del mercado y estándares internacionales.</td></tr>
</tbody></table></div>
<p>Además, la matriz debe contar con un proceso que determine su operatividad y sus reglas, incluido cómo se usa al asignar el nivel de riesgo de cada cliente.[[6]]</p>
""" + deep("""
<p><strong>Cooperativas.</strong> La Norma 001-17 del IDECOOP pide que el manual defina la matriz de riesgo del asociado con estos componentes: tipo de asociados, definición de umbrales y factores de riesgo de productos y servicios, ubicaciones geográficas y canales de distribución.[[8]]</p>
<p><strong>Reportes que salen de la matriz.</strong> La DGII pide a sus sujetos obligados remitir cada trimestre información acumulada que incluye la categoría de riesgo de la entidad y el número de clientes en cada una, además de volumen y montos por categoría de cliente.[[5]] Una matriz bien construida permite generar ese reporte sin trabajo manual.</p>
<p>En el mercado de valores, el oficial de cumplimiento remite a la Superintendencia, dentro de los primeros 10 días hábiles de cada semestre, información tabulada que incluye la categoría de riesgo y el número de clientes en cada una, la cantidad de clientes de mayor riesgo con su nivel y las operaciones con clientes extranjeros.[[6]]</p>
""")},
# 3 ------------------------------------------------------------------------------------------
{"title": "Cómo se construye una matriz de clientes", "html": ess(
"Se eligen unas pocas características por cada factor, se les da un puntaje del 1 al 5 con reglas escritas, se decide cuánto pesa cada factor, se suma y se traduce el resultado a bajo, medio o alto. Algunas condiciones, como ser PEP, ponen al cliente en alto riesgo sin importar el puntaje.") + """
<ol class="steps">
<li><strong>Elegir variables por factor.</strong> Por ejemplo: actividad económica y condición de PEP (cliente); producto contratado (producto); país y provincia (geografía); canal de vinculación (canal). La norma de seguros sugiere evaluar actividad económica, volumen o frecuencia de transacciones, naturaleza del producto, ubicación y naturaleza de las transacciones y características del canal.[[7]]</li>
<li><strong>Definir una escala</strong> para cada variable, por ejemplo de 1 (bajo) a 5 (alto), con criterios escritos para asignar cada valor.</li>
<li><strong>Asignar ponderaciones</strong> que reflejen el peso relativo de cada factor según la realidad de la entidad, y justificarlas.</li>
<li><strong>Calcular el puntaje</strong> como promedio ponderado y traducirlo a niveles (bajo, medio, alto), como mínimo los tres que piden las normas.[[5]]</li>
<li><strong>Aplicar reglas de prevalencia</strong> para las condiciones que la norma fija como alto riesgo.</li>
<li><strong>Vincular cada nivel a medidas</strong>: tipo de debida diligencia, frecuencia de actualización y umbrales de monitoreo.</li>
</ol>
<div class="callout warn"><b>Reglas que prevalecen</b>La ley ordena tratar como factores de alto riesgo, como mínimo, a las PEP y a las operaciones con jurisdicciones definidas por el GAFI (art. 46).[[1]] La norma de seguros añade, entre otros, a las personas en listas restrictivas y al beneficiario final de seguros de vida y de retiro con componente de ahorro.[[7]] La matriz debe reflejarlo con reglas que fijen el nivel alto aunque el puntaje sea bajo.</div>
""" + deep("""
<p><strong>Coincidencias en listas de la ONU.</strong> Una coincidencia confirmada con las listas del Consejo de Seguridad no es solo un factor de riesgo: activa la obligación de congelar sin demora y de comunicarlo (Ley 155-17, arts. 82 y 83).[[1]] Por eso conviene que la matriz no «puntúe» ese caso, sino que lo saque del flujo normal y lo envíe al procedimiento de congelamiento.</p>
<p><strong>Escalas con criterios escritos.</strong> Una escala «1 a 5» sin criterios produce calificaciones distintas según quién las asigne. Escribe para cada valor qué condición lo activa (por ejemplo, actividades consideradas de alto riesgo en las tipologías de la UAF o en la evaluación nacional de riesgos).</p>
""")},
# 4 ------------------------------------------------------------------------------------------
{"title": "Ejemplo resuelto", "html": ess(
"Veamos un cálculo con números. Los valores son inventados para el ejercicio: cada entidad debe fijar y justificar los suyos.") + """
<p>Las cifras siguientes son <strong>ilustrativas</strong>.</p>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Factor</th><th>Variable del cliente</th><th>Valor (1-5)</th><th>Peso</th><th>Aporte</th></tr></thead>
<tbody>
<tr><td>Cliente</td><td>Comercio de vehículos usados, persona jurídica con 2 socios</td><td>4</td><td>40 %</td><td>1.60</td></tr>
<tr><td>Producto</td><td>Cuenta corriente con alto uso de efectivo</td><td>4</td><td>25 %</td><td>1.00</td></tr>
<tr><td>Geografía</td><td>Opera en una provincia fronteriza</td><td>3</td><td>20 %</td><td>0.60</td></tr>
<tr><td>Canal</td><td>Vinculación presencial</td><td>1</td><td>15 %</td><td>0.15</td></tr>
<tr><td colspan="4"><strong>Puntaje total</strong></td><td><strong>3.35</strong></td></tr>
</tbody></table></div>
<p>Si la política define <em>bajo</em> hasta 2.00, <em>medio</em> de 2.01 a 3.20 y <em>alto</em> desde 3.21, este cliente es de <strong>riesgo alto</strong>. Corresponde debida diligencia ampliada (art. 42 de la ley): identificar y verificar a los beneficiarios finales, documentar el origen de los fondos y actualizar su información con mayor frecuencia.[[1]]</p>
<h3>Segundo cliente: la regla de prevalencia</h3>
<p>Una asalariada con producto sencillo, residente en una provincia de riesgo bajo y vinculada en sucursal obtiene 1.45 puntos. Pero es regidora municipal: los regidores están entre los cargos PEP del Decreto 408-17, por lo que la regla de prevalencia la ubica en <strong>alto</strong>, con aprobación de la alta gerencia, origen de los fondos y monitoreo intensificado.[[10]]</p>
""" + deep("""
<p><strong>Sensibilidad.</strong> Prueba qué pasa si cambias un peso: con el canal al 25 % y el cliente al 30 %, el primer ejemplo da 3.05 y bajaría a medio. Si una variación pequeña de ponderación mueve a muchos clientes de nivel, la matriz es frágil y conviene revisar los umbrales o las escalas.</p>
<p><strong>Qué documentar.</strong> Para cada cliente: los valores asignados, los pesos vigentes, el puntaje, la regla de prevalencia aplicada si hubo, el nivel resultante, quién lo preparó y la fecha, tal como pide la norma del mercado de valores.[[6]]</p>
""")},
# 5 ------------------------------------------------------------------------------------------
{"title": "Segmentación: comparar con iguales", "html": ess(
"Una operación solo parece rara si sabemos qué es normal. Por eso se agrupa a los clientes parecidos —por actividad, ingresos o volumen— y se mira quién se sale del comportamiento de su grupo.") + """
<p>La <strong>segmentación</strong> agrupa a los clientes con características similares (actividad, ingresos, volumen transaccional, zona) para definir qué es «normal» en cada grupo y detectar desviaciones.[[3]] La norma de seguros exige segmentar los factores de riesgo con una metodología propia, como base de la etapa de identificación.[[7]]</p>
<ul>
<li><strong>Por reglas</strong>: segmentos definidos por criterios de negocio (por ejemplo, asalariados con ingresos hasta cierto monto).</li>
<li><strong>Estadística</strong>: percentiles o desviaciones respecto al promedio del segmento.</li>
<li><strong>Analítica avanzada</strong>: técnicas de agrupamiento que descubren segmentos a partir de los datos; requieren validación y explicación.</li>
</ul>
<div class="case"><b>Ejemplo</b><p>En el segmento «empleados privados con ingresos hasta RD$40,000», casi nadie recibe más de diez transferencias de terceros al mes. Un cliente de ese segmento que recibe sesenta merece revisión, aunque cada transferencia sea pequeña.</p></div>
<p>La ley exige que el monitoreo verifique que las transacciones sean consistentes con el conocimiento del cliente, su actividad y su perfil de riesgo (art. 39).[[1]] La segmentación da a ese «perfil» una referencia cuantitativa.</p>
""" + deep("""
<p><strong>Umbrales.</strong> El manual de las cooperativas debe definir umbrales tanto en la matriz del asociado como en el monitoreo de operaciones, junto con el tratamiento de los cambios de perfil.[[8]] Un umbral por segmento suele producir menos falsos positivos que un umbral único para toda la cartera.</p>
<p><strong>Explicabilidad.</strong> Si los segmentos se obtienen con técnicas de agrupamiento, la entidad debe poder explicar qué variables los definen y por qué un cliente quedó en uno; el curso 13 trata la gobernanza de esos modelos.</p>
""")},
# 6 ------------------------------------------------------------------------------------------
{"title": "Gobierno de la matriz", "html": ess(
"Una matriz no es un archivo que se hace una vez: alguien debe aprobarla, revisarla al menos cada año, comprobar que califica bien y poder explicar, años después, por qué un cliente recibió su nota.") + """
<ul>
<li><strong>Metodología escrita y aprobada</strong> por la instancia que corresponda, con la justificación de variables y ponderaciones.</li>
<li><strong>Revisión periódica</strong>: en el mercado de valores, al menos una vez al año, dejando constancia de la modificación y de su finalidad y conservando la matriz anterior.[[6]]</li>
<li><strong>Calibración</strong>: revisar si la distribución de clientes por nivel es razonable y si los niveles altos concentran las alertas relevantes.</li>
<li><strong>Pruebas retrospectivas</strong>: verificar si los clientes reportados o con hallazgos estaban bien calificados.</li>
<li><strong>Actualización</strong> ante nuevos productos, cambios normativos o tipologías, y recálculo cuando cambian los datos del cliente.[[1]]</li>
<li><strong>Trazabilidad</strong>: poder reconstruir por qué un cliente obtuvo su calificación en una fecha dada.[[4,6]]</li>
</ul>
""" + deep("""
<p><strong>Conservación.</strong> Los resultados de los análisis forman parte de los registros que deben conservarse al menos 10 años (art. 43).[[1]] Guardar las versiones anteriores de la matriz permite demostrar con qué criterio se calificó a un cliente en su momento.</p>
<p><strong>Mejora continua.</strong> ISO 31000 incluye el seguimiento, la revisión y el registro como parte del proceso de gestión del riesgo; la matriz es uno de esos registros.[[4]]</p>
""")},
# 7 ------------------------------------------------------------------------------------------
{"title": "Caso práctico", "html": ess(
"Una entidad descubre que su matriz no funciona. ¿Cómo lo nota y qué hace?") + """
<div class="case"><b>Caso · «Todos son de bajo riesgo»</b>
<p>Una casa de cambio revisa su matriz y encuentra que el 96 % de sus clientes está en riesgo bajo. Sin embargo, la mayoría de las alertas investigadas el último año, y los tres ROS enviados, corresponden a clientes de ese nivel.</p>
<ol>
<li><strong>Diagnóstico:</strong> la prueba retrospectiva muestra que la matriz no discrimina. Las variables de producto y canal tienen poco peso y no hay variable de volumen ni de frecuencia de operaciones.</li>
<li><strong>Ajuste:</strong> se incorpora el volumen y la frecuencia de transacciones, como sugiere la norma de seguros para el factor cliente, y se crean segmentos por tipo de cliente.[[7]]</li>
<li><strong>Reglas:</strong> se añade la prevalencia para PEP y jurisdicciones definidas por el GAFI, que faltaba.[[1]]</li>
<li><strong>Gobierno:</strong> la nueva versión se aprueba, se documenta el cambio y su finalidad y se conserva la anterior.[[6]]</li>
<li><strong>Efecto:</strong> los clientes que pasen a riesgo alto reciben debida diligencia ampliada y su información se actualiza.</li>
</ol>
<p class="verdict yes"><b>Lección:</b> una matriz se juzga por lo que detecta, no por lo ordenada que se ve.</p>
</div>
"""},
],
"glossary": [
("Matriz de riesgo de clientes", "Herramienta que clasifica a los clientes, como mínimo, en bajo, medio y alto riesgo para aplicar debida diligencia diferenciada [[5]]."),
("Autoevaluación de riesgos", "Evaluación de cómo podría la entidad ser utilizada para lavar activos y de la eficacia de sus controles."),
("Ponderación", "Peso relativo que se asigna a cada factor o variable en el cálculo del puntaje."),
("Regla de prevalencia", "Condición que fija un nivel de riesgo con independencia del puntaje, como la condición de PEP (art. 46) [[1]]."),
("Segmentación", "Agrupación de clientes o factores con características similares para definir lo esperado y detectar desviaciones [[3,7]]."),
("Calibración", "Ajuste de variables, pesos y umbrales a partir de evidencia de la propia entidad."),
("Prueba retrospectiva", "Verificación de si los clientes con hallazgos o reportes estaban bien calificados."),
("Trazabilidad", "Capacidad de reconstruir cómo y cuándo se obtuvo una calificación [[6]]."),
],
"quiz": [
{"q": "¿Para qué sirve principalmente la matriz de riesgo de clientes?", "options": ["Para calcular comisiones", "Para asignar a cada cliente un nivel de riesgo que determina su debida diligencia y monitoreo", "Para reemplazar la evaluación de la entidad", "Para decidir qué reportar a la UAF sin análisis"], "answer": 1, "explain": "La matriz clasifica a los clientes para aplicar una debida diligencia diferenciada [[5]]."},
{"q": "Según la Norma 01-2018 de la DGII, ¿en cuántos niveles como mínimo debe clasificar la matriz?", "options": ["Dos: aceptado y rechazado", "Tres: bajo, medio y alto", "Cinco", "No exige niveles"], "answer": 1, "explain": "La norma exige clasificar a los clientes como mínimo en bajo, medio y alto riesgo [[5]]."},
{"q": "En el mercado de valores, ¿quién elabora la matriz de riesgo?", "options": ["El cliente", "El comité de cumplimiento", "La UAF", "El auditor externo"], "answer": 1, "explain": "El art. 44 de la norma del CNV encarga al comité de cumplimiento elaborar la matriz [[6]]."},
{"q": "¿Cuál de estos datos NO figura entre los requisitos mínimos de la matriz del mercado de valores?", "options": ["Productos utilizados", "Duración de la relación comercial", "Tipo de debida diligencia a aplicar", "La religión del cliente"], "answer": 3, "explain": "La norma pide datos del cliente, productos, duración, calificación y tipo de debida diligencia, entre otros; no datos como la religión [[6]]."},
{"q": "En el ejemplo resuelto, ¿por qué el primer cliente resultó de riesgo alto?", "options": ["Porque usa el canal presencial", "Porque su puntaje ponderado (3.35) superó el umbral definido para alto (3.21)", "Porque es persona jurídica", "Porque todos los clientes con cuenta corriente son de alto riesgo"], "answer": 1, "explain": "El nivel se obtiene comparando el puntaje ponderado con los rangos definidos en la política."},
{"q": "Un cliente obtiene puntaje bajo, pero es PEP. ¿Qué nivel le corresponde?", "options": ["Bajo, porque manda el puntaje", "Alto, por la regla de prevalencia que refleja el art. 46", "Medio, como promedio", "No se califica"], "answer": 1, "explain": "La ley considera a las PEP factor de alto riesgo; la matriz debe incorporar esa regla [[1]]."},
{"q": "Una coincidencia confirmada con las listas del Consejo de Seguridad de la ONU debería:", "options": ["Sumar un punto al puntaje", "Activar el procedimiento de congelamiento sin demora", "Ignorarse si el cliente es antiguo", "Esperar a la revisión anual"], "answer": 1, "explain": "Los arts. 82 y 83 de la ley obligan a congelar sin demora y comunicar la coincidencia [[1]]."},
{"q": "¿Qué aporta la segmentación al monitoreo?", "options": ["Permite definir lo esperado en grupos similares y detectar desviaciones", "Reemplaza la debida diligencia", "Sirve solo para mercadeo", "Elimina las alertas"], "answer": 0, "explain": "Comparar a un cliente con sus pares permite identificar comportamientos fuera de lo normal [[3]]."},
{"q": "En el mercado de valores, al modificar la matriz se debe:", "options": ["Borrar la versión anterior", "Dejar constancia del cambio y su finalidad y conservar la matriz anterior", "Pedir permiso a cada cliente", "Esperar cinco años"], "answer": 1, "explain": "El art. 44 exige consignar la modificación y su finalidad y conservar siempre la matriz anterior [[6]]."},
{"q": "¿Qué es una prueba retrospectiva de la matriz?", "options": ["Repetir el cálculo con otra calculadora", "Verificar si los clientes con hallazgos o reportes estaban bien calificados", "Eliminar clientes antiguos", "Enviar la matriz al cliente"], "answer": 1, "explain": "La revisión retrospectiva ayuda a calibrar variables y ponderaciones con evidencia propia."},
{"q": "En el caso práctico, ¿qué indicaba que la matriz no funcionaba?", "options": ["Que tenía muchas columnas", "Que casi todos los clientes eran de bajo riesgo, pero las alertas y ROS se concentraban en ese nivel", "Que se actualizaba cada año", "Que usaba ponderaciones"], "answer": 1, "explain": "Si los casos relevantes aparecen en el nivel bajo, la matriz no discrimina y debe recalibrarse."},
],
}
