import {
  Bar,
  CartesianGrid,
  Cell,
  ComposedChart,
  Legend,
  Line,
  ReferenceLine,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
  ZAxis,
} from 'recharts'
import { useLocale, useT } from '../i18n/useT.js'
import DondeFalla from './DondeFalla.jsx'
import Observacion2026 from './Observacion2026.jsx'
import ProductoDecision from './ProductoDecision.jsx'

const signo = (v) => (v == null ? '—' : `${v > 0 ? '+' : ''}${v}`)

function TablaPowerChirps({ val, t }) {
  return (
    <table className="tabla-datos">
      <thead>
        <tr>
          <th>{t('validacion.colPlot')}</th>
          <th>{t('validacion.colPixel')}</th>
          <th>{t('validacion.colYear')}</th>
          <th>{t('validacion.colBias')}</th>
          <th>{t('validacion.colJja')}</th>
          <th>{t('validacion.colEarly')}</th>
        </tr>
      </thead>
      <tbody>
        {val.parcelas.map((p) => {
          const a = p.power_vs_chirps['2001-2025']
          const b = p.power_vs_chirps['1991-2000']
          return (
            <tr key={p.id}>
              <td>{p.municipio}</td>
              <td className="num">
                {p.pixel_chirps ? `${p.pixel_chirps.lat_centro}, ${p.pixel_chirps.lon_centro}` : t('common.dash')}
              </td>
              <td className="num">
                {a?.todos ? `${a.todos.power_mm_mes} / ${a.todos.chirps_mm_mes}` : t('common.dash')}
              </td>
              <td className="num">{a?.todos ? `${signo(a.todos.sesgo_pct)} %` : t('common.dash')}</td>
              <td className="num">
                {a?.jul_ago
                  ? `${signo(a.jul_ago.sesgo_pct)} % · ${a.jul_ago.eam_mm_mes} mm · r ${a.jul_ago.pearson_r} · ${a.jul_ago.n}`
                  : t('common.dash')}
              </td>
              <td className="num">{b?.todos ? `${signo(b.todos.sesgo_pct)} %` : t('common.dash')}</td>
            </tr>
          )
        })}
      </tbody>
    </table>
  )
}

function Tabla2018({ val, t }) {
  return (
    <table className="tabla-datos">
      <thead>
        <tr>
          <th>{t('validacion.colPlot')}</th>
          <th>{t('validacion.colRank')}</th>
          <th>{t('validacion.colMotor')}</th>
          <th>{t('validacion.colNdvi')}</th>
          <th>{t('validacion.colSmapAnom')}</th>
          <th>{t('validacion.colMetrics')}</th>
          <th>{t('validacion.colSpearman')}</th>
        </tr>
      </thead>
      <tbody>
        {val.parcelas.map((p) => {
          const s = p.sequia_2018
          return (
            <tr key={p.id}>
              <td>{p.municipio}</td>
              <td className="num">
                {s.puesto_2018 ?? t('common.dash')} {t('common.of')} {s.puesto_2018_de}
              </td>
              <td>{s.senales_2018.motor ? t('common.yes') : t('common.no')}</td>
              <td className="num">
                {s.anomalia_ndvi_2018_de == null ? t('common.noData') : `${signo(s.anomalia_ndvi_2018_de)} DE`}
              </td>
              <td className="num">
                {s.anomalia_smap_2018_de == null ? t('common.noSmap') : `${signo(s.anomalia_smap_2018_de)} DE`}
              </td>
              <td className="num">
                {s.aciertos} · {s.falsas_alarmas} · {s.fallos} ({s.n_anios})
              </td>
              <td className="num">
                {s.spearman_deficit_vs_ndvi ?? t('common.dash')} ({s.n_spearman})
              </td>
            </tr>
          )
        })}
      </tbody>
    </table>
  )
}

