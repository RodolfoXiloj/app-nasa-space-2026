# Guía 7 para Iván: Guion para leer el inglés en voz alta y marcar trabas o errores

**Responsable:** Iván  
**Archivos revisados en este guion:**  
1. **Vista del agricultor en inglés** (`web/src/agricultor/textos.js`, `web/src/kit/textos.js`, `web/src/pictos/textos.js` y `motor/ingles.py`)  
2. **Resumen y página del proyecto en inglés** (`docs/project-page-en.md`)  
3. **Las 7 diapositivas (slides) en inglés** (`docs/slides/index.html`)  
**Tiempo estimado:** 25 a 35 minutos  

> **Por qué hace falta una persona:** Un corrector ortográfico no detecta si una oración en inglés es tan larga que te quedas sin aire al leerla, si una estructura suena calcada del español, o si una sigla o término agronómico (*canícula*, *primera*, *postrera*, *jack bean*, *standing stubble*, *ZARC*) resulta brusco para un jurado internacional de NASA Space Apps. Leer cada bloque **en voz alta** hace saltar de inmediato cualquier frase pesada o confusa.

---

## Qué debes marcar mientras lees en voz alta

Usa estas **4 marcas simples** en la tabla del final cada vez que notes algo al leer:
- **`[AIRE]` — Falta de aire:** la oración es demasiado larga y convendría partirla con un punto o punto y coma.
- **`[TRABA]` — Traba de lengua:** combinación de palabras difícil de pronunciar de corrido en voz alta.
- **`[RARO]` — Suena raro o calcado del español:** expresión que en inglés natural se diría de otra forma.
- **`[DATO]` — Duda de cifra o nombre:** un número, mes o nombre propio que parezca inconsistente con el resto.

---

## Parte 1. Textos en inglés de la vista del agricultor (primera pantalla)

Lee en voz alta estos textos tal como aparecen al abrir la aplicación web (`http://localhost:4173/`, que abre en inglés por defecto):

### 1.1 Encabezado, selector de parcela y reproductor de audio (`web/src/agricultor/textos.js`)
> **Milpa Resiliente**  
> **Plot:** Jocotán, Chiquimula — *Example plot in Jocotán.*  
> **Button:** Listen — *Short audio with subtitles.* (When playing: *Pause* / *Play from start*)  
> **Subtitles button:** Subtitles  
> **AI voice note:** AI-generated synthetic voice (edge-tts, Microsoft neural text to speech; voice en-US-JennyNeural) from the text the engine wrote with templates. It is not a person.

### 1.2 Los 3 hechos del semáforo en la vista del agricultor (`textos.js` + `pictos/textos.js` + `motor/ingles.py`)
> **Section heading:** What the satellite saw on this plot  
> **Intro:** Three facts from past years, always in the same order. They are records, not a forecast.  
>
> **States (shape + word + explanation):**  
> - **Good:** The satellite did not see the problem in this period.  
> - **Watch:** It saw it a few times.  
> - **Repeats:** It saw it often.  
> - **The satellite can't see well here:** We don't have enough data for this plot.  
>
> **Fact 1 — Bare soil (Jocotán example):**  
> - Heading: **Bare soil** — **Repeats** (*It saw it often.*)  
> - Wheel alt text: *2 of 12 months with bare soil (March and April). Little cover: February and May.*  
> - Wheel legend: *Bare soil · Little cover · Covered*  
> - Count & details: *Soil: repeats. The satellite saw 2 months of bare soil.* / *Bare: March and April.* / *Little plant cover: February and May.*  
> - Source: *Source: MODIS (NASA), 2021‑2025.*  
> - *(Variantes en las otras parcelas: Camotán/Olopa: «Soil: watch. The satellite saw 2 months with little cover, none bare.» · San Juan Ermita: «Soil: repeats. The satellite saw 3 months of bare soil.» · Zacapa: «Soil: watch. The satellite saw 1 month of bare soil and 4 with little cover.»)*  
>
> **Fact 2 — Fire near the plot (Jocotán example):**  
> - Heading: **Fire near the plot** — **Repeats** (*It saw it often.*)  
> - Grid alt text: *3 of 15 years with a fire seen nearby*  
> - Count & details: *Burning: repeats. Fires seen nearby in 3 of 15 years.* / *Months with fire: April and May.*  
> - Source: *Source: VIIRS (NASA FIRMS), 2012‑2026.*  
> - *(Variante en Zacapa: «Burning: good. No fires seen nearby in 15 years.»)*  
>
> **Fact 3 — Long dry spell (canícula) (Jocotán example):**  
> - Heading: **Long dry spell (canícula)** — **Watch** (*It saw it a few times.*)  
> - Grid alt text: *2 of 25 years with a long canícula (midsummer dry spell)*  
> - Count & details: *Midsummer drought: watch. Dry spells longer than 15 days in 2 of 25 years.* / *Between June and August.*  
> - Source: *Source: CHIRPS and IMERG (NASA), 2001‑2025.*  
> - *(Variante en Olopa: «Midsummer drought: good. No dry spell went past 15 days in 25 years.»)*

