# Guía 1 para Rodolfo Xiloj: Formulario de envío de NASA Space Apps y sección Members

**Responsable:** Rodolfo Xiloj  
**Archivo de referencia del proyecto:** `docs/project-page-en.md`  
**Tiempo estimado:** 15 a 20 minutos  

> **Por qué hace falta una persona:** El formulario oficial de NASA Space Apps solo puede abrirlo un integrante con sesión iniciada en `spaceappschallenge.org`. Los límites exactos de caracteres o palabras de cada casilla están únicamente dentro de esa plataforma y no están publicados en el repositorio.

---

## Qué necesitas antes de empezar

1. Tu cuenta de **NASA Space Apps Challenge 2026** con acceso a la página del equipo **«A dream»**.
2. El archivo `docs/project-page-en.md` abierto en tu computadora (contiene los textos listos en inglés para copiar y pegar).
3. La URL pública donde quedará desplegada la aplicación web (para el campo *Link to Final Project* y para revisar su categoría en FortiGuard).

---

## Conteo actual de `docs/project-page-en.md` (calculado automáticamente como apoyo)

Recalculado con un script sobre `main` en el commit `78de49a`, el `2026-11-14T16:54:51-06:00` (palabras = `split()`; caracteres del bloque sin su título `## ...`). Si `docs/project-page-en.md` cambia, hay que volver a contar.

Usa esta tabla como referencia inmediata mientras miras el contador de cada casilla en el formulario web de Space Apps:

| # | Campo del formulario (`docs/project-page-en.md`) | Palabras actuales | Caracteres (con espacios) | Caracteres (sin espacios) | Notas para pegar |
|---|---|---|---|---|---|
| 1 | **Project Name** | 2 | 16 | 15 | Texto: `Milpa Resiliente` |
| 2a | **High-Level Project Summary** *(versión principal)* | 306 | 1 776 | 1 471 | Pega esta primero. Si el formulario corta o pide menos caracteres/palabras, usa la **2b (Short version)**. |
| 2b | **High-Level Project Summary — Short version** *(respaldo)* | 161 | 973 | 813 | Úsala solo si la versión principal (2a) supera el límite del campo en la plataforma. |
| 3 | **Link to Project Demo** | 1 | 100 | 100 | URL del PDF de las 7 diapositivas en GitHub (`https://github.com/RodolfoXiloj/challenge-space-apps-2026/blob/main/docs/slides/milpa-resiliente.pdf`). |
| 4 | **Link to Final Project** | *(4 en borrador)* | *(20 en borrador)* | *(17 en borrador)* | Hoy dice `TBD: public site URL`. Reemplázalo por la URL pública real donde abren la vista del agricultor y *Evidence*. |
| 5 | **Detailed Project Description** | 1 376 | 8 037 | 6 654 | Incluye 8 bloques: *What it does*, *How it works*, *Local roots*, *How we test the rotations against the future*, *How we checked it*, *Benefits*, *Limits we state openly* y *Tools*. |
| 6 | **Use of Super Intelligence (SI)** | 199 | 1 183 | 985 | Declaración honesta de uso de IA (Claude, agente de búsqueda, voces sintéticas `edge-tts` y validador determinista). |
| 7 | **NASA Data** | 385 | 2 266 | 1 882 | Lista de los 8 productos de la NASA usados (MODIS MOD13Q1, FIRMS VIIRS, GPM IMERG vía CHIRPS v3, NASA POWER, SMAP SPL3SMP_E, SRTM GL3, NASA GIBS y NEX-GDDP-CMIP6), con la prueba de CHIRPS «sat» contra «rnl». |
| 8 | **Space Agency Partner Data and Other References** | 130 | 991 | 862 | Sentinel-2 (ESA Copernicus / EOX), CHIRPS v3, SoilGrids, OpenStreetMap, FAO-56/33/66, ZARC (FAO–MAGA), GIEWS 2018, FEWS NET 2026, SESAN, Oxfam, Kuxur Rum, ALMG, software y enlace al repo. |

---

## Paso a paso

### Paso 1. Abrir la página del equipo y revisar la pestaña «Members»
1. Entra a `https://www.spaceappschallenge.org/`, inicia sesión y abre la página del equipo **«A dream»**.
2. Ve a la pestaña **Members** (Integrantes).
3. Verifica quiénes están registrados oficialmente en el equipo dentro de la plataforma:
   - El equipo actual está conformado por **Rodolfo Xiloj, Mario e Iván**.
   - Comprueba en la pestaña **Members** si solo están Rodolfo Xiloj, Mario e Iván (o quiénes figuran con cuenta aceptada) para que la lista de integrantes en el formulario, el README y la lámina 7 coincidan exactamente con el registro oficial del equipo antes de enviar.

