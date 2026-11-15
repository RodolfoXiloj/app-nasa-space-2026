// Botón «Escuchar / Listen»: el audio corto por frases del motor (motor/audio_frases.py) con subtítulos
// en el idioma activo. `farmer.audio` trae `es` y, si existe, `en`; si en inglés no hay mp3, suena el de español.
// El <audio> lleva preload="none" y la pista se pone al tocar el botón: la primera pantalla no descarga nada de audio.
// Mientras suena, el hecho que nombra la voz (suelo, quema o canícula) se marca en su tarjeta (data-hablando): las
// frases de `farmer.frases` van en el mismo orden que los subtítulos en los dos idiomas. Debajo, un botón por
// hecho salta a su frase. Nada de esto mueve el foco.
import { useEffect, useRef, useState } from 'react'
import { TEXTOS as TEXTOS_VISTA } from './textos.js'

// Textos del botón: viven aquí y no en textos.js porque este archivo llega con import() después de pintar.
const TEXTOS = {
  en: {
    boton: 'Listen',
    detalle: 'Short audio with subtitles',
    detalleVozEs: 'Short audio: Spanish voice, English subtitles',
    subtitulos: 'Subtitles',
    fallo: 'The audio did not load. Check the connection and try again.',
    repetir: 'Hear one fact again',
  },
  es: {
    boton: 'Escuchar',
    detalle: 'Audio corto, con subtítulos',
    detalleVozEs: 'Audio corto, con subtítulos',
    subtitulos: 'Subtítulos',
    fallo: 'No se cargó el audio. Revise la conexión e intente otra vez.',
    repetir: 'Volver a escuchar un hecho',
  },
}

// Marca en la vista la tarjeta del hecho que se está leyendo (o ninguna). Si la tarjeta no se ve, la acerca sin
// mover el foco; con movimiento reducido, sin animación.
function marcarHecho(hecho) {
  document.querySelectorAll('.agr-lista-hechos [data-hecho]').forEach((el) => {
    const si = el.getAttribute('data-hecho') === hecho
    if (si && !el.hasAttribute('data-hablando')) {
      const r = el.getBoundingClientRect()
      if (r.top < 0 || r.bottom > window.innerHeight) {
        const quieto = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches
        el.scrollIntoView({ block: 'nearest', behavior: quieto ? 'auto' : 'smooth' })
      }
    }
    if (si) el.setAttribute('data-hablando', '')
    else el.removeAttribute('data-hablando')
  })
}

export default function Escuchar({ farmerAudio, idioma, frases = [] }) {
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
  const [suena, setSuena] = useState(false)
  const subtitulos = idioma === 'en'
    ? (activo?.subtitulos || es.subtitulos_en)
    : es.subtitulos
  const declaracionIa = (audio?.ia?.[idioma]?.declaracion) || audio?.ia?.declaracion

  useEffect(() => {
    const el = abierto && ref.current?.querySelector('track')
    if (!el) return
    const pista = el.track
    const alCambiar = () => {
      const activas = Array.from(pista.activeCues || [])
      setFrase(activas.map((c) => c.text).join(' '))
      const i = activas.length ? Array.from(pista.cues || []).indexOf(activas[0]) : -1
      marcarHecho(i >= 0 && frases[i] ? frases[i].hecho : null)
    }
    pista.mode = 'hidden'
    pista.addEventListener('cuechange', alCambiar)
    alCambiar()
    return () => {
      pista.removeEventListener('cuechange', alCambiar)
      marcarHecho(null)
    }
  }, [abierto, subtitulos])

  // Salta a la frase de un hecho: el inicio de su subtítulo (misma posición en la lista de frases).
  function irA(hecho) {
    const a = ref.current
    const i = frases.findIndex((x) => x.hecho === hecho)
    const pista = a && a.querySelector('track') && a.querySelector('track').track
    const cue = pista && pista.cues && pista.cues[i]
    if (!a || i < 0 || !cue) return
    a.currentTime = cue.startTime
    a.play().catch(() => setFallo(true))
  }
  const hechos = frases.filter((x) => x.hecho)

  // Al cambiar de idioma cambia el mp3: si estaba sonando, sigue con el del idioma nuevo.
  // La pausa que provoca el cambio de src no cuenta (llega con el src nuevo).
  const sonando = useRef(false)
  const srcSonando = useRef(null)
  const alSonar = () => {
    setSuena(true)
    sonando.current = true
    srcSonando.current = ref.current.getAttribute('src')
  }
  const alPausar = () => {
    if (ref.current.getAttribute('src') === srcSonando.current) sonando.current = false
    setSuena(false)
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
        <span className={`agr-ondas${suena ? ' agr-ondas--suena' : ''}`} aria-hidden="true">
          <i />
          <i />
          <i />
          <i />
        </span>
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
          {hechos.length > 0 && (
            <div className="agr-repetir" role="group" aria-label={t.repetir}>
              {hechos.map((x) => (
                <button key={x.id} type="button" className="agr-boton agr-boton--linea" onClick={() => irA(x.hecho)}>
                  {TEXTOS_VISTA[idioma].hechos[x.hecho]}
                </button>
              ))}
            </div>
          )}
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