### 1.3 Opciones para platicar con su técnico, confianza y Kit de compartir (`textos.js` + `kit/textos.js`)
> **Section heading:** Options to talk over with your technician  
> - **When 2 options tie (Jocotán, San Juan Ermita):** *Two options come out even: their scores are 3 points or less apart. None stands out.*  
> - **When all 3 options tie (Olopa):** *All three options come out even: their scores are 3 points or less apart. None stands out.*  
> - **When confidence is low (Camotán, Zacapa):** *We cannot recommend one option over another: confidence in the data for this plot is low. Check the three options below with your technician.*  
> - **Option labels & names:**  
>   - *What you do today:* Maize with beans in primera and beans in postrera  
>   - *Legume or cover crop:* Maize with jack bean (canavalia) in primera, beans in postrera and standing stubble  
>   - *Drought-tolerant crop:* Sorghum in primera and cowpea in postrera, with standing stubble *(or in Olopa: Short-cycle maize ICTA B-5 with beans in primera and beans in postrera)*  
>   - *In no particular order.*  
> - **How sure we are:**  
>   - *High* — *Why: All three checks pass.* (Jocotán, San Juan Ermita)  
>   - *Medium* — *Why: Two rain sources (POWER and CHIRPS) differ by 22% in July-August.* (Olopa)  
>   - *Low* — *Why: SMAP has no soil-moisture data of recommended quality for this cell; slope is 37% (erosion risk on bare soil).* (Camotán)  
>   - *Low* — *Why: Two rain sources (POWER and CHIRPS) differ by 55% in July-August; slope is 35.3% (erosion risk on bare soil).* (Zacapa)  
> - **Disclaimer:** *This is not an official alert; talk to your technician.*  
> - **Share this plot:** *One black-and-white page to print, the short audio and a WhatsApp message.* → Buttons: *Print sheet* · *Download audio* · *Share on WhatsApp*  
> - **Bottom button:** *See the evidence — Map, charts, sources and limits*

---

## Parte 2. Textos del resumen y descripción del proyecto (`docs/project-page-en.md`)

Lee en voz alta cada sección del formulario de Space Apps:

