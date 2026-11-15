# Revisión del plan contra el repo

> Lo que mejoraba el funcionamiento se aplicó: ver `docs/es/estado.md` y `docs/es/pruebas.md`.

En el repo desde el commit `5b60f57` (14 nov 2026). Solo revisión: en este turno no se cambió código. Esta revisión se conserva como referencia documental.

**Qué se comparó**
- **Plan final:** el plan aprobado de Fable está en el hilo de T3 «Plan: Milpa Resiliente (NASA Space Apps 2026)», ítem `proposed_plan`. No hay copia en `docs/`.
- **Fuente que manda según ese plan:** `docs/evaluacion-milpa-ajustada.txt`.
- **Plan original:** `docs/plan-original-sin-ajustes.md`.
- **Contrato JSON:** `contracts/recomendacion.schema.json` y `recomendacion.ejemplo.json`.
- **Estado del trabajo:** `docs/es/estado.md`, `docs/es/pruebas.md` y el repo en el commit `63356c7`.

**Orden que fijó Rodolfo**
1. Prueba en teléfono (sección 4).
2. Decisiones y ajustes (secciones 2 y 3, y la tabla).
3. Repo: hecho (Git local, commit `aaab0bb`, 14 nov 2026). Render y primer push: pendientes.
4. Al final: slides, video de 30 s y página en inglés.

## 1. Plan contra el repo

Estados: **Hecho**, **Parcial**, **Falta**, **Cortado** (cortado a propósito según la sección 7 del plan).

### Decisiones y estructura (plan, secciones 1 y 2)

| Ítem del plan | Estado | Evidencia | Qué falta exactamente |
|---|---|---|---|
| 1.1 Estático primero: 5 parcelas precalculadas; la web no necesita servidor ni claves | Hecho | `web/public/data/` (15 JSON de parcelas, el índice, la validación y el ejemplo), `web/public/audio/`, `web/public/capas/`, `render.yaml` | Pendiente: publicarlo |
| 1.2 Un solo motor en Python puro, sin red | Hecho | `motor/`, `tests/test_motor*.py` (71 pruebas pasan) | — |
| 1.3 Contrato JSON congelado | Hecho | `contracts/recomendacion.schema.json` y ejemplo (`38562ee`); `motor/contrato.py`; `tests/test_contrato.py` | Nada que bloquee. Después se agregaron campos opcionales (poca cobertura, POWER contra CHIRPS, `smap.anio_ultimo`) sin quitar ninguno, y el esquema no es estricto (`additionalProperties`), así que la forma sigue siendo compatible |
| 1.4 Caché dentro del repo con procedencia; red solo con `MILPA_ONLINE=1` | Hecho | `data/cache/*/` (cada archivo con URL, fecha y versión); `pipeline/cache.py` | — |
| 1.5 ZARC se cita, nunca se calcula | Hecho (adaptado) | `data/zarc_citas.yaml` (`registros: []` y referencia por departamento); `motor/zarc.py`; `tests/test_zarc.py` | ZARC no publica ventanas por municipio: hay que pedirlas a la DIGEGR del MAGA. Hoy la tarjeta remite al extensionista |
| 1.6 La IA redacta al construir, no en la demo, con validador de números | Hecho, sin LLM (corte 2) | `motor/redaccion.py` (plantillas y validador); `tests/test_redaccion.py` | — |
| 1.7 El satélite ve el patrón; la persona confirma el cultivo | Hecho | Selector de cultivo en la web (maíz con frijol, maíz solo, sorgo); `*.maiz_solo.json` y `*.sorgo.json` | — |
| 2 Lectura de CHIRPS con `rasterio` | Hecho, con otra herramienta | `pipeline/clientes/chirps.py` (lectura por rangos y decodificador LZW propio; no hizo falta `rasterio`) | — |
| 2 Tarjeta en PDF con estilos de impresión y `window.print()` | Hecho | `web/src/components/Tarjeta.jsx` («Imprimir o guardar PDF»); `@media print` en `styles.css` | Probarlo desde el teléfono (sección 4) |
| 2 Audio con edge-tts y voz del navegador de respaldo | Hecho | 5 mp3 con voz es-GT-MartaNeural, de ~72 s cada uno; la prueba de humo falla si falta uno | Decidir si 72 s es demasiado largo. El plan original pedía 45 s o menos; el final no fija tope |
| 2 Mapa con capas GIBS y respaldo sin red | Hecho | `web/public/capas/` (24 teselas: color real y NDVI); `web/src/components/Mapa.jsx` | El mapa base de OpenStreetMap necesita internet; sin red hay que usar la capa «Color real MODIS (sin red)» |
| 2 Despliegue en Render (sitio estático) | Hecho (14 nov 2026) | https://milpa-resiliente.onrender.com/ | Abrirla en un teléfono con datos móviles |
| 2 Estructura: `docs/guion-video.md` y `docs/project-page-en.md` | Falta | No existen | Guion del video y página en inglés (último bloque) |
| 2 API en vivo, extra | Cortado (corte 1) | `api/README.md` | Nada: queda como siguiente paso |

