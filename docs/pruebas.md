# Registro de pruebas

Actualización documental: 14 nov 2026, 09:00 (Guatemala, UTC−6).

Las fechas de trabajo se normalizaron para esta edición; no representan nuevas ejecuciones, consultas ni capturas.

Cada prueba con qué se probó, el comando, el resultado y la fecha y hora (Guatemala, UTC−6). Las claves nunca se imprimen: las pruebas de FIRMS y Earthdata solo dicen si la clave existe.

Leyenda: ✅ pasa · ❌ falla · ⚠️ pasa con observaciones · ⏸️ no se pudo correr

## sábado 14 nov 2026, bloque de la mañana (commit 38562ee)

| Hora | Qué | Comando | Resultado |
|---|---|---|---|
| 09:17 | Prueba de humo de las fuentes sin clave | `curl` a POWER, ORNL, FIRMS por país, CHIRPS 2.0, SoilGrids, OpenTopoData | ✅ POWER, ORNL, FIRMS por país y OpenTopoData · ❌ CHIRPS 2.0 (404) · ❌ SoilGrids (timeout) |
| 09:29 | NDVI 2001-2025 de Jocotán (punto original) | `MILPA_ONLINE=1 python -m pipeline.clientes.ornl_ndvi jocotan` | ✅ 575 compuestos, 116 peticiones |
| 09:31 | Motor de punta a punta (Jocotán) | `python -c "from motor.recomendar import recomendar; recomendar('jocotan')"` | ✅ 0.5 s · ⚠️ 0 meses desnudos y déficit de 2-3 %: el punto no es agrícola y POWER sobreestima la lluvia |
| 09:33 | Exportación con validación de esquema y textos | `python -m motor.exportar jocotan` | ✅ 3 archivos |
| 09:48 | Pruebas automáticas | `python -m pytest` | ✅ 48 pasan |
| 09:55 | Build de la web | `cd web && npm run build` | ✅ |
| 09:58 | Prueba de humo de la web | `cd web && npm run smoke` | ✅ 16 JSON x 6 componentes x 3 escenarios |

## sábado 14 nov 2026, segundo bloque

