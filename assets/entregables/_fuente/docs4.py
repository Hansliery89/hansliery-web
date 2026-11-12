from base import *
D={}
K4="Servicio 04 · Capacitación profesional"
# ---------- 14 Material y casos prácticos
b=call("Muestra del formato de los casos que se trabajan en los talleres. Los casos son hipotéticos: personas, montos y hechos son ficticios.","blue")
b+=h2("1","Caso: pagos fraccionados en un concesionario de vehículos")
b+='<div class="card"><h3>Hechos</h3><p>Un cliente compra un vehículo usado. En la misma mañana realiza tres pagos en efectivo en distintas cajas: US$6,000, US$5,500 y US$4,800 (o su equivalente en pesos). Pregunta en voz alta si «por debajo de quince mil no hay que llenar nada» y pide que la factura salga a nombre de una sociedad recién constituida de la que no aporta documentos. Cuando se le solicita identificación del representante, se niega y se retira con la promesa de volver.</p></div>'
b+="<h3>Señales de alerta</h3>"+ul(["Fraccionamiento de efectivo en un mismo día.","Interés en conocer los umbrales de reporte.","Uso de una sociedad sin información de beneficiario final.","Negativa a aportar información de identificación."])
b+="<h3>Preguntas para el grupo</h3>"+ol(["¿Corresponde un reporte de transacciones en efectivo (RTE)? ¿Por qué?","¿Qué implica la negativa a identificarse?","¿Qué información falta sobre la sociedad?","¿Qué no debe decirle el personal al cliente?"])
b+='<div class="card" style="background:#F4F8FB"><h3>Guía de respuesta para el facilitador</h3>'+ol(["Sí. Las operaciones en efectivo de un mismo cliente dentro de 24 horas se agregan (art. 54); el total (US$16,300) supera el umbral de US$15,000.","La negativa a proporcionar información de identificación es motivo de reporte de operación sospechosa (art. 62), que se remite en el plazo legal de cinco días hábiles.","Razón social, RNC, forma jurídica, dirección y beneficiario final (art. 40).","No se debe advertir al cliente que se reportará ni que se ha reportado (art. 63)."])+"</div>"
b+='<h2 class="pb"><b>2</b>Caso: rescate anticipado de un seguro de vida</h2>'
b+='<div class="card"><h3>Hechos</h3><p>Una persona contrata un seguro de vida con valor de rescate mediante una prima única elevada, pagada con una transferencia desde la cuenta de un tercero sin relación aparente. A los cuatro meses solicita el rescate total, acepta la penalidad sin objeciones y pide que el dinero se transfiera a una cuenta en otro país.</p></div>'
b+="<h3>Señales de alerta</h3>"+ul(["Pago de la prima por un tercero sin vínculo justificado.","Rescate anticipado con aceptación de pérdidas.","Destino de los fondos distinto del origen y en el exterior.","Prima incoherente con el perfil económico declarado."])
b+="<h3>Preguntas para el grupo</h3>"+ol(["¿Qué información adicional pedirías antes de procesar el rescate?","¿Cómo influye la jurisdicción de destino en el riesgo?","¿Qué documentarías en el expediente?","¿Cuándo se escala al oficial de cumplimiento?"])
b+='<div class="card" style="background:#F4F8FB"><h3>Guía de respuesta para el facilitador</h3>'+ol(["Relación con el tercero pagador, origen de los fondos, motivo del rescate y titularidad de la cuenta de destino.","Se consulta el catálogo de jurisdicciones de la matriz; un destino de alto riesgo eleva el puntaje y la diligencia requerida.","Solicitudes, respuestas, verificaciones, screening y la decisión con su justificación.","De inmediato ante señales de alerta que no se puedan explicar con la información del cliente."])+"</div>"
b+=h2("3","Estructura de cada caso en los talleres")
b+=tbl(["Elemento","Propósito"],[["Hechos","Situación realista del sector del participante."],["Señales de alerta","Entrenar la detección."],["Preguntas","Aplicar la norma y el procedimiento interno."],["Guía de respuesta","Respuesta fundamentada con la referencia legal."]],widths=["24%",None])
D["material-casos"]=("Material y casos prácticos",K4,"Muestra del formato de casos de taller: hechos, señales de alerta, preguntas y guía de respuesta con referencias legales.",b,False)

