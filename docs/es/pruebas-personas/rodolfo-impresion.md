# Guía 3 para Rodolfo Xiloj: Impresión en blanco y negro (tamaño carta) de la hoja de parcela y la tarjeta del agricultor

**Responsable:** Rodolfo Xiloj  
**Componentes probados:**  
1. **Hoja de parcela de la vista agricultor** (`web/src/kit/Kit.jsx` + `web/src/kit/kit.css`)  
2. **Tarjeta del agricultor en la vista Evidence** (`web/src/components/Tarjeta.jsx` + `web/src/styles.css`)  
**Tiempo estimado:** 15 a 20 minutos  

> **Por qué hace falta una persona:** Las pruebas automáticas con Playwright ya generaron los PDF en tamaño Carta y escala de grises y comprobaron que caben en 1 página sin recortes horizontales. Sin embargo, solo una impresión física en papel (y de preferencia una fotocopia en blanco y negro de esa hoja) confirma si los tres patrones de la rueda de meses (punteado, rayado y sólido), las tres formas geométricas del semáforo y el tamaño de letra se distinguen con claridad en papel real bajo luz normal.

---

## Qué dos documentos vas a imprimir

En Milpa Resiliente hay **dos vistas imprimibles distintas**, diseñadas para caber en **1 sola página tamaño Carta (Letter, 8.5 × 11 pulgadas)** en **blanco y negro**:

1. **La Hoja de parcela (desde la vista del agricultor, primera pantalla):**
   - Pensada para entregar en mano al agricultor o pegar en el cuaderno comunitario.
   - Contiene: el nombre del municipio, los 3 hechos del semáforo con su figura geométrica (círculo, triángulo o cuadrado), su palabra (*Bien*, *Atención*, *Se repite*), su pictograma (la rueda de 12 meses y las cuadrículas de 15 y 25 años), las opciones de cultivo, el nivel de confianza y el aviso de que no es alerta oficial.
2. **La Tarjeta del agricultor (desde la vista *Evidence*):**
   - Pensada para el técnico extensionista y el agricultor.
   - Contiene: encabezado de la parcela y fecha, lo que ve el satélite, la tabla comparativa de las 3 rotaciones con sus puntajes (*Agua*, *Suelo*, *Plagas*, *Total* y *Confianza*), la conclusión según prioridad, la cita textual de fechas de siembra de ZARC (con la URL completa de ZARC visible solo al imprimir) y el texto completo del guion de audio.

---

## Paso a paso

### Parte 1. Imprimir la «Hoja de parcela» (vista del agricultor)

1. Abre la aplicación web en Chrome o Edge (`http://localhost:4173/`).
2. Arriba a la derecha, selecciona **«Español»** y en el selector **Parcela** deja **«Jocotán, Chiquimula»** (puedes repetir con **Olopa** o **Zacapa** para ver los 3 estados del semáforo: círculo *Bien*, triángulo *Atención* y cuadrado *Se repite*).
3. Baja hasta la sección **«Compartir esta parcela»** y haz clic en el botón **«Imprimir hoja»**.
4. En la ventana de impresión del navegador, ajusta:
   - **Destino:** tu impresora física (o *Guardar como PDF* si vas a llevar el archivo a imprimir/fotocopiar).
   - **Color:** **Blanco y negro** (o *Escala de grises*).
   - **Tamaño de papel:** **Carta (Letter)**.
   - **Márgenes:** **Predeterminados**.
   - **Escala:** **Predeterminada (100 %)**.
5. Imprime la hoja en papel (y si tienes fotocopiadora o multifuncional a mano, sácale una fotocopia en blanco y negro).

### Parte 2. Imprimir la «Tarjeta del agricultor» (vista *Evidence*)

1. En la misma página, baja al final y haz clic en **«Ver la evidencia (Mapa, gráficas, fuentes y límites)»**.
2. Baja hasta la sección **«Tarjeta para el agricultor»** (debajo de las tres tarjetas de rotaciones).
3. Haz clic en el botón **«Imprimir / guardar PDF»** que está dentro de la tarjeta.
4. En la ventana de impresión del navegador, verifica la misma configuración:
   - **Color:** **Blanco y negro** (*Escala de grises*).
   - **Tamaño de papel:** **Carta (Letter)**.
   - **Márgenes:** **Predeterminados**.
5. Imprime la hoja en papel.

---

## Lista de verificación visual en el papel impreso (qué revisar)

Revisa cada hoja física con esta lista:

