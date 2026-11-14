import { useEffect, useState } from 'react'
import { BASE, PRIORIDADES, TIPOS, listaMeses, puntajes } from '../lib/datos.js'

function vozEspanol() {
  const voces = window.speechSynthesis?.getVoices() || []
  for (const pref of ['es-GT', 'es-MX', 'es-US', 'es-419', 'es-ES']) {
    const v = voces.find((x) => x.lang === pref || x.lang?.replace('_', '-') === pref)
    if (v) return v
  }
  return voces.find((x) => x.lang?.toLowerCase().startsWith('es')) || null
}

export default function Tarjeta({ res, lluvia, temp, prioridad }) {
  const [hablando, setHablando] = useState(false)
  const hayVoz = typeof window !== 'undefined' && 'speechSynthesis' in window
  useEffect(() => () => hayVoz && window.speechSynthesis.cancel(), [hayVoz])

  const p = res.parcela
  const d = res.deteccion
  const filas = res.rotaciones.map((r) => ({ r, pt: puntajes(res, r.id, lluvia, temp, prioridad) }))
  const mejor = filas.reduce((a, b) => (b.pt.total > a.pt.total ? b : a))

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

  return (
    <section className="tarjeta-agricultor">
      <div className="tarjeta-acciones no-imprimir">
        <h2>Tarjeta para el agricultor</h2>
        <div>
          {res.audio.mp3 ? (
            <audio
              controls
              src={BASE + res.audio.mp3}
              aria-label={`Escuchar la tarjeta de ${p.municipio} (voz sintética)`}
              title={res.audio.ia?.declaracion || 'Voz sintética generada con IA'}
            />
          ) : (
            <>
              <button type="button" onClick={hablando ? detener : escuchar} disabled={!hayVoz}>
                {hablando ? 'Detener' : 'Escuchar'}
              </button>
            </>
          )}
          <button type="button" onClick={() => window.print()}>
            Imprimir o guardar PDF
          </button>
        </div>
        <p className="nota-ia">
          {res.audio.mp3
            ? res.audio.ia?.declaracion || 'Voz sintética generada con IA (edge-tts). No es una persona.'
            : 'El botón «Escuchar» usa la voz sintética del navegador. No es una persona.'}
        </p>
      </div>
      <div className="tarjeta">
        <header>
          <h2>Milpa Resiliente · {p.municipio}, {p.departamento}</h2>
          <p>
            Parcela en {p.lat}, {p.lon} · cultivo de hoy: {res.rotaciones[0].nombre.replace('Lo que hace hoy: ', '')} ·
            prioridad: {PRIORIDADES[prioridad]}
            {lluvia !== 0 || temp !== 0 ? ` · escenario: lluvia ${lluvia} %, +${temp} °C` : ''}
          </p>
        </header>
        <p>
          <b>Lo que ve el satélite:</b>{' '}
          {d.meses_desnudos.length
            ? `suelo desnudo en ${listaMeses(d.meses_desnudos)}`
            : d.meses_poca_cobertura?.length
              ? `poca cobertura en ${listaMeses(d.meses_poca_cobertura)}`
              : 'no se ven meses con el suelo desnudo'}
          ; {d.ciclos.mediana} ciclo(s) de verdor por año; quema cercana en {d.quemas.anios_con_quema} de{' '}
          {d.quemas.anios_observados} años.
        </p>
        <table className="tabla-tarjeta">
          <thead>
            <tr>
              <th>Opción</th>
              <th>Agua</th>
              <th>Suelo</th>
              <th>Plagas</th>
              <th>Total</th>
              <th>Confianza</th>
            </tr>
          </thead>
          <tbody>
            {filas.map(({ r, pt }) => (
              <tr key={r.id} className={r.id === mejor.r.id ? 'fila-mejor' : ''}>
                <td>
                  <small>{TIPOS[r.tipo]}</small>
                  <br />
                  {r.nombre.replace('Lo que hace hoy: ', '')}
                </td>
                <td className="num">{pt.agua}</td>
                <td className="num">{pt.suelo}</td>
                <td className="num">{pt.plagas}</td>
                <td className="num">
                  <b>{pt.total}</b>
                </td>
                <td>{r.confianza.nivel}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <p>
          <b>Por qué la opción con mejor puntaje:</b> {mejor.r.por_que}
        </p>
        <p>
          <b>Fecha de siembra:</b> {res.zarc.texto}{' '}
          <span className="solo-imprimir">({res.zarc.enlace})</span>
          <a className="no-imprimir" href={res.zarc.enlace} target="_blank" rel="noreferrer">
            Ver ZARC
          </a>
          <br />
          <small>{res.zarc.nota_escenario}</small>
        </p>
        <p className="aviso-tarjeta">{res.aviso}</p>
        <p className="fuentes-tarjeta">
          Datos: {res.fuentes.filter((f) => f.es_nasa).map((f) => f.nombre.split(':')[0]).join(' · ')}. Más detalle y fuentes en la
          web.
        </p>
      </div>
      <p className="nota no-imprimir">
        El audio lee el texto que redactó el motor con clima normal y prioridad «{PRIORIDADES[res.parcela.prioridad]}»
        {res.audio.mp3 ? '' : ', con la voz de su navegador (sin conexión a internet si la voz está instalada)'}.
      </p>
    </section>
  )
}
