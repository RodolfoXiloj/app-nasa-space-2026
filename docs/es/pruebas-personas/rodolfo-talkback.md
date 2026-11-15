# Guía 2 para Rodolfo Xiloj: Prueba de la vista agricultor con TalkBack en un Android real

**Responsable:** Rodolfo Xiloj  
**Documentos base:** `docs/es/prueba-telefono.md` y `docs/accessibility.md`  
**Tiempo estimado:** 20 a 25 minutos  

> **Por qué hace falta una persona:** Un navegador automatizado en computadora (Playwright) solo puede inspeccionar el árbol de accesibilidad (los nombres y roles en el código), pero no reproduce la voz real de TalkBack en Android, los gestos táctiles con un dedo y dos dedos, ni posibles choques de volumen entre la voz del lector de pantalla y el audio corto de la parcela.

---

## Qué necesitas antes de empezar

1. **Un teléfono Android real** con Chrome instalado y audífonos o altavoz con buen volumen.
2. **Tu computadora con Windows** conectada a la **misma red Wi-Fi** que el teléfono (o el teléfono compartiendo su punto de acceso Wi-Fi a la computadora).

---

## Paso 1. Servir la web en tu red local desde la computadora

1. Abre una terminal (PowerShell) en la carpeta `web` del repositorio.
2. Construye y sirve la versión de producción exponiéndola en la red local:
   ```powershell
   npm run build
   npx vite preview --host 0.0.0.0 --port 4173
   ```
3. En la terminal verás dos direcciones:
   - `Local:   http://localhost:4173/`
   - `Network: http://192.168.X.X:4173/` (esa dirección `192.168.X.X` es la que abrirás en el teléfono).
   - *(Si no aparece la IP, corre `ipconfig` en otra ventana de PowerShell y busca `Dirección IPv4` bajo `Adaptador de LAN inalámbrica Wi-Fi`).*
4. Antes de activar TalkBack, abre Chrome en el teléfono y entra a `http://192.168.X.X:4173/`.
5. Toca el botón **«Español»** arriba a la derecha para hacer la primera recorrida en español.
   - *(Si la página no carga en el teléfono, abre el Firewall de Windows y permite temporalmente `Node.js` en redes privadas, o conecta el teléfono por cable USB y usa `adb reverse tcp:4173 tcp:4173` para abrir `http://localhost:4173`).*

---

## Paso 2. Cómo activar y apagar TalkBack en Android (y los 4 gestos básicos)

1. En el teléfono Android, abre **Ajustes (Configuración) → Accesibilidad → TalkBack**.
2. Activa **Usar TalkBack** y acepta el permiso.
   - **Tip rápido para apagarlo al terminar:** puedes mantener presionados **ambos botones de volumen (subir + bajar) durante 3 segundos** si el atajo está activo, o volver a Ajustes → Accesibilidad → TalkBack (recuerda que con TalkBack activo te desplazas por la lista con **dos dedos** y para activar un interruptor das **un toque para elegirlo y luego doble toque en cualquier parte de la pantalla**).
3. **Los 4 gestos que usarás en esta prueba:**
   - **Deslizar un dedo hacia la derecha (`→`):** avanza al siguiente elemento en orden de lectura.
   - **Deslizar un dedo hacia la izquierda (`←`):** regresa al elemento anterior.
   - **Doble toque con un dedo:** activa el botón, enlace o lista desplegable que tiene el recuadro de foco.
   - **Arrastrar con dos dedos hacia arriba o abajo:** desplaza la pantalla si quieres ver más abajo (aunque deslizar un dedo a la derecha también baja solo al llegar al borde).

---

## Paso 3. Recorrido paso a paso y qué debe anunciar cada elemento

Vuelve a Chrome con la vista del agricultor abierta en **Jocotán, Chiquimula** (en **Español**). Toca la parte superior izquierda de la pantalla y luego **desliza un dedo hacia la derecha (`→`) paso a paso**.

