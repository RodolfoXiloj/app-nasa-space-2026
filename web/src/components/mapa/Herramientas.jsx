// Herramientas del mapa de Evidence (versión interactiva):
// - Huellas: el borde o el radio de lo que ve cada producto alrededor de la parcela (data/explorar/{pid}.json,
//   calculado en motor/huellas.py). Apagadas al abrir: la celda de POWER cubre casi todo el mapa.
// - Comparador: NDVI de época seca a la izquierda y de época de lluvias a la derecha, con una división que se
//   mueve con el dedo, el ratón o las flechas. Usa las teselas que ya están guardadas en el sitio.
// - Opacidad de las capas NDVI.
// Con movimiento reducido no hay vuelos animados.
import { useEffect, useRef, useState } from 'react'
import L from 'leaflet'
import { Circle, Pane, Polygon, TileLayer, Tooltip, useMap } from 'react-leaflet'
import { useTx } from '../../i18n/explorar.js'

const ESTILO = {
  parcela: { color: '#1d2b1a', weight: 3, fillOpacity: 0.25, fillColor: '#e0b43a' },
  modis: { color: '#3f7d3a', weight: 3, fillOpacity: 0.08 },
  firms: { color: '#b23c17', weight: 3, dashArray: '8 6', fillOpacity: 0.04 },
  chirps: { color: '#1f4f7a', weight: 3, dashArray: '2 6', fillOpacity: 0 },
  smap: { color: '#6b4a8a', weight: 3, dashArray: '12 6 2 6', fillOpacity: 0 },
  power: { color: '#55624f', weight: 4, dashArray: '16 8', fillOpacity: 0 },
}

export const menosMovimiento = () =>
  typeof window !== 'undefined' && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches

const MES_ES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
const MES_EN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

export function fechaLarga(iso, loc) {
  const [a, m, d] = iso.split('-').map(Number)
  return loc === 'es' ? `${d} de ${MES_ES[m - 1]} de ${a}` : `${MES_EN[m - 1]} ${d}, ${a}`
}

export function limitesHuella(h, centro) {
  return h.forma === 'circulo' ? L.latLng(centro).toBounds(h.radio_m * 2) : L.latLngBounds(h.poligono)
}

export function nombreHuella(tx, h) {
  return tx(`huellas.nombres.${h.id}`, { lado: h.lado_m, r: h.radio_m })
}

export function areaTexto(tx, ha) {
  if (ha >= 1000) return `${tx.num(ha / 100, 0)} km²`
  return `${tx.num(ha, ha < 10 ? 2 : 1)} ha`
}

// Dentro del mapa: las seis huellas.
export function HuellasCapa({ explorar, activa }) {
  const tx = useTx()
  if (!explorar || !activa) return null
  const centro = [explorar.lat, explorar.lon]
  return (
    <Pane name="huellas" style={{ zIndex: 420 }}>
      {[...explorar.huellas].reverse().map((h) => {
        const estilo = ESTILO[h.id] || {}
        const tip = (
          <Tooltip sticky>
            <strong>{nombreHuella(tx, h)}</strong>
            <br />
            {areaTexto(tx, h.area_ha)}
            {h.id === 'smap' && h.con_datos === false ? ` · ${tx('huellas.sinSmap')}` : ''}
          </Tooltip>
        )
        return h.forma === 'circulo' ? (
          <Circle key={h.id} center={centro} radius={h.radio_m} pathOptions={estilo}>
            {tip}
          </Circle>
        ) : (
          <Polygon key={h.id} positions={h.poligono} pathOptions={estilo}>
            {tip}
          </Polygon>
        )
      })}
    </Pane>
  )
}

// Dentro del mapa: deja el mapa en una variable para los botones de fuera.
export function TomarMapa({ alTomar }) {
  const map = useMap()
  useEffect(() => {
    alTomar(map)
  }, [map, alTomar])
  return null
}

// Dentro del mapa: dos capas recortadas a cada lado de la división.
export function Comparador({ izq, der, pos, caja, opacidad }) {
  const map = useMap()
  useEffect(() => {
    const actualizar = () => {
      const a = map.getPane('cmpIzq')
      const b = map.getPane('cmpDer')
      if (!a || !b) return
      const size = map.getSize()
      const nw = map.containerPointToLayerPoint([0, 0])
      const se = map.containerPointToLayerPoint(size)
      const x = map.containerPointToLayerPoint([size.x * pos, 0]).x
      a.style.clip = `rect(${nw.y}px, ${x}px, ${se.y}px, ${nw.x}px)`
      b.style.clip = `rect(${nw.y}px, ${se.x}px, ${se.y}px, ${x}px)`
    }
    actualizar()
    map.on('move zoom resize zoomend moveend', actualizar)
    return () => map.off('move zoom resize zoomend moveend', actualizar)
  }, [map, pos])
  const comun = { bounds: caja, minNativeZoom: 7, maxNativeZoom: 9, maxZoom: 16, opacity: opacidad }
  return (
    <>
      <Pane name="cmpIzq" style={{ zIndex: 250 }}>
        <TileLayer url={izq} {...comun} />
      </Pane>
      <Pane name="cmpDer" style={{ zIndex: 251 }}>
        <TileLayer url={der} {...comun} />
      </Pane>
    </>
  )
}

