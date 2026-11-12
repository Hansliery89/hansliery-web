from base import *
D={}
K1="Servicio 01 · Consultoría y fortalecimiento PLAFT"
# ---------- 01 Informe de diagnóstico
b=kv([("Entidad",PH),("Tipo de sujeto obligado",PH),("Supervisor",PH),("Período evaluado",PH),("Fecha del informe",PH),("Versión","1.0")])
b+=h2("1","Resumen ejecutivo")
b+="<p>Síntesis para el consejo y la alta gerencia: estado general del programa de prevención de lavado de activos, financiamiento del terrorismo y de la proliferación de armas de destrucción masiva (LA/FT/FPADM), principales brechas y prioridades de corrección.</p>"
b+=tbl(["Calificación global","Componentes evaluados","Brechas de prioridad alta","Brechas de prioridad media / baja"],[[pill("Parcial")+" Requiere mejoras <span class=small>(ejemplo)</span>","9","3 <span class=small>(ejemplo)</span>","7 <span class=small>(ejemplo)</span>"]])
b+=h2("2","Alcance y marco de referencia")
b+=ul(["Ley 155-17 contra el Lavado de Activos y el Financiamiento del Terrorismo y su reglamento de aplicación.","Normativa e instructivos del supervisor sectorial y resoluciones aplicables del CONCLAFIT y de la UAF.","Recomendaciones del GAFI y buenas prácticas internacionales de gestión de riesgos.","Políticas, manuales y procedimientos internos vigentes de la entidad."])
b+=h2("3","Metodología")
b+=steps([("Levantamiento","Entrevistas con el oficial de cumplimiento, la gerencia y las áreas de negocio; revisión de políticas, manuales, actas e informes previos."),("Pruebas","Recorrido de procesos y revisión de una muestra de expedientes de clientes, alertas y reportes."),("Evaluación","Contraste de cada componente con la normativa y calificación según la escala siguiente."),("Validación","Presentación preliminar de hallazgos a la gerencia antes del informe final.")])
b+=tbl(["Calificación","Criterio"],[[pill("Implementado"),"El requisito está documentado, se aplica de forma consistente y existe evidencia."],[pill("Parcial"),"El requisito existe pero presenta debilidades de diseño, aplicación o evidencia."],[pill("No implementado"),"El requisito no está documentado o no se aplica en la práctica."]],widths=["30%",None])
b+=h2("4","Evaluación por componente")
rows=[["Gobierno y oficial de cumplimiento","Ley 155-17, art. 70 (infracciones)",pill("Parcial"),"Oficial designado; falta plan anual aprobado."],
["Evaluación de riesgos","Arts. 34 y 37",pill("Parcial"),"La autoevaluación no considera el factor canales."],
["Políticas y manual","Art. 34",pill("Parcial"),"Manual sin actualizar desde cambios normativos recientes."],
["Debida diligencia","Arts. 36 a 42",pill("Parcial"),"Beneficiario final no verificado en parte de la muestra."],
["Personas expuestas políticamente","Art. 46",pill("No implementado"),"No se identifica a familiares hasta el segundo grado."],
["Monitoreo y señales de alerta","Art. 39",pill("Parcial"),"Umbrales de alertas no calibrados."],
["Reportes a la UAF (ROS y RTE)","Ley 155-17 y art. 54",pill("Implementado"),"Reportes remitidos en plazo."],
["Capacitación","Normativa sectorial",pill("Parcial"),"Programa ejecutado; sin evaluación de aprendizaje."],
["Conservación de registros","Art. 43",pill("Implementado"),"Registros conservados por el plazo legal."]]
b+=tbl(["Componente","Referencia","Calificación (ejemplo)","Observación (ejemplo)"],rows,widths=["26%","20%","17%",None])
b+=h2("5","Formato de hallazgo")
b+='<div class="card"><h3>Hallazgo H-03 (ejemplo) · '+pill("Alta")+'</h3>'+tbl(["Elemento","Descripción"],[["Condición","En 4 de 10 expedientes PEP revisados no consta la identificación de familiares ni de colaboradores cercanos."],["Criterio","Ley 155-17, art. 46: las PEP se tratan como clientes de alto riesgo y la obligación alcanza a sus familiares hasta el segundo grado."],["Causa","El formulario de vinculación no incluye la sección correspondiente."],["Riesgo","Relaciones de alto riesgo gestionadas con diligencia estándar; posible observación del supervisor."],["Recomendación","Actualizar el formulario y la declaración PEP; revisar la cartera PEP vigente."],["Responsable y plazo",PH]],widths=["22%",None])+"</div>"
b+=h2("6","Conclusiones y próximos pasos")
b+=ul(["Validación del informe con la alta gerencia.","Aprobación del plan de acción con responsables y plazos.","Seguimiento periódico del avance y verificación del cierre de brechas."])
b+='<div class="sign"><div>Elaborado por</div><div>Revisado por</div><div>Aprobado por</div></div>'
D["informe-diagnostico"]=("Informe de diagnóstico",K1,"Evaluación estructurada del programa de cumplimiento frente a la normativa: alcance, metodología, calificación por componente, hallazgos y recomendaciones.",b,False)

