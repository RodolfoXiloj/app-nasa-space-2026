import { useEffect, useRef, useState } from 'react'
import { CircleMarker, LayersControl, MapContainer, TileLayer, Tooltip, useMap } from 'react-leaflet'
import { BASE } from '../lib/datos.js'
import { useT } from '../i18n/useT.js'

const local = (capa, ext) => `${BASE}capas/${capa}/{z}/{x}/{y}.${ext}`
const CAJA = [[14.586, -89.64], [15.021, -89.214]]
const ATRIB_GIBS = 'Imágenes: <a href="https://www.earthdata.nasa.gov/gibs">NASA GIBS</a>'
const ATRIB_S2 =
  '<a href="https://s2maps.eu">Sentinel-2 cloudless 2021</a> de EOX (datos Copernicus Sentinel 2021), CC BY-NC-SA 4.0'

const COLORES = { alta: '#2e7d32', media: '#c79100', baja: '#b23c17', pendiente: '#7a7a7a' }

function Volar({ destino }) {
  const map = useMap()
  useEffect(() => {
    if (destino) map.flyTo(destino, Math.max(map.getZoom(), 11), { duration: 0.8 })
  }, [destino, map])
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

export default function Mapa({ parcelas, seleccion, onSeleccion, res }) {
  const t = useT()
  const enLinea = useRef(null)
  const guardada = useRef(null)
  const [sinRed, setSinRed] = useState(false)
  const sel = parcelas.find((p) => p.id === seleccion)
  const destino = sel ? [sel.lat, sel.lon] : res ? [res.parcela.lat, res.parcela.lon] : null
  const puntos = parcelas.length
    ? parcelas
    : res
      ? [{ id: '__ejemplo__', nombre: res.parcela.nombre, lat: res.parcela.lat, lon: res.parcela.lon, disponible: true }]
      : []

  return (
    <div className="mapa" role="region" aria-label={t('mapa.region')}>
      <MapContainer center={[14.82, -89.45]} zoom={10} scrollWheelZoom={false} style={{ height: '100%', width: '100%' }}>
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
              maxZoom={16}
              attribution={ATRIB_GIBS}
            />
          </LayersControl.BaseLayer>
          <LayersControl.Overlay name={t('mapa.ndviDry')}>
            <TileLayer url={local('ndvi_seca', 'png')} bounds={CAJA} minNativeZoom={7} maxNativeZoom={9} maxZoom={16} opacity={0.75} attribution={ATRIB_GIBS} />
          </LayersControl.Overlay>
          <LayersControl.Overlay name={t('mapa.ndviWet')}>
            <TileLayer url={local('ndvi_lluvia', 'png')} bounds={CAJA} minNativeZoom={7} maxNativeZoom={9} maxZoom={16} opacity={0.75} attribution={ATRIB_GIBS} />
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
                <strong>{p.nombre}</strong>
                <br />
                {p.disponible ? `${t('mapa.confidence')} ${nivel}` : t('mapa.noDataYet')}
                {p.provisional ? ` · ${t('mapa.provisional')}` : ''}
              </Tooltip>
            </CircleMarker>
          )
        })}
        <Volar destino={destino} />
        <RespaldoSinRed enLinea={enLinea} guardada={guardada} avisar={setSinRed} />
      </MapContainer>
      {sinRed && (
        <p className="nota-mapa aviso-sin-red" role="status">
          {t('mapa.offlineNote')}
        </p>
      )}
      <p className="nota-mapa">{t('mapa.footnote')}</p>
    </div>
  )
}