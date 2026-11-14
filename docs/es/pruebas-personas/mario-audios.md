# Guía 4 para Mario: Escucha y revisión de los 15 audios y sus subtítulos

**Responsable:** Mario  
**Carpeta de audios:** `web/public/audio/`  
**Tiempo estimado:** 25 a 30 minutos  

> **Por qué hace falta una persona:** Un script automático puede comprobar que los archivos `.mp3` y `.vtt` existen, cuánto duran y que el texto del subtítulo coincide letra por letra con el JSON. Pero solo un oído humano detecta si la voz sintética pronuncia mal un topónimo o cultivo (*Jocotán*, *Camotán*, *Olopa*, *canícula*, *canavalia*, *caupí*, *ZARC*, *SMAP*, *ICTA B-5*), si se corta una sílaba al final de una frase o si el subtítulo va adelantado o atrasado respecto a la voz.

---

## Cómo están organizados los audios en `web/public/audio/`

La aplicación reproduce **15 audios activos** (3 por cada una de las 5 parcelas):

1. **5 audios cortos en español (`{parcela}.frases.mp3`, 26 a 29 s):** suenan en la **vista del agricultor** al poner el idioma en **Español** y tocar **«Escuchar»**. Llevan subtítulos sincronizados frase por frase desde `{parcela}.frases.es.vtt` (6 frases por audio).
2. **5 audios cortos en inglés (`{parcela}.frases.en.mp3`, 28 a 30 s):** suenan en la **vista del agricultor** al dejar el idioma en **English** y tocar **«Listen»**. Llevan subtítulos sincronizados desde `{parcela}.frases.en.vtt` (6 frases por audio).
3. **5 audios largos de la tarjeta en español (`{parcela}.mp3`, 67 a 73 s):** suenan en la **vista *Evidence*** dentro del recuadro **«Tarjeta para el agricultor»**. No usan archivo `.vtt` separado porque el texto completo que lee la voz está impreso justo debajo del reproductor (`texto_tarjeta`).

*(Nota: en la carpeta `web/public/audio/` verás 5 archivos adicionales llamados `{parcela}.en.mp3` de ~90 a 95 s. Son las lecturas en inglés de la tarjeta larga, que ya están generadas pero aún no están conectadas al reproductor de `Tarjeta.jsx`, tal como se declara en `docs/project-page-en.md`. Los incluimos al final por si deseas revisarlos también).*

---

## Paso a paso para hacer la prueba

1. Abre la aplicación web en tu navegador (`http://localhost:4173/`) o abre directamente los archivos de `web/public/audio/` con tu reproductor mientras miras la página.
   - **Recomendación:** Hazlo desde la página web (`http://localhost:4173/`) para comprobar al mismo tiempo que el recuadro de subtítulos va cambiando a la par de la voz.
2. En la **vista del agricultor**:
   - Pon el idioma en **Español**, elige cada parcela en el menú desplegable, toca **«Escuchar»** y sigue las **6 frases** en la tabla del **Grupo 1**.
   - Cambia el idioma a **English**, elige cada parcela, toca **«Listen»** y sigue las **6 frases** en la tabla del **Grupo 2**.
3. Baja y toca **«Ver la evidencia»** (*See the evidence*), ve a la sección **«Tarjeta para el agricultor»** y dale reproducir al audio de cada una de las 5 parcelas mientras sigues el párrafo del **Grupo 3**.
4. Marca en la tabla final la **hora real** en que escuchaste cada audio y anota cualquier palabra mal pronunciada, corte brusco o desfase de subtítulo.

---

## Lista completa de los 15 audios y el texto exacto que debe sonar

### Grupo 1. Vista del agricultor — 5 audios cortos en Español (voz `es-GT-MartaNeural`)

#### Audio 1: Jocotán (español corto)
- **Archivo MP3:** `web/public/audio/jocotan.frases.mp3` (duración: **26.0 s**, 105 KB)
- **Archivo de subtítulos:** `web/public/audio/jocotan.frases.es.vtt` (6 frases)

