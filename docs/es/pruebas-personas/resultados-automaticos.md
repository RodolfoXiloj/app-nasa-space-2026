# Resultados de las pruebas automáticas de apoyo (Parte B)

**Fecha de ejecución:** `2026-11-14` (zona horaria local `UTC-06:00`)  
**Rama / worktree:** `entrega-pruebas-personas`  
**Carpeta de artefactos temporales fuera del repositorio:** `$env:TEMP\milpa-pruebas` (no se sube al repo)  

> [!IMPORTANT]
> **Aviso general:** Todas las pruebas registradas en este documento son **comprobaciones automáticas de apoyo técnico**. **No reemplazan a las pruebas que deben hacer Rodolfo Xiloj, Mario e Iván**: ningún script sustituye el oído humano al escuchar la pronunciación de una voz sintética, la navegación táctil real con TalkBack en un teléfono Android físico, la lectura de una hoja impresa y fotocopiada en blanco y negro bajo luz real, la entrevista de comprensión de pictogramas con 3 a 5 adultos, ni la revisión visual de los límites dentro del formulario autenticado de NASA Space Apps.

---

## Resumen de corridas ejecutadas y tiempos reales

| # | Prueba ejecutada | Comando exacto | Inicio (`UTC-06:00`) | Fin (`UTC-06:00`) | Código de salida / Resultado |
|---|---|---|---|---|---|
| **0a** | Construcción de producción de la web (`web/dist`) | `npm run build` (en `web/`) | `2026-11-14T16:29:35-06:00` | `2026-11-14T16:29:40-06:00` | `0` — 523 módulos transformados en 4.22 s (`dist/` listo con `sw.js`). |
| **0b** | Suite de pruebas unitarias de audios, etiquetas de IA y diapositivas | `python -m pytest -v tests/test_audio_frases.py tests/test_audio_ia.py tests/test_slides.py` | `2026-11-14T16:30:16-06:00` | `2026-11-14T16:30:18-06:00` | `0` — **59 de 59 pruebas pasan** en 1.30 s. |
| **0c** | Pruebas de navegador de la vista del agricultor (360, 390 y 412 px, ES/EN) | `python web/scripts/agricultor_playwright.py` | `2026-11-14T16:30:28-06:00` | `2026-11-14T16:30:38-06:00` | `0` — **77 de 77 comprobaciones pasan**. |
| **0d** | Pruebas de navegador de la vista *Evidence* (360, 390 y 412 px, ES/EN, 3 pestañas) | `python web/scripts/evidence_playwright.py` | `2026-11-14T16:34:29-06:00` | `2026-11-14T16:34:42-06:00` | `0` — **109 de 109 comprobaciones pasan**. |
| **0e** | Prueba de humo de contratos JSON y audios | `npm run smoke` (en `web/`) | `2026-11-14T16:34:30-06:00` | `2026-11-14T16:34:42-06:00` | `0` — 16 JSON validados + `observacion_2026` + 5 mp3 en inglés con etiqueta de IA (`sin fallas`). |
| **0f** | Prueba de extremo a extremo sin red (Service Worker con red bloqueada) | `npm run sin-red` (en `web/`) | `2026-11-14T16:34:52-06:00` | `2026-11-14T16:35:05-06:00` | `0` — **23 de 23 comprobaciones pasan**. |
| **1–5** | Script integral de Parte B (conteo de `project-page-en.md`, auditoría de MP3/VTT, cruce de cifras contra JSON, árbol de accesibilidad a 360 px y generación de PDFs en Carta y escala de grises) | `python "$env:TEMP\milpa-pruebas\correr_parte_b.py"` | `2026-11-14T16:39:56-06:00` | `2026-11-14T16:40:04-06:00` | `0` — Guardado en `$env:TEMP\milpa-pruebas\resultados_parte_b.json` y 14 PDFs en Carta/escala de grises. |
| **5 (recálculo)** | Conteo de palabras y caracteres de `docs/project-page-en.md` sobre `main` en el commit `78de49a` | script de conteo por sección (`## ...`) | `2026-11-14T16:54:51-06:00` | `2026-11-14T16:54:51-06:00` | `0` — tabla de la sección 5 actualizada. |

---

## 1. Árbol de accesibilidad de la vista agricultor con Playwright a 360 px (aproximación a TalkBack)

- **Hora real de la corrida:** `2026-11-14T16:39:57-06:00` a `2026-11-14T16:40:04-06:00`
- **Comando usado:** `python "$env:TEMP\milpa-pruebas\correr_parte_b.py"` (más `python web/scripts/agricultor_playwright.py` a las `2026-11-14T16:30:28-06:00`)
- **Configuración del navegador:** Chromium (Playwright) con `viewport={"width": 360, "height": 780}`, `device_scale_factor=2`, `is_mobile=True`, `has_touch=True`.

> **Aviso:** Este árbol de accesibilidad extraído con Playwright a 360 px de ancho es una **aproximación técnica a lo que anunciaría TalkBack** y **no reemplaza la prueba con una persona en un teléfono Android real** (`rodolfo-talkback.md`). No evalúa la síntesis de voz real de Android, la destreza táctil con gestos de barrido ni la convivencia acústica entre TalkBack y el audio MP3 de la parcela.

