import { PRIORIDADES, TIPOS, puntajes } from '../lib/datos.js'
import Calendario12, { LeyendaCalendario } from './Calendario12.jsx'

function Barra({ etiqueta, valor }) {
  return (
    <div className="barra">
      <span>{etiqueta}</span>
      <div className="barra-fondo">
        <div className="barra-relleno" style={{ width: `${valor}%` }} />
      </div>
      <b>{valor}</b>
    </div>
  )
}

function Lista({ titulo, items, clase }) {
  return (
    <div className={`bloque ${clase}`}>
      <h4>{titulo}</h4>
      <ul>
        {items.map((t, i) => (
          <li key={i}>{t}</li>
        ))}
      </ul>
    </div>
  )
}

export default function Rotaciones({ res, lluvia, temp, prioridad }) {
  const pts = res.rotaciones.map((r) => puntajes(res, r.id, lluvia, temp, prioridad))
  const mejor = Math.max(...pts.map((p) => p.total))
  const esBase = lluvia === 0 && temp === 0
  return (
    <section className="rotaciones">
      <div className="titulo-seccion">
        <h2>Tres rotaciones comparadas</h2>
        <p className="sub">
          Prioridad: {PRIORIDADES[prioridad]} ·{' '}
          {esBase ? 'clima normal' : `escenario: lluvia ${lluvia} %, temperatura +${temp} °C`}
        </p>
      </div>
      <div className="rejilla-rotaciones">
        {res.rotaciones.map((r, i) => {
          const p = pts[i]
          return (
            <article key={r.id} className={`rotacion tipo-${r.tipo}${p.total === mejor ? ' mejor' : ''}`}>
              <header>
                <span className="etiqueta">{TIPOS[r.tipo]}</span>
                {p.total === mejor && <span className="etiqueta mejor-etq">Mejor puntaje</span>}
                <h3>{r.nombre}</h3>
              </header>
              <div className="puntaje-total">
                <strong>{p.total}</strong>
                <span>puntaje total</span>
              </div>
              <Barra etiqueta="Agua" valor={p.agua} />
              <Barra etiqueta="Suelo" valor={p.suelo} />
              <Barra etiqueta="Plagas" valor={p.plagas} />
              <p className="deficit">
                Déficit de agua mediano: <b>{esBase ? r.deficit.mediana_pct : p.deficit} %</b>
                {esBase && (
                  <>
                    {' '}
                    (la mitad de los años entre {r.deficit.p25_pct} y {r.deficit.p75_pct} %)
                  </>
                )}
              </p>
              <div className={`confianza nivel-${r.confianza.nivel}`}>
                <b>Confianza {r.confianza.nivel}</b>
                <span>{r.confianza.motivo}</span>
              </div>
              <div className="bloque por-que">
                <h4>Por qué</h4>
                <p>{r.por_que}</p>
              </div>
              <Calendario12 calendario={r.calendario} />
              <Lista titulo="Beneficios" items={r.beneficios} clase="beneficios" />
              <Lista titulo="Vacíos de información" items={r.vacios} clase="vacios" />
              <Lista titulo="Riesgos que debe revisar el técnico" items={r.riesgos} clase="riesgos" />
              <details className="evidencia">
                <summary>Evidencia ({r.evidencia.length} datos)</summary>
                <table>
                  <thead>
                    <tr>
                      <th>Dato</th>
                      <th>Valor</th>
                      <th>Fuente</th>
                    </tr>
                  </thead>
                  <tbody>
                    {r.evidencia.map((e, j) => (
                      <tr key={j}>
                        <td>{e.dato}</td>
                        <td className="num">
                          {e.valor ?? '—'} {e.unidad}
                        </td>
                        <td>
                          {e.fuente}
                          <small>
                            {' '}
                            · {e.resolucion}
                            {e.periodo ? ` · ${e.periodo}` : ''}
                          </small>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </details>
              <details className="evidencia">
                <summary>Cómo se calculó el puntaje</summary>
                {['agua', 'suelo', 'plagas'].map((k) => (
                  <div key={k}>
                    <h5>{k}</h5>
                    <ul>
                      {r.trazabilidad[k].map((t, j) => (
                        <li key={j}>{t}</li>
                      ))}
                    </ul>
                  </div>
                ))}
              </details>
            </article>
          )
        })}
      </div>
      <LeyendaCalendario />
    </section>
  )
}
