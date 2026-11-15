# Preguntas para el agricultor y el extensionista

Lo que el equipo necesita preguntar en la zona para cerrar lo que el satélite no puede decir. Cada pregunta dice **para qué sirve** y **qué archivo cambia** con la respuesta. Las cifras de «lo que dice hoy el sitio» salen de `web/public/data/` (corrida del 14 nov 2026).

Tiempo: unos 40 minutos con un agricultor y 20 con un extensionista. Si solo hay 10 minutos, haga las ocho preguntas marcadas con **★**.

## Antes de empezar

- **Diga qué es:** «Es una herramienta de estudiantes para un concurso de la NASA. No es un aviso oficial ni una recomendación. Quiero saber si lo que el satélite vio se parece a lo que usted vivió.»
- **Pida permiso de palabra** y diga que puede parar cuando quiera.
- **Cero datos personales:** no anote nombres, teléfonos, edad exacta ni la ubicación de la casa. Identifique cada conversación como `Agricultor 1`, `Agricultor 2`, `Extensionista 1`. Anote solo: fecha, municipio y aldea, y si es agricultor o extensionista.
- **Pregunte primero y muestre después.** En los bloques 2, 3 y 4 no enseñe la pantalla hasta tener la respuesta: si la ve antes, repetirá lo que dice el sitio.
- **No corrija ni explique** mientras responde. Si lo que cuenta no coincide con el sitio, eso es justo lo que hay que anotar.
- **Lleve:** el teléfono con el sitio abierto (vista del agricultor, en español), la hoja de parcela impresa en blanco y negro y esta guía.
- La prueba de los dibujos tiene su propio guion: `docs/es/pruebas-personas/ivan-pictogramas.md`. Aquí solo se repite lo mínimo (bloque 6).

## Lo que dice hoy el sitio de cada parcela

Las 5 parcelas son **puntos de ejemplo elegidos con satélite**; nadie los ha visitado. El satélite ve un cuadro de 250 m de lado (unas 9 manzanas) alrededor del punto, no una parcela.

| Parcela (punto) | Suelo: meses pelados · con poca cobertura | Quema a 500 m o menos (enero-mayo, 2012-2026) | Canícula de más de 15 días (2001-2025) | Opciones que muestra | Julio-agosto 2026 |
|---|---|---|---|---|---|
| **Jocotán** (14.81146, −89.39433) | marzo y abril · febrero y mayo | 3 de 15 años: 2013, 2025 y 2026 | 2 de 25 años: 2015 y 2018 | Parejas: maíz con canavalia (88), sorgo con caupí (87). Hoy: 80 | 24 % de lo normal |
| **Camotán** (14.86146, −89.37404) | ninguno · marzo y abril | 3 de 15 años: 2018, 2022 y 2023 | 2 de 25 años: 2015 y 2018 | En gris (sin dato de humedad): canavalia (90), sorgo con caupí (89). Hoy: 84 | 26 % |
| **Olopa** (14.66563, −89.29358) | ninguno · marzo y abril | 1 de 15 años: 2018 | 0 de 25 años | Las tres parejas: hoy (87), canavalia (90), maíz ICTA B-5 (92) | 22 % |
| **San Juan Ermita** (14.78646, −89.42065) | febrero, marzo y abril · enero y mayo | 2 de 15 años: 2018 y 2026 | 1 de 25 años: 2018 | Parejas: canavalia (88), sorgo con caupí (86). Hoy: 80 | 20 % |
| **Zacapa** (14.94062, −89.56000) | abril · enero, febrero, marzo y mayo | 0 de 15 años | 3 de 25 años: 2015, 2018 y 2025 | En gris (la lluvia de dos fuentes no coincide): canavalia (81), sorgo con caupí (80). Hoy: 73 | 21 % |

Años que el motor marca como de riesgo alto de sequía (2006-2025): **2009, 2014, 2015, 2018 y 2025** en Jocotán, Camotán y Zacapa; Olopa: 2010, 2014, 2015, 2018, 2021 y 2025; San Juan Ermita: 2009, 2010, 2014, 2015, 2018 y 2025. **No marca 2016, 2019 ni 2023**, que tienen pérdidas documentadas.

## Bloque 1. ¿El punto es una parcela? (5 min)

Muestre el punto en el mapa del teléfono (Evidence → mapa) o diga el lugar de palabra.

