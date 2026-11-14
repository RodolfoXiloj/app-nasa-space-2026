# Estado de Milpa Resiliente

Pruebas de línea base corridas el sábado 14 nov 2026, de 12:09 a 12:11 (pytest, humo, build y sin red: todas pasan). **Prototipo local de referencia: no se entrega ni se publica** (decisión de Rodolfo, 14 nov 2026). Repositorio Git local, sin remoto. Cada prueba corrida de verdad, con su comando, resultado y hora, está en `docs/pruebas.md`, junto con las pendientes; las decisiones y los hallazgos, en `docs/memoria/` (empezar por `Inicio.md`).

## Qué funciona

| Pieza | Estado |
|---|---|
| Parcelas | **5 puntos propuestos como definitivos**, elegidos con NDVI y revisados con imagen Sentinel-2, cada uno en un píxel distinto de CHIRPS (`data/parcelas.yaml`). Detalle y dudas en `docs/memoria/Puntos definitivos de las parcelas.md` |
| Datos sin clave | POWER 1991-2025 · NDVI MOD13Q1 2001-2025 de las 5 parcelas · FIRMS 2012-2025 · **CHIRPS v3 mensual 1991-2025** y **diario de junio a agosto 2001-2025** (lectura por rangos HTTP con decodificador LZW propio, sin rasterio) · CHIRPS v3 de julio y agosto 2026, aparte, solo para la observación de 2026 · SRTM · SoilGrids (REST, con respaldo WCS; el respaldo no tiene corrida real registrada) · teselas GIBS para el mapa sin red |
| Datos con clave (`.env`) | Earthdata Login (usuario en `.env`; la contraseña solo por tarjeta segura, nunca en disco del repo) · **FIRMS 2026** con `FIRMS_MAP_KEY`: producto estándar hasta el 31 jul y NRT después; 270 focos en la zona; ya entra al motor (15 años observados) |
| SMAP | **SPL3SMP_E.006 por AppEEARS, 31 mar 2015 a 13 nov 2026** (tarea `7c0fd22c…`; datos en el repo desde el commit `41ec4eb`, 14 nov 2026). Solo datos con calidad recomendada. Mediana de jul-ago: Jocotán y San Juan Ermita 0.247 m³/m³ (comparten la celda de 9 km), Olopa 0.274 y Zacapa 0.206. **Camotán no tiene SMAP:** su celda nunca alcanza la calidad recomendada (3007 mediciones descartadas); el motor lo dice así y usa el modelo MERRA-2 rotulado. Confianza de agua: Jocotán y San Juan Ermita «alta», Olopa «media», Zacapa «baja» (POWER se desvía 55 % de CHIRPS) y Camotán «baja» (sin SMAP) |
| Motor | Lluvia corregida con CHIRPS; clase «poca cobertura»; regla 5.1 de la validación conectada a la confianza; rechaza cachés de otra coordenada; referencia de ZARC por departamento rotulada. **Audio:** 5 mp3 (edge-tts, voz es-GT-MartaNeural, ~72 s) con la IA declarada en la web y en etiquetas ID3 (`motor/audio_id3.py`); un mp3 solo se enlaza si fue generado con el texto actual (hash en su etiqueta) |
| Validación | `python -m pipeline.validacion.validar`: POWER contra CHIRPS, sequía de 2018 y **observación preliminar de julio-agosto 2026** → `web/public/data/validacion.json` y `docs/validacion.md` (se regenera, no se edita a mano). Cotejo de cifras contra la caché (plan 12.6): sin corrida real registrada |
| Biblioteca | 8 plantillas con fuentes verificadas (ICTA, MAGA, CIMMYT, FAO, Bioversity): 3 actuales, maíz con canavalia, milpa completa, maíz con gandul, sorgo con caupí y maíz ICTA B-5. Kc y Ky verificados contra FAO-56 y FAO-66 |
| Web | Observación de 2026 en la primera pantalla, con enlace al detalle en Validación; pestaña Validación completa; capas «sin red», y **sin internet el mapa pasa solo a la capa guardada**; Sentinel-2 en línea; rótulo de voz sintética junto al reproductor. Prueba sin red automática: `npm run sin-red` (14 de 14 el 14 nov 2026, 12:10). Prueba en teléfono: `docs/prueba-telefono.md` (pendiente) |
| Memoria y grafo | `docs/memoria/` (30 notas con enlaces) y `graphify-out/` (grafo del código con Graphify, sin LLM) |

## Lo que dicen los datos

**Lo que ve el satélite y el motor en cada parcela** (rotación actual: maíz con frijol; prioridad: agua):

