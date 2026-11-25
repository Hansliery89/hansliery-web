-- =====================================================================
-- HANSLIERY ACADEMY · 0007 · Datos iniciales
-- Cursos: generados desde cursos/_fuente/c01..c13 (no se copia el contenido;
-- cada curso apunta a su página pública). Se cargan en BORRADOR: el
-- administrador fija horas académicas, precio y publica.
-- =====================================================================
insert into public.academy_settings (key, value) values
  ('inactivity_days', '100'),
  ('inactivity_warning_days', '[70, 85, 95]'),
  ('anonymization_grace_days', '30'),
  ('terms_version', '"2026-11"'),
  ('award_weights', '{"calificaciones": 50, "finalizacion": 20, "evaluaciones": 15, "asignaciones": 10, "participacion": 5}'),
  ('award_min_grade', '85'),
  ('scholarships_per_period', '3'),
  ('scholarship_percentage', '50')
on conflict (key) do nothing;

insert into public.revenue_categories (code, name, grp) values
  ('capacitacion', 'Ingresos por capacitaciones', 'training'),
  ('software', 'Ingresos por venta de software', 'software'),
  ('evaluaciones', 'Ingresos por evaluaciones', 'evaluation'),
  ('otros', 'Otros ingresos', 'other')
on conflict (code) do nothing;

insert into public.revenue_categories (code, name, grp, parent_id)
select v.code, v.name, v.grp::public.revenue_group, (select id from public.revenue_categories where code = v.parent)
from (values
  ('cap_curso_gratuito','Cursos gratuitos','training','capacitacion'),
  ('cap_curso_pago','Cursos pagos','training','capacitacion'),
  ('cap_taller','Talleres especializados','training','capacitacion'),
  ('cap_corporativa','Capacitaciones corporativas','training','capacitacion'),
  ('cap_inscripcion','Inscripciones','training','capacitacion'),
  ('sw_cgp','Compliance Guard Pro','software','software'),
  ('sw_lexium','LEXIUM Legal Suite','software','software'),
  ('sw_medinovaq','MEDINOVAQ Salud','software','software'),
  ('ev_certificacion','Exámenes de certificación','evaluation','evaluaciones'),
  ('ev_especializada','Evaluaciones especializadas','evaluation','evaluaciones'),
  ('ev_independiente','Pruebas independientes de pago','evaluation','evaluaciones')
) as v(code, name, grp, parent)
on conflict (code) do nothing;

