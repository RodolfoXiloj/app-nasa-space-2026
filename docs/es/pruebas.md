# Registro de pruebas

Solo se anotan corridas reales: cada una con la fecha y la hora en que se corrió (Guatemala, UTC−6), el comando y el resultado tal como lo imprimió.

**Corrección del 14 nov 2026:** la versión anterior de este archivo tenía filas con horas del sábado 14 nov 2026 (de 09:17 a 21:58). Eran horarios planeados, no pruebas hechas, y se quitaron. Siguen en el historial de git (commit `d84918b` y anteriores) solo como referencia del plan, no como resultados.

Leyenda: ✅ pasó · ❌ falló · Pendiente: todavía no se puede hacer.

## `main` con `entrega-impacto-6` unida y las guías corregidas: sábado 14 nov 2026

`entrega-impacto-6` se puso encima de `main` (que ya traía la línea de julio-agosto 2026 del agricultor y las guías de pruebas con personas). Sobre eso: capturas de `docs/capturas/` rehechas desde el sitio actual (script nuevo `web/scripts/evidence_capturas.py`), capturas y PDF de las diapositivas regenerados, la tarjeta de Evidence ya no repite «Lo que ve el satélite:» ni «Fecha de siembra:», las guías de `docs/es/pruebas-personas/` corregidas contra el texto real del sitio, `docs/es/preguntas-agricultor.md` y una prueba nueva (`tests/test_repo.py`: nada de lo que excluye `.gitignore` está en el repo). Mismo equipo: Windows 11, Python 3.11.9 (pytest 9.0.2), Node v24.15.0, npm 11.12.1, Playwright 1.58.0. Horas de `date` (UTC−6).

| Hora | Qué | Comando | Resultado |
|---|---|---|---|
| 17:56:08 a 17:56:14 | Build | `cd web && npm run build` | ✅ «526 modules transformed», «built in 4.65s»; JS inicial `index` 171.70 kB (gzip 56.85 kB), JS de Evidence 673.30 kB (gzip 190.77 kB); salida 0 |
| 17:56:14 a 17:56:43 | Capturas de Evidence | `cd web && python scripts/evidence_capturas.py` | ✅ «26 capturas»; salida 0 |
| 17:56:44 a 17:57:00 | Capturas del agricultor | `cd web && python scripts/agricultor_playwright.py --capturas` | ✅ «96 de 96 comprobaciones pasan»; salida 0 |
| 17:57:00 a 17:57:07 | Capturas de las diapositivas | `cd web && python scripts/slides_capturas.py` | ✅ 4 capturas «OK»; salida 0 |
| 17:57:07 a 17:57:09 | PDF de las diapositivas | `cd web && python scripts/slides_pdf.py` | ✅ «docs/slides/milpa-resiliente.pdf: 7 páginas (tope 7)»; salida 0 |
| 17:57:09 a 17:57:24 | Pruebas automáticas | `python -m pytest -q` | ✅ solo puntos, hasta «[100%]», sin fallas; salida 0 |
| 17:57:24 a 17:57:40 | Pruebas automáticas con el total | `python -m pytest -p no:cacheprovider -o addopts=''` | ✅ «250 passed in 15.20s»; salida 0 |
| 17:57:40 a 17:57:42 | Humo de la web | `cd web && npm run smoke` | ✅ «Prueba de humo de la web: sin fallas»; salida 0 |
| 17:57:42 a 17:57:55 | Sin red | `cd web && npm run sin-red -- <carpeta temporal fuera del repo>` | ✅ «23 de 23 comprobaciones pasan»; salida 0 |
| 17:57:55 a 17:58:03 | Vista del agricultor y kit a 360, 390 y 412 px | `python web/scripts/agricultor_playwright.py` | ✅ «96 de 96 comprobaciones pasan»; salida 0 |
| 17:58:03 a 17:58:15 | Vista Evidence a 360, 390 y 412 px | `python web/scripts/evidence_playwright.py` | ✅ «143 de 143 comprobaciones pasan»; salida 0 |
| 17:58:15 a 17:58:16 | Sensibilidad de la canícula | `python -m pipeline.validacion.sensibilidad_canicula --verificar` | ✅ «OK 'sat': jocotan 2, camotan 2, olopa 0, san_juan_ermita 1, zacapa 3 de 25 años»; «OK 'rnl': caché completa; totales mensuales iguales a 'sat'»; salida 0 |

