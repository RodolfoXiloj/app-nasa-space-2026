# Plan de la versión interactiva (v2)

Sábado 14 nov 2026, 20:30 (Guatemala). Sale de las dos investigaciones de hoy: la de competidores, que es una nota local fuera de git y no se sube a GitHub (decisión de Rodolfo), y [investigacion-herramientas-interactivas.md](investigacion-herramientas-interactivas.md). Aquí cada hallazgo tiene su decisión (se integra, se adapta o se descarta) y su motivo. Lo que se integra baja a ítems con los datos que usa, los archivos que toca, el peso que agrega y la prueba que lo da por terminado.

Esfuerzo: **S** son unas horas, **M** cerca de un día y **L** varios días.

## 1. Dos versiones, dos ramas

| Versión | Rama | Qué es | Dónde se ve |
|---|---|---|---|
| **Lite**, la que se entrega | `main`, y `lite` como copia fija | El sitio de hoy: la vista del agricultor y Evidence | https://milpa-resiliente.onrender.com/ (Render lo reconstruye con cada push a `main`) |
| **Interactiva (v2)** | `v2-interactiva` | Todo lo de este plan | Un segundo sitio estático en Render que sigue esta rama. Se crea aparte, sin tocar el `render.yaml` de `main`, después del envío y con las condiciones de «Lo que dicen las reglas», más abajo. La rama no lleva la investigación de competidores |

- `lite` y `v2-interactiva` salen de `main` en `29b9d18`. Hasta el envío (domingo 15 nov, 12:00, hora de Guatemala) `main` todavía puede recibir arreglos. Al enviar, `lite` avanza a ese mismo commit (avance directo, sin forzar) y el commit se marca con la etiqueta `entrega-2026-11-15`.
- **Decidido por Rodolfo (sábado 14 nov, noche):** la versión que se entrega es la lite; v2 no entra a `main` por ahora; la investigación de competidores no se sube a GitHub. Queda como archivo local, fuera de git: está en `.git/info/exclude` y en ningún commit.
- **Después del envío, nada de v2 entra a `main` hasta que se anuncien los ganadores globales de 2026.** El formulario enlaza al sitio de Render, y Render lo reconstruye con cada push a `main`: si v2 entrara, los jueces verían un sitio distinto del enviado.
- `v2-interactiva` trae los arreglos de `main` con merge, nunca con rebase.
- Las ramas de trabajo de v2 (sección 6) salen de `v2-interactiva` y Rodolfo las une, igual que con los carriles de [carriles.md](carriles.md).
- La idea de «lite» sigue viva dentro de v2: la primera pantalla de v2 sigue siendo ligera (regla 1) y el ítem A6 deja abrir la versión ligera en teléfonos que piden ahorro de datos.

### Lo que dicen las reglas de Space Apps

Revisado el sábado 14 nov a las 21:00 con el buscador. Las páginas de spaceappschallenge.org no abren desde esta máquina (error de certificado), así que la guía de 2026 no se leyó completa; lo de abajo sale de lo que el buscador muestra de las guías oficiales.