| N.º | Pregunta | Para qué sirve | Qué cambia |
|---|---|---|---|
| 1 ★ | «¿Qué hay en ese lugar: milpa, potrero, guamil, monte, casas?» | Saber si el punto es tierra de cultivo. El filtro de verdor no distingue la milpa del guamil ni del bosque seco. | `data/parcelas.yaml` (coordenada y nota). Si no es milpa, se elige otro punto |
| 2 | «¿En qué municipio y aldea queda?» | El punto de **Olopa** puede caer en Esquipulas y el de **San Juan Ermita**, en Jocotán. | `data/parcelas.yaml` (municipio) |
| 3 | «¿Me puede señalar una parcela de milpa que usted conozca bien, cerca de aquí?» Si acepta, anote la coordenada con el teléfono, **de la parcela, nunca de la casa**. | Tener un punto confirmado por alguien de la zona. | Un punto nuevo o el reemplazo de uno dudoso |
| 4 | «¿Las parcelas de alrededor, unas 9 manzanas, se trabajan igual que la suya?» | El satélite promedia todo el cuadro. Si alrededor hay potrero o monte, el dato de suelo no habla de su milpa. | La nota de la parcela y el texto del límite de escala |
| 5 | «¿Qué medida usa para la tierra: manzana, tarea, cuerda? ¿Cuánto trabaja usted?» | El sitio dice «unas 9 manzanas» y una familia promedio de 0.35 ha. | La palabra de la medida en los textos |

Dudas por parcela: **Camotán**, ladera con parcelas y guamil (¿es milpa?). **Zacapa**, ladera seca al sur de la ciudad (¿milpa o bosque seco que bota la hoja?). **Olopa**, llano abierto (¿pasto o cultivo?).

## Bloque 2. Lo que siembra hoy (7 min)

El motor supone fechas y duraciones para simular el agua. Son supuestos, no recomendaciones: la fecha de siembra el sitio la cita de ZARC, nunca la calcula.

| N.º | Pregunta | Lo que supone hoy el motor | Qué cambia |
|---|---|---|---|
| 6 ★ | «¿Qué siembra en primera y qué en postrera? ¿El frijol va junto al maíz o aparte?» | Maíz con frijol en primera y frijol en postrera. Hay otras dos plantillas: maíz solo y maicillo | Qué rotación «actual» se muestra (`data/rotaciones.yaml`) |
| 7 ★ | «¿En qué fecha sembró la primera este año? ¿Y los años anteriores? ¿Qué señal espera para sembrar?» | 25 de mayo | `siembra_mes` y `siembra_dia` en `data/rotaciones.yaml` |
| 8 | «¿Cuándo siembra la postrera?» | 15 de septiembre (frijol); 10 de septiembre (caupí); 1 de septiembre después del maíz de ciclo corto | Igual |
| 9 | «¿Qué maíz siembra: criollo o de semilla comprada? ¿Cuántos días pasan de la siembra a la dobla?» | 125 días (90 para ICTA B-5) | `data/cultivos.yaml` |
| 10 ★ | «¿Cuántos días tarda su frijol de postrera, de la siembra al arranque?» | 80 días. **Es un supuesto sin fuente** | `data/cultivos.yaml` |
| 11 | «¿Siembra maicillo? ¿Y frijol alacín o caupí? ¿Cuántos días tardan?» | Sorgo 100 días; caupí 75 días, **supuesto sin fuente** | `data/cultivos.yaml` |
| 12 | «¿Qué hace con el rastrojo: lo deja, lo come el ganado, lo vende, lo quema?» | Las opciones con «rastrojo en pie» suman puntos de suelo | Los riesgos y vacíos de cada plantilla |

## Bloque 3. Los tres hechos, sin mostrar la pantalla (8 min)

| N.º | Pregunta | Compare con | Qué cambia |
|---|---|---|---|
| 13 ★ | **Suelo.** «¿En qué meses queda la tierra pelada, sin nada encima?» | Los meses de la tabla de arriba | Si el dato de suelo se puede leer como «su parcela» o solo como «la zona» |
| 14 ★ | **Quema.** «Por aquí, ¿se quema para preparar la tierra? ¿En qué meses? ¿Todos los años o solo algunos?» Pregunte por la zona, no por la persona, y sin juzgar. | Los años de la tabla. Pregunte por los más recientes: «¿hubo quema cerca en abril o mayo de 2025? ¿Y en 2026?» | Si los años sin detección fueron años sin quema, o quemas que el satélite no vio |
| 15 | «Las quemas, ¿son grandes o chiquitas? ¿Cuánto duran?» | El satélite pasa pocas veces al día y no ve quemas breves, pequeñas o bajo nubes | El texto del límite de la quema |
| 16 ★ | **Canícula.** «¿Qué años recuerda con canícula larga, de más de dos semanas sin llover entre julio y agosto?» No diga años: espere los suyos. | Los años de la tabla. Después pregunte por los dudosos: **2014, 2019, 2021, 2023 y 2025** | La regla de la canícula y qué reparto diario de lluvia se parece más a lo vivido (ver `docs/es/sensibilidad-canicula.md`) |
| 17 | «¿Cuántos días sin lluvia ya son un problema para la milpa? ¿Una llovizna cuenta como lluvia?» | Más de 15 días seguidos con menos de 2 mm al día | Los dos umbrales. Solo se cambian con acuerdo del agrónomo, y nunca para que un año «salga bien» |

