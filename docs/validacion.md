# Validación de Milpa Resiliente

Generado por `python -m pipeline.validacion.validar` el 2026-11-14T22:51:45Z (UTC). **No editar a mano:** se regenera desde `data/cache/` y da las mismas cifras que la pestaña Validación de la web.

## Regla fijada antes de ver el resultado

No se ajustan umbrales para que 2018 salga bien. Si ninguna señal (motor, NDVI o SMAP) muestra 2018 en 3 o más parcelas, se publica así y la confianza de las recomendaciones de agua baja a «baja».

**Resultado:** 5 parcelas con señal; la regla no se activa. Ninguno.

## 5.2 Lluvia de NASA POWER contra CHIRPS

En julio-agosto, NASA POWER se desvía 4.6 % de CHIRPS en Jocotán (error medio de 45.7 mm/mes, r = 0.74, n = 50 meses, 2001-2025).

| Parcela | Píxel CHIRPS | Todo el año 2001-2025: POWER / CHIRPS (mm/mes) | Sesgo | Julio-agosto: sesgo · error medio · r · n | Sesgo 1991-2000 |
|---|---|---|---|---|---|
| Jocotán | 14.825, -89.375 | 126.6 / 100.6 | +25.8 % | +4.6 % · 45.7 mm · 0.74 · 50 | -20.7 % |
| Camotán | 14.875, -89.375 | 126.6 / 111.5 | +13.5 % | -5.8 % · 49.3 mm · 0.74 · 50 | -27.9 % |
| Olopa | 14.675, -89.275 | 114.8 / 129.6 | -11.4 % | -22.1 % · 64.6 mm · 0.71 · 50 | -44.3 % |
| San Juan Ermita | 14.775, -89.425 | 126.6 / 96.9 | +30.6 % | +2.6 % · 47.3 mm · 0.72 · 50 | -17.2 % |
| Zacapa | 14.925, -89.575 | 126.6 / 71.0 | +78.2 % | +55.4 % · 69.2 mm · 0.7 · 50 | +17.3 % |

## 5.1 La sequía de 2018

El motor, con lo que se sabía hasta 2017, marca 2018 como riesgo alto en 5 de 5 parcelas; alguna señal (motor, NDVI o SMAP) lo muestra en 5.

Riesgo alto = déficit del año mayor que el percentil 75 de los años anteriores (desde 2001), con la lluvia de CHIRPS. Años secos conocidos: 2014, 2015, 2018, 2019.

| Parcela | Puesto de 2018 (déficit) | Motor marca 2018 | NDVI jul-sep 2018 | SMAP jul-ago 2018 | Aciertos · falsas alarmas · fallos (n) | Spearman déficit vs NDVI (n) |
|---|---|---|---|---|---|---|
| Jocotán | 1 de 25 | sí | -2.35 DE | -0.67 DE | 3 · 2 · 1 (20) | +0.69 (20) |
| Camotán | 1 de 25 | sí | +0.14 DE | — DE | 3 · 2 · 1 (20) | +0.45 (20) |
| Olopa | 1 de 25 | sí | -0.14 DE | -1.06 DE | 3 · 3 · 1 (20) | +0.07 (20) |
| San Juan Ermita | 1 de 25 | sí | -1.13 DE | -0.67 DE | 3 · 3 · 1 (20) | +0.45 (20) |
| Zacapa | 1 de 25 | sí | -1.72 DE | -0.98 DE | 3 · 2 · 1 (20) | +0.86 (20) |

### Aciertos y fallos contra los años con pérdidas documentadas

La columna «Aciertos · falsas alarmas · fallos» de arriba cuenta contra los cuatro años secos listados antes de la prueba (2014, 2015, 2018 y 2019). Aquí se cuenta contra una lista más larga: 7 años con pérdidas de cosecha documentadas en fuentes públicas. La regla y los umbrales son los mismos; no se volvió a correr ni se ajustó nada.

