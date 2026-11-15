# Guía 3 para Rodolfo Xiloj: Impresión en blanco y negro (tamaño carta) de la hoja de parcela y la tarjeta del agricultor

**Responsable:** Rodolfo Xiloj  
**Componentes probados:**  
1. **Hoja de parcela de la vista agricultor** (`web/src/kit/Kit.jsx` + `web/src/kit/kit.css`)  
2. **Tarjeta del agricultor en la vista Evidence** (`web/src/components/Tarjeta.jsx` + `web/src/styles.css`)  
**Tiempo estimado:** 15 a 20 minutos  

> **Por qué hace falta una persona:** Las pruebas automáticas con Playwright ya generaron los PDF en tamaño Carta y escala de grises y comprobaron que caben en 1 página sin recortes horizontales. Sin embargo, solo una impresión física en papel (y de preferencia una fotocopia en blanco y negro de esa hoja) confirma si los tres rellenos de la rueda de meses (negro, rayado y blanco), las tres formas geométricas del semáforo y el tamaño de letra se distinguen con claridad en papel real bajo luz normal.

---

## Qué dos documentos vas a imprimir

En Milpa Resiliente hay **dos vistas imprimibles distintas**, diseñadas para caber en **1 sola página tamaño Carta (Letter, 8.5 × 11 pulgadas)** en **blanco y negro**:

1. **La Hoja de parcela (desde la vista del agricultor, primera pantalla):**
   - Pensada para entregar en mano al agricultor o pegar en el cuaderno comunitario.
   - Contiene: el título «MILPA RESILIENTE · HOJA DE LA PARCELA», el municipio, los 3 hechos del semáforo con su figura (círculo, triángulo o cuadrado), su palabra (*Bien*, *Atención*, *Se repite*), su dibujo (la rueda de 12 meses y los discos de 15 y 25 años), la frase de cada hecho y su fuente, la línea «Formas: círculo = bien, triángulo = atención, cuadrado = se repite, ? = sin dato», las opciones, «Qué tan seguros estamos», el aviso «No es un aviso oficial: platíquelo con su técnico», la línea de uso de IA y la dirección de la página.
2. **La Tarjeta del agricultor (desde la vista *Evidence*):**
   - Pensada para el técnico extensionista y el agricultor.
   - Contiene: encabezado de la parcela (coordenada, cultivo de hoy y prioridad), lo que ve el satélite, la tabla comparativa de las 3 rotaciones con sus puntajes (*Agua*, *Suelo*, *Plagas*, *Total* y *Confianza*), por qué la opción con mejor puntaje, la fecha de siembra citada de ZARC (con la URL completa visible solo al imprimir), el aviso de que la herramienta apoya y no reemplaza, las fuentes de datos y la línea de uso de IA. El guion del audio no se imprime.

---

## Paso a paso

### Parte 1. Imprimir la «Hoja de la parcela» (vista del agricultor)

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

### Parte 2. Imprimir la «Tarjeta para el agricultor» (vista *Evidence*)

1. En la misma página, baja al final y haz clic en **«Ver la evidencia»**.
2. Baja hasta la sección **«Tarjeta para el agricultor»** (debajo de las tres tarjetas de rotaciones).
3. Haz clic en el botón **«Imprimir o guardar PDF»**, arriba de la tarjeta, junto al reproductor de audio.
4. En la ventana de impresión del navegador, verifica la misma configuración:
   - **Color:** **Blanco y negro** (*Escala de grises*).
   - **Tamaño de papel:** **Carta (Letter)**.
   - **Márgenes:** **Predeterminados**.
5. Imprime la hoja en papel.

---

## Lista de verificación visual en el papel impreso (qué revisar)

Revisa cada hoja física con esta lista:

