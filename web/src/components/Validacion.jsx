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
import Observacion2026 from './Observacion2026.jsx'

const signo = (v) => (v == null ? '—' : `${v > 0 ? '+' : ''}${v}`)
const si = (b) => (b ? 'sí' : 'no')

function TablaPowerChirps({ val }) {
  return (
    <table className="tabla-datos">
      <thead>
        <tr>
          <th>Parcela</th>
          <th>Píxel CHIRPS</th>
          <th>Todo el año 2001–2025: POWER / CHIRPS (mm/mes)</th>
          <th>Sesgo</th>
          <th>Julio–agosto: sesgo · error medio · r · n</th>
          <th>Sesgo 1991–2000</th>
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
                {p.pixel_chirps ? `${p.pixel_chirps.lat_centro}, ${p.pixel_chirps.lon_centro}` : '—'}
              </td>
              <td className="num">
                {a?.todos ? `${a.todos.power_mm_mes} / ${a.todos.chirps_mm_mes}` : '—'}
              </td>
              <td className="num">{a?.todos ? `${signo(a.todos.sesgo_pct)} %` : '—'}</td>
              <td className="num">
                {a?.jul_ago
                  ? `${signo(a.jul_ago.sesgo_pct)} % · ${a.jul_ago.eam_mm_mes} mm · r ${a.jul_ago.pearson_r} · ${a.jul_ago.n}`
                  : '—'}
              </td>
              <td className="num">{b?.todos ? `${signo(b.todos.sesgo_pct)} %` : '—'}</td>
            </tr>
          )
        })}
      </tbody>
    </table>
  )
}

function Tabla2018({ val }) {
  return (
    <table className="tabla-datos">
      <thead>
        <tr>
          <th>Parcela</th>
          <th>Puesto de 2018 por déficit</th>
          <th>El motor marca 2018</th>
          <th>Anomalía NDVI jul–sep 2018</th>
          <th>Anomalía SMAP jul–ago 2018</th>
          <th>Aciertos · falsas alarmas · fallos (n años)</th>
          <th>Spearman déficit vs NDVI (n)</th>
        </tr>
      </thead>
      <tbody>
        {val.parcelas.map((p) => {
          const s = p.sequia_2018
          return (
            <tr key={p.id}>
              <td>{p.municipio}</td>
              <td className="num">
                {s.puesto_2018 ?? '—'} de {s.puesto_2018_de}
              </td>
              <td>{si(s.senales_2018.motor)}</td>
              <td className="num">{s.anomalia_ndvi_2018_de == null ? 'sin dato' : `${signo(s.anomalia_ndvi_2018_de)} DE`}</td>
              <td className="num">{s.anomalia_smap_2018_de == null ? 'sin SMAP' : `${signo(s.anomalia_smap_2018_de)} DE`}</td>
              <td className="num">
                {s.aciertos} · {s.falsas_alarmas} · {s.fallos} ({s.n_anios})
              </td>
              <td className="num">
                {s.spearman_deficit_vs_ndvi ?? '—'} ({s.n_spearman})
              </td>
            </tr>
          )
        })}
      </tbody>
    </table>
  )
}