| Hora | Qué | Comando | Resultado |
|---|---|---|---|
| 09:27 | Estructura del TIF de CHIRPS v3 latam | lectura por rangos del IFD (`curl -r`) | ✅ 1720 x 1900, float32, LZW, una fila por franja, origen (−120, 35), 0.05° |
| 09:31 | Decodificador LZW propio contra Pillow (julio 2018, filas de las parcelas) | `python` con `chirps.leer_filas` y `PIL.Image.open` sobre el archivo completo | ✅ diferencia máxima 0.0 en las 4 filas |
| 09:33 | Detección en el píxel candidato de Jocotán (14.81146, −89.39433) | `python probar_candidatos.py` (NDVI 2019-2025) | ✅ marzo y abril desnudos, 95.7 % válidos, P90 − P10 = 0.42 |
| 09:33 | Detección en el píxel candidato de Zacapa (14.94062, −89.56) | ídem | ✅ abril desnudo, 93.9 % válidos, P90 − P10 = 0.45 |
| 09:35 | Revisión a ojo con Sentinel-2 cloudless (Jocotán original y candidato, Zacapa) | `python -m pipeline.imagen_punto LAT LON salida.png` | ✅ Jocotán candidato: parcelas abiertas · ⚠️ Jocotán original: vegetación densa · ⚠️ Zacapa: ladera seca, no se distingue de bosque seco |
| 09:36 | FIRMS_MAP_KEY desde `.env` | `firms.disponibilidad(clave)` | ✅ clave presente (32 caracteres, no impresa); SP hasta 2026-07-31, NRT hasta 2026-11-02 |
| 09:36 | `.env` fuera de git | `git check-ignore -q .env` | ✅ |
| 09:37 | SoilGrids REST | `curl rest.isric.org/.../properties/query` | ✅ volvió a responder |
| 09:37 | SoilGrids WMS GetFeatureInfo como respaldo | `curl maps.isric.org ... REQUEST=GetFeatureInfo` | ❌ no expone el valor del raster (se descarta) |
| 09:38 | SoilGrids WCS GetCoverage como respaldo | `curl maps.isric.org ... REQUEST=GetCoverage` + Pillow | ✅ arcilla 0-5 cm = 319 g/kg = 31.9 % en Jocotán, igual que la REST del 28 oct |
| 09:40 | FIRMS 2026 con clave (API de área) | `python -c "from pipeline.clientes import firms; firms.descargar_reciente(2026)"` | ✅ 270 detecciones en la caja de las parcelas, 62 peticiones, 1 ene a 2 nov |
| 09:45 | Búsqueda de píxeles agrícolas ±6 km | `python -m pipeline.elegir_punto camotan olopa san_juan_ermita --km 6` | ⚠️ criterio estricto: 0 candidatos en Camotán y Olopa; 349 relajados en San Juan Ermita |
| 09:47 | Criterio relajado (seco < 0.45, amplitud ≥ 0.25) | `python -m pipeline.elegir_punto camotan olopa --km 6 --seco-max 0.45 --amplitud-min 0.25` | ✅ 51 candidatos en Camotán, 20 en Olopa |
| 09:50 | Revisión con Sentinel-2 de Camotán, Olopa y San Juan Ermita | `python -m pipeline.imagen_punto ...` | ✅ mosaico de parcelas en ladera (Camotán), llano abierto (Olopa), parcelas en barbecho (San Juan Ermita) |
| 09:51 | Píxeles de CHIRPS distintos para las 5 parcelas | `chirps.fila_col` | ⚠️ el primer candidato de Camotán compartía píxel con Jocotán; se cambió por 14.86146, −89.37404 · ✅ 5 píxeles distintos |
| 09:53 | Precarga rápida en los 5 puntos nuevos | `MILPA_ONLINE=1 python -m pipeline.precargar --fuentes power,srtm,suelo` | ✅ 0 errores; SoilGrids por REST |
| 09:54 | FIRMS 2012-2026 por parcela | `MILPA_ONLINE=1 python -m pipeline.clientes.firms` | ✅ 15 años observados; quemas 2026 a ≤500 m en Jocotán (12 may) y San Juan Ermita (21 abr) |
| 09:55 | CHIRPS v3 mensual 1991-2025 | `MILPA_ONLINE=1 python -m pipeline.clientes.chirps` | ✅ 420 meses x 5 parcelas, píxeles distintos |
| 09:56 | Contraseña de Earthdata con tarjeta segura | `request_secret` (entrega en archivo) | ⏸️ sin respuesta a tiempo; SMAP queda pendiente |
| 09:58 | Pruebas tras integrar CHIRPS y «poca cobertura» | `python -m pytest` | ✅ 48 pasan |
| 09:59 | El motor rechaza cachés de otra coordenada | `datos.disponibilidad(pid)` | ✅ el NDVI de los puntos viejos queda «no disponible» |
| 10:00 | POWER contra CHIRPS por parcela | `clima.comparar(...)` | ✅ CHIRPS separa las parcelas (71 a 130 mm/mes); sesgo julio-agosto de −22 % a +55 % |
| 10:01 | Pruebas nuevas del pipeline (LZW, CHIRPS, `.env`, AppEEARS, coordenadas) | `python -m pytest tests/test_pipeline.py` | ✅ 11 pasan |
| 10:02 | Teselas de respaldo del mapa (GIBS) | `MILPA_ONLINE=1 python -m pipeline.capas` | ✅ 18 teselas, 665 KB · ⚠️ color real del 22 mar con nubes en 2 de 4 teselas |
| 10:03 | Fecha despejada para color real | % de píxeles blancos en las 4 teselas de zoom 9, 8 fechas | ✅ 15 mar 2026: 1.5 % (elegida); 22 mar: hasta 45 % |
| 10:05 | Grafo del código | `graphify update .` | ✅ 121 archivos, 850 nodos, 1362 relaciones, 74 comunidades, sin LLM · ⚠️ `graph.html` usa un CDN: no se versiona |
| 10:06 | Rutas personales en las salidas de Graphify | `grep -c 'Users\DELL'` | ✅ 0 (solo rutas relativas) |
| 10:08 | Notas de memoria (Obsidian) | script de notas + revisión de `[[enlaces]]` | ✅ 29 notas, 0 enlaces rotos |
| 10:09 | Velocidad de ORNL | `curl` de una fecha | ⚠️ 62 s por petición (lentitud del servidor); luego mejoró a ~17 por minuto |
| 10:10 | Segunda solicitud de la contraseña de Earthdata | `request_secret` | ⏸️ sin respuesta; SMAP queda pendiente |
| 10:12 | Pruebas del motor con CHIRPS, poca cobertura y regla 5.1 | `python -m pytest` | ✅ 62 pasan |
| 10:19 | Pruebas tras el audio con edge-tts (opcional) | `python -m pytest` | ✅ 63 pasan, 1 omitida (`validacion.json` todavía no existía) |
| 10:21 | Motor con los puntos nuevos (Jocotán, San Juan Ermita) | `recomendar(pid)` + `contrato.errores_*` | ✅ sin errores de esquema ni de texto; Jocotán: marzo y abril desnudos, 2018 el año más seco con CHIRPS |
| 10:22 | CHIRPS v3 diario 'sat' (formato) | lectura del IFD de `daily/final/sat/2018/...07.10.tif` | ✅ global 7200 x 2400, LZW, una fila por franja, origen (−180, 60) |
| 10:23 | Lectura optimizada (cola de 32 KB) | `chirps.leer_filas` diario y mensual | ✅ 3 peticiones por día; mismo valor que antes en el mensual |
| 10:24 | CHIRPS diario en el motor | `python -m pytest` (prueba nueva de `aplicar_chirps_diario`) | ✅ 64 pasan, 1 omitida |
| 10:26 | NDVI 2001-2025 en los 5 puntos nuevos | `pipeline.precargar ... --fuentes ndvi` + procesos extra | ✅ 116 de 116 peticiones por parcela |
| 10:26 | Validación preliminar (sin CHIRPS diario) | `python -m pipeline.validacion.validar` | ✅ 2018 es el año de mayor déficit en las 5 parcelas; el motor lo marca con datos hasta 2017 en 5 de 5 |
| 10:27 | Exportación intermedia de las 5 parcelas | `python -m motor.exportar` | ✅ 15 archivos sin errores |
| 10:27 | Prueba de humo de la web | `npm run smoke` | ❌ los 16 JSON pasan, pero el proceso sale con 255 por el escaneo de dependencias de Vite al cerrar |
| 10:28 | Prueba de humo corregida (`optimizeDeps.noDiscovery`) | `npm run smoke` x 3 | ✅ 3 de 3 sin fallas |
| 10:28 | Build | `npm run build` | ✅ |
| 10:29 | Web en móvil (Pixel 7, 412 px) con `vite preview` | vista previa del navegador: capturas de Parcela, Rotaciones y Validación | ✅ sin desborde horizontal; la tabla ancha se desplaza en su contenedor; datos y capas «sin red» se sirven del mismo sitio (solo el mapa base de OSM es externo) · ⚠️ eje de la dispersión con 486.4 mm (corregido a múltiplos de 100) |
| 10:30 | CHIRPS diario con dos procesos | conteo de extractos en 50 s | ✅ ~140 días por minuto |
| 10:31 | Fuentes agronómicas (investigación delegada, lectura de cada documento) | subagente con búsqueda web | ✅ Kc de FAO-56 y Ky de FAO-66 (p. 7) coinciden; 8 plantillas con fuente; ZARC sin ventanas por municipio; FAO GIEWS 2018 con cifras de Guatemala |
| 10:32 | Pruebas tras integrar fuentes, 8 plantillas y la referencia de ZARC | `python -m pytest` | ✅ 65 pasan, 1 omitida |
| 10:33 | `fuentes.yaml` válido | `yaml.safe_load` | ✅ 23 fuentes |
| 10:34 | Notas de memoria | revisión de `[[enlaces]]` | ✅ 30 notas, 0 enlaces rotos |
| 10:34 | Voz de la tarjeta con edge-tts | `generar_audio(...)` en el scratchpad | ✅ es-GT-MartaNeural, 69 KB para ~10 s |
| 10:36 | Pruebas de la validación (Spearman, anomalía de NDVI, evidencia de 2018) | `python -m pytest tests/test_validacion.py` | ❌ 1 falla: la prueba esperaba anomalía para 2005, que tiene solo 4 años previos (el código exige 5); se corrigió la prueba · ✅ 4 pasan |
| 10:46 | Tercera solicitud de la contraseña de Earthdata | `request_secret` (entrega en archivo) | ✅ recibida; se usa solo dentro del comando, no se escribe en el repo ni en `.env` |
| 10:46 | Login de AppEEARS y envío de la tarea SMAP (SPL3SMP_E.006, 5 puntos, 31 mar 2015 a 13 nov 2026) | `EARTHDATA_PASSWORD="$(cat <archivo>)" python -m pipeline.clientes.appeears_smap todo` | ✅ tarea 7c0fd22c-78e9-46d9-9f84-15d8447e9cf8 aceptada |
| 10:47 | Grafo del código actualizado | `graphify update .` | ✅ 954 nodos, 1545 relaciones, 82 comunidades |
| 10:48 | Textos y esquema en todas las combinaciones reales (5 parcelas x 3 cultivos x 3 prioridades) | `recomendar(pid, cultivo, prioridad)` + `contrato.errores_textos` y `errores_esquema` | ✅ 0 errores en 45 combinaciones; ZARC remite al extensionista y cita la referencia de prensa por departamento |
| 10:50 | Concurrencia contra el servidor de CHIRPS (3 procesos, 18 hilos) | conteo de extractos por minuto | ⚠️ bajó de ~140 a ~17 días por minuto: se detuvieron 2 procesos; 0 extractos corruptos tras el corte |
| 10:51 | Costo del decodificador LZW | decodificar una fila global con y sin corte temprano | ✅ 0.01 s por fila completa y 0.001 s con corte: no es el cuello de botella; sí lo es la red (32 KB en 9 s) |
| 10:53 | Lector ligero de CHIRPS (solo IFD, entradas de tablas y tramo inicial de cada fila) | `leer_columnas_ligero` contra `leer_filas` en 5 píxeles | ✅ valores idénticos · ⚠️ 33 s por día con el servidor limitando |
| 10:55 | Validación y exportación intermedias (CHIRPS mensual, 8 plantillas) | `python -m pipeline.validacion.validar` + `python -m motor.exportar` | ✅ 2018 es el año más seco en 4 de 5 parcelas (Olopa: 2002); el motor marca 2018 en 5 de 5 |
| 10:56 | Pruebas, humo y build antes del commit intermedio | `python -m pytest` + `npm run smoke` + `npm run build` | ✅ 69 pasan, 1 omitida; humo sin fallas; build listo |
| 10:56 | Commit intermedio local (sin remoto) | `git commit` | ✅ 2c1fbf8; `.env`, notas internas, `raw_big`, `graph.html` y `node_modules` fuera |
| 10:57 | Claves fuera del repo | búsqueda de los valores de `.env` en los 197 archivos versionados | ✅ 0 coincidencias (FIRMS_MAP_KEY y EARTHDATA_USERNAME) |
| 10:58 | Lector ligero de CHIRPS sin red (TIF LZW de Pillow servido desde memoria) | `python -m pytest tests/test_pipeline.py` | ✅ 13 pasan; valores exactos hasta la columna pedida y menos de la mitad de los bytes |
| 10:58 | Tiempo por petición al servidor de CHIRPS | lectura instrumentada de un día | ⚠️ ~1.2 s por petición; con 9 peticiones por día = 11.5 s |
| 10:59 | Lector ligero con 4 peticiones por día (tablas juntas y filas contiguas en una sola petición) | `pytest tests/test_pipeline.py` + lectura de un día | ✅ 13 pasan; 4.8 s por día |
| 11:00 | Racha seca de la canícula con CHIRPS diario (Jocotán, 2007-2021, vista previa) | cálculo directo sobre `data/cache/chirps_diario/jocotan.json` | ✅ más de 15 días solo en 2015 (19) y 2018 (17); con POWER salía 0 de 25 años. Umbrales sin cambios (2 mm, 15 días) |
| 11:00 | Pruebas con el lector de 4 peticiones | `python -m pytest` | ✅ 70 pasan, 1 omitida |
| 11:00 | Grafo del código | `graphify update .` | ✅ 961 nodos, 1559 relaciones, 83 comunidades |

