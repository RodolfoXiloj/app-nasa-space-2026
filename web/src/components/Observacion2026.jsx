// Observación preliminar de julio-agosto 2026: viene de validacion.json (pipeline/validacion/validar.py).
// Es una observación del pasado, no un pronóstico; el motor no la usa en puntajes, confianza ni audio.

const mm = (v) => `${Number(v).toFixed(1)} mm`
const hum = (v) => Number(v).toFixed(3)

export function LineaObservacion2026({ obs, onDetalle }) {
  if (!obs) return null
  return (
    <div className="banda-obs no-imprimir" role="note">
      <b>{obs.titulo}.</b> {obs.resumen}{' '}
      <button type="button" className="enlace" onClick={onDetalle}>
        Ver detalle y límites
      </button>
    </div>
  )
}

export default function Observacion2026({ obs }) {
  if (!obs) return null
  return (
    <section className="panel" id="observacion-2026">
      <h2>{obs.titulo}</h2>
      <p className="sub">
        Fuera del periodo del motor (2001–2025): no cambia puntajes, confianza ni audio. Generado desde la caché con{' '}
        <code>python -m pipeline.validacion.validar</code>.
      </p>
      <p>{obs.resumen}</p>

      <h3>Lluvia de julio y agosto (CHIRPS v3 mensual, producto final)</h3>
      <div className="tabla-scroll">
        <table className="tabla-datos">
          <thead>
            <tr>
              <th>Parcela</th>
              <th>Julio + agosto 2026</th>
              <th>Mediana {obs.lluvia_chirps[0]?.periodo_referencia}</th>
              <th>% de la mediana</th>
              <th>Mínimo anterior</th>
              <th>Años más secos que 2026</th>
            </tr>
          </thead>
          <tbody>
            {obs.lluvia_chirps.map((x) => (
              <tr key={x.id}>
                <td>{x.municipio}</td>
                <td className="num">{mm(x.mm_2026)}</td>
                <td className="num">{mm(x.mediana_mm)}</td>
                <td className="num">{x.pct_de_la_mediana} %</td>
                <td className="num">
                  {mm(x.minimo_anterior_mm)} ({x.anio_minimo_anterior})
                </td>
                <td className="num">
                  {x.anios_mas_secos_que_2026} de {x.n_anios_referencia}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {obs.smap_celdas?.length > 0 && (
        <>
          <h3>Humedad del suelo de julio y agosto (SMAP, por celda de 9 km)</h3>
          <div className="tabla-scroll">
            <table className="tabla-datos">
              <thead>
                <tr>
                  <th>Celda</th>
                  <th>Parcelas</th>
                  <th>2026</th>
                  <th>Mínimo anterior</th>
                  <th>¿El más bajo?</th>
                </tr>
              </thead>
              <tbody>
                {obs.smap_celdas.map((x) => (
                  <tr key={`${x.celda.linea}-${x.celda.muestra}`}>
                    <td>
                      {x.celda.linea}, {x.celda.muestra}
                    </td>
                    <td>{x.parcelas.join(', ')}</td>
                    <td className="num">{hum(x.m3m3_2026)} m³/m³</td>
                    <td className="num">
                      {hum(x.minimo_anterior_m3m3)} ({x.anio_minimo_anterior})
                    </td>
                    <td>
                      {x.es_el_mas_bajo ? 'sí' : 'no'}, de {x.n_anios} años ({x.periodo})
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      <h3>Qué dicen otros (no son la fuente de las cifras de arriba)</h3>
      <ul className="lista-compacta">
        {obs.reportes_publicos.map((e) => (
          <li key={e.id}>
            <a href={e.url} target="_blank" rel="noreferrer">
              {e.fuente}
            </a>{' '}
            ({e.relacion}): «{e.cita}». {e.nota}
          </li>
        ))}
      </ul>

      <h3>Límites</h3>
      <ul className="lista-compacta">
        {obs.limites.map((t) => (
          <li key={t}>{t}</li>
        ))}
      </ul>
    </section>
  )
}
