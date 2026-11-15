// M5: el relieve alrededor de la parcela en 3D (MapLibre GL JS). Llega con import() solo cuando alguien toca
// «Ver el relieve en 3D»: ni la primera pantalla ni Evidence cargan este archivo por su cuenta.
// - Relieve: teselas Terrarium guardadas en web/public/terreno/ (pipeline/clientes/terreno.py; SRTM, cortesía
//   del USGS, vía Terrain Tiles de Mapzen), exagerado 1.5 veces, y sombreado.
// - Imagen: Sentinel-2 sin nubes (EOX) con señal; sin señal queda la capa MODIS guardada en el sitio.
// - Encima, las huellas de cada producto (data/explorar/{pid}.json) pegadas al terreno.
// La alternativa en texto da la altitud y la pendiente que ya trae el JSON del motor (parcela.terreno).
import { useEffect, useRef } from 'react'
import { Map as Mapa3D, setWorkerUrl } from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import urlTrabajador from 'maplibre-gl/dist/maplibre-gl-worker.mjs?url'
import { useTx } from '../../i18n/explorar.js'
import { menosMovimiento } from './Herramientas.jsx'

setWorkerUrl(urlTrabajador)

const EXAGERACION = 1.5
const CAJA = [-89.64, 14.586, -89.214, 15.021]
const COLOR = { parcela: '#e0b43a', modis: '#3f7d3a', firms: '#b23c17', chirps: '#1f4f7a', smap: '#6b4a8a', power: '#55624f' }
const VISTA = { zoom: 13.4, pitch: 62, bearing: -28 }

function circulo([lat, lon], radio, n = 64) {
  const R = 6371008.8
  const pts = []
  for (let i = 0; i <= n; i++) {
    const a = (2 * Math.PI * i) / n
    const dLat = (radio * Math.cos(a)) / R
    const dLon = (radio * Math.sin(a)) / (R * Math.cos((lat * Math.PI) / 180))
    pts.push([lon + (dLon * 180) / Math.PI, lat + (dLat * 180) / Math.PI])
  }
  return pts
}

function geoHuellas(explorar) {
  const centro = [explorar.lat, explorar.lon]
  return {
    type: 'FeatureCollection',
    features: explorar.huellas.map((h) => {
      const anillo = h.forma === 'circulo' ? circulo(centro, h.radio_m) : [...h.poligono, h.poligono[0]].map(([la, lo]) => [lo, la])
      return { type: 'Feature', properties: { id: h.id, color: COLOR[h.id] || '#1d2b1a' }, geometry: { type: 'LineString', coordinates: anillo } }
    }),
  }
}

