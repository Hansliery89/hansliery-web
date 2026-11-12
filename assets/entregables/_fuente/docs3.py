from base import *
D={}
K3="Servicio 03 · Controles internos y gobierno de cumplimiento"
K4="Servicio 04 · Capacitación profesional"
# ---------- 09 Matriz de controles
rows=[["C-01","Vinculación de clientes sin identificar al beneficiario final","Validación obligatoria del anexo de beneficiario final antes de activar la cuenta","Preventivo","Automático","Cada vinculación","Operaciones","Registro del sistema y anexo firmado","Muestra de expedientes nuevos"],
["C-02","Relación con persona sancionada","Screening en listas antes de la vinculación y rescreening al actualizarse las listas","Preventivo","Automático","Continuo","Cumplimiento","Constancia de consulta","Reejecución sobre muestra"],
["C-03","PEP gestionada como cliente estándar","Aprobación de la alta gerencia para relaciones con PEP","Preventivo","Manual","Cada caso","Alta gerencia","Formulario de aprobación","Revisión de la cartera PEP"],
["C-04","Operaciones inusuales no detectadas","Alertas por desviación del perfil transaccional","Detectivo","Automático","Diario","Cumplimiento","Bitácora de alertas","Prueba de escenarios"],
["C-05","Alertas sin análisis oportuno","Seguimiento de antigüedad de alertas con escalamiento","Detectivo","Manual","Semanal","Oficial de cumplimiento","Reporte de antigüedad","Comparación con plazos"],
["C-06","RTE fuera de plazo","Conciliación mensual de operaciones en efectivo sobre el umbral","Detectivo","Semiautomático","Mensual","Cumplimiento","Conciliación firmada","Verificar fecha de remisión"],
["C-07","Expedientes desactualizados","Calendario de actualización según nivel de riesgo","Preventivo","Semiautomático","Mensual","Operaciones","Reporte de vencimientos","Muestra de expedientes"],
["C-08","Personal sin capacitación","Control de asistencia y evaluación por actividad","Preventivo","Manual","Por actividad","Talento humano","Registro y evaluaciones","Conciliación con nómina"]]
b=tbl(["ID","Riesgo","Control","Tipo","Naturaleza","Frecuencia","Responsable","Evidencia","Prueba sugerida"],rows,widths=["5%","16%","20%","8%","9%","8%","10%","12%",None])
b+=h2("","Calificación del control y efectividad (convención sugerida)")
b+=tbl(["Calificación","Diseño","Eficacia operativa","Efectividad para la matriz"],[[pill("Fuerte"),"Cubre el riesgo, está documentado y tiene responsable","Probado sin excepciones relevantes","25 % – 30 %"],[pill("Moderado"),"Cubre el riesgo parcialmente o con documentación incompleta","Excepciones puntuales","15 % – 20 %"],[pill("Débil"),"Diseño insuficiente o no documentado","Excepciones frecuentes o sin evidencia","5 % – 10 %"]],widths=["14%",None,None,"20%"])
b+='<p class="small">El rango de efectividad es consistente con los valores de referencia de la matriz de riesgo (5 % a 30 %) y debe validarse con pruebas.</p>'
D["matriz-controles"]=("Matriz de controles",K3,"Controles preventivos y detectivos vinculados a cada riesgo, con responsable, frecuencia, evidencia y prueba sugerida.",b,True)

# ---------- 10 RACI
roles=["Consejo","Alta gerencia","Comité de cumplimiento","Oficial de cumplimiento","Áreas de negocio","Operaciones / TI","Talento humano","Auditoría interna"]
acts=[("Aprobar el manual y las políticas de prevención","A C C R I I I I"),("Designar al oficial de cumplimiento","A R I I I I I I"),("Aprobar la autoevaluación de riesgos","A C C R C C I I"),("Mantener la matriz de riesgo","I I C A C R I I"),("Debida diligencia en la vinculación","I I I C R/A C I I"),("Aprobar relaciones con PEP","I A C R C I I I"),("Screening en listas","I I I A C R I I"),("Análisis de alertas","I I I A C C I I"),("Remitir ROS y RTE a la UAF","I I I R/A C C I I"),("Conservación de registros","I I I A R R I I"),("Programa anual de capacitación","I A C R I I R I"),("Informe periódico de cumplimiento","I I C R/A I I I I"),("Seguimiento del plan de acción","I A R R R R I C"),("Revisión independiente del programa","I I I C I I I R/A")]
def cell(x):
    col={"R":"p1","A":"p4","C":"p2","I":"p3"}
    return " ".join(f'<span class="pill {col[c[0]]}">{c}</span>' for c in [x]) if x!="R/A" else '<span class="pill p1">R</span> <span class="pill p4">A</span>'
