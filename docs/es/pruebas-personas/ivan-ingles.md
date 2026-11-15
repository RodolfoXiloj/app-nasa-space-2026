# Guía 7 para Iván: Guion para leer el inglés en voz alta y marcar trabas o errores

**Responsable:** Iván  
**Archivos revisados en este guion:**  
1. **Vista del agricultor en inglés** (`web/src/agricultor/textos.js`, `web/src/agricultor/EsteAnio.jsx`, `web/src/agricultor/Futuro.jsx`, `web/src/kit/textos.js`, `web/src/pictos/textos.js`, `motor/frases.py` y `motor/ingles.py`)  
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

Lee en voz alta la pantalla tal como abre (`http://localhost:4173/`, en inglés por defecto). Este es el texto real de la parcela **Jocotán**, en el orden en que aparece, sacado del sitio construido el 14 nov 2026 y puesto al día el 15 nov 2026 con los textos del código y del JSON (palabras del semáforo, frases claras, las tarjetas «This year» y «The future» y los botones nuevos de «Share this plot»):

### 1.1 Jocotán, de arriba abajo
> **Milpa Resiliente**  
> *(Language)*  
> *(button)* English  
> *(button)* Español  
> Plot  
> *(plot)* Jocotán, Chiquimula  
> Example plot in Jocotán  
> July and August 2026  
> Rain was 24 % of normal (median 1991-2025), according to CHIRPS. Preliminary.  
> Observed, not a forecast.  
> *(button)* Listen — Short audio with subtitles  
> **What the satellite saw around this plot**  
> Three facts from past years, always in the same order. They are records, not a forecast.  
> **Bare soil**  
> Happens often  
> It saw it several times.  
> *(drawing, read by screen readers:)* 2 of 12 months with bare soil (March and April). Little cover: February and May.  
> Bare soil  
> Little cover  
> Covered  
> In March and April, your land is usually left with no plants covering it. The satellite saw it from 2021 to 2025.  
> Bare: March and April.  
> Little plant cover: February and May.  
> Source: MODIS (NASA), 2021‑2025.  
> **Fire near the plot**  
> Happens often  
> It saw it several times.  
> *(drawing, read by screen readers:)* 3 of 15 years with a fire seen nearby  
> In 3 of the last 15 years there were fires within half a kilometer of your plot, in April and May.  
> Months with fire: April and May.  
> Source: VIIRS (NASA FIRMS), 2012‑2026.  
> **Long dry spell (canícula)**  
> Watch out  
> It saw it a few times.  
> *(drawing, read by screen readers:)* 2 of 25 years with a long canícula (midsummer dry spell)  
> In 2 of the last 25 years, the midsummer drought brought more than 15 days in a row with almost no rain.  
> Between June and August.  
> Source: CHIRPS and IMERG (NASA), 2001‑2025.  
> **This year**  
> This year, July and August got only a quarter of the normal rain (24 %). That is less than in 2018, the driest year since 1991. It is a preliminary figure.  
> *(drawing, read by screen readers:)* July and August rain: a normal year, 324 millimeters; 2018, the driest year, 138 millimeters; 2026, 79 millimeters.  
> A normal year — 324 mm  
> 2018, the driest year — 138 mm  
> 2026 — 79 mm  
> July and August rain at your plot, according to CHIRPS (satellite and stations). Normal is the 1991-2025 median.  
> **Options to talk over with your extension worker**  
> Two options come out even: their scores are 3 points or less apart. None stands out.  
> Legume or cover crop  
> Maize with jack bean (canavalia) in primera, beans in postrera and standing stubble  
> Drought-tolerant crop  
> Sorghum in primera and cowpea in postrera, with standing stubble  
> In no particular order.  
> What you do today  
> Maize with beans in primera and beans in postrera  
> **How sure we are**  
> High  
> Why:  
> All three checks pass.  
> **The future: 2041 to 2060**  
> NASA computes 33 possible climates for 2041 to 2060. Planting as today, maize with beans has enough water in 3 of 33. Maize with jack bean: in 3. Sorghum with cowpea: in all 33.  
> As today: maize with beans **3 of 33**  
> *(drawing, read by screen readers:)* As today: maize with beans: 3 of 33 climates: enough water  
> Maize with jack bean **3 of 33**  
> *(drawing, read by screen readers:)* Maize with jack bean: 3 of 33 climates: enough water  
> Sorghum with cowpea **33 of 33**  
> *(drawing, read by screen readers:)* Sorghum with cowpea: 33 of 33 climates: enough water  
> Each plant is one possible climate, from a NASA model (NEX-GDDP-CMIP6, intermediate emissions). Green: enough water, at least as today. Dry: not enough.  
> This is not an official notice: talk it over with your extension worker.  
> **Share this plot**  
> One black-and-white page to print, the short audio and a WhatsApp message.  
> *(button)* Print sheet  
> *(link)* Download audio  
> *(link)* Share on WhatsApp  
> *(button)* Image for WhatsApp  
> *(button, only on localhost or https)* Save to use without signal  
> Keeps this plot, its short audio and its subtitles on this phone, so the page opens without signal.  
> *(button)* See the evidence — Map, charts, sources and limits  
> Made with AI help: an AI assistant helped write the code, the texts and the pictograms, and the team checked them. The audio is a synthetic AI voice. The facts come from the engine’s fixed rules, not from a language model.  

