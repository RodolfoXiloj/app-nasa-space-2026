// G2: la canícula día por día, 2001-2025 (bloque `canicula` de data/explorar/{pid}.json). Una fila por año del
// 15 de junio al 31 de agosto: cuadro oscuro = día seco. Un interruptor cambia el reparto diario de CHIRPS: IMERG
// (el del motor) o ERA5 (para comparar). Las rachas son las del motor (motor/clima.py, racha_seca).
import { useState } from 'react'
import { useTx } from '../i18n/explorar.js'

const W = 6
const PASO = 7
const ALTO = 10
const FILA = 13
const IZQ = 34
const ARRIBA = 16
const MARCAS = [
  { i: 0, es: '15 jun', en: 'Jun 15' },
  { i: 16, es: '1 jul', en: 'Jul 1' },
  { i: 47, es: '1 ago', en: 'Aug 1' },
  { i: 77, es: '31 ago', en: 'Aug 31' },
]

export default function CaniculaDias({ explorar }) {
  const tx = useTx()
  const can = explorar?.canicula
  const [reparto, setReparto] = useState('sat')
  const [sel, setSel] = useState(null)
  if (!can?.sat?.length) return null
  const filas = can[reparto] || can.sat
  const umbral = can.umbral_racha_dias
  const largos = filas.filter((x) => x.racha_dias > umbral)
  const n = filas[0].dias.length
  const ancho = IZQ + n * PASO + 26
  const alto = ARRIBA + filas.length * FILA + 4
  const nombreReparto = tx(`canicula.${reparto}Corto`)
  const resumen = tx('canicula.resumen', { k: largos.length, n: filas.length, dias: umbral, reparto: nombreReparto })
  const elegido = filas.find((x) => x.anio === sel)
  return (
    <section className="panel explorar-panel" aria-labelledby="canicula-dias-titulo">
      <h2 id="canicula-dias-titulo">{tx('canicula.titulo')}</h2>
      <p className="sub">{tx('canicula.sub', { mm: can.umbral_dia_seco_mm, dias: umbral })}</p>
      {can.rnl && (
        <div className="selector-chips" role="group" aria-label={tx('canicula.reparto')}>
          {['sat', 'rnl'].map((k) => (
            <button key={k} type="button" aria-pressed={k === reparto} onClick={() => setReparto(k)}>
              {tx(`canicula.${k}`)}
            </button>
          ))}
        </div>
      )}
      <p className="resumen-grafica" aria-live="polite">{resumen}</p>
      <svg className="canicula-svg" viewBox={`0 0 ${ancho} ${alto}`} role="img" aria-label={resumen}>
        {MARCAS.map((m) => (
          <text key={m.i} x={IZQ + m.i * PASO} y={10} textAnchor={m.i > 60 ? 'end' : 'start'}>
            {m[tx.loc] || m.en}
          </text>
        ))}
        {filas.map((x, f) => {
          const y = ARRIBA + f * FILA
          const larga = x.racha_dias > umbral
          return (
            <g key={x.anio} className="fila" onClick={() => setSel(x.anio === sel ? null : x.anio)}>
              <text x={0} y={y + ALTO - 1} fontWeight={larga ? 700 : 400}>
                {x.anio}
              </text>
              {[...x.dias].map((c, i) => (
                <rect key={i} x={IZQ + i * PASO} y={y} width={W} height={ALTO} className={c === '1' ? 'dia-seco' : c === '0' ? 'dia-lluvia' : 'dia-nd'} />
              ))}
              {larga && <rect className="fila-larga" x={IZQ - 2} y={y - 1.5} width={n * PASO + 2} height={ALTO + 3} rx={2} />}
              {sel === x.anio && <rect className="fila-sel" x={IZQ - 3} y={y - 2.5} width={n * PASO + 4} height={ALTO + 5} rx={2} />}
              <text x={IZQ + n * PASO + 4} y={y + ALTO - 1} fontWeight={larga ? 700 : 400}>
                {x.racha_dias}
              </text>
            </g>
          )
        })}
      </svg>
      <ul className="leyenda-linea" aria-hidden="true">
        <li><svg width="12" height="12"><rect width="12" height="12" className="dia-seco" fill="#8a5a2b" /></svg>{tx('canicula.seco')}</li>
        <li><svg width="12" height="12"><rect width="12" height="12" fill="#dce8f2" stroke="#55624f" strokeWidth="0.5" /></svg>{tx('canicula.lluvia')}</li>
      </ul>
      {elegido && (
        <p className="resumen-grafica" aria-live="polite">
          {tx('canicula.anio', { anio: elegido.anio, racha: elegido.racha_dias })}
        </p>
      )}
      <details>
        <summary>{tx('canicula.tabla')}</summary>
        <ul className="canicula-anios">
          {filas.map((x) => (
            <li key={x.anio}>
              <button type="button" className={x.racha_dias > umbral ? 'larga' : ''} aria-pressed={sel === x.anio} onClick={() => setSel(x.anio === sel ? null : x.anio)}
                aria-label={tx('canicula.anio', { anio: x.anio, racha: x.racha_dias })}>
                {x.anio}: {x.racha_dias}
              </button>
            </li>
          ))}
        </ul>
      </details>
      <p className="nota">{tx('canicula.nota')}</p>
    </section>
  )
}