## Bloque 4. Los años malos (5 min)

Es la pregunta que más le hace falta a la validación: hoy el motor se compara con reportes de país y de departamento, no con ninguna parcela.

| N.º | Pregunta | Compare con | Qué cambia |
|---|---|---|---|
| 18 ★ | «¿En qué años perdió la mitad o más del maíz? ¿Y del frijol?» No diga años. | Los años que marca el motor y los 7 con pérdidas documentadas: 2009, 2010, 2015, 2016, 2018, 2019 y 2023 | Una fila nueva en `docs/validacion.md`, rotulada como testimonio de una persona |
| 19 | Pregunte uno por uno por **2016, 2019 y 2023** (el motor no los marca) y por **2014 y 2025** (los marca y no están en la lista). | — | Saber si son fallos del motor o años en que aquí no pasó nada |
| 20 | «Esas pérdidas, ¿fueron por falta de lluvia, por lluvia de más, por plaga o por otra cosa?» | El motor solo mide falta de agua. De 2010 no sabemos la causa | El texto de los límites |
| 21 | «¿Cómo le fue en la primera de 2026?» | Julio y agosto de 2026: entre 20 % y 26 % de la lluvia normal en las 5 parcelas | Si la línea de 2026 dice algo que la gente reconoce |

## Bloque 5. Las opciones (7 min)

Muestre ahora la parte de «Opciones para platicar con su técnico». Pregunte por las dos alternativas que aparecen en esa parcela.

| N.º | Pregunta | Para qué sirve |
|---|---|---|
| 22 ★ | **Canavalia** con el maíz: «¿La conoce? ¿La ha sembrado o la ha visto? ¿Se consigue semilla?» | Saber si la opción es real en la zona. Pregunte también: «¿la comen o se la dan a los animales?» La plantilla no dice nada de eso; es una pregunta abierta para el agrónomo (`docs/es/revision-plan.md`, 3.2, pregunta 2) |
| 23 | **Maicillo con caupí** (frijol alacín): «¿Se siembra por aquí? ¿Se come, se vende?» | Igual. En Olopa pregunte por el **maíz ICTA B-5**: «¿lo conoce? ¿Dónde se compra la semilla?» |
| 24 | «¿Qué le preocuparía de probarla en un pedazo: que compita con el maíz, que se la coma el ganado, que no se venda, el trabajo?» | Riesgos que faltan en la plantilla |
| 25 | «Para usted, ¿qué pesa más: que aguante la sequía, que cuide la tierra o que tenga menos plaga?» | El sitio da 50 % al criterio elegido y 25 % a cada uno de los otros. La prioridad por defecto es el agua |
| 26 | «¿Lo visita un técnico o extensionista? ¿De qué institución? ¿Cada cuánto?» | El sitio dice «platíquelo con su técnico». Si nadie lo visita, hay que decir con quién más |
| 27 | «¿Conoce Kuxur Rum, dejar árboles y no quemar?» | El sitio dice que los tres hechos son los tres problemas que atiende Kuxur Rum |

Las opciones de **Camotán** y **Zacapa** salen en gris. Pregunte: «Aquí dice que no comparamos las opciones porque la confianza es baja. ¿Qué entiende con eso?»

## Bloque 6. ¿Se entiende? (6 min)

Enseñe la primera pantalla sin explicar nada.