### 1.1 Verificaciones de diseño y foco a 360 px
- **Sin desborde horizontal a 360 px:** `document.documentElement.scrollWidth = 360 px` tanto en español (`lang="es"`) como en inglés (`lang="en"`).
- **Tamaño táctil mínimo (`48 × 48 px`):** todos los controles interactivos cumplen $\ge 48 \times 48\text{ px}$:
  - Botón `English`: `85 × 48 px`
  - Botón `Español`: `87 × 48 px`
  - Selector `#agr-parcela` (`Parcela`): `328 × 52 px`
  - Botón `Escuchar / Listen`: `328 × 79 px`
  - Botón `Subtítulos / Subtitles`: `119 × 48 px` (ES) / `108 × 48 px` (EN)
  - Botón `Imprimir hoja / Print sheet`: `144 × 48 px` (ES) / `124 × 48 px` (EN)
  - Enlace `Descargar audio / Download audio`: `168 × 48 px` (ES) / `165 × 48 px` (EN)
  - Enlace `Compartir por WhatsApp / Share on WhatsApp`: `236 × 48 px` (ES) / `195 × 48 px` (EN)
  - Botón `Ver la evidencia / See the evidence`: `328 × 82 px`

### 1.2 Orden de lectura y nombres accesibles a 360 px (Español, `lang="es"`, parcela Jocotán)

Árbol ARIA (`locator("body").aria_snapshot()`) capturado con el reproductor de audio abierto y subtítulos activos:

```yaml
- banner:
  - heading "Milpa Resiliente" [level=1]
  - group "Idioma":
    - button "English"
    - button "Español" [pressed]
- main:
  - text: Parcela
  - combobox "Parcela":
    - option "Jocotán, Chiquimula" [selected]
    - option "Camotán, Chiquimula"
    - option "Olopa, Chiquimula"
    - option "San Juan Ermita, Chiquimula"
    - option "Zacapa, Zacapa"
  - paragraph: Parcela de ejemplo en Jocotán.
  - button "Pausar Audio corto, con subtítulos"
  - paragraph: Parcela de Jocotán, con voz de computadora.
  - button "Subtítulos" [pressed]
  - paragraph: Voz sintética generada con IA (edge-tts, texto a voz neural de Microsoft; voz es-GT-MartaNeural) a partir del texto que redactó el motor con plantillas. No es una persona.
  - region "Lo que el satélite vio en esta parcela":
    - heading "Lo que el satélite vio en esta parcela" [level=2]
    - paragraph: Tres hechos de años pasados, siempre en el mismo orden. Son registros, no un pronóstico.
    - list:
      - listitem:
        - heading "Suelo desnudo" [level=3]
        - paragraph: Se repite
        - paragraph: Lo vio seguido.
        - figure "Suelo desnudo Poca cobertura Cubierto":
          - 'img "2 de 12 meses con suelo desnudo (marzo y abril). Poca cobertura: febrero y mayo."'
          - list:
            - listitem: Suelo desnudo
            - listitem: Poca cobertura
            - listitem: Cubierto
        - paragraph: "Suelo: se repite. El satélite vio 2 meses de suelo desnudo."
        - paragraph: "Desnudo: marzo y abril."
        - paragraph: "Poca cobertura: febrero y mayo."
        - paragraph: "Fuente: MODIS (NASA), 2021‑2025."
      - listitem:
        - heading "Quema cerca de la parcela" [level=3]
        - paragraph: Se repite
        - paragraph: Lo vio seguido.
        - figure:
          - img "3 de 15 años con quema vista cerca"
        - paragraph: "Quema: se repite. Vio quemas cerca en 3 de 15 años."
        - paragraph: "Meses con quema: abril y mayo."
        - paragraph: "Fuente: VIIRS (NASA FIRMS), 2012‑2026."
      - listitem:
        - heading "Canícula larga" [level=3]
        - paragraph: Atención
        - paragraph: Lo vio pocas veces.
        - figure:
          - img "2 de 25 años con canícula larga"
        - paragraph: "Canícula: atención. Racha seca de más de 15 días en 2 de 25 años."
        - paragraph: Entre junio y agosto.
        - paragraph: "Fuente: CHIRPS y IMERG (NASA), 2001‑2025."
  - region "Opciones para platicar con su técnico":
    - heading "Opciones para platicar con su técnico" [level=2]
    - paragraph: "Dos opciones quedan parejas: sus puntajes se separan 3 puntos o menos. Ninguna se separa lo suficiente."
    - list:
      - listitem: Leguminosa o cobertura Maíz con canavalia en primera, frijol en postrera y rastrojo en pie
      - listitem: Cultivo tolerante a sequía Sorgo en primera y caupí en postrera, con rastrojo en pie
    - paragraph: Sin orden.
    - paragraph: Lo que hace hoy Maíz con frijol en primera y frijol en postrera
    - heading "Qué tan seguros estamos" [level=3]
    - paragraph: Alta
    - paragraph: "Por qué: Las tres comprobaciones se cumplen."
  - paragraph: Esto no es una alerta oficial; hable con su técnico.
  - region "Compartir esta parcela":
    - heading "Compartir esta parcela" [level=2]
    - paragraph: Una hoja en blanco y negro para imprimir, el audio corto y un mensaje por WhatsApp.
    - button "Imprimir hoja"
    - link "Descargar audio":
      - /url: ./audio/jocotan.frases.mp3
    - link "Compartir por WhatsApp":
      - /url: https://wa.me/?text=Milpa%20Resiliente%2C%20Jocot%C3%A1n%2C%20Chiquimula%0A-%20Suelo%20desnudo%3A%20Se%20repite%0A-%20Quema%20cerca%20de%20la%20parcela%3A%20Se%20repite%0A-%20Can%C3%ADcula%20larga%3A%20Atenci%C3%B3n%0AEsto%20no%20es%20una%20alerta%20oficial%3B%20hable%20con%20su%20t%C3%A9cnico.%0Ahttp%3A%2F%2F127.0.0.1%3A4179%2F
  - button "Ver la evidencia Mapa, gráficas, fuentes y límites"
```

