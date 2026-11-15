// G1 y S1 (versión interactiva), solo para maíz con frijol: la biblioteca de data/explorar/{pid}.json.
// - AguaCiclo: la curva de agua de las tres opciones que muestra el sitio.
// - Biblioteca: el extensionista prueba cualquier plantilla que aplica, con los puntajes del motor en el escenario
//   base; el total se repondera con la prioridad elegida (los mismos pesos de res.pesos). La vista del agricultor
//   sigue con tres opciones.
import { useState } from 'react'
import CurvaAgua from './CurvaAgua.jsx'
import { listaMesesI18n } from '../i18n/months.js'
import { useTx } from '../i18n/explorar.js'

export function nombreEntrada(tx, b) {
  return (tx.loc === 'en' && b.nombre_corto_en) || b.nombre_corto
}

function total(p, pesos) {
  return Math.round(pesos.agua * p.agua + pesos.suelo * p.suelo + pesos.plagas * p.plagas)
}

export function AguaCiclo({ explorar, res }) {
  const tx = useTx()
  const bib = explorar?.biblioteca || []
  const orden = (res?.rotaciones || []).map((r) => r.id)
  const elegidas = orden.map((id) => bib.find((b) => b.id === id)).filter(Boolean)
  const [rid, setRid] = useState(null)
  if (!elegidas.length) return null
  const actual = elegidas.find((b) => b.id === rid) || elegidas[0]
  return (
    <section className="panel explorar-panel" aria-labelledby="agua-ciclo-titulo">
      <h2 id="agua-ciclo-titulo">{tx('curva.titulo')}</h2>
      <div className="selector-chips" role="group" aria-label={tx('curva.opcion')}>
        {elegidas.map((b) => (
          <button key={b.id} type="button" aria-pressed={b.id === actual.id} onClick={() => setRid(b.id)}>
            {nombreEntrada(tx, b)}
          </button>
        ))}
      </div>
      <CurvaAgua key={actual.id} entrada={actual} idPatron="rayas-ciclo" />
    </section>
  )
}

export default function Biblioteca({ explorar, res, prioridad = 'agua' }) {
  const tx = useTx()
  const bib = explorar?.biblioteca || []
  const [rid, setRid] = useState(null)
  if (bib.length < 2 || !res?.pesos?.por_prioridad) return null
  const pesos = res.pesos.por_prioridad[prioridad] || res.pesos.por_prioridad.agua
  const hoy = bib.find((b) => b.es_actual)
  const alternativas = bib.filter((b) => !b.es_actual)
  const sel = bib.find((b) => b.id === rid) || alternativas.find((b) => !b.elegida) || alternativas[0]
  const meses = (ms) => (ms.length ? listaMesesI18n(ms, tx.loc) : tx('biblioteca.ninguno'))
  const fila = (etq, f) => (
    <tr>
      <th scope="row">{etq}</th>
      <td className="num">{f(sel)}</td>
      {hoy && hoy.id !== sel.id && <td className="num">{f(hoy)}</td>}
    </tr>
  )
  const lista = (b, campo) => (tx.loc === 'en' ? b[`${campo}_en`] : b[campo]) || []
  return (
    <section className="panel explorar-panel" aria-labelledby="biblioteca-titulo">
      <h2 id="biblioteca-titulo">{tx('biblioteca.titulo')}</h2>
      <p className="sub">{tx('biblioteca.sub')}</p>
      <div className="selector-chips" role="group" aria-label={tx('biblioteca.elegir')}>
        {alternativas.map((b) => (
          <button key={b.id} type="button" aria-pressed={b.id === sel.id} onClick={() => setRid(b.id)}>
            {nombreEntrada(tx, b)}
            {b.elegida ? ` · ${tx('biblioteca.enOpciones')}` : ''}
          </button>
        ))}
      </div>
      <div className="biblioteca-ficha" aria-live="polite">
        <h3 lang={tx.loc === 'en' && !sel.nombre_en ? 'es' : undefined}>{(tx.loc === 'en' && sel.nombre_en) || sel.nombre}</h3>
        <div className="tabla-scroll" role="region" aria-label={tx('biblioteca.titulo')} tabIndex={0}>
          <table className="biblioteca-tabla">
            <thead>
              <tr>
                <td />
                <th scope="col">{nombreEntrada(tx, sel)}</th>
                {hoy && hoy.id !== sel.id && <th scope="col">{tx('biblioteca.comparada')}</th>}
              </tr>
            </thead>
            <tbody>
              {fila(tx('biblioteca.agua'), (b) => b.puntajes.agua)}
              {fila(tx('biblioteca.suelo'), (b) => b.puntajes.suelo)}
              {fila(tx('biblioteca.plagas'), (b) => b.puntajes.plagas)}
              {fila(tx('biblioteca.total'), (b) => total(b.puntajes, pesos))}
              {fila(tx('biblioteca.deficit'), (b) => `${b.deficit.mediana_pct} %`)}
              {fila(tx('biblioteca.meses'), (b) => meses(b.meses_cultivo))}
              {fila(tx('biblioteca.desnudos'), (b) => meses(b.meses_desnudos))}
              {fila(tx('biblioteca.quema'), (b) => (b.quema ? tx('biblioteca.conQuema') : tx('biblioteca.sinQuema')))}
            </tbody>
          </table>
        </div>
        {lista(sel, 'beneficios').length > 0 && (
          <>
            <h4>{tx('biblioteca.beneficios')}</h4>
            <ul>{lista(sel, 'beneficios').map((x) => <li key={x}>{x}</li>)}</ul>
          </>
        )}
        {lista(sel, 'riesgos').length > 0 && (
          <>
            <h4>{tx('biblioteca.riesgos')}</h4>
            <ul>{lista(sel, 'riesgos').map((x) => <li key={x}>{x}</li>)}</ul>
          </>
        )}
        <CurvaAgua key={sel.id} entrada={sel} idPatron="rayas-biblioteca" />
        <p className="nota">
          {tx('biblioteca.fuente')}:{' '}
          {tx.loc === 'es' ? sel.fuente : <span lang="es" className="cita">«{sel.fuente}»</span>}
        </p>
        {String(sel.fuente).includes('supuesto') && <p className="nota">{tx('biblioteca.revision')}</p>}
      </div>
    </section>
  )
}