# ---------- 02 Matriz de brechas
b=kv([("Entidad",PH),("Fecha de corte",PH),("Fuente","Informe de diagnóstico")])
b+=call("<b>Cómo leer esta matriz.</b> Cada fila relaciona un requisito con la situación encontrada, la brecha, su nivel de riesgo y la prioridad de atención. Las filas son ejemplos ilustrativos.")
rows=[["B-01","Evaluación de riesgos","Considerar como mínimo clientes, productos y servicios, canales y zona geográfica (art. 37)","La autoevaluación no incluye el factor canales","Factor omitido en la medición",pill("Alto"),pill("Alta"),"Incorporar el factor y recalcular la matriz"],
["B-02","PEP","Tratar a las PEP como alto riesgo e identificar familiares hasta el 2.º grado (art. 46)","Formulario sin sección de familiares","Identificación incompleta",pill("Alto"),pill("Alta"),"Actualizar formulario y revisar cartera PEP"],
["B-03","Beneficiario final","Verificar razón social, RNC, forma jurídica, dirección y beneficiario final (art. 40)","Estructura de propiedad sin documentar en parte de la muestra","Verificación parcial",pill("Alto"),pill("Alta"),"Solicitar organigrama de propiedad y evidencias"],
["B-04","Monitoreo","Monitorear permanentemente la relación (art. 39)","Alertas con umbrales genéricos","Alto volumen de falsos positivos",pill("Medio"),pill("Media"),"Calibrar umbrales por segmento"],
["B-05","Manual","Programa basado en riesgos (art. 34)","Manual desactualizado","Procedimientos no reflejan normativa vigente",pill("Medio"),pill("Media"),"Actualizar y aprobar el manual"],
["B-06","Capacitación","Programa de capacitación según normativa sectorial","Sin evaluaciones de aprendizaje","No se mide la eficacia",pill("Bajo"),pill("Baja"),"Incluir pruebas de entrada y salida"],
["B-07","Registros","Conservar registros al menos 10 años (art. 43)","Digitalización incompleta de expedientes antiguos","Riesgo de pérdida de evidencia",pill("Medio"),pill("Media"),"Plan de digitalización y respaldo"],
["B-08","Debida diligencia simplificada","No aplicar diligencia simplificada si hay sospecha (art. 42)","Criterio no documentado en el manual","Aplicación discrecional",pill("Medio"),pill("Media"),"Documentar criterios y excepciones"]]
b+=tbl(["ID","Componente","Requisito / referencia","Situación actual","Brecha","Riesgo","Prioridad","Acción recomendada"],rows,widths=["5%","11%","21%","17%","14%","8%","8%",None])
b+=h2("","Convención de prioridad sugerida")
b+=tbl(["Prioridad","Criterio","Horizonte sugerido"],[[pill("Alta"),"Incumplimiento directo de una obligación legal o riesgo alto de observación del supervisor","0 a 3 meses"],[pill("Media"),"Debilidad de diseño o aplicación con impacto moderado","3 a 6 meses"],[pill("Baja"),"Oportunidad de mejora o buena práctica","6 a 12 meses"]],widths=["14%",None,"20%"])
D["matriz-brechas"]=("Matriz de brechas",K1,"Relación de cada requisito normativo con la situación encontrada, la brecha, el nivel de riesgo y la prioridad de atención.",b,True)

