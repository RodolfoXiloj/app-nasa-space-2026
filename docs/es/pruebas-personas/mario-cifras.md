# Guía 5 para Mario: Comprobación de todas las cifras visibles (tarjetas y vista Evidence) contra los JSON de datos

**Responsable:** Mario  
**Carpeta de datos donde se comprueba cada cifra:** `web/public/data/`  
**Tiempo estimado:** 20 a 30 minutos  

> **Por qué hace falta una persona:** El validador automático comprueba que los números de las plantillas estén en el JSON, pero una persona debe mirar la interfaz real en el navegador (tanto en la vista del agricultor como en las pestañas de *Evidence*) y confirmar visualmente que ninguna tarjeta, gráfica, etiqueta de eje o tabla muestre un número truncado, un `NaN`, un porcentaje invertido o una cifra que contradiga los archivos de `web/public/data/`.

---

## Cómo hacer esta revisión paso a paso

1. Abre la aplicación web en tu navegador (`http://localhost:4173/`) y ponla en **Español** (luego puedes cambiar a **English** para verificar que las cifras no cambian de idioma a idioma).
2. Ten abiertas (o consulta en las tablas de abajo) las rutas de `web/public/data/`:
   - `web/public/data/jocotan.json`
   - `web/public/data/camotan.json`
   - `web/public/data/olopa.json`
   - `web/public/data/san_juan_ermita.json`
   - `web/public/data/zacapa.json`
   - `web/public/data/validacion.json`
3. Recorre las **5 secciones de cifras** que están listadas aquí abajo, compara lo que ves en pantalla con el valor de la tabla y marca cada bloque en la **Tabla de registro final** con la hora real.

---

## Sección 1. Vista del agricultor — Los 3 hechos del semáforo y la confianza (5 parcelas)

En la primera pantalla, cambia el selector **Parcela** por cada uno de los 5 municipios y comprueba estas cifras:

| Parcela y archivo JSON | Hecho 1: **Suelo desnudo** (`agricultor.hechos.suelo` / `deteccion`) | Hecho 2: **Quema cerca** (`agricultor.hechos.quema` / `deteccion.quemas`) | Hecho 3: **Canícula larga** (`agricultor.hechos.canicula` / `clima.canicula`) | **Opciones y Confianza** (`agricultor.opciones`) |
|---|---|---|---|---|
| **Jocotán**<br>`web/public/data/jocotan.json` | • Estado: **Se repite** (cuadrado rojo)<br>• Rueda: **2 de 12 meses** desnudos (**marzo y abril**)<br>• Poca cobertura: **2 meses** (**febrero y mayo**)<br>• Fuente: MODIS **2021‑2025** | • Estado: **Se repite** (cuadrado rojo)<br>• Cuadrícula: **3 de 15 años** con quema<br>• Meses: **abril y mayo**<br>• Fuente: VIIRS **2012‑2026** | • Estado: **Atención** (triángulo amarillo)<br>• Cuadrícula: **2 de 25 años** con racha > **15 días**<br>• Entre junio y agosto<br>• Fuente: CHIRPS y IMERG **2001‑2025** | • **2 opciones parejas** (a **3 puntos o menos**): *Maíz con canavalia* y *Sorgo con caupí*<br>• Confianza: **Alta** (*Las tres comprobaciones se cumplen*) |
| **Camotán**<br>`web/public/data/camotan.json` | • Estado: **Atención** (triángulo amarillo)<br>• Rueda: **0 de 12 meses** desnudos; **2 meses** con poca cobertura (**marzo y abril**) | • Estado: **Se repite** (cuadrado rojo)<br>• Cuadrícula: **3 de 15 años** con quema<br>• Meses: **marzo y abril** | • Estado: **Atención** (triángulo amarillo)<br>• Cuadrícula: **2 de 25 años** con racha > **15 días** | • Estado **gris** (*No podemos recomendar una opción sobre otra: la confianza es baja*)<br>• Confianza: **Baja** (falta humedad SMAP con calidad recomendada) |
| **Olopa**<br>`web/public/data/olopa.json` | • Estado: **Atención** (triángulo amarillo)<br>• Rueda: **0 de 12 meses** desnudos; **2 meses** con poca cobertura (**marzo y abril**) | • Estado: **Atención** (triángulo amarillo)<br>• Cuadrícula: **1 de 15 años** con quema<br>• Mes: **abril** | • Estado: **Bien** (círculo verde)<br>• Cuadrícula: **0 de 25 años** con racha > **15 días** | • **Las 3 opciones quedan parejas** (87, 90 y 92 quedan en cadena a ≤ 3 puntos)<br>• Confianza: **Media** (POWER y CHIRPS se separan en jul-ago) |
| **San Juan Ermita**<br>`web/public/data/san_juan_ermita.json` | • Estado: **Se repite** (cuadrado rojo)<br>• Rueda: **3 de 12 meses** desnudos (**febrero, marzo y abril**)<br>• Poca cobertura: **enero y mayo** | • Estado: **Atención** (triángulo amarillo)<br>• Cuadrícula: **2 de 15 años** con quema<br>• Meses: **marzo y abril** | • Estado: **Atención** (triángulo amarillo)<br>• Cuadrícula: **1 de 25 años** con racha > **15 días** | • **2 opciones parejas**: *Maíz con canavalia* y *Sorgo con caupí*<br>• Confianza: **Alta** |
| **Zacapa**<br>`web/public/data/zacapa.json` | • Estado: **Atención** (triángulo amarillo)<br>• Rueda: **1 de 12 meses** desnudo (**abril**)<br>• Poca cobertura: **4 meses** (**enero, febrero, marzo y mayo**) | • Estado: **Bien** (círculo verde)<br>• Cuadrícula: **0 de 15 años** con quema | • Estado: **Se repite** (cuadrado rojo)<br>• Cuadrícula: **3 de 25 años** con racha > **15 días** | • Estado **gris** (*confianza baja*)<br>• Confianza: **Baja** (dos fuentes de lluvia no coinciden y pendiente fuerte) |