### 2.1 High-Level Project Summary (versión principal — 253 palabras)
> Milpa Resiliente turns two decades of satellite records into a three-fact traffic light designed for a smallholder farmer in Guatemala's Dry Corridor to read in seconds (the comprehension test with farmers is still pending): how many months a year the land around the plot shows bare soil or little plant cover (NASA MODIS NDVI, 250 m), how many years a satellite detected fire near the plot (NASA FIRMS VIIRS, 375 m; small or short fires can be missed), and how many years the mid-summer dry spell, the *canícula*, ran long (CHIRPS v3 daily rain, split into days with NASA GPM IMERG). Each fact has a shape, a word, a pictogram and a short audio in Spanish or English, so it does not depend on colour or on reading well. One tap away, an Evidence view lets the extension worker compare three crop rotations per plot under drier and hotter scenarios, with sources, validation and limits in plain sight. It matters because drought keeps taking these families' maize and beans: for July-September 2026 Guatemala's food security agency forecast 3.2 million people (17 %) in crisis or worse (IPC Phase 3+), with Chiquimula and Zacapa at 15-19 %; FEWS NET reported 2026 crop losses for subsistence farmers, in some cases total; and in 2019 Oxfam measured average maize losses of 78.1 % in 201 monitored communities, 23 of them in our four Chiquimula municipalities. The tool does not decide for anyone: it gives the farmer and the extension worker the same evidence to decide together.

### 2.2 High-Level Project Summary — Short version (respaldo — 149 palabras)
> Milpa Resiliente turns two decades of satellite records into a three-fact traffic light for smallholder farmers in Guatemala's Dry Corridor: months with bare soil or little cover around the plot (NASA MODIS NDVI), years with fire detected nearby (NASA FIRMS VIIRS) and years with a long mid-summer dry spell, the *canícula* (CHIRPS v3 with NASA GPM IMERG). Each fact has a shape, a word, a pictogram and a short audio in Spanish or English. One tap away, an Evidence view lets the extension worker compare three crop rotations per plot, with sources, validation and limits. It matters: for July-September 2026, 3.2 million Guatemalans (17 %) were forecast in food crisis or worse, and FEWS NET reported maize losses, in some cases total, in the Dry Corridor. The tool does not decide: it gives the farmer and the extension worker the same evidence. Comprehension tests with farmers are still pending.

### 2.3 Detailed Project Description (1 119 palabras)
Lee también en voz alta los 7 párrafos de `docs/project-page-en.md` (líneas 35 a 50):
1. **What it does** (*Farmer view* y *Evidence view*)
2. **How it works** (pipeline en Python, balance hídrico FAO-56, validador determinista y fechas de siembra de ZARC citadas, nunca calculadas)
3. **Local roots** (sistema agroforestal *Kuxur Rum*, territorio maya Ch'orti', 112 432 hablantes y por qué no se tradujo ni sintetizó Ch'orti' con máquina sin hablantes nativos)
4. **How we checked it** (regla fijada antes de ver 2018, 5 de 5 parcelas marcadas en 2018 con datos hasta 2017, 175 126 ha de pérdidas según MAGA/FAO GIEWS, conteo de aciertos y fallos en 20 años, sesgo de NASA POWER frente a CHIRPS y observación preliminar de julio–agosto de 2026 con 20 % a 26 % de la mediana 1991–2025)
5. **Benefits**
6. **Limits we state openly** (escala de 0.35 ha frente a 6.25 ha de MODIS y 9 km de SMAP, falta de SMAP recomendado en Camotán, fin de datos nuevos de Suomi NPP a inicios de noviembre de 2026 y retiro de Terra hacia VIIRS en NOAA-20/21)
7. **Tools**, más los bloques **Use of Super Intelligence (SI)**, **NASA Data** y **Space Agency Partner Data and Other References**.

---

## Parte 3. Textos de las 7 diapositivas (`docs/slides/index.html`)

Lee en voz alta cada una de las 7 láminas como si las estuvieras presentando ante el jurado:

### Slide 1 — Cover
> **Challenge:** Field Shift: Adapting Farms with NASA Data · NASA Space Apps 2026  
> **Title:** Milpa Resiliente  
> **Subtitle:** Satellite records turned into a three-fact traffic light for smallholder farmers and extension workers in Guatemala's Dry Corridor.  
> **Footer:** Team **A dream** · Chiquimula and Zacapa, Guatemala · English and Spanish · Works offline after the first visit

