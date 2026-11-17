/* LEXIUM — service worker de la DEMO PÚBLICA (solo lectura).
 * Sirve las respuestas de la API grabadas por scripts/build_public_demo.py con datos ficticios.
 * No hay servidor ni base de datos: ninguna acción modifica nada.
 */
const SCOPE = new URL(self.registration.scope).pathname          // p. ej. /hansliery-web/lexium-demo/
const API = SCOPE + 'api/'
const DATA = SCOPE + 'demo-data/'
const READ_ONLY = 'Demo pública de solo lectura: los cambios no se guardan. Solicite una demostración guiada para probar el sistema completo.'

let index = null            // { users: {email: {file, user}}, public: file, version }
const cache = {}             // archivo -> respuestas
let lastUser = ''

self.addEventListener('install', () => self.skipWaiting())
self.addEventListener('activate', e => e.waitUntil(self.clients.claim()))

async function load(file) {
  if (!cache[file]) cache[file] = fetch(DATA + file, { cache: 'no-cache' }).then(r => r.json())
  return cache[file]
}
async function getIndex() {
  if (!index) index = await (await fetch(DATA + 'index.json', { cache: 'no-cache' })).json()
  return index
}

const json = (body, status = 200) => new Response(JSON.stringify(body), {
  status, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' } })

function keyVariants(path, search) {
  const out = [path + search, path]
  return out
}

async function answer(entry) {
  if (entry.file) {
    const r = await fetch(DATA + 'files/' + entry.file)
    const h = { 'Content-Type': entry.ct || 'application/octet-stream' }
    if (entry.cd) h['Content-Disposition'] = entry.cd
    return new Response(await r.blob(), { status: entry.status || 200, headers: h })
  }
  if (entry.text !== undefined) return new Response(entry.text, { status: entry.status || 200, headers: { 'Content-Type': entry.ct || 'text/plain' } })
  return json(entry.body, entry.status || 200)
}

async function lookup(user, path, search) {
  const idx = await getIndex()
  const maps = []
  if (user && idx.users[user]) maps.push(await load(idx.users[user].file))
  maps.push(await load(idx.public))
  for (const k of keyVariants(path, search)) for (const m of maps) if (m[k]) return m[k]
  return null
}

async function lookupAny(path, search) {          // enlaces <a>/<img>: cualquier usuario que lo haya grabado
  const idx = await getIndex()
  for (const u of Object.keys(idx.users)) {
    const m = await load(idx.users[u].file)
    for (const k of keyVariants(path, search)) if (m[k]) return m[k]
  }
  return null
}

// ---- Validador de cédula / RNC / NCF (mismo algoritmo que el servidor) ----
const digits = v => (v || '').replace(/\D/g, '')
function validCedula(v) {
  const d = digits(v); if (d.length !== 11 || /^0+$/.test(d)) return false
  let t = 0
  for (let i = 0; i < 10; i++) { const p = +d[i] * (i % 2 ? 2 : 1); t += Math.floor(p / 10) + (p % 10) }
  return (10 - t % 10) % 10 === +d[10]
}
function validRnc(v) {
  const d = digits(v); if (d.length !== 9) return false
  const w = [7, 9, 8, 6, 5, 4, 3, 2]; let s = 0
  for (let i = 0; i < 8; i++) s += +d[i] * w[i]
  const r = s % 11, c = r === 0 ? 2 : r === 1 ? 1 : 11 - r
  return c === +d[8]
}
const NCF = { B01: 'Crédito fiscal', B02: 'Consumo', B03: 'Nota de débito', B04: 'Nota de crédito', B11: 'Compras', B12: 'Registro único de ingresos', B13: 'Gastos menores', B14: 'Regímenes especiales', B15: 'Gubernamental', B16: 'Exportaciones', B17: 'Pagos al exterior', E31: 'e-CF Crédito fiscal', E32: 'e-CF Consumo', E33: 'e-CF Nota de débito', E34: 'e-CF Nota de crédito', E41: 'e-CF Compras', E43: 'e-CF Gastos menores', E44: 'e-CF Regímenes especiales', E45: 'e-CF Gubernamental', E46: 'e-CF Exportaciones', E47: 'e-CF Pagos al exterior' }
function checkNcf(v) {
  const s = (v || '').trim().toUpperCase().replace(/[-\s]/g, '')
  if (!/^B\d{10}$/.test(s) && !/^E\d{12}$/.test(s)) return [false, 'Formato inválido (B + 10 dígitos, o E + 12 dígitos)']
  const t = s.slice(0, 3)
  if (!NCF[t]) return [false, `Tipo de comprobante ${t} no existe en la normativa DGII`]
  if (+s.slice(3) === 0) return [false, 'Secuencia en cero']
  return [true, NCF[t]]
}
function validateId({ kind, value }) {
  if (kind === 'cedula') { const ok = validCedula(value); return { kind: 'Cédula', value, valid: ok, detail: ok ? 'Dígito verificador correcto' : 'Dígito verificador o longitud incorrectos', verify_at: 'Junta Central Electoral (consulta oficial de cédula)' } }
  if (kind === 'rnc') { const ok = validRnc(value); return { kind: 'RNC', value, valid: ok, detail: ok ? 'Dígito verificador correcto' : 'Dígito verificador o longitud incorrectos', verify_at: 'DGII — Consulta de RNC (dgii.gov.do)' } }
  const [ok, detail] = checkNcf(value)
  return { kind: 'NCF / e-CF', value, valid: ok, detail, verify_at: 'DGII — Consulta de NCF / e-CF (dgii.gov.do)' }
}

async function handleApi(req, url) {
  const path = '/' + url.pathname.slice(API.length)
  const user = req.headers.get('X-Demo-User') || ''
  if (user) lastUser = user
  if (req.method === 'GET' || req.method === 'HEAD') {
    if (path === '/auth/session' && !user) return json({ detail: 'No autenticado' }, 401)
    const hit = req.headers.get('X-Demo-User') !== null ? await lookup(user, path, url.search)
      : (await lookup(lastUser, path, url.search)) || (await lookupAny(path, url.search))
    if (hit) return answer(hit)
    return json({ detail: 'Esta vista no está disponible en la demo pública.' }, 404)
  }
  if (path === '/auth/login') {
    const body = await req.json().catch(() => ({}))
    const idx = await getIndex()
    const u = idx.users[(body.email || '').toLowerCase()]
    if (!u) return json({ detail: 'En la demo use los accesos rápidos de esta pantalla.' }, 401)
    lastUser = body.email.toLowerCase()
    return json({ user: u.user })
  }
  if (path === '/auth/logout') { lastUser = ''; return json({ ok: true }) }
  if (path === '/forensics/validate-id') return json(validateId(await req.json().catch(() => ({}))))
  if (path === '/public/contact') return json({ detail: 'En la demo el formulario no envía mensajes. Use «Solicitar una demostración guiada».' }, 403)
  return json({ detail: READ_ONLY }, 403)
}

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url)
  if (url.origin !== self.location.origin || !url.pathname.startsWith(SCOPE)) return
  if (url.pathname.startsWith(API)) { e.respondWith(handleApi(e.request, url)); return }
  // Navegación dentro de la SPA: siempre index.html (GitHub Pages no conoce las rutas internas)
  const last = url.pathname.split('/').pop()
  if (e.request.mode === 'navigate' && !last.includes('.')) {
    e.respondWith(fetch(SCOPE + 'index.html', { cache: 'no-cache' }))
  }
})
