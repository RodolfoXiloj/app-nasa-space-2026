import { messages } from '../i18n/messages.js'
import { useLocale, useT } from '../i18n/useT.js'
import { mesCorto } from '../i18n/months.js'

export default function Calendario12({ calendario }) {
  const loc = useLocale()
  const t = useT()
  const estados = messages[loc]?.estado || messages.en.estado
  return (
    <div className="calendario" role="table" aria-label={t('cal.table')}>
      {calendario.map((m) => (
        <div
          key={m.mes}
          className={`mes estado-${m.estado}${m.alertas.length ? ' con-alerta' : ''}`}
          title={[estados[m.estado], m.cultivo, ...m.alertas].filter(Boolean).join(' · ')}
          role="cell"
        >
          <span className="mes-nombre">{mesCorto(m.mes, loc)}</span>
          {m.alertas.length > 0 && (
            <span className="alerta" aria-label={t('cal.ariaMark')}>
              !
            </span>
          )}
        </div>
      ))}
    </div>
  )
}

export function LeyendaCalendario() {
  const loc = useLocale()
  const t = useT()
  const estados = messages[loc]?.estado || messages.en.estado
  return (
    <div className="leyenda">
      {Object.entries(estados).map(([k, v]) => (
        <span key={k}>
          <i className={`estado-${k}`} /> {v}
        </span>
      ))}
      <span>
        <i className="con-alerta-muestra">!</i> {t('cal.mark')}
      </span>
    </div>
  )
}