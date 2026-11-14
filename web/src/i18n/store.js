const STORAGE_KEY = 'milpa-locale'
const DEFAULT_LOCALE = 'en'

let locale = DEFAULT_LOCALE
const listeners = new Set()

function readStored() {
  try {
    const v = localStorage.getItem(STORAGE_KEY)
    if (v === 'en' || v === 'es') return v
  } catch {
    /* private mode */
  }
  return DEFAULT_LOCALE
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