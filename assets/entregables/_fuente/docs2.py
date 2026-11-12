from base import *
import json, os
D={}
K2="Servicio 02 · Gestión de riesgos y debida diligencia"
R=json.load(open(os.path.join(os.path.dirname(__file__),'matriz_data.json'),encoding='utf-8'))
W=[.30,.20,.15,.25,.10]
def cat(v): return "Muy bajo" if v<1.5 else "Bajo" if v<2.5 else "Medio" if v<3.5 else "Alto" if v<4.5 else "Muy alto"
def f2(v): return f"{round(v+1e-9,2):.2f}"
# ---------- 05 Matriz de riesgo
b=call("<b>Entregable completo:</b> libro de Excel con hojas de resumen, parámetros, catálogo de sujetos obligados, catálogo de jurisdicciones y matrices de sujetos obligados financieros y no financieros. Esta ficha resume su estructura y muestra un extracto. Metodología propia de Hansliery Sánchez, base del motor de riesgo de Compliance Guard Pro.","blue")
b+=h2("1","Estructura del libro")
b+=tbl(["Hoja","Contenido"],[["Resumen","Instrucciones de uso, escala y rangos de categorías."],["Parámetros","Factores, pesos y escala de 1 a 5."],["Sujetos_Obligados","Catálogo de sujetos obligados financieros y no financieros (Ley 155-17, arts. 32 y 33)."],["Jurisdicciones","Catálogo de jurisdicciones con su puntaje de riesgo."],["Matriz_Financieros","23 líneas de producto de sujetos obligados financieros."],["Matriz_No_Financieros","23 líneas de producto de sujetos obligados no financieros."]],widths=["24%",None])
b+=h2("2","Parámetros")
b+='<div class="cols"><div>'+tbl(["Factor","Peso"],[["Cliente","30 %"],["Producto / servicio","20 %"],["Canal","15 %"],["Jurisdicción","25 %"],["Transaccionalidad","10 %"],["<b>Total</b>","<b>100 %</b>"]])+'</div><div>'+tbl(["Puntaje","Categoría"],[["0.00 – 1.49",pill("Muy bajo")],["1.50 – 2.49",pill("Bajo")],["2.50 – 3.49",pill("Medio")],["3.50 – 4.49",pill("Alto")],["4.50 – 5.00",pill("Muy alto")]])+'</div></div>'
b+=call("<b>Riesgo inherente</b> = Σ (puntaje del factor × peso). <b>Riesgo residual</b> = máximo entre 1 y [riesgo inherente × (1 − efectividad de los controles)]. Ambos se clasifican con los mismos rangos.")
b+=call("<b>Importante:</b> los puntajes de cada línea son valores de partida parametrizables por el oficial de cumplimiento. Deben calibrarse con los datos históricos de la entidad, aprobarse por las instancias correspondientes y revisarse periódicamente.","gold")
b+='<h2 class="pb"><b>3</b>Catálogo de jurisdicciones</h2>'
b+=tbl(["Jurisdicción","Puntaje"],[["República Dominicana (nacional)","1"],["Estados Unidos","2"],["Unión Europea / España","2"],["Latinoamérica y el Caribe","3"],["Centros offshore (paraísos fiscales)","4"],["Países de alto riesgo GAFI (lista negra o gris)","5"]],widths=[None,"14%"])
b+=h2("4","Extracto de la matriz")
rows=[]
for i in [0,2,8,15,17,23,25,27,40,41]:
    r=R[i];s=r[5];inh=sum(a*w for a,w in zip(s,W));res=max(1,inh*(1-r[7]))
    rows.append([r[0],e(r[2]),e(r[3]),e(r[4])]+[str(x) for x in s]+[f2(inh)+" "+pill(cat(inh)),f"{round(r[7]*100)} %",f2(res)+" "+pill(cat(res))])
b+=tbl(["ID","Producto","Canal","Jurisdicción","Cli.","Prod.","Can.","Jur.","Trx.","Inherente","Efect.","Residual"],rows,widths=["9%","17%","11%","15%","4%","4%","4%","4%","4%","11%","6%",None])
D["matriz-riesgo"]=("Matriz de riesgo en Excel",K2,"Ficha técnica de la matriz de riesgo parametrizada: estructura del libro, factores y pesos, rangos, fórmulas y extracto de líneas de referencia.",b,False)

