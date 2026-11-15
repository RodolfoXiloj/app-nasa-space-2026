# Guía 4 para Mario: Escucha y revisión de los 20 audios y sus subtítulos

**Responsable:** Mario  
**Carpeta de audios:** `web/public/audio/`  
**Tiempo estimado:** 40 a 45 minutos  

> **Por qué hace falta una persona:** Un script automático puede comprobar que los archivos `.mp3` y `.vtt` existen, cuánto duran y que el texto del subtítulo coincide letra por letra con el JSON. Pero solo un oído humano detecta si la voz sintética pronuncia mal un topónimo o cultivo (*Jocotán*, *Camotán*, *Olopa*, *canícula*, *canavalia*, *caupí*, *ZARC*, *SMAP*, *ICTA B-5*), si se corta una sílaba al final de una frase o si el subtítulo va adelantado o atrasado respecto a la voz.

---

## Cómo están organizados los audios en `web/public/audio/`

La aplicación reproduce **20 audios activos** (4 por cada una de las 5 parcelas):

1. **5 audios cortos en español (`{parcela}.frases.mp3`, 44.6 a 63.4 s):** suenan en la **vista del agricultor** al poner el idioma en **Español** y tocar **«Escuchar»**. Llevan subtítulos sincronizados frase por frase desde `{parcela}.frases.es.vtt` (8 frases por audio; 7 en Camotán y Zacapa, que no traen la frase `futuro` porque sus opciones van en gris).
2. **5 audios cortos en inglés (`{parcela}.frases.en.mp3`, 49.0 a 66.8 s):** suenan en la **vista del agricultor** al dejar el idioma en **English** y tocar **«Listen»**. Llevan subtítulos sincronizados desde `{parcela}.frases.en.vtt` (las mismas 8 o 7 frases que en español).
3. **5 audios largos de la tarjeta en español (`{parcela}.mp3`, 67 a 73 s):** suenan en la **vista *Evidence*** dentro del recuadro **«Tarjeta para el agricultor»**, con el idioma en **Español**. No usan archivo `.vtt` separado porque el texto completo que lee la voz está impreso justo debajo del reproductor (`texto_tarjeta`).
4. **5 audios largos de la tarjeta en inglés (`{parcela}.en.mp3`, 89 a 95 s):** suenan en el mismo reproductor de *Evidence* con el idioma en **English** (desde el 14 nov 2026; antes la tarjeta sonaba en español en los dos idiomas).

*(Nota: los subtítulos en inglés del audio corto se corrigieron el 14 nov 2026: ahora siguen los tiempos del mp3 en inglés, no los del español. Fíjate igual en si cada frase cambia a la par de la voz.)*

*(El 15 nov 2026 se rehicieron los 10 audios cortos: ahora dicen con frases claras qué pasó, cuándo y cada cuánto, y suman la lluvia de este año (`este_anio`) y los climas de 2041 a 2060 (`futuro`). Las tablas de abajo ya traen esos textos y tiempos; lo que se escuchó el 14 nov era la versión anterior. Los 10 audios largos de la tarjeta no cambiaron.)*

---

## Paso a paso para hacer la prueba

1. Abre la aplicación web en tu navegador (`http://localhost:4173/`) o abre directamente los archivos de `web/public/audio/` con tu reproductor mientras miras la página.
   - **Recomendación:** Hazlo desde la página web (`http://localhost:4173/`) para comprobar al mismo tiempo que el recuadro de subtítulos va cambiando a la par de la voz.
2. En la **vista del agricultor**:
   - Pon el idioma en **Español**, elige cada parcela en el menú desplegable, toca **«Escuchar»** y sigue las **7 u 8 frases** en la tabla del **Grupo 1**.
   - Cambia el idioma a **English**, elige cada parcela, toca **«Listen»** y sigue las **7 u 8 frases** en la tabla del **Grupo 2**.
3. Baja y toca **«Ver la evidencia»** (*See the evidence*), ve a la sección **«Tarjeta para el agricultor»** y dale reproducir al audio de cada una de las 5 parcelas mientras sigues el párrafo del **Grupo 3**.
   - Cambia el idioma a **English** dentro de *Evidence* y repite con las 5 parcelas siguiendo el **Grupo 4**: debe sonar la voz en inglés, no la española.
4. Marca en la tabla final la **hora real** en que escuchaste cada audio y anota cualquier palabra mal pronunciada, corte brusco o desfase de subtítulo.

---

## Lista completa de los 20 audios y el texto exacto que debe sonar

### Grupo 1. Vista del agricultor — 5 audios cortos en Español (voz `es-GT-MartaNeural`)

#### Audio 1: Jocotán (español corto)
- **Archivo MP3:** `web/public/audio/jocotan.frases.mp3` (duración: **60.9 s**, 244 872 bytes)
- **Archivo de subtítulos:** `web/public/audio/jocotan.frases.es.vtt` (8 frases)

