import { Bar, BarChart, CartesianGrid, Cell, Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { MESES, listaMeses } from '../lib/datos.js'

export default function PanelSatelite({ res }) {
  const d = res.deteccion
  const q = d.quemas
  const serie = d.serie.map((x) => ({ fecha: x.fecha, ndvi: x.valido ? x.ndvi : null }))
  // una marca por año (el primer compuesto de cada año), para que el eje no repita años
  const ticksAnio = serie.filter((x, i) => i === 0 || x.fecha.slice(0, 4) !== serie[i - 1].fecha.slice(0, 4)).map((x) => x.fecha)
  const poca = d.meses_poca_cobertura || []
  const mensual = d.ndvi_mensual.map((m) => ({
    mes: MESES[m.mes - 1],
    ndvi: m.mediana,
    desnudo: d.meses_desnudos.includes(m.mes),
    poca: poca.includes(m.mes),
  }))
  const p = res.parcela

  return (
    <section className="panel">
      <h2>Lo que ve el satélite</h2>
      <p className="sub">
        {p.nombre} ({p.lat}, {p.lon}) · {p.terreno.altitud_m ?? '—'} m de altitud · pendiente{' '}
        {p.terreno.pendiente_pct ?? '—'} % (SRTM)
        {p.provisional && <span className="etiqueta aviso">coordenada provisional</span>}
      </p>

      <div className="cifras">
        <div className="cifra">
          <strong>{d.meses_desnudos.length}</strong>
          <span>meses de suelo desnudo</span>
          <small>{d.meses_desnudos.length ? listaMeses(d.meses_desnudos) : `NDVI mediano nunca bajo ${d.umbral_desnudo_ndvi}`}</small>
        </div>
        {d.umbral_poca_cobertura_ndvi != null && (
          <div className="cifra">
            <strong>{poca.length}</strong>
            <span>meses de poca cobertura</span>
            <small>{poca.length ? listaMeses(poca) : 'ninguno'} (NDVI bajo {d.umbral_poca_cobertura_ndvi})</small>
          </div>
        )}
        <div className="cifra">
          <strong>{d.ciclos.mediana ?? '—'}</strong>
          <span>ciclos de verdor por año</span>
          <small>mediana {d.periodo}</small>
        </div>
        <div className="cifra">
          <strong>
            {q.anios_con_quema}/{q.anios_observados}
          </strong>
          <span>años con quema cercana</span>
          <small>
            VIIRS, ≤{q.radio_m} m, ene–may · {q.detecciones_1km} focos a ≤1 km
          </small>
        </div>
        <div className="cifra">
          <strong>{d.calidad.pct_validos} %</strong>
          <span>compuestos válidos</span>
          <small>
            {d.calidad.validos} de {d.calidad.compuestos} sin nube
          </small>
        </div>
      </div>

      <h3>Verdor (NDVI de MODIS, 250 m, cada 16 días)</h3>
      <div className="grafica">
        <ResponsiveContainer width="100%" height={170}>
          <LineChart data={serie} margin={{ top: 6, right: 8, left: -18, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e3dfd3" />
            <XAxis dataKey="fecha" ticks={ticksAnio} interval={0} tickFormatter={(f) => f.slice(0, 4)} fontSize={11} />
            <YAxis domain={[0, 1]} fontSize={11} />
            <Tooltip formatter={(v) => (v == null ? 'nube' : v.toFixed(2))} labelFormatter={(f) => f} />
            <ReferenceLine y={d.umbral_desnudo_ndvi} stroke="#8a5a2b" strokeDasharray="4 3" />
            <Line type="monotone" dataKey="ndvi" stroke="#3f7d3a" dot={false} strokeWidth={2} connectNulls={false} isAnimationActive={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <p className="nota">Línea punteada: suelo desnudo (NDVI bajo {d.umbral_desnudo_ndvi}). Los huecos son compuestos con nube.</p>
      <h3>NDVI mediano por mes ({d.periodo})</h3>
      <div className="grafica">
        <ResponsiveContainer width="100%" height={130}>
          <BarChart data={mensual} margin={{ top: 6, right: 8, left: -18, bottom: 0 }}>
            <XAxis dataKey="mes" fontSize={11} />
            <YAxis domain={[0, 1]} fontSize={11} />
            <Tooltip formatter={(v) => (v == null ? 'sin dato' : v.toFixed(2))} />
            <ReferenceLine y={d.umbral_desnudo_ndvi} stroke="#8a5a2b" strokeDasharray="4 3" />
            {d.umbral_poca_cobertura_ndvi != null && (
              <ReferenceLine y={d.umbral_poca_cobertura_ndvi} stroke="#b8913f" strokeDasharray="2 3" />
            )}
            <Bar dataKey="ndvi" isAnimationActive={false}>
              {mensual.map((m) => (
                <Cell key={m.mes} fill={m.desnudo ? '#a8754a' : m.poca ? '#d9b26f' : '#6fa35f'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
      <p className="nota">
        Barras: café = suelo desnudo (NDVI bajo {d.umbral_desnudo_ndvi}); arena = poca cobertura (bajo{' '}
        {d.umbral_poca_cobertura_ndvi ?? '—'}); verde = cubierto. {q.nota}
      </p>
    </section>
  )
}