# ---------- 06 Metodología
b=h2("1","Objetivo")
b+="<p>Establecer un método documentado, repetible y trazable para identificar, medir y clasificar el riesgo de LA/FT/FPADM de clientes, productos y relaciones, como base para asignar el nivel de debida diligencia y de monitoreo.</p>"
b+=h2("2","Fundamento")
b+=ul(["Ley 155-17: programa de cumplimiento basado en riesgos (art. 34), debida diligencia basada en riesgos (art. 36) y factores mínimos de riesgo (art. 37).","Recomendación 1 del GAFI: evaluación de riesgos y enfoque basado en riesgos.","Comité de Supervisión Bancaria de Basilea: <i>Sound management of risks related to money laundering and financing of terrorism</i>."])
b+=h2("3","Factores y ponderación")
b+="<p>La ley exige considerar, como mínimo, clientes, productos y servicios, canales de distribución y zona geográfica (art. 37). La metodología añade la <b>transaccionalidad</b> para reflejar el volumen y el comportamiento de las operaciones.</p>"
b+=tbl(["Factor","Peso","Qué mide"],[["Cliente","30 %","Tipo de persona, actividad, origen de fondos, condición PEP, antigüedad y estructura."],["Producto / servicio","20 %","Anonimato, uso de efectivo, transferibilidad y complejidad."],["Canal","15 %","Presencialidad, intermediarios y canales digitales sin contacto."],["Jurisdicción","25 %","País de residencia, origen o destino de fondos y operaciones."],["Transaccionalidad","10 %","Volumen, frecuencia y desviación respecto del perfil."]],widths=["20%","9%",None])
b+=h2("4","Escala de calificación por factor (guía)")
b+=tbl(["Nivel","Cliente","Producto / servicio","Canal","Transaccionalidad"],[["1 · Muy bajo","Persona física con ingresos verificables, residente","Producto de bajo monto y sin efectivo","Presencial con identificación directa","Operaciones dentro del perfil y de bajo monto"],["2 · Bajo","Asalariado o empresa con historial verificable","Producto estándar con controles de monto","Presencial o plataforma propia autenticada","Volumen estable y coherente"],["3 · Medio","Independiente o empresa con actividad en efectivo","Producto con transferencias o terceros","Intermediario o corresponsal regulado","Variaciones ocasionales"],["4 · Alto","Estructuras complejas o actividades sensibles","Alto valor, efectivo o fácil transferencia","Canal no presencial o intermediario no regulado","Volumen alto o picos no explicados"],["5 · Muy alto","PEP o cliente con información adversa relevante","Alto anonimato o productos de alto riesgo","Canales que dificultan la identificación","Operaciones inusuales recurrentes"]],widths=["12%",None,None,None,None])
b+='<p class="small">Para jurisdicciones se utiliza el catálogo de la matriz (de 1 para la República Dominicana a 5 para países de alto riesgo GAFI).</p>'
b+=h2("5","Cálculo")
b+=steps([("Puntuar","Asignar a cada factor un puntaje de 1 a 5 según la guía."),("Riesgo inherente","Σ (puntaje × peso). Ejemplo: 3×0.30 + 2×0.20 + 2×0.15 + 1×0.25 + 2×0.10 = 2.05 (Bajo)."),("Efectividad de controles","Estimar el porcentaje de mitigación según el diseño y la eficacia probada de los controles."),("Riesgo residual","máx(1; inherente × (1 − efectividad)). Ejemplo: 2.05 × 0.90 = 1.85 (Bajo)."),("Reglas de prevalencia","Ciertas condiciones fijan una categoría mínima con independencia del puntaje; por ejemplo, las PEP se tratan como alto riesgo (art. 46).")])
b+=h2("6","Calibración y gobierno")
b+=ul(["Calibrar pesos y puntajes con datos históricos: alertas, ROS, hallazgos y rechazos.","Aprobar la metodología y sus cambios en las instancias de gobierno de la entidad.","Revisar al menos una vez al año y cuando cambien la normativa, los productos, los canales o las tipologías.","Registrar cada cambio de parámetros con fecha, responsable y justificación."])
D["metodologia"]=("Metodología documentada",K2,"Fundamento, factores, ponderaciones, escalas, cálculo del riesgo inherente y residual, reglas de prevalencia y gobierno del modelo.",b,False)

