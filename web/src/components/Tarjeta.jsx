import { useEffect, useState } from 'react'
import { BASE, puntajes } from '../lib/datos.js'
import { listaMesesI18n } from '../i18n/months.js'
import { messages } from '../i18n/messages.js'
import { useLocale, useT } from '../i18n/useT.js'
import { leerMotor } from '../i18n/motor.js'

const HOY = /^(Lo que hace hoy|What you do today|What they do today):\s*/

// En inglés, las citas textuales en español van entre «…» dentro del texto del motor. Cada una se marca
// lang="es" como cita rotulada; la que sigue a «our translation:» ya es la traducción y queda en inglés.
function ConCitas({ txt, loc }) {
  if (loc === 'es' || !txt) return txt || null
  return txt.split(/(«[^»]*»)/).map((parte, i, partes) =>
    parte.startsWith('«') && !/translation:\s*$/.test(partes[i - 1] || '') ? (
      <span key={i} lang="es" className="cita">
        {parte}
      </span>
    ) : (
      parte
    ),
  )
}

function vozEspanol() {
  const voces = window.speechSynthesis?.getVoices() || []
  for (const pref of ['es-GT', 'es-MX', 'es-US', 'es-419', 'es-ES']) {
    const v = voces.find((x) => x.lang === pref || x.lang?.replace('_', '-') === pref)
    if (v) return v
  }
  return voces.find((x) => x.lang?.toLowerCase().startsWith('es')) || null
}