Antes de esta corrida se regeneró sin red con `python -m motor.exportar` (sin `--audio`) por un cambio de redacción en el inglés de un beneficio de la rotación actual: `puntajes`, `farmer.hechos`, `farmer.opciones` y `texto_tarjeta` quedaron idénticos; en los 5 JSON principales solo cambió esa frase.

## Subtítulos en inglés del audio corto (rama `entrega-impacto-6`): sábado 14 nov 2026

Los `.frases.en.vtt` traían los tiempos del mp3 en español (terminaban entre 25.98 y 28.60 s) aunque los `.frases.en.mp3` duran de 28.48 a 29.81 s. El exportador copiaba esos tiempos a la etiqueta del mp3 en inglés al generarlo; ahora guarda los del inglés y, para los mp3 ya generados, los lee del propio audio (las 5 uniones de 0.25 s entre frases, con ffmpeg y sin red). Regenerado con `python -m motor.exportar`, sin `--audio`: solo cambian los 5 `.en.vtt`; los mp3 no se tocaron. Horas de `date` (UTC−6).

| Hora | Qué | Comando | Resultado |
|---|---|---|---|
| 17:14:30 a 17:14:46 | Pruebas automáticas | `python -m pytest -q` | ✅ solo puntos, hasta «[100%]», sin fallas; salida 0 |
| 17:14:46 a 17:15:02 | Pruebas automáticas con el total | `python -m pytest -p no:cacheprovider -o addopts=''` | ✅ «249 passed in 15.27s» |
| 17:15:02 a 17:15:04 | Humo de la web | `cd web && npm run smoke` | ✅ «Prueba de humo de la web: sin fallas»; salida 0 |
| 17:15:04 a 17:15:10 | Build | `cd web && npm run build` | ✅ JS inicial `index` 171.54 kB (gzip 56.81 kB); salida 0 |
| 17:15:10 a 17:15:19 | Vista del agricultor y kit a 360, 390 y 412 px | `python web/scripts/agricultor_playwright.py` | ✅ «77 de 77 comprobaciones pasan»; salida 0 |

La prueba nueva `test_ultimo_subtitulo_termina_con_su_mp3` falla en las 5 parcelas con los `.en.vtt` anteriores y pasa con los nuevos.

## Rama `entrega-impacto-6` sobre `main` (`5a5d6d3`): sábado 14 nov 2026

Cambios de esta rama: bloque `perdidas_documentadas` en `validacion.json` y en `docs/validacion.md`, límite de 2026 y notas de SMAP, CHIRPS y Prensa Libre con su inglés, el mp3 de la tarjeta de Evidence en el idioma de la interfaz, capturas y PDF de las diapositivas regenerados, y pruebas nuevas en `tests/test_validacion.py` y `tests/test_slides.py`. `sin-red.mjs` ahora exige `audio/{parcela}.en.mp3` en la tarjeta cuando Evidence está en inglés (antes exigía el mp3 en español en los dos idiomas); `evidence_playwright.py` comprueba el mp3 de la tarjeta en cada idioma. Antes se regeneró sin red con `python -m pipeline.validacion.validar` y `python -m motor.exportar` (sin `--audio`): `puntajes`, `farmer.hechos`, `farmer.opciones` y `texto_tarjeta` quedaron idénticos en los 15 JSON de parcela. Mismo equipo: Windows 11, Python 3.11.9 (pytest 9.0.2), Node v24.15.0, npm 11.12.1, Playwright 1.58.0; `web/node_modules` con `npm ci`. Horas de `date` (UTC−6).