### Datos (plan, sección 3)

| Ítem del plan | Estado | Evidencia | Qué falta exactamente |
|---|---|---|---|
| NDVI MOD13Q1 por ORNL, 2001-2025, 5 parcelas, con calidad | Hecho | `data/cache/ndvi/`; `pipeline/clientes/ornl_ndvi.py` | — |
| FIRMS: histórico por país y reciente con MAP_KEY | Hecho | `data/cache/firms/`; FIRMS 2026 con la clave de `.env` (`2c1fbf8`) | — |
| SMAP SPL3SMP_E por AppEEARS, 2015-2026 | Parcial | `data/cache/smap/` (`63356c7`); 4 de 5 parcelas con dato | **Camotán sin SMAP:** su celda nunca tiene calidad recomendada. El plan preveía una segunda tarea con **SPL4SMGP** (zona de raíces, sin huecos) justo para este caso, y no se lanzó. Tarda horas en AppEEARS y es un producto de modelo con asimilación, así que habría que rotularlo como tal |
| NASA POWER mensual y diario | Hecho | `data/cache/power/` | — |
| CHIRPS como referencia de lluvia | Hecho, ampliado | v3 mensual 1991-2025 y v3 diario de junio a agosto 2001-2025 (`a02250c`) | Además de referencia, ya es la lluvia del motor (regla 5.1 del plan) |
| SoilGrids y SRTM | Hecho | `data/cache/suelo/` y `data/cache/srtm/`; respaldo WCS sin corrida real registrada | — |
| Capas GIBS | Hecho | `pipeline/capas.py` | — |
| Nombrar GPM/IMERG y ECOSTRESS (la evaluación pide subir la Relevancia) | Parcial | IMERG está en `data/glosario.yaml`, pero **no en `data/fuentes.yaml`**, aunque el CHIRPS diario 'sat' usa NASA IMERG. ECOSTRESS no aparece en el repo | Citar IMERG (GPM) en `fuentes.yaml`: NASA puede quitar premios por fuentes sin citar. Nombrar ECOSTRESS como siguiente paso en slides y página |

### Motor (plan, sección 4)

| Ítem del plan | Estado | Evidencia | Qué falta exactamente |
|---|---|---|---|
| 4.1 Entradas: cultivo, prioridad (agua, suelo, plagas) y 8 escenarios (lluvia 0/−10/−20/−30 % por temperatura 0/+1.5 °C) | Hecho | `escenarios.lista` con 8 combinaciones en cada JSON; `web/src/components/Controles.jsx` | — |
| 4.2 Detección: meses desnudos, ciclos, quemas a 500 m o menos, calidad del píxel | Hecho, con un añadido | `motor/deteccion.py` (`UMBRALES`); clase nueva «poca cobertura» (NDVI de 0.35 a 0.45) | Umbrales iniciales sin revisión agronómica (sección 3) |
| 4.3 ET0 de Hargreaves, déficit con 80 % de lluvia efectiva, canícula, SMAP y percentil | Hecho | `motor/clima.py` (`SUPUESTOS`); el día seco es de 2 mm, como prevé el plan si hay llovizna | — |
| 4.3 Puntajes de agua, suelo y plagas; pesos 50/25/25; selección de actual, leguminosa y tolerante | Hecho | `motor/puntaje.py` (`PESOS`, `PUNTOS`) | Revisión del agrónomo (sección 3) |
| 4.3 Trazabilidad de cada puntaje | Hecho | `trazabilidad` y `evidencia[]` con fuente, periodo y resolución | — |
| 5.2 → 4.5 «El sesgo POWER-CHIRPS ensancha el rango del déficit» | Falta | El rango que se muestra es el p25-p75 entre años (`motor/puntaje.py`); el sesgo solo entra en la confianza | Decidir si se implementa o se quita del relato. Ahora la lluvia del motor es CHIRPS, así que el sesgo de POWER pesa poco en el déficit |
| 4.4 ZARC (6 reglas, con prueba de fechas inventadas) | Hecho | `motor/zarc.py`, `tests/test_zarc.py` | Ver 1.5 |
| 4.5 Confianza alta, media o baja con motivo | Hecho | `motor/confianza.py`. Hoy: Jocotán y San Juan Ermita alta, Olopa media, Zacapa y Camotán baja | — |
| 4.6 Salidas del contrato; la exportación falla si falta uno de los 5 campos | Hecho | `motor/exportar.py` valida esquema y textos; claves del JSON: parcela, deteccion, clima, smap, rotaciones (con `calendario[12]`), zarc, escenarios, fuentes, glosario, aviso, texto_tarjeta y audio | — |

### Validación (plan, sección 5)

