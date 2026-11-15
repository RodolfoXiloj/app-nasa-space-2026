// Kit comunitario de una parcela: tres botones (imprimir la hoja, descargar el audio corto, compartir por
// WhatsApp) y la hoja imprimible de UNA página en blanco y negro, en el idioma activo.
// La hoja no se ve en pantalla: va en un portal directo en <body> y solo sale al imprimir con el botón,
// que pone la clase `kit-imprimiendo` en <html> mientras dura la impresión. Así Ctrl+P en la vista del
// agricultor o en Evidence imprime lo mismo que antes.
// Cada hecho lleva forma (Senal), palabra, dibujo del tema y cantidad (RuedaMeses o PuntosAnios): nada
// depende del color, que en una fotocopia se pierde.
import { useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import Senal from '../agricultor/Senal.jsx'
import { TEXTOS, empateEnCadena } from '../agricultor/textos.js'
import { Fuego, Sol, SueloCubierto, SueloDesnudo } from '../pictos/iconos.jsx'
import { RuedaMeses } from '../pictos/RuedaMeses.jsx'
import { PuntosAnios } from '../pictos/PuntosAnios.jsx'
import { TEXTOS_KIT } from './textos.js'
import { guardar, registrar, urlsParcela } from './sinSenal.js'
import { compartirImagen } from './imagen.js'
import './kit.css'

const ORDEN = ['suelo', 'quema', 'canicula']
const ESTADOS = ['verde', 'amarillo', 'rojo', 'gris']
const CLASE = 'kit-imprimiendo'

const estadoDe = (h) => (ESTADOS.includes(h.estado) ? h.estado : 'gris')

function nombreOpcion(rot, idioma) {
  let n = (rot[idioma] || {}).nombre || (idioma === 'es' && rot.nombre)
  if (!n) return null
  n = n.replace(/^(Lo que hace hoy|What you do today):\s*/, '')
  return n[0].toUpperCase() + n.slice(1)
}

// Opciones en el mismo orden que la vista: la que destaca primero, luego las parejas o alternativas y
// al final lo que hace hoy. Sin regla aplicada no hay ganadora.
function listaOpciones(op) {
  const destaca = op.estado === 'una_destaca' ? op.destaca : null
  const medio = op.estado === 'empate' && (op.empatadas || []).length ? op.empatadas : op.alternativas || []
  return [...new Set([destaca, ...medio, op.actual].filter(Boolean))].map((id) => ({ id, destaca: id === destaca }))
}

export function resumenWhatsApp({ idioma, lugar, farmer, href }) {
  const t = TEXTOS[idioma]
  const k = TEXTOS_KIT[idioma]
  const palabras = (farmer.umbrales || {}).estados || {}
  const hechos = Object.fromEntries((farmer.hechos || []).map((h) => [h.id, h]))
  const lineas = ORDEN.map((id) => {
    const e = estadoDe(hechos[id] || {})
    return `- ${t.hechos[id]}: ${(palabras[e] || {})[idioma] || t.estados[e]}`
  })
  return [k.resumen(lugar), ...lineas, t.aviso, href].join('\n')
}

function IconoHecho({ id, estado, meses, poca }) {
  const Icono = id === 'quema' ? Fuego : id === 'canicula' ? Sol : estado === 'verde' && !meses.length && !poca.length ? SueloCubierto : SueloDesnudo
  return <Icono size={28} decorativo className="kit-icono" />
}

function HechoHoja({ id, hecho, idioma, palabras, frase }) {
  const t = TEXTOS[idioma]
  const estado = estadoDe(hecho)
  const gris = estado === 'gris'
  const meses = hecho.meses || []
  const poca = hecho.meses_poca_cobertura || []
  const { valor, de } = hecho
  const conteo = !gris && valor != null && de != null
  return (
    <li className="kit-hecho" data-hecho={id} data-estado={estado}>
      <div className="kit-hecho-cabeza">
        <Senal estado={estado} />
        <div>
          <h3><IconoHecho id={id} estado={estado} meses={meses} poca={poca} /> {t.hechos[id]}</h3>
          <p className="kit-palabra">{(palabras[estado] || {})[idioma] || t.estados[estado]}</p>
        </div>
      </div>
      {id === 'suelo' ? (
        <RuedaMeses desnudos={meses} poca={poca} sinDatos={gris} lang={idioma} size={118} leyenda={false} />
      ) : (
        conteo && de > 0 && <PuntosAnios tipo={id} marcados={valor} total={de} lang={idioma} size={18} leyenda={false} />
      )}
      <p>{frase || (conteo ? `${t.conteo[id](valor, de)}.` : t.explicaEstado[estado])}</p>
      {hecho.periodo && (hecho.fuente_ids || []).length > 0 && <p className="kit-fuente">{t.fuente(hecho.fuente_ids, hecho.periodo)}</p>}
    </li>
  )
}

function Hoja({ idioma, lugar, nombre, farmer, rotaciones, href }) {
  const t = TEXTOS[idioma]
  const k = TEXTOS_KIT[idioma]
  const palabras = (farmer.umbrales || {}).estados || {}
  const hechos = Object.fromEntries((farmer.hechos || []).map((h) => [h.id, h]))
  const fraseDe = (id) => ((farmer.frases || []).find((x) => x.hecho === id) || {})[idioma] || null
  const op = farmer.opciones || {}
  const porId = Object.fromEntries((rotaciones || []).map((r) => [r.id, r]))
  const conf = op.confianza || {}
  const estadoOp = ['empate', 'una_destaca', 'gris'].includes(op.estado) ? op.estado : 'sinComparar'
  const margen = (farmer.umbrales || {}).margen_empate ?? 3
  const opciones = listaOpciones(op)
  return (
    <article className="kit-hoja" lang={idioma} aria-hidden="true">
      <header className="kit-hoja-cabeza">
        <p className="kit-marca">{t.marca} · {k.hoja}</p>
        <h1>{lugar}</h1>
        {nombre && <p>{nombre}</p>}
      </header>
      <h2>{k.hechos}</h2>
      <ul className="kit-hechos">
        {ORDEN.map((id) => (
          <HechoHoja key={id} id={id} hecho={hechos[id] || {}} idioma={idioma} palabras={palabras} frase={fraseDe(id)} />
        ))}
      </ul>
      <p className="kit-formas">{k.formas}</p>
      <section className="kit-opciones">
        <h2>{t.opcionesTitulo}</h2>
        <p>{estadoOp === 'empate' ? t.opciones.empate((op.empatadas || []).length || opciones.length, margen, empateEnCadena(op.empatadas || [], porId, margen)) : t.opciones[estadoOp]}</p>
        <ol>
          {opciones.map(({ id, destaca }) => {
            const rot = porId[id] || {}
            const n = nombreOpcion(rot, idioma)
            return (
              <li key={id} data-destaca={destaca || undefined}>
                <b>{t.tipos[rot.tipo] || id}</b>{n ? `: ${n}` : ''}
              </li>
            )
          })}
        </ol>
        {conf.nivel && <p>{k.confianza} <b>{t.confianza[conf.nivel] || conf.nivel}</b>.</p>}
      </section>
      <p className="kit-aviso">{t.aviso}</p>
      <p className="kit-fuente">{t.ia}</p>
      <p className="kit-fuente">{k.web} {href}</p>
    </article>
  )
}

export default function Kit({ idioma, pid, parcela, farmer, rotaciones }) {
  const t = TEXTOS[idioma]
  const k = TEXTOS_KIT[idioma]
  // El portal y location.href existen solo en el navegador: se montan después del primer pintado.
  const [href, setHref] = useState(null)
  // Guardar para usar sin señal: solo si el navegador registró el service worker (build, https o localhost).
  const [puedeGuardar, setPuedeGuardar] = useState(false)
  const [guardado, setGuardado] = useState(null)
  useEffect(() => {
    let vigente = true
    registrar().then((r) => vigente && setPuedeGuardar(Boolean(r)))
    return () => {
      vigente = false
    }
  }, [])
  const [imagen, setImagen] = useState(null)
  // Cada guardado o imagen lleva su turno: si mientras tanto cambia la parcela o el idioma, su resultado no se
  // muestra bajo la parcela nueva.
  const turno = useRef(0)
  useEffect(() => {
    turno.current += 1
    setGuardado(null)
    setImagen(null)
  }, [pid, idioma])
  useEffect(() => {
    setHref(window.location.href)
    const quitar = () => document.documentElement.classList.remove(CLASE)
    window.addEventListener('afterprint', quitar)
    return () => {
      window.removeEventListener('afterprint', quitar)
      quitar()
    }
  }, [pid])
  if (!farmer || !pid) return null
  const lugar = parcela ? `${parcela.municipio}, ${parcela.departamento}` : pid
  const nombre = parcela && ((parcela[idioma] || {}).nombre || (idioma === 'es' ? parcela.nombre : null))
  const texto = href ? resumenWhatsApp({ idioma, lugar, farmer, href }) : ''
  // El mp3 corto del idioma de la pantalla; si falta el inglés, el español.
  const mp3 = ((farmer.audio || {})[idioma] || {}).mp3 || `audio/${pid}.frases.mp3`

  async function hacerImagen() {
    const mio = turno.current
    setImagen('haciendo')
    const r = await compartirImagen({ idioma, lugar, farmer, href, pid, texto })
    if (turno.current === mio) setImagen(r)
  }

  async function guardarAqui() {
    const mio = turno.current
    setGuardado('guardando')
    const r = await guardar(urlsParcela({ parcela, farmer, idioma }))
    if (turno.current === mio) setGuardado(r)
  }

  function imprimir() {
    document.documentElement.classList.add(CLASE)
    window.print()
  }

  return (
    <section className="kit" aria-labelledby="kit-titulo">
      <h2 id="kit-titulo" className="kit-titulo">{k.titulo}</h2>
      <p className="kit-detalle">{k.detalle}</p>
      <div className="kit-botones">
        <button type="button" className="kit-boton kit-imprimir" onClick={imprimir}>{k.imprimir}</button>
        <a className="kit-boton kit-audio" href={import.meta.env.BASE_URL + mp3} download={mp3.split('/').pop()}>
          {k.audio}
        </a>
        <a className="kit-boton kit-whatsapp" href={`https://wa.me/?text=${encodeURIComponent(texto)}`} target="_blank" rel="noopener noreferrer">
          {k.whatsapp}
        </a>
        <button type="button" className="kit-boton kit-imagen" onClick={hacerImagen} disabled={imagen === 'haciendo'}>
          {k.imagen}
        </button>
      </div>
      {imagen && imagen !== 'haciendo' && imagen !== 'cancelada' && (
        <p className="kit-detalle" role="status">{k.imagenLista[imagen] || ''}</p>
      )}
      {puedeGuardar && (
        <div className="kit-sin-senal">
          <button type="button" className="kit-boton kit-guardar" onClick={guardarAqui} disabled={guardado === 'guardando'}>
            {k.guardar}
          </button>
          <p className="kit-detalle" aria-live="polite">
            {guardado === 'guardando'
              ? k.guardando
              : guardado && guardado.ok
                ? k.guardadoOk(Math.round(guardado.bytes / 1000))
                : guardado
                  ? k.guardadoError
                  : k.guardarDetalle}
          </p>
        </div>
      )}
      {href && createPortal(<Hoja idioma={idioma} lugar={lugar} nombre={nombre} farmer={farmer} rotaciones={rotaciones} href={href} />, document.body)}
    </section>
  )
}
