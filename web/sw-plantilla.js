// Service worker de Milpa Resiliente: que el sitio abra sin señal en un teléfono donde ya se abrió con señal.
// vite.config.js (plugin «sin-senal») escribe dist/sw.js a partir de esta plantilla: pone en VERSION un hash de
// los archivos del build, de los datos y del audio publicados, y en PRECARGA la lista de la primera pantalla.
//
// Dos cachés:
// - APP (con la versión en el nombre): la página y los archivos del build. Un despliegue nuevo la reemplaza.
// - DATOS (sin versión): datos, audio, subtítulos, capas y relieve. Un despliegue NO la borra: lo que la
//   persona guardó con el botón del kit sigue ahí. Al instalarse una versión nueva con señal, lo guardado
//   de data/ y audio/ se vuelve a bajar para que el audio diga lo mismo que los datos.
//
// - La página (navegación) y los datos (data/): primero la red, pero con un plazo de 3.5 s: con una rayita
//   de señal que no carga, sale la copia guardada en vez de una pantalla en blanco. Si la red responde
//   después, la copia se actualiza por detrás.
// - Archivos del build (assets/, con hash en el nombre): primero la copia guardada.
// - Capas y relieve (capas/, terreno/): la copia guardada al instante y, si hay red, se actualiza por detrás.
// - Audio (audio/): solo lo que el botón «Guardar para usar sin señal» guardó a pedido de la persona.
//   La primera pantalla no descarga audio (docs/peso.md); aquí tampoco se baja por su cuenta.
//   El <audio> pide rangos de bytes: se responden cortando la copia completa (206).
// - Nada de otros sitios (mapa base, Sentinel-2): pasa directo a la red y no se guarda.
const VERSION = '__VERSION__'
const APP = `milpa-app-${VERSION}`
const DATOS = 'milpa-datos'
const PRECARGA = __PRECARGA__
const PLAZO_MS = 3500
// Algunos servidores responden con «Vary: Origin» y el navegador pide los módulos con cabecera Origin: sin
// ignoreVary la copia guardada no se reconoce.
const COMO = { ignoreVary: true }

const ruta = (url) => url.pathname.slice(new URL(self.registration.scope).pathname.length)

// Con señal, vuelve a bajar lo guardado de data/ y audio/. Sin señal se deja como está.
async function refrescarGuardado() {
  const c = await caches.open(DATOS)
  for (const req of await c.keys()) {
    const r = ruta(new URL(req.url))
    if (!r.startsWith('data/') && !r.startsWith('audio/')) continue
    try {
      const nueva = await fetch(new Request(req.url, { cache: 'reload' }))
      if (nueva.ok && nueva.status === 200) await c.put(req.url, nueva)
    } catch {
      return
    }
  }
}

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches
      .open(APP)
      .then((c) => c.addAll(PRECARGA))
      .then(() => refrescarGuardado())
      .then(() => self.skipWaiting()),
  )
})

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches
      .keys()
      .then((ks) => Promise.all(ks.filter((k) => k.startsWith('milpa-') && k !== APP && k !== DATOS).map((k) => caches.delete(k))))
      .then(() => self.clients.claim()),
  )
})

function conPlazo(promesa, ms) {
  return new Promise((resolve, reject) => {
    const reloj = setTimeout(() => reject(new Error('plazo')), ms)
    promesa.then(
      (r) => {
        clearTimeout(reloj)
        resolve(r)
      },
      (err) => {
        clearTimeout(reloj)
        reject(err)
      },
    )
  })
}

// Primero la red, con plazo; sin respuesta a tiempo, la copia guardada; sin copia, se espera a la red.
function redConPlazo(req, e, cache, buscar) {
  const red = fetch(req).then(async (r) => {
    if (r.ok && r.status === 200) await (await caches.open(cache)).put(req, r.clone())
    return r
  })
  e.waitUntil(red.catch(() => null))
  return conPlazo(red, PLAZO_MS).catch(async () => (await buscar()) || red)
}

async function primeroGuardado(req) {
  const guardado = await caches.match(req, COMO)
  if (guardado) return guardado
  const r = await fetch(req)
  if (r.ok && r.status === 200) await (await caches.open(APP)).put(req, r.clone())
  return r
}

async function guardadoYActualiza(req, e) {
  const guardado = await caches.match(req, COMO)
  const red = fetch(req)
    .then(async (r) => {
      if (r.ok && r.status === 200) await (await caches.open(DATOS)).put(req, r.clone())
      return r
    })
    .catch(() => null)
  if (guardado) {
    e.waitUntil(red)
    return guardado
  }
  return (await red) || Response.error()
}

async function audio(req) {
  const guardado = await (await caches.open(DATOS)).match(req.url, COMO)
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
  if (url.origin !== self.location.origin) return
  if (req.mode === 'navigate') {
    return e.respondWith(
      redConPlazo(req, e, APP, async () => {
        const c = await caches.open(APP)
        return (await c.match(req, { ignoreSearch: true, ignoreVary: true })) || (await c.match('./', COMO))
      }),
    )
  }
  const r = ruta(url)
  if (r.startsWith('assets/')) return e.respondWith(primeroGuardado(req))
  if (r.startsWith('audio/')) return e.respondWith(audio(req))
  if (r.startsWith('data/')) return e.respondWith(redConPlazo(req, e, DATOS, () => caches.match(req, COMO)))
  if (r.startsWith('capas/') || r.startsWith('terreno/') || r === 'manifest.webmanifest' || r.startsWith('icono')) {
    return e.respondWith(guardadoYActualiza(req, e))
  }
})

// El kit pide guardar una parcela: la página (en APP) y su JSON, el audio corto y los subtítulos (en DATOS).
// Responde cuántos bytes guardó.
self.addEventListener('message', (e) => {
  const d = e.data || {}
  if (d.tipo !== 'guardar' || !Array.isArray(d.urls) || !e.ports[0]) return
  const puerto = e.ports[0]
  const pagina = new URL(self.registration.scope).href
  e.waitUntil(
    (async () => {
      let bytes = 0
      try {
        for (const u of d.urls) {
          const r = await fetch(new Request(u, { cache: 'reload' }))
          if (!r.ok || r.status !== 200) throw new Error(`${u} (${r.status})`)
          const copia = r.clone()
          bytes += (await r.arrayBuffer()).byteLength
          await (await caches.open(u === pagina ? APP : DATOS)).put(u, copia)
        }
        puerto.postMessage({ ok: true, bytes })
      } catch (err) {
        puerto.postMessage({ ok: false, error: String(err && err.message ? err.message : err) })
      }
    })(),
  )
})
