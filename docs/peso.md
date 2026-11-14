# Initial page weight / Peso inicial de la página

## English

Measured on Saturday 14 Nov 2026 at 13:55 (Guatemala), branch `main`, after merging lane A2 (phrase audio and English from the engine) and adding the Listen button with subtitles to the farmer view. Updated the same day at 14:14 on branch `entrega-kit`, with the community kit, again on `main` after merging the kit, the English docs and the slides, at 14:30 on `main` after merging the English Listen audio, again the same day on branch `entrega-a11y`, with Listen loaded after the first paint, and on branch `entrega-a11y-evidence`, with the accessibility pass on Evidence.

The first screen is the farmer view. The technical view, Evidence, loads with `import()` only when someone opens it. The map (Leaflet), the charts (Recharts) and their styles load with it.

**How we measured:** `npm run build` in `web/` (Vite 6.4.6). We count the JavaScript and CSS that `dist/index.html` requests on first load. Sizes are as Vite reports them (1 kB = 1,000 bytes); gzip is Vite's own figure.

**Budget:** the first screen's JavaScript stays at or under about 172 kB.

| What the first screen downloads | Before lane B (`d2730cd`) | Lane B alone | Pictograms (`9d3daed`) | `main` (`b69fe1c`) | With the kit (`entrega-kit`) | `main` with kit, docs and slides | `main` with English Listen audio | Listen loaded with `import()` (`entrega-a11y`) |
|---|---|---|---|---|---|---|---|---|
| JavaScript | 770.39 kB (gzip 220.58 kB) | 162.84 kB (gzip 53.32 kB) | 169.80 kB (gzip 56.13 kB) | 171.87 kB (gzip 56.77 kB) | 172.26 kB (gzip 56.91 kB) | 172.68 kB (gzip 57.03 kB) | 173.37 kB (gzip 57.27 kB) | **170.90 kB** (gzip 56.50 kB) |
| CSS | 24.99 kB (gzip 9.06 kB) | 6.56 kB (gzip 1.81 kB) | 7.17 kB (gzip 1.93 kB) | 8.22 kB (gzip 2.10 kB) | 8.22 kB (gzip 2.10 kB) | 8.22 kB (gzip 2.10 kB) | 8.22 kB (gzip 2.10 kB) | 8.40 kB (gzip 2.16 kB) |

| Loads only when Evidence opens | Size |
|---|---|
| `Evidencia-*.js`: technical view, map and charts | 657.80 kB (gzip 184.77 kB); 651.42 kB (gzip 182.90 kB) before `entrega-a11y-evidence` |
| `Evidencia-*.css`: Leaflet and technical view styles | 27.89 kB (gzip 9.73 kB); 25.38 kB (gzip 9.14 kB) before |

| Loads with `import()` right after the farmer view paints | Size |
|---|---|
| `Kit-*.js`: community kit (print sheet, audio download, WhatsApp) | 5.83 kB (gzip 2.57 kB) |
| `Kit-*.css`: kit buttons and the black-and-white print sheet | 2.10 kB (gzip 0.87 kB) |
| `Escuchar-*.js`: the Listen button, its subtitles and its texts | 2.71 kB (gzip 1.24 kB) |

- **Evidence accessibility (`entrega-a11y-evidence`) does not touch the first screen:** its JavaScript stays at 170.90 kB and its CSS at 8.40 kB. Evidence grows by 6.38 kB of JavaScript (text alternatives for the five charts and the map in both languages, map zoom and layer names, the calendar read as a list) and 2.51 kB of CSS (48 px targets, focus ring, contrast, calendar textures, reduced motion), and it still loads with `import()` only when someone opens it (see `docs/accessibility.md`, "Evidence view").
- **Back under the budget (`entrega-a11y`):** the Listen button (`web/src/agricultor/Escuchar.jsx`) and its texts now load with `import()` right after the farmer view paints, like the kit. The first screen's JavaScript drops to 170.90 kB, 1.10 kB under the 172 kB budget, with no feature removed. The button shows up a moment after the three facts. The 0.18 kB of CSS pays for the reduced-motion rule and the focus ring on the audio player (see `docs/accessibility.md`).
- **What the 0.69 kB of the English Listen audio pays for:** choosing the Spanish or English mp3 by locale, and resuming playback in the new language when the language changes while the audio plays. It is 1.37 kB over the 172 kB budget; no larger trim was attempted.
- **What the 0.42 kB on `main` pays for:** the tie text now tells a chain tie (Olopa: 87/90/92) from one where every pair is within the margin, in both languages, plus the moved doc paths in Evidence's source notes. It is slightly over the 172 kB budget.
- **What the 0.39 kB of the kit pays for:** only the door to the kit (`web/src/kit/index.jsx`, `lazy` plus `Suspense`) and the one line in `VistaAgricultor.jsx`. The kit itself (`web/src/kit/Kit.jsx`, its texts and CSS) is a separate file that the page asks for after the first paint, so it does not delay the three facts. The sheet reuses the pictograms, the month wheel and the year dots that are already in the first load.