insert into public.courses (slug, title, summary, level, tag, duration_minutes, public_url) values
  ('fundamentos-prevencion-lavado-de-activos','Fundamentos de prevención de lavado de activos','Comprende qué es el lavado de activos, cómo se mueve el dinero ilícito, qué conductas castiga la Ley 155-17, en qué se diferencia del financiamiento del terrorismo y qué papel juega cada actor del sistema de prevención dominicano, incluido tú.','Básico → Profesional','Fundamentos',50,'https://hansliery89.github.io/hansliery-web/cursos/fundamentos-prevencion-lavado-de-activos.html'),
  ('marco-regulatorio-ley-155-17','Marco regulatorio dominicano y Ley 155-17','Recorre la arquitectura normativa dominicana contra el lavado de activos: qué dice la Ley 155-17 y sus reglamentos, quiénes son sujetos obligados, qué programa de cumplimiento deben tener, qué reportes y plazos aplican, cuáles son los límites al efectivo y qué consecuencias tiene incumplir.','Básico → Profesional','Regulación',55,'https://hansliery89.github.io/hansliery-web/cursos/marco-regulatorio-ley-155-17.html'),
  ('enfoque-basado-en-riesgos','Enfoque basado en riesgos','Aprende a aplicar el enfoque basado en riesgos: qué exige la ley, cómo se identifican amenazas y vulnerabilidades, cómo se mide el riesgo inherente, qué controles corresponden y cómo se monitorea el riesgo residual, con ejemplos de la normativa sectorial dominicana.','Intermedio → Profesional','Riesgos',50,'https://hansliery89.github.io/hansliery-web/cursos/enfoque-basado-en-riesgos.html'),
  ('matrices-de-evaluacion-y-segmentacion','Matrices de evaluación y segmentación','Diseña y aplica una matriz de riesgo de clientes: qué exigen las normas, qué variables elegir, cómo construir escalas y ponderaciones, cómo convertir el puntaje en niveles de riesgo y medidas de debida diligencia, y cómo segmentar y gobernar la matriz, con un ejemplo resuelto.','Intermedio → Profesional','Riesgos',55,'https://hansliery89.github.io/hansliery-web/cursos/matrices-de-evaluacion-y-segmentacion.html'),
  ('debida-diligencia-y-conocimiento-del-cliente','Debida diligencia y conocimiento del cliente','Domina el proceso de debida diligencia: cuándo es obligatoria, qué información obtener de personas físicas y jurídicas, cómo verificarla también en canales digitales, cuándo aplicar medidas simplificadas o ampliadas, qué hacer cuando el cliente no colabora y cómo mantener, conservar y delegar la información.','Básico → Profesional','Debida diligencia',55,'https://hansliery89.github.io/hansliery-web/cursos/debida-diligencia-y-conocimiento-del-cliente.html'),
  ('beneficiario-final','Beneficiario final','Aprende a identificar a la persona física que posee o controla realmente a un cliente: la definición legal y tributaria, el umbral del 20 %, el cálculo de la propiedad indirecta, la secuencia cuando no hay un propietario claro, los fideicomisos, la información mínima que debe obtenerse y las señales de estructuras diseñadas para ocultarla.','Intermedio → Profesional','Debida diligencia',50,'https://hansliery89.github.io/hansliery-web/cursos/beneficiario-final.html'),
  ('personas-expuestas-politicamente','Personas Expuestas Políticamente (PEP)','Identifica a las personas expuestas políticamente según la ley, el reglamento y el CONCLAFIT; extiende las medidas a familiares y asociados cercanos; aplica la debida diligencia ampliada que exige la normativa y distingue con claridad entre alto riesgo y operación sospechosa.','Intermedio → Profesional','Debida diligencia',50,'https://hansliery89.github.io/hansliery-web/cursos/personas-expuestas-politicamente.html'),
  ('reporteria-ros-ras-rte','Reportería: ROS, RAS y RTE','Aprende a decidir qué reportar a la UAF y cómo hacerlo bien: el Reporte de Transacciones en Efectivo, el Reporte de Operación Sospechosa y el Reporte de Actividad Sospechosa, el análisis previo, la redacción con el método de las 5W, la confidencialidad, el registro en goAML y ejemplos propios para seis sectores, aplicando el Código Penal vigente.','Intermedio → Profesional','Reportería',60,'https://hansliery89.github.io/hansliery-web/cursos/reporteria-ros-ras-rte.html'),
  ('senales-de-alerta-y-analisis-de-casos','Señales de alerta y análisis de casos','Aprende a reconocer señales de alerta de la normativa y de las subguías de la UAF, a convertirlas en decisiones fundamentadas mediante un método de análisis en cinco pasos y a documentar el resultado, incluida la decisión de no reportar, con casos resueltos de varios sectores.','Básico → Profesional','Tipologías',50,'https://hansliery89.github.io/hansliery-web/cursos/senales-de-alerta-y-analisis-de-casos.html'),
  ('activos-virtuales-y-riesgos-emergentes','Activos virtuales y riesgos emergentes','Entiende qué son los activos virtuales y sus proveedores de servicios, cómo funcionan las billeteras y la cadena de bloques, cuál es la situación en la República Dominicana, qué exigen las Recomendaciones 15 y 16 del GAFI, qué señales de alerta publicó el GAFI y cómo aplicar debida diligencia a clientes vinculados a criptoactivos.','Básico → Profesional','Riesgos emergentes',50,'https://hansliery89.github.io/hansliery-web/cursos/activos-virtuales-y-riesgos-emergentes.html'),
  ('fraude-digital-y-delitos-financieros-tecnologicos','Fraude digital y delitos financieros tecnológicos','Conoce las modalidades más comunes de fraude habilitado por la tecnología, el marco penal dominicano aplicable con el Código Penal vigente, el papel de las «mulas» de dinero, los controles antifraude en la vinculación digital y la verificación de documentos, y cómo responder desde cumplimiento.','Básico → Profesional','Riesgos emergentes',50,'https://hansliery89.github.io/hansliery-web/cursos/fraude-digital-y-delitos-financieros-tecnologicos.html'),
  ('automatizacion-de-procesos-de-cumplimiento','Automatización de procesos de cumplimiento','Descubre qué exige la normativa en materia de infraestructura tecnológica, qué procesos de cumplimiento conviene automatizar, qué herramientas accesibles existen y qué controles de calidad de datos, trazabilidad, protección de datos personales y confidencialidad deben acompañarlos, con una hoja de ruta medible.','Básico → Profesional','Tecnología',50,'https://hansliery89.github.io/hansliery-web/cursos/automatizacion-de-procesos-de-cumplimiento.html'),
  ('inteligencia-artificial-aplicada-a-plaft','Inteligencia artificial aplicada a PLAFT','Explora cómo la inteligencia artificial puede apoyar la prevención del lavado de activos, qué tipos de IA existen y para qué sirve cada uno, cuáles son sus riesgos y qué marco de gobierno —NIST AI RMF e ISO/IEC 42001— permite usarla de forma responsable, supervisada y compatible con la confidencialidad que exige la ley.','Intermedio → Profesional','Tecnología',50,'https://hansliery89.github.io/hansliery-web/cursos/inteligencia-artificial-aplicada-a-plaft.html')