| N.º | Pregunta | Qué se busca |
|---|---|---|
| 28 ★ | «¿Qué le dice esta pantalla?» | Que hable de su tierra y de años pasados, no de un aviso |
| 29 | Señale cada palabra: **Bien**, **Atención**, **Se repite**. «¿Qué quiere decir?» | Que «Se repite» se entienda como «ha pasado varias veces», no como una orden |
| 30 | Señale el gris: **«El satélite no ve bien aquí»**. «¿Y esto?» | Que se lea como «falta el dato», no como «algo anda mal» |
| 31 | Señale la línea de julio y agosto de 2026. «Esto, ¿ya pasó o va a pasar?» | Que se lea como algo que ya ocurrió. **Si alguien lo toma como pronóstico, hay que cambiar el texto** |
| 32 | Toque **Escuchar**. Al terminar: «¿Qué entendió? ¿Qué palabra no se entendió? ¿La voz se entiende?» | Palabras que cambiar. La voz es de computadora y lo dice al empezar |
| 33 | «¿Usted dice canícula, rastrojo, postrera, tierra pelada? ¿Cómo le dicen aquí?» | Las palabras de los textos y del audio |
| 34 | «¿Qué idioma se habla en su casa? ¿Le serviría oírlo en ch'orti'?» | El guion en ch'orti' espera hablantes que lo graben (`docs/es/chorti.md`) |
| 35 | Con la hoja impresa: «¿Se ve claro así, en blanco y negro?» | Que no dependa del color |
| 36 | «Después de ver esto, ¿qué haría?» | Que la respuesta sea «platicarlo» y no «hacer lo que dice» |

## Bloque 7. Teléfono y uso (2 min)

| N.º | Pregunta | Para qué sirve |
|---|---|---|
| 37 | «¿Tiene teléfono con internet? ¿Hay señal en la parcela, o solo en el pueblo?» | El sitio funciona sin internet solo si alguien lo sirve desde una laptop en una red local. Todavía no se ha probado en campo |
| 38 | «¿Usa WhatsApp? ¿Le mandan audios?» | El kit comparte un resumen por WhatsApp y permite bajar el audio |
| 39 | «¿Prefiere leerlo, oírlo o que alguien se lo explique? ¿Con quién lo vería?» | Si la primera pantalla debe abrir con el audio |

## Para el extensionista o agrónomo (20 min)

Las diez preguntas sobre las reglas de puntaje y las 8 plantillas están en `docs/es/revision-plan.md`, sección 3.2. Además:

| N.º | Pregunta | Qué cambia |
|---|---|---|
| E1 | «¿Tiene la ventana de siembra de ZARC para este municipio? ¿En qué documento, página y fecha?» | `data/zarc_citas.yaml`, que solo admite texto literal con documento, página y fecha de consulta. Hoy el sitio cita una nota de prensa por departamento |
| E2 | «¿80 días para el frijol de postrera y 75 para el caupí son razonables aquí?» | `data/cultivos.yaml`. Del caupí tampoco hay factor de respuesta al agua (Ky) con fuente |
| E3 | «¿Los cinco puntos caen en tierra de cultivo? ¿Olopa y San Juan Ermita están en su municipio?» | `data/parcelas.yaml` |
| E4 | «¿Alguna de estas opciones podría hacer daño si alguien la sigue sin asesoría, por ejemplo en ladera?» | Los riesgos de cada plantilla |
| E5 | «¿Qué años fueron de sequía en su zona de trabajo?» | La misma comparación del bloque 4, con otra voz |
| E6 | «¿Puede decirnos su institución y su cargo para citarlo como revisor?» Solo con su permiso. | El aviso «Reglas de la opción sin revisar por un agrónomo» que el sitio pone en cada opción, y la diapositiva 6 |

## Cómo anotar y qué hacemos con las respuestas

Una fila por pregunta, con el número, y la respuesta **con las palabras de la persona**:

| N.º | Respuesta, tal como la dijo | ¿Coincide con el sitio? (sí, no, a medias) | Nota |
|---|---|---|---|
| | | | |

Guarde las hojas en `docs/es/respuestas-campo.md` (una sección por conversación: fecha, municipio y aldea, agricultor o extensionista). Con eso:

- **Puntos** (1 a 4, E3): se corrigen en `data/parcelas.yaml` y se vuelve a correr todo el flujo de datos para ese punto.
- **Fechas y duraciones** (7 a 11, E2): se cambian en `data/rotaciones.yaml` y `data/cultivos.yaml`, con la fuente «comunicación de un agricultor o extensionista de [municipio], [fecha]», y se regeneran los JSON. **Aquí sí pueden cambiar los puntajes**, y se dice cuáles y por qué.
- **Años malos** (16, 18 a 21, E5): entran a la validación como una fila rotulada «testimonio», sin tocar la regla. No se ajusta ningún umbral para que un año coincida.
- **Palabras y comprensión** (28 a 36): se cambian los textos y el audio se vuelve a generar.
- **Lo que no coincida** se escribe en «Dónde falla», aunque no se pueda arreglar.

Una conversación no es una muestra: en los documentos se escribe «un agricultor de Jocotán dijo…», nunca «los agricultores dicen…».
