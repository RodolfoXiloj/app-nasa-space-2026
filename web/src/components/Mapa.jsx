import { useCallback, useEffect, useRef, useState } from 'react'
import { CircleMarker, LayersControl, MapContainer, TileLayer, Tooltip, ZoomControl, useMap } from 'react-leaflet'
import { Comparador, EtiquetasComparador, Herramientas, HuellasCapa, PARES, TomarMapa } from './mapa/Herramientas.jsx'
import './explorar.css'
import { useTx } from '../i18n/explorar.js'
import { BASE } from '../lib/datos.js'
import { useLocale, useT } from '../i18n/useT.js'
import { leerMotor } from '../i18n/motor.js'

const local = (capa, ext) => `${BASE}capas/${capa}/{z}/{x}/{y}.${ext}`
const CAJA = [[14.586, -89.64], [15.021, -89.214]]
const ATRIB_GIBS = 'Imágenes: <a href="https://www.earthdata.nasa.gov/gibs">NASA GIBS</a>'
const ATRIB_S2 =
  '<a href="https://s2maps.eu">Sentinel-2 cloudless 2021</a> de EOX (datos Copernicus Sentinel 2021), CC BY-NC-SA 4.0'

const ATRIB_SRTM = 'SRTM data courtesy of the <a href="https://www.usgs.gov/">U.S. Geological Survey</a> · Terrain Tiles: Mapzen'

const COLORES = { alta: '#2e7d32', media: '#c79100', baja: '#b23c17', pendiente: '#7a7a7a' }

const menosMovimiento = () =>
  typeof window !== 'undefined' && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches

function Volar({ destino }) {
  const map = useMap()
  useEffect(() => {
    if (!destino) return
    const zoom = Math.max(map.getZoom(), 11)
    // Con movimiento reducido el mapa salta al punto, sin vuelo animado.
    if (menosMovimiento()) map.setView(destino, zoom, { animate: false })
    else map.flyTo(destino, zoom, { duration: 0.8 })
  }, [destino, map])
  return null
}

// Leaflet pone «Layers» en inglés al botón de capas: aquí lleva el nombre en el idioma activo.
function NombreCapas({ nombre }) {
  const map = useMap()
  useEffect(() => {
    const boton = map.getContainer().querySelector('.leaflet-control-layers-toggle')
    if (!boton) return
    boton.setAttribute('aria-label', nombre)
    boton.setAttribute('title', nombre)
  }, [map, nombre])
  return null
}

function RespaldoSinRed({ enLinea, guardada, avisar }) {
  const map = useMap()
  useEffect(() => {
    const capa = enLinea.current
    if (!capa) return undefined
    let cargadas = 0
    let errores = 0
    let hecho = false
    const carga = () => {
      cargadas += 1
    }
    const error = () => {
      errores += 1
      if (!hecho && cargadas === 0 && errores >= 3 && map.hasLayer(capa) && guardada.current) {
        hecho = true
        map.removeLayer(capa)
        map.addLayer(guardada.current)
        avisar(true)
      }
    }
    capa.on('tileload', carga)
    capa.on('tileerror', error)
    return () => {
      capa.off('tileload', carga)
      capa.off('tileerror', error)
    }
  }, [map, enLinea, guardada, avisar])
  return null
}

// Fechas de las capas NDVI guardadas (pipeline/capas.py, web/public/capas/capas.json).
const FECHAS = { ndvi_seca: '2026-03-22', ndvi_lluvia: '2026-09-14', ndvi_ago_2025: '2025-08-13', ndvi_ago_2026: '2026-08-13' }