### Slide 2 — 1 · The problem in the Dry Corridor
> **Heading:** Drought keeps hitting subsistence maize and beans  
> - **3.2 M people in Guatemala (17 %)** forecast in food crisis or worse (IPC Phase 3+) for July–September 2026; Chiquimula and Zacapa are at 15–19 % (SESAN IPC analysis, May 2026).  
> - **78.1 % average maize loss** measured by Oxfam in August 2019 across 201 communities in the Dry Corridor, including 23 in Jocotán, Camotán, Olopa and San Juan Ermita.  
> - **20–26 % of median Jul–Aug rain** fell in 2026 across our five plots' CHIRPS v3 cells: the driest July–August in all 36 years (1991–2026). FEWS NET reported crop losses, in some cases total.  
> - **Why satellite tables do not reach the plot:** Smallholder families farm about **0.35 ha** (~half a *manzana*). Adult literacy is **52.9 %** in Jocotán and **59.4 %** in Camotán, and **112,432 people** speak Ch'orti' Maya. Charts in English, red-green maps and web apps that need mobile data leave the farmer out of the conversation with the extension worker.

### Slide 3 — 2 · What the farmer sees first
> **Heading:** Three satellite facts, a shape, a word and a voice  
> **Mockup (Jocotán, Chiquimula — Listen · 26 s · subtitles on):**  
> 1. `[!] Square` **Bare soil — Repeats:** 2 of 12 months bare (March and April). MODIS NDVI, 250 m, 2021–2025.  
> 2. `[!] Square` **Fire near the plot — Repeats:** 3 of 15 years with fire within 500 m. FIRMS VIIRS, 375 m, 2012–2026.  
> 3. `[!] Triangle` **Long canícula — Watch:** 2 of 25 years with a dry spell over 15 days. CHIRPS v3 + GPM IMERG, 2001–2025.  
> **Options to talk over with your technician:** Two options come out even (within 3 points): **Maize + canavalia** (88) and **Sorghum + cowpea** (87), vs. current milpa (80). Confidence: **High**.  
> **Design rules:**  
> - **No colour-only encoding:** green circle “Good”, yellow triangle “Watch”, red square “Repeats”, gray when a sensor cannot see well. No orange and no word “alert”, so it is never confused with CONRED's official alerts.  
> - **Pictograms + short audio:** a 12-month wheel for bare soil, one dot per year for fires and dry spells, and a 21–29 s synthetic-voice audio with WebVTT subtitles in Spanish and English.  
> - **Kit without internet:** prints on one black-and-white letter page, downloads the mp3 and shares a plain-text summary on WhatsApp. Works offline via a service worker.

### Slide 4 — 3 · Local roots and the Evidence view
> **Heading:** Kuxur Rum, Ch'orti' territory and the extension worker's view  
> - **Rooted in Chiquimula:** The cover-crop and no-burn option follows **Kuxur Rum** (“my humid land” in Ch'orti'), an agroforestry system promoted by FAO and MAGA in Jocotán, Camotán and Olopa since 2000: permanent soil cover, no burning and more moisture through the *canícula*. Over 7,000 farms had adopted it by 2006.  
> - **Respect for Ch'orti':** The data contract reserves the `chorti` audio slot and `docs/chorti.md` holds the 6-phrase script for native speakers to translate and record. We did not machine-translate or synthesise Ch'orti'.  
> - **Planting dates are quoted, never calculated:** The tool points to **ZARC (FAO–MAGA)** for municipal planting windows and quotes the published 2026 adjustment (May → June in Chiquimula and Zacapa).  
> - **One tap away: Evidence view:**  
>   - Map with offline NASA GIBS MODIS true-colour tiles and online Sentinel-2.  
>   - Three rotations scored on water, soil and pests under 0, −10, −20 and −30 % rain and +1.5 °C.  
>   - “NASA product → decision” table and a “Where it fails” panel.  
>   - Deterministic text templates checked by a validator: no invented numbers.

