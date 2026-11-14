import { useEffect, useState } from 'react'
import { PICTOS, TITULOS, RuedaMeses, PuntosAnios, PixelManzanas } from './index.js'

// Galería de prueba, solo para desarrollo. Se abre con `npm run dev` en /src/pictos/galeria.html.
// No la importa ninguna vista, así que no entra en el build de producción.
// Lee los JSON reales de web/public/data/ y no trae cifras propias, salvo la superficie de la manzana,
// que no está en el contrato todavía (ver docs/pictos.md).

const PARCELAS = ['jocotan', 'camotan', 'olopa', 'san_juan_ermita', 'zacapa']
const M2_POR_MANZANA = 6987 // 1 manzana = 10 000 varas² ≈ 6 987 m². Por confirmar: docs/pictos.md

const MODOS = {
  papel: { es: 'Papel (b/n)', en: 'Paper (b/w)' },
  color: { es: 'Color', en: 'Colour' },
  grises: { es: 'Grises', en: 'Greyscale' },
}

const COLOR = {
  '--picto-desnudo': '#8a5a2b',
  '--picto-poca': '#a8754a',
  '--picto-marca': '#3a2a1c',
  color: '#1d2b1a',
}

function deJson(d) {
  const det = d.deteccion
  const can = d.clima.canicula
  const modis = d.fuentes.find((f) => f.id === 'modis_mod13q1')
  return {
    nombre: d.parcela.municipio,
    desnudos: det.meses_desnudos,
    poca: det.meses_poca_cobertura ?? [],
    quema: { valor: det.quemas.anios_con_quema, de: det.quemas.anios_observados },
    canicula: { valor: can.anios_racha_larga, de: can.anios_total },
    ladoPixelM: parseFloat(modis?.resolucion),
  }
}

export default function Galeria() {
  const [lang, setLang] = useState('es')
  const [modo, setModo] = useState('papel')
  const [parcela, setParcela] = useState(PARCELAS[0])
  const [datos, setDatos] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    let vivo = true
    setDatos(null)
    fetch(`/data/${parcela}.json`)
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(`HTTP ${r.status}`))))
      .then((d) => vivo && setDatos(deJson(d)))
      .catch((e) => vivo && setError(String(e)))
    return () => {
      vivo = false
    }
  }, [parcela])

  const estilo = modo === 'papel' ? { color: '#000' } : COLOR
  const filtro = modo === 'grises' ? 'grayscale(1)' : 'none'

  return (
    <main className="galeria" lang={lang} style={{ ...estilo, filter: filtro }}>
      <style>{CSS}</style>
      <header>
        <h1>{lang === 'en' ? 'Pictograms' : 'Pictogramas'}</h1>
        <p className="nota">
          {lang === 'en'
            ? 'Development page. Not linked in the app. Data from web/public/data/.'
            : 'Página de desarrollo. No se enlaza en la app. Datos de web/public/data/.'}
        </p>
        <div className="controles">
          <fieldset>
            <legend>{lang === 'en' ? 'Language' : 'Idioma'}</legend>
            {['es', 'en'].map((l) => (
              <button key={l} type="button" aria-pressed={lang === l} onClick={() => setLang(l)}>
                {l === 'es' ? 'Español' : 'English'}
              </button>
            ))}
          </fieldset>
          <fieldset>
            <legend>{lang === 'en' ? 'Print' : 'Impresión'}</legend>
            {Object.keys(MODOS).map((m) => (
              <button key={m} type="button" aria-pressed={modo === m} onClick={() => setModo(m)}>
                {MODOS[m][lang]}
              </button>
            ))}
          </fieldset>
          <label>
            {lang === 'en' ? 'Plot' : 'Parcela'}{' '}
            <select value={parcela} onChange={(e) => setParcela(e.target.value)}>
              {PARCELAS.map((p) => (
                <option key={p} value={p}>
                  {p}
                </option>
              ))}
            </select>
          </label>
        </div>
      </header>

      <section aria-labelledby="t-iconos">
        <h2 id="t-iconos">{lang === 'en' ? 'The 10 required pictograms' : 'Los 10 pictogramas obligatorios'}</h2>
        <ul className="iconos">
          {Object.entries(PICTOS).map(([clave, Icono]) => (
            <li key={clave}>
              <Icono lang={lang} size={64} />
              <span className="es">{TITULOS[clave].es}</span>
              <span className="en">{TITULOS[clave].en}</span>
            </li>
          ))}
        </ul>
        <div className="tamanos" aria-label={lang === 'en' ? 'Small sizes' : 'Tamaños pequeños'}>
          {Object.entries(PICTOS).map(([clave, Icono]) => (
            <Icono key={clave} decorativo size={24} />
          ))}
        </div>
      </section>

      {error && <p role="alert">{error}</p>}
      {datos && (
        <>
          <section aria-labelledby="t-rueda">
            <h2 id="t-rueda">
              {lang === 'en' ? 'Soil through the year' : 'El suelo en el año'}: {datos.nombre}
            </h2>
            <RuedaMeses desnudos={datos.desnudos} poca={datos.poca} lang={lang} size={260} />
            <h3>{lang === 'en' ? 'No data (grey state)' : 'Sin datos (estado gris)'}</h3>
            <RuedaMeses desnudos={[]} poca={[]} sinDatos lang={lang} size={140} />
          </section>

          <section aria-labelledby="t-anios">
            <h2 id="t-anios">{lang === 'en' ? 'Years as dots' : 'Los años como puntos'}</h2>
            <PuntosAnios tipo="quema" marcados={datos.quema.valor} total={datos.quema.de} lang={lang} size={34} />
            <PuntosAnios tipo="canicula" marcados={datos.canicula.valor} total={datos.canicula.de} lang={lang} size={34} />
          </section>

          <section aria-labelledby="t-pixel">
            <h2 id="t-pixel">{lang === 'en' ? 'What the satellite sees' : 'Lo que ve el satélite'}</h2>
            <PixelManzanas ladoPixelM={datos.ladoPixelM} m2PorManzana={M2_POR_MANZANA} lang={lang} size={260} />
          </section>
        </>
      )}
    </main>
  )
}