| Hora | Qué | Comando | Resultado |
|---|---|---|---|
| 17:05:14 a 17:05:24 | Pruebas automáticas | `python -m pytest -q` | ✅ solo puntos, hasta «[100%]», sin fallas; salida 0 |
| 17:05:24 a 17:05:34 | Pruebas automáticas con el total | `python -m pytest -p no:cacheprovider -o addopts=''` | ✅ «237 passed in 9.43s»; salida 0 |
| 17:05:35 a 17:05:36 | Humo de la web | `cd web && npm run smoke` | ✅ 16 JSON «ok», «audio de la tarjeta en inglés con etiqueta de IA: 5 mp3», «ok futuros_nasa (5 parcelas)»; «Prueba de humo de la web: sin fallas»; salida 0 |
| 17:05:36 a 17:05:42 | Build | `cd web && npm run build` | ✅ «525 modules transformed», «built in 4.48s»; JS inicial `index` 171.54 kB (gzip 56.81 kB), JS de Evidence 673.19 kB (gzip 190.72 kB); salida 0 |
| 17:05:42 a 17:05:55 | Sin red | `cd web && npm run sin-red -- <carpeta temporal fuera del repo>` | ✅ «23 de 23 comprobaciones pasan»; la tarjeta de cada parcela suena con `{parcela}.en.mp3`; salida 0 |
| 17:05:55 a 17:06:04 | Vista del agricultor y kit a 360, 390 y 412 px | `python web/scripts/agricultor_playwright.py` | ✅ «77 de 77 comprobaciones pasan»; salida 0 |
| 17:06:04 a 17:06:19 | Vista Evidence a 360, 390 y 412 px | `python web/scripts/evidence_playwright.py` | ✅ «143 de 143 comprobaciones pasan»; salida 0 |
| 17:06:19 a 17:06:21 | PDF de las diapositivas | `cd web && python scripts/slides_pdf.py` | ✅ «docs/slides/milpa-resiliente.pdf: 7 páginas (tope 7)»; «python-pptx no está instalado: no se genera .pptx»; salida 0 |
| 17:06:21 a 17:06:22 | Sensibilidad de la canícula | `python -m pipeline.validacion.sensibilidad_canicula --verificar` | ✅ «OK 'sat': jocotan 2, camotan 2, olopa 0, san_juan_ermita 1, zacapa 3 de 25 años»; «OK 'rnl': caché completa; totales mensuales iguales a 'sat'»; salida 0 |

Antes de esta corrida, la misma batería tuvo dos fallas que se corrigieron:

- `evidence_playwright.py` (sin hora anotada): «137 de 143». Las 6 en «Validación», «sin scroll horizontal» (ancho 419 a 420 px), por la URL del README de CHIRPS en la nota nueva. Se agregó `.lista-compacta li` a la regla `overflow-wrap: anywhere` de `evidence.css`; después, «143 de 143».
- `npm run sin-red`, 16:58:38 a 17:00:05: «18 de 23», salida 1. Las 5 «Parcela …: 3 rotaciones, tarjeta y audio mp3» esperaban `audio/{parcela}.mp3` con Evidence en inglés, que ahora toca `audio/{parcela}.en.mp3`. Se cambió la comprobación para exigir el mp3 del idioma activo; después, «23 de 23».

## Rama `entrega-impacto-1` sobre `main` (`4fdf64f`): sábado 14 nov 2026

Mientras se trabajaba esta rama, `main` recibió tres commits (`61bf817`, `b69bcd1` y `4fdf64f`: audio de la tarjeta en inglés, diapositivas y fuentes). La rama se rebasó sobre `4fdf64f`, sin archivos en común, y todos los comandos se corrieron otra vez sobre la rama rebasada con los cambios de esta rama. Mismo equipo y versiones que la sección siguiente; `web/node_modules` viene del `npm ci` anotado ahí. Horas de `date` (UTC−6).

