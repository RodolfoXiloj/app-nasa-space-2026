// «Este año»: la lluvia de julio y agosto de esta parcela frente a un año normal y al año más seco desde 1991, en
// tres barras que se entienden sin leer números (15 nov 2026: el antes y después, también para el agricultor). Las
// cifras vienen del bloque `farmer.este_anio` del JSON (motor/farmer.py, de data/validacion.json y
// data/explorar/{pid}.json) y la frase es la misma que lee el audio corto (`farmer.frases`, id «este_anio»).
// Es una observación preliminar, no un pronóstico: lo dice la frase. Llega con import() después de pintar, como la
// línea 2026, y sus textos viven aquí para no crecer el JS de la primera pantalla.
import './tarjetas.css'

const TEXTOS = {
  es: {
    titulo: 'Este año',
    normal: 'Un año normal',
    seco: (a) => `${a}, el año más seco`,
    este: '2026',
    mm: (n) => `${n} mm`,
    resumen: (n, s, a, e) => `Lluvia de julio y agosto: un año normal, ${n} milímetros; ${a}, ${s}; 2026, ${e}.`,
    nota: 'Lluvia de julio y agosto en su parcela, según CHIRPS (satélite y estaciones). Lo normal es la mediana de 1991 a 2025.',
  },
  en: {
    titulo: 'This year',
    normal: 'A normal year',
    seco: (a) => `${a}, the driest year`,
    este: '2026',
    mm: (n) => `${n} mm`,
    resumen: (n, s, a, e) => `July and August rain: a normal year, ${n} millimeters; ${a}, ${s}; 2026, ${e}.`,
    nota: 'July and August rain at your plot, according to CHIRPS (satellite and stations). Normal is the 1991-2025 median.',
  },
}

export default function EsteAnio({ farmer, idioma }) {
  const e = farmer && farmer.este_anio
  const frase = ((farmer && farmer.frases) || []).find((x) => x.id === 'este_anio')
  // Sin la cifra o sin la frase no se muestra nada: no se adivina.
  if (!e || !frase || typeof e.mediana_mm !== 'number' || typeof e.total_2026_mm !== 'number') return null
  const t = TEXTOS[idioma] || TEXTOS.es
  const filas = [{ id: 'normal', nombre: t.normal, mm: e.mediana_mm }]
  if (e.anio_mas_seco && typeof e.total_mas_seco_mm === 'number') {
    filas.push({ id: 'seco', nombre: t.seco(e.anio_mas_seco), mm: e.total_mas_seco_mm })
  }
  filas.push({ id: 'este', nombre: t.este, mm: e.total_2026_mm })
  const tope = Math.max(...filas.map((f) => f.mm))
  const resumen = t.resumen(e.mediana_mm, e.total_mas_seco_mm, e.anio_mas_seco, e.total_2026_mm)
  return (
    <section className="agr-tarjeta agr-anio" aria-labelledby="agr-anio-titulo" lang={idioma} data-este-anio={e.pct_de_la_mediana}>
      <h2 id="agr-anio-titulo" className="agr-subtitulo">{t.titulo}</h2>
      <p className="agr-tarjeta-frase">{frase[idioma] || frase.es}</p>
      <figure className="agr-barras" role="img" aria-label={resumen}>
        {filas.map((f) => (
          <div key={f.id} className={`agr-barra agr-barra--${f.id}`} aria-hidden="true">
            <span className="agr-barra-nombre">{f.nombre}</span>
            <span className="agr-barra-fondo">
              <span className="agr-barra-lleno" style={{ width: `${Math.max(2, (100 * f.mm) / tope)}%` }} />
            </span>
            <span className="agr-barra-mm">{t.mm(f.mm)}</span>
          </div>
        ))}
      </figure>
      <p className="agr-nota">{t.nota}</p>
    </section>
  )
}