b=tbl(["Actividad"]+roles,[[a]+[cell(x) for x in s.split()] for a,s in acts],widths=["22%"]+["9.75%"]*8)
b+='<div class="cols"><div>'+tbl(["Letra","Significado"],[[cell("R"),"Responsable: ejecuta la actividad"],[cell("A"),"Aprueba y rinde cuentas (uno por actividad)"],[cell("C"),"Consultado antes de decidir"],[cell("I"),"Informado del resultado"]],widths=["18%",None])+'</div><div>'+call("<b>Notas.</b> La asignación es un ejemplo y depende de la estructura de cada entidad. Conviene evitar que quien ejecuta un control sea quien lo evalúa: la auditoría interna conserva su independencia respecto de la operación del programa.")+'</div></div>'
D["matriz-responsabilidades"]=("Matriz de responsabilidades (RACI)",K3,"Quién ejecuta, aprueba, es consultado o es informado en cada actividad del programa de prevención.",b,True)

# ---------- 11 Tablero de indicadores
b='<div class="tiles"><div><span>Expedientes completos</span><b>92 %</b><i style="background:#2563EB"></i></div><div><span>Alertas atendidas en plazo</span><b>81 %</b><i style="background:#FACC15"></i></div><div><span>Personal capacitado</span><b>96 %</b><i style="background:#2563EB"></i></div><div><span>Acciones del plan cerradas</span><b>58 %</b><i style="background:#FB923C"></i></div></div>'
b+=h2("1","Indicadores de gestión (KPI)")+'<p class="small">Tarjetas con valores ilustrativos. Semáforo: verde dentro de la meta, amarillo en tolerancia, naranja fuera de umbral.</p>'
b+=tbl(["Indicador","Fórmula","Meta","Umbral","Frecuencia","Fuente"],[["Expedientes completos","Expedientes completos / expedientes revisados","≥ 95 %","< 90 %","Mensual","Muestreo"],["Expedientes actualizados en plazo","Actualizados en plazo / con vencimiento","≥ 95 %","< 85 %","Mensual","Sistema"],["Alertas atendidas en plazo","Alertas cerradas en plazo / alertas generadas","≥ 90 %","< 80 %","Mensual","Bitácora"],["ROS remitidos en plazo","ROS dentro de 5 días hábiles / ROS remitidos","100 %","< 100 %","Mensual","Registro de reportes"],["RTE remitidos en plazo","RTE dentro de los 10 primeros días del mes siguiente / RTE","100 %","< 100 %","Mensual","Registro de reportes"],["Personal capacitado","Capacitados / personal que requiere capacitación","≥ 95 %","< 90 %","Trimestral","Talento humano"],["Acciones cerradas en plazo","Cerradas en plazo / programadas","≥ 90 %","< 75 %","Trimestral","Plan de acción"]],widths=["20%","30%","8%","8%","10%",None])
b+=h2("2","Indicadores de riesgo (KRI)")
b+=tbl(["Indicador","Lectura","Frecuencia"],[["Clientes de riesgo alto y muy alto / cartera","Cambios relevantes en la exposición de la cartera","Trimestral"],["Coincidencias potenciales pendientes","Acumulación de casos sin resolver en screening","Semanal"],["Alertas con más de 30 días","Retrasos en el análisis","Mensual"],["Operaciones con jurisdicciones de alto riesgo","Exposición geográfica","Mensual"]],widths=["40%",None,"14%"])
b+=call("Los indicadores sobre reportes a la UAF se presentan solo de forma agregada, para preservar la confidencialidad exigida por la ley (art. 63).","gold")
D["tablero-indicadores"]=("Tablero de indicadores",K3,"Indicadores de gestión y de riesgo con fórmula, meta, umbral, frecuencia y fuente, y propuesta de visualización.",b,False)

