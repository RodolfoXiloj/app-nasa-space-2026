# Initial page weight / Peso inicial de la página

## English

Measured on Saturday 14 Nov 2026 at 19:42 (Guatemala), branch `main`, after merging lane B and adding the pictograms and traffic-light colors to the farmer view.

The first screen is the farmer view. The technical view, Evidence, loads with `import()` only when someone opens it. The map (Leaflet), the charts (Recharts) and their styles load with it.

**How we measured:** `npm run build` in `web/` (Vite 6.4.6). We count the JavaScript and CSS that `dist/index.html` requests on first load. Sizes are as Vite reports them (1 kB = 1,000 bytes); gzip is Vite's own figure.

**Budget:** the first screen's JavaScript stays at or under about 170 kB.

| What the first screen downloads | Before lane B (`d2730cd`) | Lane B alone | Now on `main` |
|---|---|---|---|
| JavaScript | 770.39 kB (gzip 220.58 kB) | 162.84 kB (gzip 53.32 kB) | **169.80 kB** (gzip 56.13 kB) |
| CSS | 24.99 kB (gzip 9.06 kB) | 6.56 kB (gzip 1.81 kB) | 7.17 kB (gzip 1.93 kB) |

| Loads only when Evidence opens | Size |
|---|---|
| `Evidencia-*.js`: technical view, map and charts | 651.39 kB (gzip 182.88 kB) |
| `Evidencia-*.css`: Leaflet and technical view styles | 25.38 kB (gzip 9.14 kB) |

- **What the 7 kB since lane B pays for:** the month wheel, the year dots and the 5 pictograms the farmer view now draws (about 8.3 kB), minus what we trimmed. The farmer view no longer imports `lib/datos.js`, so Evidence's scoring helpers load only with Evidence.
- **Most of the 169.80 kB is React and React DOM.** Going much lower means replacing React, a new dependency that needs agreement.
- **How we checked it:** `npm run sin-red` confirms that the first screen does not request the Evidence file. It is only requested after one tap on "See the evidence".

## Español

Medido el sábado 14 nov 2026 a las 19:42 (Guatemala), rama `main`, después de unir el carril B y de poner los pictogramas y los colores del semáforo en la vista del agricultor.

La primera pantalla es la vista del agricultor. La vista técnica, Evidence, se carga con `import()` solo cuando alguien la abre. Con ella llegan el mapa (Leaflet), las gráficas (Recharts) y sus estilos.

**Cómo se midió:** `npm run build` en `web/` (Vite 6.4.6). Se cuentan el JavaScript y el CSS que `dist/index.html` pide al abrir. Los tamaños son los que reporta Vite (1 kB = 1000 bytes); el gzip es la cifra del propio Vite.

**Tope:** el JavaScript de la primera pantalla no pasa de unos 170 kB.

| Lo que descarga la primera pantalla | Antes del carril B (`d2730cd`) | Solo el carril B | Ahora en `main` |
|---|---|---|---|
| JavaScript | 770.39 kB (gzip 220.58 kB) | 162.84 kB (gzip 53.32 kB) | **169.80 kB** (gzip 56.13 kB) |
| CSS | 24.99 kB (gzip 9.06 kB) | 6.56 kB (gzip 1.81 kB) | 7.17 kB (gzip 1.93 kB) |

| Se carga solo al abrir Evidence | Tamaño |
|---|---|
| `Evidencia-*.js`: vista técnica, mapa y gráficas | 651.39 kB (gzip 182.88 kB) |
| `Evidencia-*.css`: estilos de Leaflet y de la vista técnica | 25.38 kB (gzip 9.14 kB) |

- **Qué pagan los 7 kB desde el carril B:** la rueda de meses, los puntos de años y los 5 pictogramas que ahora dibuja la vista del agricultor (unos 8.3 kB), menos lo que se recortó. La vista del agricultor ya no importa `lib/datos.js`, así que los puntajes de Evidence se cargan solo con Evidence.
- **Casi todo lo que pesan los 169.80 kB es React y React DOM.** Bajar mucho más obliga a reemplazar React, una dependencia nueva que necesita acuerdo.
- **Cómo se comprobó:** `npm run sin-red` confirma que la primera pantalla no pide el archivo de Evidence. Solo se pide después de un toque en «Ver la evidencia».