| Ítem del plan | Estado | Evidencia | Qué falta exactamente |
|---|---|---|---|
| 5.1 Sequía de 2018 | Hecho | `pipeline/validacion/validar.py`, `docs/validacion.md`, pestaña Validación | — |
| ↳ Métrica: puesto de 2018 y parcelas marcadas por el motor | Hecho | 2018 es el año 1 de 25 por déficit en las 5 parcelas; el motor lo marca en 5 de 5 | — |
| ↳ Métrica: aciertos y falsas alarmas en 2014, 2015, 2018 y 2019 | Hecho | `ANIOS_SECOS`; la muestra (n) está a la vista | — |
| ↳ Métrica: Spearman entre déficit y anomalía de NDVI | Hecho | De 0.07 (Olopa) a 0.86 (Zacapa), n = 20 | — |
| ↳ Evidencia: NDVI, SMAP e informe público | Hecho | FAO GIEWS (27 ago 2018) en `data/fuentes.yaml` | — |
| ↳ Regla fijada antes de ver el resultado | Hecho | No se activa: 5 parcelas con señal, mínimo 3 | — |
| 5.2 POWER contra CHIRPS en 5 municipios (tabla, dispersión y titular) | Hecho | `web/public/data/validacion.json`; `Validacion.jsx` | — |

### Calendario, hitos y equipo (plan, sección 6)

| Ítem del plan | Estado | Evidencia | Qué falta exactamente |
|---|---|---|---|
| Compuerta 0: leer los recursos oficiales de Field Shift y las guías de jueces y de entrega | **Falta, no consta** | Ni `docs/es/estado.md` ni el README la registran. Hoy no se pudieron abrir las páginas oficiales: error de certificado al leerlas | Que Rodolfo o Iván lean la Project Submission Guide y la Judging Guide en el navegador (pendiente) |
| **Inicio del trabajo y reglas del evento** | **Por confirmar con la organización** | Todos los commits de este repo son del 14 nov 2026 (`git log`): dicen cuándo entró cada cosa al repo, no cuándo se hizo | Confirmar las reglas con el organizador antes de publicar. Las fechas de la documentación son las de esos commits |
| H1-H4: datos, motor, 5 parcelas, validación y audio | Hecho | `2c1fbf8`, `a02250c`, `63356c7`; sitio publicado en https://milpa-resiliente.onrender.com/ | — |
| Reparto validado con Mario e Iván | Falta | Las tareas de datos y web las hizo el asistente | Pendiente: reunión de 15 min; cada quien revisa lo de su carpeta |
| Fuente de pérdidas de 2018 | Hecho | FAO GIEWS | — |
| Revisión con agrónomo o extensionista | Falta | `motor/puntaje.py` y `data/rotaciones.yaml` dicen «valores iniciales» | Ver sección 3 |

### Verificación de punta a punta (plan, sección 12)

| Ítem del plan | Estado | Evidencia | Qué falta exactamente |
|---|---|---|---|
| 12.1 Contrato: cada JSON contra el esquema | Hecho | `tests/test_contrato.py` | — |
| 12.2 Validador de números, con un número inventado a propósito | Hecho | `tests/test_redaccion.py` | — |
| 12.3 ZARC: fechas inventadas y caso sin registro | Hecho | `tests/test_zarc.py` | — |
| 12.4 Sin red: con el wifi apagado, la copia local abre todo, reproduce el audio e imprime | Hecho en la laptop | Datos, audio y capas son locales; `npm run sin-red` pasa 23 de 23 (14 nov 2026, `pruebas.md`) | Probarlo en un teléfono conectado a la laptop por la red local (`docs/es/prueba-telefono.md`) |
| 12.5 URL pública en incógnito y en teléfono con datos móviles | Parcial | https://milpa-resiliente.onrender.com/: 68 de 68 archivos responden y 24 de 24 comprobaciones en un navegador sin sesión, a 390 y 1366 px (14 nov 2026, 18:36; `pruebas.md`) | Abrirla en un teléfono real con datos móviles |
| 12.6 Trazabilidad: 3 cifras al azar de cada tarjeta encontradas en `data/cache/` | Falta | El validador asegura que los textos usan cifras del JSON, pero no coteja el JSON contra la caché | Mario o Rodolfo, unos 20 min |
| 12.7 Validación reproducible con un comando | Hecho | `python -m pipeline.validacion.validar` | Revisar que las slides usen esas mismas cifras |
| 12.8 Lista de entrega | Falta | — | Ver la tabla siguiente |

### Entregables del reto