| Frase | Tiempo (`.vtt`) | Texto del subtítulo que debe verse y escucharse |
|---|---|---|
| 1 (`parcela`) | `00:00.000 → 00:02.649` | `Parcela de Jocotán, con voz de computadora.` |
| 2 (`suelo`) | `00:02.899 → 00:07.729` | `Suelo: se repite. El satélite vio 2 meses de suelo desnudo.` |
| 3 (`quema`) | `00:07.979 → 00:12.359` | `Quema: se repite. Vio quemas cerca en 3 de 15 años.` |
| 4 (`canicula`) | `00:12.609 → 00:18.503` | `Canícula: atención. Racha seca de más de 15 días en 2 de 25 años.` |
| 5 (`opciones`) | `00:18.753 → 00:22.681` | `Hay dos opciones parejas: maíz con canavalia o sorgo con caupí.` |
| 6 (`cierre`) | `00:22.931 → 00:25.984` | `No es un aviso oficial: platíquelo con su técnico.` |

#### Audio 2: Camotán (español corto)
- **Archivo MP3:** `web/public/audio/camotan.frases.mp3` (duración: **27.4 s**, 111 KB)
- **Archivo de subtítulos:** `web/public/audio/camotan.frases.es.vtt` (6 frases)

| Frase | Tiempo (`.vtt`) | Texto del subtítulo que debe verse y escucharse |
|---|---|---|
| 1 (`parcela`) | `00:00.000 → 00:02.636` | `Parcela de Camotán, con voz de computadora.` |
| 2 (`suelo`) | `00:02.886 → 00:08.925` | `Suelo: atención. El satélite vio 2 meses con poca cobertura, ninguno desnudo.` |
| 3 (`quema`) | `00:09.175 → 00:13.555` | `Quema: se repite. Vio quemas cerca en 3 de 15 años.` |
| 4 (`canicula`) | `00:13.805 → 00:19.698` | `Canícula: atención. Racha seca de más de 15 días en 2 de 25 años.` |
| 5 (`opciones`) | `00:19.948 → 00:24.131` | `No podemos decir qué opción conviene más: falta la humedad del suelo de SMAP.` |
| 6 (`cierre`) | `00:24.381 → 00:27.435` | `No es un aviso oficial: platíquelo con su técnico.` |

#### Audio 3: Olopa (español corto)
- **Archivo MP3:** `web/public/audio/olopa.frases.mp3` (duración: **28.6 s**, 116 KB)
- **Archivo de subtítulos:** `web/public/audio/olopa.frases.es.vtt` (6 frases)

| Frase | Tiempo (`.vtt`) | Texto del subtítulo que debe verse y escucharse |
|---|---|---|
| 1 (`parcela`) | `00:00.000 → 00:02.466` | `Parcela de Olopa, con voz de computadora.` |
| 2 (`suelo`) | `00:02.716 → 00:08.754` | `Suelo: atención. El satélite vio 2 meses con poca cobertura, ninguno desnudo.` |
| 3 (`quema`) | `00:09.004 → 00:13.445` | `Quema: atención. Vio quemas cerca en 1 de 15 años.` |
| 4 (`canicula`) | `00:13.695 → 00:19.308` | `Canícula: bien. Ninguna racha seca pasó de 15 días en 25 años.` |
| 5 (`opciones`) | `00:19.558 → 00:25.294` | `Las tres opciones quedan parejas: lo que siembra hoy, maíz con canavalia y maíz de ciclo corto.` |
| 6 (`cierre`) | `00:25.544 → 00:28.597` | `No es un aviso oficial: platíquelo con su técnico.` |

#### Audio 4: San Juan Ermita (español corto)
- **Archivo MP3:** `web/public/audio/san_juan_ermita.frases.mp3` (duración: **26.4 s**, 107 KB)
- **Archivo de subtítulos:** `web/public/audio/san_juan_ermita.frases.es.vtt` (6 frases)

