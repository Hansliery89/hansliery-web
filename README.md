# Hansliery Sánchez · Compliance & Risk Advisory

Sitio web profesional (portada + páginas interiores): consultoría PLAFT, compliance, gestión de riesgos, debida diligencia, capacitación y automatización.

**Estrategia. Prevención. Confianza.**

---

## Contenido del proyecto

El sitio ya no es una sola página: la portada resume y las páginas interiores detallan.

```
hansliery-web/
├── index.html               ← Portada (resumen: servicios, perfil, software, cursos, costos, preguntas, contacto)
├── sobre-mi.html            ← Trayectoria, credenciales y diferenciadores
├── servicio-consultoria.html│
├── servicio-riesgos.html    │ Una página por servicio (incluye la matriz de riesgo interactiva en «riesgos»)
├── servicio-controles.html  │
├── servicio-capacitacion.html
├── software.html            ← Compliance Guard Pro, LEXIUM y MEDINOVAQ
├── costos.html              ← Planes, proyectos, calculadora de factura y facturación electrónica
├── 404.html                 ← Página de error (GitHub Pages la usa automáticamente)
├── diagnostico-riesgos.html ← Evaluador preliminar de riesgos LA/FT
├── assets/
│   ├── css/site.css         ← Estilos comunes a todas las páginas generadas
│   ├── js/site.js           ← Comportamiento común (menú, formulario, calculadora, matriz…)
│   ├── sitio/               ← GENERADOR de las páginas anteriores
│   │   ├── build.py         ← Configuración (bloque SITE) + encabezado, menú y pie comunes
│   │   ├── paginas/*.html   ← Contenido editable de cada página
│   │   └── partes/          ← Iconos SVG y datos estructurados
│   ├── og-image.jpg         ← Vista previa en redes (69 KB; og-image.png se conserva para cursos y legales)
│   ├── entregables/         ← 16 PDF modelo de los entregables
│   └── …                    ← Fotos y capturas
├── legal/  cursos/  lexium-demo/
```

## Cómo editar las páginas principales

**No edite** `index.html`, `sobre-mi.html`, `costos.html`, `software.html`, `servicio-*.html` ni `404.html` directamente: se regeneran. Edite el archivo equivalente en `assets/sitio/paginas/` y ejecute:

```
python3 assets/sitio/build.py
```

El menú (5 opciones: Servicios · Sobre mí · Software · Cursos · Costos) y el pie se definen una sola vez en `build.py`.

### Configuración (bloque `SITE` de `assets/sitio/build.py`)

| Clave | Para qué sirve |
|---|---|
| `whatsapp` | Solo dígitos con código de país. Muestra «Escribir por WhatsApp» en Contacto. |
| `agenda` | Enlace de Calendly / Google Calendar / Bookings. Muestra «Agendar una reunión». |
| `form_endpoint` | Dirección de Formspree (`https://formspree.io/f/…`). El formulario envía directo, sin depender del correo del visitante. **Al activarlo, actualice la Política de privacidad**, que hoy dice que el sitio no transmite datos. |
| `plausible_domain` | Analítica sin cookies (Plausible). La política de seguridad se ajusta sola. |
| `url`, `base_path` | Cámbielos si adquiere un dominio propio. |
| `indexable` | `True` para aparecer en Google: cambia `robots` y genera `sitemap.xml`. |

`TESTIMONIOS`: lista de testimonios **reales y autorizados**. La sección aparece en la portada solo cuando hay al menos uno.

## Cursos

Los cursos se generan a partir de archivos de contenido en `cursos/_fuente/`:

- `c01.py` … `c13.py`: un archivo por curso (módulos, glosario, evaluación y fuentes).
- `capas.py`: ayudas `ess()` («Lo esencial», para público general) y `deep()` («Para profundizar», desplegable de nivel profesional). Cada módulo combina: esencial + desarrollo + profundizar.
- `fuentes.py`: registro único de fuentes oficiales citadas.
- `build.py`: genera las páginas HTML, el catálogo y `indice.json`.

Para editar un curso, modifique su archivo de contenido y ejecute:

```
python3 cursos/_fuente/build.py
```

Dentro del texto, `[[3]]` crea una cita a la fuente número 3 del curso. El generador mezcla las opciones de cada pregunta para que la respuesta correcta no caiga siempre en la misma letra, y valida que toda cita apunte a una fuente existente.

