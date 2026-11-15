// G4: lluvia de julio y agosto de 2026 frente a la mediana 1991-2025 y al año más seco antes de 2026
// (bloque `lluvia_jul_ago` de data/explorar/{pid}.json; las mismas cifras de la pestaña Validación).
// 2026 es una observación preliminar: no entra en los puntajes.
import { Bar, BarChart, CartesianGrid, LabelList, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { useTx } from '../i18n/explorar.js'

export default function LluviaJulAgo({ explorar }) {
  const tx = useTx()
  const ll = explorar?.lluvia_jul_ago
  if (!ll) return null
  const nombres = {
    a2026: tx('lluvia.anio2026'),
    mediana: tx('lluvia.mediana', { periodo: ll.periodo_referencia }),
    seco: tx('lluvia.seco', { anio: ll.anio_mas_seco }),
  }
  const datos = [
    { mes: tx('lluvia.julio'), a2026: ll.anio_2026['7'], mediana: ll.mediana['7'], seco: ll.mas_seco['7'] },
    { mes: tx('lluvia.agosto'), a2026: ll.anio_2026['8'], mediana: ll.mediana['8'], seco: ll.mas_seco['8'] },
  ]
  const resumen = tx('lluvia.resumen', {
    t26: tx.num(ll.total_2026_mm, 1),
    periodo: ll.periodo_referencia,
    med: tx.num(ll.mediana_jul_ago_mm, 1),
    anio: ll.anio_mas_seco,
    seco: tx.num(ll.total_mas_seco_mm, 1),
  })
  const etiqueta = (v) => tx.num(v)
  return (
    <section className="panel explorar-panel" aria-labelledby="lluvia-jul-ago-titulo">
      <h2 id="lluvia-jul-ago-titulo">{tx('lluvia.titulo')}</h2>
      <p className="resumen-grafica">{resumen}</p>
      <div className="explorar-grafica" role="img" aria-label={resumen}>
        <ResponsiveContainer width="100%" height={230}>
          <BarChart data={datos} margin={{ top: 18, right: 8, bottom: 0, left: -10 }}>
            <defs>
              <pattern id="rayas-2026" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
                <rect width="6" height="6" fill="#a8541f" />
                <rect width="2" height="6" fill="#f3d9c5" />
              </pattern>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e3dfd3" />
            <XAxis dataKey="mes" fontSize={11} />
            <YAxis fontSize={11} unit=" mm" width={58} />
            <Tooltip formatter={(v, n) => [`${tx.num(v, 1)} mm`, n]} />
            <Legend wrapperStyle={{ fontSize: 11 }} formatter={(v) => <span style={{ color: '#1d2b1a' }}>{v}</span>} />
            <Bar dataKey="a2026" name={nombres.a2026} fill="url(#rayas-2026)" stroke="#a8541f" isAnimationActive={false}>
              <LabelList dataKey="a2026" position="top" fontSize={10} formatter={etiqueta} />
            </Bar>
            <Bar dataKey="mediana" name={nombres.mediana} fill="#5b8fb9" isAnimationActive={false}>
              <LabelList dataKey="mediana" position="top" fontSize={10} formatter={etiqueta} />
            </Bar>
            <Bar dataKey="seco" name={nombres.seco} fill="#c9c4b6" stroke="#55624f" isAnimationActive={false}>
              <LabelList dataKey="seco" position="top" fontSize={10} formatter={etiqueta} />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
      <p className="nota">{tx('lluvia.nota')}</p>
    </section>
  )
}