---

## Sección 2. Vista *Evidence* — Tarjeta del agricultor y las 3 tarjetas de Rotaciones (`rotaciones[]`)

Haz clic en **«Ver la evidencia»**. Con el selector *Qué sembró el último ciclo* en **«Maíz + frijol (milpa)»** y *Prioridad* en **«Agua»**, comprueba las cifras de las **3 opciones de rotación** y de la **Tarjeta para el agricultor**:

| Parcela y archivo JSON | Opción 1 (*Lo que hace hoy*)<br>Agua / Suelo / Plagas → **Total** · Déficit mediana (p25–p75) · Pérdida | Opción 2 (*Leguminosa o cobertura*)<br>Agua / Suelo / Plagas → **Total** · Déficit mediana (p25–p75) · Pérdida | Opción 3 (*Tolerante a sequía*)<br>Agua / Suelo / Plagas → **Total** · Déficit mediana (p25–p75) · Pérdida | Nivel de confianza en las 3 opciones (`confianza.nivel`) |
|---|---|---|---|---|
| **Jocotán**<br>`jocotan.json` | *Maíz + frijol*: **80 / 81 / 80 → Total 80**<br>Déficit: **16 %** (11–19 %) · Pérdida: **19 %** | *Maíz + canavalia*: **80 / 100 / 90 → Total 88**<br>Déficit: **16 %** (11–19 %) · Pérdida: **19 %** | *Sorgo + caupí*: **91 / 97 / 70 → Total 87**<br>Déficit: **9 %** (5–15 %) · Pérdida: **8 %** | **Alta** |
| **Camotán**<br>`camotan.json` | *Maíz + frijol*: **84 / 90 / 80 → Total 84**<br>Déficit: **12 %** (9–16 %) · Pérdida: **14 %** | *Maíz + canavalia*: **84 / 100 / 90 → Total 90**<br>Déficit: **12 %** (9–16 %) · Pérdida: **14 %** | *Sorgo + caupí*: **93 / 100 / 70 → Total 89**<br>Déficit: **6 %** (3–12 %) · Pérdida: **6 %** | **Baja** |
| **Olopa**<br>`olopa.json` | *Maíz + frijol*: **86 / 97 / 80 → Total 87**<br>Déficit: **11 %** (9–15 %) · Pérdida: **14 %** | *Maíz + canavalia*: **86 / 100 / 90 → Total 90**<br>Déficit: **11 %** (9–15 %) · Pérdida: **14 %** | *Maíz ciclo corto ICTA B-5*: **94 / 100 / 80 → Total 92**<br>Déficit: **5 %** (3–13 %) · Pérdida: **6 %** | **Media** |
| **San Juan Ermita**<br>`san_juan_ermita.json` | *Maíz + frijol*: **81 / 77 / 80 → Total 80**<br>Déficit: **15 %** (11–19 %) · Pérdida: **18 %** | *Maíz + canavalia*: **81 / 100 / 90 → Total 88**<br>Déficit: **15 %** (11–19 %) · Pérdida: **18 %** | *Sorgo + caupí*: **90 / 94 / 70 → Total 86**<br>Déficit: **9 %** (5–14 %) · Pérdida: **9 %** | **Alta** |
| **Zacapa**<br>`zacapa.json` | *Maíz + frijol*: **67 / 78 / 80 → Total 73**<br>Déficit: **25 %** (21–32 %) · Pérdida: **30 %** | *Maíz + canavalia*: **67 / 100 / 90 → Total 81**<br>Déficit: **25 %** (21–32 %) · Pérdida: **30 %** | *Sorgo + caupí*: **80 / 92 / 70 → Total 80**<br>Déficit: **19 %** (15–25 %) · Pérdida: **18 %** | **Baja** |

