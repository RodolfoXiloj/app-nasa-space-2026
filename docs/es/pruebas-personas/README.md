# Pruebas con personas antes del envío — Equipo «A dream» (Milpa Resiliente)

Esta carpeta reúne las **7 guías paso a paso** para las pruebas que deben realizar los integrantes del equipo **«A dream»** (**Rodolfo Xiloj, Mario e Iván**) antes de cerrar el envío del domingo a **NASA Space Apps 2026**, junto con el reporte de **pruebas automáticas de apoyo** (`resultados-automaticos.md`).

> **Importante:** Las pruebas automáticas en `resultados-automaticos.md` sirven como apoyo técnico previo (verifican el árbol de accesibilidad en navegador, generan los PDF en Carta y escala de grises, validan los MP3/VTT, cruzan las cifras contra los JSON y cuentan palabras/caracteres), pero **no reemplazan a las pruebas con personas reales**. Cada integrante debe completar su tabla con el resultado observado y la **hora real**.

---

## Índice de archivos y quién hace qué

| Integrante | Archivo de guía | Qué prueba realiza | Tiempo estimado | Estado |
|---|---|---|---|---|
| **Rodolfo Xiloj** | [`rodolfo-formulario.md`](./rodolfo-formulario.md) | **1. Formulario de Space Apps y sección Members:** abrir el formulario oficial de envío, revisar los límites de caracteres o palabras de cada casilla frente a `docs/project-page-en.md` (con el conteo exacto ya calculado), verificar los enlaces públicos / FortiGuard y revisar la pestaña *Members* del equipo. | 15–20 min | `[ ] Pendiente` |
| **Rodolfo Xiloj** | [`rodolfo-talkback.md`](./rodolfo-talkback.md) | **2. TalkBack en un Android real:** servir la web en la red local, activar TalkBack en el teléfono, recorrer la vista del agricultor con un dedo (`→`), comprobar qué anuncia cada elemento frente a los textos alternativos del código y probar en Modo avión. | 20–25 min | `[ ] Pendiente` |
| **Rodolfo Xiloj** | [`rodolfo-impresion.md`](./rodolfo-impresion.md) | **3. Impresión en blanco y negro (tamaño Carta):** imprimir en papel (y de ser posible fotocopiar en B/N) la **Hoja de parcela** de la vista agricultor y la **Tarjeta del agricultor** de *Evidence*; comprobar que caben en 1 página sin cortes y que las formas y patrones se leen sin color. | 15–20 min | `[ ] Pendiente` |
| **Mario** | [`mario-audios.md`](./mario-audios.md) | **4. Escucha de los 15 audios y subtítulos:** escuchar los 15 audios activos de `web/public/audio/` (5 cortos en español, 5 cortos en inglés y 5 tarjetas en español en *Evidence*) siguiendo el texto exacto de cada subtítulo/tarjeta y marcar errores de pronunciación o sincronía. | 25–30 min | `[ ] Pendiente` |
| **Mario** | [`mario-cifras.md`](./mario-cifras.md) | **5. Verificación de cifras visibles contra JSON:** comprobar en pantalla cada cifra de las tarjetas de la vista del agricultor y de las secciones de *Evidence* (rotaciones, observación de 2026, satélite, clima y validación) frente a `web/public/data/*.json`. | 20–30 min | `[ ] Pendiente` |
| **Iván** | [`ivan-pictogramas.md`](./ivan-pictogramas.md) | **6. Prueba de comprensión de pictogramas con 3 a 5 adultos:** protocolo con consentimiento verbal, cero datos personales y preguntas abiertas sin explicar antes para verificar si se entienden los iconos de los 3 hechos, las formas del semáforo, la rueda de 12 meses y las cuadrículas de años. | 20–30 min | `[ ] Pendiente` |
| **Iván** | [`ivan-ingles.md`](./ivan-ingles.md) | **7. Lectura del inglés en voz alta:** guion para leer en voz alta los textos en inglés de la vista del agricultor, el resumen y página del proyecto (`docs/project-page-en.md`) y las 7 diapositivas (`docs/slides/index.html`), marcando frases largas, trabas o expresiones poco naturales. | 25–35 min | `[ ] Pendiente` |
| *(Apoyo automático)* | [`resultados-automaticos.md`](./resultados-automaticos.md) | **Reporte de pruebas automáticas (Parte B):** resultados reales corridos en la máquina con hora exacta y comando usado (árbol de accesibilidad a 360 px con Playwright, PDF de impresión en Carta y escala de grises, verificación de MP3/VTT, cruce de cifras contra JSON y conteo de `docs/project-page-en.md`). | Ya ejecutado | `[x] Completado` |

---

## Orden recomendado antes de enviar el domingo

1. **En paralelo:**
   - **Mario** realiza [`mario-audios.md`](./mario-audios.md) y [`mario-cifras.md`](./mario-cifras.md).
   - **Iván** realiza [`ivan-pictogramas.md`](./ivan-pictogramas.md) (con 3 a 5 adultos) e [`ivan-ingles.md`](./ivan-ingles.md).
   - **Rodolfo** realiza [`rodolfo-talkback.md`](./rodolfo-talkback.md) y [`rodolfo-impresion.md`](./rodolfo-impresion.md).
2. **Cierre conjunto con [`rodolfo-formulario.md`](./rodolfo-formulario.md):**
   - Con los resultados de la impresión en papel (Rodolfo) y de la comprensión de pictogramas con 3 a 5 adultos (Iván), **Rodolfo** actualiza las tres frases de *«pending test»* en el formulario de Space Apps, verifica la pestaña **Members** (para que los nombres de integrantes coincidan con **Rodolfo Xiloj, Mario e Iván**) y guarda el envío final.