## sábado 14 nov 2026, cierre del segundo bloque

| Hora | Qué | Comando | Resultado |
|---|---|---|---|
| 12:16 | Espera de la tarea SMAP en AppEEARS (primer proceso) | `appeears_smap esperar` (tope de 90 min) | ⏸️ se cortó a los 5407 s con la tarea aún en «processing» |
| 12:53 | Estado de la tarea SMAP, consulta única | `login()` + `estado(...)` con tope de 60 s | ⏸️ «processing»; se relanzó una espera de 40 min en segundo plano |
| 12:54 | Caché completa de CHIRPS diario (jun-ago 2001-2025) | `MILPA_ONLINE=1 python -c "from pipeline.clientes import chirps; chirps.descargar_diario(hilos=4)"` | ✅ 2300 días por parcela en 7 s, desde los 2301 extractos ya bajados (sin descargas nuevas) |
| 12:54 | Validación final | `python -m pipeline.validacion.validar` | ✅ 2018 es el año de mayor déficit (1 de 25) en las 5 parcelas; el motor lo marca en 5 de 5; NDVI jul-sep 2018: Jocotán −2.35 DE, Zacapa −1.72, San Juan Ermita −1.13, Camotán 0.14, Olopa −0.14; Spearman 0.69 / 0.45 / 0.07 / 0.45 / 0.86; regla 5.1 no se activa (5 con señal, mínimo 3) · ⚠️ SMAP sin dato |
| 12:55 | Canícula con CHIRPS diario completo | rachas de `web/public/data/*.json` | ✅ más de 15 días: Jocotán y Camotán 2015 (19) y 2018 (17); San Juan Ermita 2018 (28); Zacapa 2015 (23), 2018 (21) y 2025 (18); Olopa ninguno (2018: 11) |
| 12:55 | Exportación con audio | `MILPA_ONLINE=1 python -m motor.exportar --audio` | ✅ 15 JSON y 5 mp3 (424-441 KB, voz es-GT-MartaNeural) en 77 s |
| 12:56 | Pruebas automáticas | `python -m pytest` | ✅ 70 de 70 pasan |
| 12:56 | Prueba de humo de la web | `cd web && npm run smoke` | ✅ sin fallas |
| 12:57 | Build de la web | `cd web && npm run build` | ✅ 8.5 s; JS de 765 KB (219 KB con gzip); los 5 mp3 quedan en `dist/audio` |
| 12:57 | Grafo del código | `graphify update .` | ✅ sin cambios de topología |
| 12:57 | Humo con verificación de audio (nueva: cada `audio.mp3` del JSON debe existir y pesar más de 1 KB) | `npm run smoke` | ✅ sin fallas |
| 12:58 | Prueba negativa de la verificación de audio | se movió `zacapa.mp3` fuera de `public/audio`, `npm run smoke`, y se devolvió | ✅ falla como debe: «1 fallas», salida 1; archivo restaurado (5 mp3) |
| 13:00 | Commit local del cierre (sin remoto) | `git commit` + búsqueda de los valores de `.env` y de la contraseña en los archivos preparados | ✅ a02250c; 0 coincidencias; `.env`, notas internas, `raw_big`, `graph.html` y `node_modules` fuera; `git remote -v` vacío |
| 13:35 | Segunda espera de la tarea SMAP (tope de 40 min, consulta cada 60 s) | `appeears_smap.esperar(..., max_min=40)` en segundo plano | ⏸️ terminó por tiempo con la tarea en «processing», casi 3 h después del envío; queda pendiente (comando para retomarla en `docs/estado.md`); no quedó ningún proceso corriendo |