| Frase | Tiempo (`.vtt`) | Texto del subtítulo que debe verse y escucharse |
|---|---|---|
| 1 (`parcela`) | `00:00.000 → 00:03.906` | `Parcela de Jocotán. Le habla una voz de computadora.` |
| 2 (`suelo`) | `00:04.156 → 00:11.943` | `En marzo y abril, su tierra suele quedar sin plantas que la cubran. Lo vio el satélite de 2021 a 2025.` |
| 3 (`quema`) | `00:12.193 → 00:17.460` | `En 3 de los últimos 15 años hubo quemas a menos de medio kilómetro de su parcela, en abril y mayo.` |
| 4 (`canicula`) | `00:17.710 → 00:23.141` | `En 2 de los últimos 25 años, la canícula dejó más de 15 días seguidos casi sin lluvia.` |
| 5 (`este_anio`) | `00:23.391 → 00:36.560` | `Este año, en julio y agosto, llovió solo la cuarta parte de lo normal (24 %). Es menos que en 2018, el año más seco desde 1991. Es un dato preliminar.` |
| 6 (`opciones`) | `00:36.810 → 00:40.968` | `Hoy hay dos opciones parejas: maíz con canavalia o sorgo con caupí.` |
| 7 (`futuro`) | `00:41.218 → 00:57.594` | `La NASA calcula 33 climas posibles para 2041 a 2060. Si siembra como hoy, maíz con frijol, le alcanza el agua en 3 de 33. Maíz con canavalia: en 3. Sorgo con caupí: en los 33.` |
| 8 (`cierre`) | `00:57.844 → 01:00.897` | `No es un aviso oficial: platíquelo con su técnico.` |

#### Audio 2: Camotán (español corto)
- **Archivo MP3:** `web/public/audio/camotan.frases.mp3` (duración: **44.6 s**, 179 580 bytes)
- **Archivo de subtítulos:** `web/public/audio/camotan.frases.es.vtt` (7 frases)

| Frase | Tiempo (`.vtt`) | Texto del subtítulo que debe verse y escucharse |
|---|---|---|
| 1 (`parcela`) | `00:00.000 → 00:03.892` | `Parcela de Camotán. Le habla una voz de computadora.` |
| 2 (`suelo`) | `00:04.142 → 00:12.184` | `En marzo y abril, su tierra suele quedar con pocas plantas que la cubran. Lo vio el satélite de 2021 a 2025.` |
| 3 (`quema`) | `00:12.434 → 00:17.773` | `En 3 de los últimos 15 años hubo quemas a menos de medio kilómetro de su parcela, en marzo y abril.` |
| 4 (`canicula`) | `00:18.023 → 00:23.454` | `En 2 de los últimos 25 años, la canícula dejó más de 15 días seguidos casi sin lluvia.` |
| 5 (`este_anio`) | `00:23.704 → 00:36.835` | `Este año, en julio y agosto, llovió solo la cuarta parte de lo normal (26 %). Es menos que en 2018, el año más seco desde 1991. Es un dato preliminar.` |
| 6 (`opciones`) | `00:37.085 → 00:41.268` | `No podemos decir qué opción conviene más: falta la humedad del suelo de SMAP.` |
| 7 (`cierre`) | `00:41.518 → 00:44.572` | `No es un aviso oficial: platíquelo con su técnico.` |

#### Audio 3: Olopa (español corto)
- **Archivo MP3:** `web/public/audio/olopa.frases.mp3` (duración: **63.4 s**, 254 760 bytes)
- **Archivo de subtítulos:** `web/public/audio/olopa.frases.es.vtt` (8 frases)

| Frase | Tiempo (`.vtt`) | Texto del subtítulo que debe verse y escucharse |
|---|---|---|
| 1 (`parcela`) | `00:00.000 → 00:03.785` | `Parcela de Olopa. Le habla una voz de computadora.` |
| 2 (`suelo`) | `00:04.035 → 00:12.077` | `En marzo y abril, su tierra suele quedar con pocas plantas que la cubran. Lo vio el satélite de 2021 a 2025.` |
| 3 (`quema`) | `00:12.327 → 00:17.219` | `En 1 de los últimos 15 años hubo quemas a menos de medio kilómetro de su parcela, en abril.` |
| 4 (`canicula`) | `00:17.469 → 00:22.860` | `En los últimos 25 años, la canícula nunca dejó más de 15 días seguidos casi sin lluvia.` |
| 5 (`este_anio`) | `00:23.110 → 00:36.762` | `Este año, en julio y agosto, llovió solo la quinta parte de lo normal (22 %). Es menos que en 1997, el año más seco desde 1991. Es un dato preliminar.` |
| 6 (`opciones`) | `00:37.012 → 00:43.175` | `Hoy, las tres opciones quedan parejas: lo que siembra hoy, maíz con canavalia y maíz de ciclo corto.` |
| 7 (`futuro`) | `00:43.425 → 01:00.079` | `La NASA calcula 33 climas posibles para 2041 a 2060. Si siembra como hoy, maíz con frijol, le alcanza el agua en 9 de 33. Maíz con canavalia: en 9. Maíz de ciclo corto: en los 33.` |
| 8 (`cierre`) | `01:00.329 → 01:03.382` | `No es un aviso oficial: platíquelo con su técnico.` |

