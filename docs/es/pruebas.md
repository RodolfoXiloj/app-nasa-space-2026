# Registro de pruebas

Solo se anotan corridas reales: cada una con la fecha y la hora en que se corrió (Guatemala, UTC−6), el comando y el resultado tal como lo imprimió.

**Corrección del 14 nov 2026:** la versión anterior de este archivo tenía filas con horas del sábado 14 nov 2026 (de 09:17 a 21:58). Eran horarios planeados, no pruebas hechas, y se quitaron. Siguen en el historial de git (commit `d84918b` y anteriores) solo como referencia del plan, no como resultados.

Leyenda: ✅ pasó · ❌ falló · Pendiente: todavía no se puede hacer.

## Audio en inglés unido a `main`: sábado 14 nov 2026

Unión en un commit de la rama `entrega-audio-en` sobre `main` (con el kit, los documentos y las diapositivas). Cambios de la unión: el kit ofrece `audio/{parcela}.frases.en.mp3` en «Download audio» cuando el idioma es inglés (si falta, el de español); el botón Escuchar ya no se reinicia al cambiar de idioma y, si estaba sonando, sigue con el mp3 del idioma nuevo. Mismo equipo y versiones. Horas de `date`.

| Hora | Qué | Comando | Resultado |
|---|---|---|---|
| 14:30:05 a 14:30:13 | Pruebas automáticas | `python -m pytest -q` | ✅ 222 pasan; salida 0 |
| 14:30:13 a 14:30:15 | Humo de la web | `cd web && npm run smoke` | ✅ «Prueba de humo de la web: sin fallas» |
| 14:30:15 a 14:30:20 | Build | `cd web && npm run build` | ✅ 523 módulos; JS inicial 173.37 kB (gzip 57.27 kB), ver [../peso.md](../peso.md) |
| 14:30:20 a 14:30:33 | Sin red | `cd web && npm run sin-red -- <carpeta temp>` | ✅ 23 de 23; «Listen» con `jocotan.frases.en.mp3` y `.frases.en.vtt`; el kit baja `jocotan.frases.en.mp3` (200 audio/mpeg) |
| 14:30:33 a 14:30:37 | Vista del agricultor a 390 y 412 px | `python web/scripts/agricultor_playwright.py` | ✅ 25 de 25; en inglés suena `jocotan.frases.en.mp3`; al cambiar de idioma con el audio abierto carga la pista del otro idioma |
| 14:30:37 a 14:30:39 | PDF de las diapositivas | `python web/scripts/slides_pdf.py` | ✅ 7 páginas (tope 7) |

## Audio corto en inglés (rama `entrega-audio-en`, antes del commit de esta entrega)

Equipo: Windows 11, Python 3.11.9 (pytest 9.0.2), Node v24.15.0, npm 11.12.1. `npm ci` en `web/` (lockfile del repo). Generación de mp3: `MILPA_ONLINE=1 python -m motor.exportar --audio` y después `python -m motor.exportar` para enlazar JSON.

**Qué reproduce Evidence en inglés:** la interfaz (menús, rotaciones, tarjeta, validación) sale en inglés, pero el audio largo de la tarjeta en cada parcela sigue siendo `audio/{parcela}.mp3` con voz **es-GT-MartaNeural** (mismo archivo que en español). El audio corto en inglés (`audio/{parcela}.frases.en.mp3`, voz en-US-JennyNeural) solo lo usa la vista del agricultor con el botón **Listen** en la primera pantalla.

| Qué | Comando | Resultado |
|---|---|---|
| Pruebas automáticas | `python -m pytest -q` | ✅ 217 pasan; salida 0 |
| Humo de la web | `cd web && npm run smoke` | ✅ 16 JSON + `observacion_2026`; sin fallas |
| Build | `cd web && npm run build` | ✅ vite v6.4.6, 519 módulos, ~3.5 s |
| Sin red | `cd web && npm run sin-red -- <carpeta temp>` | ✅ 20 de 20; «Listen» con `jocotan.frases.en.mp3` y subtítulos `.frases.en.vtt`; totales de Jocotán 80/88/87 sin cambio |

## Línea base del paso 0: sábado 14 nov 2026 (commit `15c5130`)

Después de agregar el bloque `farmer` al contrato, el contraste de los bordes y los espacios fijos de `Controles.jsx`. No se regeneraron datos: los JSON y los mp3 de `web/public/` son los mismos de la línea base anterior. Mismo equipo y mismas versiones (Python 3.11.9, pytest 9.0.2, Node v24.15.0, npm 11.12.1). Las horas son las que imprimió `date` al empezar y al terminar cada comando.

| Fecha y hora | Qué | Comando | Resultado |
|---|---|---|---|
| 14 nov 2026, 12:58:16 a 12:58:21 | Pruebas automáticas | `python -m pytest -rs` | ✅ 98 pasan, 0 fallan, 0 omitidas (3.83 s); salida 0. Son las 79 anteriores más 19 nuevas de `tests/test_farmer.py` |
| 14 nov 2026, 12:58:25 a 12:58:56 | Prueba de humo de la web | `cd web && npm run smoke` | ✅ 16 de 16 JSON «ok» y `observacion_2026` «ok»; «Prueba de humo de la web: sin fallas»; salida 0 |
| 14 nov 2026, 12:58:56 a 12:59:07 | Build de la web | `cd web && npm run build` | ✅ vite v6.4.6, 498 módulos, «built in 10.00s»; JS de 770.39 kB (220.58 kB con gzip) y CSS de 24.99 kB; salida 0 |
| 14 nov 2026, 12:59:11 a 12:59:23 | Prueba sin red (Edge sin interfaz, sobre el build anterior) | `cd web && npm run sin-red -- <carpeta temporal fuera del repo>` | ✅ «14 de 14 comprobaciones pasan»; salida 0. Las mismas 14 comprobaciones de abajo; audio de 71 a 73 s y PDF de 61 KB |
| 14 nov 2026, 12:59:29 | Procesos después de las pruebas | `Get-NetTCPConnection` (puertos 4173, 4174 y 9334) + búsqueda de procesos de Edge sin interfaz y de vite + `git status --short` | ✅ ningún puerto escuchando, ningún proceso de Edge sin interfaz ni de vite; árbol de trabajo sin cambios |