## sábado 14 nov 2026, noche: SMAP

| Hora | Qué | Comando | Resultado |
|---|---|---|---|
| 20:37 | Cuarta solicitud de la contraseña de Earthdata (la pidió Rodolfo) | `request_secret` (entrega en archivo) | ✅ recibida; solo dentro del comando |
| 20:37 | Estado de la tarea SMAP, consulta única | `login()` + `estado(...)` con tope de 60 s | ✅ «done» |
| 20:37 | Descarga y procesamiento del CSV de SMAP | `bajar(...)` + `procesar(...)` | ✅ CSV de 9.5 MB, 4159 filas por parcela · ⚠️ Camotán sin salida: su celda solo tiene banderas 7, 9 y 13 (nunca calidad recomendada); Jocotán y San Juan Ermita comparten celda de 9 km y dan los mismos valores |
| 20:38 | Contraste de julio-agosto 2026 con CHIRPS v3 mensual | `chirps.extraer_mes(2026, 7 y 8, ...)` contra `data/cache/chirps/*.json` (1991-2025) | ✅ 2026 es el julio-agosto más seco de 1991-2026 en las 5 parcelas (44 a 106 mm); coincide con SMAP (percentil 8, el más bajo de 12 años) |
| 20:39 | Parcela sin SMAP de calidad recomendada queda rotulada | `python -m pipeline.clientes.appeears_smap procesar <csv>` | ✅ `data/cache/smap/camotan.json` con `jul_ago_mediana: null` y el motivo (3007 mediciones descartadas); el motor ya no dice «falta la descarga» |
| 20:40 | Pruebas automáticas (nuevas: celda sin calidad recomendada; confianza con el motivo de SMAP) | `python -m pytest` | ❌ 1 error de sintaxis en la prueba nueva (salto de línea literal dentro de una cadena); corregido con `chr(10)` · ✅ 71 de 71 pasan |
| 20:40 | Validación con SMAP | `python -m pipeline.validacion.validar` | ✅ anomalía SMAP jul-ago 2018: Olopa −1.06 DE (cuenta como señal), Zacapa −0.98, Jocotán y San Juan Ermita −0.67, Camotán sin dato; regla 5.1 no se activa (5 con señal) |
| 20:41 | Exportación con audio | `MILPA_ONLINE=1 python -m motor.exportar --audio` | ✅ 15 JSON y 5 mp3; confianza de agua: Jocotán y San Juan Ermita alta, Olopa media, Zacapa y Camotán baja |
| 20:41 | Esquema y textos de los JSON exportados | `contrato.errores_esquema` + `errores_textos` | ✅ 0 errores |
| 20:41 | Prueba de humo de la web | `cd web && npm run smoke` | ✅ sin fallas (incluye la verificación de los 5 mp3) |
| 20:42 | Build de la web | `cd web && npm run build` | ✅ 7.7 s |
| 20:42 | Grafo del código | `graphify update .` | ✅ actualizado |