### 1.2 Lo que cambia en las otras parcelas

Cambia el selector **Plot** y lee también estas partes, que son distintas en cada parcela. Las frases numeradas (8; 7 en Camotán y Zacapa) son las que dice la voz al tocar **Listen**; las de los tres hechos, la de «This year» y la de «The future» también salen escritas en su tarjeta:

**Camotán**

> July and August 2026. Rain was 26 % of normal (median 1991-2025), according to CHIRPS. Preliminary. Observed, not a forecast.  
> 1. Camotán plot. A computer voice is reading this.  
> 2. In March and April, your land usually has little plant cover. The satellite saw it from 2021 to 2025.  
> 3. In 3 of the last 15 years there were fires within half a kilometer of your plot, in March and April.  
> 4. In 2 of the last 25 years, the midsummer drought brought more than 15 days in a row with almost no rain.  
> 5. This year, July and August got only a quarter of the normal rain (26 %). That is less than in 2018, the driest year since 1991. It is a preliminary figure.  
> 6. We can't say which option is best: SMAP soil moisture is missing.  
> 7. This is not an official notice: talk it over with your extension worker.  
> This year  
> A normal year — 355 mm  
> 2018, the driest year — 154 mm  
> 2026 — 94 mm  
> Options to talk over with your extension worker  
> We do not compare the options here because confidence is low.  
> Reason:  
> The 9 km SMAP cell has no recommended-quality data in the whole record (3007 measurements discarded by the quality flag).  
> Legume or cover crop  
> Maize with jack bean (canavalia) in primera, beans in postrera and standing stubble  
> Drought-tolerant crop  
> Sorghum in primera and cowpea in postrera, with standing stubble  
> In no particular order.  
> What you do today  
> Maize with beans in primera and beans in postrera  
> How sure we are  
> Low  
> Why:  
> The 9 km SMAP cell has no recommended-quality data in the whole record (3007 measurements discarded by the quality flag).  
> *(Aquí no sale la tarjeta «The future»: con confianza baja no se comparan las opciones.)*

**Olopa**

> July and August 2026. Rain was 22 % of normal (median 1991-2025), according to CHIRPS. Preliminary. Observed, not a forecast.  
> 1. Olopa plot. A computer voice is reading this.  
> 2. In March and April, your land usually has little plant cover. The satellite saw it from 2021 to 2025.  
> 3. In 1 of the last 15 years there were fires within half a kilometer of your plot, in April.  
> 4. In the last 25 years, the midsummer drought never brought more than 15 days in a row with almost no rain.  
> 5. This year, July and August got only a fifth of the normal rain (22 %). That is less than in 1997, the driest year since 1991. It is a preliminary figure.  
> 6. Today, all three options come out even: what you plant today, maize with jack bean and short-cycle maize.  
> 7. NASA computes 33 possible climates for 2041 to 2060. Planting as today, maize with beans has enough water in 9 of 33. Maize with jack bean: in 9. Short-cycle maize: in all 33.  
> 8. This is not an official notice: talk it over with your extension worker.  
> This year  
> A normal year — 475 mm  
> 1997, the driest year — 211 mm  
> 2026 — 106 mm  
> Options to talk over with your extension worker  
> Three options come out even: each is within 3 points of another, so none stands out.  
> What you do today  
> Maize with beans in primera and beans in postrera  
> Legume or cover crop  
> Maize with jack bean (canavalia) in primera, beans in postrera and standing stubble  
> Drought-tolerant crop  
> Short-cycle maize ICTA B-5 with beans in primera and beans in postrera  
> In no particular order.  
> How sure we are  
> Medium  
> Why:  
> POWER differs 22.1 % from CHIRPS (less than 15 % required).  
> The future: 2041 to 2060  
> As today: maize with beans 9 of 33  
> Maize with jack bean 9 of 33  
> Short-cycle maize 33 of 33  

