import { Bar, CartesianGrid, ComposedChart, Legend, Line, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { MESES } from '../lib/datos.js'

export default function Clima({ res }) {
  const c = res.clima
  const s = res.smap
  const datos = MESES.map((m, i) => ({ mes: m, lluvia: c.lluvia_mensual_normal_mm[i], et0: c.et0_mensual_normal_mm[i] }))
  const can = c.canicula
  return (
    <section className="panel">
      <h2>Clima de la zona</h2>
      <p className="sub">
        {c.periodo} · {c.resolucion}
      </p>
      <div className="grafica">
        <ResponsiveContainer width="100%" height={170}>
          <ComposedChart data={datos} margin={{ top: 6, right: 8, left: -14, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e3dfd3" />
            <XAxis dataKey="mes" fontSize={11} />
            <YAxis fontSize={11} unit=" mm" width={58} />
            <Tooltip formatter={(v) => `${v} mm`} />
            <Legend wrapperStyle={{ fontSize: 11 }} />
            <Bar dataKey="lluvia" name={c.fuente_lluvia?.startsWith('CHIRPS') ? 'Lluvia normal (CHIRPS)' : 'Lluvia normal (POWER)'} fill="#5b8fb9" isAnimationActive={false} />
            <Line dataKey="et0" name="ET0 (agua que pide el ambiente)" stroke="#c0622f" strokeWidth={2} dot={false} isAnimationActive={false} />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
      <ul className="lista-compacta">
        <li>
          Canícula ({can.ventana}): en <strong>{can.anios_racha_larga}</strong> de {can.anios_total} años la racha seca pasó de{' '}
          {can.umbral_racha_dias} días (día seco: menos de {can.umbral_dia_seco_mm} mm). Racha mediana: {can.racha_mediana_dias} días.
        </li>
        <li>
          Año más seco del periodo: <strong>{c.anio_mas_seco.anio}</strong> ({c.anio_mas_seco.mm} mm).
        </li>
        {c.power_vs_chirps?.jul_ago && (
          <li>
            Lluvia de julio–agosto: NASA POWER {c.power_vs_chirps.jul_ago.power_mm_mes} mm/mes y CHIRPS{' '}
            {c.power_vs_chirps.jul_ago.chirps_mm_mes} mm/mes ({c.power_vs_chirps.jul_ago.sesgo_pct > 0 ? '+' : ''}
            {c.power_vs_chirps.jul_ago.sesgo_pct} %, r = {c.power_vs_chirps.jul_ago.pearson_r}, n ={' '}
            {c.power_vs_chirps.jul_ago.n} meses).
          </li>
        )}
        <li>
          {s.disponible ? (
            <>
              Humedad del suelo SMAP (julio–agosto, {s.periodo}): mediana de {s.humedad_jul_ago_m3m3} m³/m³.
              {s.puesto_ultimo
                ? s.puesto_ultimo === 1
                  ? ` En ${s.anio_ultimo} fue la más baja de los ${s.n_anios} años con SMAP.`
                  : ` En ${s.anio_ultimo} quedó en el puesto ${s.puesto_ultimo} de ${s.n_anios} años, de la más baja a la más alta.`
                : ''}
            </>
          ) : (
            <>
              <span className="etiqueta aviso">modelo, no SMAP</span> Humedad de raíz julio–agosto: {s.respaldo?.jul_ago_mediana} (
              {s.respaldo?.unidad}, {s.respaldo?.etiqueta}, {s.respaldo?.periodo}). {s.nota}
            </>
          )}
        </li>
      </ul>
    </section>
  )
}