const CSS = `
  body { margin: 0; background: #fff; }
  .galeria {
    font-family: system-ui, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif;
    line-height: 1.45; padding: 16px; max-width: 760px; margin: 0 auto; background: #fff;
  }
  .galeria h1 { font-size: 1.6rem; margin: 0 0 4px; }
  .galeria h2 { font-size: 1.15rem; margin: 0 0 12px; }
  .galeria h3 { font-size: 0.95rem; margin: 16px 0 8px; }
  .galeria .nota { margin: 0 0 12px; font-size: 0.9rem; }
  .galeria section { border-top: 3px solid currentColor; padding: 16px 0 20px; display: flex; flex-direction: column; gap: 16px; align-items: flex-start; }
  .galeria section h2, .galeria section h3 { align-self: stretch; }
  .controles { display: flex; flex-wrap: wrap; gap: 8px 16px; align-items: flex-end; margin-bottom: 8px; }
  .controles fieldset { border: 0; padding: 0; margin: 0; display: flex; gap: 4px; flex-wrap: wrap; }
  .controles legend { font-size: 0.8rem; padding: 0; margin-bottom: 2px; }
  .controles button, .controles select {
    font: inherit; font-size: 0.9rem; min-height: 40px; padding: 6px 10px;
    border: 2px solid currentColor; border-radius: 6px; background: #fff; color: inherit;
  }
  .controles button[aria-pressed="true"] { background: #000; color: #fff; border-color: #000; }
  .controles button:focus-visible, .controles select:focus-visible { outline: 3px solid #000; outline-offset: 2px; }
  .iconos { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(104px, 1fr)); gap: 16px 8px; width: 100%; }
  .iconos li { display: flex; flex-direction: column; align-items: center; text-align: center; gap: 2px; }
  .iconos li svg { margin-bottom: 4px; }
  .iconos .es { font-weight: 700; font-size: 0.9rem; }
  .iconos .en { font-size: 0.8rem; }
  .tamanos { display: flex; flex-wrap: wrap; gap: 12px; }
`
