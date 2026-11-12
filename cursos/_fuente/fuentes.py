"""Registro único de fuentes citadas en los cursos (texto + URL verificada cuando existe)."""

LEY = {"text": "Congreso Nacional de la República Dominicana. Ley núm. 155-17 contra el lavado de activos y el financiamiento del terrorismo, del 1 de junio de 2017 (copia publicada por la Superintendencia de Bancos).",
       "url": "https://www.sb.gob.do/media/oepagpnr/ley-no-155-17-contra-el-lavado-de-activos-y-el-financiamiento-del-terrorismo.pdf"}
REG = {"text": "Poder Ejecutivo. Decreto núm. 408-17, Reglamento de aplicación de la Ley núm. 155-17 (copia publicada por la Superintendencia de Bancos).",
       "url": "https://sb.gob.do/media/wkrboumv/reglamento-de-aplicacion-de-la-ley-no-155-17-contra-el-lavado-de-activos-el-financiamiento-del-terrorismo-y-la-proliferaci.pdf"}
GAFI40 = {"text": "GAFI (2012-2025). Estándares internacionales sobre la lucha contra el lavado de activos, el financiamiento del terrorismo y de la proliferación: Las Recomendaciones del GAFI (versión en español publicada por la UAF, diciembre 2025).",
          "url": "https://uaf.gob.do/phocadownload/SobreNosotros/NacionaleInternacional/documentosGAFIGAFILAT/GAFI/40%20Recomendaciones%20del%20GAFI%20Diciembre-2025.pdf"}
UAF_ROS = {"text": "Unidad de Análisis Financiero (2024). Guía de Calidad para los Reportes de Operaciones Sospechosas (ROS). Dirección de Análisis, enero 2024. Disponible en el portal de la UAF, sección Publicaciones.",
           "url": "https://www.uaf.gob.do"}
UAF_SEG = {"text": "Unidad de Análisis Financiero (2025). Subguía de Calidad de ROS para el Sector Seguros. Septiembre 2025.", "url": "https://www.uaf.gob.do"}
UAF_COOP = {"text": "Unidad de Análisis Financiero (2024). Subguía de Calidad de los ROS para el Sector Cooperativas. Enero 2024.", "url": "https://www.uaf.gob.do"}
UAF_CAMB = {"text": "Unidad de Análisis Financiero (2024). Subguía de Calidad para los ROS del Sector Agentes de Cambio y Remesadoras. Enero 2024.", "url": "https://www.uaf.gob.do"}
UAF_VAL = {"text": "Unidad de Análisis Financiero (2024). Subguía de Calidad de los ROS para el Sector del Mercado de Valores. Enero 2024.", "url": "https://www.uaf.gob.do"}
UAF_CAS = {"text": "Unidad de Análisis Financiero (2024). Subguía de Calidad de los ROS para Casinos, Juegos de Azar, Bancas de Lotería o Apuestas y Concesionarios de Lotería. Enero 2024.", "url": "https://www.uaf.gob.do"}
UAF_DGII = {"text": "Unidad de Análisis Financiero (2024). Subguía de Calidad de los ROS para los Sujetos Obligados Supervisados por la DGII. Enero 2024.", "url": "https://www.uaf.gob.do"}
GOAML = {"text": "Unidad de Análisis Financiero (2021). Manual de Usuario web goAML.", "url": "https://goaml.uaf.gob.do/Home"}
TIGA03 = {"text": "Unidad de Análisis Financiero, Dirección de TIC. Guía TI-GA-03 «Registro en goAML para usuarios», versión 00 (elaborada por Hansliery Sánchez Figuereo).", "url": "https://www.uaf.gob.do"}
DGII_BRO = {"text": "Dirección General de Impuestos Internos (DGII). Prevención y detección del lavado de activos y financiamiento del terrorismo (material informativo).",
            "url": "https://dgii.gov.do/legislacion/prevencionLavado/informacionEspecializada/Documents/BrochureLavadoDeActivos.pdf"}
DGII_GLO = {"text": "Dirección General de Impuestos Internos (DGII). Glosario PLAFT.",
            "url": "https://dgii.gov.do/publicacionesOficiales/bibliotecaVirtual/contribuyentes/lavadoActivos/Documents/Glosario%20PLAFT.pdf"}
DGII_BF = {"text": "Dirección General de Impuestos Internos (DGII). Beneficiario Final (portal de prevención de lavado).",
           "url": "https://dgii.gov.do/legislacion/prevencionLavado/beneficiarioFinal"}
DGII_N01 = {"text": "Dirección General de Impuestos Internos (DGII). Norma General núm. 01-2018 sobre prevención de lavado de activos para sujetos obligados no financieros.",
            "url": "https://www.dgii.gov.do/legislacion/normasGenerales/Documents/Normas%20Sectoriales/Norma01-18.pdf"}
DGII_CRIPTO = {"text": "Dirección General de Impuestos Internos (DGII). Consulta técnica sobre criptomonedas (septiembre 2024), que recoge el aviso del Banco Central del 29 de junio de 2017.",
               "url": "https://dgii.gov.do/legislacion/consultas/Consultas%20Tecnicas%202024/Septiembre/Consulta%2031-Criptomonedas.pdf"}
LEY_311 = {"text": "Congreso Nacional. Ley núm. 311-14 sobre Declaración Jurada de Patrimonio (art. 2, funcionarios obligados a declarar)."}
LEY_5307 = {"text": "Congreso Nacional. Ley núm. 53-07 sobre Crímenes y Delitos de Alta Tecnología, del 23 de abril de 2007 (copia publicada por la DGII).",
            "url": "https://dgii.gov.do/legislacion/leyesTributarias/Documents/Otras%20Leyes%20de%20Inter%C3%A9s/53-07.pdf"}
