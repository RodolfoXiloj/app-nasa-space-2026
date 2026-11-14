import { ESTADOS, MESES } from '../lib/datos.js'

export default function Calendario12({ calendario }) {
  return (
    <div className="calendario" role="table" aria-label="Calendario de 12 meses">
      {calendario.map((m) => (
        <div
          key={m.mes}
          className={`mes estado-${m.estado}${m.alertas.length ? ' con-alerta' : ''}`}
          title={[ESTADOS[m.estado], m.cultivo, ...m.alertas].filter(Boolean).join(' · ')}
          role="cell"
        >
          <span className="mes-nombre">{MESES[m.mes - 1]}</span>
          {m.alertas.length > 0 && <span className="alerta" aria-label="alerta">!</span>}
        </div>
      ))}
    </div>
  )
}

export function LeyendaCalendario() {
  return (
    <div className="leyenda">
      {Object.entries(ESTADOS).map(([k, v]) => (
        <span key={k}>
          <i className={`estado-${k}`} /> {v}
        </span>
      ))}
      <span>
        <i className="con-alerta-muestra">!</i> alerta (pase el cursor)
      </span>
    </div>
  )
}