# ---------- 12 Informe gerencial
b=kv([("Dirigido a","Consejo de administración / alta gerencia"),("Período",PH),("Elaborado por","Oficial de cumplimiento")])
secs=[("Resumen del período","Hechos relevantes, cumplimiento general del programa y temas que requieren decisión."),("Perfil de riesgo de la cartera","Distribución de clientes por categoría de riesgo y variación respecto del período anterior."),("Indicadores","Tablero de KPI y KRI con semáforo y explicación de desviaciones."),("Monitoreo y reportes","Alertas generadas, analizadas y pendientes; cantidad de ROS y RTE remitidos en forma agregada."),("Debida diligencia y screening","Expedientes actualizados, relaciones PEP aprobadas y coincidencias gestionadas."),("Capacitación","Actividades ejecutadas, cobertura y resultados de evaluación."),("Plan de acción","Estado de las acciones, vencidas y reprogramadas."),("Cambios normativos","Nuevas disposiciones y su impacto en la entidad."),("Temas para decisión","Asuntos que requieren aprobación o recursos.")]
b+="".join(f'<div class="card"><h3>{i+1}. {a}</h3><p class="small">{c}</p><div class="fld"><div class="w">{PH}</div></div></div>' for i,(a,c) in enumerate(secs))
b+='<div class="sign"><div>Oficial de cumplimiento</div><div>Recibido por</div><div>Fecha</div></div>'
D["informe-gerencial"]=("Plantilla de informe gerencial",K3,"Estructura del informe periódico de cumplimiento para el consejo y la alta gerencia.",b,False)

# ---------- 13 Plan de capacitación
b=kv([("Entidad",PH),("Año",PH),("Aprobado por",PH)])
b+=h2("1","Programa por audiencia")
b+=tbl(["Audiencia","Temas","Modalidad","Duración","Período","Evaluación"],[["Consejo y alta gerencia","Responsabilidades, gobierno del riesgo, régimen sancionador y riesgo reputacional","Presencial","2 h","T1","Caso de discusión"],["Oficial y equipo de cumplimiento","Actualización normativa, tipologías, reportería, beneficiario final y matriz de riesgo","Mixta","16 h","T1–T4","Prueba y caso práctico"],["Primera línea (atención y ventas)","Debida diligencia, señales de alerta, PEP y confidencialidad","Virtual / presencial","4 h","T2","Prueba de salida"],["Operaciones y TI","Expedientes, conservación de registros, screening y calidad de datos","Presencial","3 h","T2","Prueba de salida"],["Personal de nuevo ingreso","Inducción al programa de prevención","Virtual","2 h","Al ingresar","Prueba de salida"],["Auditoría interna","Evaluación del programa basado en riesgos","Presencial","4 h","T3","Caso práctico"]],widths=["18%","34%","11%","8%","10%",None])
b+='<p class="small">Duraciones y períodos ilustrativos; se ajustan al tamaño de la entidad, a su normativa sectorial y a los resultados de la evaluación de riesgos.</p>'
b+=h2("2","Criterios del programa")
b+=ul(["Contenidos alineados con los riesgos identificados en la autoevaluación y con los hallazgos de supervisión y auditoría.","Casos prácticos del sector de la entidad.","Evaluación de entrada y de salida con una nota mínima de aprobación definida.","Reprogramación y refuerzo para quienes no aprueben.","Evidencias completas para auditoría y supervisión (ver registro de evidencias)."])
b+=h2("3","Indicadores del programa")
b+=tbl(["Indicador","Meta sugerida"],[["Cobertura del personal objetivo","≥ 95 %"],["Promedio de la evaluación de salida","≥ 80 %"],["Actividades ejecutadas según el plan","≥ 90 %"]],widths=[None,"22%"])
D["plan-capacitacion"]=("Plan de capacitación",K4,"Programa anual por audiencia con temas, modalidad, duración, período, evaluación e indicadores.",b,False)