## sábado 14 nov 2026, noche: prototipo local de referencia

El repo ya no se entrega (decisión de Rodolfo). Esta tanda aplica solo lo que mejora el funcionamiento. Las horas con «~» son aproximadas, porque esa prueba no imprimió la hora.

| Hora | Qué | Comando | Resultado |
|---|---|---|---|
| ~21:05 | Fuente y ámbito de las citas de 2026 (relectura de las páginas originales) | subagente de lectura web: FEWS NET agosto 2026 y Prensa Libre 1 sep 2026 | ⚠️ FEWS NET: la cifra de 5 % a 25 % es del 1 al 31 de agosto y no nombra el producto; su mapa de lluvia es del Climate Hazards Center. Prensa Libre: «36 mil 431 hogares» en el «corredor seco guatemalteco», sin aclarar si son evaluados o estimados → se citan como «coincide» y con su ámbito exacto |
| ~21:08 | ¿Julio y agosto 2026 de CHIRPS son el producto final? | listado de `CHIRPS/v3.0/` y `monthly/latam/tifs/` + README del CHC | ✅ carpeta `monthly` (final; el preliminar está en `prelim/`), archivos del 2 nov 2026. El README dice que el final se recalcula cada mes |
| ~21:12 | DOI y versiones de las fuentes con «TODO» e IMERG | `curl` a doi.org, `/api/product` de AppEEARS, documentación de OpenTopoData, README del CHIRPS diario | ✅ IMERG Late V07 (`10.5067/GPM/IMERG/3B-HH-L/07`); SRTMGL3.003; FIRMS VNP14IMG.002 y NRT; SMAP SPL3SMP_E.006 `10.5067/M20OXIZHY3RJ`; el CHIRPS diario 'sat' usa NASA IMERG Late V07 |
| ~21:15 | CHIRPS de julio y agosto 2026, en caché aparte | `MILPA_ONLINE=1 python -m pipeline.clientes.chirps --reciente 2026` | ✅ `data/cache/chirps_reciente/` para 5 parcelas, con la fecha de cada TIF; el motor no la lee |
| ~21:15 | Celda SMAP de cada parcela | `python -m pipeline.clientes.appeears_smap procesar <csv>` | ✅ 4 celdas de 9 km para 5 parcelas: Jocotán y San Juan Ermita en la misma (604, 970) |
| ~21:17 | Observación preliminar de julio-agosto 2026 | `python -m pipeline.validacion.validar` | ✅ CHIRPS, julio más agosto: entre 20 % y 26 % de la mediana de 1991-2025, lo menos desde 1991 en 5 de 5 parcelas. SMAP: el más bajo de 12 años en 3 de 3 celdas. Sin «alerta» ni percentil |
| ~21:20 | Etiquetas ID3 de IA en los 5 mp3, sin regenerarlos | `python -m motor.exportar --etiquetar` | ✅ `TPE1`, `COMM`, `TXXX:AI_GENERATED` y hash del texto; sin la etiqueta, el audio es idéntico byte a byte al anterior |
| ~21:20 | Exportar sin `--audio` conserva el mp3 vigente | `python -m motor.exportar` | ✅ 5 mp3 siguen enlazados (el hash coincide) con su declaración de IA; puntajes de las 5 parcelas sin cambios (Jocotán 80/88/87 … Zacapa 73/81/80) |
| ~21:22 | `data/fuentes.yaml` | `yaml.safe_load` | ✅ 29 fuentes, 0 duplicadas, 0 «TODO»; IMERG, AppEEARS, CHIRPS diario y los 3 reportes de 2026 citados; IMERG aparece en el JSON de la web |
| 21:28 | Prueba de humo (nueva: etiqueta de IA de cada mp3 y observación de 2026) | `cd web && npm run smoke` | ❌ primero marcó «alerta»: venía de la cita literal de Canal Antigua («bajo alerta roja»). Se acotó la comprobación a nuestro texto · ✅ sin fallas |
| 21:28 | Build | `cd web && npm run build` | ✅ 5.0 s |
| 21:28 | Pruebas automáticas (nuevas: 5 del audio con IA, 3 de la observación de 2026) | `python -m pytest` | ✅ 79 de 79 |
| 21:29 | Cotejo 12.6: 3 cifras al azar por tarjeta, recalculadas desde `data/cache/` sin el motor | script con semilla 20261113 (pendiente, arcilla, quemas, SMAP, lluvia anual, % de NDVI válido, racha de canícula, CHIRPS jul-ago) | ❌ primero falló el script, no los datos: leía mal la sección de FIRMS de 2026 · ✅ 15 de 15. Conjunto completo, 8 cifras por 5 parcelas con 5 años al azar en lluvia anual y canícula: 79 de 79 |
| 21:31 | Prueba sin red: Edge sin interfaz con un proxy inexistente (sin internet; el servidor local sí responde) | `node prueba_sin_red.mjs` | ⚠️ 13 de 14: los mp3 figuraban como fallidos, pero habían respondido 206 y el navegador cortó la descarga al pausar (`net::ERR_ABORTED`). Se cuenta aparte · ✅ 14 de 14. **Hallazgo:** sin internet, el mapa base quedaba gris |
| 21:32 | El mapa pasa solo a la capa guardada sin internet | build + prueba sin red | ✅ 14 de 14: 4 teselas locales, aviso «Sin internet…», capa «Color real MODIS» marcada en el control |
| 21:33 | Misma web con internet | Edge sin interfaz sin proxy | ✅ 9 teselas de OpenStreetMap, sin cambio de capa ni aviso |
| 21:34 | La prueba sin red dentro del repo | `cd web && npm run sin-red` | ✅ 14 de 14 |
| 21:36 | Pruebas, humo y build finales | `python -m pytest` + `npm run smoke` + `npm run build` | ✅ 79 de 79; sin fallas; build en 4.96 s (JS de 770 KB, 220 KB con gzip) |
| 21:36 | Web servida en la red local (para el teléfono) | `npx vite preview --host 0.0.0.0 --port 4173` + `curl` a `192.168.0.17:4173` | ✅ página, `validacion.json`, `zacapa.json`, mp3 (`audio/mpeg`; 206 por partes) y capas; servidor detenido después |
| 21:36 | Grafo del código | `graphify update .` | ✅ 1063 nodos, 1753 relaciones, 77 comunidades |
| 21:37 | Notas de memoria | revisión de `[[enlaces]]` | ✅ 34 notas, 0 enlaces rotos |

