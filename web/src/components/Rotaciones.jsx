import { puntajes } from '../lib/datos.js'
import { messages } from '../i18n/messages.js'
import { useLocale, useT } from '../i18n/useT.js'
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

function Lista({ titulo, items, clase, lang }) {
  return (
    <div className={`bloque ${clase}`}>
      <h4>{titulo}</h4>
      <ul lang={lang}>
        {items.map((txt, i) => (
          <li key={i}>{txt}</li>
        ))}
      </ul>
    </div>
  )
}

export default function Rotaciones({ res, lluvia, temp, prioridad }) {
  const t = useT()
  const loc = useLocale()
  const dict = messages[loc] || messages.en
  const pts = res.rotaciones.map((r) => puntajes(res, r.id, lluvia, temp, prioridad))
  const mejor = Math.max(...pts.map((p) => p.total))
  const esBase = lluvia === 0 && temp === 0
  // Los textos del motor (nombre, por qué, listas, evidencia) vienen en español: en inglés se marcan lang="es".
  const langMotor = loc === 'es' ? undefined : 'es'
  return (
    <section className="rotaciones">
      <div className="titulo-seccion">
        <h2>{t('rotaciones.title')}</h2>
        <p className="sub">
          {t('rotaciones.subPriority', { p: dict.prioridad[prioridad] })}
          {esBase ? t('rotaciones.normalClimate') : t('rotaciones.scenario', { lluvia, temp })}
        </p>
      </div>
      <div className="rejilla-rotaciones">
        {res.rotaciones.map((r, i) => {
          const p = pts[i]
          return (
            <article key={r.id} className={`rotacion tipo-${r.tipo}${p.total === mejor ? ' mejor' : ''}`}>
              <header>
                <span className="etiqueta">{dict.tipo[r.tipo]}</span>
                {p.total === mejor && <span className="etiqueta mejor-etq">{t('rotaciones.bestScore')}</span>}
                <h3 lang={langMotor}>{r.nombre}</h3>
              </header>
              <div className="puntaje-total">
                <strong>{p.total}</strong>
                <span>{t('rotaciones.totalScore')}</span>
              </div>
              <Barra etiqueta={t('rotaciones.water')} valor={p.agua} />
              <Barra etiqueta={t('rotaciones.soil')} valor={p.suelo} />
              <Barra etiqueta={t('rotaciones.pests')} valor={p.plagas} />
              <p className="deficit">
                {t('rotaciones.deficit')}
                <b>{esBase ? r.deficit.mediana_pct : p.deficit} %</b>
                {esBase && t('rotaciones.deficitRange', { p25: r.deficit.p25_pct, p75: r.deficit.p75_pct })}
              </p>
              <div className={`confianza nivel-${r.confianza.nivel}`}>
                <b>
                  {t('rotaciones.confidence')} {r.confianza.nivel}
                </b>
                <span lang={langMotor}>{r.confianza.motivo}</span>
              </div>
              <div className="bloque por-que">
                <h4>{t('rotaciones.why')}</h4>
                <p lang={langMotor}>{r.por_que}</p>
              </div>
              <Calendario12 calendario={r.calendario} />
              <Lista titulo={t('rotaciones.benefits')} items={r.beneficios} clase="beneficios" lang={langMotor} />
              <Lista titulo={t('rotaciones.gaps')} items={r.vacios} clase="vacios" lang={langMotor} />
              <Lista titulo={t('rotaciones.risks')} items={r.riesgos} clase="riesgos" lang={langMotor} />
              <details className="evidencia">
                <summary>{t('rotaciones.evidence', { n: r.evidencia.length })}</summary>
                <table>
                  <thead>
                    <tr>
                      <th>{t('rotaciones.colData')}</th>
                      <th>{t('rotaciones.colValue')}</th>
                      <th>{t('rotaciones.colSource')}</th>
                    </tr>
                  </thead>
                  <tbody lang={langMotor}>
                    {r.evidencia.map((e, j) => (
                      <tr key={j}>
                        <td>{e.dato}</td>
                        <td className="num">
                          {e.valor ?? t('common.dash')} {e.unidad}
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
                <summary>{t('rotaciones.scoreHow')}</summary>
                {[
                  ['agua', t('rotaciones.water')],
                  ['suelo', t('rotaciones.soil')],
                  ['plagas', t('rotaciones.pests')],
                ].map(([k, label]) => (
                  <div key={k}>
                    <h4>{label}</h4>
                    <ul lang={langMotor}>
                      {r.trazabilidad[k].map((txt, j) => (
                        <li key={j}>{txt}</li>
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