# ---------- 15 Evaluaciones y resultados
Q=[("¿Durante cuánto tiempo, como mínimo, deben conservarse los registros de debida diligencia y de las transacciones?",["5 años","10 años después de terminada la relación o la transacción","Mientras dure la relación","2 años"],1,"Art. 43"),
("¿Hasta qué grado de parentesco alcanza la ley a los familiares de una PEP?",["Primer grado","Segundo grado","Tercer grado","No alcanza a familiares"],1,"Art. 46"),
("¿Cuándo no es aceptable aplicar debida diligencia simplificada?",["Cuando el cliente es nuevo","Cuando existe sospecha de LA/FT","Cuando el producto es de bajo monto","Nunca es aceptable"],1,"Art. 42"),
("Un cliente realiza tres depósitos en efectivo en un mismo día que suman más de US$15,000. ¿Qué corresponde?",["Nada, ninguno supera el umbral","Agregarlos y reportar el RTE","Solo un ROS","Devolver el dinero"],1,"Art. 54"),
("¿Cuáles son los factores de riesgo mínimos que exige la ley?",["Clientes, productos y servicios, canales y zona geográfica","Solo clientes","Clientes y transacciones","Productos y precios"],0,"Art. 37"),
("¿A quiénes se aplica la debida diligencia?",["Solo a clientes nuevos","A clientes actuales y potenciales","Solo a personas jurídicas","Solo a clientes de alto riesgo"],1,"Art. 38"),
("¿Qué debe hacer el personal ante un cliente que pregunta si será reportado?",["Confirmarle que sí","No revelar la existencia de un reporte","Pedirle que firme una autorización","Cancelar su cuenta de inmediato"],1,"Art. 63"),
("¿Qué datos de una persona jurídica deben verificarse, entre otros?",["Solo el nombre comercial","Razón social, RNC, forma jurídica, dirección y beneficiario final","Solo el representante legal","Los estados financieros auditados"],1,"Art. 40")]
b=fld(["Nombre","Área","Fecha","Tipo de prueba:  Entrada ☐   Salida ☐"])
b+=h2("1","Prueba de conocimientos (muestra)")
for i,(q,o,a,r) in enumerate(Q):
    b+=f'<div style="break-inside:avoid;margin-bottom:7px"><b>{i+1}. {q}</b>'+'<ul class="chk">'+"".join(f"<li>{chr(97+j)}) {x}</li>" for j,x in enumerate(o))+"</ul></div>"
b+='<h2 class="pb"><b>2</b>Clave de respuestas</h2>'
b+=tbl(["Pregunta","Respuesta","Fundamento (Ley 155-17)"],[[str(i+1),chr(97+a)+") "+o[a],r] for i,(q,o,a,r) in enumerate(Q)],widths=["12%",None,"24%"])
b+=h2("3","Informe de resultados")
b+=kv([("Actividad",PH),("Participantes",PH),("Nota mínima de aprobación",PH)])
b+=tbl(["Medida","Prueba de entrada","Prueba de salida","Variación"],[["Promedio",PH,PH,PH],["% de aprobados",PH,PH,PH],["Nota mínima / máxima",PH,PH,""]],widths=["28%",None,None,None])
b+=tbl(["Pregunta o tema con menor acierto","% de acierto","Acción de refuerzo"],[[PH,PH,PH]]*3,widths=[None,"16%","34%"])
b+='<p class="small">Las preguntas son una muestra; cada evaluación se elabora según los contenidos y la audiencia de la actividad.</p>'
D["evaluaciones-resultados"]=("Evaluaciones y resultados",K4,"Prueba de conocimientos de muestra con clave fundamentada en la Ley 155-17 e informe de resultados de entrada y salida.",b,False)

# ---------- 16 Registro de evidencias
b=h2("1","Ficha de la actividad")
b+=fld(["Nombre de la actividad","Código","Fecha","Horario","Modalidad","Duración (horas)","Facilitador","Audiencia","!Objetivos","!Temas tratados"])
b+=h2("2","Lista de asistencia")
b+=tbl(["#","Nombre completo","Cargo","Área","Firma o registro de conexión"],[[str(i),"","","",""] for i in range(1,13)],widths=["5%","32%","20%","18%",None])
b+='<p class="small">En actividades virtuales, se anexa el reporte de asistencia de la plataforma con hora de entrada y salida.</p>'
b+=h2("3","Checklist de evidencias")
b+=ul(["Plan de capacitación aprobado y ubicación de la actividad en el plan.","Agenda y objetivos.","Material utilizado (presentación, casos, lecturas).","Lista de asistencia firmada o reporte de la plataforma.","Pruebas de entrada y de salida.","Informe de resultados.","Constancias o certificados emitidos.","Acciones de refuerzo para quienes no aprobaron."],"chk")
b+=call("Las evidencias se archivan según la política documental de la entidad y deben estar disponibles para la auditoría interna y la supervisión.","gold")
b+='<div class="sign"><div>Facilitador</div><div>Oficial de cumplimiento</div><div>Talento humano</div></div>'
D["registro-evidencias"]=("Registro de evidencias",K4,"Ficha de la actividad, lista de asistencia y checklist de evidencias para auditoría y supervisión.",b,False)