#### Audio 4: San Juan Ermita (español corto)
- **Archivo MP3:** `web/public/audio/san_juan_ermita.frases.mp3` (duración: **61.9 s**, 249 012 bytes)
- **Archivo de subtítulos:** `web/public/audio/san_juan_ermita.frases.es.vtt` (8 frases)

| Frase | Tiempo (`.vtt`) | Texto del subtítulo que debe verse y escucharse |
|---|---|---|
| 1 (`parcela`) | `00:00.000 → 00:04.251` | `Parcela de San Juan Ermita. Le habla una voz de computadora.` |
| 2 (`suelo`) | `00:04.501 → 00:13.011` | `En febrero, marzo y abril, su tierra suele quedar sin plantas que la cubran. Lo vio el satélite de 2021 a 2025.` |
| 3 (`quema`) | `00:13.261 → 00:18.573` | `En 2 de los últimos 15 años hubo quemas a menos de medio kilómetro de su parcela, en marzo y abril.` |
| 4 (`canicula`) | `00:18.823 → 00:24.358` | `En 1 de los últimos 25 años, la canícula dejó más de 15 días seguidos casi sin lluvia.` |
| 5 (`este_anio`) | `00:24.608 → 00:37.533` | `Este año, en julio y agosto, llovió solo la quinta parte de lo normal (20 %). Es menos que en 2018, el año más seco desde 1991. Es un dato preliminar.` |
| 6 (`opciones`) | `00:37.783 → 00:41.942` | `Hoy hay dos opciones parejas: maíz con canavalia o sorgo con caupí.` |
| 7 (`futuro`) | `00:42.192 → 00:58.626` | `La NASA calcula 33 climas posibles para 2041 a 2060. Si siembra como hoy, maíz con frijol, le alcanza el agua en 5 de 33. Maíz con canavalia: en 5. Sorgo con caupí: en los 33.` |
| 8 (`cierre`) | `00:58.876 → 01:01.929` | `No es un aviso oficial: platíquelo con su técnico.` |

#### Audio 5: Zacapa (español corto)
- **Archivo MP3:** `web/public/audio/zacapa.frases.mp3` (duración: **47.0 s**, 189 275 bytes)
- **Archivo de subtítulos:** `web/public/audio/zacapa.frases.es.vtt` (7 frases)

| Frase | Tiempo (`.vtt`) | Texto del subtítulo que debe verse y escucharse |
|---|---|---|
| 1 (`parcela`) | `00:00.000 → 00:03.847` | `Parcela de Zacapa. Le habla una voz de computadora.` |
| 2 (`suelo`) | `00:04.097 → 00:14.816` | `En abril, su tierra suele quedar sin plantas que la cubran; en enero, febrero, marzo y mayo, con pocas. Lo vio el satélite de 2021 a 2025.` |
| 3 (`quema`) | `00:15.066 → 00:20.096` | `En los últimos 15 años, el satélite no vio quemas a menos de medio kilómetro de su parcela.` |
| 4 (`canicula`) | `00:20.346 → 00:25.834` | `En 3 de los últimos 25 años, la canícula dejó más de 15 días seguidos casi sin lluvia.` |
| 5 (`este_anio`) | `00:26.084 → 00:39.175` | `Este año, en julio y agosto, llovió solo la quinta parte de lo normal (21 %). Es menos que en 2018, el año más seco desde 1991. Es un dato preliminar.` |
| 6 (`opciones`) | `00:39.425 → 00:43.711` | `No podemos decir qué opción conviene más: dos fuentes de lluvia no coinciden.` |
| 7 (`cierre`) | `00:43.961 → 00:47.015` | `No es un aviso oficial: platíquelo con su técnico.` |

---

### Grupo 2. Vista del agricultor — 5 audios cortos en Inglés (voz `en-US-JennyNeural`)

*(Nota técnica útil: cada `.frases.en.vtt` lleva sus propios tiempos, medidos sobre el mp3 en inglés, así que no coinciden con los del español; revisa al escuchar si el cambio de cada subtítulo en inglés acompaña bien a la voz).*

#### Audio 6: Jocotán (inglés corto)
- **Archivo MP3:** `web/public/audio/jocotan.frases.en.mp3` (duración: **65.4 s**, 263 010 bytes)
- **Archivo de subtítulos:** `web/public/audio/jocotan.frases.en.vtt` (8 frases)

