import { productDecisions } from '../i18n/evidence.js'
import { useLocale, useT } from '../i18n/useT.js'

export default function ProductoDecision() {
  const loc = useLocale()
  const t = useT()
  const rows = productDecisions(loc)
  return (
    <section className="panel" id="producto-decision">
      <h2>{t('validacion.productTitle')}</h2>
      <p className="sub">{t('validacion.productSub')}</p>
      <div className="tabla-scroll" role="region" aria-label={t('a11y.table', { titulo: t('validacion.productTitle') })} tabIndex={0}>
        <table className="tabla-datos">
          <thead>
            <tr>
              <th>{t('validacion.colProduct')}</th>
              <th>{t('validacion.colDecision')}</th>
              <th>{t('validacion.colSource')}</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.product}>
                <td>{r.product}</td>
                <td>{r.decision}</td>
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