### Paso 2. Revisar los límites de cada campo del formulario («Project Submission»)
1. Abre la pestaña **Project** (o *Edit Project* / *Project Submission*).
2. Para cada campo del formulario, mira debajo o al lado de la caja de texto qué límite muestra la plataforma (por ejemplo: *«Max 1000 characters»*, *«Max 250 words»*, etc.) y anótalo en la tabla de resultados al final de esta guía.
3. Pega el bloque correspondiente de `docs/project-page-en.md` (sin copiar el título `## ...` del archivo Markdown) y verifica que no se corte ni una sola palabra al final.
4. En **High-Level Project Summary**:
   - Prueba primero el párrafo completo (**306 palabras / 1 776 caracteres con espacios**).
   - Si el formulario marca exceso de longitud o recorta el final, bórralo y pega el bloque **Short version** (**161 palabras / 973 caracteres con espacios**).

### Paso 3. Comprobar los enlaces públicos y FortiGuard
1. En **Link to Project Demo**, verifica que el enlace `https://github.com/RodolfoXiloj/challenge-space-apps-2026/blob/main/docs/slides/milpa-resiliente.pdf` abra sin pedir inicio de sesión (pruébalo en una ventana de incógnito).
2. En **Link to Final Project**, pega la URL pública de la aplicación desplegada y ábrela en ventana de incógnito para confirmar que carga directo en inglés (`lang="en"`).
3. Entra a `https://www.fortiguard.com/webfilter` y pega la URL pública del sitio para comprobar que tiene categoría asignada y no aparece como *Unrated* o bloqueada (requisito de la guía de envío cuando se usa un dominio propio o de alojamiento gratuito).

### Paso 4.Actualizar las frases de pruebas pendientes (cuando Mario, Iván y tú terminen)
En `docs/project-page-en.md` hay tres frases escritas con honestidad porque al redactar el borrador aún faltaban las pruebas humanas:
- En *High-Level Project Summary*: `(the comprehension test with farmers is still pending)` / `Comprehension tests with farmers are still pending.`
- En *Detailed Project Description → Benefits*: `a real photocopy and a test with users are still pending.`
- En *Detailed Project Description → Limits we state openly*: `The pictograms still need a comprehension test with users.`

Una vez que tú termines las pruebas 2 y 3 (TalkBack e impresión/fotocopia) e Iván termine la prueba 6 (comprensión de pictogramas con 3 a 5 adultos), actualiza esas líneas en el formulario con el resultado real (por ejemplo, cuántas personas participaron y qué se observó) antes de pulsar el envío definitivo.

---

## Tabla para anotar el resultado y la hora real

Completa esta tabla mientras revisas el formulario:

| Fecha y hora real (ej. `2026-11-15 09:30`) | Campo o sección revisada | Límite que muestra Space Apps (caracteres o palabras) | Conteo actual en `docs/project-page-en.md` | ¿Cabe completo sin recortarse? (Sí / No) | Qué versión o ajuste se dejó pegado / Observaciones |
|---|---|---|---|---|---|
| | **Sección Members** (integrantes registrados en Space Apps) | N/A | Texto actual dice: `Rodolfo Xiloj, Mario, Iván` | | ¿Quiénes aparecen en Members?: |
| | **Project Name** | | 2 palabras / 16 caracteres | | |
| | **High-Level Project Summary** | | Principal: 306 pal. / 1 776 car.<br>Corta: 161 pal. / 973 car. | | ¿Se usó la principal o la versión corta?: |
| | **Link to Project Demo** | | 1 palabra / 100 caracteres | | ¿Abre en ventana de incógnito sin login?: |
| | **Link to Final Project** | | URL pública definitiva | | URL pegada y categoría en FortiGuard: |
| | **Detailed Project Description** | | 1 376 palabras / 8 037 caracteres | | |
| | **Use of Super Intelligence (SI)** | | 199 palabras / 1 183 caracteres | | |
| | **NASA Data** | | 385 palabras / 2 266 caracteres | | |
| | **Space Agency Partner Data and Other References** | | 130 palabras / 991 caracteres | | |
| | **Frases de pruebas pendientes** (fotocopia y pictogramas) | N/A | 3 menciones en el borrador | | ¿Actualizadas tras las pruebas de Rodolfo e Iván?: |
