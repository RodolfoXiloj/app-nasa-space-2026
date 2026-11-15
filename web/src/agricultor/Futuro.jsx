// «El futuro»: cada opción en los 33 climas posibles de la NASA para 2041-2060 (NEX-GDDP-CMIP6, SSP2-4.5), dibujada
// como 33 matas: verde si en ese clima le alcanza el agua (al menos como hoy) y seca si no. Así el «3 de 33» se ve
// sin explicar porcentajes (15 nov 2026: los futuros también para el agricultor, súper fáciles de entender).
// Las cifras vienen de `farmer.futuros` (motor/farmer.py, de data/futuros_nasa.json) y la frase es la misma que lee
// el audio corto (`farmer.frases`, id «futuro»). Con confianza baja el motor no dice esta frase y aquí no se muestra.
// Llega con import() después de pintar; sus textos viven aquí para no crecer el JS de la primera pantalla.
import './tarjetas.css'

const TEXTOS = {
  es: {
    titulo: (a, b) => `El futuro: ${a} a ${b}`,
    hoy: (n) => `Como hoy: ${n}`,
    cuantas: (k, n) => `${k} de ${n}`,
    matas: (k, n) => `${k} de ${n} climas: le alcanza el agua`,
    leyenda: 'Cada mata es un clima posible, de un modelo de la NASA (NEX-GDDP-CMIP6, emisiones intermedias). Verde: le alcanza el agua, al menos como hoy. Seca: no le alcanza.',
  },
  en: {
    titulo: (a, b) => `The future: ${a} to ${b}`,
    hoy: (n) => `As today: ${n}`,
    cuantas: (k, n) => `${k} of ${n}`,
    matas: (k, n) => `${k} of ${n} climates: enough water`,
    leyenda: 'Each plant is one possible climate, from a NASA model (NEX-GDDP-CMIP6, intermediate emissions). Green: enough water, at least as today. Dry: not enough.',
  },
}

// El cultivo de hoy con su nombre («maíz con frijol»), del nombre largo de la rotación actual (igual que el motor).
function nombreHoy(rot, idioma) {
  const largo = idioma === 'en' ? (rot.en && rot.en.nombre) || rot.nombre : rot.nombre
  const corte = idioma === 'en' ? ' in primera' : ' en primera'
  return (largo || '').replace(/^.*?:\s*/, '').split(corte)[0].trim() || rot.nombre_corto || rot.id
}

function nombreCorto(rot, idioma) {
  const n = idioma === 'en' ? (rot.en && rot.en.nombre_corto) || rot.nombre_corto : rot.nombre_corto
  return n ? n.charAt(0).toUpperCase() + n.slice(1) : rot.id
}

function Mata({ viva }) {
  return viva ? (
    <svg className="agr-mata agr-mata--viva" viewBox="0 0 20 34" aria-hidden="true" focusable="false">
      <path d="M10 33 V6" />
      <path d="M10 26 C 6 23, 3 24, 1 27" />
      <path d="M10 20 C 14 16, 17 17, 19 20" />
      <path d="M10 14 C 6 10, 3 11, 2 13" />
      <path className="agr-mata-flor" d="M10 6 L8 1 M10 6 L10 0 M10 6 L12 1" />
    </svg>
  ) : (
    <svg className="agr-mata agr-mata--seca" viewBox="0 0 20 34" aria-hidden="true" focusable="false">
      <path d="M10 33 C 10 24, 11 15, 15 8" />
      <path d="M10 26 C 7 27, 4 30, 3 33" />
      <path d="M11 20 C 14 21, 16 25, 16 29" />
      <path d="M12 14 C 9 15, 7 18, 7 21" />
    </svg>
  )
}

export default function Futuro({ farmer, rotaciones, idioma }) {
  const fu = farmer && farmer.futuros
  const frase = ((farmer && farmer.frases) || []).find((x) => x.id === 'futuro')
  if (!fu || !frase || !Array.isArray(fu.rotaciones)) return null
  const t = TEXTOS[idioma] || TEXTOS.es
  const porId = Object.fromEntries((rotaciones || []).map((r) => [r.id, r]))
  // La de hoy primero, luego las alternativas en el orden del motor.
  const orden = [...(rotaciones || [])].sort((a, b) => Number(b.es_actual) - Number(a.es_actual))
  const filas = orden.map((r) => fu.rotaciones.find((x) => x.id === r.id)).filter(Boolean)
  return (
    <section className="agr-tarjeta agr-futuro" aria-labelledby="agr-futuro-titulo" lang={idioma} data-futuro={fu.n_modelos}>
      <h2 id="agr-futuro-titulo" className="agr-subtitulo">{t.titulo(fu.desde, fu.hasta)}</h2>
      <p className="agr-tarjeta-frase">{frase[idioma] || frase.es}</p>
      <ul className="agr-futuro-lista">
        {filas.map((x) => {
          const rot = porId[x.id]
          const nombre = rot.es_actual ? t.hoy(nombreHoy(rot, idioma)) : nombreCorto(rot, idioma)
          return (
            <li key={x.id} className={`agr-futuro-fila${rot.es_actual ? ' agr-futuro-fila--hoy' : ''}`} data-aguantan={x.aguantan}>
              <p className="agr-futuro-nombre">
                <span>{nombre}</span> <strong>{t.cuantas(x.aguantan, x.de)}</strong>
              </p>
              <div className="agr-matas" role="img" aria-label={`${nombre}: ${t.matas(x.aguantan, x.de)}`}>
                {(x.por_modelo || []).map((viva, i) => (
                  <Mata key={i} viva={viva} />
                ))}
              </div>
            </li>
          )
        })}
      </ul>
      <p className="agr-nota">{t.leyenda}</p>
    </section>
  )
}
