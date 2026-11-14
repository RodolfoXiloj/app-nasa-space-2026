import { useEffect, useMemo, useState } from 'react'
import { cargarJSON } from './lib/datos.js'
import Mapa from './components/Mapa.jsx'
import Controles from './components/Controles.jsx'
import PanelSatelite from './components/PanelSatelite.jsx'
import Clima from './components/Clima.jsx'
import Rotaciones from './components/Rotaciones.jsx'
import Tarjeta from './components/Tarjeta.jsx'
import Validacion from './components/Validacion.jsx'
import Glosario from './components/Glosario.jsx'
import { LineaObservacion2026 } from './components/Observacion2026.jsx'

const PESTANAS = [
  ['parcela', 'Parcela'],
  ['validacion', 'Validación'],
  ['glosario', 'Glosario y fuentes'],
]

export default function App() {
  const [indice, setIndice] = useState(null)
  const [pid, setPid] = useState(null)
  const [cultivo, setCultivo] = useState('maiz_frijol')
  const [prioridad, setPrioridad] = useState('agua')
  const [lluvia, setLluvia] = useState(0)
  const [temp, setTemp] = useState(0)
  const [res, setRes] = useState(null)
  const [error, setError] = useState(null)
  const [pestana, setPestana] = useState('parcela')
  const [validacion, setValidacion] = useState(null)

  useEffect(() => {
    cargarJSON('data/validacion.json')
      .then(setValidacion)
      .catch(() => setValidacion(null))
  }, [])

  // Índice de parcelas; si no hay ninguna calculada, se usa el contrato de ejemplo.
  useEffect(() => {
    cargarJSON('data/parcelas.json')
      .then((j) => {
        setIndice(j.parcelas)
        const primera = j.parcelas.find((p) => p.disponible)
        setPid(primera ? primera.id : '__ejemplo__')
      })
      .catch(() => {
        setIndice([])
        setPid('__ejemplo__')
      })
  }, [])

  const parcela = useMemo(() => indice?.find((p) => p.id === pid), [indice, pid])

  function verObservacion2026() {
    setPestana('validacion')
    setTimeout(() => document.getElementById('observacion-2026')?.scrollIntoView({ behavior: 'smooth' }), 60)
  }

  useEffect(() => {
    if (!pid) return
    let ruta = 'data/ejemplo.json'
    if (pid !== '__ejemplo__') {
      if (!parcela?.disponible) {
        setRes(null)
        return
      }
      ruta = parcela.archivos[cultivo] || parcela.archivos.maiz_frijol
    }
    setError(null)
    cargarJSON(ruta)
      .then((j) => setRes(j))
      .catch((e) => setError(e.message))
  }, [pid, cultivo, parcela])

  return (
    <div className="app">
      <header className="cabecera no-imprimir">
        <div>
          <h1>Milpa Resiliente</h1>
          <p className="lema">
            El satélite ya sabe cómo ha usado su parcela. Le mostramos qué rotación aguanta mejor la próxima canícula y por
            qué, para que el técnico y el agricultor decidan.
          </p>
        </div>
        <nav className="pestanas" aria-label="Secciones">
          {PESTANAS.map(([id, txt]) => (
            <button key={id} type="button" className={pestana === id ? 'activa' : ''} aria-current={pestana === id ? 'page' : undefined} onClick={() => setPestana(id)}>
              {txt}
            </button>
          ))}
        </nav>
      </header>

      {res?.meta?.tipo === 'ejemplo' && (
        <div className="banda-ejemplo no-imprimir" role="status">
          DATOS DE EJEMPLO: este archivo sirve para desarrollar la web; no es una recomendación.
        </div>
      )}
      {error && <div className="banda-error no-imprimir">{error}</div>}
      {pestana === 'parcela' && (
        <LineaObservacion2026 obs={validacion?.observacion_2026} onDetalle={verObservacion2026} />
      )}

      {pestana === 'parcela' && (
        <main className="contenido">
          <section className="fila-superior no-imprimir">
            <div className="columna-mapa">
              <Mapa parcelas={indice || []} seleccion={pid} onSeleccion={setPid} res={res} />
              <Controles
                indice={indice || []}
                pid={pid}
                setPid={setPid}
                cultivo={cultivo}
                setCultivo={setCultivo}
                prioridad={prioridad}
                setPrioridad={setPrioridad}
                lluvia={lluvia}
                setLluvia={setLluvia}
                temp={temp}
                setTemp={setTemp}
                res={res}
              />
            </div>
            <div className="columna-datos">
              {res ? (
                <>
                  <PanelSatelite res={res} />
                  <Clima res={res} />
                </>
              ) : (
                <div className="tarjeta-vacia">
                  {parcela && !parcela.disponible
                    ? `Parcela pendiente: falta en la caché ${parcela.faltan.join(', ')}. Corra la precarga y la exportación.`
                    : 'Cargando…'}
                </div>
              )}
            </div>
          </section>
          {res && (
            <>
              <Rotaciones res={res} lluvia={lluvia} temp={temp} prioridad={prioridad} />
              <Tarjeta res={res} lluvia={lluvia} temp={temp} prioridad={prioridad} />
              {res.meta.datos_de_ejemplo?.length > 0 && (
                <details className="pendientes no-imprimir">
                  <summary>Respaldos y vacíos de datos en esta parcela ({res.meta.datos_de_ejemplo.length})</summary>
                  <ul>
                    {res.meta.datos_de_ejemplo.map((t) => (
                      <li key={t}>{t}</li>
                    ))}
                  </ul>
                </details>
              )}
            </>
          )}
        </main>
      )}
      {pestana === 'validacion' && <Validacion res={res} validacion={validacion} />}
      {pestana === 'glosario' && <Glosario res={res} />}

      <footer className="pie no-imprimir">
        <p>{res?.aviso || 'Milpa Resiliente apoya, no reemplaza, al técnico ni al agricultor.'}</p>
        <p>
          Prototipo local de referencia. Los audios de las tarjetas son voz sintética generada con IA (edge-tts); los
          textos y las cifras salen de plantillas y reglas del motor, no de un modelo de lenguaje.
        </p>
        <p>
          NASA Space Apps Challenge 2026 · Reto «Field Shift: Adapting Farms with NASA Data» · Equipo «A dream», Guatemala.
          Contrato {res?.version_contrato || '1.0'} · motor {res?.meta?.motor_version || '—'} · generado{' '}
          {res?.meta?.generado || '—'}
        </p>
      </footer>
    </div>
  )
}