### 1.3 Orden de lectura y nombres accesibles a 360 px (Inglés, `lang="en"`, parcela Jocotán)

```yaml
- banner:
  - heading "Milpa Resiliente" [level=1]
  - group "Language":
    - button "English" [pressed]
    - button "Español"
- main:
  - text: Plot
  - combobox "Plot":
    - option "Jocotán, Chiquimula" [selected]
    - option "Camotán, Chiquimula"
    - option "Olopa, Chiquimula"
    - option "San Juan Ermita, Chiquimula"
    - option "Zacapa, Zacapa"
  - paragraph: Example plot in Jocotán.
  - button "Pause Short audio with subtitles"
  - paragraph: Jocotán plot, read by a computer voice.
  - button "Subtitles" [pressed]
  - paragraph: AI-generated synthetic voice (edge-tts, Microsoft neural text to speech; voice en-US-JennyNeural) from the text the engine wrote with templates. It is not a person.
  - region "What the satellite saw on this plot":
    - heading "What the satellite saw on this plot" [level=2]
    - paragraph: Three facts from past years, always in the same order. They are records, not a forecast.
    - list:
      - listitem:
        - heading "Bare soil" [level=3]
        - paragraph: Repeats
        - paragraph: It saw it often.
        - figure "Bare soil Little cover Covered":
          - 'img "2 of 12 months with bare soil (March and April). Little cover: February and May."'
          - list:
            - listitem: Bare soil
            - listitem: Little cover
            - listitem: Covered
        - paragraph: "Soil: repeats. The satellite saw 2 months of bare soil."
        - paragraph: "Bare: March and April."
        - paragraph: "Little plant cover: February and May."
        - paragraph: "Source: MODIS (NASA), 2021‑2025."
      - listitem:
        - heading "Fire near the plot" [level=3]
        - paragraph: Repeats
        - paragraph: It saw it often.
        - figure:
          - img "3 of 15 years with a fire seen nearby"
        - paragraph: "Burning: repeats. Fires seen nearby in 3 of 15 years."
        - paragraph: "Months with fire: April and May."
        - paragraph: "Source: VIIRS (NASA FIRMS), 2012‑2026."
      - listitem:
        - heading "Long dry spell (canícula)" [level=3]
        - paragraph: Watch
        - paragraph: It saw it a few times.
        - figure:
          - img "2 of 25 years with a long canícula (midsummer dry spell)"
        - paragraph: "Midsummer drought: watch. Dry spells longer than 15 days in 2 of 25 years."
        - paragraph: Between June and August.
        - paragraph: "Source: CHIRPS and IMERG (NASA), 2001‑2025."
  - region "Options to talk over with your technician":
    - heading "Options to talk over with your technician" [level=2]
    - paragraph: "Two options come out even: their scores are 3 points or less apart. None stands out."
    - list:
      - listitem: Legume or cover crop Maize with jack bean (canavalia) in primera, beans in postrera and standing stubble
      - listitem: Drought-tolerant crop Sorghum in primera and cowpea in postrera, with standing stubble
    - paragraph: In no particular order.
    - paragraph: What you do today Maize with beans in primera and beans in postrera
    - heading "How sure we are" [level=3]
    - paragraph: High
    - paragraph: "Why: All three checks pass."
  - paragraph: This is not an official alert; talk to your technician.
  - region "Share this plot":
    - heading "Share this plot" [level=2]
    - paragraph: One black-and-white page to print, the short audio and a WhatsApp message.
    - button "Print sheet"
    - link "Download audio":
      - /url: ./audio/jocotan.frases.en.mp3
    - link "Share on WhatsApp":
      - /url: https://wa.me/?text=Milpa%20Resiliente%2C%20Jocot%C3%A1n%2C%20Chiquimula%0A-%20Bare%20soil%3A%20Repeats%0A-%20Fire%20near%20the%20plot%3A%20Repeats%0A-%20Long%20dry%20spell%20(can%C3%ADcula)%3A%20Watch%0AThis%20is%20not%20an%20official%20alert%3B%20talk%20to%20your%20technician.%0Ahttp%3A%2F%2F127.0.0.1%3A4179%2F
  - button "See the evidence Map, charts, sources and limits"
```

