import { whereItFails } from '../i18n/evidence.js'
import { useLocale, useT } from '../i18n/useT.js'

export default function DondeFalla() {
  const loc = useLocale()
  const t = useT()
  const rows = whereItFails(loc)
  return (
    <section className="panel" id="donde-falla">
      <h2>{t('validacion.failsTitle')}</h2>
      <p className="sub">{t('validacion.failsSub')}</p>
      <div className="tabla-scroll">
        <table className="tabla-datos">
          <thead>
            <tr>
              <th>{t('validacion.colLimit')}</th>
              <th>{t('validacion.colFigure')}</th>
              <th>{t('validacion.colSource')}</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.limit}>
                <td>{r.limit}</td>
                <td>{r.figure}</td>
                <td>
                  <small>{r.source}</small>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}