| Parcela | Suelo desnudo | Poca cobertura | Ciclos/año | Quemas ≤500 m | Lluvia anual CHIRPS (mediana) | Año más seco | Canícula >15 días | Déficit actual | Mejores opciones (total) | Confianza |
|---|---|---|---|---|---|---|---|---|---|---|
| Jocotán | mar, abr | feb, may | 1 | 3 de 15 años | 1186 mm | 2018 (805 mm) | 2 de 25 años | 16 % | Maíz con canavalia en primera, frijol en postrer (88); Sorgo en primera y caupí en postrera, con rastro (87) | alta |
| Camotán | ninguno | mar, abr | 1 | 3 de 15 años | 1300 mm | 2018 (901 mm) | 2 de 25 años | 12 % | Maíz con canavalia en primera, frijol en postrer (90); Sorgo en primera y caupí en postrera, con rastro (89) | baja |
| Olopa | ninguno | mar, abr | 1 | 1 de 15 años | 1556 mm | 2002 (1147 mm) | 0 de 25 años | 11 % | Maíz con canavalia en primera, frijol en postrer (90); Maíz de ciclo corto ICTA B-5 con frijol en prime (92) | media |
| San Juan Ermita | feb, mar, abr | ene, may | 2 | 2 de 15 años | 1186 mm | 2018 (776 mm) | 1 de 25 años | 15 % | Maíz con canavalia en primera, frijol en postrer (88); Sorgo en primera y caupí en postrera, con rastro (86) | alta |
| Zacapa | abr | ene, feb, mar, may | 1 | 0 de 15 años | 806 mm | 2018 (530 mm) | 3 de 25 años | 25 % | Maíz con canavalia en primera, frijol en postrer (81); Sorgo en primera y caupí en postrera, con rastro (80) | baja |

**Validación** (`docs/validacion.md`, generado por `python -m pipeline.validacion.validar`):

- En julio-agosto, NASA POWER se desvía 4.6 % de CHIRPS en Jocotán (error medio de 45.7 mm/mes, r = 0.74, n = 50 meses, 2001-2025).
- El motor, con lo que se sabía hasta 2017, marca 2018 como riesgo alto en 5 de 5 parcelas; alguna señal (motor, NDVI o SMAP) lo muestra en 5. Regla 5.1: 5 parcelas con señal; no se activa.
- Evidencia pública: FAO GIEWS (27 ago 2018) reporta para Guatemala 175 126 ha de maíz y frijol perdidas y 1 290 785 personas afectadas; Chiquimula entre los departamentos más afectados.
- Jocotán: 2018 es el año 1 de 25 por déficit; motor sí; NDVI jul-sep 2018 -2.35 DE; SMAP jul-ago 2018 -0.67 DE; aciertos 3, falsas alarmas 2, fallos 1 (n = 20); Spearman 0.69 (n = 20); POWER frente a CHIRPS en jul-ago 4.6 %.
- Camotán: 2018 es el año 1 de 25 por déficit; motor sí; NDVI jul-sep 2018 0.14 DE; SMAP jul-ago 2018 sin dato; aciertos 3, falsas alarmas 2, fallos 1 (n = 20); Spearman 0.45 (n = 20); POWER frente a CHIRPS en jul-ago -5.8 %.
- Olopa: 2018 es el año 1 de 25 por déficit; motor sí; NDVI jul-sep 2018 -0.14 DE; SMAP jul-ago 2018 -1.06 DE; aciertos 3, falsas alarmas 3, fallos 1 (n = 20); Spearman 0.07 (n = 20); POWER frente a CHIRPS en jul-ago -22.1 %.
- San Juan Ermita: 2018 es el año 1 de 25 por déficit; motor sí; NDVI jul-sep 2018 -1.13 DE; SMAP jul-ago 2018 -0.67 DE; aciertos 3, falsas alarmas 3, fallos 1 (n = 20); Spearman 0.45 (n = 20); POWER frente a CHIRPS en jul-ago 2.6 %.
- Zacapa: 2018 es el año 1 de 25 por déficit; motor sí; NDVI jul-sep 2018 -1.72 DE; SMAP jul-ago 2018 -0.98 DE; aciertos 3, falsas alarmas 2, fallos 1 (n = 20); Spearman 0.86 (n = 20); POWER frente a CHIRPS en jul-ago 55.4 %.

**Por qué importa:** NASA POWER pone 4 de las 5 parcelas en la misma celda de ~50 km y sobreestima la lluvia (+78 % en Zacapa en todo el año); su serie cambia de nivel antes de 2001. Con CHIRPS (~5 km) cada parcela tiene su lluvia; 2018 es el año de mayor déficit en las 5 parcelas y el de menos lluvia anual en 4 (en Olopa fue 2002).

## Decisiones (revisar con el equipo)

