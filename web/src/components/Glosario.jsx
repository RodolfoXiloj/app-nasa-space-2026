export default function Glosario({ res }) {
  if (!res) return <main className="contenido"><div className="tarjeta-vacia">Cargando…</div></main>
  return (
    <main className="contenido dos-columnas">
      <section className="panel">
        <h2>¿Qué significa?</h2>
        <dl className="glosario">
          {res.glosario.map((g) => (
            <div key={g.termino}>
              <dt>{g.termino}</dt>
              <dd>{g.definicion}</dd>
            </div>
          ))}
        </dl>
      </section>
      <section className="panel">
        <h2>Fuentes y citas</h2>
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
                {f.resolucion ? ` · resolución ${f.resolucion}` : ''}
                {f.fecha_consulta ? ' · ' : ''}
                {f.fecha_consulta && <span className="sin-corte">consultado {f.fecha_consulta.slice(0, 10)}</span>}
              </small>
            </li>
          ))}
        </ul>
      </section>
    </main>
  )
}