| Hora | Qué | Comando | Resultado |
|---|---|---|---|
| 16:11:47 a 16:11:57 | Pruebas automáticas | `python -m pytest -q` | ✅ solo puntos, hasta «[100%]», sin fallas; salida 0 |
| 16:11:57 a 16:12:06 | Humo de la web | `cd web && npm run smoke` | ✅ 16 JSON «ok», `observacion_2026` «ok» y «audio de la tarjeta en inglés con etiqueta de IA: 5 mp3»; «Prueba de humo de la web: sin fallas»; salida 0 |
| 16:12:06 a 16:12:14 | Build | `cd web && npm run build` | ✅ «523 modules transformed», «built in 6.11s»; JS inicial `index` 170.90 kB (gzip 56.50 kB), JS de Evidence 657.80 kB (gzip 184.77 kB); salida 0 |
| 16:12:14 a 16:12:28 | Sin red | `cd web && npm run sin-red -- <carpeta temporal fuera del repo>` | ✅ «23 de 23 comprobaciones pasan»; salida 0 |
| 16:12:28 a 16:12:37 | Vista del agricultor y kit a 360, 390 y 412 px | `python web/scripts/agricultor_playwright.py` | ✅ «77 de 77 comprobaciones pasan»; salida 0 |
| 16:12:37 a 16:12:49 | Vista Evidence a 390 y 412 px | `python web/scripts/evidence_playwright.py` | ✅ «109 de 109 comprobaciones pasan»; salida 0 |
| 16:12:49 a 16:12:50 | PDF de las diapositivas | `cd web && python scripts/slides_pdf.py` | ✅ «docs/slides/milpa-resiliente.pdf: 7 páginas (tope 7)»; «python-pptx no está instalado: no se genera .pptx»; salida 0. El PDF reescrito se restauró con `git checkout` |
| Justo después, antes de las 16:13:17 | Pruebas automáticas con el total | `python -m pytest` | ✅ «226 passed in 9.53s» |
| Justo después, antes de las 16:13:17 | Lo mismo en el entorno limpio fuera del repo | `python -m pytest -q` (con el Python del entorno limpio) | ✅ salida 0 |

## Rama `entrega-impacto-1`, primera pasada sobre `eed0b1f`: sábado 14 nov 2026

Esta rama solo cambia documentos, `requirements.txt` y `render.yaml`. Las corridas de la web y del navegador de abajo se hicieron en la rama en el commit `eed0b1f` (el mismo de `main`), antes de esos cambios; las tres últimas filas se corrieron después. Mismo equipo: Windows 11, Python 3.11.9 (pytest 9.0.2), Node v24.15.0, npm 11.12.1, Playwright 1.58.0. El worktree no tenía `web/node_modules`, así que primero se corrió `npm ci`. Las horas son las que imprimió `date` al empezar y al terminar cada comando (UTC−6).

| Hora | Qué | Comando | Resultado |
|---|---|---|---|
| 15:57:47 a 15:57:56 | Instalar las dependencias de la web | `cd web && npm ci` | ✅ «added 108 packages, and audited 109 packages in 8s»; «found 0 vulnerabilities»; salida 0 |
| 15:57:56 a 15:58:15 | Pruebas automáticas | `python -m pytest -q` | ✅ solo puntos, hasta «[100%]», sin fallas; con `addopts = "-q"` en `pyproject.toml` este comando no imprime el total; salida 0 |
| 15:58:15 a 15:58:19 | Humo de la web | `cd web && npm run smoke` | ✅ 16 JSON «ok» y `observacion_2026` «ok»; «Prueba de humo de la web: sin fallas»; salida 0 |
| 15:58:19 a 15:58:27 | Build | `cd web && npm run build` | ✅ vite v6.4.6, «523 modules transformed», «built in 5.98s»; JS inicial `index` 170.90 kB (gzip 56.50 kB), JS de Evidence 657.80 kB (gzip 184.77 kB); salida 0 |
| 15:58:27 a 15:58:46 | Sin red | `cd web && npm run sin-red -- <carpeta temporal fuera del repo>` | ❌ «21 de 23 comprobaciones pasan»; salida 1. Las dos marcadas «NO»: el audio de la tarjeta de San Juan Ermita («suena 0.0 s de 67 s») y «Español elegido en Evidence sigue al volver a la vista del agricultor» (imprimió «en: What the satellite saw on this plot») |
| 16:01:02 a 16:01:16 | Sin red, repetida sin cambiar nada | `cd web && npm run sin-red -- <otra carpeta temporal>` | ✅ «23 de 23 comprobaciones pasan»; salida 0. No se encontró la causa de las dos fallas de la primera corrida |
| 15:58:46 a 15:58:57 | Vista del agricultor y kit a 360, 390 y 412 px | `python web/scripts/agricultor_playwright.py` | ✅ «77 de 77 comprobaciones pasan»; salida 0 |
| 15:58:57 a 15:59:09 | Vista Evidence a 390 y 412 px | `python web/scripts/evidence_playwright.py` | ✅ «109 de 109 comprobaciones pasan»; salida 0 |
| 15:59:09 a 15:59:11 | PDF de las diapositivas | `cd web && python scripts/slides_pdf.py` | ✅ «docs/slides/milpa-resiliente.pdf: 7 páginas (tope 7)»; «python-pptx no está instalado: no se genera .pptx»; salida 0. El comando reescribió `docs/slides/milpa-resiliente.pdf`; se restauró con `git checkout` |
| 15:59:48 a 16:00:46 | Entorno limpio fuera del repo | `python -m venv <carpeta temporal>`, `pip install -r requirements.txt`, `python -m pytest -q` | ✅ instaló PyYAML 6.0.3, requests 2.34.2, pytest 9.2.0, jsonschema 4.26.0 y Pillow 13.0.0; solo puntos, hasta «[100%]», sin fallas |
| 16:08:43 a 16:08:52 | Pruebas automáticas, después de los cambios de esta rama | `python -m pytest -q` | ✅ solo puntos, hasta «[100%]», sin fallas; salida 0 |
| 16:08:52 a 16:09:01 | Lo mismo, en el entorno limpio | `python -m pytest -q` (con el Python del entorno limpio) | ✅ solo puntos, hasta «[100%]», sin fallas; salida 0 |
| Justo después (sin hora anotada) | Pruebas automáticas con el total | `python -m pytest` | ✅ «222 passed in 8.10s» |

