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

// El mismo redondeo que round() de Python en motor/puntaje.py: un .5 exacto va al número par (84.5 -> 84).
// Math.round lo subiría (85) y la tarjeta mostraría otro total que el motor, el texto y el audio.
// Los pesos (0.25, 0.5) y los puntajes enteros dan sumas exactas en binario, así que el .5 se detecta sin error.
export function redondearComoPython(x) {
  const abajo = Math.floor(x)
  const resto = x - abajo
  if (resto === 0.5) return abajo % 2 === 0 ? abajo : abajo + 1
  return Math.round(x)
}

// Puntajes de una rotación en el escenario elegido, con el total re-ponderado según la prioridad.
export function puntajes(res, rotId, lluvia, temp, prioridad) {
  const esc = res.escenarios.lista.find((e) => e.id === idEscenario(lluvia, temp))
  const base = esc?.rotaciones?.[rotId]
  const p = base ? { ...base.puntajes } : { ...res.rotaciones.find((r) => r.id === rotId).puntajes }
  const w = res.pesos.por_prioridad[prioridad]
  p.total = redondearComoPython(w.agua * p.agua + w.suelo * p.suelo + w.plagas * p.plagas)
  return { ...p, deficit: base?.deficit_mediano_pct }
}

export function fuente(res, id) {
  return res.fuentes.find((f) => f.id === id)
}