| Frase | Tiempo (`.vtt`) | Texto del subtítulo que debe verse y escucharse |
|---|---|---|
| 1 (`parcela`) | `00:00.000 → 00:03.902` | `Jocotán plot. A computer voice is reading this.` |
| 2 (`suelo`) | `00:04.152 → 00:12.991` | `In March and April, your land is usually left with no plants covering it. The satellite saw it from 2021 to 2025.` |
| 3 (`quema`) | `00:13.241 → 00:19.342` | `In 3 of the last 15 years there were fires within half a kilometer of your plot, in April and May.` |
| 4 (`canicula`) | `00:19.592 → 00:26.193` | `In 2 of the last 25 years, the midsummer drought brought more than 15 days in a row with almost no rain.` |
| 5 (`este_anio`) | `00:26.443 → 00:39.809` | `This year, July and August got only a quarter of the normal rain (24 %). That is less than in 2018, the driest year since 1991. It is a preliminary figure.` |
| 6 (`opciones`) | `00:40.059 → 00:44.621` | `Today there are two even options: maize with jack bean or sorghum with cowpea.` |
| 7 (`futuro`) | `00:44.871 → 01:01.301` | `NASA computes 33 possible climates for 2041 to 2060. Planting as today, maize with beans has enough water in 3 of 33. Maize with jack bean: in 3. Sorghum with cowpea: in all 33.` |
| 8 (`cierre`) | `01:01.551 → 01:05.425` | `This is not an official notice: talk it over with your extension worker.` |

#### Audio 7: Camotán (inglés corto)
- **Archivo MP3:** `web/public/audio/camotan.frases.en.mp3` (duración: **49.0 s**, 197 420 bytes)
- **Archivo de subtítulos:** `web/public/audio/camotan.frases.en.vtt` (7 frases)

| Frase | Tiempo (`.vtt`) | Texto del subtítulo que debe verse y escucharse |
|---|---|---|
| 1 (`parcela`) | `00:00.000 → 00:03.893` | `Camotán plot. A computer voice is reading this.` |
| 2 (`suelo`) | `00:04.143 → 00:12.399` | `In March and April, your land usually has little plant cover. The satellite saw it from 2021 to 2025.` |
| 3 (`quema`) | `00:12.649 → 00:18.946` | `In 3 of the last 15 years there were fires within half a kilometer of your plot, in March and April.` |
| 4 (`canicula`) | `00:19.196 → 00:25.943` | `In 2 of the last 25 years, the midsummer drought brought more than 15 days in a row with almost no rain.` |
| 5 (`este_anio`) | `00:26.193 → 00:40.022` | `This year, July and August got only a quarter of the normal rain (26 %). That is less than in 2018, the driest year since 1991. It is a preliminary figure.` |
| 6 (`opciones`) | `00:40.272 → 00:44.801` | `We can't say which option is best: SMAP soil moisture is missing.` |
| 7 (`cierre`) | `00:45.051 → 00:49.040` | `This is not an official notice: talk it over with your extension worker.` |

#### Audio 8: Olopa (inglés corto)
- **Archivo MP3:** `web/public/audio/olopa.frases.en.mp3` (duración: **65.4 s**, 263 008 bytes)
- **Archivo de subtítulos:** `web/public/audio/olopa.frases.en.vtt` (8 frases)

| Frase | Tiempo (`.vtt`) | Texto del subtítulo que debe verse y escucharse |
|---|---|---|
| 1 (`parcela`) | `00:00.000 → 00:03.862` | `Olopa plot. A computer voice is reading this.` |
| 2 (`suelo`) | `00:04.112 → 00:12.305` | `In March and April, your land usually has little plant cover. The satellite saw it from 2021 to 2025.` |
| 3 (`quema`) | `00:12.555 → 00:17.955` | `In 1 of the last 15 years there were fires within half a kilometer of your plot, in April.` |
| 4 (`canicula`) | `00:18.205 → 00:24.617` | `In the last 25 years, the midsummer drought never brought more than 15 days in a row with almost no rain.` |
| 5 (`este_anio`) | `00:24.867 → 00:38.326` | `This year, July and August got only a fifth of the normal rain (22 %). That is less than in 1997, the driest year since 1991. It is a preliminary figure.` |
| 6 (`opciones`) | `00:38.576 → 00:44.731` | `Today, all three options come out even: what you plant today, maize with jack bean and short-cycle maize.` |
| 7 (`futuro`) | `00:44.981 → 01:01.324` | `NASA computes 33 possible climates for 2041 to 2060. Planting as today, maize with beans has enough water in 9 of 33. Maize with jack bean: in 9. Short-cycle maize: in all 33.` |
| 8 (`cierre`) | `01:01.574 → 01:05.447` | `This is not an official notice: talk it over with your extension worker.` |

#### Audio 9: San Juan Ermita (inglés corto)
- **Archivo MP3:** `web/public/audio/san_juan_ermita.frases.en.mp3` (duración: **66.8 s**, 268 388 bytes)
- **Archivo de subtítulos:** `web/public/audio/san_juan_ermita.frases.en.vtt` (8 frases)

