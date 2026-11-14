# Pictogramas / Pictograms

Paso 3 del plan (ideas A3, A7 y A9). Código en `web/src/pictos/`. Captura a 390 px: `docs/capturas/pictos.png`.
Step 3 of the plan (ideas A3, A7 and A9). Code in `web/src/pictos/`. Screenshot at 390 px: `docs/capturas/pictos.png`.

**Estado: falta la prueba de comprensión.** Iván decide con esa prueba si cada dibujo se entiende. Hasta entonces, ninguno está aprobado.
**Status: the comprehension test is still pending.** Iván decides with that test whether each drawing is understood. Until then, none is approved.

## Cómo están hechos / How they are made

- SVG propios, dibujados para este proyecto. Sin IA, sin juegos de íconos de terceros y sin dependencias nuevas.
  Our own SVGs, drawn for this project. No AI, no third-party icon sets and no new dependencies.
- Una sola línea gruesa en `currentColor` y rellenos solo en negro sólido. Se leen igual en color, en grises y en fotocopia en blanco y negro. Ningún dibujo depende del color.
  One thick line in `currentColor`, and fills only in solid black. They read the same in colour, in greyscale and on a black-and-white photocopy. No drawing depends on colour.
- Cada uno lleva un `<title>` en español o inglés según la prop `lang`, para lectores de pantalla. Con `decorativo` se ocultan (`aria-hidden`).
  Each one has a Spanish or English `<title>`, chosen by the `lang` prop, for screen readers. With `decorativo` they are hidden (`aria-hidden`).
- Todas las cantidades llegan por props. Los componentes no traen cifras propias.
  All quantities come in through props. The components carry no numbers of their own.
- Todavía no se usan en las vistas: se conectan al unir los carriles.
  They are not used in the views yet: they get wired in when the lanes are merged.

Galería de desarrollo: `npm run dev` y abrir `/src/pictos/galeria.html`. Lee los JSON de `web/public/data/` y no entra en el build.
Development gallery: `npm run dev` and open `/src/pictos/galeria.html`. It reads the JSON files in `web/public/data/` and is not part of the build.

## Los 10 pictogramas obligatorios / The 10 required pictograms

La idea A3 lista 14. Estos 10 cubren los 3 hechos del semáforo, las opciones con maíz y frijol, el satélite y «hable con su técnico». Quedan para después: maicillo, ayote, canavalia y rastrojo.
Idea A3 lists 14. These 10 cover the 3 traffic-light facts, the maize-and-bean options, the satellite and "talk with your extension worker". Left for later: sorghum (maicillo), squash (ayote), jack bean (canavalia) and crop residue (rastrojo).

| Componente | Qué representa / What it stands for | Dibujo / Drawing | Pregunta de comprensión / Comprehension question |
|---|---|---|---|
| `SueloDesnudo` | Suelo desnudo: el hecho «suelo» del semáforo (MODIS MOD13Q1) / Bare soil: the "soil" fact (MODIS MOD13Q1) | Franja de tierra negra con grietas blancas / Black strip of earth with white cracks | «¿Qué ve aquí? ¿Cómo está la tierra?» / "What do you see here? How is the soil?" |
| `SueloCubierto` | Suelo cubierto por plantas o rastrojo / Soil covered by plants or residue | La misma franja con tres plantitas encima / The same strip with three small plants on top | «¿En qué se diferencia del dibujo anterior?» / "How is it different from the previous drawing?" |
| `Fuego` | Quema cerca de la parcela: el hecho «quema» (FIRMS VIIRS) / Fire near the plot: the "fire" fact (FIRMS VIIRS) | Llama con lengua interior negra / Flame with a black inner tongue | «¿Qué pasó aquí?» / "What happened here?" |
| `Sol` | Sol fuerte, días seguidos sin lluvia: el hecho «canícula» (CHIRPS diario con IMERG) / Strong sun, days in a row without rain: the "canícula" fact (daily CHIRPS with IMERG) | Disco negro con 8 rayos / Black disc with 8 rays | «¿Este dibujo le hace pensar en la canícula?» / "Does this drawing make you think of the canícula?" |
| `Lluvia` | Lluvia / Rain | Nube con tres trazos inclinados / Cloud with three slanted strokes | «¿Qué cae de la nube?» / "What is falling from the cloud?" |
| `Gota` | Agua: la prioridad «agua» de las opciones / Water: the "water" priority of the options | Gota con brillo / Drop with a highlight | «¿Qué es esto?» / "What is this?" |
| `Maiz` | Maíz / Maize | Mazorca con granos y dos hojas de tusa negras / Cob with kernels and two black husk leaves | «¿Qué cultivo es?» / "Which crop is it?" |
| `Frijol` | Frijol / Beans | Dos granos en forma de riñón, uno negro y uno de línea / Two kidney-shaped seeds, one black and one outlined | «¿Qué cultivo es?» (riesgo: que se lea como piedras) / "Which crop is it?" (risk: it may read as stones) |
| `Satelite` | El satélite: de dónde salen los datos / The satellite: where the data come from | Cuerpo negro, dos paneles y ondas hacia abajo / Black body, two panels and waves pointing down | «¿Qué es? ¿Qué hace?» / "What is it? What does it do?" |
| `Platicar` | Platicar con su técnico: el cierre de cada recomendación / Talk with your extension worker: how every suggestion ends | Dos personas frente a frente y un globo de diálogo / Two people facing each other and a speech bubble | «¿Qué le está pidiendo este dibujo que haga?» / "What is this drawing asking you to do?" |

