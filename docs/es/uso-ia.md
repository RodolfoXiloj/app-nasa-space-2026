# Uso de IA (Super Intelligence, SI) en Milpa Resiliente

La declaración para la entrega, en inglés, está en [../ai-use.md](../ai-use.md).

## En un párrafo

Un agente de código de IA (Claude, de Anthropic) escribió la mayor parte del código, la mayor parte de los textos en los dos idiomas y el código SVG de los pictogramas, siempre bajo la dirección y la revisión del equipo. Un agente de investigación con búsqueda web encontró las fuentes agronómicas y, el 14 de noviembre, las cifras de impacto y el estado de cada sensor; cada cifra que usamos lleva su URL, y las que no se pudieron confirmar quedaron fuera. Antes de construir, un asistente de IA comparó esta idea con otras cinco; el equipo eligió. El equipo decidió el alcance, las cinco parcelas, los umbrales del semáforo, la regla de empate y la regla de validación. El audio usa voces sintéticas (edge-tts: es-GT-MartaNeural y en-US-JennyNeural), rotuladas como generadas con IA junto al reproductor y en las etiquetas de cada mp3. Ninguna IA produce cifras que vea la persona usuaria: las cifras salen de los datos y de reglas en el código, y los textos salen de plantillas fijas revisadas por un validador que rechaza cualquier cifra que no esté en la salida del motor. Es el mismo texto del campo SI del formulario ([../project-page-en.md](../project-page-en.md)), en español.

La guía de Space Apps 2026 pide describir cómo se usó la IA. Cada integrante anota aquí lo que use, con fecha.

La fecha de cada fila es la del commit en que ese trabajo entró a este repo (`git log`); no indica cuándo se hizo.

## Regla del proyecto

Ninguna cifra que ve el agricultor o el técnico la genera una IA. Los números salen de datos (NASA y otras fuentes citadas) y de reglas escritas en el código (`motor/`). Los textos de la tarjeta salen de plantillas deterministas; si en algún momento un modelo de lenguaje los reescribe, un validador (`motor/redaccion.py`) rechaza cualquier cifra que no esté en el JSON del motor y cualquier fecha de siembra que no venga de ZARC, y se vuelve a la plantilla.

## Registro

| Fecha | Quién | Herramienta | Para qué | Qué revisó una persona |
|---|---|---|---|---|
| Por confirmar (archivo fuera de git) | Rodolfo | Asistente de IA | Evaluación de la idea y comparación con otras 5 (`docs/evaluacion-milpa-ajustada.txt`) | Pendiente de completar |
| 14 nov 2026 | Rodolfo | Claude (Anthropic), asistente de código | Plan de construcción; esqueleto del repo, clientes de datos, motor, pruebas y web | Pendiente: revisión del equipo |
| 14 nov 2026 | Rodolfo | Claude (Anthropic), asistente de código | Segundo bloque: elección de puntos con NDVI e imagen, CHIRPS v3 (lector propio), FIRMS 2026, cliente de SMAP, validación, capas sin red, memoria y pruebas | Pendiente: revisión del equipo; cada prueba está en `docs/es/pruebas.md` |
| 14 nov 2026 | Rodolfo | Claude (Anthropic), subagente de investigación con búsqueda web | Buscar y leer fuentes de Kc, Ky, rotaciones, ZARC y pérdidas de 2018; cada cita marcada como verificada o no verificada | Las citas se revisaron contra los documentos; las no verificadas quedan rotuladas en `data/fuentes.yaml` |
| 14 nov 2026 | Rodolfo | edge-tts (voz neural de Microsoft) | Audio mp3 de la tarjeta, voz es-GT-MartaNeural | Solo lee el texto que generó el motor |
| 14 nov 2026 | Rodolfo | Claude (Anthropic), agente de investigación con búsqueda web | Cifras de impacto, herramientas que ya existen y estado de cada sensor (Suomi NPP, Terra, CHIRPS v3, POWER) | El equipo decidió qué cifras usar; las que el agente marcó como dudosas quedaron fuera. Cada cifra tiene su URL en [../impact.md](../impact.md) ([impacto.md](impacto.md) en español) |
| 14 nov 2026 | Rodolfo | Claude (Anthropic), agente de código | Revisó la coherencia de los documentos con el código y los datos y redactó las correcciones | Rodolfo aprueba cada merge a `main` |
| 14 nov 2026 (noche) | Rodolfo | Claude (Anthropic), agente de código, y un subagente con búsqueda web | Versión interactiva (rama `v2-interactiva`): plan a partir de dos investigaciones (verificó qué se sostenía), exportes del motor para el explorador, huellas de cada satélite, comparador de fechas, relieve y vista 3D, gráficas nuevas, biblioteca de plantillas, audio que marca el hecho, imagen para WhatsApp y uso sin señal; pruebas de Python y de navegador para cada pieza; una revisión independiente del código por otro agente | Rodolfo decide a las 09:00 del domingo si se lanza (`docs/es/plan-version-interactiva.md`, sección 12); ninguna cifra nueva sale de un modelo de lenguaje: todas salen del motor o de la caché y las cubren pruebas |

## Por declarar en la entrega

- Asistentes de código usados por cada integrante.
- Modelo de lenguaje para redactar textos, si se usa al exportar (hoy no se usa: solo plantillas).
- Voz: mp3 generado con `edge-tts` (voz neural sintética es-GT) al exportar; si no hay mp3, la del navegador (`speechSynthesis`).
- **Falta revisar:** ninguna persona ha vuelto a abrir todavía cada página detrás de las cifras de impacto agregadas el 14 de noviembre.
- **Declarado en los 5 mp3 (14 nov 2026):** la web dice junto al reproductor y en el pie que es voz sintética generada con IA, y cada archivo lleva etiquetas ID3 (`TPE1`, `COMM` y `TXXX:AI_GENERATED`; `motor/audio_id3.py`). La prueba de humo falla si un mp3 no tiene la etiqueta; un mp3 solo se enlaza si fue generado con el texto actual de la tarjeta.