**San Juan Ermita**

> July and August 2026. Rain was 20 % of normal (median 1991-2025), according to CHIRPS. Preliminary. Observed, not a forecast.  
> 1. San Juan Ermita plot. A computer voice is reading this.  
> 2. In February, March and April, your land is usually left with no plants covering it. The satellite saw it from 2021 to 2025.  
> 3. In 2 of the last 15 years there were fires within half a kilometer of your plot, in March and April.  
> 4. In 1 of the last 25 years, the midsummer drought brought more than 15 days in a row with almost no rain.  
> 5. This year, July and August got only a fifth of the normal rain (20 %). That is less than in 2018, the driest year since 1991. It is a preliminary figure.  
> 6. Today there are two even options: maize with jack bean or sorghum with cowpea.  
> 7. NASA computes 33 possible climates for 2041 to 2060. Planting as today, maize with beans has enough water in 5 of 33. Maize with jack bean: in 5. Sorghum with cowpea: in all 33.  
> 8. This is not an official notice: talk it over with your extension worker.  
> This year  
> A normal year — 345 mm  
> 2018, the driest year — 140 mm  
> 2026 — 69 mm  
> Options to talk over with your extension worker  
> Two options come out even: their scores are 3 points or less apart. None stands out.  
> Legume or cover crop  
> Maize with jack bean (canavalia) in primera, beans in postrera and standing stubble  
> Drought-tolerant crop  
> Sorghum in primera and cowpea in postrera, with standing stubble  
> In no particular order.  
> What you do today  
> Maize with beans in primera and beans in postrera  
> How sure we are  
> High  
> Why:  
> All three checks pass.  
> The future: 2041 to 2060  
> As today: maize with beans 5 of 33  
> Maize with jack bean 5 of 33  
> Sorghum with cowpea 33 of 33  

**Zacapa**

> July and August 2026. Rain was 21 % of normal (median 1991-2025), according to CHIRPS. Preliminary. Observed, not a forecast.  
> 1. Zacapa plot. A computer voice is reading this.  
> 2. In April, your land is usually left with no plants covering it; in January, February, March and May, with little cover. The satellite saw it from 2021 to 2025.  
> 3. In the last 15 years, the satellite saw no fires within half a kilometer of your plot.  
> 4. In 3 of the last 25 years, the midsummer drought brought more than 15 days in a row with almost no rain.  
> 5. This year, July and August got only a fifth of the normal rain (21 %). That is less than in 2018, the driest year since 1991. It is a preliminary figure.  
> 6. We can't say which option is best: two rain sources disagree.  
> 7. This is not an official notice: talk it over with your extension worker.  
> This year  
> A normal year — 206 mm  
> 2018, the driest year — 90 mm  
> 2026 — 44 mm  
> Options to talk over with your extension worker  
> We do not compare the options here because confidence is low.  
> Reason:  
> POWER differs 55.4 % from CHIRPS (less than 15 % required).  
> Legume or cover crop  
> Maize with jack bean (canavalia) in primera, beans in postrera and standing stubble  
> Drought-tolerant crop  
> Sorghum in primera and cowpea in postrera, with standing stubble  
> In no particular order.  
> What you do today  
> Maize with beans in primera and beans in postrera  
> How sure we are  
> Low  
> Why:  
> POWER differs 55.4 % from CHIRPS (less than 15 % required).  
> *(Aquí no sale la tarjeta «The future»: con confianza baja no se comparan las opciones.)*

### 1.3 Evidence en inglés (opcional, si queda tiempo)

Toca **See the evidence** y lee en voz alta, de la parcela Jocotán: el encabezado, el recuadro «Preliminary observation: July–August 2026», una de las tres rotaciones completa (por qué, evidencia, beneficios, vacíos y riesgos) y el panel «Where it fails» de la pestaña Validation.

---

## Parte 2. Textos del resumen y descripción del proyecto (`docs/project-page-en.md`)