- **What the 2.07 kB since the pictograms pays for:** the Listen button (`web/src/agricultor/Escuchar.jsx`), its subtitles and its texts, plus reading the engine's English names and reasons from the JSON. The phrase audio is not part of the first load: the `<audio>` uses `preload="none"` and the subtitle track is added on the first tap, so the mp3 (about 105 to 116 kB) and the `.vtt` (under 1 kB) download only then.
- **What the 7 kB from lane B to the pictograms paid for:** the month wheel, the year dots and the 5 pictograms the farmer view now draws (about 8.3 kB), minus what we trimmed. The farmer view no longer imports `lib/datos.js`, so Evidence's scoring helpers load only with Evidence.
- **Most of the 171.87 kB is React and React DOM.** Going much lower means replacing React, a new dependency that needs agreement.
- **How we checked it:** `npm run sin-red` confirms that the first screen does not request the Evidence file. It is only requested after one tap on "See the evidence". `python scripts/agricultor_playwright.py` (in `web/`, after the build) confirms at 390 and 412 px that nothing from the phrase audio is requested before the tap on Listen.

## Español

Medido el sábado 14 nov 2026 a las 13:55 (Guatemala), rama `main`, después de unir el carril A2 (audio por frases e inglés del motor) y de poner el botón Escuchar con subtítulos en la vista del agricultor. Actualizado el mismo día a las 14:14 en la rama `entrega-kit`, con el kit comunitario, otra vez en `main` después de unir el kit, los documentos en inglés y las diapositivas, a las 14:30 en `main` después de unir el audio Escuchar en inglés, otra vez el mismo día en la rama `entrega-a11y`, con Escuchar cargado después del primer pintado, y en la rama `entrega-a11y-evidence`, con la revisión de accesibilidad de Evidence.

La primera pantalla es la vista del agricultor. La vista técnica, Evidence, se carga con `import()` solo cuando alguien la abre. Con ella llegan el mapa (Leaflet), las gráficas (Recharts) y sus estilos.

**Cómo se midió:** `npm run build` en `web/` (Vite 6.4.6). Se cuentan el JavaScript y el CSS que `dist/index.html` pide al abrir. Los tamaños son los que reporta Vite (1 kB = 1000 bytes); el gzip es la cifra del propio Vite.

**Tope:** el JavaScript de la primera pantalla no pasa de unos 172 kB.

| Lo que descarga la primera pantalla | Antes del carril B (`d2730cd`) | Solo el carril B | Pictogramas (`9d3daed`) | `main` (`b69fe1c`) | Con el kit (`entrega-kit`) | `main` con kit, docs y diapositivas | `main` con el audio Escuchar en inglés | Escuchar con `import()` (`entrega-a11y`) |
|---|---|---|---|---|---|---|---|---|
| JavaScript | 770.39 kB (gzip 220.58 kB) | 162.84 kB (gzip 53.32 kB) | 169.80 kB (gzip 56.13 kB) | 171.87 kB (gzip 56.77 kB) | 172.26 kB (gzip 56.91 kB) | 172.68 kB (gzip 57.03 kB) | 173.37 kB (gzip 57.27 kB) | **170.90 kB** (gzip 56.50 kB) |
| CSS | 24.99 kB (gzip 9.06 kB) | 6.56 kB (gzip 1.81 kB) | 7.17 kB (gzip 1.93 kB) | 8.22 kB (gzip 2.10 kB) | 8.22 kB (gzip 2.10 kB) | 8.22 kB (gzip 2.10 kB) | 8.22 kB (gzip 2.10 kB) | 8.40 kB (gzip 2.16 kB) |