### A. En la «Hoja de parcela» (vista agricultor)
1. **Cabe en 1 sola página Carta:** No sale una segunda hoja en blanco ni con el aviso final suelto.
2. **Se ocultó el resto de la interfaz:** En el papel **no** aparecen los botones `English / Español`, ni el selector desplegable de parcela, ni el reproductor de audio, ni los botones `Imprimir hoja / Descargar audio / Compartir por WhatsApp`, ni el botón `Ver la evidencia`.
3. **Semáforo legible sin color (forma + palabra):**
   - **Se repite (rojo en pantalla):** se distingue claramente como un **cuadrado con signo `!`** acompañado de la palabra **«Se repite»**.
   - **Atención (amarillo en pantalla):** se distingue claramente como un **triángulo con signo `!`** acompañado de la palabra **«Atención»**.
   - **Bien (verde en pantalla, ej. Canícula en Olopa o Quema en Zacapa):** se distingue claramente como un **círculo con marca `✓`** acompañado de la palabra **«Bien»**.
4. **Rueda de 12 meses (`RuedaMeses`) legible en blanco y negro:**
   - Los meses de **suelo desnudo** (marzo y abril en Jocotán) tienen **punteado con borde grueso**.
   - Los meses de **poca cobertura** (febrero y mayo en Jocotán) tienen **rayado diagonal**.
   - Los meses **cubiertos** (junio a enero) tienen **relleno oscuro continuo**.
   - Verifica que en el papel en blanco y negro se distingan los **tres patrones** sin necesidad de color, y que las letras de los 12 meses (`E, F, M, A...`) se lean sin encimarse.
5. **Cuadrículas de años (`PuntosAnios` de 15 y 25 años):**
   - En Quema (3 de 15 años) se distinguen 3 cuadros rellenos con marca interior frente a 12 cuadros vacíos.
   - En Canícula (2 de 25 años) se distinguen 2 cuadros rellenos con marca interior frente a 23 cuadros vacíos.
6. **Sin cortes en los bordes:** Ningún texto, borde o dibujo queda mordido a la izquierda o derecha de la hoja.

### B. En la «Tarjeta del agricultor» (vista *Evidence*)
1. **Cabe en 1 sola página Carta:** Toda la tarjeta `.tarjeta` sale en una sola página y no se corta la tabla de rotaciones a la mitad.
2. **Se ocultó el resto de *Evidence*:** En el papel **no** salen el mapa Leaflet, ni el panel de satélite, ni las gráficas de clima/escenarios, ni las pestañas superiores, ni el reproductor `<audio>` ni el botón *Imprimir / guardar PDF*.
3. **Tabla de las 3 rotaciones completa y legible en blanco y negro:**
   - Las 6 columnas (*Opción, Agua, Suelo, Plagas, Total, Confianza*) entran completas en el ancho del papel sin cortarse a la derecha.
   - Los números (`80, 88, 87` en Jocotán) y las etiquetas de confianza (`Alta`) tienen contraste negro sobre blanco.
4. **URL de ZARC impresa en texto:** Debajo de *Fecha de siembra*, donde en pantalla solo había un enlace clicable, en el papel impreso aparece visible la dirección completa: `ZARC (FAO–MAGA): https://zarc.maga.gob.gt/` (clase `.solo-imprimir`).

---

## Tabla para anotar el resultado y la hora real

| Fecha y hora real (ej. `2026-11-15 11:00`) | Documento impreso y parcela | Impresora usada / ¿Se sacó fotocopia B/N? | ¿Cabe en 1 sola página Carta sin cortes? (Sí / No) | ¿Se distinguen sin color las 3 formas y los 3 patrones (punteado, rayado, sólido)? (Sí / No) | ¿Se ocultaron botones/mapa y salió impresa la URL de ZARC? (Sí / No) | Observaciones o ajustes necesarios |
|---|---|---|---|---|---|---|
| | **1. Hoja de parcela** (Vista agricultor — Jocotán, Español) | | | | | |
| | **2. Hoja de parcela** (Vista agricultor — Olopa o Zacapa, para ver círculo *Bien*) | | | | | |
| | **3. Fotocopia en B/N de la Hoja de parcela** (prueba de contraste real) | | | | | |
| | **4. Tarjeta del agricultor** (Vista *Evidence* — Jocotán, Español) | | | | | |
| | **5. Tarjeta del agricultor** (Vista *Evidence* — Inglés, opcional) | | | | | |