Compara lo que dice TalkBack en voz alta con esta lista extraída de los textos alternativos (`aria-label`, `<title>` de cada SVG y encabezados) del código:

| Orden | Elemento que recibe el foco en pantalla | Qué debe anunciar TalkBack en Español (parcela Jocotán) | Qué debe anunciar si cambias a Inglés (`English`, parcela Jocotán) |
|---|---|---|---|
| **1** | Título superior (`<h1>`) | **«Milpa Resiliente, encabezado 1»** | **«Milpa Resiliente, heading 1»** |
| **2** | Grupo de botones de idioma (`role="group"`) y sus 2 botones | Agrupación **«Idioma»**:<br>• **«English, sin presionar, botón»** (cambia a voz en inglés por tener `lang="en"`)<br>• **«Español, presionado, botón»** (`aria-pressed="true"`) | Agrupación **«Language»**:<br>• **«English, pressed, button»** (`aria-pressed="true"`)<br>• **«Español, not pressed, button»** (`lang="es"`) |
| **3** | Selector de parcela (`<label>` + `<select id="agr-parcela">`) | **«Parcela: Jocotán, Chiquimula, lista desplegable»**.<br>debajo: **«Parcela de ejemplo en Jocotán.»** | **«Plot: Jocotán, Chiquimula, dropdown list»**.<br>debajo: **«Example plot in Jocotán.»** |
| **3b** | Línea de julio y agosto de 2026 (un párrafo, debajo del selector) | **«Julio y agosto de 2026. Llovió el 24 % de lo normal (mediana 1991-2025), según CHIRPS. Dato preliminar. Observado, no es un pronóstico.»** | **«July and August 2026. Rain was 24 % of normal (median 1991-2025), according to CHIRPS. Preliminary. Observed, not a forecast.»** |
| **4** | Botón grande de audio corto | **«Escuchar. Audio corto, con subtítulos, botón»**.<br>*(Haz **doble toque** aquí: debe empezar a sonar `jocotan.frases.mp3` (8 frases, 60.9 s). El botón sigue diciendo «Escuchar»; abajo aparecen el reproductor de audio (nombre «Escuchar»), el cuadro de subtítulos con `aria-live="polite"`, el botón **«Subtítulos, presionado»**, el grupo **«Volver a escuchar un hecho»** con tres botones (**«Suelo desnudo»**, **«Quema cerca de la parcela»** y **«Canícula larga»**) y la nota de voz sintética generada con IA).* | **«Listen. Short audio with subtitles, button»**.<br>*(Al hacer doble toque suena `jocotan.frases.en.mp3` (8 frases, 65.4 s); el botón sigue diciendo «Listen» y aparecen los subtítulos, el botón **«Subtitles, pressed»** y el grupo **«Hear one fact again»** con **«Bare soil»**, **«Fire near the plot»** y **«Long dry spell (canícula)»**).* |
| **5** | Encabezado de sección de los 3 hechos (`<h2>`) | **«Lo que el satélite vio alrededor de esta parcela, encabezado 2»** seguido de *«Tres hechos de años pasados, siempre en el mismo orden. Son registros, no un pronóstico.»* | **«What the satellite saw around this plot, heading 2»** seguido de *«Three facts from past years, always in the same order. They are records, not a forecast.»* |
| **6** | **Hecho 1: Suelo desnudo** (dentro de lista de 3 elementos) | • Encabezado: **«Suelo desnudo, encabezado 3»**<br>• Estado: **«Pasa seguido»** — *«Lo vio varias veces.»* *(Nota: el cuadrado rojo del semáforo tiene `aria-hidden="true"`, no debe leer código basura del icono)*<br>• Pictograma (rueda de 12 meses, `role="img"`): **«2 de 12 meses con suelo desnudo (marzo y abril). Poca cobertura: febrero y mayo., gráfico»** *(los 12 gajos internos tienen `aria-hidden="true"`, así que NO debe deletrear `E, F, M, A...`)*<br>• Leyenda: **«Suelo desnudo, Poca cobertura, Cubierto»**<br>• Frase y detalles: **«En marzo y abril, su tierra suele quedar sin plantas que la cubran. Lo vio el satélite de 2021 a 2025.»**, **«Desnudo: marzo y abril.»**, **«Poca cobertura: febrero y mayo.»**, **«Fuente: MODIS (NASA), 2021‑2025.»** | • Encabezado: **«Bare soil, heading 3»**<br>• Estado: **«Happens often»** — *«It saw it several times.»*<br>• Pictograma (`role="img"`): **«2 of 12 months with bare soil (March and April). Little cover: February and May., graphic»**<br>• Leyenda: **«Bare soil, Little cover, Covered»**<br>• Frase y detalles: **«In March and April, your land is usually left with no plants covering it. The satellite saw it from 2021 to 2025.»**, **«Bare: March and April.»**, **«Little plant cover: February and May.»**, **«Source: MODIS (NASA), 2021‑2025.»** |
| **7** | **Hecho 2: Quema cerca de la parcela** | • Encabezado: **«Quema cerca de la parcela, encabezado 3»**<br>• Estado: **«Pasa seguido»** — *«Lo vio varias veces.»*<br>• Pictograma (15 puntos, `role="img"`): **«3 de 15 años con quema vista cerca, gráfico»**<br>• Frase y detalles: **«En 3 de los últimos 15 años hubo quemas a menos de medio kilómetro de su parcela, en abril y mayo.»**, **«Meses con quema: abril y mayo.»**, **«Fuente: VIIRS (NASA FIRMS), 2012‑2026.»** | • Encabezado: **«Fire near the plot, heading 3»**<br>• Estado: **«Happens often»** — *«It saw it several times.»*<br>• Pictograma (`role="img"`): **«3 of 15 years with a fire seen nearby, graphic»**<br>• Frase y detalles: **«In 3 of the last 15 years there were fires within half a kilometer of your plot, in April and May.»**, **«Months with fire: April and May.»**, **«Source: VIIRS (NASA FIRMS), 2012‑2026.»** |
| **8** | **Hecho 3: Canícula larga** | • Encabezado: **«Canícula larga, encabezado 3»**<br>• Estado: **«Ponga atención»** — *«Lo vio pocas veces.»*<br>• Pictograma (25 puntos, `role="img"`): **«2 de 25 años con canícula larga, gráfico»**<br>• Frase y detalles: **«En 2 de los últimos 25 años, la canícula dejó más de 15 días seguidos casi sin lluvia.»**, **«Entre junio y agosto.»**, **«Fuente: CHIRPS y IMERG (NASA), 2001‑2025.»** | • Encabezado: **«Long dry spell (canícula), heading 3»**<br>• Estado: **«Watch out»** — *«It saw it a few times.»*<br>• Pictograma (`role="img"`): **«2 of 25 years with a long canícula (midsummer dry spell), graphic»**<br>• Frase y detalles: **«In 2 of the last 25 years, the midsummer drought brought more than 15 days in a row with almost no rain.»**, **«Between June and August.»**, **«Source: CHIRPS and IMERG (NASA), 2001‑2025.»** |
| **8b** | **Tarjeta «Este año»** (`<h2>`, después de los 3 hechos) | • **«Este año, encabezado 2»**<br>• Frase: **«Este año, en julio y agosto, llovió solo la cuarta parte de lo normal (24 %). Es menos que en 2018, el año más seco desde 1991. Es un dato preliminar.»**<br>• Figura de 3 barras (`role="img"`; los nombres y milímetros de las barras tienen `aria-hidden="true"`): **«Lluvia de julio y agosto: un año normal, 324 milímetros; 2018, el año más seco, 138 milímetros; 2026, 79 milímetros., gráfico»**<br>• Nota: **«Lluvia de julio y agosto en su parcela, según CHIRPS (satélite y estaciones). Lo normal es la mediana de 1991 a 2025.»** | • **«This year, heading 2»**<br>• Frase: **«This year, July and August got only a quarter of the normal rain (24 %). That is less than in 2018, the driest year since 1991. It is a preliminary figure.»**<br>• Figura (`role="img"`): **«July and August rain: a normal year, 324 millimeters; 2018, the driest year, 138 millimeters; 2026, 79 millimeters., graphic»**<br>• Nota: **«July and August rain at your plot, according to CHIRPS (satellite and stations). Normal is the 1991-2025 median.»** |
| **9** | **Opciones para platicar con su técnico** (`<h2>`) | • **«Opciones para platicar con su técnico, encabezado 2»**<br>• **«Dos opciones quedan parejas: sus puntajes se separan 3 puntos o menos. Ninguna se separa lo suficiente.»**<br>• Lista de 2 opciones parejas: **«Leguminosa o cobertura: Maíz con canavalia en primera, frijol en postrera y rastrojo en pie»** y **«Cultivo tolerante a sequía: Sorgo en primera y caupí en postrera, con rastrojo en pie»**<br>• **«Sin orden.»**<br>• **«Lo que hace hoy: Maíz con frijol en primera y frijol en postrera»**<br>• **«Qué tan seguros estamos, encabezado 3»** → **«Alta»** → **«Por qué: Las tres comprobaciones se cumplen.»** | • **«Options to talk over with your extension worker, heading 2»**<br>• **«Two options come out even: their scores are 3 points or less apart. None stands out.»**<br>• Lista de 2 opciones parejas en inglés + **«In no particular order.»** + **«What you do today...»**<br>• **«How sure we are, heading 3»** → **«High»** → **«Why: All three checks pass.»** |
| **9b** | **Tarjeta «El futuro: 2041 a 2060»** (`<h2>`, después de las opciones) | • **«El futuro: 2041 a 2060, encabezado 2»**<br>• Frase: **«La NASA calcula 33 climas posibles para 2041 a 2060. Si siembra como hoy, maíz con frijol, le alcanza el agua en 3 de 33. Maíz con canavalia: en 3. Sorgo con caupí: en los 33.»**<br>• Lista de 3 filas; cada una dice su nombre y su conteo, y su fila de 33 matas es una figura (`role="img"`; cada mata tiene `aria-hidden="true"`):<br>**«Como hoy: maíz con frijol 3 de 33»** → **«Como hoy: maíz con frijol: 3 de 33 climas: le alcanza el agua, gráfico»**<br>**«Maíz con canavalia 3 de 33»** → **«Maíz con canavalia: 3 de 33 climas: le alcanza el agua, gráfico»**<br>**«Sorgo con caupí 33 de 33»** → **«Sorgo con caupí: 33 de 33 climas: le alcanza el agua, gráfico»**<br>• Leyenda: **«Cada mata es un clima posible, de un modelo de la NASA (NEX-GDDP-CMIP6, emisiones intermedias). Verde: le alcanza el agua, al menos como hoy. Seca: no le alcanza.»** | • **«The future: 2041 to 2060, heading 2»**<br>• Frase: **«NASA computes 33 possible climates for 2041 to 2060. Planting as today, maize with beans has enough water in 3 of 33. Maize with jack bean: in 3. Sorghum with cowpea: in all 33.»**<br>• Filas (`role="img"`): **«As today: maize with beans: 3 of 33 climates: enough water, graphic»**, **«Maize with jack bean: 3 of 33 climates: enough water, graphic»** y **«Sorghum with cowpea: 33 of 33 climates: enough water, graphic»**<br>• Leyenda: **«Each plant is one possible climate, from a NASA model (NEX-GDDP-CMIP6, intermediate emissions). Green: enough water, at least as today. Dry: not enough.»** |
| **10** | Aviso de que no es un aviso oficial | **«No es un aviso oficial: platíquelo con su técnico.»** | **«This is not an official notice: talk it over with your extension worker.»** |
| **11** | **Compartir esta parcela** (Kit, `<h2>`) | • **«Compartir esta parcela, encabezado 2»**<br>• **«Imprimir hoja, botón»**<br>• **«Descargar audio, enlace»**<br>• **«Compartir por WhatsApp, enlace»**<br>• **«Imagen para WhatsApp, botón»**<br>• **«Guardar para usar sin señal, botón»** solo si la página se abrió por `localhost` (con `adb reverse`) o por https; con `http://192.168.X.X:4173` no sale, y es lo esperado | • **«Share this plot, heading 2»**<br>• **«Print sheet, button»**<br>• **«Download audio, link»**<br>• **«Share on WhatsApp, link»**<br>• **«Image for WhatsApp, button»**<br>• **«Save to use without signal, button»** (con la misma condición) |
| **12** | Botón para abrir *Evidence* | **«Ver la evidencia. Mapa, gráficas, fuentes y límites, botón»** | **«See the evidence. Map, charts, sources and limits, button»** |