| Se carga solo al abrir Evidence | Tamaño |
|---|---|
| `Evidencia-*.js`: vista técnica, mapa y gráficas | 657.80 kB (gzip 184.77 kB); 651.42 kB (gzip 182.90 kB) antes de `entrega-a11y-evidence` |
| `Evidencia-*.css`: estilos de Leaflet y de la vista técnica | 27.89 kB (gzip 9.73 kB); 25.38 kB (gzip 9.14 kB) antes |

| Se carga con `import()` justo después de pintar la vista del agricultor | Tamaño |
|---|---|
| `Kit-*.js`: kit comunitario (hoja para imprimir, descarga del audio, WhatsApp) | 5.83 kB (gzip 2.57 kB) |
| `Kit-*.css`: botones del kit y hoja de impresión en blanco y negro | 2.10 kB (gzip 0.87 kB) |
| `Escuchar-*.js`: el botón Escuchar, sus subtítulos y sus textos | 2.71 kB (gzip 1.24 kB) |

- **La accesibilidad de Evidence (`entrega-a11y-evidence`) no toca la primera pantalla:** su JavaScript sigue en 170.90 kB y su CSS en 8.40 kB. Evidence crece 6.38 kB de JavaScript (alternativas en texto de las cinco gráficas y del mapa en los dos idiomas, nombres del zoom y de las capas del mapa, el calendario leído como lista) y 2.51 kB de CSS (objetivos de 48 px, foco visible, contraste, texturas del calendario, movimiento reducido), y sigue llegando con `import()` solo cuando alguien la abre (ver `docs/accessibility.md`, «Evidence view»).
- **De nuevo bajo el tope (`entrega-a11y`):** el botón Escuchar (`web/src/agricultor/Escuchar.jsx`) y sus textos ahora llegan con `import()` justo después de pintar la vista del agricultor, como el kit. El JavaScript de la primera pantalla baja a 170.90 kB, 1.10 kB bajo el tope de 172 kB, sin quitar ninguna función. El botón aparece un instante después de los tres hechos. Los 0.18 kB de CSS pagan la regla de movimiento reducido y el foco visible del reproductor de audio (ver `docs/accessibility.md`).
- **Qué pagan los 0.69 kB del audio Escuchar en inglés:** elegir el mp3 en español o en inglés según el idioma, y seguir sonando en el idioma nuevo si se cambia de idioma con el audio sonando. Queda 1.37 kB por encima del tope de 172 kB; no se intentó un recorte grande.
- **Qué pagan los 0.42 kB en `main`:** el texto del empate ahora distingue el empate en cadena (Olopa: 87/90/92) del empate en que todas las parejas están dentro del margen, en los dos idiomas, y las rutas nuevas de los documentos en las fuentes de Evidence. Queda un poco por encima del tope de 172 kB.
- **Qué pagan los 0.39 kB del kit:** solo la puerta del kit (`web/src/kit/index.jsx`, `lazy` y `Suspense`) y la línea en `VistaAgricultor.jsx`. El kit (`web/src/kit/Kit.jsx`, sus textos y su CSS) es un archivo aparte que la página pide después del primer pintado, así que no atrasa los tres hechos. La hoja reutiliza los pictogramas, la rueda de meses y los puntos de años que ya están en la carga inicial.

- **Qué pagan los 2.07 kB desde los pictogramas:** el botón Escuchar (`web/src/agricultor/Escuchar.jsx`), sus subtítulos y sus textos, y leer del JSON los nombres y motivos en inglés del motor. El audio por frases no entra en la carga inicial: el `<audio>` lleva `preload="none"` y la pista de subtítulos se pone al primer toque, así que el mp3 (unos 105 a 116 kB) y el `.vtt` (menos de 1 kB) se descargan solo entonces.
- **Qué pagaron los 7 kB del carril B a los pictogramas:** la rueda de meses, los puntos de años y los 5 pictogramas que ahora dibuja la vista del agricultor (unos 8.3 kB), menos lo que se recortó. La vista del agricultor ya no importa `lib/datos.js`, así que los puntajes de Evidence se cargan solo con Evidence.
- **Casi todo lo que pesan los 171.87 kB es React y React DOM.** Bajar mucho más obliga a reemplazar React, una dependencia nueva que necesita acuerdo.
- **Cómo se comprobó:** `npm run sin-red` confirma que la primera pantalla no pide el archivo de Evidence. Solo se pide después de un toque en «Ver la evidencia». `python scripts/agricultor_playwright.py` (en `web/`, después del build) confirma a 390 y 412 px que no se pide nada del audio por frases antes de tocar Escuchar.
