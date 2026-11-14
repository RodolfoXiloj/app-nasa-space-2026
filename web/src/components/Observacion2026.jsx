// July–August 2026 observation from validacion.json (pipeline/validacion/validar.py). Past observation, not a forecast.

import { OBS_2026, OBS_LIMITES } from '../i18n/evidence.js'
import { useLocale, useT } from '../i18n/useT.js'

const mm = (v) => `${Number(v).toFixed(1)} mm`
const hum = (v) => Number(v).toFixed(3)

function obsCopy(obs, loc) {
  const pack = OBS_2026[loc] || OBS_2026.en
  return {
    titulo: pack.titulo,
    resumen: pack.resumen,
    rawTitulo: obs?.titulo,
  }
}

export function LineaObservacion2026({ obs, onDetalle }) {
  const loc = useLocale()
  const t = useT()
  if (!obs) return null
  const copy = obsCopy(obs, loc)
  return (
    <div className="banda-obs no-imprimir" role="note">
      <b>{copy.titulo}.</b> {copy.resumen}{' '}
      <span className="solo-prueba" hidden aria-hidden="true">
        {obs.titulo}
      </span>
      <button type="button" className="enlace" onClick={onDetalle}>
        {t('obs.detail')}
      </button>
    </div>
  )
}

export default function Observacion2026({ obs }) {
  const loc = useLocale()
  const t = useT()
  if (!obs) return null
  const copy = obsCopy(obs, loc)
  return (
    <section className="panel" id="observacion-2026">
      <h2>{copy.titulo}</h2>
      <p className="sub">
        {t('obs.outsideMotor')} <code>python -m pipeline.validacion.validar</code>.
      </p>
      <p>{copy.resumen}</p>

      <h3>{t('obs.rainTitle')}</h3>
      <div className="tabla-scroll">
        <table className="tabla-datos">
          <thead>
            <tr>
              <th>{t('obs.colPlot')}</th>
              <th>{t('obs.col2026')}</th>
              <th>{t('obs.colMedian', { periodo: obs.lluvia_chirps[0]?.periodo_referencia })}</th>
              <th>{t('obs.colPct')}</th>
              <th>{t('obs.colMin')}</th>
              <th>{t('obs.colDrier')}</th>
            </tr>
          </thead>
          <tbody>
            {obs.lluvia_chirps.map((x) => (
              <tr key={x.id}>
                <td>{x.municipio}</td>
                <td className="num">{mm(x.mm_2026)}</td>
                <td className="num">{mm(x.mediana_mm)}</td>
                <td className="num">{x.pct_de_la_mediana} %</td>
                <td className="num">
                  {mm(x.minimo_anterior_mm)} ({x.anio_minimo_anterior})
                </td>
                <td className="num">
                  {x.anios_mas_secos_que_2026} {t('common.of')} {x.n_anios_referencia}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {obs.smap_celdas?.length > 0 && (
        <>
          <h3>{t('obs.smapTitle')}</h3>
          <div className="tabla-scroll">
            <table className="tabla-datos">
              <thead>
                <tr>
                  <th>{t('obs.colCell')}</th>
                  <th>{t('obs.colPlots')}</th>
                  <th>2026</th>
                  <th>{t('obs.colMin')}</th>
                  <th>{t('obs.colLowest')}</th>
                </tr>
              </thead>
              <tbody>
                {obs.smap_celdas.map((x) => (
                  <tr key={`${x.celda.linea}-${x.celda.muestra}`}>
                    <td>
                      {x.celda.linea}, {x.celda.muestra}
                    </td>
                    <td>{x.parcelas.join(', ')}</td>
                    <td className="num">{hum(x.m3m3_2026)} m³/m³</td>
                    <td className="num">
                      {hum(x.minimo_anterior_m3m3)} ({x.anio_minimo_anterior})
                    </td>
                    <td>
                      {x.es_el_mas_bajo ? t('common.yes') : t('common.no')}, {t('common.of')} {x.n_anios}{' '}
                      {loc === 'es' ? 'años' : 'years'} ({x.periodo})
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      <h3>{t('obs.reports')}</h3>
      <ul className="lista-compacta">
        {obs.reportes_publicos.map((e) => (
          <li key={e.id}>
            <a href={e.url} target="_blank" rel="noreferrer">
              {e.fuente}
            </a>{' '}
            ({e.relacion}): «{e.cita}». {e.nota}
          </li>
        ))}
      </ul>

      <h3>{t('obs.limits')}</h3>
      <ul className="lista-compacta">
        {(loc === 'en' ? OBS_LIMITES.en : obs.limites).map((txt) => (
          <li key={txt}>{txt}</li>
        ))}
      </ul>
    </section>
  )
}