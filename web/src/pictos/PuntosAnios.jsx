import { useId } from 'react'
import { frases } from './textos.js'

// Años como puntos (idea A7 del plan): «3 de 15 años» son 15 puntos y 3 llevan una llama.
// El mismo componente sirve para la quema (15 años de FIRMS) y la canícula (25 años de lluvia diaria).
// Los años marcados van primero, en un disco negro con el dibujo en blanco; los demás son un aro.
// No se dice qué año fue cuál: el contrato solo trae el conteo.
// Datos por props desde `farmer.hechos[quema|canicula].valor` y `.de`.

// Dibujos del marcador en una celda de 24 × 24 centrada en 0,0. Blanco sobre el disco.
const MARCAS = {
  quema: (
    <>
      <path d="M0-9c1 3 6 6 6 12a6 6 0 0 1-12 0c0-3 1.5-5 3-6.5 0 2.5 1 4 2.5 4C-1.5 0-1-4.5 0-9z" fill="var(--picto-fondo, #fff)" />
    </>
  ),
  canicula: (
    <>
      <circle r="3.6" fill="var(--picto-fondo, #fff)" />
      <path
        d="M0-9v2.5M0 6.5V9M-9 0h2.5M6.5 0H9M-6.4-6.4l1.8 1.8M4.6 4.6l1.8 1.8M-6.4 6.4l1.8-1.8M4.6-4.6l1.8-1.8"
        stroke="var(--picto-fondo, #fff)"
        strokeWidth="2"
        strokeLinecap="round"
      />
    </>
  ),
}

const PASO = 28
const RADIO = 12

/**
 * @param {'quema'|'canicula'} tipo
 * @param {number} marcados  años en que el satélite vio el hecho
 * @param {number} total     años observados
 * @param {number} columnas  puntos por fila (5 da filas de 5 años, fáciles de contar)
 */
export function PuntosAnios({ tipo, marcados, total, columnas = 5, lang = 'es', size = 28, leyenda = true, className }) {
  const id = useId()
  const n = Number.isInteger(total) && total > 0 ? total : 0
  const m = Math.min(Math.max(Number.isInteger(marcados) ? marcados : 0, 0), n)
  const cols = Math.min(columnas, Math.max(n, 1))
  const filas = Math.ceil(n / cols) || 1
  const ancho = cols * PASO
  const alto = filas * PASO
  const escala = size / PASO
  const titulo = frases.anios(lang, tipo, m, n)

  return (
    <figure className={className} style={{ margin: 0, display: 'inline-flex', flexDirection: 'column', alignItems: 'flex-start', gap: 6 }}>
      <svg
        viewBox={`0 0 ${ancho} ${alto}`}
        width={ancho * escala}
        height={alto * escala}
        role="img"
        aria-labelledby={`${id}-t`}
        data-picto={`puntos-${tipo}`}
        data-marcados={m}
        data-total={n}
      >
        <title id={`${id}-t`}>{titulo}</title>
        {Array.from({ length: n }, (_, i) => {
          const x = (i % cols) * PASO + PASO / 2
          const y = Math.floor(i / cols) * PASO + PASO / 2
          const marcado = i < m
          return (
            <g key={i} transform={`translate(${x} ${y})`} data-marcado={marcado || undefined}>
              {marcado ? (
                <>
                  <circle r={RADIO} fill="var(--picto-marca, currentColor)" />
                  {MARCAS[tipo]}
                </>
              ) : (
                <circle r={RADIO - 4} fill="none" stroke="currentColor" strokeWidth="2" />
              )}
            </g>
          )
        })}
      </svg>
      {leyenda && (
        <figcaption style={{ fontSize: '0.95rem', maxWidth: '22rem' }}>
          {titulo}
        </figcaption>
      )}
    </figure>
  )
}