### 1.4 Nombres accesibles (`svg[role="img"] > title`) verificados en las 5 parcelas (ES y EN)

| Parcela | Idioma | Pictograma Suelo (`RuedaMeses`) | Pictograma Quema (`PuntosAnios`) | Pictograma Canícula (`PuntosAnios`) |
|---|---|---|---|---|
| **Jocotán** | ES | `2 de 12 meses con suelo desnudo (marzo y abril). Poca cobertura: febrero y mayo.` | `3 de 15 años con quema vista cerca` | `2 de 25 años con canícula larga` |
| **Jocotán** | EN | `2 of 12 months with bare soil (March and April). Little cover: February and May.` | `3 of 15 years with a fire seen nearby` | `2 of 25 years with a long canícula (midsummer dry spell)` |
| **Camotán** | ES | `0 de 12 meses con suelo desnudo. Poca cobertura: marzo y abril.` | `3 de 15 años con quema vista cerca` | `2 de 25 años con canícula larga` |
| **Camotán** | EN | `0 of 12 months with bare soil. Little cover: March and April.` | `3 of 15 years with a fire seen nearby` | `2 of 25 years with a long canícula (midsummer dry spell)` |
| **Olopa** | ES | `0 de 12 meses con suelo desnudo. Poca cobertura: marzo y abril.` | `1 de 15 años con quema vista cerca` | `0 de 25 años con canícula larga` |
| **Olopa** | EN | `0 of 12 months with bare soil. Little cover: March and April.` | `1 of 15 years with a fire seen nearby` | `0 of 25 years with a long canícula (midsummer dry spell)` |
| **San Juan Ermita** | ES | `3 de 12 meses con suelo desnudo (febrero, marzo y abril). Poca cobertura: enero y mayo.` | `2 de 15 años con quema vista cerca` | `1 de 25 años con canícula larga` |
| **San Juan Ermita** | EN | `3 of 12 months with bare soil (February, March and April). Little cover: January and May.` | `2 of 15 years with a fire seen nearby` | `1 of 25 years with a long canícula (midsummer dry spell)` |
| **Zacapa** | ES | `1 de 12 meses con suelo desnudo (abril). Poca cobertura: enero, febrero, marzo y mayo.` | `0 de 15 años con quema vista cerca` | `3 de 25 años con canícula larga` |
| **Zacapa** | EN | `1 of 12 months with bare soil (April). Little cover: January, February, March and May.` | `0 of 15 years with a fire seen nearby` | `3 of 25 years with a long canícula (midsummer dry spell)` |

---

## 2. Vista de impresión: emulación de `print`, PDF en tamaño Carta y escala de grises, y revisión de cortes

