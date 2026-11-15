import { useId } from 'react'
import { COBERTURA, INICIALES, frases } from './textos.js'

// Rueda de 12 gajos, uno por mes, enero arriba y en el sentido del reloj (idea A7 del plan).
// Cada gajo dice cómo vio el satélite el suelo ese mes, sin depender del color:
//   desnudo  → relleno sólido
//   poca     → rayado en diagonal
//   cubierto → blanco con borde
// Los meses llegan por props desde `farmer.hechos[suelo].meses` y `.meses_poca_cobertura` (1 = enero).

const MESES_ANIO = 12
const C = 120 // centro del viewBox de 240
const R_EXT = 92
const R_INT = 50
const R_LETRA = 108
const HUECO = 1.6 // grados entre gajos

const rad = (g) => ((g - 90) * Math.PI) / 180
const punto = (r, g) => [C + r * Math.cos(rad(g)), C + r * Math.sin(rad(g))]
const f = (n) => n.toFixed(2)

function gajo(i) {
  const a0 = i * 30 + HUECO / 2
  const a1 = (i + 1) * 30 - HUECO / 2
  const [x0, y0] = punto(R_EXT, a0)
  const [x1, y1] = punto(R_EXT, a1)
  const [x2, y2] = punto(R_INT, a1)
  const [x3, y3] = punto(R_INT, a0)
  return `M${f(x0)} ${f(y0)}A${R_EXT} ${R_EXT} 0 0 1 ${f(x1)} ${f(y1)}L${f(x2)} ${f(y2)}A${R_INT} ${R_INT} 0 0 0 ${f(x3)} ${f(y3)}Z`
}

const limpiar = (meses) =>
  [...new Set((meses ?? []).map(Number).filter((m) => Number.isInteger(m) && m >= 1 && m <= MESES_ANIO))].sort((a, b) => a - b)

export function estadoMes(mes, desnudos, poca) {
  if (desnudos.includes(mes)) return 'desnudo'
  if (poca.includes(mes)) return 'poca'
  return 'cubierto'
}

function Muestra({ tipo, patron }) {
  return (
    <svg viewBox="0 0 20 20" width="20" height="20" aria-hidden="true" focusable="false">
      <rect x="1.5" y="1.5" width="17" height="17" rx="2" {...rellenoGajo(tipo, patron)} stroke="currentColor" strokeWidth="2" />
    </svg>
  )
}

function rellenoGajo(tipo, patron) {
  if (tipo === 'desnudo') return { fill: 'var(--picto-desnudo, currentColor)' }
  if (tipo === 'poca') return { fill: `url(#${patron})` }
  return { fill: 'var(--picto-cubierto, #fff)' }
}

/**
 * @param {number[]} desnudos  meses con suelo desnudo (1-12)
 * @param {number[]} poca      meses con poca cobertura (1-12); si un mes está en los dos, cuenta como desnudo
 * @param {boolean}  sinDatos  el satélite no vio bien: gajos punteados y «?» en el centro, sin adivinar
 */
export function RuedaMeses({ desnudos, poca, lang = 'es', size = 240, leyenda = true, sinDatos = false, className }) {
  const id = useId()
  const patron = `${id}-raya`
  const d = limpiar(desnudos)
  const p = limpiar(poca).filter((m) => !d.includes(m))
  const titulo = sinDatos
    ? (lang === 'en' ? "The satellite can't see well here" : 'El satélite no ve bien aquí')
    : frases.rueda(lang, d, p, MESES_ANIO)

  return (
    <figure className={className} style={{ margin: 0, display: 'inline-flex', flexDirection: 'column', alignItems: 'center', gap: 8 }}>
      <svg viewBox="0 0 240 240" width={size} height={size} role="img" aria-label={titulo} data-picto="ruedaMeses">
        <defs>
          <pattern id={patron} width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
            <rect width="7" height="7" fill="var(--picto-cubierto, #fff)" />
            <path d="M0 0v7" stroke="var(--picto-poca, currentColor)" strokeWidth="3.2" />
          </pattern>
        </defs>
        {INICIALES[lang].map((letra, i) => {
          const mes = i + 1
          const tipo = sinDatos ? 'cubierto' : estadoMes(mes, d, p)
          const [lx, ly] = punto(R_LETRA, i * 30 + 15)
          return (
            <g key={mes} data-mes={mes} data-estado={sinDatos ? 'sin-datos' : tipo}>
              <path
                d={gajo(i)}
                {...rellenoGajo(tipo, patron)}
                stroke="currentColor"
                strokeWidth="2.5"
                strokeLinejoin="round"
                strokeDasharray={sinDatos ? '5 5' : undefined}
              />
              <text
                x={f(lx)}
                y={f(ly)}
                textAnchor="middle"
                dominantBaseline="central"
                fontSize="15"
                fontWeight={tipo === 'cubierto' ? 500 : 800}
                fill="currentColor"
                aria-hidden="true"
              >
                {letra}
              </text>
            </g>
          )
        })}
        <g aria-hidden="true" fill="currentColor" textAnchor="middle">
          <text x={C} y={C - 2} fontSize="40" fontWeight="800" dominantBaseline="central">
            {sinDatos ? '?' : d.length}
          </text>
          {!sinDatos && (
            <text x={C} y={C + 26} fontSize="12" dominantBaseline="central">
              {frases.ruedaCentro(lang, MESES_ANIO)}
            </text>
          )}
        </g>
      </svg>
      {leyenda && !sinDatos && (
        <figcaption style={{ fontSize: '0.95rem' }}>
          <ul style={{ listStyle: 'none', margin: 0, padding: 0, display: 'flex', flexWrap: 'wrap', gap: '6px 14px', justifyContent: 'center' }}>
            {['desnudo', 'poca', 'cubierto'].map((tipo) => (
              <li key={tipo} style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}>
                <Muestra tipo={tipo} patron={patron} />
                {COBERTURA[tipo][lang]}
              </li>
            ))}
          </ul>
        </figcaption>
      )}
    </figure>
  )
}
