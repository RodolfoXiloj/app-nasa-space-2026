// Vista «Para el agricultor»: la primera pantalla. Lee solo el bloque `farmer` del JSON (motor/farmer.py)
// y el nombre de las rotaciones. No calcula estados: el color de cada hecho es el del semáforo que el
// motor ya aplicó con data/umbrales_semaforo.yaml (verde, amarillo, rojo; gris solo si falta el dato).
// Nunca solo color: cada estado lleva su forma, su palabra y el dibujo del hecho. Los tres hechos van
// siempre en el mismo orden y lugar: suelo, quema, canícula.
// Los objetos del JSON se normalizan al entrar ({} o []) para no repetir `?.`, que el build convierte en
// código largo: la primera pantalla tiene que pesar poco.
import Senal, { claseSenal } from './Senal.jsx'
import { Fuego, Sol, SueloCubierto, SueloDesnudo } from '../pictos/iconos.jsx'
import { RuedaMeses } from '../pictos/RuedaMeses.jsx'
import { PuntosAnios } from '../pictos/PuntosAnios.jsx'
import { IDIOMAS, NOMBRE_IDIOMA, TEXTOS, empateEnCadena } from './textos.js'
import Escuchar from './Escuchar.jsx'
import KitParcela from '../kit/index.jsx'

const ORDEN = ['suelo', 'quema', 'canicula']
const ESTADOS = ['verde', 'amarillo', 'rojo', 'gris']

// Texto del motor en el idioma elegido: el JSON trae `es.campo` y `en.campo` (y, de antes, `campo` en
// español y `campo_en` en inglés). Si falta el inglés, va el español marcado con lang="es".
function TextoMotor({ obj, campo, idioma }) {
  const txt = (obj[idioma] || {})[campo] || (idioma === 'en' ? obj[campo + '_en'] : obj[campo])
  return txt ? <span lang={idioma}>{txt}</span> : <span lang="es">{obj[campo]}</span>
}

// Dibujo del tema de cada hecho (web/src/pictos/iconos.jsx). El suelo sale cubierto solo cuando el
// satélite no vio ningún mes desnudo ni con poca cobertura.
function IconoHecho({ id, estado, meses, poca }) {
  const Icono = id === 'quema' ? Fuego : id === 'canicula' ? Sol : estado === 'verde' && !meses.length && !poca.length ? SueloCubierto : SueloDesnudo
  return <Icono size={32} decorativo className="agr-hecho-icono" />
}

function Idiomas({ idioma, setIdioma }) {
  const t = TEXTOS[idioma]
  return (
    <div className="agr-idiomas" role="group" aria-label={t.idioma}>
      {IDIOMAS.map((i) => (
        <button key={i} type="button" lang={i} className="agr-boton agr-idioma" aria-pressed={idioma === i} onClick={() => setIdioma(i)}>
          {NOMBRE_IDIOMA[i]}
        </button>
      ))}
    </div>
  )
}

function Hecho({ id, hecho, frase, idioma, sinResumen, palabras }) {
  const t = TEXTOS[idioma]
  // Un estado fuera de los 4 del contrato (o null) es un dato que falta: va en gris, sin adivinar.
  const estado = !sinResumen && ESTADOS.includes(hecho.estado) ? hecho.estado : 'gris'
  const gris = estado === 'gris'
  const palabra = sinResumen ? t.estados.sinResumen : (palabras[estado] || {})[idioma] || t.estados[estado]
  const meses = hecho.meses || []
  const poca = hecho.meses_poca_cobertura || []
  const { valor, de } = hecho
  const tieneConteo = !gris && valor != null && de != null
  const p = (txt, clase = 'agr-hecho-detalle') => <p className={clase}>{txt}</p>
  return (
    <li className={`agr-hecho agr-hecho--${claseSenal(estado)}`} data-hecho={id} data-estado={estado}>
      <Senal estado={estado} />
      <div className="agr-hecho-texto">
        <h3 className="agr-hecho-nombre">
          <IconoHecho id={id} estado={estado} meses={meses} poca={poca} />
          <span>{t.hechos[id]}</span>
        </h3>
        {p(palabra, 'agr-hecho-estado')}
        {!sinResumen && p(t.explicaEstado[estado], 'agr-hecho-explica')}
        {gris && hecho.motivo_gris && p(<>{t.motivoGris} <TextoMotor obj={hecho} campo="motivo_gris" idioma={idioma} /></>)}
        {/* Cantidad como dibujo: rueda de 12 meses para el suelo, puntos de años para quema y canícula.
            En gris la rueda va punteada con «?» y no se dibujan años: no se adivina. */}
        {!sinResumen && id === 'suelo' && (
          <RuedaMeses className="agr-hecho-dibujo" desnudos={meses} poca={poca} sinDatos={gris} lang={idioma} size={184} />
        )}
        {tieneConteo && id !== 'suelo' && de > 0 && (
          <PuntosAnios className="agr-hecho-dibujo" tipo={id} marcados={valor} total={de} lang={idioma} size={26} leyenda={false} />
        )}
        {frase ? p(frase, 'agr-hecho-conteo') : tieneConteo && p(`${t.conteo[id](valor, de)}.`, 'agr-hecho-conteo')}
        {!gris && id === 'suelo' && meses.length > 0 && p(t.detalleMeses.suelo(meses))}
        {!gris && id === 'suelo' && poca.length > 0 && p(t.detalleMeses.pocaCobertura(poca))}
        {!gris && id === 'quema' && meses.length > 0 && p(t.detalleMeses.quema(meses))}
        {id === 'canicula' && tieneConteo && valor > 0 && p(t.detalleMeses.canicula())}
        {hecho.periodo && (hecho.fuente_ids || []).length > 0 && p(t.fuente(hecho.fuente_ids, hecho.periodo), 'agr-hecho-fuente')}
      </div>
    </li>
  )
}