LEY_7425 = {"text": "Ley Orgánica núm. 74-25 que instituye el Código Penal de la República Dominicana (vigente desde agosto de 2026; arts. 237 a 242 sobre la estafa). Resumen ejecutivo de Pellerano & Herrera.",
            "url": "https://phlaw.com/wp-content/uploads/2025/08/Ley-74-25-que-modifica-el-Co%CC%81digo-Penal-Dominicano-.pdf"}
ESTAFA_7425 = {"text": "El Caribe. «Los delitos financieros en el nuevo Código Penal dominicano» (art. 237: estafa simple, 3 a 5 años; arts. 238 a 242: estafa agravada, colectiva y piramidal, 5 a 10 años).",
               "url": "https://www.elcaribe.com.do/opiniones/los-delitos-financieros-en-el-nuevo-codigo-penal-dominicano/"}
LEY_17213 = {"text": "Congreso Nacional. Ley núm. 172-13 que tiene por objeto la protección integral de los datos personales asentados en archivos, registros públicos, bancos de datos u otros medios."}
GAFI_PEP = {"text": "GAFI (2013). Guía del GAFI: Personas Expuestas Políticamente (Recomendaciones 12 y 22). Disponible en www.fatf-gafi.org."}
GAFI_BF = {"text": "GAFI (2023). Guidance on Beneficial Ownership of Legal Persons (Recomendación 24). Disponible en www.fatf-gafi.org."}
GAFI_RBA = {"text": "GAFI (2014). Guidance for a Risk-Based Approach: The Banking Sector. Disponible en www.fatf-gafi.org."}
GAFI_VA = {"text": "GAFI (2021). Updated Guidance for a Risk-Based Approach to Virtual Assets and Virtual Asset Service Providers. Disponible en www.fatf-gafi.org."}
GAFI_VA_RF = {"text": "GAFI (2020). Virtual Assets: Red Flag Indicators of Money Laundering and Terrorist Financing. Disponible en www.fatf-gafi.org."}
GAFI_CEF = {"text": "GAFI, INTERPOL y Grupo Egmont (2023). Illicit Financial Flows from Cyber-enabled Fraud (incluye versión en español).",
            "url": "https://www.fatf-gafi.org/en/publications/Methodsandtrends/illicit-financial-flows-cyber-enabled-fraud.html"}
GAFI_TECH = {"text": "GAFI (2021). Opportunities and Challenges of New Technologies for AML/CFT.",
             "url": "https://www.fatf-gafi.org/publications/fatfrecommendations/documents/opportunities-challenges-new-technologies-for-aml-cft.html"}
NIST_AI = {"text": "National Institute of Standards and Technology (2023). Artificial Intelligence Risk Management Framework (AI RMF 1.0).",
           "url": "https://www.nist.gov/itl/ai-risk-management-framework"}
ISO_31000 = {"text": "ISO 31000:2018. Gestión del riesgo — Directrices.", "url": "https://www.iso.org/standard/65694.html"}
ISO_42001 = {"text": "ISO/IEC 42001:2023. Tecnología de la información — Inteligencia artificial — Sistema de gestión.", "url": "https://www.iso.org/standard/81230.html"}

# --- Normativa complementaria (verificada en los documentos oficiales) ---
CONCLAFIT_2024 = {"text": "CONCLAFIT. Resolución núm. CONCLAFIT-2024-01, del 3 de julio de 2024, que actualiza las multas administrativas de los arts. 74, 75 y 78 de la Ley 155-17 según el Índice de Precios al Consumidor."}
CONCLAFIT_2025_01 = {"text": "CONCLAFIT. Resolución núm. CONCLAFIT-2025-01, que aumenta los umbrales del art. 64 de la Ley 155-17, y su Nota aclaratoria del 10 de diciembre de 2025."}
CONCLAFIT_2025_02 = {"text": "CONCLAFIT. Resolución núm. CONCLAFIT-2025-02, del 26 de noviembre de 2025, sobre el alcance de la condición de sujeto obligado no financiero de las empresas constructoras."}
CONCLAFIT_2021_02 = {"text": "CONCLAFIT. Resolución núm. 02-2021, que ratifica la condición de persona expuesta políticamente de los Cónsules Generales Honorarios."}
SIS_NORMA = {"text": "Superintendencia de Seguros de la República Dominicana. Norma sobre prevención del lavado de activos, financiamiento del terrorismo y de la proliferación de armas de destrucción masiva (versión actualizada)."}
IDECOOP_NORMA = {"text": "Instituto de Desarrollo y Crédito Cooperativo (IDECOOP). Norma 001-17 sobre prevención de lavado de activos para las cooperativas."}
SIB_DD = {"text": "Superintendencia de Bancos. Circular SIB núm. 012-17, Segunda versión del Instructivo sobre Debida Diligencia."}
DEC_407 = {"text": "Poder Ejecutivo. Decreto núm. 407-17, reglamento sobre congelamiento preventivo de bienes vinculados al terrorismo, su financiamiento y la proliferación de armas de destrucción masiva."}
LEY_4426 = {"text": "Ley núm. 44-26 que modifica 27 artículos de la Ley Orgánica 74-25 (Código Penal), promulgada el 27 de julio de 2026. Análisis de Pellerano & Herrera.",
            "url": "https://phlaw.com/es/ley-44-26-principales-modificaciones-al-nuevo-codigo-penal-de-la-republica-dominicana/"}