Lee en voz alta cada sección **directamente del archivo** `docs/project-page-en.md` (así lees el texto vigente y no una copia). Tamaños al 15 nov 2026:

- **2.1 High-Level Project Summary** (versión principal): 306 palabras, un solo párrafo. Es el más largo de leer de corrido: marca dónde te quedas sin aire.
- **2.2 Short version** (respaldo): 161 palabras.
- **2.3 Detailed Project Description**: 1456 palabras, en 8 bloques que empiezan en negrita: *What it does*, *How it works*, *Local roots*, *How we test the rotations against the future*, *How we checked it*, *Benefits*, *Limits we state openly*, *Tools*.
- **2.4 Use of Super Intelligence (SI)** (199 palabras), **NASA Data** (385) y **Space Agency Partner Data and Other References** (130).

---

## Parte 3. Textos de las 7 diapositivas (`docs/slides/index.html`)

Lee en voz alta cada lámina como si la presentaras ante el jurado. Puedes leerlas del PDF (`docs/slides/milpa-resiliente.pdf`) o de aquí: este es el texto real de cada una, sacado de `index.html` el 14 nov 2026 (las láminas 3 y 7 cambiaron el 15 nov y ya van al día). Las diapositivas 3, 4 y 7 llevan además capturas de la pantalla, que no se leen.

### Slide 1 — Milpa Resiliente
> NASA satellite records turned into three facts a farmer can see and hear, for the milpa in Guatemala’s Dry Corridor.  
> Challenge: Field ShiftNASA Space Apps Challenge 2026  
> Team “A dream”  
> Rodolfo Xiloj · Mario · Iván  

### Slide 2 — Chiquimula: the same three hits
> Canícula  
> 2 — of 25 years  
> Midsummer dry spell longer than 15 days in Jocotán.  
> Burning  
> 3 — of 15 years  
> Fire detected within 500 m of the Jocotán plot, Jan–May.  
> Bare soil  
> 3 — of 12 months  
> Bare soil around the plot in Feb–Apr at San Juan Ermita, before the rains.  
> 2026: 3.2 million people (17 %) forecast in food crisis or worse in Guatemala for Jul–Sep; Chiquimula and Zacapa at 15–19 % (SESAN, IPC forecast).  
> 2019: average maize losses of 78.1 % in 201 communities monitored by Oxfam, 23 of them in Jocotán, Camotán, San Juan Ermita and Olopa.  
> 2018: 175,126 ha of crop losses in Guatemala, mainly maize and beans (preliminary MAGA figure, via FAO GIEWS). Jul–Aug 2026: 20–26 % of normal rain at our 5 plots (CHIRPS v3). An observation, not a forecast.  

### Slide 3 — Farmer view: an icon and a word
> Good — Circle  
> Watch out — Triangle  
> Happens often — Square  
> Grey: “The satellite can’t see well here” — When data is missing, we say so instead of guessing.  
> Camotán: no quality SMAP data, so the options turn grey.  
> The three facts are the three problems that Kuxur Rum (“my humid land” in Ch’orti’) tackles: permanent cover, no burning and soil moisture through the canícula. FAO and Guatemala’s Ministry of Agriculture have promoted it in Chiquimula since 2000; by 2006 more than 7,000 farms had adopted it.  

### Slide 4 — A tie: no winner today. Not in 2041–2060.
> Olopa, three rotations: score today and NASA NEX-GDDP-CMIP6 futures held (SSP2-4.5, 2041–2060):  
> 879/33What you plant today  
> 909/33Maize with jack bean  
> 9233/33Short-cycle maize ICTA B-5  
> Rule: 3 points or less apart = a tie. Jack bean ties with both others, so all three are shown, in no order. The rule works as a chain. Holds = water as good as today’s practice in today’s climate. Median model: -6.7 % June–August rain, +1.4 °C. With high emissions, today’s practice holds in 3 of 34.  
> Elsewhere both alternatives lead today’s practice by 5 to 8 points and tie with each other: Jocotán 88 / 87 vs 80, San Juan Ermita 88 / 86 vs 80. Camotán (90 / 89 vs 84) and Zacapa (81 / 80 vs 73) show the same gap, but confidence is low there, so the options go grey.  