| Frase | Tiempo (`.vtt`) | Texto del subtítulo que debe verse y escucharse |
|---|---|---|
| 1 (`parcela`) | `00:00.000 → 00:02.990` | `Parcela de San Juan Ermita, con voz de computadora.` |
| 2 (`suelo`) | `00:03.240 → 00:08.127` | `Suelo: se repite. El satélite vio 3 meses de suelo desnudo.` |
| 3 (`quema`) | `00:08.377 → 00:12.764` | `Quema: atención. Vio quemas cerca en 2 de 15 años.` |
| 4 (`canicula`) | `00:13.014 → 00:18.947` | `Canícula: atención. Racha seca de más de 15 días en 1 de 25 años.` |
| 5 (`opciones`) | `00:19.197 → 00:23.125` | `Hay dos opciones parejas: maíz con canavalia o sorgo con caupí.` |
| 6 (`cierre`) | `00:23.375 → 00:26.428` | `No es un aviso oficial: platíquelo con su técnico.` |

#### Audio 5: Zacapa (español corto)
- **Archivo MP3:** `web/public/audio/zacapa.frases.mp3` (duración: **26.9 s**, 109 KB)
- **Archivo de subtítulos:** `web/public/audio/zacapa.frases.es.vtt` (6 frases)

| Frase | Tiempo (`.vtt`) | Texto del subtítulo que debe verse y escucharse |
|---|---|---|
| 1 (`parcela`) | `00:00.000 → 00:02.558` | `Parcela de Zacapa, con voz de computadora.` |
| 2 (`suelo`) | `00:02.808 → 00:08.701` | `Suelo: atención. El satélite vio 1 mes de suelo desnudo y 4 con poca cobertura.` |
| 3 (`quema`) | `00:08.951 → 00:12.835` | `Quema: bien. No vio quemas cerca en 15 años.` |
| 4 (`canicula`) | `00:13.085 → 00:19.038` | `Canícula: se repite. Racha seca de más de 15 días en 3 de 25 años.` |
| 5 (`opciones`) | `00:19.288 → 00:23.574` | `No podemos decir qué opción conviene más: dos fuentes de lluvia no coinciden.` |
| 6 (`cierre`) | `00:23.824 → 00:26.877` | `No es un aviso oficial: platíquelo con su técnico.` |

---

### Grupo 2. Vista del agricultor — 5 audios cortos en Inglés (voz `en-US-JennyNeural`)

*(Nota técnica útil: los archivos `.frases.en.vtt` comparten las marcas de tiempo de las 6 frases con el español; revisa al escuchar si el cambio de cada subtítulo en inglés acompaña bien a la voz de Jenny).*

**Aviso:** los subtítulos de los audios cortos en inglés se están corrigiendo en la rama `entrega-impacto-6`. Si esa rama ya se unió a `main` cuando hagas la prueba, revisa los tiempos nuevos; si no, anota igual los desfases que oigas.

#### Audio 6: Jocotán (inglés corto)
- **Archivo MP3:** `web/public/audio/jocotan.frases.en.mp3` (duración: **28.5 s**, 115 KB)
- **Archivo de subtítulos:** `web/public/audio/jocotan.frases.en.vtt` (6 frases)

| Frase | Tiempo (`.vtt`) | Texto del subtítulo que debe verse y escucharse |
|---|---|---|
| 1 (`parcela`) | `00:00.000 → 00:02.649` | `Jocotán plot, read by a computer voice.` |
| 2 (`suelo`) | `00:02.899 → 00:07.729` | `Soil: repeats. The satellite saw 2 months of bare soil.` |
| 3 (`quema`) | `00:07.979 → 00:12.359` | `Burning: repeats. Fires seen nearby in 3 of 15 years.` |
| 4 (`canicula`) | `00:12.609 → 00:18.503` | `Midsummer drought: watch. Dry spells longer than 15 days in 2 of 25 years.` |
| 5 (`opciones`) | `00:18.753 → 00:22.681` | `There are two even options: maize with jack bean or sorghum with cowpea.` |
| 6 (`cierre`) | `00:22.931 → 00:25.984` | `This is not an official notice: talk it over with your extension worker.` |

