// Uso sin señal (dist/sw.js, escrito por vite.config.js desde sw-plantilla.js). Este archivo llega con el kit o
// con Evidence, después del primer pintado: la primera pantalla no crece.
// Solo en el build y en un contexto seguro (https o localhost); en otro caso no hace nada.
let registro = null

export function registrar() {
  if (registro) return registro
  const puede = import.meta.env.PROD && typeof navigator !== 'undefined' && 'serviceWorker' in navigator && window.isSecureContext
  registro = puede ? navigator.serviceWorker.register(import.meta.env.BASE_URL + 'sw.js').catch(() => null) : Promise.resolve(null)
  return registro
}

const absoluta = (ruta) => new URL(import.meta.env.BASE_URL + ruta, window.location.href).href

// La parcela guardada se recuerda en el teléfono, como el idioma: src/agricultor/Inicio.jsx la abre primero (con
// esta misma clave), así que sin señal abre la que sí está guardada aunque no sea la primera de la lista. Antes del
// 15 nov 2026 la página siempre abría Jocotán y, sin señal, otra parcela guardada no se veía.
export function recordarParcela(id) {
  try {
    localStorage.setItem('milpa-parcela', id)
  } catch {
    /* modo privado: abre la primera parcela, como antes */
  }
}

// Lo que hace falta para abrir esta parcela sin señal: la página, el índice, su JSON, la línea de 2026, el audio
// corto en el idioma elegido y sus subtítulos. El resto de la primera pantalla ya lo guardó el service worker.
export function urlsParcela({ parcela, farmer, idioma }) {
  const a = (farmer && farmer.audio) || {}
  const es = a.es || {}
  const en = a.en || {}
  const voz = (idioma === 'en' && en.mp3 ? en : es).mp3
  const rutas = ['', 'data/parcelas.json', 'data/validacion.json', parcela && parcela.archivos && parcela.archivos.maiz_frijol, voz,
    es.subtitulos, es.subtitulos_en, en.subtitulos, en.subtitulos_es]
  return [...new Set(rutas.filter((r) => typeof r === 'string'))].map(absoluta)
}

export async function guardar(urls) {
  const reg = await Promise.race([registrar(), new Promise((r) => setTimeout(() => r(null), 8000))])
  if (!reg) return { ok: false, error: 'sin service worker' }
  const listo = await Promise.race([navigator.serviceWorker.ready, new Promise((r) => setTimeout(() => r(null), 15000))])
  const sw = listo && listo.active
  if (!sw) return { ok: false, error: 'sin service worker activo' }
  return new Promise((resolve) => {
    const canal = new MessageChannel()
    const reloj = setTimeout(() => resolve({ ok: false, error: 'tiempo' }), 90000)
    canal.port1.onmessage = (e) => {
      clearTimeout(reloj)
      resolve(e.data || { ok: false })
    }
    sw.postMessage({ tipo: 'guardar', urls }, [canal.port2])
  })
}