- **El envío es final.** La [guía de envío](https://www.spaceappschallenge.org/resources/project-submission-guide/) dice que lo guardado o enviado después del plazo no se evalúa y que después del plazo no hay pedidos de cambio ni excepciones. Los jueces ven solo el último envío.
- **Todo enlace debe abrir sin contraseña, permiso ni registro.** Si los jueces no pueden abrir el proyecto, no lo evalúan. Por eso el repo tiene que estar público antes de enviar y el sitio de Render tiene que seguir en línea mientras dure la evaluación.
- **La evaluación dura semanas.** En 2025, los nominados globales salieron el 5 nov, los finalistas el 26 nov y los ganadores el 18 dic ([guía de evaluación y premios](https://www.spaceappschallenge.org/resources/judging-awards-guide), [premios 2025](https://spaceappschallenge.org/2025/awards)). Las fechas de 2026 hay que verlas en el sitio oficial.
- **Lo que no encontramos:** ninguna regla habla de cambiar el sitio o el repo enlazados después del plazo. La lectura segura es que lo enlazado se queda como estaba al enviar; cualquier otra cosa necesitaría una excepción de la organización.

Con eso, el segundo sitio de v2 (decidido por Rodolfo) va con tres condiciones:

1. Se crea **después** del envío, no antes.
2. Arriba de todo lleva un aviso visible, en los dos idiomas: «Versión en desarrollo, posterior al envío del 15 nov 2026. La versión evaluada es https://milpa-resiliente.onrender.com/».
3. No se enlaza desde el formulario, ni desde el README de `main`, ni desde el sitio evaluado. Si `v2-interactiva` se sube a GitHub con el repo ya público, `main` sigue siendo la rama por defecto y el README de la rama lleva el mismo aviso.

## 2. Reglas que v2 no rompe

1. **La primera pantalla sigue en 172 kB de JavaScript o menos.** Hoy pesa 171.53 kB ([../peso.md](../peso.md)), así que quedan 0.47 kB. Todo lo nuevo de la vista del agricultor llega con `import()` después del primer pintado, como ya pasa con Escuchar, el kit y la línea de 2026.
2. **Ninguna cifra sale de otro lado que no sea el motor o la caché con procedencia.** Si una gráfica necesita una cifra nueva, la calcula Python (motor o pipeline), la exporta al JSON y la cubre una prueba. La web solo dibuja.
3. **Sin servidor, sin claves y sin red de terceros para ver las parcelas.** Las capas y los datos nuevos se guardan en `web/public/`. No se usan CDN ni tokens de Mapbox o de otros servicios.
4. **La escala se dice siempre.** La herramienta describe la tierra alrededor de la parcela, no la parcela. Cada capa nueva lleva su resolución y su fecha.
5. **La accesibilidad queda igual o mejor.** Nada depende solo del color. Cada gráfica y cada control nuevo tiene alternativa en texto, se usa con teclado y tiene objetivos de 48 px. Con `prefers-reduced-motion` nada se anima. Todo va en español y en inglés.
6. **Las dependencias nuevas necesitan acuerdo** (regla de los carriles). Cada una dice cuánto pesa y en qué archivo se carga.
7. **Cada fase cierra con la batería completa:** `python -m pytest`, `npm run smoke`, `npm run build` (con el peso), `npm run sin-red` y Playwright del agricultor y de Evidence.

## 3. Qué de la investigación se sostiene

Revisado el sábado 14 nov de 20:00 a 20:20 con buscador y leyendo las páginas. La página de retos de 2026 y la de ganadores de 2025 en spaceappschallenge.org no abrieron desde esta máquina (error de certificado), y la de ganadores de 2024 devolvió 403.

| Afirmación | Estado | Qué hacemos |
|---|---|---|
| Los cinco equipos de Field Shift 2026 que nombra la investigación de competidores | **Sin verificar.** No aparece ninguno en el buscador y la lista de equipos no abrió | No se nombran en el repo, en documentos públicos ni en las diapositivas. Sus «debilidades» no tienen fuente. Sus ideas se evalúan por lo que valen solas |
| NVS-knot (Kyiv, Ucrania), Galactic Impact 2024 | Confirmado por una fuente secundaria (Universe Magazine, 20 ene 2025): es una app para que los agricultores usen datos de NASA ante problemas de agua. La fuente no menciona SMAP ni OpenET | Se puede citar con esa fuente y sin decir qué datos usa |
| GaamaRamma, app WaterWise, Best Use of Data 2024 | Confirmado por la misma fuente: mapea campos y muestra lluvia a 7 días con datos de OpenET | Sirve de referencia para el patrón «mapa con serie» |
| Zumorroda-X (El Cairo, Egipto), Art & Technology 2025, reto NASA Farm Navigators | Sale en resultados de spaceappschallenge.org, pero la página de ganadores no abrió | Probable. Abrir la página a mano antes de citarlo |
| OpenET: NASA, USGS, DRI, EDF y Google; ensamble de 6 modelos | No se revisó esta noche. Coincide con lo que se sabe de OpenET. Cubre Estados Unidos, no Guatemala | Es un referente de diseño válido |
| «Milpa adopta los estándares visuales de OpenET» (fila nueva de `existing-tools.md`) | **Falso hoy.** El sitio no tiene contorno de parcela ni desglose de modelos | Corregido en esta rama: OpenET queda como referente de v2, no como algo ya hecho |
| «Milpa es 100 % offline-first y funciona sin red en la parcela» | **Exagerado.** El sitio no necesita red de terceros y el mapa cambia solo a la capa guardada. Pero no hay service worker, así que sin señal la página tiene que estar abierta de antes | Lo arregla el ítem A5. Mientras tanto no se dice así |
| «El SRTM ya está en el pipeline» (para el 3D) | Parcial. Solo hay altitud y pendiente de los 5 puntos (OpenTopoData `srtm90m`); no hay modelo de elevación en teselas | El relieve necesita un cliente nuevo (M4) |
| «Las teselas de terreno pesan menos de 2 MB» | Sin medir | Se mide al bajarlas |
| Capas para el «antes y después» | Ya existen en el sitio: NDVI del 22 mar 2026 (época seca) y del 14 sep 2026 (lluvias), zoom 7 a 9 | El primer comparador se puede hacer ya. Compara época seca con época de lluvias, no «año normal contra sequía» |
| Futuros en 3D con el puntaje de cada modelo en el eje Z | `futuros_nasa.json` trae, por modelo, el cambio de lluvia, el de temperatura y si cada rotación aguanta (sí o no). No trae un puntaje por modelo | Se hace en 2D (G3) |
| «Lego agronómico» con «probabilidad de soportar la canícula» y «ahorro de humedad en los primeros 30 cm» | El motor no calcula ninguna de las dos cifras | Se adapta sin ellas (S1) |

## 4. Cada hallazgo y su decisión

| # | Hallazgo (de dónde sale) | Decisión | Ítem |
|---|---|---|---|
| 1 | Comparador «antes y después» con deslizador (competidores §5.1, herramientas §2.1 C) | Se integra | M3 |
| 2 | Relieve 3D con SRTM (competidores §5.2, herramientas §2.1 A) | Se adapta en dos pasos: primero el relieve sombreado; el 3D después y con compuerta | M4, M5 |
| 3 | Línea de tiempo de la canícula que se recorre con el dedo (competidores §5.3, herramientas §2.2 A) | Se integra | G2 |
| 4 | Onda de sonido y subtítulos tipo karaoke (competidores §5.4, herramientas §2.3 A) | Se adapta: la frase que suena ilumina su hecho; barras decorativas hechas con CSS; sin Wavesurfer.js | A1, A2 |
| 5 | Constructor de rotaciones (competidores §5.5, herramientas §2.2 C) | Se adapta: se elige entre las plantillas de la biblioteca con los puntajes del motor; sin cifras inventadas; botones en lugar de arrastrar y soltar | S1 |
| 6 | Contorno de la parcela con opacidad graduable (OpenET) | Se adapta: la huella real de cada producto (MODIS, FIRMS, CHIRPS, SMAP, POWER) y la opacidad de las capas | M1, M2 |
| 7 | Mapa y serie sincronizados (OpenET) | Se adapta a lo que hay: al elegir parcela cambian sus gráficas (ya pasa hoy) y tocar un año en G2 lo marca en G1 y G4 | G2 |
| 8 | Curva de agua acumulada (OpenET) y déficit por etapa del cultivo (competidores §2.4) | Se integra | G1 |
| 9 | Desglose del ensamble de modelos (OpenET) | Se integra con los modelos CMIP6 | G3 |
| 10 | Comparación entre años (OpenET) | Se integra | G4 |
| 11 | Escenarios con respuesta visual inmediata (competidores §2.3) | Ya existe (`Controles.jsx`); solo se agrega una transición corta, que no corre con movimiento reducido | G5 |
| 12 | Rotación vista como secuencia de temporadas (competidores §2.2) | Ya existe el calendario de 12 meses; S1 lo reutiliza | S1 |
| 13 | Tarjeta tipo infografía para WhatsApp (competidores §2.5) | Se integra | K1 |
| 14 | Pictogramas con microanimaciones (herramientas §2.3 B) | Se integra con límites y después de la prueba con personas | A3 |
| 15 | Tocar un hecho y ver sus años (herramientas, fase 1.3) | Se integra con `import()`; la prueba con personas decide si va | A4 |
| 16 | Partículas de viento (herramientas §2.1 D) | **Se descarta.** No hay datos de viento a la escala de la parcela y sugeriría una causa que el análisis no estudia | — |
| 17 | deck.gl-raster y álgebra de bandas en la GPU (herramientas §2.1 B) | **Se descarta.** No tenemos las bandas, solo imágenes de GIBS ya pintadas, y pesa mucho | — |
| 18 | Columnas hexagonales H3 en 3D (herramientas §2.1 B) | **Se descarta.** Son 5 puntos, no una malla | — |
| 19 | Futuros en 3D con ECharts o Three.js (herramientas §2.2 B) | **Se descarta el 3D.** Queda G3 en 2D con Recharts, que ya está en Evidence | G3 |
| 20 | Observable Plot o D3 para recorrer gráficas (herramientas §2.2 A) | **Se descarta la librería.** Recharts ya trae `Brush` y G2 es un SVG propio | — |
| 21 | Predicción de rendimiento con aprendizaje automático (competidores §2.3) | **Se descarta.** El motor no da kg/ha ni quintales | — |
| 22 | Alertas automáticas por SMS o WhatsApp (competidores §2.5) | **Se descarta en v2.** Necesita servidor y números de teléfono, que son datos personales | — |
| 23 | Riego de precisión (competidores §2.4) | **No aplica.** La milpa del Corredor Seco es de temporal | — |
| 24 | «Offline-first» (competidores §4) | Se hace cierto | A5 |
| 25 | Cargar lo pesado solo cuando se pide (herramientas §4) | Ya es la regla; v2 la sigue y suma el modo ligero | A6 |

## 5. Los ítems

### Mapa (Evidence)

**M1. Lo que ve cada satélite.** Al elegir una parcela, el mapa dibuja alrededor del punto la parcela familiar promedio (0.35 ha), el píxel de MODIS, el radio de 500 m de FIRMS, la celda de CHIRPS (0.05°), la de SMAP (9 km) y la de POWER (0.5° × 0.625°). Un botón «De la parcela al satélite» aleja el mapa paso a paso; con movimiento reducido salta sin animar. Debajo, una lista en texto con la superficie de cada una. Es la versión honesta del «contorno de parcela» de OpenET: muestra lo que mira cada producto.
- **Datos:** Python calcula los bordes con la geometría de cada malla (sinusoidal de MODIS, EASE-Grid 2.0 de SMAP y la malla regular de CHIRPS y de POWER) y los escribe en un archivo nuevo, `web/public/data/huellas.json`, sin tocar el contrato. CHIRPS ya trae su píxel en `validacion.json` (`pixel_chirps`).
- **Archivos:** `motor/huellas.py` (nuevo), `tests/test_huellas.py`, `web/src/components/Mapa.jsx`, `web/src/i18n/`.
- **Peso:** unos 2 a 3 kB en Evidence; nada en la primera pantalla.
- **Se da por hecho cuando:** una prueba de Python comprueba que el píxel de MODIS contiene el punto y mide 231.66 m de lado, y que la celda de CHIRPS coincide con `pixel_chirps`; Playwright ve las seis huellas y la lista en texto.
- **Esfuerzo:** M. **Sugerido:** Rodolfo (motor y web); Mario revisa las mallas.

**M2. Opacidad de las capas NDVI.** Un deslizador de 0 a 100 % para las dos capas NDVI guardadas, para ver el color real debajo.
- **Datos:** ya están. **Archivos:** `Mapa.jsx`, `i18n/`. **Peso:** menos de 1 kB en Evidence.
- **Se da por hecho cuando:** se mueve con las flechas del teclado, tiene nombre en los dos idiomas y `npm run sin-red` sigue pasando (23 de 23).
- **Esfuerzo:** S. **Sugerido:** Rodolfo.

**M3. Antes y después.** El mapa se parte en dos con una barra que se arrastra o se mueve con las flechas.
- **Paso 1 (con lo que ya hay):** a la izquierda, el NDVI del 22 mar 2026 (época seca); a la derecha, el del 14 sep 2026 (lluvias). Hace visible el hecho del suelo desnudo a escala de paisaje.
- **Paso 2 (capas nuevas):** la misma época en dos años, el compuesto de 16 días de fines de agosto de 2025 contra el de 2026, para ver la canícula de 2026. Se agregan las dos fechas a `CAPAS` en `pipeline/capas.py`. Antes de publicarlo hay que mirar las teselas: si las nubes o el compuesto no muestran diferencia, no se publica.
- **Rótulo:** «Paisaje de la zona a 250 m, no la parcela». En el paso 2 se agrega «2026: observación preliminar».
- **Implementación:** un recorte propio con `clip-path` sobre un panel de Leaflet y un `<input type="range">`. No se usa `leaflet-side-by-side`, que no tiene mantenimiento.
- **Peso:** 1 a 2 kB en Evidence. Las teselas nuevas pesarían algo parecido a las de hoy (las 3 capas guardadas suman 681 kB).
- **Esfuerzo:** M. **Sugerido:** Mario (teselas), Rodolfo (web).

**M4. Relieve sombreado.** Una capa de relieve sombreado hecha en Python desde el SRTM y guardada como teselas PNG (zoom 10 a 13 alrededor de las 5 parcelas), puesta sobre el mapa de hoy. Deja ver la ladera y la conecta con la pendiente que ya usa el puntaje de suelo.
- **Datos:** hay que bajar el modelo de elevación SRTM, GL1 (30 m) o GL3 (90 m), de LP DAAC con la cuenta de Earthdata que ya está en `.env`. Va en un cliente nuevo, `pipeline/clientes/srtm_dem.py`, con su procedencia. Los archivos `.hgt` son una malla de enteros que se lee con la biblioteca estándar y el sombreado se pinta con Pillow, que ya está en `requirements.txt`. No hace falta rasterio.
- **Peso:** nada de JavaScript. El peso de las teselas se mide; la meta es menos de 2 MB.
- **Esfuerzo:** M a L. **Sugerido:** Mario.

**M5. Vista 3D, con compuerta.** Un botón «Ver el relieve en 3D» en Evidence que carga MapLibre GL JS con `import()`, con teselas de elevación locales hechas desde el mismo SRTM. Solo entra si se cumplen las cuatro condiciones:
1. M4 ya está hecho.
2. `npm run build` mide el archivo nuevo y el equipo acepta su peso.
3. Funciona en el teléfono Android de prueba.
4. Si no hay WebGL o el teléfono está en modo ligero, el botón no aparece y queda M4.
- **Dependencia nueva:** `maplibre-gl`, aceptada por Rodolfo el 14 nov a condición de medirla primero. **Peso:** se mide con `npm run build` y se anota en `docs/peso.md` antes de unir la rama.
- **Esfuerzo:** L. **Sugerido:** Rodolfo.

### Gráficas (Evidence)

**G1. El agua del ciclo, acumulada.** Para cada rotación, la lluvia acumulada contra el agua que pide el cultivo (ETc de FAO-56, acumulada), desde la siembra de primera hasta la cosecha. Se marcan la franja de la canícula y la floración del maíz. El tramo donde la demanda supera a la lluvia va sombreado con textura, no solo con color. Un selector cambia entre el año típico (el del déficit mediano) y el año más seco de la parcela (`clima.anio_mas_seco`: 2018 en cuatro parcelas, 2002 en Olopa).
- **Datos:** los calcula el motor; `motor/clima.py` ya tiene `balance_ciclo` y `kc_dia`. Se exporta un punto cada 5 días para no engordar el JSON, en un bloque nuevo y opcional del contrato (`curva_agua`).
- **Se da por hecho cuando:** una prueba comprueba que el último punto de cada curva es igual a lo que devuelve `balance_ciclo` para ese año (la misma cifra que sostiene el puntaje) y el validador de números sigue en verde.
- **Peso:** unos 3 kB en Evidence y unos 5 a 8 kB más por cada JSON de parcela.
- **Esfuerzo:** M a L. **Sugerido:** Rodolfo (motor); Iván revisa las etapas del cultivo en `data/cultivos.yaml`.

**G2. La canícula día por día, 2001-2025.** Una franja por año (25 filas de 92 días, junio a agosto). Cada día seco (por debajo de `canicula.umbral_dia_seco_mm`) va pintado y las rachas de más de 15 días llevan borde grueso. Al tocar un año, la franja se agranda y se lee en texto. Un interruptor compara el reparto diario «sat» (IMERG, el que usa el motor) con «rnl» (ERA5), y así se ve por qué el color cambia en 3 de 5 parcelas ([sensibilidad-canicula.md](sensibilidad-canicula.md)).
- **Datos:** ya están en caché (`data/cache/chirps_diario/` y `chirps_diario_rnl/`). Python los exporta en forma compacta (los días secos de cada año como una cadena). 2026 no tiene datos diarios, solo los meses de julio y agosto, así que no entra en la franja.
- **Implementación:** un SVG propio, sin librería. La alternativa en texto es la lista de años con su racha más larga, que ya está en `canicula.por_anio`.
- **Se da por hecho cuando:** una prueba comprueba que la racha más larga de cada año en la franja es igual a `canicula.por_anio`.
- **Peso:** 3 a 4 kB en Evidence; unos 2 kB por parcela y por reparto.
- **Esfuerzo:** M. **Sugerido:** Rodolfo; Mario confirma que el umbral es el mismo del motor.

**G3. La nube de modelos.** En «Futuros de NASA», cada modelo CMIP6 es un punto: en el eje x va el cambio de lluvia y en el eje y el de temperatura. La forma y el relleno dicen si la rotación elegida mantiene su puntaje de agua en ese futuro: círculo lleno si aguanta, cruz si no. Hay un selector de rotación y otro de escenario (SSP2-4.5 o SSP5-8.5), y la mediana va marcada. Al tocar un punto sale el nombre del modelo.
- **Datos:** ya están (`futuros_nasa.json`, `modelos[]`). Se dibuja con el `ScatterChart` de Recharts, que ya viene con Evidence.
- **Alternativa en texto:** una tabla plegable de los modelos.
- **Peso:** unos 2 kB en Evidence. **Esfuerzo:** S a M. **Sugerido:** Rodolfo.
- Es candidato para antes del envío (sección 7).

**G4. 2026 contra otros años.** Barras de julio y de agosto con 2026, la mediana 1991-2025 y el año más seco de la parcela, y el rótulo «2026 es una observación preliminar y no entra en el puntaje».
- **Datos:** 2026 está en `data/cache/chirps_reciente/` y en `validacion.json`; los meses de cada año, en `data/cache/chirps/`. Se exportan 3 números por mes.
- **Esfuerzo:** S. **Sugerido:** Rodolfo.

**G5. Escenarios con transición.** Al cambiar la lluvia o la temperatura, los puntajes se mueven con una transición corta. Con movimiento reducido cambian sin animación.
- **Esfuerzo:** S.

### Vista del agricultor (primera pantalla)

**A1. La voz señala el hecho.** Mientras suena Escuchar, el hecho que nombra la voz (suelo, quema o canícula) se marca con un borde grueso y su pictograma crece un poco. Con movimiento reducido, solo el borde.
- **Datos:** los subtítulos ya van por frase y en orden fijo. El motor les pone identificador a las frases del `.vtt` (`suelo`, `quema`, `canicula`) para no depender del orden. Solo se regeneran los `.vtt`, con los tiempos que ya guarda cada mp3. Hay que confirmar que `motor.exportar` puede hacerlo sin volver a sintetizar la voz.
- **Archivos:** `motor/audio_frases.py`, `web/src/agricultor/Escuchar.jsx`, `agricultor.css`.
- **Peso:** nada en el JavaScript inicial, porque Escuchar llega después del primer pintado. Menos de 0.3 kB de CSS.
- **Se da por hecho cuando:** Playwright ve que, al pasar cada frase, la tarjeta correcta queda marcada; TalkBack no lee nada dos veces (los subtítulos ya se anuncian); y la prueba con personas dice si ayuda o distrae.
- **Esfuerzo:** S a M. **Sugerido:** Rodolfo; Mario revisa el audio.

**A2. Repetir una frase.** Debajo del reproductor van las frases como botones («Suelo», «Quema», «Canícula»): al tocar uno, el audio salta a esa frase. Unas barras de «está sonando» son solo decorativas (CSS, `aria-hidden`) y se quedan quietas con movimiento reducido. No se usa Web Audio ni Wavesurfer.js.
- **Peso:** nada en el JavaScript inicial. **Esfuerzo:** S.

**A3. Pictogramas que se mueven una vez.** Al aparecer, la hoja brota o el humo sube una sola vez y el dibujo termina igual que hoy, así que el estado final es el mismo de la fotocopia. No se anima en la hoja impresa ni con movimiento reducido. Va después de la prueba de comprensión de los pictogramas, no antes.
- **Peso:** solo CSS. **Esfuerzo:** S.

**A4. Tocar un hecho.** Abre una hoja con la rueda de 12 meses o los puntos de años en grande y una frase por año. Llega con `import()`. La prueba con personas decide si entra.
- **Esfuerzo:** M.

**A5. Sin señal, de verdad.** Un service worker propio, sin librería, que se registra desde un archivo que llega después del primer pintado. Guarda la página, los JSON de la parcela abierta, su audio corto con subtítulos y las capas del mapa. Un manifiesto permite «Agregar a la pantalla de inicio». La caché se nombra con el hash del build: al final del build se genera la lista de archivos, así un despliegue nuevo reemplaza lo viejo.
- **Se da por hecho cuando:** Playwright hace una primera visita con red y una segunda con la red cortada, y en la segunda abre la vista del agricultor, Escuchar suena y Evidence abre con la capa guardada. Además, `npm run sin-red` sigue en 23 de 23.
- **Peso:** nada en el JavaScript inicial. El service worker es un archivo aparte de unos 2 kB.
- **Esfuerzo:** M. **Sugerido:** Rodolfo.
- **Riesgo:** un service worker con la versión mal puesta deja a la gente con un sitio viejo. Por eso va en v2 y no en la entrega.

**A6. Modo ligero.** Si el teléfono pide ahorro de datos (`Save-Data` o `navigator.connection.saveData`) o no tiene WebGL, v2 no ofrece el 3D ni baja capas grandes por su cuenta. Un enlace «Versión ligera» lo activa a mano.
- **Esfuerzo:** S.

### Compartir

**K1. Imagen para WhatsApp.** El kit dibuja en un `canvas` una tarjeta con el nombre de la parcela, los tres hechos (forma, palabra y pictograma) y la línea «Verifíquelo con su extensionista». La comparte con el menú de compartir del teléfono (Web Share con archivo) o, si no se puede, la descarga. Las cifras salen solo del bloque `farmer`.
- **Archivos:** `web/src/kit/`. **Peso:** nada en el JavaScript inicial, porque el kit llega después.
- **Esfuerzo:** M. **Sugerido:** Rodolfo; Iván revisa los textos.

### Simulador (Evidence)

**S1. Probar otra rotación de la biblioteca.** El extensionista elige cualquiera de las plantillas que aplican a la parcela (maíz con canavalia, milpa completa, maíz con gandul, sorgo con caupí, maíz ICTA B-5…) y ve, al lado de la práctica actual, sus puntajes de agua, suelo y plagas, el déficit y el calendario de 12 meses. Se elige con botones, sin arrastrar y soltar.
- **Datos:** el motor ya evalúa todas las plantillas candidatas para elegir la mejor leguminosa y la mejor tolerante (`_evaluar` en `motor/recomendar.py`). Se exportan todas en un bloque nuevo y opcional (`biblioteca`). No hay cifras nuevas: nada de «probabilidad de soportar la canícula» ni de «ahorro de humedad».
- **Paso 2:** cuántos futuros aguanta cada plantilla. Pide correr `motor.futuros` con todas.
- **Se da por hecho cuando:** una prueba comprueba que el puntaje de cada plantilla en `biblioteca` es idéntico al que tiene cuando sale elegida en `rotaciones`.
- **Esfuerzo:** M. **Sugerido:** Rodolfo (motor y web); Iván (plantillas).
- **Riesgo:** más opciones van contra la idea de «tres opciones para conversar». Por eso S1 vive solo en Evidence, para el extensionista. La vista del agricultor sigue con tres.

### Documentos

- **D1.** Las filas de OpenET en [herramientas-existentes.md](herramientas-existentes.md) y [../existing-tools.md](../existing-tools.md) dicen ahora que OpenET es un referente para v2, no algo hecho. Listo en esta rama.
- **D2.** La investigación de competidores lleva al inicio el aviso de los equipos sin verificar. Queda como archivo local, fuera de git (`docs/es/investigacion-competidores.md`, excluido en `.git/info/exclude`), y no se sube a GitHub.
- **D3.** [../peso.md](../peso.md): una fila por cada fase de v2.
- **D4.** [../accessibility.md](../accessibility.md): cada control nuevo, con su alternativa.

## 6. Orden de trabajo

| Fase | Ítems | Por qué en este orden |
|---|---|---|
| 1 | M2, G3, M3 (paso 1), A1, A2, A5, A6 | Usan datos que ya existen. Sin dependencias nuevas. Del contrato solo cambian los identificadores de los `.vtt` |
| 2 | M1, G1, G2, G4, S1, K1, M3 (paso 2) | Piden cálculo nuevo en Python: los bloques opcionales `curva_agua` y `biblioteca`, y los archivos `huellas.json` y de la canícula diaria |
| 3 | M4, luego M5 con su compuerta; A3, A4 y G5 | M5 trae una dependencia nueva. A3 y A4 esperan la prueba con personas |

Cada fase cierra con la batería de la regla 7 y con una fila nueva en `docs/peso.md`.

**Carriles de v2.** Cada uno en su rama, que sale de `v2-interactiva`; Rodolfo las une:

| Carril | Rama | Ítems | Puede tocar |
|---|---|---|---|
| V2-A, motor | `v2-motor` | G1, G2, G4 y S1 (exportes), M1 (cálculo), A1 (identificadores de los `.vtt`) | `motor/`, `contracts/`, `tests/`, `web/public/data/`, `web/public/audio/*.vtt` |
| V2-B, mapa | `v2-mapa` | M1 (web), M2, M3, M4, M5 | `web/src/components/Mapa.jsx` y archivos nuevos en `web/src/components/mapa/`, `pipeline/capas.py`, `pipeline/clientes/` (cliente nuevo del SRTM), `web/public/capas/` |
| V2-C, gráficas | `v2-graficas` | G1 a G5 (web), S1 (web) | `web/src/components/` (salvo el mapa), `web/src/i18n/` |
| V2-D, agricultor | `v2-agricultor` | A1 a A6, K1 | `web/src/agricultor/`, `web/src/kit/`, el service worker y el manifiesto en `web/public/` |

- Archivos compartidos, como en [carriles.md](carriles.md): `App.jsx`, `main.jsx`, `package.json`, `smoke.mjs` y `sin-red.mjs`. Los integra Rodolfo.
- V2-A arranca primero: deja los bloques nuevos en el esquema y un JSON de ejemplo escrito a mano, como se hizo con el contrato v1. Así V2-C dibuja las gráficas sin esperar al motor.

## 7. Antes del envío (domingo 15 nov, 12:00)

v2 no tiene que estar lista para el envío. Para la versión lite hay dos opciones:

**Decidido: opción (a).** La versión lite es la de la entrega.

- **(a) Recomendada: no tocar el sitio.** Se termina solo lo que pide la entrega: el formulario, hacer público el repo y las pruebas con personas ([revision-plan.md](revision-plan.md)).
- **(b) Si sobra tiempo y Rodolfo lo decide:** G3 y M2 son solo de Evidence. No tocan la primera pantalla, el motor ni el contrato, y usan datos que ya están. Entrarían a `main` con la batería completa antes de las 10:00, para dejarle margen a Render (el CDN puede guardar un 404 hasta 300 s después de desplegar).

Si se quiere la fila de OpenET en los documentos de la entrega, se lleva con la redacción corregida de esta rama.

## 8. Pruebas nuevas

- **pytest:** huellas (M1), curva de agua que cierra con `balance_ciclo` (G1), canícula diaria igual a `canicula.por_anio` (G2), `biblioteca` igual a `rotaciones` (S1) y `.vtt` con identificadores (A1).
- **`npm run smoke`:** dibuja cada componente nuevo con cada JSON exportado.
- **`npm run sin-red`:** las capas nuevas vienen del sitio y el 3D no pide nada afuera.
- **Playwright:** el comparador con teclado, las huellas visibles, la frase activa marcada y el service worker sin red en la segunda visita.
- **Personas:** A1, A3, A4 y K1 con agricultores y con un extensionista, con las guías de [pruebas-personas/](pruebas-personas/README.md).

## 9. Riesgos

- **Lo vistoso se malinterpreta más fácil.** Un mapa en 3D o una imagen nítida pueden hacer creer que vemos la parcela. Por eso M1 va antes que M4 y M5, y cada capa dice su resolución.
- **Teléfonos de gama baja.** WebGL y capas grandes. Lo cubren A6 y la compuerta de M5.
- **Un service worker viejo.** Lo cubren la versión por hash y un aviso de «hay una versión nueva».
- **Cambios en el contrato.** Los bloques nuevos son opcionales; la versión lite no los lee y sigue funcionando con los JSON de v2.
- **El retiro de Terra.** Las capas MODIS de 2025 y 2026 ya existen en GIBS. Si Terra deja de publicar, las capas nuevas pasan a VIIRS, como ya dice el README para el NDVI.

## 10. Decisiones

Tomadas por Rodolfo el sábado 14 nov, en la noche:

1. La entrega es la versión lite, sin G3 ni M2 (sección 7).
2. v2 no entra a `main` hasta que se anuncien los ganadores globales (sección 1).
3. La investigación de competidores no se sube a GitHub. Las ramas `lite` y `v2-interactiva` sí se pueden subir cuando Rodolfo lo pida.
4. v2 se publica en un segundo sitio de Render, con las tres condiciones de la sección 1. Lo recomendado es crearlo cuando la fase 1 tenga algo que mostrar.
5. Se acepta `maplibre-gl` para M5 si primero se mide. Las otras condiciones de la compuerta siguen en pie.
6. S1 va solo en Evidence, para el extensionista; la vista del agricultor se queda con tres opciones (fue la recomendación de este plan).

No queda nada pendiente de decidir para arrancar la fase 1.