### Slide 5 — NASA product → the decision it drives
> Product | Decision on the farmer screen  
> MODIS MOD13Q1 — NDVI, 250 m, 16-day | → Bare-soil and low-cover months → Bare soil fact and soil score  
> FIRMS (VIIRS, Suomi NPP) — Active fire, 375 m; a detection is a pixel centre | → Fire years within 500 m, Jan–May → Burning fact  
> CHIRPS v3 daily “sat” — Rain at ~5 km; NASA IMERG’s daily split arrives inside it | → Dry spells over 15 days (< 2 mm/day) → Canícula fact and water deficit  
> SMAP SPL3SMP_E — Soil moisture, 9 km, top 5 cm | → Jul–Aug soil moisture; missing quality data → grey, low confidence  
> NEX-GDDP-CMIP6 — 33–34 climate models, 0.25°, 2041–2060 | → Rain and heat change per model → how many futures each rotation holds (Evidence)  
> CHIRPS comes from the UCSB Climate Hazards Center (Funk et al., 2026); we did not download IMERG directly. MODIS, FIRMS, SMAP and NEX-GDDP-CMIP6 come from NASA (CMIP6 precomputed offline in Google Earth Engine). Also used: NASA POWER (temperature, ET0), SRTM (slope, 90 m) and cached NASA GIBS map layers.  

### Slide 6 — Where it fails
> Not an official alert. — The audio ends: “This is not an official notice: talk it over with your extension worker.”  
> Thresholds were set after seeing the data. — The cut-offs were chosen after counting the 5 plots, not before. An agronomist still has to review them.  
> The 5 plots are example points chosen by satellite, not verified in the field.  
> 2018 back-test: high risk at 5 of 5 plots, but also 2–3 false alarms and 1 miss in 20 years per plot. Against seven years with documented losses it misses 2016, 2019 and 2023 at every plot.  
> Olopa: greenness barely follows the rain deficit, Spearman ρ = 0.07.  
> Zacapa: NASA POWER differs 55.4 % from CHIRPS in Jul–Aug → grey.  
> Camotán: 3007 SMAP readings fail the quality flag → grey.  
> A family here farms about 0.35 ha on average; one MODIS pixel is 6.25 ha. We see the land around the plot, not the plot.  
> Suomi NPP stopped delivering new data in early November 2026 and Terra is being retired: updates would move to VIIRS on NOAA-20 and NOAA-21.  

### Slide 7 — Audio, no internet, next steps
> Audio  
> One tap on Listen: about a minute or less per plot, in plain words, Spanish or English voice, with subtitles in both. The voice is synthetic (AI) and says so.  
> No internet  
> Built to be served from a laptop on a local network: 5 plots, audio and data are local files. Not yet tried in the field.  
> The map falls back to saved MODIS layers.  
> Checked by npm run sin-red with the internet blocked.  
> Next steps  
> Visit the plots with extension workers.  
> Agronomist review of thresholds and scores.  
> Comprehension test of pictograms and audio.  
> Ch’orti’ audio recorded by native speakers: the script and the audio slot are ready.  

---

## Tabla para anotar el resultado y la hora real

| Fecha y hora real (ej. `2026-11-15 15:00`) | Sección leída en voz alta | Tiempo aproximado que tomó leerla | ¿Se leyó fluido de principio a fin? (Sí / No) | Frases marcadas con `[AIRE]`, `[TRABA]`, `[RARO]` o `[DATO]` y cambio sugerido |
|---|---|---|---|---|
| | **1.1 Vista agricultor — Jocotán, de arriba abajo** | | | |
| | **1.2 Vista agricultor — Lo que cambia en Camotán, Olopa, San Juan Ermita y Zacapa** | | | |
| | **1.3 Evidence en inglés (opcional)** | | | |
| | **2.1 `project-page-en.md` — High-Level Project Summary (306 palabras)** | | | |
| | **2.2 `project-page-en.md` — Short version (161 palabras)** | | | |
| | **2.3 `project-page-en.md` — Detailed Project Description, SI y NASA Data** | | | |
| | **3.1 `docs/slides/index.html` — Slides 1, 2 y 3 (portada, el problema y la vista del agricultor)** | | | |
| | **3.2 `docs/slides/index.html` — Slides 4 y 5 (el empate y los futuros de NASA; producto → decisión)** | | | |
| | **3.3 `docs/slides/index.html` — Slides 6 y 7 (dónde falla; audio, sin internet y siguientes pasos)** | | | |
