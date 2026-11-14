# Hansliery Sánchez · Compliance & Risk Advisory

Sitio web profesional de una sola página: consultoría PLAFT, compliance, gestión de riesgos, debida diligencia, capacitación y automatización.

**Estrategia. Prevención. Confianza.**

---

## Contenido del proyecto

```
hansliery-web/
├── index.html          ← Sitio completo (HTML + CSS + JavaScript integrados)
├── favicon.svg         ← Icono del sitio (marca HS)
├── robots.txt          ← Indicaciones para buscadores
├── README.md           ← Este archivo
├── assets/
│   ├── og-image.png    ← Imagen 1200×630 para vista previa en redes sociales
│   ├── entregables/    ← 16 PDF modelo de los entregables de cada servicio
│   │   └── _fuente/    ← Generador (python3 build.py; requiere Playwright, Chrome y las fuentes Sora/Manrope)
│   ├── lexium-dashboard.(jpg|webp) ← Captura de LEXIUM (datos de demostración)
│   ├── medinovaq-agenda.(jpg|webp) ← Captura de MEDINOVAQ (datos ficticios; demo en https://medinovaq.pages.dev)
│   └── hansliery-sanchez.(jpg|webp) ← Foto de perfil
├── legal/              ← Términos, privacidad, cookies, aviso legal y accesibilidad (generadas con legal/_fuente/build.py)
└── cursos/             ← Capacitaciones gratuitas (13 cursos + catálogo)
    ├── index.html      ← Catálogo
    ├── <curso>.html    ← Una página por curso (generada)
    ├── cursos.css / cursos.js
    └── _fuente/        ← Contenido editable y generador
```

## Cursos

Los cursos se generan a partir de archivos de contenido en `cursos/_fuente/`:

- `cursos_1.py` … `cursos_4.py`: texto, evaluación y fuentes de cada curso.
- `fuentes.py`: registro único de fuentes oficiales citadas.
- `build.py`: genera las páginas HTML, el catálogo y `indice.json`.

Para editar un curso, modifique su archivo de contenido y ejecute:

```
python3 cursos/_fuente/build.py
```

Dentro del texto, `[[3]]` crea una cita a la fuente número 3 del curso. El generador mezcla las opciones de cada pregunta para que la respuesta correcta no caiga siempre en la misma letra, y valida que toda cita apunte a una fuente existente.

No requiere instalación, compilación ni frameworks. Solo depende de Google Fonts (Sora + Manrope). Si las fuentes no cargan, el sitio usa tipografías del sistema y sigue funcionando.

## Costos

La sección `#costos` muestra precios de referencia en RD$ (más ITBIS 18 %) y en US$ para clientes del exterior. Para cambiar un precio, edite los atributos `data-dop` y `data-usd` de cada `.pc-amt` (el texto visible se recalcula al cargar) y, en la calculadora, el `value` de cada opción de `#pcc-svc`. Las tasas de retención (ISR 15 % a personas físicas, Ley 30-26; ITBIS 100 % o 30 % según Norma 02-05) están en el bloque `pricing` del `<script>`. Revise los precios cada seis meses.

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

Para volver a hacerlo visible en Google: cambie la etiqueta a `index, follow` en `index.html`, `cursos/_fuente/build.py` (y regenere cursos y páginas legales), vuelva a crear `sitemap.xml` y añada la línea `Sitemap:` en `robots.txt`.

### Si adquiere un dominio propio

1. Configure el dominio en *Settings → Pages → Custom domain* del repositorio.
2. Reemplace `https://hansliery89.github.io/hansliery-web/` por el nuevo dominio en `index.html` (canonical, og:url, og:image, twitter:image y JSON-LD) y en los generadores de `cursos/_fuente` y `legal/_fuente`.
3. Si decide hacerlo público, siga los pasos de «Visibilidad» y registre el sitio en Google Search Console.

## Personalización rápida

Todo está en `index.html`, organizado por secciones comentadas.

- **Colores:** variables en `:root` al inicio del `<style>` (`--night`, `--petrol`, `--teal`, `--electric`, `--gold`, `--ice`).
- **Textos:** cada sección está marcada con un comentario (`A. HEADER`, `B. HERO`, `C. PERFIL`…).
- **Indicadores de capacitación:** atributos `data-count` en la sección Perfil (el texto dentro de la etiqueta es el valor que se muestra sin JavaScript; mantenga ambos iguales).
- **Nuevos canales de contacto:** en el `<script>`, objeto `CONTACT_CONFIG`. Complete `phone`, `whatsapp` (solo dígitos con código de país) o `linkedin` (URL completa) y aparecerán automáticamente en Contacto. Si están vacíos, no se muestra nada.

## Cómo funciona el formulario

El sitio **no tiene servidor** y no almacena ni transmite datos. Al pulsar «Preparar correo»:

1. Se validan los campos (nombre, correo, servicio y una descripción de al menos 20 caracteres).
2. Se limpia el contenido (caracteres de control, etiquetas HTML, longitudes máximas).
3. Se abre la aplicación de correo del visitante con asunto y mensaje ya redactados.
4. Si el visitante no tiene una aplicación de correo configurada, puede usar «Copiar mensaje» y enviarlo manualmente.

Para recibir los mensajes directamente sin depender del cliente de correo, puede integrarse más adelante un servicio como Formspree, Netlify Forms o una función propia. En ese caso, actualice también la directiva `connect-src` / `form-action` de la política de seguridad (`<meta http-equiv="Content-Security-Policy">`).

## Accesibilidad y rendimiento

- HTML semántico con un único `h1` y jerarquía de encabezados ordenada.
- Enlace «Saltar al contenido», estados de foco visibles y menú móvil operable con teclado (Escape cierra, foco atrapado).
- Respeta `prefers-reduced-motion`: sin escritura animada, partículas estáticas, contadores con su valor final.
- La red de partículas se pausa cuando el hero no está visible o la pestaña está oculta.
- Efectos de cursor e inclinación 3D solo en dispositivos con puntero preciso.
- Sin imágenes externas: toda la iconografía es SVG integrado.

## Aviso

Los indicadores de experiencia formativa (2,300+ participantes, 214 horas, 93.38 % de evaluación promedio) representan experiencia formativa y no resultados comerciales ni garantías de desempeño. Los paneles del hero y la matriz de riesgo son visualizaciones ilustrativas, no datos reales.

---
© 2026 Hansliery Sánchez · Compliance & Risk Advisory
