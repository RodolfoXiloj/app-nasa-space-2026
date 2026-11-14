import { messages } from '../i18n/messages.js'
import { useLocale, useT } from '../i18n/useT.js'
import { mesCorto } from '../i18n/months.js'
import { leerMotor } from '../i18n/motor.js'

export default function Calendario12({ calendario }) {
  const loc = useLocale()
  const t = useT()
  const estados = messages[loc]?.estado || messages.en.estado
  return (
    // Una lista de 12 meses: cada mes dice su estado en texto (no solo con el color) para el lector de pantalla.
    <ul className="calendario" aria-label={t('cal.table')} style={{ listStyle: 'none', padding: 0, margin: 0 }}>
      {calendario.map((mes) => {
        // Cultivo y avisos del mes en el idioma activo (campos `en` del JSON).
        const m = { ...mes, cultivo: leerMotor(mes, 'cultivo', loc).txt, alertas: leerMotor(mes, 'alertas', loc).txt || [] }
        return (
          <li
            key={m.mes}
            className={`mes estado-${m.estado}${m.alertas.length ? ' con-alerta' : ''}`}
            title={[estados[m.estado], m.cultivo, ...m.alertas].filter(Boolean).join(' · ')}
          >
            <span className="mes-nombre" aria-hidden="true">
              {mesCorto(m.mes, loc)}
            </span>
            {m.alertas.length > 0 && (
              <span className="alerta" aria-hidden="true">
                !
              </span>
            )}
            <span className="sr-solo">
              {[(messages[loc] || messages.en).mesLargo[m.mes - 1], estados[m.estado], m.cultivo, m.alertas.length ? `${t('cal.ariaMark')}: ${m.alertas.join(', ')}` : '']
                .filter(Boolean)
                .join(', ')}
            </span>
          </li>
        )
      })}
    </ul>
  )
}

export function LeyendaCalendario() {
  const loc = useLocale()
  const t = useT()
  const estados = messages[loc]?.estado || messages.en.estado
  return (
    <div className="leyenda" aria-hidden="true">
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