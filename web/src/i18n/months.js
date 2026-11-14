import { messages } from './messages.js'
import { getLocale } from './store.js'

export function listaMesesI18n(ms, loc = getLocale()) {
  const dict = messages[loc] || messages.en
  const n = [...ms].sort((a, b) => a - b).map((m) => dict.mesLargo[m - 1])
  if (!n.length) return dict.common.monthsNone
  if (n.length === 1) return n[0]
  const y = loc === 'es' ? ' y ' : ' and '
  return n.slice(0, -1).join(', ') + y + n[n.length - 1]
}

export function mesCorto(mes, loc = getLocale()) {
  const dict = messages[loc] || messages.en
  return dict.mesCorto[mes - 1]
}