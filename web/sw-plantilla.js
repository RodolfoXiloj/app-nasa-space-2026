// Service worker de Milpa Resiliente: que el sitio abra sin señal en un teléfono donde ya se abrió con señal.
// vite.config.js (plugin «sin-senal») escribe dist/sw.js a partir de esta plantilla: pone en VERSION un hash de
// los archivos del build y en PRECARGA la lista de archivos de la primera pantalla.
//
// - La página (navegación): primero la red; sin red, la copia guardada.
// - Archivos del build (assets/, con hash en el nombre): primero la copia guardada.
// - Datos y capas (data/, capas/): la copia guardada al instante y, si hay red, se actualiza por detrás.
// - Audio (audio/): solo lo que el botón «Guardar para usar sin señal» del kit guardó a pedido de la persona.
//   La primera pantalla no descarga audio (docs/peso.md); aquí tampoco se baja por su cuenta.
//   El <audio> pide rangos de bytes: se responden cortando la copia completa (206).
// - Nada de otros sitios (mapa base, Sentinel-2): pasa directo a la red y no se guarda.
const VERSION = '__VERSION__'
const CACHE = `milpa-${VERSION}`
const PRECARGA = __PRECARGA__

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches
      .open(CACHE)
      .then((c) => c.addAll(PRECARGA))
      .then(() => self.skipWaiting()),
  )
})

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches
      .keys()
      .then((ks) => Promise.all(ks.filter((k) => k.startsWith('milpa-') && k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim()),
  )
})

const mismoSitio = (url) => url.origin === self.location.origin
const ruta = (url) => url.pathname.slice(new URL(self.registration.scope).pathname.length)
// Algunos servidores responden con «Vary: Origin» y el navegador pide los módulos con cabecera Origin: sin
// ignoreVary la copia guardada no se reconoce.
const COMO = { ignoreVary: true }

async function deRed(req, guardar) {
  const r = await fetch(req)
  if (guardar && r.ok && r.status === 200) {
    const c = await caches.open(CACHE)
    await c.put(req, r.clone())
  }
  return r
}

async function pagina(req) {
  try {
    return await deRed(req, true)
  } catch {
    const c = await caches.open(CACHE)
    return (await c.match(req, { ignoreSearch: true, ignoreVary: true })) || (await c.match('./', COMO)) || Response.error()
  }
}

async function primeroGuardado(req) {
  const c = await caches.open(CACHE)
  return (await c.match(req, COMO)) || deRed(req, true)
}

async function guardadoYActualiza(req, e) {
  const c = await caches.open(CACHE)
  const guardado = await c.match(req, COMO)
  const red = deRed(req, true).catch(() => null)
  if (guardado) {
    e.waitUntil(red)
    return guardado
  }
  return (await red) || Response.error()
}

async function audio(req) {
  const c = await caches.open(CACHE)
  const guardado = await c.match(req.url, COMO)
  if (!guardado) return fetch(req)
  const rango = req.headers.get('range')
  if (!rango) return guardado
  const datos = await guardado.arrayBuffer()
  const m = /bytes=(\d*)-(\d*)/.exec(rango)
  const total = datos.byteLength
  let ini = m && m[1] ? Number(m[1]) : 0
  let fin = m && m[2] ? Number(m[2]) : total - 1
  if (m && !m[1] && m[2]) {
    ini = Math.max(0, total - Number(m[2]))
    fin = total - 1
  }
  fin = Math.min(fin, total - 1)
  if (ini > fin) return new Response(null, { status: 416, headers: { 'Content-Range': `bytes */${total}` } })
  return new Response(datos.slice(ini, fin + 1), {
    status: 206,
    headers: {
      'Content-Type': guardado.headers.get('Content-Type') || 'audio/mpeg',
      'Content-Range': `bytes ${ini}-${fin}/${total}`,
      'Content-Length': String(fin - ini + 1),
      'Accept-Ranges': 'bytes',
    },
  })
}

self.addEventListener('fetch', (e) => {
  const req = e.request
  if (req.method !== 'GET') return
  const url = new URL(req.url)
  if (!mismoSitio(url)) return
  if (req.mode === 'navigate') return e.respondWith(pagina(req))
  const r = ruta(url)
  if (r.startsWith('assets/')) return e.respondWith(primeroGuardado(req))
  if (r.startsWith('audio/')) return e.respondWith(audio(req))
  if (r.startsWith('data/') || r.startsWith('capas/') || r === 'manifest.webmanifest' || r.startsWith('icono')) {
    return e.respondWith(guardadoYActualiza(req, e))
  }
})

// El kit pide guardar una parcela: su JSON, el audio corto y los subtítulos. Responde cuántos bytes guardó.
self.addEventListener('message', (e) => {
  const d = e.data || {}
  if (d.tipo !== 'guardar' || !Array.isArray(d.urls) || !e.ports[0]) return
  const puerto = e.ports[0]
  e.waitUntil(
    (async () => {
      const c = await caches.open(CACHE)
      let bytes = 0
      try {
        for (const u of d.urls) {
          const r = await fetch(new Request(u, { cache: 'reload' }))
          if (!r.ok || r.status !== 200) throw new Error(`${u} (${r.status})`)
          const copia = r.clone()
          bytes += (await r.arrayBuffer()).byteLength
          await c.put(u, copia)
        }
        puerto.postMessage({ ok: true, bytes })
      } catch (err) {
        puerto.postMessage({ ok: false, error: String(err && err.message ? err.message : err) })
      }
    })(),
  )
})