| Frase | Tiempo (`.vtt`) | Texto del subtítulo que debe verse y escucharse |
|---|---|---|
| 1 (`parcela`) | `00:00.000 → 00:04.380` | `San Juan Ermita plot. A computer voice is reading this.` |
| 2 (`suelo`) | `00:04.630 → 00:14.509` | `In February, March and April, your land is usually left with no plants covering it. The satellite saw it from 2021 to 2025.` |
| 3 (`quema`) | `00:14.759 → 00:20.960` | `In 2 of the last 15 years there were fires within half a kilometer of your plot, in March and April.` |
| 4 (`canicula`) | `00:21.210 → 00:27.769` | `In 1 of the last 25 years, the midsummer drought brought more than 15 days in a row with almost no rain.` |
| 5 (`este_anio`) | `00:28.019 → 00:41.028` | `This year, July and August got only a fifth of the normal rain (20 %). That is less than in 2018, the driest year since 1991. It is a preliminary figure.` |
| 6 (`opciones`) | `00:41.278 → 00:45.841` | `Today there are two even options: maize with jack bean or sorghum with cowpea.` |
| 7 (`futuro`) | `00:46.091 → 01:02.667` | `NASA computes 33 possible climates for 2041 to 2060. Planting as today, maize with beans has enough water in 5 of 33. Maize with jack bean: in 5. Sorghum with cowpea: in all 33.` |
| 8 (`cierre`) | `01:02.917 → 01:06.790` | `This is not an official notice: talk it over with your extension worker.` |

#### Audio 10: Zacapa (inglés corto)
- **Archivo MP3:** `web/public/audio/zacapa.frases.en.mp3` (duración: **50.9 s**, 204 716 bytes)
- **Archivo de subtítulos:** `web/public/audio/zacapa.frases.en.vtt` (7 frases)

| Frase | Tiempo (`.vtt`) | Texto del subtítulo que debe verse y escucharse |
|---|---|---|
| 1 (`parcela`) | `00:00.000 → 00:03.958` | `Zacapa plot. A computer voice is reading this.` |
| 2 (`suelo`) | `00:04.208 → 00:16.691` | `In April, your land is usually left with no plants covering it; in January, February, March and May, with little cover. The satellite saw it from 2021 to 2025.` |
| 3 (`quema`) | `00:16.941 → 00:22.380` | `In the last 15 years, the satellite saw no fires within half a kilometer of your plot.` |
| 4 (`canicula`) | `00:22.630 → 00:29.227` | `In 3 of the last 25 years, the midsummer drought brought more than 15 days in a row with almost no rain.` |
| 5 (`este_anio`) | `00:29.477 → 00:42.750` | `This year, July and August got only a fifth of the normal rain (21 %). That is less than in 2018, the driest year since 1991. It is a preliminary figure.` |
| 6 (`opciones`) | `00:43.000 → 00:46.738` | `We can't say which option is best: two rain sources disagree.` |
| 7 (`cierre`) | `00:46.988 → 00:50.861` | `This is not an official notice: talk it over with your extension worker.` |

---

### Grupo 3. Vista *Evidence* — 5 audios largos de la Tarjeta del agricultor (`Tarjeta.jsx`, voz `es-GT-MartaNeural`)

En estos 5 audios el texto completo está escrito como párrafo fijo en la tarjeta debajo del reproductor (`audio.texto` / `texto_tarjeta` en `web/public/data/{parcela}.json`).

#### Audio 11: Jocotán (tarjeta en *Evidence*)
- **Archivo MP3:** `web/public/audio/jocotan.mp3` (duración: **70.9 s**, 426 KB)
- **Texto que debe sonar:**
  > «Parcela de Jocotán, Chiquimula. Lo que ve el satélite: el suelo queda desnudo en marzo y abril. Comparamos tres opciones. Opción uno, lo que hace hoy: maíz con frijol en primera y frijol en postrera. Puntaje 80. Opción dos: Maíz con canavalia en primera, frijol en postrera y rastrojo en pie. Puntaje 88. Opción tres: Sorgo en primera y caupí en postrera, con rastrojo en pie. Puntaje 87. Según su prioridad, agua, ninguna opción se separa lo suficiente: la opción dos y la opción tres quedan parejas. Confianza alta. Fecha de siembra: consúltela en ZARC (FAO–MAGA) con su extensionista. Referencia publicada para el departamento (no es la ventana del municipio): «específicamente en Chiquimula, Quiché y Zacapa… la ZARC determinó un ajuste estratégico: mover las fechas de siembra de mayo a junio» (La Estrella de Panamá, «Países del Corredor Seco afinan siembras con datos climáticos», abril de 2026 (nota de prensa sobre ZARC)). Esta herramienta apoya, no reemplaza, a su técnico.»

