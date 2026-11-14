// Botón «Escuchar / Listen»: el audio corto por frases del motor (motor/audio_frases.py) con subtítulos
// en el idioma activo. El mp3 y los .vtt llegan en `farmer.audio.es` del JSON (la voz es en español; en
// inglés van los subtítulos en inglés). El <audio> lleva preload="none" y la pista se pone al tocar el
// botón: la primera pantalla no descarga nada de audio. El botón reproduce; pausar y adelantar van en los
// controles del <audio>, que aparecen al primer toque. Un <audio> no dibuja subtítulos (solo <video>), así
// que la pista va en modo «hidden» y la frase activa se escribe debajo del botón, visible por defecto.
import { useEffect, useRef, useState } from 'react'
import { TEXTOS } from './textos.js'

export default function Escuchar({ audio, idioma }) {
  const t = TEXTOS[idioma].escuchar
  const ref = useRef(null)
  const [abierto, setAbierto] = useState(false)
  const [conSubtitulos, setConSubtitulos] = useState(true)
  const [frase, setFrase] = useState('')
  const [fallo, setFallo] = useState(false)
  const vtt = idioma === 'en' ? audio.subtitulos_en : audio.subtitulos
  const ia = (audio.ia || {})[idioma] || {}

  // La pista del idioma activo: al cambiar de idioma React pone otra <track> (key) y esto se vuelve a enganchar.
  useEffect(() => {
    const el = abierto && ref.current.querySelector('track')
    if (!el) return
    const pista = el.track
    const alCambiar = () => setFrase(Array.from(pista.activeCues || [], (c) => c.text).join(' '))
    pista.mode = 'hidden'
    pista.addEventListener('cuechange', alCambiar)
    alCambiar()
    return () => pista.removeEventListener('cuechange', alCambiar)
  }, [abierto, vtt])

  function tocar() {
    const a = ref.current
    setAbierto(true)
    setFallo(false)
    a.play().catch(() => setFallo(true))
  }

  const base = import.meta.env.BASE_URL
  return (
    <div className="agr-escuchar">
      <button type="button" className="agr-boton agr-escuchar-boton" aria-controls="agr-audio" onClick={tocar}>
        {/* Altavoz; el trazo y el tamaño van en agricultor.css */}
        <svg viewBox="0 0 32 32" aria-hidden="true">
          <path d="M3 12h6l8-7v22l-8-7H3z" />
          <path d="M21 11a7 7 0 0 1 0 10m4-14a12 12 0 0 1 0 18" />
        </svg>
        <span>
          <b>{t.boton}</b>
          <small>{t.detalle}</small>
        </span>
      </button>
      <audio id="agr-audio" ref={ref} src={base + audio.mp3} preload="none" controls hidden={!abierto}>
        {abierto && <track key={vtt} kind="subtitles" src={base + vtt} srcLang={idioma} label={t.subtitulos} default />}
      </audio>
      {abierto && (
        <>
          {conSubtitulos && (
            <p className="agr-subtitulos" lang={idioma}>
              {frase}
            </p>
          )}
          <button type="button" className="agr-boton agr-boton--linea" aria-pressed={conSubtitulos} onClick={() => setConSubtitulos(!conSubtitulos)}>
            {t.subtitulos}
          </button>
          {ia.declaracion && <p className="agr-nota">{ia.declaracion}</p>}
        </>
      )}
      {fallo && (
        <p className="agr-banda" role="alert">
          {t.fallo}
        </p>
      )}
    </div>
  )
}
