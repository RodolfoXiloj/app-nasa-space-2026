// Vista «Para el agricultor»: la primera pantalla. Lee solo el bloque `farmer` del JSON (motor/farmer.py)
// y el nombre de las rotaciones. No calcula estados: si un estado viene en null, lo dibuja en gris y dice
// por qué. Los tres hechos van siempre en el mismo orden y lugar: suelo, quema, canícula.
import Senal, { claseSenal } from './Senal.jsx'
import { IDIOMAS, NOMBRE_IDIOMA, TEXTOS } from './textos.js'

const ORDEN = ['suelo', 'quema', 'canicula']

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

function Hecho({ id, hecho, frase, idioma, sinResumen }) {
  const t = TEXTOS[idioma]
  // Un estado que no es uno de los 4 del contrato se trata como null: sin color y sin adivinar.
  const conocido = ['verde', 'amarillo', 'rojo', 'gris'].includes(hecho?.estado)
  const clave = sinResumen ? 'sinResumen' : conocido ? hecho.estado : 'pendiente'
  const meses = hecho?.meses || []
  const poca = hecho?.meses_poca_cobertura || []
  const tieneConteo = hecho && hecho.valor != null && hecho.de != null
  return (
    <li className={`agr-hecho agr-hecho--${claseSenal(hecho?.estado)}`} data-hecho={id} data-estado={hecho?.estado ?? 'null'}>
      <Senal estado={hecho?.estado} />
      <div className="agr-hecho-texto">
        <h3 className="agr-hecho-nombre">{t.hechos[id]}</h3>
        <p className="agr-hecho-estado">{t.estados[clave]}</p>
        {clave !== 'pendiente' && t.explicaEstado[clave] && <p className="agr-hecho-explica">{t.explicaEstado[clave]}</p>}
        {hecho?.estado === 'gris' && hecho.motivo_gris && (
          <p className="agr-hecho-detalle">
            {t.motivoGris} <span lang="es">{hecho.motivo_gris}</span>
          </p>
        )}
        {frase ? (
          <p className="agr-hecho-conteo">{frase}</p>
        ) : (
          tieneConteo && <p className="agr-hecho-conteo">{t.conteo[id](hecho.valor, hecho.de)}.</p>
        )}
        {id === 'suelo' && meses.length > 0 && <p className="agr-hecho-detalle">{t.detalleMeses.suelo(meses)}</p>}
        {id === 'suelo' && poca.length > 0 && <p className="agr-hecho-detalle">{t.detalleMeses.pocaCobertura(poca)}</p>}
        {id === 'quema' && meses.length > 0 && <p className="agr-hecho-detalle">{t.detalleMeses.quema(meses)}</p>}
        {id === 'canicula' && tieneConteo && hecho.valor > 0 && <p className="agr-hecho-detalle">{t.detalleMeses.canicula()}</p>}
        {hecho?.fuente_ids?.length > 0 && hecho.periodo && <p className="agr-hecho-fuente">{t.fuente(hecho.fuente_ids, hecho.periodo)}</p>}
      </div>
    </li>
  )
}

// Tipo de opción en el idioma elegido y, en español, el nombre que trae el JSON (el JSON no trae nombres en inglés).
function Opcion({ id, rot, idioma, as: Tag = 'li', clase = '' }) {
  const t = TEXTOS[idioma]
  let nombre = idioma === 'es' && rot?.nombre ? rot.nombre.replace(/^Lo que hace hoy:\s*/, '') : null
  if (nombre) nombre = nombre[0].toUpperCase() + nombre.slice(1)
  return (
    <Tag className={`agr-opcion ${clase}`.trim()}>
      <span className="agr-opcion-tipo">{t.tipos[rot?.tipo] || id}</span>
      {nombre && <span className="agr-opcion-nombre">{nombre}</span>}
    </Tag>
  )
}