### Qué textos alternativos debes oír si cambias el selector de parcela a las otras 4 parcelas (en español):

| Parcela | Pictograma 1 (Suelo, `RuedaMeses`) | Pictograma 2 (Quema, `PuntosAnios`) | Pictograma 3 (Canícula, `PuntosAnios`) | Figura de «Este año» | Filas de matas de «El futuro» |
|---|---|---|---|---|---|
| **Camotán** | `0 de 12 meses con suelo desnudo. Poca cobertura: marzo y abril.` | `3 de 15 años con quema vista cerca` | `2 de 25 años con canícula larga` | `Lluvia de julio y agosto: un año normal, 355 milímetros; 2018, el año más seco, 154 milímetros; 2026, 94 milímetros.` | No sale (confianza baja) |
| **Olopa** | `0 de 12 meses con suelo desnudo. Poca cobertura: marzo y abril.` | `1 de 15 años con quema vista cerca` | `0 de 25 años con canícula larga` | `Lluvia de julio y agosto: un año normal, 475 milímetros; 1997, el año más seco, 211 milímetros; 2026, 106 milímetros.` | `Como hoy: maíz con frijol: 9 de 33 climas: le alcanza el agua`<br>`Maíz con canavalia: 9 de 33 climas: le alcanza el agua`<br>`Maíz de ciclo corto: 33 de 33 climas: le alcanza el agua` |
| **San Juan Ermita** | `3 de 12 meses con suelo desnudo (febrero, marzo y abril). Poca cobertura: enero y mayo.` | `2 de 15 años con quema vista cerca` | `1 de 25 años con canícula larga` | `Lluvia de julio y agosto: un año normal, 345 milímetros; 2018, el año más seco, 140 milímetros; 2026, 69 milímetros.` | `Como hoy: maíz con frijol: 5 de 33 climas: le alcanza el agua`<br>`Maíz con canavalia: 5 de 33 climas: le alcanza el agua`<br>`Sorgo con caupí: 33 de 33 climas: le alcanza el agua` |
| **Zacapa** | `1 de 12 meses con suelo desnudo (abril). Poca cobertura: enero, febrero, marzo y mayo.` | `0 de 15 años con quema vista cerca` | `3 de 25 años con canícula larga` | `Lluvia de julio y agosto: un año normal, 206 milímetros; 2018, el año más seco, 90 milímetros; 2026, 44 milímetros.` | No sale (confianza baja) |