No requiere instalación, compilación ni frameworks. Solo depende de Google Fonts (Sora + Manrope). Si las fuentes no cargan, el sitio usa tipografías del sistema y sigue funcionando.

## Academy (aula virtual)

Sección independiente en `academy/` con su propia navegación y autenticación, y la misma identidad del portal. Se accede con el botón «Acceder al aula virtual» de la sección Capacitaciones de la portada y de la página del servicio de capacitación.

| Página | Fuente | Función |
|---|---|---|
| `academy/index.html` | `assets/sitio/paginas/academy-index.html` | Iniciar sesión, registro (correo o Google), verificación en dos pasos, códigos de recuperación y restablecimiento de contraseña. |
| `academy/panel.html` | `academy-panel.html` | Panel del estudiante: resumen, capacitaciones, evaluaciones en línea (temporizador y autoguardado), entregas de asignaciones, certificados, reconocimientos y becas, consultas, notificaciones, pagos registrados, perfil y seguridad. |
| `academy/admin.html` | `academy-admin.html` | Centro de control (requiere rol de personal y 2FA): resumen, estudiantes, cursos y materiales, evaluaciones y calificación, asignaciones, certificados, mensajes y avisos, finanzas, reconocimientos y becas, cuentas y roles, configuración y auditoría. Cada rol ve solo lo que le corresponde. |
| `academy/certificado.html` | `academy-certificado.html` | Certificado imprimible (A4 horizontal, «Guardar como PDF») con código y QR de verificación. |
| `academy/verificar.html` | `academy-verificar.html` | Verificador público de certificados. |
| `academy/ayuda.html` | `academy-ayuda.html` | Centro de ayuda. |

- Las páginas se generan con `python3 assets/sitio/build.py` (metadatos `csp: academy` y `scripts:`). Tienen una política de seguridad propia que solo permite conectarse al proyecto Supabase y a la comprobación de contraseñas filtradas; el resto del portal conserva la suya.
- JavaScript: `academy/js/core.js` (cliente y utilidades), `acceso.js`, `panel.js`, `admin.js`, `certificado.js`, `verificar.js`. Las librerías `supabase-js` 2.119.2 y `qrcode-generator` 1.4.4 (MIT) están copiadas en `academy/js/vendor/` (sin CDN).
- La URL y la clave **pública** de Supabase están en el bloque `ACADEMY` de `assets/sitio/build.py`. Nunca coloque ahí claves secretas.
- Backend, migraciones, pruebas y configuración de Auth: ver `supabase/README.md`.

## Diagnóstico preliminar de riesgos

`diagnostico-riesgos.html` es un cuestionario de 26 preguntas en 6 pasos que calcula, solo en el navegador, el riesgo inherente y residual por factor con la metodología de la matriz (pesos 30/20/15/25/10, controles hasta 30 %). Muestra un mapa de calor, las brechas prioritarias y un informe imprimible como PDF. Se accede desde la tarjeta del Servicio 02. Preguntas, puntajes y recomendaciones están en `assets/diagnostico/diagnostico.js`; estilos en `diagnostico.css`; el marco de la página en `body.html` (ejecute `python3 assets/diagnostico/build.py` tras editarlo). El botón «Solicitar asesoría profesional» abre `index.html?servicio=riesgos&dx=…&pts=…#contacto`, que preselecciona el servicio y redacta el mensaje.

## Costos

La página `costos.html` (fuente: `assets/sitio/paginas/costos.html`) muestra precios de referencia en RD$ (más ITBIS 18 %) y en US$ para clientes del exterior. Para cambiar un precio, edite los atributos `data-dop` y `data-usd` de cada `.pc-amt` (el texto visible se recalcula al cargar) y, en la calculadora, el `value` de cada opción de `#pcc-svc`. Las tasas de retención (ISR 15 % a personas físicas, Ley 30-26; ITBIS 100 % o 30 % según Norma 02-05) están en el bloque `pricing` de `assets/js/site.js`. **Si cambia un precio, actualícelo también** en el resumen de la portada (`paginas/index.html`: tarjetas «Desde RD$…» y planes) y en la tabla de la página del servicio. Revise los precios cada seis meses.

## Cómo verlo

Haga doble clic en `index.html`. Se abre en cualquier navegador moderno (Chrome, Edge, Firefox, Safari).

## Cómo publicarlo

Cualquier hosting estático sirve. Suba **la carpeta completa** (no solo `index.html`).