- **Hora real de la corrida:** `2026-11-14T16:39:57-06:00` a `2026-11-14T16:40:04-06:00`
- **Comando usado:** `python "$env:TEMP\milpa-pruebas\correr_parte_b.py"`
- **Carpeta donde quedaron guardados los 15 PDFs generados:** `$env:TEMP\milpa-pruebas\` (fuera del repo)

> **Aviso:** Esta prueba emula `@media print`, aplica escala de grises (`grayscale(100%)`), genera el archivo PDF en tamaño **Carta (`Letter`, 8.5 × 11 in)** y comprueba geométricamente en el DOM que ningún elemento se corte ni pase a una segunda página. **No reemplaza la impresión física en papel ni la fotocopia en blanco y negro que debe hacer Rodolfo** (`rodolfo-impresion.md`).

### 2.1 Resultados de la «Hoja de parcela» (Kit en la vista del agricultor, `.kit-hoja`)

| Archivo PDF generado en `%TEMP%\milpa-pruebas\` | Parcela e idioma | Tamaño del PDF | Páginas en tamaño Carta | Dimensiones de `.kit-hoja` (`ancho × alto`) | Hechos y formas visibles | Elementos cortados o desbordados (`cortados`) |
|---|---|---|---|---|---|---|
| `hoja-parcela-jocotan-es-carta-gris.pdf` | Jocotán (`es`) | 357 051 B (349 KB) | **1 página** | `816 × 610 px` | 3 hechos / 3 formas | `[]` (ninguno) |
| `hoja-parcela-camotan-es-carta-gris.pdf` | Camotán (`es`) | 367 167 B (359 KB) | **1 página** | `816 × 610 px` | 3 hechos / 3 formas | `[]` (ninguno) |
| `hoja-parcela-olopa-es-carta-gris.pdf` | Olopa (`es`) | 363 451 B (355 KB) | **1 página** | `816 × 610 px` | 3 hechos / 3 formas | `[]` (ninguno) |
| `hoja-parcela-san_juan_ermita-es-carta-gris.pdf` | San Juan Ermita (`es`) | 362 982 B (354 KB) | **1 página** | `816 × 610 px` | 3 hechos / 3 formas | `[]` (ninguno) |
| `hoja-parcela-zacapa-es-carta-gris.pdf` | Zacapa (`es`) | 358 945 B (351 KB) | **1 página** | `816 × 610 px` | 3 hechos / 3 formas | `[]` (ninguno) |
| `hoja-parcela-jocotan-en-carta-gris.pdf` | Jocotán (`en`) | 351 131 B (343 KB) | **1 página** | `816 × 610 px` | 3 hechos / 3 formas | `[]` (ninguno) |
| `hoja-parcela-olopa-en-carta-gris.pdf` | Olopa (`en`) | 360 032 B (352 KB) | **1 página** | `816 × 610 px` | 3 hechos / 3 formas | `[]` (ninguno) |
| `hoja-parcela-camotan-en-carta-gris.pdf` | Camotán (`en`) | 361 032 B (353 KB) | **1 página** | `816 × 610 px` | 3 hechos / 3 formas | `[]` (ninguno) |

### 2.2 Resultados de la «Tarjeta del agricultor» en la vista *Evidence* (`.tarjeta`)

| Archivo PDF generado en `%TEMP%\milpa-pruebas\` | Parcela e idioma | Tamaño del PDF | Páginas en tamaño Carta | Dimensiones de `.tarjeta` (`ancho × alto`) | Tabla `.tabla-tarjeta` (`clientWidth / scrollWidth`) | Elementos `.no-imprimir` visibles | URL de ZARC impresa (`.solo-imprimir`) | Elementos cortados (`cortados`) |
|---|---|---|---|---|---|---|---|---|
| `tarjeta-evidence-jocotan-es-carta-gris.pdf` | Jocotán (`es`) | 446 488 B (436 KB) | **1 página** | `816 × 711 px` | `782 px / 782 px` (3 filas) | `0` | `true` | `[]` (ninguno) |
| `tarjeta-evidence-camotan-es-carta-gris.pdf` | Camotán (`es`) | 451 915 B (441 KB) | **1 página** | `816 × 711 px` | `782 px / 782 px` (3 filas) | `0` | `true` | `[]` (ninguno) |
| `tarjeta-evidence-olopa-es-carta-gris.pdf` | Olopa (`es`) | 477 495 B (466 KB) | **1 página** | `816 × 734 px` | `782 px / 782 px` (3 filas) | `0` | `true` | `[]` (ninguno) |
| `tarjeta-evidence-san_juan_ermita-es-carta-gris.pdf` | San Juan Ermita (`es`) | 447 614 B (437 KB) | **1 página** | `816 × 711 px` | `782 px / 782 px` (3 filas) | `0` | `true` | `[]` (ninguno) |
| `tarjeta-evidence-zacapa-es-carta-gris.pdf` | Zacapa (`es`) | 443 157 B (433 KB) | **1 página** | `816 × 711 px` | `782 px / 782 px` (3 filas) | `0` | `true` | `[]` (ninguno) |
| `tarjeta-evidence-jocotan-en-carta-gris.pdf` | Jocotán (`en`) | 443 019 B (433 KB) | **1 página** | `816 × 711 px` | `782 px / 782 px` (3 filas) | `0` | `true` | `[]` (ninguno) |
| `tarjeta-evidence-camotan-en-carta-gris.pdf` | Camotán (`en`) | 446 731 B (436 KB) | **1 página** | `816 × 711 px` | `782 px / 782 px` (3 filas) | `0` | `true` | `[]` (ninguno) |

---

## 3. Verificación automática de los audios (existencia, duración, etiquetas IA y subtítulos)

- **Hora real de la corrida:** `2026-11-14T16:39:56-06:00` a `2026-11-14T16:39:57-06:00` (más `pytest tests/test_audio_frases.py tests/test_audio_ia.py` a las `2026-11-14T16:30:16-06:00`)
- **Comando usado:** `python "$env:TEMP\milpa-pruebas\correr_parte_b.py"` y `python -m pytest -v tests/test_audio_frases.py tests/test_audio_ia.py`

> **Aviso:** Esta comprobación verifica que cada archivo `.mp3` existe en disco, que sus tramas MPEG son válidas, que sus etiquetas ID3 (`TXXX:ai_generated=true`, `TXXX:ai_tool`, `TXXX:text_sha256`) coinciden con el texto del motor y que cada archivo `.vtt` tiene sus 6 frases sincronizadas e idénticas al JSON. **No reemplaza la escucha humana que debe hacer Mario** (`mario-audios.md`) para detectar errores de pronunciación o entonación.

### Tabla de los 15 audios activos en la aplicación (más los 5 `.en.mp3` de tarjeta en disco)

| # | Grupo / Vista | Ruta en el repositorio | ¿Existe? | Tamaño (bytes) | Duración real (`s`) | Bitrate / Frecuencia | Archivo de subtítulo o fuente del texto | ¿Texto y hash ID3 coinciden al 100 %? |
|---|---|---|---|---|---|---|---|---|
| **1** | Vista agricultor (ES) | `web/public/audio/jocotan.frases.mp3` | Sí | 105 162 | **26.0 s** (`25.984 s`) | 32 kbps, 24 kHz, mono | `web/public/audio/jocotan.frases.es.vtt` (6 frases) | Sí |
| **2** | Vista agricultor (ES) | `web/public/audio/camotan.frases.mp3` | Sí | 111 018 | **27.4 s** (`27.435 s`) | 32 kbps, 24 kHz, mono | `web/public/audio/camotan.frases.es.vtt` (6 frases) | Sí |
| **3** | Vista agricultor (ES) | `web/public/audio/olopa.frases.mp3` | Sí | 115 624 | **28.6 s** (`28.597 s`) | 32 kbps, 24 kHz, mono | `web/public/audio/olopa.frases.es.vtt` (6 frases) | Sí |
| **4** | Vista agricultor (ES) | `web/public/audio/san_juan_ermita.frases.mp3` | Sí | 106 992 | **26.4 s** (`26.428 s`) | 32 kbps, 24 kHz, mono | `web/public/audio/san_juan_ermita.frases.es.vtt` (6 frases) | Sí |
| **5** | Vista agricultor (ES) | `web/public/audio/zacapa.frases.mp3` | Sí | 108 713 | **26.9 s** (`26.877 s`) | 32 kbps, 24 kHz, mono | `web/public/audio/zacapa.frases.es.vtt` (6 frases) | Sí |
| **6** | Vista agricultor (EN) | `web/public/audio/jocotan.frases.en.mp3` | Sí | 115 136 | **28.5 s** (`28.482 s`) | 32 kbps, 24 kHz, mono | `web/public/audio/jocotan.frases.en.vtt` (6 frases) | Sí |
| **7** | Vista agricultor (EN) | `web/public/audio/camotan.frases.en.mp3` | Sí | 118 496 | **29.3 s** (`29.317 s`) | 32 kbps, 24 kHz, mono | `web/public/audio/camotan.frases.en.vtt` (6 frases) | Sí |
| **8** | Vista agricultor (EN) | `web/public/audio/olopa.frases.en.mp3` | Sí | 90 630 | **29.8 s** (`29.814 s`) | 24 kbps, 24 kHz, mono | `web/public/audio/olopa.frases.en.vtt` (6 frases) | Sí |
| **9** | Vista agricultor (EN) | `web/public/audio/san_juan_ermita.frases.en.mp3` | Sí | 115 814 | **28.6 s** (`28.641 s`) | 32 kbps, 24 kHz, mono | `web/public/audio/san_juan_ermita.frases.en.vtt` (6 frases) | Sí |
| **10** | Vista agricultor (EN) | `web/public/audio/zacapa.frases.en.mp3` | Sí | 117 247 | **29.0 s** (`29.005 s`) | 32 kbps, 24 kHz, mono | `web/public/audio/zacapa.frases.en.vtt` (6 frases) | Sí |
| **11** | Tarjeta *Evidence* (ES) | `web/public/audio/jocotan.mp3` | Sí | 426 026 | **70.9 s** | 48 kbps, 24 kHz, mono | `texto_tarjeta` impreso en `Tarjeta.jsx` | Sí |
| **12** | Tarjeta *Evidence* (ES) | `web/public/audio/camotan.mp3` | Sí | 409 610 | **68.2 s** | 48 kbps, 24 kHz, mono | `texto_tarjeta` impreso en `Tarjeta.jsx` | Sí |
| **13** | Tarjeta *Evidence* (ES) | `web/public/audio/olopa.mp3` | Sí | 441 432 | **73.5 s** | 48 kbps, 24 kHz, mono | `texto_tarjeta` impreso en `Tarjeta.jsx` | Sí |
| **14** | Tarjeta *Evidence* (ES) | `web/public/audio/san_juan_ermita.mp3` | Sí | 430 786 | **71.7 s** | 48 kbps, 24 kHz, mono | `texto_tarjeta` impreso en `Tarjeta.jsx` | Sí |
| **15** | Tarjeta *Evidence* (ES) | `web/public/audio/zacapa.mp3` | Sí | 403 273 | **67.1 s** | 48 kbps, 24 kHz, mono | `texto_tarjeta` impreso en `Tarjeta.jsx` | Sí |
| *16* | *Extra en disco (EN)* | `web/public/audio/jocotan.en.mp3` | Sí | 556 622 | **92.7 s** | 48 kbps, 24 kHz, mono | `en.texto_tarjeta` (no conectado en `Tarjeta.jsx`) | Sí |
| *17* | *Extra en disco (EN)* | `web/public/audio/camotan.en.mp3` | Sí | 540 782 | **90.0 s** | 48 kbps, 24 kHz, mono | `en.texto_tarjeta` (no conectado en `Tarjeta.jsx`) | Sí |
| *18* | *Extra en disco (EN)* | `web/public/audio/olopa.en.mp3` | Sí | 571 740 | **95.2 s** | 48 kbps, 24 kHz, mono | `en.texto_tarjeta` (no conectado en `Tarjeta.jsx`) | Sí |
| *19* | *Extra en disco (EN)* | `web/public/audio/san_juan_ermita.en.mp3` | Sí | 566 278 | **94.3 s** | 48 kbps, 24 kHz, mono | `en.texto_tarjeta` (no conectado en `Tarjeta.jsx`) | Sí |
| *20* | *Extra en disco (EN)* | `web/public/audio/zacapa.en.mp3` | Sí | 536 893 | **89.4 s** | 48 kbps, 24 kHz, mono | `en.texto_tarjeta` (no conectado en `Tarjeta.jsx`) | Sí |

---

## 4. Comparación automática de las cifras de las tarjetas y vistas contra los JSON de `web/public/data/`

- **Hora real de la corrida:** `2026-11-14T16:39:57-06:00`
- **Comando usado:** `python "$env:TEMP\milpa-pruebas\correr_parte_b.py"` y `npm run smoke` (en `web/`)

> **Aviso:** Esta validación cruza automáticamente las cifras de `agricultor.hechos`, `deteccion`, `clima`, `smap`, `rotaciones`, `texto_tarjeta` y `en.texto_tarjeta` en los 16 archivos JSON de `web/public/data/` y en `validacion.json` usando `motor.contrato.errores_textos()` y `motor.contrato.errores_esquema()`. **No reemplaza la revisión visual en pantalla que debe hacer Mario** (`mario-cifras.md`).

### Resultado del cruce automático
- **5 archivos principales (`jocotan.json`, `camotan.json`, `olopa.json`, `san_juan_ermita.json`, `zacapa.json`):**
  - `coincide_deteccion` (Suelo desnudo y Quemas): **`true` en las 5 parcelas**.
  - `coincide_clima` (Canícula larga): **`true` en las 5 parcelas**.
  - `contrato.errores_textos(res)` (verifica que cada número en los textos en español e inglés exista en el JSON y que no haya fechas de siembra inventadas): **`[]` (0 errores en las 5 parcelas)**.
  - `contrato.errores_esquema(res)`: **`[]` (0 errores en las 5 parcelas)**.
- **10 archivos de variantes (`*.maiz_solo.json` y `*.sorgo.json`):**
  - `contrato.errores_textos(res)`: **`[]` (0 errores en los 10 archivos)**.
  - `contrato.errores_esquema(res)`: **`[]` (0 errores en los 10 archivos)**.
- **`web/public/data/validacion.json`:**
  - Las 5 parcelas en `observacion_2026.lluvia_chirps` tienen entre **20 % y 26 %** de la mediana 1991–2025 en julio–agosto de 2026 (`0` años más secos en los 35 años de referencia).
  - Las 3 celdas con calidad recomendada en `observacion_2026.smap_celdas` tienen `es_el_mas_bajo = true` en los 12 años de SMAP (2015–2026).
  - En `sequia_2018`, las **5 de 5 parcelas** tienen `puesto_2018 = 1` (de 25) y `senales_2018.motor = true` usando solo datos hasta 2017.

---

## 5. Conteo de caracteres y palabras de cada sección de `docs/project-page-en.md`

- **Hora real de la corrida:** `2026-11-14T16:54:51-06:00` (recálculo sobre `main` en el commit `78de49a`; la primera corrida, a las `2026-11-14T16:39:56-06:00`, se hizo sobre un `main` anterior y sus cifras ya no valen)
- **Método:** palabras = `split()` del bloque; caracteres del bloque sin su título `## ...`; «sin saltos de línea» quita los saltos de línea; párrafos = bloques separados por una línea en blanco. El encabezado se cuenta sin el título `# ...`.

