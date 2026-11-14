import { useEffect, useMemo, useState } from 'react'
import { cargarJSON } from './lib/datos.js'
import Mapa from './components/Mapa.jsx'
import Controles from './components/Controles.jsx'
import PanelSatelite from './components/PanelSatelite.jsx'
import Clima from './components/Clima.jsx'
import Rotaciones from './components/Rotaciones.jsx'
import FuturosNasa from './components/FuturosNasa.jsx'
import Tarjeta from './components/Tarjeta.jsx'
import Validacion from './components/Validacion.jsx'
import Glosario from './components/Glosario.jsx'
import { LineaObservacion2026 } from './components/Observacion2026.jsx'
import { useLocale, useT } from './i18n/useT.js'
import { leerMotor } from './i18n/motor.js'

const PESTANAS = ['parcela', 'validacion', 'glosario']

// Con movimiento reducido el salto a la observación 2026 es instantáneo.
const movimiento = () => (window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth')

export default function App({ pidInicial = null }) {
  const t = useT()
  const loc = useLocale()
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
  const [futuros, setFuturos] = useState(null)

  useEffect(() => {
    cargarJSON('data/futuros_nasa.json')
      .then(setFuturos)
      .catch(() => setFuturos(null))
  }, [])

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
        const primera = j.parcelas.find((p) => p.id === pidInicial && p.disponible) || j.parcelas.find((p) => p.disponible)
        setPid(primera ? primera.id : '__ejemplo__')
      })
      .catch(() => {
        setIndice([])
        setPid('__ejemplo__')
      })
  }, [])

  const parcela = useMemo(() => indice?.find((p) => p.id === pid), [indice, pid])
  // Textos del motor en el idioma activo; si falta el inglés, va el español marcado con lang="es".
  const aviso = leerMotor(res, 'aviso', loc)
  const vacios = leerMotor(res?.meta, 'datos_de_ejemplo', loc)
  const langDe = (m) => (m.txt && m.lang !== loc ? m.lang : undefined)

  function verObservacion2026() {
    setPestana('validacion')
    setTimeout(() => document.getElementById('observacion-2026')?.scrollIntoView({ behavior: movimiento() }), 60)
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
          <p className="lema">{t('app.tagline')}</p>
        </div>
        <nav className="pestanas" aria-label={t('app.sections')}>
          {PESTANAS.map((id) => (
            <button key={id} type="button" className={pestana === id ? 'activa' : ''} aria-current={pestana === id ? 'page' : undefined} onClick={() => setPestana(id)}>
              {t(`app.tabs.${id}`)}
            </button>
          ))}
        </nav>
      </header>

      {res?.meta?.tipo === 'ejemplo' && (
        <div className="banda-ejemplo no-imprimir" role="status">
          {t('app.example')}
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
                    ? t('parcelaVacia.pending', { lista: parcela.faltan.join(', ') })
                    : t('common.loading')}
                </div>
              )}
            </div>
          </section>
          {res && (
            <>
              <Rotaciones res={res} lluvia={lluvia} temp={temp} prioridad={prioridad} />
              <FuturosNasa futuros={futuros} pid={res.parcela?.id} cultivo={cultivo} />
              <Tarjeta res={res} lluvia={lluvia} temp={temp} prioridad={prioridad} />
              {vacios.txt?.length > 0 && (
                <details className="pendientes no-imprimir">
                  <summary>{t('app.gaps', { n: vacios.txt.length })}</summary>
                  <ul lang={langDe(vacios)}>
                    {vacios.txt.map((txt) => (
                      <li key={txt}>{txt}</li>
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
        <p lang={langDe(aviso)}>{aviso.txt || t('app.aviso')}</p>
        <p className="pie-ia">{t('app.ia')}</p>
        <p>
          {t('app.credit')}{' '}
          {t('app.build', {
            contrato: res?.version_contrato || '1.0',
            motor: res?.meta?.motor_version || t('common.dash'),
            generado: res?.meta?.generado || t('common.dash'),
          })}
        </p>
      </footer>
    </div>
  )
}