export default function Tarjeta({ res, lluvia, temp, prioridad }) {
  const t = useT()
  const loc = useLocale()
  const dict = messages[loc] || messages.en
  const [hablando, setHablando] = useState(false)
  const hayVoz = typeof window !== 'undefined' && 'speechSynthesis' in window
  useEffect(() => () => hayVoz && window.speechSynthesis.cancel(), [hayVoz])

  const p = res.parcela
  const d = res.deteccion
  const filas = res.rotaciones.map((r) => ({ r, pt: puntajes(res, r.id, lluvia, temp, prioridad) }))
  const mejor = filas.reduce((a, b) => (b.pt.total > a.pt.total ? b : a))

  let detalleSat = t('tarjeta.detalleOk')
  if (d.meses_desnudos.length) detalleSat = t('tarjeta.detalleBare', { meses: listaMesesI18n(d.meses_desnudos, loc) })
  else if (d.meses_poca_cobertura?.length) detalleSat = t('tarjeta.detalleLow', { meses: listaMesesI18n(d.meses_poca_cobertura, loc) })

  function escuchar() {
    if (!hayVoz) return
    window.speechSynthesis.cancel()
    const u = new SpeechSynthesisUtterance(res.audio.texto || res.texto_tarjeta)
    const v = vozEspanol()
    if (v) u.voice = v
    u.lang = v?.lang || 'es-MX'
    u.rate = 0.95
    u.onend = () => setHablando(false)
    u.onerror = () => setHablando(false)
    setHablando(true)
    window.speechSynthesis.speak(u)
  }

  function detener() {
    window.speechSynthesis?.cancel()
    setHablando(false)
  }

  // Textos del motor en el idioma activo (campos `en` del JSON); lo que falte va en español con lang="es".
  const m = (obj, campo) => leerMotor(obj, campo, loc)
  const lang = (x) => (x.txt && x.lang !== loc ? x.lang : undefined)
  const nombre = (r) => (m(r, 'nombre').txt || '').replace(HOY, '')
  const porQue = m(mejor.r, 'por_que')
  const zarc = m(res.zarc, 'texto')
  const notaZarc = m(res.zarc, 'nota_escenario')
  const aviso = m(res, 'aviso')
  const declaracion = m(res.audio.ia, 'declaracion').txt

  return (
    <section className="tarjeta-agricultor">
      <div className="tarjeta-acciones no-imprimir">
        <h2>{t('tarjeta.farmerCard')}</h2>
        <div>
          {res.audio.mp3 ? (
            <audio
              controls
              src={BASE + res.audio.mp3}
              aria-label={t('tarjeta.listenAria', { municipio: p.municipio })}
              title={declaracion || t('tarjeta.synthVoice')}
            />
          ) : (
            <button type="button" onClick={hablando ? detener : escuchar} disabled={!hayVoz}>
              {hablando ? t('tarjeta.stop') : t('tarjeta.listen')}
            </button>
          )}
          <button type="button" onClick={() => window.print()}>
            {t('tarjeta.print')}
          </button>
        </div>
        <p className="nota-ia">
          {res.audio.mp3 ? declaracion || t('tarjeta.synthVoice') : t('tarjeta.synthBrowser')}
        </p>
      </div>
      <div className="tarjeta">
        <header>
          <h3>{t('tarjeta.header', { municipio: p.municipio, depto: p.departamento })}</h3>
          <p>
            {t('tarjeta.parcelLine', {
              lat: p.lat,
              lon: p.lon,
              cultivo: nombre(res.rotaciones[0]),
              prioridad: dict.prioridad[prioridad],
              escenario: lluvia !== 0 || temp !== 0 ? t('tarjeta.escenario', { lluvia, temp }) : '',
            })}
          </p>
        </header>
        <p>
          <b>{t('panel.title')}:</b>{' '}
          {t('tarjeta.satellite', {
            detalle: detalleSat,
            ciclos: d.ciclos.mediana,
            quema: d.quemas.anios_con_quema,
            total: d.quemas.anios_observados,
          })}
        </p>
        <table className="tabla-tarjeta">
          <thead>
            <tr>
              <th>{t('tarjeta.colOption')}</th>
              <th>{t('tarjeta.colWater')}</th>
              <th>{t('tarjeta.colSoil')}</th>
              <th>{t('tarjeta.colPests')}</th>
              <th>{t('tarjeta.colTotal')}</th>
              <th>{t('tarjeta.colConfidence')}</th>
            </tr>
          </thead>
          <tbody>
            {filas.map(({ r, pt }) => (
              <tr key={r.id} className={r.id === mejor.r.id ? 'fila-mejor' : ''}>
                <td>
                  <small>{dict.tipo[r.tipo]}</small>
                  <br />
                  {nombre(r)}
                </td>
                <td className="num">{pt.agua}</td>
                <td className="num">{pt.suelo}</td>
                <td className="num">{pt.plagas}</td>
                <td className="num">
                  <b>{pt.total}</b>
                </td>
                <td>{t(`a11y.nivel.${r.confianza.nivel}`)}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <p>
          <b>{t('tarjeta.whyBest')}</b> <span lang={lang(porQue)}>{porQue.txt}</span>
        </p>
        <p>
          <b>{t('tarjeta.planting')}</b>{' '}
          <span lang={lang(zarc)}>
            <ConCitas txt={zarc.txt} loc={lang(zarc) || loc} />
          </span>{' '}
          <span className="solo-imprimir">({res.zarc.enlace})</span>
          <a className="no-imprimir" href={res.zarc.enlace} target="_blank" rel="noreferrer">
            {t('common.seeZarc')}
          </a>
          <br />
          <small lang={lang(notaZarc)}>{notaZarc.txt}</small>
        </p>
        <p className="aviso-tarjeta" lang={lang(aviso)}>
          {aviso.txt}
        </p>
        <p className="fuentes-tarjeta">
          {t('tarjeta.sources', {
            nasa: res.fuentes
              .filter((f) => f.es_nasa)
              .map((f) => f.nombre.split(':')[0])
              .join(' · '),
          })}
        </p>
        <p className="fuentes-tarjeta ia-tarjeta">{t('app.ia')}</p>
      </div>
      <p className="nota no-imprimir">
        {t('tarjeta.audioNote', {
          prioridad: dict.prioridad[res.parcela.prioridad],
          offline: res.audio.mp3 ? '' : t('tarjeta.offlineVoice'),
        })}
      </p>
    </section>
  )
}