on conflict (slug) do nothing;

insert into public.course_modules (course_id, position, title, anchor)
select c.id, v.pos, v.title, v.anchor
from (values
  ('fundamentos-prevencion-lavado-de-activos',1,'Dinero sucio que busca parecer limpio','modulo-1'),
  ('fundamentos-prevencion-lavado-de-activos',2,'Las tres etapas clásicas del proceso','modulo-2'),
  ('fundamentos-prevencion-lavado-de-activos',3,'Lo que castiga la ley','modulo-3'),
  ('fundamentos-prevencion-lavado-de-activos',4,'Financiamiento del terrorismo y de la proliferación','modulo-4'),
  ('fundamentos-prevencion-lavado-de-activos',5,'¿Por qué importa a todos?','modulo-5'),
  ('fundamentos-prevencion-lavado-de-activos',6,'Quién hace qué en el sistema dominicano','modulo-6'),
  ('fundamentos-prevencion-lavado-de-activos',7,'Tu papel en la primera línea','modulo-7'),
  ('marco-regulatorio-ley-155-17',1,'La arquitectura normativa','modulo-1'),
  ('marco-regulatorio-ley-155-17',2,'¿Quiénes están obligados?','modulo-2'),
  ('marco-regulatorio-ley-155-17',3,'El programa de cumplimiento','modulo-3'),
  ('marco-regulatorio-ley-155-17',4,'Las obligaciones del día a día','modulo-4'),
  ('marco-regulatorio-ley-155-17',5,'Límites al uso del efectivo (art. 64)','modulo-5'),
  ('marco-regulatorio-ley-155-17',6,'Infracciones y multas vigentes','modulo-6'),
  ('marco-regulatorio-ley-155-17',7,'Caso integrador','modulo-7'),
  ('enfoque-basado-en-riesgos',1,'Recursos limitados, riesgos distintos','modulo-1'),
  ('enfoque-basado-en-riesgos',2,'El vocabulario del riesgo','modulo-2'),
  ('enfoque-basado-en-riesgos',3,'Los cuatro factores mínimos','modulo-3'),
  ('enfoque-basado-en-riesgos',4,'Las etapas de la gestión del riesgo','modulo-4'),
  ('enfoque-basado-en-riesgos',5,'Del nivel de riesgo a la medida de control','modulo-5'),
  ('enfoque-basado-en-riesgos',6,'Errores que conviene evitar','modulo-6'),
  ('enfoque-basado-en-riesgos',7,'Caso práctico','modulo-7'),
  ('matrices-de-evaluacion-y-segmentacion',1,'Dos matrices, dos propósitos','modulo-1'),
  ('matrices-de-evaluacion-y-segmentacion',2,'Lo que piden las normas','modulo-2'),
  ('matrices-de-evaluacion-y-segmentacion',3,'Cómo se construye una matriz de clientes','modulo-3'),
  ('matrices-de-evaluacion-y-segmentacion',4,'Ejemplo resuelto','modulo-4'),
  ('matrices-de-evaluacion-y-segmentacion',5,'Segmentación: comparar con iguales','modulo-5'),
  ('matrices-de-evaluacion-y-segmentacion',6,'Gobierno de la matriz','modulo-6'),
  ('matrices-de-evaluacion-y-segmentacion',7,'Caso práctico','modulo-7'),
  ('debida-diligencia-y-conocimiento-del-cliente',1,'Conocer al cliente no es un formulario','modulo-1'),
  ('debida-diligencia-y-conocimiento-del-cliente',2,'¿Cuándo es obligatoria?','modulo-2'),
  ('debida-diligencia-y-conocimiento-del-cliente',3,'Qué información pedir','modulo-3'),
  ('debida-diligencia-y-conocimiento-del-cliente',4,'Tres intensidades de diligencia','modulo-4'),
  ('debida-diligencia-y-conocimiento-del-cliente',5,'Verificar a distancia: onboarding digital','modulo-5'),
  ('debida-diligencia-y-conocimiento-del-cliente',6,'Cuando el cliente no colabora','modulo-6'),
  ('debida-diligencia-y-conocimiento-del-cliente',7,'Actualizar, conservar y delegar','modulo-7'),
  ('beneficiario-final',1,'Siempre una persona física','modulo-1'),
  ('beneficiario-final',2,'Calcular la propiedad indirecta','modulo-2'),
  ('beneficiario-final',3,'La secuencia de identificación','modulo-3'),
  ('beneficiario-final',4,'Fideicomisos y entes sin personalidad jurídica','modulo-4'),
  ('beneficiario-final',5,'Información mínima, conservación y actualización','modulo-5'),
  ('beneficiario-final',6,'Señales de opacidad y testaferros','modulo-6'),
  ('beneficiario-final',7,'Caso integrador','modulo-7'),
  ('personas-expuestas-politicamente',1,'¿Quién es PEP?','modulo-1'),
  ('personas-expuestas-politicamente',2,'Los cargos del Decreto 408-17','modulo-2'),
  ('personas-expuestas-politicamente',3,'Funcionarios consulares honorarios','modulo-3'),
  ('personas-expuestas-politicamente',4,'El círculo cercano','modulo-4'),
  ('personas-expuestas-politicamente',5,'Medidas de debida diligencia ampliada','modulo-5'),
  ('personas-expuestas-politicamente',6,'Ser PEP no es una sospecha','modulo-6'),
  ('personas-expuestas-politicamente',7,'La condición en el tiempo','modulo-7'),
  ('reporteria-ros-ras-rte',1,'Tres reportes, tres lógicas','modulo-1'),
  ('reporteria-ros-ras-rte',2,'El Reporte de Transacciones en Efectivo (RTE)','modulo-2'),
  ('reporteria-ros-ras-rte',3,'El Reporte de Operación Sospechosa (ROS)','modulo-3'),
  ('reporteria-ros-ras-rte',4,'Redactar con el método de las 5W','modulo-4'),
  ('reporteria-ros-ras-rte',5,'Lo que, por sí solo, no justifica un ROS','modulo-5'),
  ('reporteria-ros-ras-rte',6,'El Reporte de Actividad Sospechosa (RAS)','modulo-6'),
  ('reporteria-ros-ras-rte',7,'Confidencialidad, protección y consecuencias','modulo-7'),
  ('reporteria-ros-ras-rte',8,'goAML en la práctica','modulo-8'),
  ('reporteria-ros-ras-rte',9,'Ejemplos por sector','modulo-9'),
  ('senales-de-alerta-y-analisis-de-casos',1,'Alerta no es sospecha','modulo-1'),
  ('senales-de-alerta-y-analisis-de-casos',2,'Señales en la normativa','modulo-2'),
  ('senales-de-alerta-y-analisis-de-casos',3,'Categorías de señales','modulo-3'),
  ('senales-de-alerta-y-analisis-de-casos',4,'Un método de análisis en cinco pasos','modulo-4'),
  ('senales-de-alerta-y-analisis-de-casos',5,'Casos para practicar','modulo-5'),
  ('senales-de-alerta-y-analisis-de-casos',6,'Casos de seguros y sector no financiero','modulo-6'),
  ('senales-de-alerta-y-analisis-de-casos',7,'Documentar también lo que no se reporta','modulo-7'),
  ('activos-virtuales-y-riesgos-emergentes',1,'Conceptos básicos','modulo-1'),
  ('activos-virtuales-y-riesgos-emergentes',2,'Billeteras y cadena de bloques','modulo-2'),
  ('activos-virtuales-y-riesgos-emergentes',3,'Situación en la República Dominicana','modulo-3'),
  ('activos-virtuales-y-riesgos-emergentes',4,'Lo que exige el GAFI','modulo-4'),
  ('activos-virtuales-y-riesgos-emergentes',5,'Señales de alerta','modulo-5'),
  ('activos-virtuales-y-riesgos-emergentes',6,'Debida diligencia en la práctica','modulo-6'),
  ('activos-virtuales-y-riesgos-emergentes',7,'Caso integrador','modulo-7'),
  ('fraude-digital-y-delitos-financieros-tecnologicos',1,'Un delito global y veloz','modulo-1'),
  ('fraude-digital-y-delitos-financieros-tecnologicos',2,'Marco penal dominicano','modulo-2'),
  ('fraude-digital-y-delitos-financieros-tecnologicos',3,'Las «mulas» de dinero','modulo-3'),
  ('fraude-digital-y-delitos-financieros-tecnologicos',4,'Controles en la vinculación digital','modulo-4'),
  ('fraude-digital-y-delitos-financieros-tecnologicos',5,'Documentos falsos y verificación digital','modulo-5'),
  ('fraude-digital-y-delitos-financieros-tecnologicos',6,'Respuesta desde cumplimiento','modulo-6'),
  ('fraude-digital-y-delitos-financieros-tecnologicos',7,'Casos integradores','modulo-7'),
  ('automatizacion-de-procesos-de-cumplimiento',1,'Por qué automatizar','modulo-1'),
  ('automatizacion-de-procesos-de-cumplimiento',2,'Lo que piden las normas','modulo-2'),
  ('automatizacion-de-procesos-de-cumplimiento',3,'Qué automatizar y qué no','modulo-3'),
  ('automatizacion-de-procesos-de-cumplimiento',4,'Herramientas accesibles','modulo-4'),
  ('automatizacion-de-procesos-de-cumplimiento',5,'Datos personales y confidencialidad','modulo-5'),
  ('automatizacion-de-procesos-de-cumplimiento',6,'Controles que no pueden faltar','modulo-6'),
  ('automatizacion-de-procesos-de-cumplimiento',7,'Hoja de ruta y caso','modulo-7'),
  ('inteligencia-artificial-aplicada-a-plaft',1,'Qué es (y qué no es) la IA en cumplimiento','modulo-1'),
  ('inteligencia-artificial-aplicada-a-plaft',2,'Casos de uso','modulo-2'),
  ('inteligencia-artificial-aplicada-a-plaft',3,'Riesgos que hay que gestionar','modulo-3'),
  ('inteligencia-artificial-aplicada-a-plaft',4,'Gobierno responsable: NIST AI RMF','modulo-4'),
  ('inteligencia-artificial-aplicada-a-plaft',5,'Gobierno responsable: ISO/IEC 42001 y pasos prácticos','modulo-5'),
  ('inteligencia-artificial-aplicada-a-plaft',6,'Uso responsable de la IA generativa','modulo-6'),
  ('inteligencia-artificial-aplicada-a-plaft',7,'Evaluar un caso de uso','modulo-7')
) as v(slug, pos, title, anchor)
join public.courses c on c.slug = v.slug
on conflict (course_id, position) do nothing;