1. **Puntos de las parcelas.** Ver la tabla en `docs/memoria/Puntos definitivos de las parcelas.md`. Camotán y Olopa se eligieron con criterio relajado: muestran «poca cobertura», no suelo desnudo. La parcela de Olopa puede caer en Esquipulas, y la de Zacapa puede ser bosque seco.
2. **Lluvia del motor = CHIRPS.** Total mensual de CHIRPS (~5 km). En junio-agosto, CHIRPS diario 'sat' (péntadas repartidas con NASA IMERG); el resto del año, repartido con los días de POWER. La temperatura sigue siendo de POWER.
3. **Calibración de la detección** (antes de correr 2018): el suelo desnudo sigue en NDVI < 0.35 y se agregó «poca cobertura» de 0.35 a 0.45, que resta la mitad.
4. **Duraciones de cultivo** con fuente: maíz de 125 días (FAO-56 Tabla 11), ICTA B-5 de 90 días y sorgo ICTA Blanco de 100 días. El frijol de postrera (80 días) y el caupí (75) siguen siendo supuestos.
5. **ZARC.** No publica ventanas por municipio. La tarjeta remite al extensionista y muestra entre comillas la referencia de prensa por departamento.
6. **SMAP solo con calidad recomendada** (bit 0 de `retrieval_qual_flag` en 0). Por eso Camotán queda sin SMAP: no se usaron sus mediciones de calidad no recomendada (bandera 9) para no rellenar con datos dudosos.

## Observación preliminar: julio-agosto 2026

Está en la primera pantalla de la web y en detalle en la pestaña Validación. Sale de `pipeline/validacion/validar.py` (`observacion_2026`), con las cifras tomadas de la caché:
- **CHIRPS v3 mensual, producto final** (carpeta `monthly`, no `prelim/`, archivos del 2 nov 2026): julio más agosto de 2026 fue entre el 20 % y el 26 % de la mediana de 1991-2025 en las 5 parcelas, lo menos desde 1991 en las 5.
- **SMAP:** la humedad de julio-agosto más baja de sus 12 años en **3 de 3 celdas de 9 km** con dato. Jocotán y San Juan Ermita comparten celda; Camotán no tiene dato de calidad recomendada. No se da percentil.
- **Reportes públicos, con su ámbito exacto:**
  - FEWS NET (agosto) **coincide**, pero no es confirmación independiente: su mapa de lluvia es del mismo grupo que CHIRPS.
  - Prensa Libre: «36 mil 431 hogares» en el corredor seco guatemalteco, según una evaluación de Oxfam y Acción contra el Hambre. La nota no aclara si son hogares evaluados o estimados, y no se atribuye a Chiquimula.
  - Canal Antigua: 113 825 familias afectadas en 15 municipios de Chiquimula y Jutiapa.
- **Límites:** es una observación del pasado, no un pronóstico ni una alerta. El motor usa 2001-2025 y no la usa en puntajes, confianza ni audio. El Climate Hazards Center recalcula CHIRPS cada mes.

## Qué falta

**Necesita a Rodolfo o a alguien de la zona**
- Prueba en un teléfono real con `docs/prueba-telefono.md`: servir en la red local, recorrer la lista y anotar los resultados. También pendientes: TalkBack y una prueba de comprensión (ver `docs/pruebas.md`).
- Confirmar en campo, o con alguien de la zona, los 5 puntos y los límites municipales de Olopa y San Juan Ermita.
- Revisar con un agrónomo o extensionista las reglas de puntaje y las 8 plantillas (preguntas en `docs/revision-plan.md`, sección 3.2).

**Técnico (opcional)**
- Canícula: con CHIRPS diario las rachas son más realistas, pero el umbral de 15 días y el día seco de 2 mm siguen siendo los del plan; no se recalibraron para que 2018 salga bien.
- Camotán sin SMAP: la segunda tarea con SPL4SMGP (modelo, zona de raíces) tardaría horas y habría que rotularla como modelo. Queda como está.

**Ya no aplica** (el repo no se entrega): Render, repo público, push, slides, video, página en inglés y formulario de Space Apps.

## Comandos

```bash
pip install -r requirements.txt
MILPA_ONLINE=1 python -m pipeline.precargar                 # POWER, SRTM, FIRMS, suelo y NDVI 2001-2025
MILPA_ONLINE=1 python -m pipeline.clientes.chirps           # CHIRPS mensual; --diario para junio-agosto
MILPA_ONLINE=1 python -m pipeline.clientes.chirps --reciente 2026   # julio y agosto 2026, solo para la observación
MILPA_ONLINE=1 python -m pipeline.clientes.firms --reciente 2026
MILPA_ONLINE=1 python -m pipeline.capas                     # teselas del mapa sin red
python -m pipeline.validacion.validar                       # validacion.json y docs/validacion.md
MILPA_ONLINE=1 python -m motor.exportar --audio             # JSON y mp3 de la web
python -m motor.exportar --etiquetar                        # solo las etiquetas ID3 de IA de los mp3
python -m pytest
cd web && npm install && npm run smoke && npm run build && npm run sin-red
graphify update .                                           # grafo del código
```