#### Audio 7: Camotán (inglés corto)
- **Archivo MP3:** `web/public/audio/camotan.frases.en.mp3` (duración: **29.3 s**, 118 KB)
- **Archivo de subtítulos:** `web/public/audio/camotan.frases.en.vtt` (6 frases)

| Frase | Tiempo (`.vtt`) | Texto del subtítulo que debe verse y escucharse |
|---|---|---|
| 1 (`parcela`) | `00:00.000 → 00:02.636` | `Camotán plot, read by a computer voice.` |
| 2 (`suelo`) | `00:02.886 → 00:08.925` | `Soil: watch. The satellite saw 2 months with little cover, none bare.` |
| 3 (`quema`) | `00:09.175 → 00:13.555` | `Burning: repeats. Fires seen nearby in 3 of 15 years.` |
| 4 (`canicula`) | `00:13.805 → 00:19.698` | `Midsummer drought: watch. Dry spells longer than 15 days in 2 of 25 years.` |
| 5 (`opciones`) | `00:19.948 → 00:24.131` | `We can't say which option is best: SMAP soil moisture is missing.` |
| 6 (`cierre`) | `00:24.381 → 00:27.435` | `This is not an official notice: talk it over with your extension worker.` |

#### Audio 8: Olopa (inglés corto)
- **Archivo MP3:** `web/public/audio/olopa.frases.en.mp3` (duración: **29.8 s**, 91 KB)
- **Archivo de subtítulos:** `web/public/audio/olopa.frases.en.vtt` (6 frases)

| Frase | Tiempo (`.vtt`) | Texto del subtítulo que debe verse y escucharse |
|---|---|---|
| 1 (`parcela`) | `00:00.000 → 00:02.466` | `Olopa plot, read by a computer voice.` |
| 2 (`suelo`) | `00:02.716 → 00:08.754` | `Soil: watch. The satellite saw 2 months with little cover, none bare.` |
| 3 (`quema`) | `00:09.004 → 00:13.445` | `Burning: watch. Fires seen nearby in 1 of 15 years.` |
| 4 (`canicula`) | `00:13.695 → 00:19.308` | `Midsummer drought: good. No dry spell went past 15 days in 25 years.` |
| 5 (`opciones`) | `00:19.558 → 00:25.294` | `All three options come out even: what you plant today, maize with jack bean and short-cycle maize.` |
| 6 (`cierre`) | `00:25.544 → 00:28.597` | `This is not an official notice: talk it over with your extension worker.` |

#### Audio 9: San Juan Ermita (inglés corto)
- **Archivo MP3:** `web/public/audio/san_juan_ermita.frases.en.mp3` (duración: **28.6 s**, 116 KB)
- **Archivo de subtítulos:** `web/public/audio/san_juan_ermita.frases.en.vtt` (6 frases)

| Frase | Tiempo (`.vtt`) | Texto del subtítulo que debe verse y escucharse |
|---|---|---|
| 1 (`parcela`) | `00:00.000 → 00:02.990` | `San Juan Ermita plot, read by a computer voice.` |
| 2 (`suelo`) | `00:03.240 → 00:08.127` | `Soil: repeats. The satellite saw 3 months of bare soil.` |
| 3 (`quema`) | `00:08.377 → 00:12.764` | `Burning: watch. Fires seen nearby in 2 of 15 years.` |
| 4 (`canicula`) | `00:13.014 → 00:18.947` | `Midsummer drought: watch. Dry spells longer than 15 days in 1 of 25 years.` |
| 5 (`opciones`) | `00:19.197 → 00:23.125` | `There are two even options: maize with jack bean or sorghum with cowpea.` |
| 6 (`cierre`) | `00:23.375 → 00:26.428` | `This is not an official notice: talk it over with your extension worker.` |

#### Audio 10: Zacapa (inglés corto)
- **Archivo MP3:** `web/public/audio/zacapa.frases.en.mp3` (duración: **29.0 s**, 117 KB)
- **Archivo de subtítulos:** `web/public/audio/zacapa.frases.en.vtt` (6 frases)