## Cantidades como dibujos / Quantities as drawings

| Componente | Qué representa / What it stands for | Props (de dónde salen / where they come from) | Pregunta de comprensión / Comprehension question |
|---|---|---|---|
| `RuedaMeses` | Los 12 meses, enero arriba, en el sentido del reloj. Negro = suelo desnudo; rayado = poca cobertura; blanco = cubierto. El número del centro es la cantidad de meses desnudos / The 12 months, January at the top, clockwise. Black = bare soil; hatched = little cover; white = covered. The number in the middle counts the bare months | `desnudos` y `poca` (`farmer.hechos[suelo].meses` y `.meses_poca_cobertura`, 1 = enero); `sinDatos` para el estado gris | «¿En qué meses está pelada la tierra?» y «¿qué quiere decir el rayado?» / "In which months is the soil bare?" and "what does the hatching mean?" |
| `PuntosAnios` con `tipo="quema"` | Un punto por año observado; los años con quema vista llevan una llama blanca en un disco negro y van primero / One dot per observed year; years with a fire seen carry a white flame on a black disc and come first | `marcados` y `total` (`farmer.hechos[quema].valor` y `.de`) | «¿Cuántos años hubo quema cerca?» / "In how many years was there a fire nearby?" |
| `PuntosAnios` con `tipo="canicula"` | Lo mismo con un sol, para los años con canícula larga / The same with a sun, for years with a long canícula | `marcados` y `total` (`farmer.hechos[canicula].valor` y `.de`) | «¿Cuántos años la canícula fue larga?» / "In how many years was the canícula long?" |
| `PixelManzanas` | El cuadro que ve el satélite, dividido en manzanas; la manzana rayada es una / The square the satellite sees, divided into manzanas; the hatched one is one manzana | `ladoPixelM` (resolución de MODIS MOD13Q1 en `fuentes`) y `m2PorManzana` | «¿El satélite ve solo su parcela o algo más grande?» / "Does the satellite see only your plot or something bigger?" |

- No se dibuja qué año tuvo quema o canícula larga: el contrato solo trae el conteo. Por eso los años marcados van primero y no en orden de calendario.
  The drawing does not say which year had a fire or a long canícula: the contract only carries the count. That is why marked years come first and not in calendar order.
- Con los datos de hoy la galería da lo mismo que la tabla «Los conteos reales» de `docs/umbrales.md` (revisado en Jocotán, Olopa y Zacapa).
  With today's data the gallery matches the "Los conteos reales" table in `docs/umbrales.md` (checked for Jocotán, Olopa and Zacapa).

## Lo que falta confirmar / Still to confirm

1. **Superficie de la manzana.** La galería usa 6 987 m² (1 manzana = 10 000 varas cuadradas, vara de 0.8359 m). Es la conversión habitual en Guatemala, pero sale de memoria y no del repo: verificar con una fuente y, si sirve, agregarla al contrato o a `data/glosario.yaml` (carril A). Con ese valor, 250 m × 250 m = 6.25 ha ≈ 8.9 manzanas, que se redondea a «unas 9», como dice el plan.
   **Area of a manzana.** The gallery uses 6,987 m² (1 manzana = 10,000 square varas, 0.8359 m vara). It is the usual conversion in Guatemala, but it comes from memory, not from the repo: check it against a source and, if it holds, add it to the contract or to `data/glosario.yaml` (lane A). With that value, 250 m × 250 m = 6.25 ha ≈ 8.9 manzanas, rounded to "about 9", as the plan says.
2. **Prueba de comprensión (Iván).** Mostrar cada dibujo sin la palabra, hacer la pregunta de la tabla y anotar la respuesta tal cual. Un dibujo pasa si la mayoría lo entiende sin ayuda. Si uno falla, se corrige antes del domingo 9:00; después, se publica qué falló (riesgo R10 del plan).
   **Comprehension test (Iván).** Show each drawing without its word, ask the question in the table and write down the answer as given. A drawing passes if most people understand it without help. If one fails, fix it before Sunday 9:00; after that, publish what failed (risk R10 in the plan).
3. **Impresión.** Imprimir la galería en modo «Papel (b/n)» en una impresora láser y fotocopiarla una vez. Revisar que el rayado de la rueda no se confunda con el negro.
   **Printing.** Print the gallery in "Paper (b/w)" mode on a laser printer and photocopy it once. Check that the wheel's hatching is not mistaken for solid black.