### Puntajes totales si cambias el selector «Qué sembró el último ciclo»:
- **Si eliges «Maíz solo (sin frijol)» (`{parcela}.maiz_solo.json`):**
  - Jocotán: **68 / 88 / 87** · Camotán: **72 / 90 / 89** · Olopa: **77 / 90 / 92** · San Juan Ermita: **68 / 88 / 86** · Zacapa: **58 / 81 / 80**.
- **Si eliges «Sorgo» (`{parcela}.sorgo.json`):**
  - Jocotán: **70 / 88 / 87** · Camotán: **73 / 90 / 89** · Olopa: **78 / 90 / 92** · San Juan Ermita: **71 / 88 / 86** · Zacapa: **64 / 81 / 80**.

---

## Sección 3. Vista *Evidence* — Recuadro «Observación preliminar: julio–agosto de 2026» (`validacion.json → observacion_2026`)

Al abrir *Evidence*, arriba del todo aparece el bloque de la observación de 2026. Despliega el detalle **«Ver cifras por parcela (CHIRPS y SMAP)»** y comprueba las dos tablas contra `web/public/data/validacion.json`:

### Tabla A: Lluvia de julio + agosto de 2026 en CHIRPS v3 (`observacion_2026.lluvia_chirps`, 35 años: 1991–2025)

| Parcela | Lluvia jul–ago 2026 (`mm_2026`) | Mediana 1991–2025 (`mediana_mm`) | % de la mediana (`pct_de_la_mediana`) | Mínimo anterior 1991–2025 (`minimo_anterior_mm` y año) | Años más secos que 2026 (`anios_mas_secos_que_2026`) |
|---|---|---|---|---|---|
| **Jocotán** | **78.7 mm** | **323.9 mm** | **24 %** | **138.1 mm** (**2018**) | **0 de 35** |
| **Camotán** | **93.9 mm** | **355.2 mm** | **26 %** | **154.4 mm** (**2018**) | **0 de 35** |
| **Olopa** | **106.4 mm** | **475.1 mm** | **22 %** | **211.0 mm** (**1997**) | **0 de 35** |
| **San Juan Ermita** | **69.2 mm** | **344.7 mm** | **20 %** | **140.3 mm** (**2018**) | **0 de 35** |
| **Zacapa** | **43.9 mm** | **206.1 mm** | **21 %** | **90.4 mm** (**2018**) | **0 de 35** |

### Tabla B: Humedad superficial del suelo SMAP en julio–agosto de 2026 (`observacion_2026.smap_celdas`, 2015–2026)

| Parcela(s) | Celda EASE-Grid 2.0 (9 km) | Media jul–ago 2026 (`m3m3_2026`) | Mínimo anterior 2015–2025 (`minimo_anterior_m3m3` y año) | Posición en los 12 años (`n_anios`) |
|---|---|---|---|---|
| **Jocotán, San Juan Ermita** | `(604, 970)` | **0.162 m³/m³** | **0.182 m³/m³** (**2015**) | **El más bajo de 12 años** |
| **Olopa** | `(606, 971)` | **0.180 m³/m³** | **0.216 m³/m³** (**2015**) | **El más bajo de 12 años** |
| **Zacapa** | `(602, 968)` | **0.152 m³/m³** | **0.172 m³/m³** (**2019**) | **El más bajo de 12 años** |

*(Y debajo debe indicar que **Camotán** en la celda `(603, 970)` no tiene mediciones con la calidad recomendada por NASA).*

---

## Sección 4. Vista *Evidence* — Paneles «Lo que ve el satélite» y «Clima de la zona» (`{parcela}.json`)

Al cambiar de parcela en *Evidence*, verifica en los dos paneles superiores:

| Parcela (`{parcela}.json`) | Altitud y pendiente (`parcela.terreno`) · Suelo (`parcela.suelo`) | Compuestos válidos MODIS (`deteccion.calidad`) y ciclos/año | Quemas VIIRS (`deteccion.quemas`) | Año más seco CHIRPS (`clima.anio_mas_seco`) y racha mediana canícula | POWER vs CHIRPS jul–ago (`clima.power_vs_chirps.jul_ago`) | Humedad SMAP jul–ago (`smap`) |
|---|---|---|---|---|---|---|
| **Jocotán** | **571 m**, pend. **11.1 %** · Arcilla **31.1 %**, C **29.0 g/kg**, pH **6.7** | **95.7 %** (**110/115**) · **1** ciclo/año | **3 de 15 años** (**6** det. a ≤ 1 km, radio **500 m**) | **2018** (**805 mm**) · racha mediana **7 días** (**2 de 25 años > 15 d**) | POWER **179.8** vs CHIRPS **171.9 mm/mes** · sesgo **+4.6 %**, $r = \mathbf{0.74}$ ($n = 50$) | **0.247 m³/m³** · 2026 es el más seco de **12 años** |
| **Camotán** | **829 m**, pend. **37.0 %** · Arcilla **34.4 %**, C **32.7 g/kg**, pH **6.6** | **80.9 %** (**93/115**) · **1** ciclo/año | **3 de 15 años** (**24** det. a ≤ 1 km, radio **500 m**) | **2018** (**901 mm**) · racha mediana **7 días** (**2 de 25 años > 15 d**) | POWER **179.8** vs CHIRPS **190.8 mm/mes** · sesgo **−5.8 %**, $r = \mathbf{0.74}$ ($n = 50$) | **Sin calidad recomendada** (**3 007** mediciones; respaldo mediana **0.64 m³/m³**) |
| **Olopa** | **980 m**, pend. **3.2 %** · Arcilla **34.8 %**, C **31.8 g/kg**, pH **6.5** | **93.0 %** (**107/115**) · **1** ciclo/año | **1 de 15 años** (**3** det. a ≤ 1 km, radio **500 m**) | **2002** (**1 147 mm**) · racha mediana **7 días** (**0 de 25 años > 15 d**) | POWER **181.6** vs CHIRPS **232.9 mm/mes** · sesgo **−22.1 %**, $r = \mathbf{0.71}$ ($n = 50$) | **0.274 m³/m³** · 2026 es el más seco de **12 años** |
| **San Juan Ermita** | **637 m**, pend. **8.3 %** · Arcilla **29.5 %**, C **32.0 g/kg**, pH **6.6** | **95.7 %** (**110/115**) · **2** ciclos/año | **2 de 15 años** (**11** det. a ≤ 1 km, radio **500 m**) | **2018** (**776 mm**) · racha mediana **8 días** (**1 de 25 años > 15 d**) | POWER **179.8** vs CHIRPS **175.2 mm/mes** · sesgo **+2.6 %**, $r = \mathbf{0.72}$ ($n = 50$) | **0.247 m³/m³** · 2026 es el más seco de **12 años** |
| **Zacapa** | **308 m**, pend. **35.3 %** · Arcilla **28.3 %**, C **30.5 g/kg**, pH **6.9** | **93.9 %** (**108/115**) · **1** ciclo/año | **0 de 15 años** (**0** det. a ≤ 1 km, radio **500 m**) | **2018** (**530 mm**) · racha mediana **9 días** (**3 de 25 años > 15 d**) | POWER **179.8** vs CHIRPS **115.7 mm/mes** · sesgo **+55.4 %**, $r = \mathbf{0.70}$ ($n = 50$) | **0.206 m³/m³** · 2026 es el más seco de **12 años** |

---

## Sección 5. Pestaña «Validación» (`web/public/data/validacion.json`)

Haz clic en la pestaña superior **«Validación»** de *Evidence* y comprueba estas cifras clave:

1. **Cifra pública de impacto 2018 (`evidencia_publica_2018`):**
   - Fuente: **FAO GIEWS Update – Central America, 27 de agosto de 2018** (citando estimación preliminar del MAGA del 13 de agosto de 2018).
   - Guatemala: **175 126 ha** perdidas y **1 290 785 personas** afectadas (y en El Salvador, Guatemala y Honduras juntos: **282 000 ha** y **2.2 millones** de personas).
2. **Tabla de la prueba de 2018 y los 20 años de prueba (2006–2025, `validacion.json → parcelas[].sequia_2018`):**