#### Audio 12: Camotán (tarjeta en *Evidence*)
- **Archivo MP3:** `web/public/audio/camotan.mp3` (duración: **68.2 s**, 410 KB)
- **Texto que debe sonar:**
  > «Parcela de Camotán, Chiquimula. Lo que ve el satélite: el suelo queda con poca cobertura en marzo y abril. Comparamos tres opciones. Opción uno, lo que hace hoy: maíz con frijol en primera y frijol en postrera. Puntaje 84. Opción dos: Maíz con canavalia en primera, frijol en postrera y rastrojo en pie. Puntaje 90. Opción tres: Sorgo en primera y caupí en postrera, con rastrojo en pie. Puntaje 89. Con la confianza baja, no decimos cuál opción conviene más. Confianza baja. Fecha de siembra: consúltela en ZARC (FAO–MAGA) con su extensionista. Referencia publicada para el departamento (no es la ventana del municipio): «específicamente en Chiquimula, Quiché y Zacapa… la ZARC determinó un ajuste estratégico: mover las fechas de siembra de mayo a junio» (La Estrella de Panamá, «Países del Corredor Seco afinan siembras con datos climáticos», abril de 2026 (nota de prensa sobre ZARC)). Esta herramienta apoya, no reemplaza, a su técnico.»

#### Audio 13: Olopa (tarjeta en *Evidence*)
- **Archivo MP3:** `web/public/audio/olopa.mp3` (duración: **73.5 s**, 441 KB)
- **Texto que debe sonar:**
  > «Parcela de Olopa, Chiquimula. Lo que ve el satélite: el suelo queda con poca cobertura en marzo y abril. Comparamos tres opciones. Opción uno, lo que hace hoy: maíz con frijol en primera y frijol en postrera. Puntaje 87. Opción dos: Maíz con canavalia en primera, frijol en postrera y rastrojo en pie. Puntaje 90. Opción tres: Maíz de ciclo corto ICTA B-5 con frijol en primera y frijol en postrera. Puntaje 92. Según su prioridad, agua, ninguna opción se separa lo suficiente: la opción uno, la opción dos y la opción tres quedan parejas. Confianza media. Fecha de siembra: consúltela en ZARC (FAO–MAGA) con su extensionista. Referencia publicada para el departamento (no es la ventana del municipio): «específicamente en Chiquimula, Quiché y Zacapa… la ZARC determinó un ajuste estratégico: mover las fechas de siembra de mayo a junio» (La Estrella de Panamá, «Países del Corredor Seco afinan siembras con datos climáticos», abril de 2026 (nota de prensa sobre ZARC)). Esta herramienta apoya, no reemplaza, a su técnico.»

#### Audio 14: San Juan Ermita (tarjeta en *Evidence*)
- **Archivo MP3:** `web/public/audio/san_juan_ermita.mp3` (duración: **71.7 s**, 431 KB)
- **Texto que debe sonar:**
  > «Parcela de San Juan Ermita, Chiquimula. Lo que ve el satélite: el suelo queda desnudo en febrero, marzo y abril. Comparamos tres opciones. Opción uno, lo que hace hoy: maíz con frijol en primera y frijol en postrera. Puntaje 80. Opción dos: Maíz con canavalia en primera, frijol en postrera y rastrojo en pie. Puntaje 88. Opción tres: Sorgo en primera y caupí en postrera, con rastrojo en pie. Puntaje 86. Según su prioridad, agua, ninguna opción se separa lo suficiente: la opción dos y la opción tres quedan parejas. Confianza alta. Fecha de siembra: consúltela en ZARC (FAO–MAGA) con su extensionista. Referencia publicada para el departamento (no es la ventana del municipio): «específicamente en Chiquimula, Quiché y Zacapa… la ZARC determinó un ajuste estratégico: mover las fechas de siembra de mayo a junio» (La Estrella de Panamá, «Países del Corredor Seco afinan siembras con datos climáticos», abril de 2026 (nota de prensa sobre ZARC)). Esta herramienta apoya, no reemplaza, a su técnico.»

#### Audio 15: Zacapa (tarjeta en *Evidence*)
- **Archivo MP3:** `web/public/audio/zacapa.mp3` (duración: **67.1 s**, 403 KB)
- **Texto que debe sonar:**
  > «Parcela de Zacapa, Zacapa. Lo que ve el satélite: el suelo queda desnudo en abril. Comparamos tres opciones. Opción uno, lo que hace hoy: maíz con frijol en primera y frijol en postrera. Puntaje 73. Opción dos: Maíz con canavalia en primera, frijol en postrera y rastrojo en pie. Puntaje 81. Opción tres: Sorgo en primera y caupí en postrera, con rastrojo en pie. Puntaje 80. Con la confianza baja, no decimos cuál opción conviene más. Confianza baja. Fecha de siembra: consúltela en ZARC (FAO–MAGA) con su extensionista. Referencia publicada para el departamento (no es la ventana del municipio): «específicamente en Chiquimula, Quiché y Zacapa… la ZARC determinó un ajuste estratégico: mover las fechas de siembra de mayo a junio» (La Estrella de Panamá, «Países del Corredor Seco afinan siembras con datos climáticos», abril de 2026 (nota de prensa sobre ZARC)). Esta herramienta apoya, no reemplaza, a su técnico.»

---

### Grupo 4. Vista *Evidence* — 5 tarjetas en inglés (voz `en-US-JennyNeural`)

Suenan en *Evidence* con el idioma en **English**, en el mismo reproductor de «Card for the farmer». El texto que lee la voz es el del campo `audio.en.texto` de cada JSON.