> **Aviso:** Este conteo mide exactamente el texto actual en el repositorio (`docs/project-page-en.md`), pero **no reemplaza la revisión que debe hacer Rodolfo Xiloj** (`rodolfo-formulario.md`) dentro del formulario web autenticado de NASA Space Apps para comprobar los límites reales de cada campo y la pestaña **Members**.

| # | Sección en `docs/project-page-en.md` | Nivel | Palabras | Caracteres (con espacios) | Caracteres (sin saltos de línea) | Caracteres (sin espacios) | Párrafos / bloques |
|---|---|---|---|---|---|---|---|
| 0 | *Encabezado y notas previas («Before sending»)* | `H1` | 104 | 635 | 626 | 529 | 4 |
| 1 | **`Project Name`** | `H2` | **2** | **16** | **16** | **15** | 1 |
| 2a | **`High-Level Project Summary`** *(versión principal)* | `H2` | **306** | **1 776** | **1 776** | **1 471** | 1 |
| 2b | **`Short version`** *(respaldo bajo High-Level Summary)* | `H3` | **161** | **973** | **973** | **813** | 1 |
| 3 | **`Link to Project Demo`** | `H2` | **1** | **100** | **100** | **100** | 1 |
| 4 | **`Link to Final Project`** *(marcador `TBD: public site URL`)* | `H2` | **4** | **20** | **20** | **17** | 1 |
| 5 | **`Detailed Project Description`** | `H2` | **1 398** | **8 161** | **8 144** | **6 756** | 9 |
| 6 | **`Use of Super Intelligence (SI)`** | `H2` | **199** | **1 183** | **1 183** | **985** | 1 |
| 7 | **`NASA Data`** | `H2` | **385** | **2 266** | **2 259** | **1 882** | 1 |
| 8 | **`Space Agency Partner Data and Other References`** | `H2` | **130** | **991** | **988** | **862** | 1 |