---

## Qué debes vigilar especialmente durante la prueba

0. **Las tres figuras de los hechos tienen que decir su significado, no solo «imagen».** Hasta el 14 nov 2026, Chrome de Android las exponía sin nombre; se corrigió ese día y se comprobó en un emulador (`resultados-automaticos.md`, sección 8). Confírmalo con el dedo: al llegar a la rueda debe decir «2 de 12 meses con suelo desnudo…». Lo mismo con las figuras de las dos tarjetas del 15 nov 2026 (las tres barras de «Este año» y cada fila de matas de «El futuro»): también llevan su nombre en `aria-label`.

1. **Que no lea letras sueltas dentro de los pictogramas:** Al pasar por la rueda de meses (`RuedaMeses`), TalkBack debe leer de corrido la frase resumen (`"2 de 12 meses con suelo desnudo..."`) y **no** ponerse a deletrear las 12 iniciales `E, F, M, A, M, J, J, A, S, O, N, D`.
2. **Qué pasa cuando suena el audio corto y los subtítulos cambian:** El párrafo `.agr-subtitulos` tiene `aria-live="polite"`. Observa y anota si TalkBack intenta leer cada subtítulo mientras ya está sonando la voz de Marta (`jocotan.frases.mp3`) o si espera en silencio mientras no mueves el foco.
3. **Cambio de parcela a mitad de reproducción:** Si el audio de Jocotán está sonando y cambias el selector `#agr-parcela` a **Camotán**, el audio de Jocotán debe callarse de inmediato.
4. **Prueba sin internet en el teléfono:** abierto con `http://192.168.X.X:4173`, el sitio **no registra su service worker** (Chrome solo lo deja con https o `localhost`): funciona sin internet porque todos sus archivos (datos, audio y capas del mapa) los sirve la computadora por la red local. Deja el teléfono en el mismo Wi-Fi que la computadora y **quítale el internet a la red** (desconecta el cable de internet del router, o usa un punto de acceso sin datos). Recarga la pestaña de Chrome y toca **«Escuchar»** con doble toque: la página, el audio corto y los subtítulos deben cargar igual. Si apagas el Wi-Fi del teléfono o lo pones en modo avión, la página no recarga: es lo esperado.