// Tipo de opción y nombre que trae el JSON, los dos en el idioma elegido (`es.nombre` / `en.nombre`).
function Opcion({ id, rot = {}, idioma, as: Tag = 'li', clase = '' }) {
  const t = TEXTOS[idioma]
  let nombre = (rot[idioma] || {}).nombre || (idioma === 'es' && rot.nombre)
  nombre = nombre ? nombre.replace(/^(Lo que hace hoy|What you do today):\s*/, '') : null
  if (nombre) nombre = nombre[0].toUpperCase() + nombre.slice(1)
  return (
    <Tag className={`agr-opcion ${clase}`.trim()}>
      <span className="agr-opcion-tipo">{t.tipos[rot.tipo] || id}</span>
      {nombre && <span className="agr-opcion-nombre">{nombre}</span>}
    </Tag>
  )
}

function Opciones({ farmer, rotaciones, idioma }) {
  const t = TEXTOS[idioma]
  const op = farmer.opciones
  const porId = Object.fromEntries((rotaciones || []).map((r) => [r.id, r]))
  const margen = (farmer.umbrales || {}).margen_empate ?? 3
  // Sin regla aplicada (umbrales en «pendiente») no se compara: se muestra como el gris, sin ganadora.
  const estado = ['empate', 'una_destaca', 'gris'].includes(op.estado) ? op.estado : 'sinComparar'
  // Empate (puntajes a `margen` puntos o menos, en cadena): las opciones parejas, en el orden del motor y
  // sin ganadora. En Olopa la práctica actual entra al empate y salen las tres.
  const empatadas = op.empatadas || []
  const mostradas = estado === 'empate' && empatadas.length ? empatadas : op.alternativas
  const destaca = estado === 'una_destaca' && porId[op.destaca] ? op.destaca : null
  const lista = (estado === 'sinComparar' ? [op.actual, ...op.alternativas] : mostradas).filter((id) => id !== destaca)
  const muestraHoy = op.actual !== destaca && !lista.includes(op.actual)
  const enGris = estado === 'gris' || estado === 'sinComparar'
  return (
    <section className={`agr-opciones agr-opciones--${estado}`} aria-labelledby="agr-opciones-titulo" data-opciones={estado}>
      <h2 id="agr-opciones-titulo" className="agr-subtitulo">{t.opcionesTitulo}</h2>
      <p className={`agr-opciones-estado${enGris ? ' agr-opciones-estado--gris' : ''}`}>
        {enGris && <Senal estado="gris" />}
        <span>{estado === 'empate' ? t.opciones.empate(lista.length, margen, empateEnCadena(mostradas, porId, margen)) : t.opciones[estado]}</span>
      </p>
      {estado === 'gris' && op.motivo_gris && (
        <p className="agr-hecho-detalle">
          {t.motivoGris} <TextoMotor obj={op} campo="motivo_gris" idioma={idioma} />
        </p>
      )}
      {destaca && <Opcion id={destaca} rot={porId[destaca]} idioma={idioma} as="p" clase="agr-opcion--destaca" />}
      <ul className="agr-lista-opciones">
        {lista.map((id) => (
          <Opcion key={id} id={id} rot={porId[id]} idioma={idioma} />
        ))}
      </ul>
      {!destaca && lista.length > 1 && <p className="agr-nota">{t.sinOrden}</p>}
      {muestraHoy && <Opcion id={op.actual} rot={porId[op.actual]} idioma={idioma} as="p" clase="agr-opcion--hoy" />}
      <div className="agr-confianza">
        <h3 className="agr-confianza-titulo">{t.confianzaTitulo}</h3>
        <p className="agr-confianza-nivel">{t.confianza[op.confianza.nivel] || op.confianza.nivel}</p>
        <p className="agr-hecho-detalle">
          {t.motivo} <TextoMotor obj={op.confianza} campo="motivo" idioma={idioma} />
        </p>
      </div>
    </section>
  )
}