---

## 6. Hallazgos y observaciones importantes para el equipo

> **Actualización del 14 nov 2026, 17:50 (UTC−6):** los hallazgos 1 y 2 de abajo ya están resueltos en `main` (ver la sección 7). Se dejan como se escribieron, porque describen lo que la corrida de las 16:39 encontró.

1. **Audio de la tarjeta en inglés en *Evidence* (`{parcela}.en.mp3`):**
   - Los 5 archivos `web/public/audio/{parcela}.en.mp3` existen en disco, duran entre 89.4 y 95.2 s y pasan todas las validaciones de etiquetas de IA, pero `web/src/components/Tarjeta.jsx` reproduce actualmente `res.audio.mp3` (español) en ambos idiomas, tal como ya se declara honestamente en `docs/project-page-en.md` (*«The Evidence page still plays the longer card audio in Spanish only (the English card mp3 is generated but not yet played)»*). En la vista del agricultor, en cambio, el botón **«Listen»** sí reproduce los 5 audios cortos en inglés (`{parcela}.frases.en.mp3`) con subtítulos en inglés (`{parcela}.frases.en.vtt`).
2. **Marcas de tiempo de `.frases.en.vtt`:**
   - Los 5 archivos `.frases.en.vtt` reutilizan los intervalos de tiempo de las 6 frases en español (hasta ~26–28.6 s), mientras que los MP3 cortos en inglés duran ~28.5–29.8 s (1.5 a 2.5 s más). Mario debe poner especial atención en la Guía 4 (`mario-audios.md`) a si el cambio entre la frase 5 y la frase 6 en inglés se siente natural al oído.

