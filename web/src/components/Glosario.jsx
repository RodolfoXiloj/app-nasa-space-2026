import { useLocale, useT } from '../i18n/useT.js'

export default function Glosario({ res }) {
  const t = useT()
  const loc = useLocale()
  if (!res) {
    return (
      <main className="contenido">
        <div className="tarjeta-vacia">{t('common.loading')}</div>
      </main>
    )
  }
  return (
    <main className="contenido dos-columnas">
      <section className="panel">
        <h2>{t('glosario.terms')}</h2>
        {loc === 'en' && <p className="sub">{t('glosario.dataEs')}</p>}
        <dl className="glosario" lang={loc === 'es' ? undefined : 'es'}>
          {res.glosario.map((g) => (
            <div key={g.termino}>
              <dt>{g.termino}</dt>
              <dd>{g.definicion}</dd>
            </div>
          ))}
        </dl>
      </section>
      <section className="panel">
        <h2>{t('glosario.sources')}</h2>
        <ul className="fuentes">
          {res.fuentes.map((f) => (
            <li key={f.id}>
              <b>{f.nombre}</b>
              {f.es_nasa && <span className="etiqueta nasa">NASA</span>}
              <p>{f.cita}</p>
              <small>
                <a href={f.url} target="_blank" rel="noreferrer">
                  {f.url}
                </a>
                {f.resolucion ? ` · ${t('glosario.resolution')} ${f.resolucion}` : ''}
                {f.fecha_consulta ? ' · ' : ''}
                {f.fecha_consulta && (
                  <span className="sin-corte">
                    {t('glosario.consulted')} {f.fecha_consulta.slice(0, 10)}
                  </span>
                )}
              </small>
            </li>
          ))}
        </ul>
      </section>
    </main>
  )
}