# ---------- 07 Formularios y checklists
b=h2("A","Conozca a su cliente · persona física")
b+=fld(["Nombres y apellidos","Documento de identidad y número","Nacionalidad","Fecha de nacimiento","!Dirección de residencia","Teléfono y correo","Ocupación o profesión","Empleador o actividad económica","Ingresos mensuales (rango)","!Origen de los fondos","Propósito de la relación","Volumen transaccional esperado","¿Es PEP o familiar o colaborador cercano de una PEP?  Sí ☐  No ☐","¿Actúa por cuenta de un tercero?  Sí ☐  No ☐"])
b+=h2("B","Conozca a su cliente · persona jurídica")
b+=fld(["Razón social","RNC","Forma jurídica","Fecha de constitución","!Dirección","Actividad económica","Representante legal","!Beneficiarios finales (anexo C)","Países donde opera","Volumen transaccional esperado"])
b+='<p class="small">La ley exige verificar, entre otros, razón social, RNC, forma jurídica, dirección y beneficiario final (art. 40).</p>'
b+='<h2 class="pb"><b>C</b>Declaración de beneficiario final</h2>'
b+=tbl(["Nombre completo","Documento","Nacionalidad","% de participación","Forma de control","¿PEP?"],[["","","","","",""]]*4,widths=["26%","16%","14%","14%","20%",None])
b+='<p class="small">Identificar a las personas físicas que en último término poseen o controlan al cliente, conforme al umbral y criterios de la normativa aplicable. Adjuntar organigrama de propiedad.</p>'
b+=h2("D","Declaración de persona expuesta políticamente (PEP)")
b+=fld(["Cargo público o función desempeñada","Institución","Fecha de inicio","Fecha de cese (si aplica)","!Familiares hasta el segundo grado y colaboradores cercanos","!Origen del patrimonio y de los fondos"])
b+='<p class="small">Las PEP se tratan como clientes de alto riesgo; la obligación alcanza a sus familiares hasta el segundo grado (art. 46).</p>'
b+=h2("E","Checklist por nivel de debida diligencia")
b+=tbl(["Medida","Simplificada","Estándar","Ampliada"],[[a,*x] for a,x in [("Identificación y verificación del cliente",["✓","✓","✓"]),("Identificación del beneficiario final",["✓","✓","✓"]),("Propósito y naturaleza de la relación",["Básico","✓","✓"]),("Origen de los fondos",["—","Declarado","Documentado"]),("Origen del patrimonio",["—","—","Documentado"]),("Aprobación de la alta gerencia",["—","—","✓"]),("Screening en listas",["✓","✓","✓"]),("Actualización del expediente",["Menos frecuente","Periódica","Más frecuente"]),("Intensidad del monitoreo",["Reducida","Regular","Reforzada"])]],widths=[None,"17%","17%","17%"])
b+=call("La debida diligencia simplificada no es aceptable cuando existe sospecha de lavado de activos o financiamiento del terrorismo (art. 42). Las frecuencias concretas se definen en el manual de la entidad.","gold")
D["formularios-checklists"]=("Formularios y checklists de debida diligencia",K2,"Formularios modelo para personas físicas y jurídicas, beneficiario final y PEP, y checklist de medidas por nivel de riesgo.",b,False)

# ---------- 08 Procedimiento de screening
b=kv([("Código","PR-04"),("Responsable","Oficial de cumplimiento"),("Versión",PH)])
b+=h2("1","Objetivo y alcance")
b+="<p>Verificar a clientes, beneficiarios finales, representantes y contrapartes contra listas de sanciones, bases de PEP y fuentes de información adversa, y gestionar las coincidencias de forma oportuna y documentada.</p>"
b+=h2("2","Fuentes")
b+=tbl(["Fuente","Uso"],[["Listas del Consejo de Seguridad de las Naciones Unidas","Obligatoria: sanciones financieras dirigidas, que deben aplicarse sin demora."],["Listas y comunicaciones de las autoridades nacionales","Obligatoria según la normativa vigente."],["Otras listas internacionales (por ejemplo OFAC o Unión Europea)","Según la política de riesgo y las relaciones de la entidad."],["Bases de datos de PEP","Identificación de PEP, familiares y colaboradores cercanos."],["Medios e información pública","Información adversa relevante para el perfil de riesgo."]],widths=["38%",None])
b+=h2("3","Momentos de consulta")
b+=ul(["Antes de iniciar la relación o ejecutar una transacción ocasional.","En cada actualización del expediente.","Cuando se actualizan las listas (rescreening de toda la cartera).","Antes de pagos o transferencias a terceros, según el producto."])
b+=h2("4","Flujo de gestión de coincidencias")
b+=steps([("Consulta","Ejecutar la búsqueda con nombre completo, documento, fecha de nacimiento y nacionalidad."),("Análisis","Comparar los datos de identificación para descartar homonimias."),("Clasificación","Clasificar el resultado según la tabla siguiente y documentar la decisión."),("Escalamiento","Escalar al oficial de cumplimiento toda coincidencia potencial o confirmada."),("Medidas","Ante coincidencia confirmada en listas de sanciones, aplicar las medidas de congelamiento sin demora y comunicar a las autoridades conforme a la normativa; evaluar la remisión de un ROS."),("Registro","Conservar la evidencia de la consulta y de la decisión al menos 10 años (art. 43).")])
b+=tbl(["Resultado","Criterio","Acción"],[[pill("Sin coincidencia"),"No hay resultados","Continuar el proceso y guardar la constancia."],[pill("Falso positivo"),"Coincide el nombre pero no los demás identificadores","Descartar con justificación documentada."],[pill("Potencial"),"Coincidencias parciales sin poder descartar","Suspender el proceso y escalar; solicitar información adicional."],[pill("Confirmada"),"Los identificadores coinciden","Aplicar medidas, informar a las autoridades y evaluar ROS."]],widths=["18%","34%",None])
b+=call("<b>Confidencialidad:</b> no se debe revelar al cliente ni a terceros que se ha realizado o se realizará un reporte o una comunicación a las autoridades (art. 63).","gold")
b+=h2("5","Constancia de screening")
b+=fld(["Nombre consultado","Documento","Fecha y hora","Fuentes consultadas","Resultado","Analista","!Justificación de la decisión","Aprobación del oficial de cumplimiento (si aplica)"])
D["procedimiento-screening"]=("Procedimiento de screening",K2,"Fuentes, momentos de consulta, flujo de análisis y clasificación de coincidencias, medidas, confidencialidad y constancia.",b,False)