# ---------- 03 Plan de acción
b=kv([("Entidad",PH),("Aprobado por",PH),("Fecha de aprobación",PH)])
M=["E","F","M","A","M","J","J","A","S","O","N","D"]
def g(a,z,c=""): return [f'<span class="{c}"></span>' if a<=i<=z else "" for i in range(12)]
rows=[["A-01","B-01","Incorporar el factor canales y recalcular la matriz de riesgo","Oficial de cumplimiento","Matriz aprobada"]+g(0,1),
["A-02","B-02","Actualizar formulario y declaración PEP; revisar cartera","Cumplimiento / Negocios","100 % cartera PEP revisada"]+g(0,2),
["A-03","B-03","Completar documentación de beneficiario final","Operaciones","% expedientes completos"]+g(1,4,"o"),
["A-04","B-04","Calibrar umbrales de alertas por segmento","Cumplimiento / TI","Reducción de falsos positivos"]+g(2,5,"o"),
["A-05","B-05","Actualizar y aprobar el manual de prevención","Oficial de cumplimiento","Acta de aprobación"]+g(3,6,"o"),
["A-06","B-07","Digitalizar y respaldar expedientes antiguos","Operaciones / TI","% expedientes digitalizados"]+g(4,10,"d"),
["A-07","B-06","Incluir evaluaciones en el programa de capacitación","Talento humano / Cumplimiento","Resultados por actividad"]+g(6,11,"d")]
b+=tbl(["ID","Brecha","Acción","Responsable","Indicador"]+M,rows,"gantt",widths=["4%","5%","24%","13%","13%"]+["3.4%"]*12)
b+='<p class="small">Barras: <span class="pill p1">prioridad alta</span> <span class="pill p2">prioridad media</span> <span class="pill p3">prioridad baja</span> · cronograma ilustrativo.</p>'
b+=h2("","Seguimiento")
b+=tbl(["ID","Avance","Estado","Evidencia de cierre","Comentarios"],[["A-01","100 %",pill("Cerrada"),"Matriz y acta de aprobación",""],["A-02","60 %",pill("En curso"),"Formulario actualizado; revisión en proceso",""],["A-03","0 %",pill("Pendiente"),PH,""]],widths=["8%","10%","14%","34%",None])
b+=call("<b>Buenas prácticas de seguimiento:</b> informar el avance al comité de cumplimiento y a la alta gerencia con la periodicidad acordada, cerrar cada acción solo con evidencia verificable y registrar las reprogramaciones con su justificación.","gold")
D["plan-accion"]=("Plan de acción",K1,"Acciones para cerrar las brechas, con responsables, plazos, indicadores, cronograma y control de seguimiento.",b,True)

# ---------- 04 Manual y procedimientos
b=kv([("Código","MAN-PLAFT-01"),("Versión",PH),("Aprobación",PH+" (consejo de administración)")])
b+=h2("1","Estructura modelo del manual de prevención LA/FT/FPADM")
caps=[("Disposiciones generales","Objetivo, alcance, base legal, definiciones y vigencia."),("Gobierno del programa","Funciones del consejo, la alta gerencia, el comité y el oficial de cumplimiento."),("Enfoque basado en riesgos","Metodología de autoevaluación y matriz de riesgo; factores mínimos del art. 37."),("Aceptación de clientes","Criterios de aceptación, rechazo y relaciones prohibidas."),("Debida diligencia","Niveles simplificado, estándar y ampliado; personas físicas y jurídicas; beneficiario final."),("Personas expuestas políticamente","Identificación, aprobación, origen de fondos y monitoreo reforzado (art. 46)."),("Listas y sanciones","Procedimiento de screening y medidas ante coincidencias."),("Monitoreo y señales de alerta","Perfil transaccional, alertas, análisis y documentación."),("Reportes a la UAF","ROS, RTE y otros reportes; plazos, responsables y confidencialidad (art. 63)."),("Conservación de registros","Plazo mínimo de 10 años y forma de archivo (art. 43)."),("Capacitación","Programa anual por audiencias y evidencias."),("Selección y conducta del personal","Conozca a su empleado, código de ética y régimen disciplinario."),("Revisión independiente","Auditoría interna o externa del programa."),("Anexos","Formularios, checklists, matriz de riesgo y glosario.")]
b+=tbl(["Cap.","Contenido","Descripción"],[[f"{i+1:02d}",f"<b>{a}</b>",c] for i,(a,c) in enumerate(caps)],widths=["7%","28%",None])
b+=h2("2","Procedimientos asociados")
b+=tbl(["Código","Procedimiento","Responsable"],[["PR-01","Vinculación y debida diligencia de clientes","Negocios / Operaciones"],["PR-02","Identificación de beneficiario final","Operaciones"],["PR-03","Gestión de PEP","Cumplimiento"],["PR-04","Screening en listas","Cumplimiento"],["PR-05","Gestión de alertas","Cumplimiento"],["PR-06","Elaboración y remisión de reportes","Oficial de cumplimiento"],["PR-07","Actualización periódica de expedientes","Operaciones"]],widths=["12%",None,"30%"])
b+=h2("3","Control de versiones")
b+=tbl(["Versión","Fecha","Descripción del cambio","Aprobado por"],[["1.0",PH,"Emisión inicial",PH],["1.1",PH,"Actualización por cambios normativos",PH],["",PH,"",""]],widths=["10%","15%",None,"22%"])
D["manual-procedimientos"]=("Manual y procedimientos actualizados",K1,"Estructura modelo del manual de prevención, procedimientos asociados y control de versiones.",b,False)
