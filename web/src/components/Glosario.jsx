import { useLocale, useT } from '../i18n/useT.js'
import { leerMotor } from '../i18n/motor.js'

export default function Glosario({ res }) {
  const t = useT()
  const loc = useLocale()
  // Glosario y fuentes en el idioma activo (campos `en` del JSON); lo que falte va en español con lang="es".
  const m = (obj, campo) => leerMotor(obj, campo, loc)
  const lang = (x) => (x.txt && x.lang !== loc ? x.lang : undefined)
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
        {res.glosario.some((g) => lang(m(g, 'definicion'))) && <p className="sub">{t('glosario.dataEs')}</p>}
        <dl className="glosario">
          {res.glosario.map((g) => {
            const [termino, definicion] = [m(g, 'termino'), m(g, 'definicion')]
            return (
              <div key={g.termino}>
                <dt lang={lang(termino)}>{termino.txt}</dt>
                <dd lang={lang(definicion)}>{definicion.txt}</dd>
              </div>
            )
          })}
        </dl>
      </section>
      <section className="panel">
        <h2>{t('glosario.sources')}</h2>
        <ul className="fuentes">
          {res.fuentes.map((f) => {
            const [nombre, cita, resol] = [m(f, 'nombre'), m(f, 'cita'), m(f, 'resolucion')]
            return (
              <li key={f.id}>
                <b lang={lang(nombre)}>{nombre.txt}</b>
                {f.es_nasa && <span className="etiqueta nasa">NASA</span>}
                <p lang={lang(cita)}>{cita.txt}</p>
                <small>
                  <a href={f.url} target="_blank" rel="noreferrer">
                    {f.url}
                  </a>
                  {resol.txt ? ` · ${t('glosario.resolution')} ` : ''}
                  {resol.txt && <span lang={lang(resol)}>{resol.txt}</span>}
                  {f.fecha_consulta ? ' · ' : ''}
                  {f.fecha_consulta && (
                    <span className="sin-corte">
                      {t('glosario.consulted')} {f.fecha_consulta.slice(0, 10)}
                    </span>
                  )}
                </small>
              </li>
            )
          })}
        </ul>
      </section>
    </main>
  )
}