### A. En la «Hoja de la parcela» (vista agricultor)
1. **Cabe en 1 sola página Carta:** No sale una segunda hoja en blanco ni con el aviso final suelto.
2. **Se ocultó el resto de la interfaz:** En el papel **no** aparecen los botones `English / Español`, ni el selector desplegable de parcela, ni el reproductor de audio, ni los botones `Imprimir hoja / Descargar audio / Compartir por WhatsApp`, ni el botón `Ver la evidencia`.
3. **Semáforo legible sin color (forma + palabra):**
   - Las figuras son lisas, sin signos dentro: la palabra de al lado dice el estado.
   - **Se repite (rojo en pantalla):** se distingue claramente como un **cuadrado** acompañado de la palabra **«Se repite»**.
   - **Atención (amarillo en pantalla):** se distingue claramente como un **triángulo** acompañado de la palabra **«Atención»**.
   - **Bien (verde en pantalla, ej. Canícula en Olopa o Quema en Zacapa):** se distingue claramente como un **círculo** acompañado de la palabra **«Bien»**.
   - Debajo de los tres hechos sale la línea **«Formas: círculo = bien, triángulo = atención, cuadrado = se repite, ? = sin dato.»**
4. **Rueda de 12 meses (`RuedaMeses`) legible en blanco y negro:**
   - Los meses de **suelo desnudo** (marzo y abril en Jocotán) van en **negro sólido**.
   - Los meses de **poca cobertura** (febrero y mayo en Jocotán) tienen **rayado diagonal**.
   - Los meses **cubiertos** (junio a enero) van en **blanco con borde**.
   - Verifica que en el papel en blanco y negro se distingan los **tres rellenos** sin necesidad de color, y que las letras de los 12 meses (`E, F, M, A...`) se lean sin encimarse.
5. **Discos de años (`PuntosAnios` de 15 y 25 años):**
   - En Quema (3 de 15 años) se distinguen 3 discos negros con una llama blanca dentro frente a 12 aros vacíos.
   - En Canícula (2 de 25 años) se distinguen 2 discos negros con un sol blanco dentro frente a 23 aros vacíos.
6. **Sin cortes en los bordes:** Ningún texto, borde o dibujo queda mordido a la izquierda o derecha de la hoja.

### B. En la «Tarjeta para el agricultor» (vista *Evidence*)
1. **Cabe en 1 sola página Carta:** Toda la tarjeta `.tarjeta` sale en una sola página y no se corta la tabla de rotaciones a la mitad.
2. **Se ocultó el resto de *Evidence*:** En el papel **no** salen el mapa Leaflet, ni el panel de satélite, ni las gráficas de clima/escenarios, ni las pestañas superiores, ni el reproductor `<audio>` ni el botón *Imprimir o guardar PDF*.
3. **Tabla de las 3 rotaciones completa y legible en blanco y negro:**
   - Las 6 columnas (*Opción, Agua, Suelo, Plagas, Total, Confianza*) entran completas en el ancho del papel sin cortarse a la derecha.
   - Los números (`80, 88, 87` en Jocotán) y las etiquetas de confianza (`Alta`) tienen contraste negro sobre blanco.
4. **URL de ZARC impresa en texto:** Debajo de *Fecha de siembra*, donde en pantalla solo había un enlace clicable, en el papel impreso aparece entre paréntesis la dirección completa: `(https://www.maga.gob.gt/herramienta-digital-zarc-mejorara-decisiones-de-siembra/)` (clase `.solo-imprimir`).

---

## Tabla para anotar el resultado y la hora real

| Fecha y hora real (ej. `2026-11-15 11:00`) | Documento impreso y parcela | Impresora usada / ¿Se sacó fotocopia B/N? | ¿Cabe en 1 sola página Carta sin cortes? (Sí / No) | ¿Se distinguen sin color las 3 formas y los 3 rellenos (negro, rayado, blanco)? (Sí / No) | ¿Se ocultaron botones/mapa y salió impresa la URL de ZARC? (Sí / No) | Observaciones o ajustes necesarios |
|---|---|---|---|---|---|---|
| | **1. Hoja de parcela** (Vista agricultor — Jocotán, Español) | | | | | |
| | **2. Hoja de parcela** (Vista agricultor — Olopa o Zacapa, para ver círculo *Bien*) | | | | | |
| | **3. Fotocopia en B/N de la Hoja de parcela** (prueba de contraste real) | | | | | |
| | **4. Tarjeta del agricultor** (Vista *Evidence* — Jocotán, Español) | | | | | |
| | **5. Tarjeta del agricultor** (Vista *Evidence* — Inglés, opcional) | | | | | |