export default function VistaAgricultor({ idioma, setIdioma, indice, pid, setPid, res, cargando, error, onEvidencia }) {
  const t = TEXTOS[idioma]
  const parcelas = indice || []
  const parcela = parcelas.find((p) => p.id === pid)
  const farmer = (res && res.farmer) || null
  const f = farmer || {}
  const sinResumen = Boolean(res) && !farmer
  // Palabra de cada estado tal como la fija data/umbrales_semaforo.yaml (viene en el JSON del motor).
  const palabras = (f.umbrales || {}).estados || {}
  const hechos = Object.fromEntries((f.hechos || []).map((h) => [h.id, h]))
  const fraseDe = (id) => ((f.frases || []).find((x) => x.hecho === id) || {})[idioma] || null
  const disponibles = parcelas.filter((p) => p.disponible)
  const farmerAudio = f.audio

  return (
    <div className="agr">
      <header className="agr-cabecera">
        <h1 className="agr-marca">{t.marca}</h1>
        <Idiomas idioma={idioma} setIdioma={setIdioma} />
      </header>

      <main className="agr-cuerpo">
        {res && res.meta && res.meta.tipo === 'ejemplo' && <p className="agr-banda" role="status">{t.ejemplo}</p>}

        {disponibles.length > 0 && (
          <div className="agr-parcela">
            <label htmlFor="agr-parcela" className="agr-etiqueta">{t.parcela}</label>
            <select id="agr-parcela" className="agr-select" value={pid || ''} onChange={(e) => setPid(e.target.value)}>
              {disponibles.map((p) => (
                <option key={p.id} value={p.id}>{`${p.municipio}, ${p.departamento}`}</option>
              ))}
            </select>
            {parcela && (
              <p className="agr-nota">
                {(parcela[idioma] || {}).nombre || (idioma === 'es' ? parcela.nombre : t.parcelaEjemplo)}
                {parcela.provisional ? `. ${t.ubicacionProvisional}.` : '.'}
              </p>
            )}
          </div>
        )}

        {/* Un toque desde la primera pantalla: el audio corto de esta parcela, con subtítulos. */}
        {farmerAudio?.es?.mp3 && !cargando && (
          <Escuchar
            key={farmerAudio.es.mp3}
            farmerAudio={farmerAudio}
            idioma={idioma}
          />
        )}

        <section className="agr-hechos" aria-labelledby="agr-titulo" aria-busy={cargando || undefined}>
          <h2 id="agr-titulo" className="agr-subtitulo">{t.titulo}</h2>
          <p className="agr-entradilla">{t.entradilla}</p>
          <div aria-live="polite">
            {cargando && <p className="agr-nota">{t.cargando}</p>}
            {error && <p className="agr-banda agr-banda--error" role="alert">{t.errorDatos}</p>}
            {parcela && !parcela.disponible && <p className="agr-banda">{t.noDisponible}</p>}
            {sinResumen && <p className="agr-banda">{t.sinResumen}</p>}
          </div>
          {(farmer || sinResumen) && (
            <ul className="agr-lista-hechos">
              {ORDEN.map((id) => (
                <Hecho key={id} id={id} hecho={hechos[id] || {}} frase={fraseDe(id)} idioma={idioma} sinResumen={sinResumen} palabras={palabras} />
              ))}
            </ul>
          )}
        </section>

        {farmer && <Opciones farmer={farmer} rotaciones={res.rotaciones} idioma={idioma} />}

        <p className="agr-aviso">{t.aviso}</p>
        {farmer && <KitParcela idioma={idioma} pid={pid} parcela={parcela} farmer={farmer} rotaciones={res.rotaciones} />}

        <button type="button" className="agr-boton agr-evidencia" onClick={onEvidencia}>
          <span className="agr-evidencia-titulo">{t.evidencia}</span>
          <span className="agr-evidencia-detalle">{t.evidenciaDetalle}</span>
        </button>
      </main>
    </div>
  )
}
