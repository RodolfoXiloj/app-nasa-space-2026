// Acceso a los JSON estáticos (contrato v1) y utilidades de presentación.
export const BASE = import.meta.env.BASE_URL

export async function cargarJSON(ruta) {
  const r = await fetch(BASE + ruta)
  if (!r.ok) throw new Error(`No se pudo leer ${ruta} (${r.status})`)
  return r.json()
}

export const MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
export const MESES_LARGOS = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto',
  'septiembre', 'octubre', 'noviembre', 'diciembre']

export const CULTIVOS = { maiz_frijol: 'Maíz + frijol', maiz_solo: 'Maíz solo', sorgo: 'Sorgo (maicillo)' }
export const PRIORIDADES = { agua: 'Ahorrar agua', suelo: 'Cuidar el suelo', plagas: 'Cortar plagas' }
export const TIPOS = {
  actual: 'Lo que hace hoy',
  leguminosa_cobertura: 'Leguminosa o cobertura',
  tolerante_sequia: 'Tolerante a sequía',
}
export const ESTADOS = {
  cultivo: 'Cultivo', cobertura: 'Cobertura viva', rastrojo: 'Rastrojo o vegetación', desnudo: 'Suelo desnudo', quema: 'Quema',
}

export function listaMeses(ms) {
  const n = [...ms].sort((a, b) => a - b).map((m) => MESES_LARGOS[m - 1])
  if (!n.length) return 'ninguno'
  if (n.length === 1) return n[0]
  return n.slice(0, -1).join(', ') + ' y ' + n[n.length - 1]
}

export function idEscenario(lluvia, temp) {
  return `lluvia_${lluvia}_temp_${temp}`
}

// Puntajes de una rotación en el escenario elegido, con el total re-ponderado según la prioridad.
export function puntajes(res, rotId, lluvia, temp, prioridad) {
  const esc = res.escenarios.lista.find((e) => e.id === idEscenario(lluvia, temp))
  const base = esc?.rotaciones?.[rotId]
  const p = base ? { ...base.puntajes } : { ...res.rotaciones.find((r) => r.id === rotId).puntajes }
  const w = res.pesos.por_prioridad[prioridad]
  p.total = Math.round(w.agua * p.agua + w.suelo * p.suelo + w.plagas * p.plagas)
  return { ...p, deficit: base?.deficit_mediano_pct }
}

export function fuente(res, id) {
  return res.fuentes.find((f) => f.id === id)
}
