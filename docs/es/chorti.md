# Ch'orti': guion de grabación para hablantes

Copia en español de [../chorti.md](../chorti.md). Si las dos difieren, manda la versión en inglés.

## Por qué importa

Jocotán, Camotán y Olopa, tres de nuestras cinco parcelas, son territorio maya ch'orti'. Según la ALMG, 112,432 personas hablan ch'orti' (censo de 2018; https://almg.org.gt/idioma_chorti/). Los perfiles municipales de UNICEF dan 80.4 % de población indígena en Jocotán, 64 % en Camotán y 52 % de población ch'orti' en Olopa, donde predomina el español (URL en [impacto.md](impacto.md)). Un agricultor que no lee bien, o que se siente más cómodo en ch'orti' que en español, debería poder oír los tres hechos en su idioma.

## Qué hay hoy

- El contrato de datos ya tiene una ranura para el ch'orti' (código ISO 639-3 `caa`): `motor/farmer.py` define `IDIOMAS = ("es", "en", "caa")`.
- En el JSON de cada parcela (`web/public/data/{parcela}.json`), `farmer.audio.caa` es `null` y cada frase de `farmer.frases[]` tiene `"caa": null`. Todavía no suena nada en ch'orti'.
- No tradujimos ni sintetizamos ch'orti' con máquina. Sin la revisión de hablantes podría estar mal y ser una falta de respeto.

## El guion

Son las ocho frases de la parcela de Jocotán, copiadas de `farmer.frases` en `web/public/data/jocotan.json`. Las frases cambian con los estados, las cifras y las opciones de cada parcela (por ejemplo, la frase de opciones de Olopa dice que las tres opciones quedan parejas), así que un guion completo también necesita las frases de las otras cuatro parcelas, en sus propios JSON. Camotán y Zacapa no tienen la frase del futuro: sus opciones están en gris.

| id | Español | Inglés | Ch'orti' (lo llena un hablante) |
|---|---|---|---|
| parcela | Parcela de Jocotán. Le habla una voz de computadora. | Jocotán plot. A computer voice is reading this. | |
| suelo | En marzo y abril, su tierra suele quedar sin plantas que la cubran. Lo vio el satélite de 2021 a 2025. | In March and April, your land is usually left with no plants covering it. The satellite saw it from 2021 to 2025. | |
| quema | En 3 de los últimos 15 años hubo quemas a menos de medio kilómetro de su parcela, en abril y mayo. | In 3 of the last 15 years there were fires within half a kilometer of your plot, in April and May. | |
| canicula | En 2 de los últimos 25 años, la canícula dejó más de 15 días seguidos casi sin lluvia. | In 2 of the last 25 years, the midsummer drought brought more than 15 days in a row with almost no rain. | |
| este_anio | Este año, en julio y agosto, llovió solo la cuarta parte de lo normal (24 %). Es menos que en 2018, el año más seco desde 1991. Es un dato preliminar. | This year, July and August got only a quarter of the normal rain (24 %). That is less than in 2018, the driest year since 1991. It is a preliminary figure. | |
| opciones | Hoy hay dos opciones parejas: maíz con canavalia o sorgo con caupí. | Today there are two even options: maize with jack bean or sorghum with cowpea. | |
| futuro | La NASA calcula 33 climas posibles para 2041 a 2060. Si siembra como hoy, maíz con frijol, le alcanza el agua en 3 de 33. Maíz con canavalia: en 3. Sorgo con caupí: en los 33. | NASA computes 33 possible climates for 2041 to 2060. Planting as today, maize with beans has enough water in 3 of 33. Maize with jack bean: in 3. Sorghum with cowpea: in all 33. | |
| cierre | No es un aviso oficial: platíquelo con su técnico. | This is not an official notice: talk it over with your extension worker. | |

La primera frase dice «Le habla una voz de computadora» porque el audio de hoy es sintético. Una grabación hecha por una persona necesitaría su propia primera frase, sin ese rótulo.

Las palabras de los cuatro estados (`data/umbrales_semaforo.yaml` → `estados`):

| Estado | Español | Inglés | Ch'orti' (lo llena un hablante) |
|---|---|---|---|
| Verde | Bien | Good | |
| Amarillo | Ponga atención | Watch out | |
| Rojo | Pasa seguido | Happens often | |
| Gris | El satélite no ve bien aquí | The satellite can't see well here | |

Un nombre que los hablantes quizá quieran usar: **Kuxur Rum**, «mi tierra húmeda» en ch'orti', el sistema agroforestal sin quema y con cobertura permanente que la FAO y el Ministerio de Agricultura de Guatemala promueven en Chiquimula desde 2000 (https://openknowledge.fao.org/server/api/core/bitstreams/1800c8af-a373-462f-a231-21dbf734ca18/content).

## Cómo grabar

- Una frase por pista, en mp3, mono.
- Nombrar cada archivo con la parcela y el id de la frase, por ejemplo `jocotan.suelo.mp3`, para emparejarlo con la tabla de arriba.
- Basta un cuarto silencioso y el teléfono a la misma distancia en cada pista.
- Grabar también las cuatro palabras de los estados, cada una en su pista.

## A quién pedirlo

- ALMG, Academia de Lenguas Mayas de Guatemala: https://almg.org.gt/idioma_chorti/
- Radio Chortí – FM Tierra, en Jocotán: https://www.fger.org/chorti/

## La regla

- Nada generado por máquina: ni traducción automática ni voz sintética en ch'orti'.
- Lo que llegue se rotula «draft reviewed by one speaker» («borrador revisado por un hablante») hasta que lo valide la ALMG.
- Fuera del nombre Kuxur Rum, citado de la FAO, ninguna palabra en ch'orti' entra a este repositorio hasta que la dé un hablante.