Antes de la fila del entorno limpio, un primer entorno limpio sin Pillow (sin hora anotada) falló 3 pruebas de `tests/test_pipeline.py` (`test_lzw_igual_que_pillow`, `test_lzw_con_muchos_codigos`, `test_lector_ligero_lee_solo_hasta_la_columna`) con «ModuleNotFoundError: No module named 'PIL'». Por eso Pillow ahora es una línea obligatoria de `requirements.txt`.

## Futuros de NASA NEX-GDDP-CMIP6 (rama `carril-g-earth-engine`): sábado 14 nov 2026

Corrido en una copia del repo sin los binarios (mp3, png, pdf). Las 23 fallas son todas por esos archivos que faltan en esa copia (`test_audio_frases`, `test_audio_ia`, `test_slides`) y fallan igual sin este cambio. Falta repetir las 4 pruebas en una copia completa antes de unir.

| Hora | Qué | Comando | Resultado |
|---|---|---|---|
| 15:39 | Pruebas automáticas | `python -m pytest -q` | 202 pasan, 23 fallan solo por binarios ausentes; `tests/test_futuros.py` 3 de 3 |
| 15:39 | Humo de la web | `cd web && npm run smoke` | «ok futuros_nasa (5 parcelas)»; las únicas fallas son mp3 ausentes |
| 15:39 | Build | `cd web && npm run build` | ✅ |
| 15:39 | Evidence a 1280 y 390 px | Playwright, `#evidence` | Sección visible en inglés, sin desplazamiento horizontal a 390 px |
| Pendiente | Sin red | `cd web && npm run sin-red` | Sin correr: necesita los mp3 |

Repetido en una copia completa de la rama en `2403e3f` (con mp3, png y pdf), en Linux con Chromium sin interfaz (`NAVEGADOR` apuntando a Chromium con `--no-sandbox`):

| Hora | Qué | Comando | Resultado |
|---|---|---|---|
| 15:54 | Pruebas automáticas | `python -m pytest -q` | ✅ 225 pasan |
| 15:55 | Humo de la web | `cd web && npm run smoke` | ✅ «Prueba de humo de la web: sin fallas» |
| 15:55 | Build | `cd web && npm run build` | ✅ |
| 15:58 | Sin red | `cd web && npm run sin-red` | ✅ 23 de 23 |
| 15:59 | PDF de las diapositivas | `python web/scripts/slides_pdf.py` | ✅ 7 páginas (tope 7), con la diapositiva 4 de futuros |

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