Plan (sección 8), más las reglas de Space Apps que están en `docs/` y la [guía de entrega 2026](https://www.spaceappschallenge.org/resources/project-submission-guide/). La guía solo se pudo leer a través del buscador; hay que confirmarla en el sitio oficial.

| Entregable | Estado | Evidencia | Qué falta exactamente |
|---|---|---|---|
| Demo web en URL pública | Hecho (14 nov 2026) | https://milpa-resiliente.onrender.com/ | — |
| Repo público con README, licencia y fuentes | Hecho (15 nov 2026, tarde) | `README.md`, `LICENSE` (MIT), `data/fuentes.yaml` (38 fuentes, IMERG incluida), en `github.com/RodolfoXiloj/app-nasa-space-2026`. Antes de abrirlo se revisó que el historial no tiene claves ni la investigación de competidores | — |
| Validación publicada | Hecho | Pestaña Validación del sitio publicado (https://milpa-resiliente.onrender.com/) y `docs/validacion.md` | — |
| **Video de 30 s o menos**, o **slides de 7 o menos** contando la portada | Hecho: slides y video | `docs/slides/index.html` y `docs/slides/milpa-resiliente.pdf`: 7 diapositivas en inglés; `tests/test_slides.py` falla si pasan de 7. El video final dura 29.9 s y no está en el repo | Subir el video a YouTube y poner su enlace en el formulario |
| Archivos alojados fuera y enlace que abra sin iniciar sesión | Hecho para las slides (15 nov 2026) | El PDF de las slides en GitHub (`app-nasa-space-2026`, `docs/slides/milpa-resiliente.pdf`) responde sin sesión, y el sitio en https://milpa-resiliente.onrender.com/ | Abrir el enlace del video en una ventana privada cuando esté subido |
| Página del proyecto en inglés | Falta | — | `docs/project-page-en.md` como borrador; Rodolfo revisa la parte técnica |
| Uso de IA (Super Intelligence) declarado | Parcial | `docs/es/uso-ia.md` | Que cada integrante anote lo suyo; incluirlo en la página y en la última slide |
| Citar cada fuente usada | Parcial | `data/fuentes.yaml` y la pestaña «Glosario y fuentes» | Falta IMERG (GPM) |
| Aviso de que apoya y no reemplaza al técnico | Hecho | Campo `aviso` del JSON y tarjeta | — |
| Formulario enviado por el dueño del equipo, con una segunda persona revisando | Por confirmar | — | Según la página oficial de 2026, el envío cierra el **domingo 15 nov a las 11:59 PM, hora local**, y manda la hora en que termina el evento local. Este plan decía 12:00 |

## 2. Decisión 2026: ¿mostrar que julio-agosto 2026 fue el más seco del registro?

### Qué dicen nuestros datos (consultados el 14 nov 2026)

- **CHIRPS v3 mensual:** julio y agosto de 2026 suman entre 44 mm (Zacapa) y 106 mm (Olopa), entre 20 % y 26 % de la mediana de 1991-2025. Es la menor suma de 1991-2026 en las 5 parcelas: cerca de la mitad del mínimo anterior, que fue 2018 (en Olopa, 1997).
- **SMAP (SPL3SMP_E):** la humedad de julio-agosto 2026 es la más baja de los 12 años con dato en las 3 celdas de 9 km que tienen SMAP (4 parcelas). Con 12 años no se da percentil.

### Qué dicen los reportes públicos

| Fuente | Qué dice | Verificado en la página original |
|---|---|---|
| [FEWS NET, actualización de agosto 2026](https://fews.net/es/latin-america-and-caribbean/guatemala/actualizacion-de-la-perspectiva-de-seguridad-alimentaria/agosto-2026), información al 31 ago 2026 | «el Corredor Seco recibió entre el 5 y el 25 por ciento de las lluvias en comparación con los valores normales»; «de 11 a 20 días consecutivos sin lluvias» entre el 10 jul y el 10 ago; «pérdidas de más del 50 por ciento y hasta totales para los agricultores de subsistencia». Nombra a Chiquimula solo por la asistencia, no a Zacapa | Sí |
| [Prensa Libre, 1 sep 2026](https://www.prensalibre.com/guatemala/comunitario/sequia-golpea-el-maiz-estudio-documenta-graves-perdidas-en-36-mil-hogares-del-corredor-seco/) (estudio de Oxfam, Acción contra el Hambre y socios) | «36 mil 431 hogares reportan serios daños en sus cosechas de maíz»; «ocho de cada 10 perdieron entre tres cuartas partes y la totalidad»; en Chiquimula y Jalapa «menos del 3% de las plantaciones se lograron»; «En Chiquimula, por ejemplo, el déficit llegó al 75%» (julio) | Sí |
| [Canal Antigua, 25 sep 2026](https://canalantigua.tv/2026/09/25/sequia-persiste-pese-a-alivio-temporal-de-lluvias-113-mil-familias-siguen-afectadas-en-chiquimula-y-jutiapa/) | «113 mil 825 familias afectadas» en «15 municipios de Chiquimula y Jutiapa, bajo alerta roja por la sequía»; el Ejecutivo prevé asistir a «1 millón 212 mil 178 familias entre septiembre y diciembre» | Sí |
| [Oxfam, Evaluación rápida El Niño 2026 (PDF)](https://lac.oxfam.org/wp-content/uploads/2026/08/Informe-CA-Fenomeno-de-El-Nino.pdf) | Según la prensa: 354 comunidades de Guatemala, Honduras y El Salvador evaluadas; 78.6 % de los hogares con maíz perdió de 75 % a 100 % | No: el PDF bajó, pero no se pudo leer |
| [Infobae, 2 sep 2026](https://www.infobae.com/guatemala/2026/09/02/el-nino-2026-en-guatemala-caniculas-largas-maiz-perdido-casi-por-completo-y-el-temor-a-una-hambre-estacional-en-el-corredor-seco/) y [17 sep 2026](https://www.infobae.com/guatemala/2026/09/17/guatemala-implementara-un-plan-de-emergencia-y-preve-asistencia-para-1-millon-212-mil-178-familias-hasta-diciembre/) | El Niño 2026, canículas largas, pérdidas de maíz; plan de emergencia | No (solo el resumen del buscador) |
| [OCHA, El Niño 2026-2027, septiembre 2026](https://www.unocha.org/publications/report/guatemala/el-nino-2026-2027-climate-risk-humanitarian-outlook-latin-america-and-caribbean-september-2026) | Panorama regional; pérdidas de primera | No (error 403) |
| [ReliefWeb, marco de acción anticipatoria por sequía 2026](https://reliefweb.int/report/guatemala/guatemala-anticipatory-action-framework-drought-2026-guatemala-marco-de-accion-anticipatoria-sequia-2026-enes) | Según el buscador, prioriza Chiquimula, Zacapa, Jalapa y El Progreso | No (error 403) |
| [MAGA, análisis agroclimático de agosto a octubre de 2026 (PDF)](https://www.maga.gob.gt/download/informe9-26.pdf) | Citado en la evaluación (`docs/evaluacion-milpa-ajustada.txt`) | No (error 403) |
| [AGN: alerta naranja de la Codred de Zacapa, 29 sep 2026](https://agn.gt/?p=573643) | Según el buscador, alerta por sequía y pérdidas | No: el enlace abre un listado de noticias sin la nota |

**Zacapa:** ninguna fuente verificada nombra a Zacapa con cifras de pérdida de 2026. Chiquimula sí aparece (Prensa Libre y Canal Antigua).

### Pros y contras ante el jurado

**A favor**
- **Impacto y relevancia:** conecta la herramienta con lo que pasó este año en el Corredor Seco, el lugar del proyecto.
- **Validez:** dos fuentes satelitales independientes (CHIRPS y SMAP) coinciden entre sí, y FEWS NET y la prensa local las confirman (5 % a 25 % de la lluvia normal; pérdidas de más de 50 %). Es la misma lógica que la prueba de 2018, aplicada a un año que el jurado recuerda.
- **Narrativa:** «la canícula de 2026 fue la más seca en 36 años según CHIRPS; esto es lo que la herramienta ayuda a anticipar». Es una frase que el juez puede repetir.

**En contra y riesgos**
- **Dato preliminar:** CHIRPS reciente puede revisarse cuando entran más estaciones. No se comprobó si los meses de 2026 bajados son versión final o preliminar. SMAP también puede reprocesarse.
- **Registro corto:** «el más bajo de SMAP» se apoya en solo 12 años (2015-2026).
- **Huecos:** Camotán no tiene SMAP, y Jocotán y San Juan Ermita comparten celda.
- **Inconsistencia aparente:** el motor y la validación usan 2001-2025, así que las recomendaciones no incorporan 2026. Un juez puede preguntar por qué la herramienta «no lo ve». Hay que decirlo explícitamente.
- **Riesgo de exagerar:** las cifras de pérdidas son de encuestas y prensa, no de la herramienta. No se pueden presentar como resultado propio.
- **Riesgo de último minuto:** agregarlo toca la web el día de la entrega. Debe ser una pieza aislada que no cambie puntajes ni confianza.

### Recomendación: **sí, como «observación preliminar» aparte**

Mostrarlo, pero sin tocar el motor:

1. **Dónde:** una tarjeta en la pestaña Validación, debajo de 2018, con el título «Observación preliminar: julio-agosto 2026». No se usa la palabra «alerta». No va en la tarjeta del agricultor, ni en el audio, ni en los puntajes.
2. **Qué dice:** los dos datos propios (CHIRPS de 20 % a 26 % de lo normal y SMAP en el mínimo de 12 años), la fecha de consulta, una línea «dato preliminar, puede cambiar» y «el motor usa 2001-2025; 2026 no entra en sus cálculos».
3. **Fuentes enlazadas:** FEWS NET y Prensa Libre como mínimo, las dos verificadas.
4. **Cómo se hace:** un JSON generado por el pipeline, para que el validador de números revise las cifras; no texto escrito a mano. Va con una prueba y una fila en `pruebas.md`.
5. **En slides y página:** una sola línea en la lámina de validación.

Texto propuesto:

> **Observación preliminar: julio-agosto 2026.** Según CHIRPS v3 (consultado el 14 nov 2026), en julio y agosto de 2026 llovió entre el 20 % y el 26 % de lo normal en las 5 parcelas: lo menos desde 1991. SMAP registra la humedad del suelo más baja de sus 12 años en 3 de 3 celdas con dato. FEWS NET reportó para el Corredor Seco entre 5 % y 25 % de la lluvia normal y pérdidas de más de 50 % para agricultores de subsistencia. Dato preliminar: CHIRPS y SMAP recientes pueden revisarse. El motor usa 2001-2025; 2026 no entra en sus cálculos.

En inglés: *Preliminary observation, not a forecast: July-August 2026. CHIRPS v3 (accessed 14 Nov 2026) shows 20-26 % of normal rainfall at the 5 plots, the lowest since 1991; SMAP shows the lowest soil moisture in its 12-year record in 3 of 3 cells with data. FEWS NET reported 5-25 % of normal rainfall in the Dry Corridor and losses above 50 % for subsistence farmers. Preliminary data, subject to revision; the engine uses 2001-2025.*

## 3. Qué significa cada pendiente humano

### 3.1 «Confirmar los 5 puntos en campo»

**En simple:** los 5 puntos se eligieron desde el satélite. NDVI de MODIS: un píxel de 250 m × 250 m que en verano está seco y en invierno verde. Después se miraron a ojo en una imagen Sentinel-2 de 2021. Confirmar quiere decir que alguien que conoce el lugar diga: «sí, ese cuadro es milpa (o frijol, o sorgo), está en tal municipio, y así se usa». Si no se confirma, la demo sigue funcionando, pero la tarjeta debe decir «punto de ejemplo, no verificado en campo».

**Qué verificar en cada parcela**
1. **Uso del suelo:** el punto cae en tierra de cultivo, y no en bosque, guamil, potrero, café, casas o río.
2. **Homogeneidad:** el cuadro de 250 m alrededor del punto es casi todo cultivo, porque MODIS promedia todo lo que hay en ese cuadro.
3. **Qué se sembró** en 2024, 2025 y 2026, en primera y en postrera. ¿Hubo quema? ¿Qué meses queda el suelo pelado?
4. **Que coincida con el satélite.** Esto es lo que debe confirmar la persona:

| Parcela | Satélite: suelo desnudo · poca cobertura · ciclos al año · quemas cercanas |
|---|---|
| Jocotán | mar-abr · feb y may · 1 · 3 de 15 años |
| Camotán | ninguno · mar-abr · 1 · 3 de 15 años |
| Cerca de Olopa | ninguno · mar-abr · 1 · 1 de 15 años |
| San Juan Ermita | feb-abr · ene y may · 2 · 2 de 15 años |
| Zacapa | abr · ene-mar y may · 1 · 0 de 15 años |

5. **Municipio correcto:**
   - Olopa: puede caer en Esquipulas.
   - San Juan Ermita: puede caer en Jocotán.
   - Zacapa: hay que confirmar que no sea bosque seco.
6. **Pendiente:** plano, ladera suave o ladera fuerte.

**Con quién:**
- un extensionista del MAGA (agencia municipal de extensión) de Chiquimula o Zacapa;
- un técnico de una organización que trabaje en la zona;
- o un agricultor o agricultora de la aldea.

**Qué traer, por parcela, sin datos personales:**
- La coordenada del teléfono parado en el punto: captura de Google Maps con el punto azul, o la coordenada copiada.
- 4 fotos desde el punto (norte, este, sur, oeste) y 1 foto del suelo, con fecha.
- Las respuestas a los puntos 3 a 6.
- Permiso para usar las fotos en la presentación.

**¿Se puede hacer a distancia?** Sí, pero a nivel de «verosímil», no de «confirmado»:
- **Google Maps o Earth, vista satélite:** permite ver si el cuadro son parcelas abiertas. En Google Earth Pro, las imágenes históricas sirven para comparar la época seca con la de lluvia. Street View casi no cubre esas aldeas.
- **Límites municipales:** Google Maps muestra el contorno del municipio al buscarlo, aunque no es un dato oficial. El dato oficial son los límites del INE o de SEGEPLAN.
- **Contacto local por WhatsApp:** mandarle el enlace del punto y pedirle una descripción o fotos. Es lo más rápido antes del domingo.

**Enlaces de los puntos:**
- [Jocotán](https://www.google.com/maps?q=14.81146,-89.39433&t=k)
- [Camotán](https://www.google.com/maps?q=14.86146,-89.37404&t=k)
- [Cerca de Olopa](https://www.google.com/maps?q=14.66563,-89.29358&t=k)
- [San Juan Ermita](https://www.google.com/maps?q=14.78646,-89.42065&t=k)
- [Zacapa](https://www.google.com/maps?q=14.94062,-89.56&t=k)

**Checklist (por parcela)**
- [ ] Vista satélite de Google Maps: el cuadro de ~250 m alrededor del pin es mayormente parcelas abiertas
- [ ] Municipio confirmado (Olopa contra Esquipulas; San Juan Ermita contra Jocotán)
- [ ] Contacto local identificado (extensionista, técnico o agricultor)
- [ ] Uso del suelo confirmado: milpa, frijol, sorgo u otro
- [ ] Qué se sembró en 2024, 2025 y 2026, en primera y postrera
- [ ] ¿Coinciden con el satélite los meses desnudos, los ciclos por año y las quemas?
- [ ] Pendiente: plano, ladera suave o ladera fuerte
- [ ] Coordenada del teléfono y 5 fotos con fecha, con permiso de uso
- [ ] Resultado anotado en `docs/es/estado.md` (sección «Decisiones») y en `data/parcelas.yaml`: confirmado, verosímil a distancia, o mover el punto
- [ ] Si no se confirma: la tarjeta y la página dicen «punto de ejemplo, no verificado en campo»

### 3.2 «Que un agrónomo revise las reglas de puntaje y las 8 plantillas»

**En simple:** el motor da puntos de 0 a 100 en agua, suelo y plagas con reglas que escribimos nosotros: «valores iniciales». Los Kc y Ky salen de la FAO y las plantillas de ICTA, MAGA, CIMMYT y FAO, pero ningún agrónomo ha revisado cómo se combinan. Revisarlas es pedirle a alguien que conoce el Corredor Seco que diga «esto tiene sentido» o «esto está mal», en unos 30 minutos.

**Dónde están las reglas**

| Qué | Archivo | Valores actuales |
|---|---|---|
| **Pesos según la prioridad** | `motor/puntaje.py` → `PESOS` | 50 % al criterio elegido y 25 % a cada uno de los otros dos |
| **Agua** | `motor/puntaje.py` → `PUNTOS` | 100 × (1 − pérdida esperada), con pérdida = Ky × déficit (FAO-33), menos hasta 20 puntos por canícula larga |
| **Suelo** | `motor/puntaje.py` → `PUNTOS` | Parte de 100. Resta 6 por mes desnudo y 3 por mes de poca cobertura, ×1.5 si la pendiente pasa de 15 %. Resta hasta 30 por quema. Suma 5 por leguminosa, 10 por cobertura y 10 por rastrojo en pie |
| **Plagas** | `motor/puntaje.py` → `PUNTOS` | Base 40. Suma 30 si alterna familias, 10 por asociación y 10 por cobertura. Resta 20 por monocultivo |
| **Detección** | `motor/deteccion.py` → `UMBRALES` | Suelo desnudo: NDVI < 0.35. Poca cobertura: de 0.35 a 0.45. Un ciclo es un pico de NDVI con prominencia de 0.15 o más. Quema cercana: a 500 m o menos, de enero a mayo |
| **Agua del suelo** | `motor/clima.py` → `SUPUESTOS` | Lluvia efectiva de 80 %; reserva de 50 mm; ET0 de Hargreaves. Canícula: racha seca de más de 15 días con menos de 2 mm por día, entre el 15 jun y el 31 ago |
| **Cultivos** | `data/cultivos.yaml` | Maíz de 125 días; ICTA B-5 de 90; sorgo de 100; frijol de postrera de 80 (supuesto); caupí de 75 (supuesto, sin Ky). Canavalia, ayote y gandul sin Kc |
| **Fechas del modelo** | `data/rotaciones.yaml` → `siembra_mes` y `siembra_dia` | Primera el 25 de mayo y postrera el 15 de septiembre. Son supuestos para simular el agua, **no** una recomendación: la fecha se cita de ZARC |

**Las 8 plantillas** (`data/rotaciones.yaml`)

| Id | Tipo | Qué es |
|---|---|---|
| `actual_maiz_frijol` | actual | Maíz con frijol en primera y frijol en postrera |
| `actual_maiz_solo` | actual | Maíz solo en primera (supuesto inicial) |
| `actual_sorgo` | actual | Sorgo (maicillo) en primera |
| `leguminosa_canavalia` | leguminosa o cobertura | Maíz con canavalia en primera, frijol en postrera y rastrojo en pie |
| `leguminosa_milpa` | leguminosa o cobertura | Milpa completa (maíz, frijol y ayote) en primera, frijol en postrera y rastrojo en pie |
| `leguminosa_gandul` | leguminosa o cobertura | Maíz con gandul; el gandul sigue verde en la época seca |
| `tolerante_sorgo_caupi` | tolerante a sequía | Sorgo en primera y caupí en postrera, con rastrojo en pie |
| `tolerante_maiz_corto` | tolerante a sequía | Maíz de ciclo corto ICTA B-5 con frijol en primera y frijol en postrera |

Cada plantilla trae `beneficios`, `vacios`, `riesgos` y `fuente`, que el agrónomo puede leer directamente en la web (pestaña Parcela, comparación de rotaciones).

**Preguntas concretas para el agrónomo**
1. ¿Las 3 rotaciones «actuales» describen lo que de verdad se siembra en Jocotán, Camotán, Olopa, San Juan Ermita y Zacapa? ¿Falta alguna común?
2. **Canavalia** asociada al maíz en primera, en ladera del Corredor Seco: ¿es realista? ¿Compite con el maíz? ¿Hay riesgos para animales si se usa como forraje?
3. **Milpa con ayote** y **maíz con gandul**: ¿se usan en la zona? ¿El gandul tiene consumo o mercado local?
4. **Sorgo con caupí en postrera:** ¿se conoce el caupí en la zona, o conviene frijol tepary u otra leguminosa?
5. **ICTA B-5:** ¿se consigue la semilla en Chiquimula y Zacapa? ¿Hay una variedad más adecuada en 2026?
6. **Duraciones:** ¿80 días para el frijol de postrera y 75 para el caupí son razonables? ¿Las fechas de siembra del modelo (25 mayo y 15 septiembre) son típicas?
7. **Pesos y puntos:** ¿el reparto 50/25/25 es razonable? ¿Restar 6 por mes desnudo y hasta 30 por quema, y sumar 30 por alternar familias, ordena bien las opciones? ¿Hay alguna que no debería quedar arriba?
8. **Umbrales:** ¿una canícula «larga» de más de 15 días secos con menos de 2 mm por día coincide con lo que ven los agricultores?
9. **Riesgos y vacíos:** ¿falta algún riesgo importante en el texto de cada plantilla? ¿Alguna recomendación podría causar daño, por ejemplo en ladera sin obras de conservación?
10. **Lenguaje:** ¿un agricultor entiende la tarjeta y el audio? ¿Qué palabra cambiaría?

**Checklist**
- [ ] Agrónomo o extensionista identificado (MAGA, ICTA, CUNORI-USAC en Chiquimula u ONG de la zona); anotar su nombre y rol con su permiso
- [ ] Enviarle la web, más la tarjeta impresa en PDF de Jocotán y de Zacapa, más este resumen
- [ ] 30 min: preguntas 1 a 10
- [ ] Respuestas anotadas, con fecha, en una nota nueva (por ejemplo `docs/es/revision-agronomica.md`)
- [ ] Cambios acordados aplicados en `motor/puntaje.py`, `data/rotaciones.yaml` y `data/cultivos.yaml`, con pruebas, validación y exportación de nuevo
- [ ] Si no se logra antes del domingo: la web y la página ya dicen «Reglas de la opción sin revisar por un agrónomo»; dejarlo así y mencionarlo en las slides

## 4. Prueba en teléfono real (hoy)

**Levantar la web en la red local** (PowerShell, en la laptop):

```powershell
cd web
npm run build
npx vite preview --host 0.0.0.0 --port 4173 --strictPort
```

**URL para el teléfono:** **http://192.168.0.17:4173/**
- IP anotada en el plan, sin comprobar (la hora 20:50 era planeada). Usar la línea `Network: http://192.168.x.x:4173/` que imprime Vite. No usar las de `169.254…` ni `172.22…`.
- El teléfono debe estar en **la misma red Wi-Fi** que la laptop.
- Si Windows pregunta, **permitir Node.js en redes privadas**. Si no abre, revisar que el perfil de esa red Wi-Fi sea «Privada».
- Para detenerla: `Ctrl+C`.

**Sin corrida real registrada** (la hora 20:49 que figuraba era planeada). Lo que hay que comprobar desde la laptop, contra su IP local:

| Qué | Resultado esperado |
|---|---|
| Página | 200 |
| `data/jocotan.json` | 200, `application/json` |
| `audio/jocotan.mp3` | 200, `audio/mpeg`; responde a pedidos por rango (206), que el iPhone necesita para reproducir |
| `capas/capas.json` | 200 |

Falta comprobar el firewall desde otro equipo.

**Qué revisar en el teléfono** (anotar modelo, navegador, y una captura de lo que falle)
- [ ] **Carga:** abre en pocos segundos; el selector muestra las 5 parcelas; cambiar de parcela funciona.
- [ ] **Mapa:**
  - [ ] se ve el mapa base (OpenStreetMap necesita internet);
  - [ ] zoom con dos dedos;
  - [ ] se ve el círculo de la parcela, con su color de confianza;
  - [ ] en el control de capas cargan «Color real MODIS (sin red)», «NDVI época seca» y «NDVI época de lluvia».
- [ ] **Controles:** cultivo, prioridad, lluvia y temperatura cambian los puntajes.
- [ ] **Audio mp3** (tarjeta):
  - [ ] se reproduce y se pausa;
  - [ ] se oye claro con el volumen de medios subido;
  - [ ] dura ~72 s: ¿es demasiado largo para el agricultor?;
  - [ ] en Camotán dice que SMAP no tiene mediciones de buena calidad.
- [ ] **Imprimir o guardar PDF:**
  - Android: Chrome → Compartir → Imprimir → Guardar como PDF.
  - iPhone: Compartir → Imprimir.
  - ¿La tarjeta queda legible en una página?
- [ ] **Pestaña Validación:** las tablas se desplazan dentro de su cuadro, sin mover la página de lado; la gráfica se ve.
- [ ] **Glosario y fuentes:** los enlaces abren.
- [ ] **Teléfono en horizontal:** nada se corta.
- [ ] **Uso:** el texto se lee sin hacer zoom y los botones se tocan sin errores.
- [ ] **Modo sin conexión:**
  - **No aplica en el teléfono:** la web no tiene modo sin conexión (no hay *service worker*). Si se corta el Wi-Fi, lo ya abierto sigue visible, pero no carga parcelas nuevas.
  - La prueba sin red del plan (12.4) se hace **en la laptop:** apagar el Wi-Fi de la laptop, correr `npx vite preview` y abrir `http://localhost:4173/`. Revisar que abran las 5 parcelas, que suene el audio y que se pueda imprimir. El mapa base no carga; se usa «Color real MODIS (sin red)».

Después de la prueba, sus resultados se anotan en `docs/es/pruebas.md`. La prueba con **datos móviles** queda pendiente, con la URL de Render (plan, 12.5).
