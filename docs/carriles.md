# Carriles de trabajo

Sábado 14 nov 2026. Sale de la sección 5 del plan de ejecución. Cada carril trabaja en su rama y solo toca sus archivos. Rodolfo es el único que une las ramas a `main`.

## Ramas

Las 4 ramas salen de `main` al terminar el paso 0. Todavía no hay worktrees: se crean cuando arranque cada carril.

| Carril | Rama | Qué hace | Quién | Skills |
|---|---|---|---|---|
| A | `carril-a-motor` | Semáforo de 3 hechos con los umbrales confirmados, regla de empate, frases, audio por frases con subtítulos, pruebas | Opus, con Rodolfo (motor) y Mario (audio y regresión) | — |
| B | `carril-b-agricultor` | Vista «Para el agricultor» como primera pantalla, reproductor propio, subtítulos, narración visual | Opus | `frontend-design`, `accessibility` (como reglas de diseño) |
| C | `carril-c-evidence` | Vista «Evidence» en inglés, tabla «NASA product → decision», panel «Where it fails» | Composer 2.5 o Antigravity; Opus revisa | `writing-guidelines` |
| D | `carril-d-pictos` | Pictogramas SVG, rueda de 12 gajos, 15 puntos, píxel en manzanas | Opus; una persona decide si se entienden | `frontend-design` |

## Qué archivos puede tocar cada carril

| Carril | Puede tocar | No toca |
|---|---|---|
| A | `motor/`, `contracts/`, `tests/`, `data/*.yaml`; y, solo después de que Rodolfo confirme `docs/umbrales.md`, los JSON y mp3 regenerados en `web/public/data/` y `web/public/audio/` | `web/src/`, `pipeline/`, `data/cache/` |
| B | `web/src/agricultor/` (nuevo), con sus propios estilos dentro de esa carpeta | `web/src/components/`, `web/src/styles.css`, `motor/`, `contracts/`, `web/public/data/` |
| C | `web/src/components/`, `web/src/i18n/` (nuevo) | `web/src/agricultor/`, `web/src/pictos/`, `motor/`, `contracts/` |
| D | `web/src/pictos/` (nuevo) | Todo lo demás |

Los otros carriles del plan todavía no tienen rama:

| Carril | Puede tocar |
|---|---|
| Kit: hoja impresa, compartir, descargas | `web/src/kit/` (nuevo) |
| Documentos en inglés, guion de radio, borrador del formulario | `README.md`, `docs/` |
| G. Earth Engine (pendiente de la compuerta de las 5:00 p. m.) | `pipeline/clientes/`, `data/cache/` |
| Slides y verificación final | `docs/` |

## Archivos compartidos

Ningún carril los cambia sin avisar a Rodolfo, que los integra al unir:

- `web/src/App.jsx` y `web/src/main.jsx`: aquí se conecta la vista del agricultor como primera pantalla y la vista «Evidence».
- `web/package.json` y `web/package-lock.json`: nada de dependencias nuevas sin acuerdo.
- `web/scripts/smoke.mjs` y `web/scripts/sin-red.mjs`: cada carril propone sus comprobaciones nuevas y Rodolfo las une.
- `docs/pruebas.md`: solo se agregan filas al final de la sección del día, con hora real.

## Reglas

- **Contrato:** el bloque `farmer` ya está en `contracts/recomendacion.schema.json` y lo arma `motor/farmer.py`. Solo el carril A lo cambia. Se pueden agregar campos; no se quitan ni se renombran sin avisar.
- **Umbrales:** nadie regenera datos hasta que Rodolfo confirme `docs/umbrales.md`. Hasta entonces, cada `estado` es `null` y la web no inventa uno.
- **Datos para desarrollar B y D antes de la regeneración:** correr `motor.recomendar.recomendar()` en memoria y guardar la salida en una carpeta temporal fuera del repo. No escribir en `web/public/data/`.
- **Commits:** pequeños y por cambio lógico. Sin menciones a agentes ni archivos de agentes.
- **Push y despliegue:** ningún agente hace push ni despliega; el push lo decide Rodolfo. Nadie despliega en Render hasta que él lo diga.
- **Pruebas antes de pedir la unión:** `python -m pytest`, y en `web/`: `npm run smoke`, `npm run build` y `npm run sin-red`.
- **Carril A, al regenerar el audio:** quitar «prototipo local» del álbum de las etiquetas ID3 (`motor/exportar.py`, función `etiquetar`).
