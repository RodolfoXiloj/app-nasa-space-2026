// G1: el agua del ciclo de primera, sumada día a día, para una opción (bloque `curva_agua` de
// data/explorar/{pid}.json, calculado en motor/explorar.py con el mismo balance que los puntajes).
// Azul: lluvia; café: el agua que pide el cultivo (ETc FAO-56); verde: el agua que pudo tomar del suelo.
// El tramo entre café y verde (el déficit) va rayado, no solo de color.
import { useState } from 'react'
import { Area, CartesianGrid, ComposedChart, Line, ReferenceArea, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { useTx } from '../i18n/explorar.js'

const MESES_ES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
const MESES_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

function fecha(mmdd, loc) {
  const [m, d] = mmdd.split('-').map(Number)
  return loc === 'es' ? `${d} de ${MESES_ES[m - 1]}` : `${MESES_EN[m - 1]} ${d}`
}

export default function CurvaAgua({ entrada, idPatron = 'rayas-deficit' }) {
  const tx = useTx()
  const cur = entrada?.curva_agua
  const [clave, setClave] = useState('tipico')
  if (!cur || !cur.anios?.tipico) return <p className="nota">{tx('curva.sinCurva')}</p>
  const x = cur.anios[clave] || cur.anios.tipico
  const datos = x.puntos.map(([dia, lluvia, demanda, usada]) => ({ dia, lluvia, demanda, usada, hueco: Math.max(0, demanda - usada) }))
  const nombreCultivo = (tx.loc === 'en' && cur.nombre_cultivo_en) || cur.nombre_cultivo
  const resumen = tx('curva.resumen', { anio: x.anio, demanda: tx.num(x.demanda_mm), usada: tx.num(x.usada_mm), deficit: x.deficit_pct })
  const banda = (a, b) => [Math.max(1, a), Math.min(cur.dias, b)]
  const [c1, c2] = banda(cur.canicula[0], cur.canicula[1])
  const [e1, e2] = banda(cur.etapa_media[0], cur.etapa_media[1])
  return (
    <div className="curva-agua">
      <p className="sub">
        {tx('curva.sub', { cultivo: nombreCultivo[0].toUpperCase() + nombreCultivo.slice(1), fecha: fecha(cur.siembra, tx.loc), dias: cur.dias })}
      </p>
      <div className="selector-chips" role="group" aria-label={tx('curva.titulo')}>
        {['tipico', 'dificil'].map((k) =>
          cur.anios[k] ? (
            <button key={k} type="button" aria-pressed={k === clave} onClick={() => setClave(k)}>
              {tx(`curva.${k}`, { anio: cur.anios[k].anio })}
            </button>
          ) : null,
        )}
      </div>
      <p className="resumen-grafica" aria-live="polite">{resumen}</p>
      <div className="explorar-grafica" role="img" aria-label={`${resumen} ${tx('curva.leyendaBandas')}`}>
        <ResponsiveContainer width="100%" height={260}>
          <ComposedChart data={datos} margin={{ top: 18, right: 10, bottom: 22, left: -6 }}>
            <defs>
              <pattern id={idPatron} width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
                <rect width="6" height="6" fill="#fff" />
                <rect width="3" height="6" fill="#f3d9c5" />
              </pattern>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e3dfd3" />
            {c2 > c1 && (
              <ReferenceArea x1={c1} x2={c2} fill="#fff1c9" fillOpacity={0.7} ifOverflow="hidden"
                label={{ value: tx('curva.canicula'), position: 'insideTop', fontSize: 10 }} />
            )}
            {e2 > e1 && (
              <ReferenceArea x1={e1} x2={e2} fill="#e3efdc" fillOpacity={0.6} ifOverflow="hidden"
                label={{ value: tx('curva.etapa'), position: 'insideBottom', fontSize: 10 }} />
            )}
            <XAxis dataKey="dia" type="number" domain={[1, cur.dias]} fontSize={11}
              ticks={[1, ...Array.from({ length: Math.floor(cur.dias / 30) }, (_, i) => (i + 1) * 30), cur.dias].filter((v, i, a) => a.indexOf(v) === i)}
              label={{ value: tx('curva.ejeX'), position: 'insideBottom', offset: -12, fontSize: 11 }} />
            <YAxis fontSize={11} unit=" mm" width={62} />
            <Tooltip
              labelFormatter={(d) => tx('curva.dia', { d })}
              formatter={(v, n) => [`${tx.num(v)} mm`, n]}
            />
            <Area dataKey="usada" stackId="s" stroke="none" fill="none" isAnimationActive={false} legendType="none" tooltipType="none" />
            <Area dataKey="hueco" stackId="s" stroke="none" fill={`url(#${idPatron})`} isAnimationActive={false} legendType="none" tooltipType="none" />
            <Line dataKey="lluvia" name={tx('curva.lluvia')} stroke="#5b8fb9" strokeWidth={2} strokeDasharray="6 4" dot={false} isAnimationActive={false} />
            <Line dataKey="demanda" name={tx('curva.demanda')} stroke="#a8541f" strokeWidth={2.5} dot={false} isAnimationActive={false} />
            <Line dataKey="usada" name={tx('curva.usada')} stroke="#3f7d3a" strokeWidth={2.5} dot={false} isAnimationActive={false} />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
      <ul className="leyenda-linea" aria-hidden="true">
        <li className="l-lluvia"><i />{tx('curva.lluvia')}</li>
        <li className="l-demanda"><i />{tx('curva.demanda')}</li>
        <li className="l-usada"><i />{tx('curva.usada')}</li>
        <li className="l-deficit"><i />{tx('curva.deficit')}</li>
      </ul>
      <p className="nota">{tx('curva.leyendaBandas')}</p>
      {cur.reserva_suelo_mm != null && (
        <p className="nota">{tx('curva.porQue', { reserva: cur.reserva_suelo_mm, efectiva: cur.lluvia_efectiva_pct })}</p>
      )}
      <p className="nota">{tx('curva.nota')}</p>
    </div>
  )
}