Antes de esta línea base, el mismo 14 nov 2026 (sin hora anotada), se corrió `motor.recomendar.recomendar()` en memoria para las 5 parcelas, sin escribir archivos: el bloque `farmer` cumple el esquema y `contrato.errores_textos` no da errores en ninguna. Esas corridas dan las cifras de `docs/umbrales.md`.

## Línea base: sábado 14 nov 2026 (commit `d84918b`)

Equipo: laptop con Windows 11, Python 3.11.9 (pytest 9.0.2), Node v24.15.0 y npm 11.12.1. No se instaló nada: `web/node_modules` ya estaba en el repo. Las horas son las que imprimió `date` al empezar y al terminar cada comando.

| Fecha y hora | Qué | Comando | Resultado |
|---|---|---|---|
| 14 nov 2026, 12:09:41 a 12:09:47 | Pruebas automáticas | `python -m pytest -rs` | ✅ 79 pasan, 0 fallan, 0 omitidas (3.91 s); salida 0 |
| 14 nov 2026, 12:09:51 a 12:10:22 | Prueba de humo de la web | `cd web && npm run smoke` | ✅ 16 de 16 JSON «ok» (según el script, cada uno con 6 componentes × 3 escenarios y su mp3 con la etiqueta de IA) y `observacion_2026` «ok»; «Prueba de humo de la web: sin fallas»; salida 0 |
| 14 nov 2026, 12:10:29 a 12:10:39 | Build de la web | `cd web && npm run build` | ✅ vite v6.4.6, 498 módulos, «built in 9.38s»; JS de 770.39 kB (220.58 kB con gzip) y CSS de 24.94 kB; salida 0 |
| 14 nov 2026, 12:10:45 a 12:10:56 | Prueba sin red (Edge sin interfaz con un proxy inexistente, sobre el build anterior) | `cd web && npm run sin-red -- <carpeta temporal fuera del repo>` | ✅ «14 de 14 comprobaciones pasan»; salida 0. Detalle abajo |
| 14 nov 2026, 12:11 | Procesos y árbol de trabajo después de las pruebas | `Get-NetTCPConnection` (puertos 4173, 4174 y 9334) + búsqueda de procesos de Edge sin interfaz y de vite + `git status --short` | ✅ ningún puerto escuchando, ningún proceso de Edge sin interfaz ni de vite; árbol de trabajo sin cambios |

Las 14 comprobaciones de `npm run sin-red`, tal como las imprimió:

1. Sin internet: la petición a `tile.openstreetmap.org` falló («Failed to fetch»).
2. La página abre (título).
3. Observación de 2026 en la primera pantalla, sin «alerta».
4. a 8. Las 5 parcelas (Jocotán, Camotán, Olopa, San Juan Ermita, Zacapa): 3 rotaciones, tarjeta y audio mp3 que suena (de 71 a 73 s de duración), con el rótulo de IA.
9. El mapa pasa solo a la capa «Color real MODIS (sin red)»: 4 teselas locales, con aviso y con el control de capas marcado.
10. Pestaña Validación con el detalle de 2026.
11. Pestaña Glosario y fuentes (cita IMERG).
12. Imprimir o guardar PDF: 61 KB.
13. Peticiones locales: 20, todas responden. El navegador cortó 6 descargas de mp3 después de que respondieron (206, `net::ERR_ABORTED`); el script no las cuenta como falla.
14. Peticiones externas: 19 (`tile.openstreetmap.org`); ninguna llegó.

Ninguna prueba falló en esta corrida.

## Pendiente

Todavía no se pueden hacer, así que no tienen hora ni resultado:

| Prueba | Estado |
|---|---|
| Teléfono real (Android o iPhone), con la lista de `docs/es/prueba-telefono.md` | Pendiente |
| TalkBack (lector de pantalla de Android) en el teléfono | Pendiente |
| Revisión con un agrónomo o extensionista de las reglas de puntaje y las 8 plantillas | Pendiente |
| Prueba de comprensión con personas usuarias (tarjeta y audio) | Pendiente |

## Sin corrida real registrada

El registro anterior también daba como hechas, con horas planeadas, estas pruebas y tareas. No se corrieron en esta línea base, así que no tienen resultado:

- Consultas y descargas en línea: POWER, ORNL, FIRMS, CHIRPS, SoilGrids (REST y su respaldo WCS), SMAP por AppEEARS, GIBS y Sentinel-2.
- `python -m pipeline.validacion.validar` y `python -m motor.exportar` (con `--audio` o `--etiquetar`, o sin ellas).
- Cotejo de cifras de las tarjetas contra `data/cache/` (plan 12.6). El script no está en el repo.
- La web servida en la red local (`npx vite preview --host 0.0.0.0`) y consultada por la IP de la laptop.
- La web con internet en Edge sin interfaz (sin proxy).
- Las capturas de `docs/capturas/` y su verificación (audio, consola, desborde de la tarjeta a 360, 390 y 1366 px).
- La prueba negativa de la verificación de audio del humo (quitar un mp3 y ver que falle).
- `graphify update .` y la revisión de los `[[enlaces]]` de `docs/es/memoria/`.