export default function Relieve3D({ explorar, res, onCerrar }) {
  const tx = useTx()
  const caja = useRef(null)
  const mapa = useRef(null)
  const base = new URL(import.meta.env.BASE_URL, window.location.href).href
  const centro = [explorar.lon, explorar.lat]

  useEffect(() => {
    const quieto = menosMovimiento()
    const m = new Mapa3D({
      container: caja.current,
      center: centro,
      zoom: quieto ? VISTA.zoom : 11,
      pitch: quieto ? VISTA.pitch : 0,
      bearing: quieto ? VISTA.bearing : 0,
      maxPitch: 75,
      // Los créditos van en una línea visible debajo del mapa (el recuadro de MapLibre tapaba el terreno).
      attributionControl: false,
      style: {
        version: 8,
        sources: {
          modis: { type: 'raster', tiles: [`${base}capas/color_real_seca/{z}/{x}/{y}.jpg`], tileSize: 256, minzoom: 7, maxzoom: 9, bounds: CAJA,
            attribution: 'NASA GIBS (MODIS)' },
          s2: { type: 'raster', tiles: ['https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2021_3857/default/g/{z}/{y}/{x}.jpg'], tileSize: 256, maxzoom: 15,
            attribution: 'Sentinel-2 cloudless 2021 by EOX (Copernicus Sentinel data 2021), CC BY-NC-SA 4.0' },
          dem: { type: 'raster-dem', tiles: [`${base}terreno/{z}/{x}/{y}.png`], encoding: 'terrarium', tileSize: 256, minzoom: 8, maxzoom: 11, bounds: CAJA,
            attribution: 'SRTM data courtesy of the U.S. Geological Survey · Terrain Tiles: Mapzen' },
          sombra: { type: 'raster-dem', tiles: [`${base}terreno/{z}/{x}/{y}.png`], encoding: 'terrarium', tileSize: 256, minzoom: 8, maxzoom: 11, bounds: CAJA },
          huellas: { type: 'geojson', data: geoHuellas(explorar) },
          punto: { type: 'geojson', data: { type: 'Feature', properties: {}, geometry: { type: 'Point', coordinates: centro } } },
        },
        layers: [
          { id: 'fondo', type: 'background', paint: { 'background-color': '#e9e4d6' } },
          { id: 'modis', type: 'raster', source: 'modis' },
          { id: 's2', type: 'raster', source: 's2' },
          { id: 'sombra', type: 'hillshade', source: 'sombra', paint: { 'hillshade-exaggeration': 0.35 } },
          { id: 'huellas', type: 'line', source: 'huellas', paint: { 'line-color': ['get', 'color'], 'line-width': 3.5 } },
          { id: 'punto', type: 'circle', source: 'punto', paint: { 'circle-radius': 7, 'circle-color': '#e0b43a', 'circle-stroke-color': '#1d2b1a', 'circle-stroke-width': 3 } },
        ],
        terrain: { source: 'dem', exaggeration: EXAGERACION },
      },
    })
    mapa.current = m
    m.on('load', () => {
      if (!quieto) m.flyTo({ center: centro, ...VISTA, duration: 4500, essential: true })
    })
    return () => {
      m.remove()
      mapa.current = null
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [explorar.parcela])

  const mover = (cambio) => {
    const m = mapa.current
    if (!m) return
    const destino = { bearing: m.getBearing() + (cambio.giro || 0), pitch: Math.max(0, Math.min(75, m.getPitch() + (cambio.inclinar || 0))) }
    if (menosMovimiento()) m.jumpTo(destino)
    else m.easeTo({ ...destino, duration: 900 })
  }
  const volver = () => {
    const m = mapa.current
    if (!m) return
    if (menosMovimiento()) m.jumpTo({ center: centro, ...VISTA })
    else m.flyTo({ center: centro, ...VISTA, duration: 1800 })
  }

  const terreno = (res && res.parcela && res.parcela.terreno) || {}
  const resumen = tx('relieve.resumen', { alt: terreno.altitud_m != null ? Math.round(terreno.altitud_m) : '—', pend: terreno.pendiente_pct ?? '—', exa: EXAGERACION })
  return (
    <section className="relieve3d" aria-labelledby="relieve3d-titulo">
      <h3 id="relieve3d-titulo">{tx('relieve.titulo')}</h3>
      <p className="resumen-grafica">{resumen}</p>
      <div ref={caja} className="relieve3d-mapa" role="img" aria-label={`${tx('relieve.titulo')}. ${resumen}`} />
      <div className="mapa-botones" role="group" aria-label={tx('relieve.controles')}>
        <button type="button" onClick={() => mover({ giro: -45 })}>{tx('relieve.girarIzq')}</button>
        <button type="button" onClick={() => mover({ giro: 45 })}>{tx('relieve.girarDer')}</button>
        <button type="button" onClick={() => mover({ inclinar: 15 })}>{tx('relieve.masInclinado')}</button>
        <button type="button" onClick={() => mover({ inclinar: -15 })}>{tx('relieve.menosInclinado')}</button>
        <button type="button" onClick={volver}>{tx('relieve.volver')}</button>
        <button type="button" onClick={onCerrar}>{tx('relieve.cerrar')}</button>
      </div>
      <p className="nota creditos-3d">
        Sentinel-2 cloudless 2021 by <a href="https://s2maps.eu">EOX</a> (Copernicus Sentinel data 2021), CC BY-NC-SA 4.0 · NASA GIBS (MODIS) · SRTM data courtesy of the U.S. Geological Survey · Terrain Tiles: Mapzen
      </p>
      <p className="nota">{tx('relieve.nota', { exa: EXAGERACION })}</p>
    </section>
  )
}
