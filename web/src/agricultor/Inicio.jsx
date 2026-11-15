// Raíz de la web: abre en la vista «Para el agricultor» y lleva a la vista «Evidence/Evidencia» con un
// toque (#evidence en la dirección). Evidence se carga con import() solo al abrirla, con el mapa y las
// gráficas; la primera pantalla no las descarga.
import { Component, Suspense, lazy, useEffect, useRef, useState, useSyncExternalStore } from 'react'
import { getLocale, guardado, setLocale, subscribeLocale } from '../i18n/store.js'
import VistaAgricultor from './VistaAgricultor.jsx'
import { TEXTOS } from './textos.js'
import './agricultor.css'

// Lee un JSON de public/. Es el mismo cargarJSON de lib/datos.js, copiado aquí a propósito: si esta vista
// importara lib/datos.js, ese archivo (con los puntajes que solo usa Evidence) iría en la primera pantalla.
const cargarJSON = (ruta) =>
  fetch(import.meta.env.BASE_URL + ruta).then((r) => {
    if (!r.ok) throw new Error(`${ruta} (${r.status})`)
    return r.json()
  })

const Evidencia = lazy(() => import('./Evidencia.jsx'))
const HASH_EVIDENCIA = '#evidence'

const vistaDeHash = () => (window.location.hash === HASH_EVIDENCIA ? 'evidencia' : 'agricultor')

// Si el bloque de Evidence no llega (sin red y sin copia en caché), se dice qué pasó y cómo reintentar.
class FalloEvidencia extends Component {
  state = { fallo: false }
  static getDerivedStateFromError() {
    return { fallo: true }
  }
  render() {
    if (!this.state.fallo) return this.props.children
    const t = TEXTOS[this.props.idioma]
    return (
      <div className="agr agr-fallo" role="alert">
        <p>{t.errorEvidencia}</p>
        <button type="button" className="agr-boton agr-boton--linea" onClick={() => window.location.reload()}>
          {t.reintentar}
        </button>
      </div>
    )
  }
}

export default function Inicio() {
  // Un solo idioma activo en toda la web: el del store de i18n (inglés por defecto, se recuerda en
  // localStorage). El selector de esta vista y el de Evidence escriben en el mismo lugar.
  const idioma = useSyncExternalStore(subscribeLocale, getLocale, () => 'en')
  const [vista, setVista] = useState(vistaDeHash)
  const [indice, setIndice] = useState(null)
  const [pid, setPid] = useState(null)
  const [res, setRes] = useState(null)
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState(false)
  const botonVolver = useRef(null)
  const abrioDesdeAqui = useRef(false)
  const primeraVez = useRef(true)

  useEffect(() => {
    const alCambiar = () => setVista(vistaDeHash())
    window.addEventListener('hashchange', alCambiar)
    return () => window.removeEventListener('hashchange', alCambiar)
  }, [])

  // Al cambiar de vista: arriba de la página y el foco en el botón que regresa o en el que abrió Evidence.
  useEffect(() => {
    if (primeraVez.current) {
      primeraVez.current = false
      return
    }
    window.scrollTo(0, 0)
    const destino = vista === 'evidencia' ? botonVolver.current : document.querySelector('.agr-evidencia')
    if (destino) destino.focus({ preventScroll: true })
  }, [vista])

  useEffect(() => {
    cargarJSON('data/parcelas.json')
      .then((j) => {
        setIndice(j.parcelas)
        // Primero la parcela guardada con «Guardar para usar sin señal» (src/kit/sinSenal.js la recuerda con esta
        // clave): sin señal es la que está en el teléfono. Si no hay ninguna, la primera disponible.
        const guardada = guardado('milpa-parcela')
        const primera = j.parcelas.find((p) => p.disponible && p.id === guardada) || j.parcelas.find((p) => p.disponible)
        setPid(primera ? primera.id : null)
        if (!primera) setCargando(false)
      })
      .catch(() => {
        setIndice([])
        setCargando(false)
        setError(true)
      })
  }, [])

  useEffect(() => {
    const parcela = (indice || []).find((p) => p.id === pid)
    if (!parcela || !parcela.disponible) return
    let vigente = true
    setCargando(true)
    setError(false)
    // La vista del agricultor usa el cultivo que declara la parcela (maíz con frijol).
    cargarJSON(parcela.archivos.maiz_frijol)
      .then((j) => vigente && setRes(j))
      .catch(() => {
        if (!vigente) return
        setRes(null)
        setError(true)
      })
      .finally(() => vigente && setCargando(false))
    return () => {
      vigente = false
    }
  }, [indice, pid])

  function abrirEvidencia() {
    abrioDesdeAqui.current = true
    window.location.hash = HASH_EVIDENCIA
  }

  function volver() {
    if (abrioDesdeAqui.current) {
      abrioDesdeAqui.current = false
      window.history.back()
      return
    }
    window.history.replaceState(null, '', window.location.pathname + window.location.search)
    setVista('agricultor')
  }

  const t = TEXTOS[idioma]

  if (vista === 'evidencia') {
    return (
      <>
        <nav className="agr-barra" aria-label={t.evidencia}>
          <button ref={botonVolver} type="button" className="agr-boton agr-boton--linea" onClick={volver}>
            <span aria-hidden="true">←</span> {t.volver}
          </button>
        </nav>
        <FalloEvidencia idioma={idioma}>
          <Suspense fallback={<p className="agr agr-cargando" role="status">{t.cargandoEvidencia}</p>}>
            <Evidencia pidInicial={pid} />
          </Suspense>
        </FalloEvidencia>
      </>
    )
  }

  return (
    <VistaAgricultor
      idioma={idioma}
      setIdioma={setLocale}
      indice={indice}
      pid={pid}
      setPid={setPid}
      res={res}
      cargando={cargando}
      error={error}
      onEvidencia={abrirEvidencia}
    />
  )
}
