import { useId } from 'react'
import { Satelite } from './iconos.jsx'
import { frases } from './textos.js'

// El píxel en medida local (idea A9 del plan): «el satélite ve un cuadro de unas 9 manzanas,
// no solo su parcela». El cuadro grande es un píxel; las celdas son manzanas; la rayada es una.
// Las dos medidas llegan por props: el lado del píxel (MODIS MOD13Q1: 250 m) y la superficie de una
// manzana en m² (la fuente y el valor van en docs/pictos.md). Aquí no hay cifras fijas.

const X0 = 34
const Y0 = 62
const LADO = 180

/**
 * @param {number} ladoPixelM    lado del píxel en metros
 * @param {number} m2PorManzana  superficie de una manzana en m²
 */
export function PixelManzanas({ ladoPixelM, m2PorManzana, lang = 'es', size = 240, leyenda = true, className }) {
  const id = useId()
  const patron = `${id}-raya`
  const valido = ladoPixelM > 0 && m2PorManzana > 0
  const area = valido ? ladoPixelM * ladoPixelM : 0
  const manzanas = valido ? area / m2PorManzana : 0
  const ha = area / 10000
  const n = Math.max(1, Math.round(Math.sqrt(manzanas)))
  const celda = LADO / n
  const centro = Math.floor(n / 2)
  const titulo = valido ? frases.pixel(lang, ladoPixelM, ha, manzanas) : ''
  const etiquetaLado = valido ? `${ladoPixelM.toLocaleString(lang === 'en' ? 'en-US' : 'es-GT')} m` : ''

  if (!valido) return null

  return (
    <figure className={className} style={{ margin: 0, display: 'inline-flex', flexDirection: 'column', alignItems: 'center', gap: 6 }}>
      <svg viewBox="0 0 240 262" width={size} height={(size * 262) / 240} role="img" aria-labelledby={`${id}-t`} data-picto="pixelManzanas" data-manzanas={manzanas.toFixed(2)}>
        <title id={`${id}-t`}>{titulo}</title>
        <defs>
          <pattern id={patron} width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
            <rect width="7" height="7" fill="var(--picto-cubierto, #fff)" />
            <path d="M0 0v7" stroke="currentColor" strokeWidth="3.2" />
          </pattern>
        </defs>
        {/* Lo que ve el satélite: líneas de mira hasta las esquinas del cuadro. */}
        <g stroke="currentColor" strokeWidth="1.5" strokeDasharray="4 5" fill="none">
          <path d={`M110 40L${X0} ${Y0}M130 40L${X0 + LADO} ${Y0}`} />
        </g>
        <svg x="96" y="0" width="48" height="48" overflow="visible">
          <Satelite decorativo />
        </svg>
        {/* Manzanas */}
        <g stroke="currentColor" fill="none">
          {Array.from({ length: n - 1 }, (_, i) => (
            <path key={i} d={`M${X0 + celda * (i + 1)} ${Y0}v${LADO}M${X0} ${Y0 + celda * (i + 1)}h${LADO}`} strokeWidth="1.5" strokeDasharray="6 4" />
          ))}
          <rect x={X0 + celda * centro} y={Y0 + celda * centro} width={celda} height={celda} fill={`url(#${patron})`} strokeWidth="2.5" />
          <rect x={X0} y={Y0} width={LADO} height={LADO} strokeWidth="4" />
        </g>
        {/* Medidas del píxel */}
        <g fill="currentColor" fontSize="14" fontWeight="700" textAnchor="middle" aria-hidden="true">
          <text x={X0 + LADO / 2} y={Y0 + LADO + 18}>{etiquetaLado}</text>
          <text x={X0 - 14} y={Y0 + LADO / 2} transform={`rotate(-90 ${X0 - 14} ${Y0 + LADO / 2})`}>{etiquetaLado}</text>
        </g>
      </svg>
      {leyenda && (
        <figcaption style={{ fontSize: '0.95rem', maxWidth: '22rem', textAlign: 'center' }}>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6, fontWeight: 700 }}>
            <svg viewBox="0 0 20 20" width="20" height="20" aria-hidden="true" focusable="false">
              <rect x="1.5" y="1.5" width="17" height="17" fill={`url(#${patron})`} stroke="currentColor" strokeWidth="2" />
            </svg>
            {frases.unaManzana(lang)}
          </span>
          <br />
          {titulo}
        </figcaption>
      )}
    </figure>
  )
}