---

## 7. Actualización tras unir `entrega-impacto-6` (sábado 14 nov 2026)

Las secciones 1 a 6 son corridas de las 16:29 a las 16:54 sobre un `main` anterior. Después entró la rama `entrega-impacto-6`, que cambia tres cosas de este reporte. Las corridas completas con su hora están en `docs/es/pruebas.md`.

1. **Tarjeta en inglés (hallazgo 1): resuelto.** `Tarjeta.jsx` reproduce `audio/{parcela}.en.mp3` cuando la interfaz está en inglés y `audio/{parcela}.mp3` en español. Los audios activos pasan de 15 a **20** (las filas 16 a 20 de la tabla de la sección 3 ya no son «extra en disco»), y la guía de Mario los incluye como Grupo 4. Lo comprueban `web/scripts/evidence_playwright.py` («la tarjeta reproduce el mp3 en inglés / en español») y `npm run sin-red`.
2. **Tiempos de los `.frases.en.vtt` (hallazgo 2): resuelto.** Los subtítulos en inglés ahora usan los tiempos del mp3 en inglés (su último subtítulo termina con el audio, de 28.482 a 29.814 s). La prueba `test_ultimo_subtitulo_termina_con_su_mp3` falla con los archivos anteriores y pasa con los nuevos.
3. **Conteo de `docs/project-page-en.md` (sección 5): cambia una fila.** Se quitó de «Detailed Project Description» la frase que decía que la tarjeta de *Evidence* sonaba solo en español, y se agregó el lema al encabezado (fuera de los campos para pegar). Recuento con el mismo método, hecho a las `2026-11-14T17:47-06:00`:

| # | Sección | Palabras | Caracteres (con espacios) | Caracteres (sin saltos de línea) | Caracteres (sin espacios) | Párrafos / bloques |
|---|---|---|---|---|---|---|
| 0 | *Encabezado y notas previas* | 138 | 824 | 813 | 683 | 5 |
| 5 | **`Detailed Project Description`** | **1 376** | **8 037** | **8 020** | **6 654** | 9 |

Las demás filas de la sección 5 no cambian (`Project Name` 2 / 16, `High-Level Project Summary` 306 / 1 776, `Short version` 161 / 973, `Use of Super Intelligence (SI)` 199 / 1 183, `NASA Data` 385 / 2 266, `Space Agency Partner Data and Other References` 130 / 991).

Dos precisiones más sobre las secciones 0 a 2, para que nadie las tome como el estado actual:

4. **El sitio no tiene Service Worker.** Las filas 0a («`dist/` listo con `sw.js`») y 0f («Service Worker con red bloqueada») lo mencionan por error: `web/dist/` no trae ningún `sw.js`. `npm run sin-red` abre un navegador con un proxy inexistente, de modo que solo responde el servidor local, y comprueba que todo lo que el sitio pide (datos, audio, capas del mapa) es local. Sin internet funciona mientras alguien lo sirva en la red local; no «queda guardado» en el teléfono.
5. **El árbol de accesibilidad de las secciones 1.2 y 1.3 es de un árbol de trabajo anterior.** Trae «What the satellite saw on this plot», «Options to talk over with your technician» y «This is not an official alert; talk to your technician», y no trae la línea de julio y agosto de 2026. El sitio actual dice «What the satellite saw around this plot», «Options to talk over with your extension worker» y «This is not an official notice: talk it over with your extension worker». Los textos vigentes, en el orden de lectura, están en `rodolfo-talkback.md` y en `ivan-ingles.md`, que se corrigieron contra el sitio construido el 14 nov 2026 (`web/scripts/agricultor_playwright.py`: 96 de 96).

