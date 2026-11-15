// G3: cada modelo de NASA NEX-GDDP-CMIP6 es un punto (cambio de lluvia de mayo a octubre y de temperatura).
// Círculo lleno: la opción elegida mantiene su puntaje de agua de hoy en ese futuro; cruz: no. Los datos son los
// de futuros_nasa.json (python -m motor.futuros): aquí no se calcula nada.
import { useState } from 'react'
import { CartesianGrid, ReferenceDot, ReferenceLine, ResponsiveContainer, Scatter, ScatterChart, Tooltip, XAxis, YAxis } from 'recharts'
import { useTx } from '../i18n/explorar.js'

const signo = (x) => (x > 0 ? `+${x}` : `${x}`)

function Circulo({ cx, cy }) {
  return <circle cx={cx} cy={cy} r={6} fill="#3f7d3a" stroke="#1d2b1a" strokeWidth={1} />
}

function Cruz({ cx, cy }) {
  return (
    <g stroke="#a8541f" strokeWidth={2.5} strokeLinecap="round">
      <line x1={cx - 5} y1={cy - 5} x2={cx + 5} y2={cy + 5} />
      <line x1={cx - 5} y1={cy + 5} x2={cx + 5} y2={cy - 5} />
    </g>
  )
}

function Ayuda({ active, payload, tx }) {
  if (!active || !payload?.length) return null
  const m = payload[0].payload
  return (
    <div className="recharts-default-tooltip" style={{ background: '#fff', border: '1px solid #ddd7c8', padding: '6px 8px', fontSize: 12 }}>
      <b>{m.modelo}</b>
      <br />
      {tx('nube.lluvia')}: {signo(m.x)} % · {tx('nube.temp')}: +{m.y} °C
      <br />
      {tx('nube.aguanta')}: {m.si ? tx('nube.si') : tx('nube.no')}
    </div>
  )
}

export default function NubeModelos({ escenario, rotaciones, nombreEsc, futuro, base, nombre }) {
  const tx = useTx()
  const [rid, setRid] = useState(rotaciones[0]?.id)
  const rot = rotaciones.find((r) => r.id === rid) || rotaciones[0]
  if (!rot) return null
  const puntos = escenario.modelos.map((m) => ({ modelo: m.modelo, x: m.lluvia_pct, y: m.temp_c, si: Boolean(m.aguanta[rot.id]) }))
  const si = puntos.filter((p) => p.si)
  const no = puntos.filter((p) => !p.si)
  const resumen = tx('nube.resumen', { rot: nombre(rot), k: si.length, n: puntos.length, esc: nombreEsc })
  return (
    <div className="nube-modelos">
      <h3>{tx('nube.titulo')}</h3>
      <p className="sub">{tx('nube.sub', { futuro, base })}</p>
      <div className="selector-chips" role="group" aria-label={tx('nube.rotacion')}>
        {rotaciones.map((r) => (
          <button key={r.id} type="button" aria-pressed={r.id === rot.id} onClick={() => setRid(r.id)}>
            {nombre(r)}
          </button>
        ))}
      </div>
      <p className="resumen-grafica" aria-live="polite">{resumen}</p>
      <div className="explorar-grafica" role="img" aria-label={resumen}>
        <ResponsiveContainer width="100%" height={280}>
          <ScatterChart margin={{ top: 10, right: 12, bottom: 28, left: 4 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e3dfd3" />
            <XAxis type="number" dataKey="x" name={tx('nube.lluvia')} unit=" %" fontSize={11} domain={['auto', 'auto']}
              label={{ value: tx('nube.ejeX'), position: 'insideBottom', offset: -16, fontSize: 11 }} />
            <YAxis type="number" dataKey="y" name={tx('nube.temp')} unit=" °C" fontSize={11} width={56} domain={['auto', 'auto']}
              label={{ value: tx('nube.ejeY'), angle: -90, position: 'insideLeft', offset: 12, fontSize: 11, style: { textAnchor: 'middle' } }} />
            <ReferenceLine x={0} stroke="#55624f" strokeDasharray="4 4" />
            <ReferenceDot x={escenario.lluvia_pct.mediana} y={escenario.temp_c.mediana} r={9} fill="none" stroke="#1f4f7a" strokeWidth={2}
              label={{ value: tx('nube.mediana'), position: 'top', fontSize: 10 }} />
            <Tooltip content={<Ayuda tx={tx} />} cursor={false} />
            <Scatter data={no} shape={<Cruz />} isAnimationActive={false} />
            <Scatter data={si} shape={<Circulo />} isAnimationActive={false} />
          </ScatterChart>
        </ResponsiveContainer>
      </div>
      <details>
        <summary>{tx('nube.tabla')}</summary>
        <div className="tabla-scroll" role="region" aria-label={tx('nube.tabla')} tabIndex={0}>
          <table className="tabla-datos">
            <thead>
              <tr>
                <th>{tx('nube.modelo')}</th>
                <th>{tx('nube.lluvia')}</th>
                <th>{tx('nube.lluviaCan')}</th>
                <th>{tx('nube.temp')}</th>
                <th>{tx('nube.aguanta')}</th>
              </tr>
            </thead>
            <tbody>
              {escenario.modelos.map((m) => (
                <tr key={m.modelo}>
                  <td>{m.modelo}</td>
                  <td>{signo(m.lluvia_pct)} %</td>
                  <td>{signo(m.lluvia_canicula_pct)} %</td>
                  <td>+{m.temp_c} °C</td>
                  <td>{m.aguanta[rot.id] ? tx('nube.si') : tx('nube.no')}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </details>
    </div>
  )
}