| Parcela | Años marcados como riesgo alto | Aciertos | Falsas alarmas | Fallos |
|---|---|---|---|---|
| Jocotán | 2009, 2014, 2015, 2018, 2025 | 3 (2009, 2015, 2018) | 2 (2014, 2025) | 4 (2010, 2016, 2019, 2023) |
| Camotán | 2009, 2014, 2015, 2018, 2025 | 3 (2009, 2015, 2018) | 2 (2014, 2025) | 4 (2010, 2016, 2019, 2023) |
| Olopa | 2010, 2014, 2015, 2018, 2021, 2025 | 3 (2010, 2015, 2018) | 3 (2014, 2021, 2025) | 4 (2009, 2016, 2019, 2023) |
| San Juan Ermita | 2009, 2010, 2014, 2015, 2018, 2025 | 4 (2009, 2010, 2015, 2018) | 2 (2014, 2025) | 3 (2016, 2019, 2023) |
| Zacapa | 2009, 2014, 2015, 2018, 2025 | 3 (2009, 2015, 2018) | 2 (2014, 2025) | 4 (2010, 2016, 2019, 2023) |

El motor no marca 2016, 2019 ni 2023 en ninguna parcela.

Los años con pérdidas documentadas:

| Año | Qué documenta la fuente | Ámbito | Fuente |
|---|---|---|---|
| 2009 | Chiquimula perdió 30 642 de 38 201 manzanas de maíz | Departamento de Chiquimula | FAO/PMA (2010): evaluación de cosecha y seguridad alimentaria en Guatemala, https://www.fao.org/4/ak344s/ak344s00.htm |
| 2010 | Pérdidas parciales o totales de maíz y frijol (pérdidas documentadas; la causa no está en nuestras notas) | Comunidades ch'orti' de Camotán, Jocotán y Olopa | FAO: perfil de las comunidades ch'orti', https://openknowledge.fao.org/server/api/core/bitstreams/b4f735d8-7008-423c-b28a-300ab920c241/content/src/html/sec8_1.html |
| 2015 | Pérdidas parciales o totales de maíz y frijol | Comunidades ch'orti' de Camotán, Jocotán y Olopa | FAO: perfil de las comunidades ch'orti', https://openknowledge.fao.org/server/api/core/bitstreams/b4f735d8-7008-423c-b28a-300ab920c241/content/src/html/sec8_1.html |
| 2016 | Pérdidas parciales o totales de maíz y frijol | Comunidades ch'orti' de Camotán, Jocotán y Olopa | FAO: perfil de las comunidades ch'orti', https://openknowledge.fao.org/server/api/core/bitstreams/b4f735d8-7008-423c-b28a-300ab920c241/content/src/html/sec8_1.html |
| 2018 | Estimación preliminar del MAGA de 175 126 ha de pérdidas de cultivos, sobre todo maíz y frijol, y 1 290 785 personas afectadas, al 13 de agosto de 2018; también pérdidas parciales o totales en las comunidades ch'orti' | Guatemala; comunidades ch'orti' de Camotán, Jocotán y Olopa | FAO GIEWS: pérdidas por la sequía de 2018 en Centroamérica, https://www.fao.org/3/CA1321EN/ca1321en.pdf; FAO: perfil de las comunidades ch'orti', https://openknowledge.fao.org/server/api/core/bitstreams/b4f735d8-7008-423c-b28a-300ab920c241/content/src/html/sec8_1.html |
| 2019 | 96 512 familias afectadas, 14 830 de ellas en Chiquimula; Oxfam midió pérdidas promedio de 78.1 % en maíz y 70.4 % en frijol en 201 comunidades monitoreadas, 23 de ellas en Jocotán, Camotán, San Juan Ermita y Olopa | Guatemala y Chiquimula (MAGA); 201 comunidades monitoreadas (Oxfam) | MAGA: boletín SMC de julio de 2019, https://precios.maga.gob.gt/archivos/smc/2019/07%20Bolet%c3%adn%20SMC%20-%20Julio%20%20-%202019.pdf; Oxfam (2019): informe del déficit de lluvias, https://reliefweb.int/attachments/017ed79d-0dfa-3d24-a502-3474f5d9ddb7/Informe%20d%C3%A9fict%20de%20lluvias%202019.pdf |
| 2023 | 53 129.82 ha de maíz y frijol dañadas y 101 184 familias afectadas; FEWS NET informó pérdidas de al menos el 50 % en la Primera para agricultores de subsistencia | 75 municipios, entre ellos de Chiquimula y Zacapa (SIINSAN); Guatemala (FEWS NET) | SIINSAN: pronóstico SAN de octubre a diciembre de 2023, https://portal.siinsan.gob.gt/wp-content/uploads/PRONOSTICO-SAN-OCTUBRE-DICIEMBRE-2023.pdf; FEWS NET: perspectiva de seguridad alimentaria de Guatemala, octubre de 2023, https://fews.net/latin-america-and-caribbean/guatemala/food-security-outlook/october-2023-0/print |

