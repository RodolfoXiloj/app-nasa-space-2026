// Línea de julio-agosto 2026 en la primera pantalla: el porcentaje de la mediana 1991-2025 de la lluvia
// de esa parcela, tal como lo trae data/validacion.json (observacion_2026.lluvia_chirps, de
// pipeline/validacion/validar.py). Aquí no se calcula nada: se lee la cifra y se dice de dónde sale.
// Es una observación, no un pronóstico, y lo dice con palabras. Sin color de aviso.
// Llega con import() después de pintar, como el kit y Escuchar: el JS inicial no crece. Los textos viven
// aquí y no en textos.js por la misma razón.
import { useEffect, useState } from 'react'

const TEXTOS = {
  en: {
    titulo: 'July and August 2026',
    cifra: (pct, ref) => `Rain was ${pct} % of normal (median ${ref}), according to CHIRPS. Preliminary.`,
    nota: 'Observed, not a forecast.',
  },
  es: {
    titulo: 'Julio y agosto de 2026',
    cifra: (pct, ref) => `Llovió el ${pct} % de lo normal (mediana ${ref}), según CHIRPS. Dato preliminar.`,
    nota: 'Observado, no es un pronóstico.',
  },
}

// Un solo pedido por visita, aunque se cambie de parcela o de idioma.
let pedido = null
const cargar = () => {
  if (!pedido) {
    pedido = fetch(import.meta.env.BASE_URL + 'data/validacion.json')
      .then((r) => (r.ok ? r.json() : null))
      .catch(() => null)
  }
  return pedido
}

export default function Linea2026({ pid, idioma }) {
  const [filas, setFilas] = useState(null)
  useEffect(() => {
    let vigente = true
    cargar().then((j) => {
      const obs = (j && j.observacion_2026) || {}
      if (vigente) setFilas(obs.lluvia_chirps || [])
    })
    return () => {
      vigente = false
    }
  }, [])

  const fila = (filas || []).find((x) => x.id === pid)
  // Sin la cifra (archivo que no llegó o parcela que no está) no se muestra nada: no se adivina.
  if (!fila || typeof fila.pct_de_la_mediana !== 'number' || !fila.periodo_referencia) return null
  const t = TEXTOS[idioma] || TEXTOS.es
  return (
    <p className="agr-linea2026" lang={idioma} data-linea2026={pid} data-pct={fila.pct_de_la_mediana}>
      <strong className="agr-linea2026-titulo">{t.titulo}.</strong>{' '}
      <span className="agr-linea2026-cifra">{t.cifra(fila.pct_de_la_mediana, fila.periodo_referencia)}</span>{' '}
      <em className="agr-linea2026-nota">{t.nota}</em>
    </p>
  )
}
