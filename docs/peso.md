# Initial page weight / Peso inicial de la página

## English

Measured on Saturday 14 Nov 2026 at 13:17 (Guatemala), lane B, branch `carril-b-agricultor`.

The first screen is now the farmer view. The technical view, renamed Evidence, loads with `import()` only when someone opens it. The map (Leaflet), the charts (Recharts) and their styles load with it.

**How we measured:** `npm run build` in `web/` (Vite 6.4.6). We count the JavaScript and CSS that `dist/index.html` requests on first load. Sizes are as Vite reports them (1 kB = 1,000 bytes); gzip is Vite's own figure.

| What the first screen downloads | Before (`d2730cd`) | After | Change |
|---|---|---|---|
| JavaScript | 770.39 kB (gzip 220.58 kB) | 162.84 kB (gzip 53.32 kB) | −78.9 % (gzip −75.8 %) |
| CSS | 24.99 kB (gzip 9.06 kB) | 6.56 kB (gzip 1.81 kB) | −73.8 % (gzip −80.0 %) |

| Loads only when Evidence opens | Size |
|---|---|
| `Evidencia-*.js`: technical view, map and charts | 622.67 kB (gzip 172.91 kB) |
| `Evidencia-*.css`: Leaflet and technical view styles | 24.99 kB (gzip 9.06 kB) |

- **Evidence costs a little more in total:** first screen plus Evidence is 785.51 kB of JavaScript, 15.12 kB more than before. That is the farmer view itself.
- **The 150 kB goal is not met:** most of the 162.84 kB is React and React DOM. Getting under 150 kB means replacing React, which is a new dependency, and lanes do not add dependencies without agreement.
- **How we checked it:** `npm run sin-red` confirms that the first screen does not request the Evidence file. It is only requested after one tap on "See the evidence".

## Español

Medido el sábado 14 nov 2026 a las 13:17 (Guatemala), carril B, rama `carril-b-agricultor`.

La primera pantalla ahora es la vista del agricultor. La vista técnica, que ahora se llama Evidence, se carga con `import()` solo cuando alguien la abre. Con ella llegan el mapa (Leaflet), las gráficas (Recharts) y sus estilos.

**Cómo se midió:** `npm run build` en `web/` (Vite 6.4.6). Se cuentan el JavaScript y el CSS que `dist/index.html` pide al abrir. Los tamaños son los que reporta Vite (1 kB = 1000 bytes); el gzip es la cifra del propio Vite.

| Lo que descarga la primera pantalla | Antes (`d2730cd`) | Después | Cambio |
|---|---|---|---|
| JavaScript | 770.39 kB (gzip 220.58 kB) | 162.84 kB (gzip 53.32 kB) | −78.9 % (gzip −75.8 %) |
| CSS | 24.99 kB (gzip 9.06 kB) | 6.56 kB (gzip 1.81 kB) | −73.8 % (gzip −80.0 %) |

| Se carga solo al abrir Evidence | Tamaño |
|---|---|
| `Evidencia-*.js`: vista técnica, mapa y gráficas | 622.67 kB (gzip 172.91 kB) |
| `Evidencia-*.css`: estilos de Leaflet y de la vista técnica | 24.99 kB (gzip 9.06 kB) |

- **Evidence cuesta un poco más en total:** la primera pantalla más Evidence suman 785.51 kB de JavaScript, 15.12 kB más que antes. Es lo que pesa la vista del agricultor.
- **No se llegó a 150 kB:** casi todo lo que pesan los 162.84 kB es React y React DOM. Bajar de 150 kB obliga a reemplazar React, que es una dependencia nueva, y los carriles no agregan dependencias sin acuerdo.
- **Cómo se comprobó:** `npm run sin-red` confirma que la primera pantalla no pide el archivo de Evidence. Solo se pide después de un toque en «Ver la evidencia».