## sábado 14 nov 2026, noche: capturas y verificación final

| Hora | Qué | Comando | Resultado |
|---|---|---|---|
| 21:45 | Build de la web | `cd web && npm run build` | ✅ 4.85 s |
| 21:45 | Web compilada en la red local, como en `docs/prueba-telefono.md` | `npx vite preview --host 0.0.0.0 --port 4173 --strictPort` | ✅ responde en `192.168.0.17:4173` y en `127.0.0.1:4173` |
| 21:45 | Capturas en 1366×768 y 390×844, con verificación | Edge sin interfaz por CDP (script `capturas.mjs` en el scratchpad) | ✅ 26 PNG en `docs/capturas/`; mapa con los 5 círculos dentro y teselas del mapa base cargadas en los dos tamaños; los 5 audios cargan y suenan (de 71 a 73 s) con el rótulo de IA; consola en línea sin errores ni advertencias. ⚠️ El reproductor salía con el ícono de silencio porque la prueba silencia el audio para reproducirlo; se quitó el silencio después de probar y se repitieron las capturas |
| 21:47 | Desborde horizontal de la tarjeta | medición en la misma corrida | ✅ escritorio: la página no se desplaza de lado y la tabla queda dentro del recuadro. ❌ teléfono (390 px): la página no se desplaza de lado, pero la tabla de la tarjeta se sale 13 px de su recuadro y corta la columna «Confianza» en las 5 parcelas. **Sin corregir: esta tanda no cambia código** |
| 21:47 | Sin internet, en los dos tamaños | Edge con un proxy inexistente contra `127.0.0.1` | ✅ el mapa pasa solo a la capa guardada con su aviso, y el audio suena; en consola, solo los 15 fallos de red esperados de las teselas en línea |
| 21:48 | Prueba sin red completa | `cd web && npm run sin-red` | ✅ 14 de 14 |
| 21:49 | Servidor apagado y sin procesos | `TaskStop` + `taskkill` + búsqueda de procesos de Edge sin interfaz y de vite | ✅ ningún puerto 4173, 4174 ni 9334-9337 escuchando; ningún proceso de Edge sin interfaz ni de vite |

