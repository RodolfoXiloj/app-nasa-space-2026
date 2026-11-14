// Botón «Escuchar / Listen»: el audio corto por frases del motor (motor/audio_frases.py) con subtítulos
// en el idioma activo. `farmer.audio` trae `es` y, si existe, `en`; si en inglés no hay mp3, suena el de español.
// El <audio> lleva preload="none" y la pista se pone al tocar el botón: la primera pantalla no descarga nada de audio.
import { useEffect, useRef, useState } from 'react'

// Textos del botón: viven aquí y no en textos.js porque este archivo llega con import() después de pintar.
const TEXTOS = {
  en: {
    boton: 'Listen',
    detalle: 'Short audio with subtitles',
    detalleVozEs: 'Short audio: Spanish voice, English subtitles',
    subtitulos: 'Subtitles',
    fallo: 'The audio did not load. Check the connection and try again.',
  },
  es: {
    boton: 'Escuchar',
    detalle: 'Audio corto, con subtítulos',
    detalleVozEs: 'Audio corto, con subtítulos',
    subtitulos: 'Subtítulos',
    fallo: 'No se cargó el audio. Revise la conexión e intente otra vez.',
  },
}

export default function Escuchar({ farmerAudio, idioma }) {
  const t = TEXTOS[idioma]
  const es = farmerAudio?.es
  const en = farmerAudio?.en
  const activo = idioma === 'en' && en?.mp3 ? en : es
  const audio = activo || es
  const ref = useRef(null)
  const [abierto, setAbierto] = useState(false)
  const [conSubtitulos, setConSubtitulos] = useState(true)
  const [frase, setFrase] = useState('')
  const [fallo, setFallo] = useState(false)
  const subtitulos = idioma === 'en'
    ? (activo?.subtitulos || es.subtitulos_en)
    : es.subtitulos
  const declaracionIa = (audio?.ia?.[idioma]?.declaracion) || audio?.ia?.declaracion

  useEffect(() => {
    const el = abierto && ref.current?.querySelector('track')
    if (!el) return
    const pista = el.track
    const alCambiar = () => setFrase(Array.from(pista.activeCues || [], (c) => c.text).join(' '))
    pista.mode = 'hidden'
    pista.addEventListener('cuechange', alCambiar)
    alCambiar()
    return () => pista.removeEventListener('cuechange', alCambiar)
  }, [abierto, subtitulos])

  // Al cambiar de idioma cambia el mp3: si estaba sonando, sigue con el del idioma nuevo.
  // La pausa que provoca el cambio de src no cuenta (llega con el src nuevo).
  const sonando = useRef(false)
  const srcSonando = useRef(null)
  const alSonar = () => {
    sonando.current = true
    srcSonando.current = ref.current.getAttribute('src')
  }
  const alPausar = () => {
    if (ref.current.getAttribute('src') === srcSonando.current) sonando.current = false
  }
  const mp3 = activo?.mp3 || es?.mp3
  useEffect(() => {
    if (sonando.current) ref.current?.play().catch(() => setFallo(true))
  }, [mp3])

  function tocar() {
    const a = ref.current
    setAbierto(true)
    setFallo(false)
    a.play().catch(() => setFallo(true))
  }

  if (!es?.mp3) return null

  const base = import.meta.env.BASE_URL

  return (
    <div className="agr-escuchar">
      <button type="button" className="agr-boton agr-escuchar-boton" aria-controls="agr-audio" onClick={tocar}>
        <svg viewBox="0 0 32 32" aria-hidden="true">
          <path d="M3 12h6l8-7v22l-8-7H3z" />
          <path d="M21 11a7 7 0 0 1 0 10m4-14a12 12 0 0 1 0 18" />
        </svg>
        <span>
          <b>{t.boton}</b>
          <small>{idioma === 'en' && !(en && en.mp3) ? t.detalleVozEs : t.detalle}</small>
        </span>
      </button>
      <audio id="agr-audio" ref={ref} src={base + mp3} preload="none" controls aria-label={t.boton} hidden={!abierto} onPlay={alSonar} onPause={alPausar}>
        {abierto && (
          <track key={subtitulos} kind="subtitles" src={base + subtitulos} srcLang={idioma} label={t.subtitulos} default />
        )}
      </audio>
      {abierto && (
        <>
          {conSubtitulos && (
            <p className="agr-subtitulos" lang={idioma} aria-live="polite">
              {frase}
            </p>
          )}
          <button type="button" className="agr-boton agr-boton--linea" aria-pressed={conSubtitulos} onClick={() => setConSubtitulos(!conSubtitulos)}>
            {t.subtitulos}
          </button>
          {declaracionIa && <p className="agr-nota">{declaracionIa}</p>}
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