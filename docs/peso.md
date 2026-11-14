# Initial page weight / Peso inicial de la página

## English

Measured on Saturday 14 Nov 2026 at 13:55 (Guatemala), branch `main`, after merging lane A2 (phrase audio and English from the engine) and adding the Listen button with subtitles to the farmer view.

The first screen is the farmer view. The technical view, Evidence, loads with `import()` only when someone opens it. The map (Leaflet), the charts (Recharts) and their styles load with it.

**How we measured:** `npm run build` in `web/` (Vite 6.4.6). We count the JavaScript and CSS that `dist/index.html` requests on first load. Sizes are as Vite reports them (1 kB = 1,000 bytes); gzip is Vite's own figure.

**Budget:** the first screen's JavaScript stays at or under about 172 kB.

| What the first screen downloads | Before lane B (`d2730cd`) | Lane B alone | Pictograms (`9d3daed`) | Now on `main` |
|---|---|---|---|---|
| JavaScript | 770.39 kB (gzip 220.58 kB) | 162.84 kB (gzip 53.32 kB) | 169.80 kB (gzip 56.13 kB) | **171.87 kB** (gzip 56.77 kB) |
| CSS | 24.99 kB (gzip 9.06 kB) | 6.56 kB (gzip 1.81 kB) | 7.17 kB (gzip 1.93 kB) | 8.22 kB (gzip 2.10 kB) |

| Loads only when Evidence opens | Size |
|---|---|
| `Evidencia-*.js`: technical view, map and charts | 651.39 kB (gzip 182.88 kB) |
| `Evidencia-*.css`: Leaflet and technical view styles | 25.38 kB (gzip 9.14 kB) |

- **What the 2.07 kB since the pictograms pays for:** the Listen button (`web/src/agricultor/Escuchar.jsx`), its subtitles and its texts, plus reading the engine's English names and reasons from the JSON. The phrase audio is not part of the first load: the `<audio>` uses `preload="none"` and the subtitle track is added on the first tap, so the mp3 (about 105 to 116 kB) and the `.vtt` (under 1 kB) download only then.
- **What the 7 kB from lane B to the pictograms paid for:** the month wheel, the year dots and the 5 pictograms the farmer view now draws (about 8.3 kB), minus what we trimmed. The farmer view no longer imports `lib/datos.js`, so Evidence's scoring helpers load only with Evidence.
- **Most of the 171.87 kB is React and React DOM.** Going much lower means replacing React, a new dependency that needs agreement.
- **How we checked it:** `npm run sin-red` confirms that the first screen does not request the Evidence file. It is only requested after one tap on "See the evidence". `python scripts/agricultor_playwright.py` (in `web/`, after the build) confirms at 390 and 412 px that nothing from the phrase audio is requested before the tap on Listen.

## Español

Medido el sábado 14 nov 2026 a las 13:55 (Guatemala), rama `main`, después de unir el carril A2 (audio por frases e inglés del motor) y de poner el botón Escuchar con subtítulos en la vista del agricultor.

La primera pantalla es la vista del agricultor. La vista técnica, Evidence, se carga con `import()` solo cuando alguien la abre. Con ella llegan el mapa (Leaflet), las gráficas (Recharts) y sus estilos.

**Cómo se midió:** `npm run build` en `web/` (Vite 6.4.6). Se cuentan el JavaScript y el CSS que `dist/index.html` pide al abrir. Los tamaños son los que reporta Vite (1 kB = 1000 bytes); el gzip es la cifra del propio Vite.

**Tope:** el JavaScript de la primera pantalla no pasa de unos 172 kB.

| Lo que descarga la primera pantalla | Antes del carril B (`d2730cd`) | Solo el carril B | Pictogramas (`9d3daed`) | Ahora en `main` |
|---|---|---|---|---|
| JavaScript | 770.39 kB (gzip 220.58 kB) | 162.84 kB (gzip 53.32 kB) | 169.80 kB (gzip 56.13 kB) | **171.87 kB** (gzip 56.77 kB) |
| CSS | 24.99 kB (gzip 9.06 kB) | 6.56 kB (gzip 1.81 kB) | 7.17 kB (gzip 1.93 kB) | 8.22 kB (gzip 2.10 kB) |

| Se carga solo al abrir Evidence | Tamaño |
|---|---|
| `Evidencia-*.js`: vista técnica, mapa y gráficas | 651.39 kB (gzip 182.88 kB) |
| `Evidencia-*.css`: estilos de Leaflet y de la vista técnica | 25.38 kB (gzip 9.14 kB) |

- **Qué pagan los 2.07 kB desde los pictogramas:** el botón Escuchar (`web/src/agricultor/Escuchar.jsx`), sus subtítulos y sus textos, y leer del JSON los nombres y motivos en inglés del motor. El audio por frases no entra en la carga inicial: el `<audio>` lleva `preload="none"` y la pista de subtítulos se pone al primer toque, así que el mp3 (unos 105 a 116 kB) y el `.vtt` (menos de 1 kB) se descargan solo entonces.
- **Qué pagaron los 7 kB del carril B a los pictogramas:** la rueda de meses, los puntos de años y los 5 pictogramas que ahora dibuja la vista del agricultor (unos 8.3 kB), menos lo que se recortó. La vista del agricultor ya no importa `lib/datos.js`, así que los puntajes de Evidence se cargan solo con Evidence.
- **Casi todo lo que pesan los 171.87 kB es React y React DOM.** Bajar mucho más obliga a reemplazar React, una dependencia nueva que necesita acuerdo.
- **Cómo se comprobó:** `npm run sin-red` confirma que la primera pantalla no pide el archivo de Evidence. Solo se pide después de un toque en «Ver la evidencia». `python scripts/agricultor_playwright.py` (en `web/`, después del build) confirma a 390 y 412 px que no se pide nada del audio por frases antes de tocar Escuchar.