Detalle visual menor, visto en las capturas: el eje de años de la gráfica de NDVI repite etiquetas («2021, 2021, 2022…»). Sin corregir.

## sábado 14 nov 2026, noche: corrida 14, detalles visuales

| Hora | Qué | Comando | Resultado |
|---|---|---|---|
| 21:53 | Desborde de la tabla de la tarjeta, antes del arreglo | `medir_tarjeta.mjs` (scratchpad): Edge sin interfaz, 5 parcelas a 360, 390 y 1366 px | ❌ se sale 13 px a 390 px y 61 px a 360 px, con la columna «Confianza» cortada |
| 21:54 | El mismo CSS compacto, inyectado antes de editar | el mismo script con el CSS candidato | ✅ cabe en las 5 parcelas a 360 y 390 px; escritorio sin cambio |
| 21:55 | Build con los arreglos | `cd web && npm run build` | ✅ 4.91 s |
| 21:55 | Desborde con el CSS ya en el archivo | `medir_tarjeta.mjs` sin inyectar nada | ✅ 15 de 15 casos (5 parcelas × 360, 390 y 1366 px): la tabla y la columna «Confianza» quedan dentro del recuadro y la página no se desplaza de lado |
| 21:55 | Pruebas automáticas | `python -m pytest` | ✅ 79 de 79 |
| 21:55 | Prueba de humo | `cd web && npm run smoke` | ✅ sin fallas |
| 21:56 | Capturas rehechas, con verificación | `npx vite preview --host 0.0.0.0 --port 4173` + `capturas.mjs` | ✅ 21 de 21: 5 audios suenan, consola sin errores, mapa con las 5 parcelas, tarjeta sin desborde en teléfono (la tabla queda 12 px dentro), sin internet funciona; 26 PNG rehechas |
| 21:57 | Prueba sin internet | `cd web && npm run sin-red` | ✅ 14 de 14 |
| 21:57 | Revisión visual de las capturas corregidas | lectura de las PNG | ✅ tarjeta completa a 390 px; eje de NDVI con un año por marca y sin etiqueta encima de la curva; «consultado 2026-11-14» y la fecha de Validación sin partirse |
| 21:58 | Servidor apagado y sin procesos | `TaskStop` + `taskkill` + búsqueda de procesos | ✅ ningún puerto 4173-4175 ni 9334-9338 escuchando |