export default function Mapa({ parcelas, seleccion, onSeleccion, res, explorar = null }) {
  const t = useT()
  const tx = useTx()
  const loc = useLocale()
  const quieto = menosMovimiento()
  const enLinea = useRef(null)
  const guardada = useRef(null)
  const [sinRed, setSinRed] = useState(false)
  const [mapa, setMapa] = useState(null)
  const tomar = useCallback((m) => setMapa(m), [])
  const [huellas, setHuellas] = useState(false)
  const [comparar, setComparar] = useState(null)
  const [pos, setPos] = useState(0.5)
  const [opacidad, setOpacidad] = useState(0.75)
  const sel = parcelas.find((p) => p.id === seleccion)
  const destino = sel ? [sel.lat, sel.lon] : res ? [res.parcela.lat, res.parcela.lon] : null
  const puntos = parcelas.length
    ? parcelas
    : res
      ? [{ ...res.parcela, id: '__ejemplo__', disponible: true }]
      : []

  return (
    <>
      <div className="mapa" role="region" aria-label={t('mapa.region')}>
        <div className="mapa-marco">
        <MapContainer
          center={[14.82, -89.45]}
          zoom={10}
          scrollWheelZoom={false}
          zoomControl={false}
          zoomAnimation={!quieto}
          fadeAnimation={!quieto}
          markerZoomAnimation={!quieto}
          style={{ height: '100%', width: '100%' }}
        >
          <ZoomControl key={t('a11y.zoomIn')} position="topleft" zoomInTitle={t('a11y.zoomIn')} zoomOutTitle={t('a11y.zoomOut')} />
          <LayersControl position="topright">
            <LayersControl.BaseLayer checked name={t('mapa.osm')}>
              <TileLayer
                ref={enLinea}
                url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                maxZoom={18}
              />
            </LayersControl.BaseLayer>
            <LayersControl.BaseLayer name={t('mapa.s2')}>
              <TileLayer
                url="https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2021_3857/default/g/{z}/{y}/{x}.jpg"
                attribution={ATRIB_S2}
                maxZoom={17}
              />
            </LayersControl.BaseLayer>
            <LayersControl.BaseLayer name={t('mapa.modisOffline')}>
              <TileLayer
                ref={guardada}
                url={local('color_real_seca', 'jpg')}
                bounds={CAJA}
                minNativeZoom={7}
                maxNativeZoom={9}
                maxZoom={18}
                attribution={ATRIB_GIBS}
              />
            </LayersControl.BaseLayer>
            <LayersControl.Overlay name={t('mapa.ndviDry')}>
              <TileLayer url={local('ndvi_seca', 'png')} bounds={CAJA} minNativeZoom={7} maxNativeZoom={9} maxZoom={18} opacity={opacidad} attribution={ATRIB_GIBS} />
            </LayersControl.Overlay>
            <LayersControl.Overlay name={t('mapa.ndviWet')}>
              <TileLayer url={local('ndvi_lluvia', 'png')} bounds={CAJA} minNativeZoom={7} maxNativeZoom={9} maxZoom={18} opacity={opacidad} attribution={ATRIB_GIBS} />
            </LayersControl.Overlay>
            <LayersControl.Overlay name={tx('relieve.capa')}>
              <TileLayer url={local('relieve', 'png')} bounds={CAJA} minNativeZoom={8} maxNativeZoom={11} maxZoom={18} attribution={ATRIB_SRTM} />
            </LayersControl.Overlay>
          </LayersControl>
          {puntos.map((p) => {
            const nivel = p.disponible ? p.resumen?.confianza || 'media' : 'pendiente'
            const activa = p.id === seleccion
            return (
              <CircleMarker
                key={p.id}
                center={[p.lat, p.lon]}
                radius={activa ? 11 : 8}
                pathOptions={{ color: '#1d2b1a', weight: activa ? 3 : 1.5, fillColor: COLORES[nivel], fillOpacity: 0.9 }}
                eventHandlers={{ click: () => p.id !== '__ejemplo__' && onSeleccion(p.id) }}
              >
                <Tooltip direction="top">
                  <strong>{leerMotor(p, 'nombre', loc).txt}</strong>
                  <br />
                  {p.disponible ? `${t('mapa.confidence')} ${t(`a11y.nivel.${nivel}`)}` : t('mapa.noDataYet')}
                  {p.provisional ? ` · ${t('mapa.provisional')}` : ''}
                </Tooltip>
              </CircleMarker>
            )
          })}
          {comparar && (
            <Comparador key={comparar} izq={local(PARES[comparar].izq, 'png')} der={local(PARES[comparar].der, 'png')} pos={pos} caja={CAJA} opacidad={Math.max(opacidad, 0.5)} />
          )}
          <HuellasCapa explorar={explorar} activa={huellas} />
          <TomarMapa alTomar={tomar} />
          <Volar destino={destino} />
          <NombreCapas nombre={t('a11y.layers')} />
          <RespaldoSinRed enLinea={enLinea} guardada={guardada} avisar={setSinRed} />
        </MapContainer>
        {comparar && <EtiquetasComparador pos={pos} fechas={FECHAS} par={comparar} />}
        </div>
        {sinRed && (
          <p className="nota-mapa aviso-sin-red" role="status">
            {t('mapa.offlineNote')}
          </p>
        )}
        <p className="nota-mapa">{t('mapa.footnote')}</p>
      </div>
      <Herramientas
        mapa={mapa}
        explorar={explorar}
        res={res}
        huellas={huellas}
        setHuellas={setHuellas}
        comparar={comparar}
        setComparar={setComparar}
        pos={pos}
        setPos={setPos}
        opacidad={opacidad}
        setOpacidad={setOpacidad}
        fechas={FECHAS}
      />
      {/* El color del círculo no es la única señal: la misma información, en texto. */}
      <details className="mapa-texto">
        <summary>{t('a11y.mapList', { n: puntos.length })}</summary>
        <ul>
          {puntos.map((p) => {
            const nivel = p.disponible ? p.resumen?.confianza || 'media' : null
            return (
              <li key={p.id}>
                <b>{leerMotor(p, 'nombre', loc).txt}</b>:{' '}
                {nivel ? `${t('mapa.confidence')} ${t(`a11y.nivel.${nivel}`)}` : t('mapa.noDataYet')}
                {p.provisional ? ` · ${t('mapa.provisional')}` : ''}
              </li>
            )
          })}
        </ul>
      </details>
    </>
  )
}