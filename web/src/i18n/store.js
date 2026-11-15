const STORAGE_KEY = 'milpa-locale'
const DEFAULT_LOCALE = 'en'

let locale = DEFAULT_LOCALE
const listeners = new Set()

// Lee una clave guardada en el teléfono: el idioma, y la parcela que se guardó para usar sin señal
// (src/agricultor/Inicio.jsx). En modo privado, sin localStorage, devuelve null.
export function guardado(clave) {
  try {
    return localStorage.getItem(clave)
  } catch {
    return null
  }
}

function readStored() {
  const v = guardado(STORAGE_KEY)
  return v === 'en' || v === 'es' ? v : DEFAULT_LOCALE
}

if (typeof window !== 'undefined') {
  locale = readStored()
  document.documentElement.lang = locale
}

export function getLocale() {
  return locale
}

export function setLocale(next) {
  if (next !== 'en' && next !== 'es') return
  locale = next
  try {
    localStorage.setItem(STORAGE_KEY, next)
  } catch {
    /* ignore */
  }
  if (typeof document !== 'undefined') document.documentElement.lang = next
  listeners.forEach((fn) => fn())
}

export function subscribeLocale(fn) {
  listeners.add(fn)
  return () => listeners.delete(fn)
}