// Sobre el mapa: la línea de la división y el nombre de cada lado (decorativo: el texto va también abajo).
export function EtiquetasComparador({ pos, fechas }) {
  const tx = useTx()
  return (
    <div className="cmp-capa" aria-hidden="true">
      <div className="cmp-division" style={{ left: `${pos * 100}%` }} />
      <span className="cmp-etiqueta cmp-etiqueta--izq">◀ {tx('capas.izquierda', { fecha: fechaLarga(fechas.seca, tx.loc) })}</span>
      <span className="cmp-etiqueta cmp-etiqueta--der">{tx('capas.derecha', { fecha: fechaLarga(fechas.lluvia, tx.loc) })} ▶</span>
    </div>
  )
}

// Fuera del mapa: botones, lista de huellas, comparador y opacidad.
export function Herramientas({ mapa, explorar, huellas, setHuellas, comparar, setComparar, pos, setPos, opacidad, setOpacidad, fechas }) {
  const tx = useTx()
  const [paso, setPaso] = useState(null)
  const reloj = useRef(null)
  const centro = explorar ? [explorar.lat, explorar.lon] : null

  const acercar = (h) => {
    if (!mapa || !centro) return
    const b = limitesHuella(h, centro)
    if (menosMovimiento()) mapa.fitBounds(b, { padding: [24, 24], animate: false })
    else mapa.flyToBounds(b, { padding: [24, 24], duration: 1.1 })
  }

  const detener = () => {
    clearTimeout(reloj.current)
    reloj.current = null
    setPaso(null)
  }

  useEffect(() => detener, [])
  useEffect(detener, [explorar])

  // El NDVI guardado llega hasta el zoom 9: para comparar, el mapa se aleja al paisaje alrededor de la parcela.
  const abrirComparar = (si) => {
    setComparar(si)
    if (!si || !mapa) return
    const zoom = Math.min(mapa.getZoom(), 10)
    const destino = centro || mapa.getCenter()
    if (menosMovimiento()) mapa.setView(destino, zoom, { animate: false })
    else mapa.flyTo(destino, zoom, { duration: 0.8 })
  }

  const recorrer = () => {
    if (!explorar) return
    if (paso != null) return detener()
    setHuellas(true)
    const lista = explorar.huellas
    const ir = (i) => {
      setPaso(i)
      acercar(lista[i])
      if (i + 1 < lista.length) reloj.current = setTimeout(() => ir(i + 1), menosMovimiento() ? 2500 : 2200)
      else reloj.current = setTimeout(() => setPaso(null), 2200)
    }
    ir(0)
  }

  return (
    <div className="mapa-herramientas">
      <div className="mapa-botones">
        {explorar && (
          <>
            <label className="mapa-check">
              <input type="checkbox" checked={huellas} onChange={(e) => setHuellas(e.target.checked)} />
              <span>{tx('huellas.mostrar')}</span>
            </label>
            <button type="button" onClick={recorrer} aria-pressed={paso != null}>
              {paso != null ? tx('huellas.detener') : tx('huellas.recorrido')}
            </button>
          </>
        )}
        <button type="button" onClick={() => abrirComparar(!comparar)} aria-pressed={comparar}>
          {comparar ? tx('capas.cerrarComparar') : tx('capas.comparar')}
        </button>
      </div>

      {comparar && (
        <div className="mapa-rango">
          <label htmlFor="cmp-pos">{tx('capas.divisor')}</label>
          <input id="cmp-pos" type="range" min="0" max="100" step="1" value={Math.round(pos * 100)} onChange={(e) => setPos(Number(e.target.value) / 100)} aria-valuetext={`${Math.round(pos * 100)} %`} />
          <p className="nota">
            ◀ {tx('capas.izquierda', { fecha: fechaLarga(fechas.seca, tx.loc) })} · {tx('capas.derecha', { fecha: fechaLarga(fechas.lluvia, tx.loc) })} ▶
          </p>
        </div>
      )}

      <div className="mapa-rango">
        <label htmlFor="ndvi-op">{tx('capas.opacidad')}</label>
        <input id="ndvi-op" type="range" min="0" max="100" step="5" value={Math.round(opacidad * 100)} onChange={(e) => setOpacidad(Number(e.target.value) / 100)} aria-valuetext={`${Math.round(opacidad * 100)} %`} />
      </div>
      <p className="nota">{tx('capas.nota')}</p>

      {explorar && huellas && (
        <section className="huellas-lista" aria-labelledby="huellas-titulo">
          <h3 id="huellas-titulo">{tx('huellas.titulo')}</h3>
          <p className="nota">{tx('huellas.intro')}</p>
          <ol>
            {explorar.huellas.map((h, i) => (
              <li key={h.id} className={`huella huella--${h.id}${paso === i ? ' activa' : ''}`} aria-current={paso === i ? 'step' : undefined}>
                <i aria-hidden="true" />
                <span>
                  {nombreHuella(tx, h)} · <b>{areaTexto(tx, h.area_ha)}</b>
                  {h.id === 'smap' && h.con_datos === false ? ` · ${tx('huellas.sinSmap')}` : ''}
                </span>
                <button type="button" className="enlace" onClick={() => acercar(h)}>
                  {tx('huellas.ver')}
                </button>
              </li>
            ))}
          </ol>
        </section>
      )}
    </div>
  )
}