export default function Validacion({ res, validacion }) {
  if (!validacion) {
    return (
      <main className="contenido">
        <section className="panel">
          <h2>Validación</h2>
          <div className="banda-ejemplo">
            Aún no hay resultados: corra <code>python -m pipeline.validacion.validar</code> y la exportación.
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

  return (
    <main className="contenido">
      <section className="panel">
        <h2>Validación</h2>
        <p className="sub">
          Reproducible con <code>python -m pipeline.validacion.validar</code> · generado{' '}
          <span className="sin-corte">{validacion.generado}</span>
        </p>
        <div className={r51.se_activa ? 'banda-error' : 'banda-ok'}>
          Regla fijada antes de ver el resultado: si ninguna señal muestra 2018 en {r51.minimo} o más parcelas, la confianza de las
          recomendaciones de agua baja a «baja». Parcelas con señal: <b>{r51.parcelas_con_senal_2018}</b>. Efecto: {r51.efecto}
        </div>
        <ul className="lista-compacta titulares">
          {validacion.titular_power_chirps && <li>{validacion.titular_power_chirps}</li>}
          <li>{validacion.titular_2018}</li>
        </ul>
      </section>

      <Observacion2026 obs={validacion.observacion_2026} />

      <section className="panel">
        <h2>Lluvia de NASA POWER contra CHIRPS en 5 municipios</h2>
        <p className="sub">
          POWER: celdas de ~50 km. CHIRPS: ~5 km, mezcla satélite y estaciones; no es medición en tierra.
        </p>
        <div className="tabla-scroll">
          <TablaPowerChirps val={validacion} />
        </div>
        <h3>Julio–agosto en {sel?.municipio}: cada punto es un mes (2001–2025)</h3>
        <div className="grafica">
          <ResponsiveContainer width="100%" height={260}>
            <ScatterChart margin={{ top: 8, right: 12, left: 0, bottom: 14 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e3dfd3" />
              <XAxis type="number" dataKey="chirps" name="CHIRPS" unit=" mm" domain={[0, maximo]} fontSize={11}
                label={{ value: 'CHIRPS (mm/mes)', position: 'insideBottom', offset: -8, fontSize: 11 }} />
              <YAxis type="number" dataKey="power" name="POWER" unit=" mm" domain={[0, maximo]} fontSize={11} width={60} />
              <ZAxis range={[36, 36]} />
              <Tooltip formatter={(v) => `${v} mm`} labelFormatter={() => ''} />
              <ReferenceLine segment={[{ x: 0, y: 0 }, { x: maximo, y: maximo }]} stroke="#8a5a2b" strokeDasharray="4 3" />
              <Scatter data={dispersion} fill="#5b8fb9" isAnimationActive={false} />
            </ScatterChart>
          </ResponsiveContainer>
        </div>
        <p className="nota">La línea punteada es el acuerdo perfecto. Arriba de la línea, POWER da más lluvia que CHIRPS.</p>
      </section>

      <section className="panel">
        <h2>La sequía de 2018: ¿el motor la habría visto venir?</h2>
        <p className="sub">
          Para cada año se usa solo lo que se sabía antes: «riesgo alto» si el déficit supera el percentil 75 de los años
          anteriores. Años secos conocidos: {(sel?.sequia_2018?.anios_secos_conocidos || []).join(', ')}.
        </p>
        <div className="tabla-scroll">
          <Tabla2018 val={validacion} />
        </div>
        {validacion.evidencia_publica_2018 && (
          <div className="banda-ok">
            <b>Evidencia pública:</b> {validacion.evidencia_publica_2018.fuente}: en Guatemala se perdieron{' '}
            {validacion.evidencia_publica_2018.guatemala_ha_perdidas.toLocaleString('es-GT')} ha de maíz y frijol y hubo{' '}
            {validacion.evidencia_publica_2018.guatemala_personas_afectadas.toLocaleString('es-GT')} personas afectadas;
            Chiquimula entre los departamentos más afectados.{' '}
            <a href={validacion.evidencia_publica_2018.url} target="_blank" rel="noreferrer">
              Ver informe
            </a>
          </div>
        )}
        <h3>Déficit de agua de la rotación actual en {sel?.municipio} y anomalía de verdor</h3>
        <div className="grafica">
          <ResponsiveContainer width="100%" height={260}>
            <ComposedChart data={anios} margin={{ top: 8, right: 8, left: -6, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e3dfd3" />
              <XAxis dataKey="anio" fontSize={11} />
              <YAxis yAxisId="d" fontSize={11} unit=" %" width={50} />
              <YAxis yAxisId="n" orientation="right" fontSize={11} width={40} domain={[-3, 3]} />
              <Tooltip />
              <Legend wrapperStyle={{ fontSize: 11 }} />
              <Bar yAxisId="d" dataKey="deficit_pct" name="Déficit del año (%)" isAnimationActive={false}>
                {anios.map((a) => (
                  <Cell key={a.anio} fill={a.es2018 ? '#b23c17' : a.riesgo_alto ? '#c79100' : '#5b8fb9'} />
                ))}
              </Bar>
              <Line yAxisId="d" dataKey="umbral_p75_previo_pct" name="Umbral con años anteriores (%)" stroke="#8a5a2b"
                strokeDasharray="4 3" dot={false} isAnimationActive={false} />
              <Line yAxisId="n" dataKey="anomalia_ndvi_jul_sep_de" name="Anomalía NDVI jul–sep (DE)" stroke="#3f7d3a"
                strokeWidth={2} dot={{ r: 2 }} isAnimationActive={false} connectNulls={false} />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
        <p className="nota">Rojo: 2018. Amarillo: otros años que el motor marcó como riesgo alto. Línea verde: NDVI bajo lo normal es negativo.</p>
        <h3>Notas</h3>
        <ul className="lista-compacta">
          {validacion.notas.map((n) => (
            <li key={n}>{n}</li>
          ))}
        </ul>
      </section>
    </main>
  )
}