| Parcela | Puesto de 2018 en lluvia jul–ago (2001–2025) | ¿El motor marca 2018 con datos hasta 2017? | Déficit hídrico 2018 (`deficit_pct`) | Anomalía NDVI jul–ago 2018 (DE) | Anomalía SMAP jul–ago 2018 (DE) | Aciertos / Falsas alarmas / Fallos (4 años secos listados: 2014, 2015, 2018, 2019 en 20 años) | Spearman $\rho$ (déficit vs NDVI) |
|---|---|---|---|---|---|---|---|
| **Jocotán** | **1 de 25** | **Sí** | **35 %** | **−2.35 DE** | **−0.67 DE** | **3 / 2 / 1** | **+0.69** |
| **Camotán** | **1 de 25** | **Sí** | **32 %** | **+0.14 DE** | **sin datos** | **3 / 2 / 1** | **+0.45** |
| **Olopa** | **1 de 25** | **Sí** | **26 %** | **−0.14 DE** | **−1.06 DE** | **3 / 3 / 1** | **+0.07** |
| **San Juan Ermita** | **1 de 25** | **Sí** | **34 %** | **−1.13 DE** | **−0.67 DE** | **3 / 3 / 1** | **+0.45** |
| **Zacapa** | **1 de 25** | **Sí** | **43 %** | **−1.72 DE** | **−0.98 DE** | **3 / 2 / 1** | **+0.86** |

3. **Tabla POWER vs CHIRPS (2001–2025, todos los meses vs julio–agosto, `validacion.json → parcelas[].power_vs_chirps`):**
   - **Jocotán:** todos los meses **126.6 vs 100.6 mm/mes (+25.8 %)** · jul–ago **+4.6 %**, EAM **45.7 mm**, $r = \mathbf{0.74}$ · sesgo 1991–2000 **−20.7 %**.
   - **Camotán:** todos los meses **126.6 vs 111.5 mm/mes (+13.5 %)** · jul–ago **−5.8 %**, EAM **49.3 mm**, $r = \mathbf{0.74}$ · sesgo 1991–2000 **−27.9 %**.
   - **Olopa:** todos los meses **114.8 vs 129.6 mm/mes (−11.4 %)** · jul–ago **−22.1 %**, EAM **64.6 mm**, $r = \mathbf{0.71}$ · sesgo 1991–2000 **−44.3 %**.
   - **San Juan Ermita:** todos los meses **126.6 vs 96.9 mm/mes (+30.6 %)** · jul–ago **+2.6 %**, EAM **47.3 mm**, $r = \mathbf{0.72}$ · sesgo 1991–2000 **−17.2 %**.
   - **Zacapa:** todos los meses **126.6 vs 71.0 mm/mes (+78.2 %)** · jul–ago **+55.4 %**, EAM **69.2 mm**, $r = \mathbf{0.70}$ · sesgo 1991–2000 **+17.3 %**.

---

## Tabla para anotar el resultado y la hora real

| Fecha y hora real (ej. `2026-11-15 11:30`) | Bloque revisado en pantalla | Archivo(s) de `web/public/data/` contra los que se comprobó | ¿Todas las cifras coinciden sin errores ni `NaN`? (Sí / No) | Observaciones o discrepancias encontradas |
|---|---|---|---|---|
| | **1. Vista agricultor — Jocotán** (3 hechos + opciones + confianza) | `web/public/data/jocotan.json` | | |
| | **2. Vista agricultor — Camotán** (3 hechos + opciones + confianza) | `web/public/data/camotan.json` | | |
| | **3. Vista agricultor — Olopa** (3 hechos + 3 opciones parejas + confianza) | `web/public/data/olopa.json` | | |
| | **4. Vista agricultor — San Juan Ermita** (3 hechos + opciones + confianza) | `web/public/data/san_juan_ermita.json` | | |
| | **5. Vista agricultor — Zacapa** (3 hechos + opciones + confianza) | `web/public/data/zacapa.json` | | |
| | **6. Evidence — Tarjeta del agricultor y 3 rotaciones** (5 parcelas + variantes maíz solo y sorgo) | `jocotan.json`, `camotan.json`, `olopa.json`, `san_juan_ermita.json`, `zacapa.json` y `*.maiz_solo.json` / `*.sorgo.json` | | |
| | **7. Evidence — Observación preliminar julio–agosto 2026** (tablas CHIRPS y SMAP) | `web/public/data/validacion.json` (`observacion_2026`) | | |
| | **8. Evidence — Paneles «Lo que ve el satélite» y «Clima de la zona»** (5 parcelas) | `web/public/data/*.json` (`parcela`, `deteccion`, `clima`, `smap`) | | |
| | **9. Evidence — Pestaña «Validación» y «Dónde falla»** (FAO GIEWS 2018, 20 años de prueba, POWER vs CHIRPS) | `web/public/data/validacion.json` (`evidencia_publica_2018`, `parcelas`) | | |