| Frase | Tiempo (`.vtt`) | Texto del subtítulo que debe verse y escucharse |
|---|---|---|
| 1 (`parcela`) | `00:00.000 → 00:02.558` | `Zacapa plot, read by a computer voice.` |
| 2 (`suelo`) | `00:02.808 → 00:08.701` | `Soil: watch. The satellite saw 1 month of bare soil and 4 with little cover.` |
| 3 (`quema`) | `00:08.951 → 00:12.835` | `Burning: good. No fires seen nearby in 15 years.` |
| 4 (`canicula`) | `00:13.085 → 00:19.038` | `Midsummer drought: repeats. Dry spells longer than 15 days in 3 of 25 years.` |
| 5 (`opciones`) | `00:19.288 → 00:23.574` | `We can't say which option is best: two rain sources disagree.` |
| 6 (`cierre`) | `00:23.824 → 00:26.877` | `This is not an official notice: talk it over with your extension worker.` |

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

### Archivos adicionales en `web/public/audio/` (5 tarjetas en inglés generadas, aún no conectadas al reproductor de `Tarjeta.jsx`)

- `web/public/audio/jocotan.en.mp3` (92.7 s)
- `web/public/audio/camotan.en.mp3` (90.0 s)
- `web/public/audio/olopa.en.mp3` (95.2 s)
- `web/public/audio/san_juan_ermita.en.mp3` (94.3 s)
- `web/public/audio/zacapa.en.mp3` (89.4 s)

---

## Tabla para anotar el resultado y la hora real

| # | Fecha y hora real (ej. `2026-11-15 10:00`) | Ruta del archivo MP3 | Archivo de subtítulos o texto | Duración esperada | ¿Se escuchó completo y claro? (Sí / No) | ¿El subtítulo coincidió con la voz? (Sí / No) | Palabras mal pronunciadas, cortes o errores detectados |
|---|---|---|---|---|---|---|---|
| **1** | | `web/public/audio/jocotan.frases.mp3` | `jocotan.frases.es.vtt` (6 frases) | 26.0 s | | | |
| **2** | | `web/public/audio/camotan.frases.mp3` | `camotan.frases.es.vtt` (6 frases) | 27.4 s | | | |
| **3** | | `web/public/audio/olopa.frases.mp3` | `olopa.frases.es.vtt` (6 frases) | 28.6 s | | | |
| **4** | | `web/public/audio/san_juan_ermita.frases.mp3` | `san_juan_ermita.frases.es.vtt` (6 frases) | 26.4 s | | | |
| **5** | | `web/public/audio/zacapa.frases.mp3` | `zacapa.frases.es.vtt` (6 frases) | 26.9 s | | | |
| **6** | | `web/public/audio/jocotan.frases.en.mp3` | `jocotan.frases.en.vtt` (6 frases) | 28.5 s | | | |
| **7** | | `web/public/audio/camotan.frases.en.mp3` | `camotan.frases.en.vtt` (6 frases) | 29.3 s | | | |
| **8** | | `web/public/audio/olopa.frases.en.mp3` | `olopa.frases.en.vtt` (6 frases) | 29.8 s | | | |
| **9** | | `web/public/audio/san_juan_ermita.frases.en.mp3` | `san_juan_ermita.frases.en.vtt` (6 frases) | 28.6 s | | | |
| **10** | | `web/public/audio/zacapa.frases.en.mp3` | `zacapa.frases.en.vtt` (6 frases) | 29.0 s | | | |
| **11** | | `web/public/audio/jocotan.mp3` | `texto_tarjeta` en `jocotan.json` | 70.9 s | | | |
| **12** | | `web/public/audio/camotan.mp3` | `texto_tarjeta` en `camotan.json` | 68.2 s | | | |
| **13** | | `web/public/audio/olopa.mp3` | `texto_tarjeta` en `olopa.json` | 73.5 s | | | |
| **14** | | `web/public/audio/san_juan_ermita.mp3` | `texto_tarjeta` en `san_juan_ermita.json` | 71.7 s | | | |
| **15** | | `web/public/audio/zacapa.mp3` | `texto_tarjeta` en `zacapa.json` | 67.1 s | | | |