Notas:

- La lista de siete años se tomó entera de fuentes públicas después de la prueba, no se eligió para el resultado: guarda todos los años con pérdidas documentadas que encontramos, también los que el motor no marca.
- 2010 figura como año con pérdidas documentadas, no como sequía: la causa no está en nuestras notas.
- Las fuentes tienen ámbitos distintos (el país, un departamento o las comunidades ch'orti') y ninguna mide nuestros cinco puntos.
- Para reproducirlo: en `web/public/data/validacion.json`, `perdidas_documentadas.parcelas[]` sale de los `anio` de `parcelas[].sequia_2018.anios[]` con `riesgo_alto` en `true`.

### Evidencia pública de la sequía de 2018

FAO GIEWS Update – Central America, 27 de agosto de 2018 (https://www.fao.org/3/CA1321EN/ca1321en.pdf): «As of 15 August 2018, the Governments of El Salvador, Guatemala and Honduras reported losses of 282 000 hectares in maize and bean crops, resulting in an estimated 2.2 million people at risk of food insecurity.» Guatemala: 175126 ha perdidas y 1290785 personas afectadas; departamentos más afectados: Jutiapa, Chiquimula, El Progreso, Jalapa, Baja Verapaz. Estimación del MAGA del 13 ago 2018 citada por FAO GIEWS; no hay porcentaje de pérdida solo para Guatemala.

## Observación preliminar: julio-agosto 2026

En julio y agosto de 2026 llovió entre el 20 % y el 26 % de lo normal (mediana 1991-2025) en las 5 parcelas, según CHIRPS v3; es lo menos desde 1991 en 5 de 5. SMAP registra la humedad del suelo de julio-agosto más baja de sus 12 años en 3 de 3 celdas de 9 km con dato.

| Parcela | Julio + agosto (mm) | Mediana de referencia (mm) | % de la mediana | Mínimo anterior (año) | Años más secos |
|---|---|---|---|---|---|
| Jocotán | 78.7 | 323.9 | 24 % | 138.1 (2018) | 0 de 35 |
| Camotán | 93.9 | 355.2 | 26 % | 154.4 (2018) | 0 de 35 |
| Olopa | 106.4 | 475.1 | 22 % | 211.0 (1997) | 0 de 35 |
| San Juan Ermita | 69.2 | 344.7 | 20 % | 140.3 (2018) | 0 de 35 |
| Zacapa | 43.9 | 206.1 | 21 % | 90.4 (2018) | 0 de 35 |

| Celda SMAP (9 km) | Parcelas | Julio-agosto 2026 (m³/m³) | Mínimo anterior (año) | ¿El más bajo? | Años |
|---|---|---|---|---|---|
| 604, 970 | Jocotán, San Juan Ermita | 0.162 | 0.182 (2015) | sí | 12 (2015-2026) |
| 606, 971 | Olopa | 0.18 | 0.216 (2015) | sí | 12 (2015-2026) |
| 602, 968 | Zacapa | 0.152 | 0.172 (2019) | sí | 12 (2015-2026) |

Reportes públicos (no son la fuente de las cifras de arriba):

- FEWS NET, Guatemala: actualización de la perspectiva de seguridad alimentaria, agosto 2026 (coincide): «Entre el 01 y el 31 de agosto, el Corredor Seco recibió entre el 5 y el 25 por ciento de las lluvias en comparación con los valores normales». Coincide con CHIRPS, pero no es una confirmación independiente: el informe no dice de qué producto sale la cifra y su mapa de lluvia (figura 1) es del Climate Hazards Center, el mismo grupo que produce CHIRPS. Se refiere solo a agosto y a todo el Corredor Seco. https://fews.net/es/latin-america-and-caribbean/guatemala/actualizacion-de-la-perspectiva-de-seguridad-alimentaria/agosto-2026
- Prensa Libre, 1 sep 2026, sobre una evaluación de Oxfam, Acción contra el Hambre y organizaciones socias (independiente: encuesta de hogares): «En el corredor seco guatemalteco, 36 mil 431 hogares reportan serios daños en sus cosechas de maíz, según una evaluación de Oxfam, organizaciones socias y Acción contra el Hambre.». Ámbito según la nota: el corredor seco de Guatemala, sin lista de departamentos ni municipios. Según la nota, el estudio incorporó 4260 participantes, representativos de unos 91 121 hogares: los 36 431 hogares son una estimación representativa, no un conteo. El estudio completo abarca Guatemala, Honduras y El Salvador. No se atribuye a Chiquimula ni a Zacapa. https://www.prensalibre.com/guatemala/comunitario/sequia-golpea-el-maiz-estudio-documenta-graves-perdidas-en-36-mil-hogares-del-corredor-seco/
- Canal Antigua, 25 sep 2026 (independiente: conteo oficial de familias afectadas): «se contabilizan 113 mil 825 familias afectadas». Ámbito según la nota: «15 municipios de Chiquimula y Jutiapa, bajo alerta roja por la sequía». No da cifras de Zacapa. https://canalantigua.tv/2026/09/25/sequia-persiste-pese-a-alivio-temporal-de-lluvias-113-mil-familias-siguen-afectadas-en-chiquimula-y-jutiapa/

Límites:

- Es una observación del pasado, no un pronóstico. La lluvia y la humedad de 2026 no entran en los puntajes ni en la confianza: el clima del motor es 2001-2025. La lluvia de julio-agosto de 2026 sí se dice en la vista del agricultor y en su audio corto, como dato preliminar. Los focos de enero a mayo de 2026 sí cuentan en el hecho de quema.
- Preliminar: el Climate Hazards Center recalcula CHIRPS cada mes y SMAP puede reprocesarse. Los meses de 2026 vienen de la carpeta del producto final (no de prelim/); se guarda la fecha de cada archivo.
- SMAP: 3 celdas de 9 km con dato (4 parcelas; Jocotán y San Juan Ermita comparten celda); sin dato de calidad recomendada: Camotán. Con 12 años, «el más bajo» es todo lo que se puede decir; no se da percentil.
- Las parcelas son puntos de ejemplo elegidos con satélite, no verificados en campo.

## Notas y límites

- CHIRPS no es medición en tierra: mezcla satélite y estaciones. Según su README, CHIRPS v3 ya mezcla estaciones de INSIVUMEH (https://data.chc.ucsb.edu/products/CHIRPS/v3.0/README-CHIRPSv3.0.txt); falta una comparación independiente con estaciones.
- POWER: celda de 0.5° x 0.625° (~50 km). CHIRPS: 0.05° (~5 km).
- La lluvia del motor es el total mensual de CHIRPS repartido con los días de POWER.
- Riesgo alto = déficit del año mayor que el percentil 75 de los años anteriores (desde 2001).
- Señal de NDVI = anomalía de julio-septiembre de -1 desviación estándar o menos.
- Anomalía de SMAP de 2018 = julio-agosto de 2018 frente a los demás años con SMAP (desde 2015, incluidos años posteriores a 2018). SMAP no entra en la corrida «con lo que se sabía hasta 2017»: esa corrida solo usa el déficit de agua con la lluvia de CHIRPS.
- SMAP: SPL3SMP_E.006 por AppEEARS, solo datos con calidad recomendada. Camotán no tiene ninguno; Jocotán y San Juan Ermita comparten la celda de 9 km. SMAP mide los primeros 0-5 cm del suelo y describe unos 9 km del paisaje, no la parcela.
- Las 5 parcelas son puntos de ejemplo elegidos con NDVI e imagen Sentinel-2, no verificados en campo; ver docs/es/estado.md.
- El hecho de canícula depende de cómo CHIRPS reparte la lluvia por día: la comparación de «sat» (IMERG) con «rnl» (ERA5) está en [es/sensibilidad-canicula.md](es/sensibilidad-canicula.md).