| Opción | Pasos |
|---|---|
| **Netlify** (más simple) | Entre a app.netlify.com/drop y arrastre la carpeta. Obtiene una URL al instante y luego puede conectar su dominio. |
| **GitHub Pages** | Cree un repositorio, suba los archivos y active *Settings → Pages → Deploy from branch (main / root)*. |
| **Vercel / Cloudflare Pages** | Importe la carpeta o el repositorio; no hace falta comando de build. |
| **Hosting tradicional (cPanel)** | Suba los archivos a `public_html` por el administrador de archivos o FTP. |

## Dirección publicada

**https://hansliery89.github.io/hansliery-web/** (GitHub Pages, rama `main`). Cada cambio subido a `main` se publica automáticamente en 1–2 minutos.

El canonical, Open Graph y datos estructurados ya apuntan a esa dirección.

### Visibilidad: sitio no indexado

El sitio está oculto para los buscadores: todas las páginas llevan `<meta name="robots" content="noindex, nofollow, noarchive, nosnippet">` y no hay `sitemap.xml`. Solo lo encuentra quien tenga el enlace. **No es una protección de acceso**: cualquiera que reciba el enlace puede abrirlo y reenviarlo.

Para volver a hacerlo visible en Google: ponga `indexable: True` en `assets/sitio/build.py` (genera `sitemap.xml`), cambie la etiqueta a `index, follow` en `cursos/_fuente/build.py` y `legal/_fuente` (y regenere), y añada la línea `Sitemap:` en `robots.txt`.

### Si adquiere un dominio propio

1. Configure el dominio en *Settings → Pages → Custom domain* del repositorio.
2. Cambie `url` y `base_path` en `assets/sitio/build.py`, reemplace la dirección en `assets/sitio/partes/jsonld.html` y en los generadores de `cursos/_fuente` y `legal/_fuente`, y regenere.
3. Si decide hacerlo público, siga los pasos de «Visibilidad» y registre el sitio en Google Search Console.

## Personalización rápida

Contenido en `assets/sitio/paginas/`, estilos en `assets/css/site.css`.

- **Colores:** variables en `:root` al inicio de `assets/css/site.css` (`--night`, `--petrol`, `--teal`, `--electric`, `--gold`, `--ice`).
- **Textos:** cada sección de `assets/sitio/paginas/index.html` está marcada con un comentario.
- **Indicadores de capacitación:** atributos `data-count` en la sección Perfil (el texto dentro de la etiqueta es el valor que se muestra sin JavaScript; mantenga ambos iguales).
- **Canales de contacto:** bloque `SITE` de `assets/sitio/build.py` (ver tabla arriba).

## Cómo funciona el formulario

Por defecto el sitio **no tiene servidor** y no almacena ni transmite datos. Al pulsar «Preparar correo»:

1. Se validan los campos (nombre, correo, servicio y una descripción de al menos 20 caracteres).
2. Se limpia el contenido (caracteres de control, etiquetas HTML, longitudes máximas).
3. Se abre la aplicación de correo del visitante con asunto y mensaje ya redactados.
4. Si el visitante no tiene una aplicación de correo configurada, puede usar «Copiar mensaje» y enviarlo manualmente.

Para recibir los mensajes directamente, complete `form_endpoint` en `assets/sitio/build.py` con su dirección de Formspree y regenere: el botón pasa a «Enviar mensaje» y la política de seguridad se ajusta sola. Actualice entonces la Política de privacidad.

## Accesibilidad y rendimiento

- HTML semántico con un único `h1` y jerarquía de encabezados ordenada.
- Enlace «Saltar al contenido», estados de foco visibles y menú móvil operable con teclado (Escape cierra, foco atrapado).
- Respeta `prefers-reduced-motion`: sin escritura animada, partículas estáticas, contadores con su valor final.
- La red de partículas se pausa cuando el hero no está visible o la pestaña está oculta.
- Efectos de cursor e inclinación 3D solo en dispositivos con puntero preciso.
- Sin imágenes externas: toda la iconografía es SVG integrado.
- Verificado con axe-core (WCAG 2.2 AA): 0 violaciones en portada, perfil, software, costos y servicios, y en el catálogo y los 13 cursos (nov. 2026).

## Aviso

Los indicadores de experiencia formativa (2,300+ participantes, 214 horas, 93.38 % de evaluación promedio) representan experiencia formativa y no resultados comerciales ni garantías de desempeño. Los paneles del hero y la matriz de riesgo son visualizaciones ilustrativas, no datos reales.

---
© 2026 Hansliery Sánchez · Compliance & Risk Advisory