---

## Resultado (domingo 15 nov 2026)

Rodolfo hizo esta prueba en un teléfono Android real: «todo bien». Lo informó hacia las 13:25 (UTC−6). No quedaron anotados la hora de la prueba, el modelo del teléfono, las versiones de Android y Chrome ni lo que anunció cada paso; por eso la tabla de abajo sigue vacía.

## Tabla para anotar el resultado y la hora real

| Fecha y hora real (ej. `2026-11-15 10:15`) | Modelo de teléfono Android y versión de Android / Chrome | Paso o elemento probado | ¿Qué anunció TalkBack exactamente? | ¿Correcto? (Sí / No) | Observaciones o fallos encontrados |
|---|---|---|---|---|---|
| | | **1. Encabezado y botones de idioma** (`English` / `Español`, estado presionado) | | | |
| | | **2. Selector de parcela** (`Parcela: Jocotán, Chiquimula`) | | | |
| | | **2b. Línea de julio y agosto de 2026** (¿se oye completa, como algo que ya pasó?) | | | |
| | | **3. Botón «Escuchar» y subtítulos** (¿choca la voz de TalkBack con el mp3 al sonar?) | | | |
| | | **4. Hecho 1 — Suelo desnudo** (encabezado, «Pasa seguido», rueda de 12 meses sin deletrear letras sueltas) | | | |
| | | **5. Hecho 2 — Quema cerca de la parcela** (encabezado, «Pasa seguido», «3 de 15 años con quema vista cerca») | | | |
| | | **6. Hecho 3 — Canícula larga** (encabezado, «Ponga atención», «2 de 25 años con canícula larga») | | | |
| | | **6b. Tarjeta «Este año»** (encabezado, frase y figura de las 3 barras) | | | |
| | | **7. Opciones para platicar con su técnico y confianza** | | | |
| | | **7b. Tarjeta «El futuro: 2041 a 2060»** (encabezado, frase y las 3 filas de matas) | | | |
| | | **8. Kit «Compartir esta parcela» y botón «Ver la evidencia»** | | | |
| | | **9. Cambio de parcela a Camotán / Olopa** (se calla el audio anterior y cambian los textos alternativos; en Camotán no sale «El futuro») | | | |
| | | **10. Sin internet, con el teléfono en el Wi-Fi de la computadora** (recargar y tocar «Escuchar») | | | |
