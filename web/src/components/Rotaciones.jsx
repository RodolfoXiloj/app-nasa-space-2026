import { puntajes } from '../lib/datos.js'
import { messages } from '../i18n/messages.js'
import { useLocale, useT } from '../i18n/useT.js'
import { leerMotor } from '../i18n/motor.js'
import Calendario12, { LeyendaCalendario } from './Calendario12.jsx'

// La traza del puntaje sale del motor solo en español y con estas plantillas fijas; en inglés se traduce
// línea por línea. Si el JSON trae `en.trazabilidad`, se usa esa. Una línea que no encaja queda en
// español con lang="es".
const NUM = '(-?[\\d.]+)'
const TRAZA_EN = [
  [`^Base ${NUM}$`, 'Base $1'],
  [
    `^Déficit de agua mediano ${NUM} % \\(entre ${NUM} y ${NUM} % la mitad de los años\\), balance diario con NASA POWER (\\d+-\\d+) y ET0 de Hargreaves \\(FAO-56\\)$`,
    'Median water deficit $1 % (between $2 and $3 % in half of the years), daily water balance with NASA POWER $4 and Hargreaves ET0 (FAO-56)',
  ],
  [`^Pérdida relativa esperada = Ky x déficit \\(FAO-33\\): mediana ${NUM} %$`, 'Expected relative yield loss = Ky x deficit (FAO-33): median $1 %'],
  [`^Resta por canícula larga: ${NUM} puntos \\(frecuencia ${NUM} %, Ky ${NUM}\\)$`, 'Subtracted for a long canícula: $1 points (frequency $2 %, Ky $3)'],
  [`^${NUM} meses de suelo desnudo x ${NUM} puntos \\(pendiente fuerte: ${NUM} %\\)$`, '$1 bare-soil months x $2 points (steep slope: $3 %)'],
  [`^${NUM} meses de suelo desnudo x ${NUM} puntos$`, '$1 bare-soil months x $2 points'],
  [`^${NUM} meses de poca cobertura x ${NUM} puntos$`, '$1 low-cover months x $2 points'],
  [`^Quema: resta ${NUM} puntos$`, 'Burning: subtracts $1 points'],
  [`^Suma ${NUM} por cobertura$`, 'Adds $1 for a cover crop'],
  [`^Suma ${NUM} por leguminosa$`, 'Adds $1 for a legume'],
  [`^Suma ${NUM} por rastrojo en pie$`, 'Adds $1 for standing stubble'],
  [`^Suma ${NUM}: alterna familias entre ciclos \\((.+)\\)$`, 'Adds $1: alternates plant families between cycles ($2)'],
  [`^Suma ${NUM}: asocia familias distintas en primera$`, 'Adds $1: intercrops different families in primera'],
  [`^Suma ${NUM}: cobertura que rompe el ciclo de plagas$`, 'Adds $1: cover that breaks the pest cycle'],
  [`^Resta ${NUM}: el mismo cultivo cada año sin asociación$`, 'Subtracts $1: the same crop every year, with no intercrop'],
].map(([re, en]) => [new RegExp(re), en])

function lineaTraza(txt, loc) {
  if (loc === 'es') return { txt }
  const hit = TRAZA_EN.find(([re]) => re.test(txt))
  return hit ? { txt: txt.replace(hit[0], hit[1]) } : { txt, lang: 'es' }
}

// Fila de evidencia: primero `fila.en`, luego `rotacion.en.evidencia[j]` (lista paralela), luego español.
function campoEvidencia(r, e, j, campo, loc) {
  const m = leerMotor(e, campo, loc)
  if (m.lang === loc || loc === 'es') return m
  const alt = (((r[loc] || {}).evidencia || [])[j] || {})[campo]
  return alt ? { txt: alt, lang: loc } : m
}

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

function Lista({ titulo, m, clase, lang }) {
  const items = m.txt || []
  return (
    <div className={`bloque ${clase}`}>
      <h4>{titulo}</h4>
      <ul lang={lang(m)}>
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
  // Textos del motor en el idioma activo (r.en.* en inglés); lo que falte va en español con lang="es".
  const m = (obj, campo) => leerMotor(obj, campo, loc)
  const lang = (x) => (x.txt && x.lang !== loc ? x.lang : undefined)
  const nivel = (n) => t(`a11y.nivel.${n}`)
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
                <h3 lang={lang(m(r, 'nombre'))}>{m(r, 'nombre').txt}</h3>
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
                  {t('rotaciones.confidence')} {nivel(r.confianza.nivel)}
                </b>
                <span lang={lang(m(r.confianza, 'motivo'))}>{m(r.confianza, 'motivo').txt}</span>
              </div>
              <div className="bloque por-que">
                <h4>{t('rotaciones.why')}</h4>
                <p lang={lang(m(r, 'por_que'))}>{m(r, 'por_que').txt}</p>
              </div>
              <Calendario12 calendario={r.calendario} />
              <Lista titulo={t('rotaciones.benefits')} m={m(r, 'beneficios')} clase="beneficios" lang={lang} />
              <Lista titulo={t('rotaciones.gaps')} m={m(r, 'vacios')} clase="vacios" lang={lang} />
              <Lista titulo={t('rotaciones.risks')} m={m(r, 'riesgos')} clase="riesgos" lang={lang} />
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
                  <tbody>
                    {r.evidencia.map((e, j) => {
                      const c = (campo) => campoEvidencia(r, e, j, campo, loc)
                      const [dato, unidad, fuente, resol] = ['dato', 'unidad', 'fuente', 'resolucion'].map(c)
                      return (
                        <tr key={j}>
                          <td lang={lang(dato)}>{dato.txt}</td>
                          <td className="num">
                            {e.valor ?? t('common.dash')} <span lang={lang(unidad)}>{unidad.txt}</span>
                          </td>
                          <td>
                            <span lang={lang(fuente)}>{fuente.txt}</span>
                            <small>
                              {' '}
                              · <span lang={lang(resol)}>{resol.txt}</span>
                              {e.periodo ? ` · ${e.periodo}` : ''}
                            </small>
                          </td>
                        </tr>
                      )
                    })}
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
                    <ul>
                      {(((r[loc] || {}).trazabilidad || {})[k] || r.trazabilidad[k]).map((txt, j) => {
                        const l = (r[loc] || {}).trazabilidad ? { txt } : lineaTraza(txt, loc)
                        return (
                          <li key={j} lang={l.lang}>
                            {l.txt}
                          </li>
                        )
                      })}
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