#### Audio 16: Jocotán (tarjeta en inglés en *Evidence*)
- **Archivo MP3:** `web/public/audio/jocotan.en.mp3` (duración: **92.7 s**, 557 KB)
- **Texto que debe sonar:**
  > «Plot in Jocotán, Chiquimula. What the satellite sees: the soil is left bare in March and April. We compare three options. Option one, what you do today: maize with beans in primera and beans in postrera. Score 80. Option two: Maize with jack bean (canavalia) in primera, beans in postrera and standing stubble. Score 88. Option three: Sorghum in primera and cowpea in postrera, with standing stubble. Score 87. By your priority, water, no option stands out enough: option two and option three are about even. Confidence high. Planting date: check it in ZARC (FAO–MAGA) with your extension worker. Published reference for the department (not the municipality's window): «específicamente en Chiquimula, Quiché y Zacapa… la ZARC determinó un ajuste estratégico: mover las fechas de siembra de mayo a junio» (our translation: «specifically in Chiquimula, Quiché and Zacapa… ZARC set a strategic adjustment: move planting dates from May to June») (La Estrella de Panamá, «Países del Corredor Seco afinan siembras con datos climáticos» (Dry Corridor countries fine-tune planting with climate data), April 2026 (press note on ZARC)). This tool supports, and does not replace, your extension worker.»

#### Audio 17: Camotán (tarjeta en inglés en *Evidence*)
- **Archivo MP3:** `web/public/audio/camotan.en.mp3` (duración: **90.0 s**, 541 KB)
- **Texto que debe sonar:**
  > «Plot in Camotán, Chiquimula. What the satellite sees: the soil has little cover in March and April. We compare three options. Option one, what you do today: maize with beans in primera and beans in postrera. Score 84. Option two: Maize with jack bean (canavalia) in primera, beans in postrera and standing stubble. Score 90. Option three: Sorghum in primera and cowpea in postrera, with standing stubble. Score 89. With low confidence, we do not say which option is better. Confidence low. Planting date: check it in ZARC (FAO–MAGA) with your extension worker. Published reference for the department (not the municipality's window): «específicamente en Chiquimula, Quiché y Zacapa… la ZARC determinó un ajuste estratégico: mover las fechas de siembra de mayo a junio» (our translation: «specifically in Chiquimula, Quiché and Zacapa… ZARC set a strategic adjustment: move planting dates from May to June») (La Estrella de Panamá, «Países del Corredor Seco afinan siembras con datos climáticos» (Dry Corridor countries fine-tune planting with climate data), April 2026 (press note on ZARC)). This tool supports, and does not replace, your extension worker.»

#### Audio 18: Olopa (tarjeta en inglés en *Evidence*)
- **Archivo MP3:** `web/public/audio/olopa.en.mp3` (duración: **95.2 s**, 572 KB)
- **Texto que debe sonar:**
  > «Plot in Olopa, Chiquimula. What the satellite sees: the soil has little cover in March and April. We compare three options. Option one, what you do today: maize with beans in primera and beans in postrera. Score 87. Option two: Maize with jack bean (canavalia) in primera, beans in postrera and standing stubble. Score 90. Option three: Short-cycle maize ICTA B-5 with beans in primera and beans in postrera. Score 92. By your priority, water, no option stands out enough: option one, option two and option three are about even. Confidence medium. Planting date: check it in ZARC (FAO–MAGA) with your extension worker. Published reference for the department (not the municipality's window): «específicamente en Chiquimula, Quiché y Zacapa… la ZARC determinó un ajuste estratégico: mover las fechas de siembra de mayo a junio» (our translation: «specifically in Chiquimula, Quiché and Zacapa… ZARC set a strategic adjustment: move planting dates from May to June») (La Estrella de Panamá, «Países del Corredor Seco afinan siembras con datos climáticos» (Dry Corridor countries fine-tune planting with climate data), April 2026 (press note on ZARC)). This tool supports, and does not replace, your extension worker.»

#### Audio 19: San Juan Ermita (tarjeta en inglés en *Evidence*)
- **Archivo MP3:** `web/public/audio/san_juan_ermita.en.mp3` (duración: **94.3 s**, 566 KB)
- **Texto que debe sonar:**
  > «Plot in San Juan Ermita, Chiquimula. What the satellite sees: the soil is left bare in February, March and April. We compare three options. Option one, what you do today: maize with beans in primera and beans in postrera. Score 80. Option two: Maize with jack bean (canavalia) in primera, beans in postrera and standing stubble. Score 88. Option three: Sorghum in primera and cowpea in postrera, with standing stubble. Score 86. By your priority, water, no option stands out enough: option two and option three are about even. Confidence high. Planting date: check it in ZARC (FAO–MAGA) with your extension worker. Published reference for the department (not the municipality's window): «específicamente en Chiquimula, Quiché y Zacapa… la ZARC determinó un ajuste estratégico: mover las fechas de siembra de mayo a junio» (our translation: «specifically in Chiquimula, Quiché and Zacapa… ZARC set a strategic adjustment: move planting dates from May to June») (La Estrella de Panamá, «Países del Corredor Seco afinan siembras con datos climáticos» (Dry Corridor countries fine-tune planting with climate data), April 2026 (press note on ZARC)). This tool supports, and does not replace, your extension worker.»

#### Audio 20: Zacapa (tarjeta en inglés en *Evidence*)
- **Archivo MP3:** `web/public/audio/zacapa.en.mp3` (duración: **89.4 s**, 537 KB)
- **Texto que debe sonar:**
  > «Plot in Zacapa, Zacapa. What the satellite sees: the soil is left bare in April. We compare three options. Option one, what you do today: maize with beans in primera and beans in postrera. Score 73. Option two: Maize with jack bean (canavalia) in primera, beans in postrera and standing stubble. Score 81. Option three: Sorghum in primera and cowpea in postrera, with standing stubble. Score 80. With low confidence, we do not say which option is better. Confidence low. Planting date: check it in ZARC (FAO–MAGA) with your extension worker. Published reference for the department (not the municipality's window): «específicamente en Chiquimula, Quiché y Zacapa… la ZARC determinó un ajuste estratégico: mover las fechas de siembra de mayo a junio» (our translation: «specifically in Chiquimula, Quiché and Zacapa… ZARC set a strategic adjustment: move planting dates from May to June») (La Estrella de Panamá, «Países del Corredor Seco afinan siembras con datos climáticos» (Dry Corridor countries fine-tune planting with climate data), April 2026 (press note on ZARC)). This tool supports, and does not replace, your extension worker.»
---

## Tabla para anotar el resultado y la hora real

| # | Fecha y hora real (ej. `2026-11-15 10:00`) | Ruta del archivo MP3 | Archivo de subtítulos o texto | Duración esperada | ¿Se escuchó completo y claro? (Sí / No) | ¿El subtítulo coincidió con la voz? (Sí / No) | Palabras mal pronunciadas, cortes o errores detectados |
|---|---|---|---|---|---|---|---|
| **1** | | `web/public/audio/jocotan.frases.mp3` | `jocotan.frases.es.vtt` (8 frases) | 60.9 s | | | |
| **2** | | `web/public/audio/camotan.frases.mp3` | `camotan.frases.es.vtt` (7 frases) | 44.6 s | | | |
| **3** | | `web/public/audio/olopa.frases.mp3` | `olopa.frases.es.vtt` (8 frases) | 63.4 s | | | |
| **4** | | `web/public/audio/san_juan_ermita.frases.mp3` | `san_juan_ermita.frases.es.vtt` (8 frases) | 61.9 s | | | |
| **5** | | `web/public/audio/zacapa.frases.mp3` | `zacapa.frases.es.vtt` (7 frases) | 47.0 s | | | |
| **6** | | `web/public/audio/jocotan.frases.en.mp3` | `jocotan.frases.en.vtt` (8 frases) | 65.4 s | | | |
| **7** | | `web/public/audio/camotan.frases.en.mp3` | `camotan.frases.en.vtt` (7 frases) | 49.0 s | | | |
| **8** | | `web/public/audio/olopa.frases.en.mp3` | `olopa.frases.en.vtt` (8 frases) | 65.4 s | | | |
| **9** | | `web/public/audio/san_juan_ermita.frases.en.mp3` | `san_juan_ermita.frases.en.vtt` (8 frases) | 66.8 s | | | |
| **10** | | `web/public/audio/zacapa.frases.en.mp3` | `zacapa.frases.en.vtt` (7 frases) | 50.9 s | | | |
| **11** | | `web/public/audio/jocotan.mp3` | `texto_tarjeta` en `jocotan.json` | 70.9 s | | | |
| **12** | | `web/public/audio/camotan.mp3` | `texto_tarjeta` en `camotan.json` | 68.2 s | | | |
| **13** | | `web/public/audio/olopa.mp3` | `texto_tarjeta` en `olopa.json` | 73.5 s | | | |
| **14** | | `web/public/audio/san_juan_ermita.mp3` | `texto_tarjeta` en `san_juan_ermita.json` | 71.7 s | | | |
| **15** | | `web/public/audio/zacapa.mp3` | `texto_tarjeta` en `zacapa.json` | 67.1 s | | | |
| **16** | | `web/public/audio/jocotan.en.mp3` | `audio.en.texto` en `jocotan.json` | 92.7 s | | | |
| **17** | | `web/public/audio/camotan.en.mp3` | `audio.en.texto` en `camotan.json` | 90.0 s | | | |
| **18** | | `web/public/audio/olopa.en.mp3` | `audio.en.texto` en `olopa.json` | 95.2 s | | | |
| **19** | | `web/public/audio/san_juan_ermita.en.mp3` | `audio.en.texto` en `san_juan_ermita.json` | 94.3 s | | | |
| **20** | | `web/public/audio/zacapa.en.mp3` | `audio.en.texto` en `zacapa.json` | 89.4 s | | | |