function Opciones({ farmer, rotaciones, idioma }) {
  const t = TEXTOS[idioma]
  const op = farmer.opciones
  const porId = Object.fromEntries((rotaciones || []).map((r) => [r.id, r]))
  const estado = op.estado
  // Empate: las opciones parejas, sin orden. `empatadas` es opcional en el contrato; si no viene, son las alternativas.
  const mostradas = estado === 'empate' && Array.isArray(op.empatadas) ? op.empatadas : op.alternativas
  const destaca = estado === 'una_destaca' && porId[op.destaca] ? op.destaca : null
  const lista = (estado === 'pendiente' ? [op.actual, ...op.alternativas] : mostradas).filter((id) => id !== destaca)
  const muestraHoy = op.actual !== destaca && !lista.includes(op.actual)
  return (
    <section className={`agr-opciones agr-opciones--${estado}`} aria-labelledby="agr-opciones-titulo">
      <h2 id="agr-opciones-titulo" className="agr-subtitulo">{t.opcionesTitulo}</h2>
      <p className="agr-opciones-estado">
        {estado === 'empate' ? t.opciones.empate(lista.length) : t.opciones[estado]}
      </p>
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
          {t.motivo} <span lang="es">{op.confianza.motivo}</span>
        </p>
      </div>
    </section>
  )
}

export default function VistaAgricultor({ idioma, setIdioma, indice, pid, setPid, res, cargando, error, onEvidencia }) {
  const t = TEXTOS[idioma]
  const parcela = indice?.find((p) => p.id === pid)
  const farmer = res?.farmer || null
  const sinResumen = Boolean(res) && !farmer
  // Estados en null: el motivo se dice una vez arriba de la lista, no en cada hecho.
  const hayPendientes = Boolean(farmer?.hechos?.some((h) => !['verde', 'amarillo', 'rojo', 'gris'].includes(h.estado)))
  const hechos = Object.fromEntries((farmer?.hechos || []).map((h) => [h.id, h]))
  const frases = farmer?.frases || []
  const fraseDe = (id) => frases.find((f) => f.hecho === id)?.[idioma] || null
  const disponibles = (indice || []).filter((p) => p.disponible)

  return (
    <div className="agr">
      <header className="agr-cabecera">
        <h1 className="agr-marca">{t.marca}</h1>
        <Idiomas idioma={idioma} setIdioma={setIdioma} />
      </header>

      <main className="agr-cuerpo">
        {res?.meta?.tipo === 'ejemplo' && <p className="agr-banda" role="status">{t.ejemplo}</p>}

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
                {idioma === 'es' ? parcela.nombre : t.parcelaEjemplo}
                {parcela.provisional ? `. ${t.ubicacionProvisional}.` : '.'}
              </p>
            )}
          </div>
        )}

        <section className="agr-hechos" aria-labelledby="agr-titulo" aria-busy={cargando || undefined}>
          <h2 id="agr-titulo" className="agr-subtitulo">{t.titulo}</h2>
          <p className="agr-entradilla">{t.entradilla}</p>
          <div aria-live="polite">
            {cargando && <p className="agr-nota">{t.cargando}</p>}
            {error && <p className="agr-banda agr-banda--error" role="alert">{t.errorDatos}</p>}
            {parcela && !parcela.disponible && <p className="agr-banda">{t.noDisponible}</p>}
            {sinResumen && <p className="agr-banda">{t.sinResumen}</p>}
            {hayPendientes && <p className="agr-banda">{t.explicaEstado.pendiente}</p>}
          </div>
          {(farmer || sinResumen) && (
            <ul className="agr-lista-hechos">
              {ORDEN.map((id) => (
                <Hecho key={id} id={id} hecho={hechos[id]} frase={fraseDe(id)} idioma={idioma} sinResumen={sinResumen} />
              ))}
            </ul>
          )}
        </section>

        {farmer && <Opciones farmer={farmer} rotaciones={res.rotaciones} idioma={idioma} />}

        <p className="agr-aviso">{t.aviso}</p>

        <button type="button" className="agr-boton agr-evidencia" onClick={onEvidencia}>
          <span className="agr-evidencia-titulo">{t.evidencia}</span>
          <span className="agr-evidencia-detalle">{t.evidenciaDetalle}</span>
        </button>
      </main>
    </div>
  )
}
