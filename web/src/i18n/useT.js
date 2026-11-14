import { useMemo, useSyncExternalStore } from 'react'
import { messages } from './messages.js'
import { getLocale, subscribeLocale } from './store.js'

function getByPath(obj, path) {
  return path.split('.').reduce((o, k) => (o == null ? undefined : o[k]), obj)
}

function interpolate(str, vars) {
  if (!vars || typeof str !== 'string') return str
  return str.replace(/\{(\w+)\}/g, (_, k) => (vars[k] != null ? String(vars[k]) : `{${k}}`))
}

export function useLocale() {
  const loc = useSyncExternalStore(subscribeLocale, getLocale, () => DEFAULT_FALLBACK)
  return loc
}

const DEFAULT_FALLBACK = 'en'

export function useT() {
  const loc = useLocale()
  return useMemo(() => {
    const dict = messages[loc] || messages.en
    const fallback = messages.en
    return (key, vars) => {
      const raw = getByPath(dict, key) ?? getByPath(fallback, key) ?? key
      return interpolate(raw, vars)
    }
  }, [loc])
}

export function tStatic(key, loc, vars) {
  const dict = messages[loc] || messages.en
  const raw = getByPath(dict, key) ?? getByPath(messages.en, key) ?? key
  return interpolate(raw, vars)
}