export default function Validacion({ res, validacion }) {
  const t = useT()
  const loc = useLocale()
  if (!validacion) {
    return (
      <main className="contenido">
        <section className="panel">
          <h2>{t('validacion.title')}</h2>
          <div className="banda-ejemplo">
            {t('validacion.empty')} <code>python -m pipeline.validacion.validar</code> {t('validacion.andExport')}
          </div>
        </section>
      </main>
    )
  }
  const pid = res?.parcela?.id
  const sel = validacion.parcelas.find((p) => p.id === pid) || validacion.parcelas[0]
  const dispersion = (sel?.power_vs_chirps?.pares_jul_ago || []).map(([anio, mes, power, chirps]) => ({ anio, mes, power, chirps }))
  const maximo = Math.ceil(Math.max(100, ...dispersion.map((d) => Math.max(d.power, d.chirps))) / 100) * 100
  const anios = (sel?.sequia_2018?.anios || []).map((a) => ({ ...a, es2018: a.anio === 2018 }))
  const r51 = validacion.regla_5_1
  const localeEs = loc === 'es'

  return (
    <main className="contenido">
      <section className="panel">
        <h2>{t('validacion.title')}</h2>
        <p className="sub">
          {t('validacion.reproducible')} <code>python -m pipeline.validacion.validar</code> · {t('validacion.generated')}{' '}
          <span className="sin-corte">{validacion.generado}</span>
        </p>
        <div className={r51.se_activa ? 'banda-error' : 'banda-ok'}>
          {t('validacion.rule51', { min: r51.minimo, n: r51.parcelas_con_senal_2018, efecto: r51.efecto })}
        </div>
        <ul className="lista-compacta titulares">
          {validacion.titular_power_chirps && <li>{validacion.titular_power_chirps}</li>}
          <li>{validacion.titular_2018}</li>
        </ul>
      </section>

      <Observacion2026 obs={validacion.observacion_2026} />
      <ProductoDecision />
      <DondeFalla />

      <section className="panel">
        <h2>{t('validacion.powerTitle')}</h2>
        <p className="sub">{t('validacion.powerSub')}</p>
        <div className="tabla-scroll">
          <TablaPowerChirps val={validacion} t={t} />
        </div>
        <h3>{t('validacion.chartTitle', { muni: sel?.municipio })}</h3>
        <div className="grafica">
          <ResponsiveContainer width="100%" height={260}>
            <ScatterChart margin={{ top: 8, right: 12, left: 0, bottom: 14 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e3dfd3" />
              <XAxis
                type="number"
                dataKey="chirps"
                name="CHIRPS"
                unit=" mm"
                domain={[0, maximo]}
                fontSize={11}
                label={{ value: t('validacion.chartX'), position: 'insideBottom', offset: -8, fontSize: 11 }}
              />
              <YAxis type="number" dataKey="power" name="POWER" unit=" mm" domain={[0, maximo]} fontSize={11} width={60} />
              <ZAxis range={[36, 36]} />
              <Tooltip formatter={(v) => `${v} mm`} labelFormatter={() => ''} />
              <ReferenceLine segment={[{ x: 0, y: 0 }, { x: maximo, y: maximo }]} stroke="#8a5a2b" strokeDasharray="4 3" />
              <Scatter data={dispersion} fill="#5b8fb9" isAnimationActive={false} />
            </ScatterChart>
          </ResponsiveContainer>
        </div>
        <p className="nota">{t('validacion.chartNote')}</p>
      </section>

      <section className="panel">
        <h2>{t('validacion.droughtTitle')}</h2>
        <p className="sub">
          {t('validacion.droughtSub', { lista: (sel?.sequia_2018?.anios_secos_conocidos || []).join(', ') })}
        </p>
        <div className="tabla-scroll">
          <Tabla2018 val={validacion} t={t} />
        </div>
        {validacion.evidencia_publica_2018 && (
          <div className="banda-ok">
            <b>{t('validacion.publicEvidence')}</b>{' '}
            {t('validacion.publicBody', {
              fuente: validacion.evidencia_publica_2018.fuente,
              ha: validacion.evidencia_publica_2018.guatemala_ha_perdidas.toLocaleString(localeEs ? 'es-GT' : 'en-US'),
              pers: validacion.evidencia_publica_2018.guatemala_personas_afectadas.toLocaleString(localeEs ? 'es-GT' : 'en-US'),
            })}{' '}
            <a href={validacion.evidencia_publica_2018.url} target="_blank" rel="noreferrer">
              {t('common.seeReport')}
            </a>
          </div>
        )}
        <h3>{t('validacion.chart2', { muni: sel?.municipio })}</h3>
        <div className="grafica">
          <ResponsiveContainer width="100%" height={260}>
            <ComposedChart data={anios} margin={{ top: 8, right: 8, left: -6, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e3dfd3" />
              <XAxis dataKey="anio" fontSize={11} />
              <YAxis yAxisId="d" fontSize={11} unit=" %" width={50} />
              <YAxis yAxisId="n" orientation="right" fontSize={11} width={40} domain={[-3, 3]} />
              <Tooltip />
              <Legend wrapperStyle={{ fontSize: 11 }} />
              <Bar yAxisId="d" dataKey="deficit_pct" name={t('validacion.serieDeficit')} isAnimationActive={false}>
                {anios.map((a) => (
                  <Cell key={a.anio} fill={a.es2018 ? '#b23c17' : a.riesgo_alto ? '#c79100' : '#5b8fb9'} />
                ))}
              </Bar>
              <Line
                yAxisId="d"
                dataKey="umbral_p75_previo_pct"
                name={t('validacion.serieThreshold')}
                stroke="#8a5a2b"
                strokeDasharray="4 3"
                dot={false}
                isAnimationActive={false}
              />
              <Line
                yAxisId="n"
                dataKey="anomalia_ndvi_jul_sep_de"
                name={t('validacion.serieNdvi')}
                stroke="#3f7d3a"
                strokeWidth={2}
                dot={{ r: 2 }}
                isAnimationActive={false}
                connectNulls={false}
              />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
        <p className="nota">{t('validacion.chart2Note')}</p>
        <h3>{t('validacion.notes')}</h3>
        <ul className="lista-compacta">
          {validacion.notas.map((n) => (
            <li key={n}>{n}</li>
          ))}
        </ul>
      </section>
    </main>
  )
}