### Slide 5 — 4 · NASA data → agricultural decision
> **Heading:** Six NASA products, each tied to a concrete check  
> *(Lee las 6 filas de la tabla: MODIS MOD13Q1 NDVI v061, FIRMS VIIRS S-NPP, GPM IMERG Late V07 via CHIRPS v3 daily “sat”, NASA POWER, SMAP SPL3SMP_E v6 y SRTM GL3 90 m + NASA GIBS).*

### Slide 6 — 5 · Validation and honest limits
> **Heading:** Checked against 2018 and 20 years of records — misses included  
> - **5 / 5 plots flagged in 2018 using only data up to 2017:** With thresholds fixed beforehand on 2001–2017 water deficit (CHIRPS rain + POWER ETo; SMAP is not part of this run), the rule flags 2018 at all five plots. In August 2018 MAGA estimated **175,126 ha** of crop losses in Guatemala (relayed by FAO GIEWS).  
> - **20 test years (2006–2025): hits and misses:** One year and five points are a sanity check, not a skill score. Across 2006–2025 the rule flags 5 or 6 years per plot:  
>   - Against the 4 dry years listed beforehand (2014, 2015, 2018, 2019): **3 hits, 2–3 false alarms, 1 miss (2019)**.  
>   - Against 7 years with documented crop losses (2009, 2010, 2015, 2016, 2018, 2019, 2023): **3–4 hits**; misses **2016, 2019 and 2023** at every plot.  
> - **Limits we state in the app:**  
>   - **Scale:** a plot is ~0.35 ha; MODIS is 6.25 ha and SMAP is 9 km. The tool describes the surrounding land, not the plot.  
>   - **Pending field checks:** plots were chosen from imagery; agronomic review, a real photocopy test and user comprehension tests are still pending.  
>   - **Sensor transition:** S-NPP stopped delivering new data in early Nov 2026 and Terra is retiring; updates move to VIIRS on NOAA-20/21.

### Slide 7 — 6 · Summary
> **Heading:** Same satellite evidence for the farmer and the extension worker  
> 1. **Built for the first screen:** Three facts, shapes + words, pictograms and a 26 s audio with subtitles. No login, no keys, works offline after the first load.  
> 2. **Transparent by construction:** Plain Python rules + FAO-56 water balance. Every sentence comes from a template and a validator rejects any number not in the JSON.  
> 3. **Ready to inspect:** Live web app, 5 real plots in Chiquimula and Zacapa, full source code, tests and data provenance in the repository.  
> **Footer:** Milpa Resiliente · Team **A dream** (Rodolfo Xiloj, Mario, Iván) · `github.com/RodolfoXiloj/challenge-space-apps-2026`

---

## Tabla para anotar el resultado y la hora real

| Fecha y hora real (ej. `2026-11-15 15:00`) | Sección leída en voz alta | Tiempo aproximado que tomó leerla | ¿Se leyó fluido de principio a fin? (Sí / No) | Frases marcadas con `[AIRE]`, `[TRABA]`, `[RARO]` o `[DATO]` y cambio sugerido |
|---|---|---|---|---|
| | **1.1 Vista agricultor — Encabezado, controles y aviso de voz IA** | | | |
| | **1.2 Vista agricultor — Los 3 hechos y estados del semáforo (5 parcelas)** | | | |
| | **1.3 Vista agricultor — Opciones, confianza y Kit de compartir** | | | |
| | **2.1 `project-page-en.md` — High-Level Project Summary (253 palabras)** | | | |
| | **2.2 `project-page-en.md` — Short version (149 palabras)** | | | |
| | **2.3 `project-page-en.md` — Detailed Project Description, SI y NASA Data** | | | |
| | **3.1 `docs/slides/index.html` — Slides 1, 2 y 3 (Portada, Problema y Vista agricultor)** | | | |
| | **3.2 `docs/slides/index.html` — Slides 4 y 5 (Raíces locales, Evidence y Tabla NASA)** | | | |
| | **3.3 `docs/slides/index.html` — Slides 6 y 7 (Validación, Límites y Cierre)** | | | |
