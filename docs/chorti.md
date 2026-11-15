# Ch'orti': recording script for native speakers

Spanish copy: [es/chorti.md](es/chorti.md).

## Why it matters

Jocotán, Camotán and Olopa, three of our five plots, are Ch'orti' Maya territory. According to the ALMG, 112,432 people speak Ch'orti' (2018 census; https://almg.org.gt/idioma_chorti/). UNICEF's municipal profiles give 80.4 % indigenous population in Jocotán, 64 % in Camotán and 52 % Ch'orti' population in Olopa, where Spanish predominates (URLs in [impact.md](impact.md)). A farmer who does not read well, or who is more at ease in Ch'orti' than in Spanish, should be able to hear the three facts in their own language.

## What exists today

- The data contract already has a slot for Ch'orti' (ISO 639-3 code `caa`): `motor/farmer.py` lists `IDIOMAS = ("es", "en", "caa")`.
- In each plot's JSON (`web/public/data/{plot}.json`), `farmer.audio.caa` is `null` and every phrase in `farmer.frases[]` has `"caa": null`. Nothing plays in Ch'orti' yet.
- We did not machine-translate or synthesise Ch'orti'. Without review by speakers it could be wrong and disrespectful.

## The script

These are the eight phrases of the Jocotán plot, copied from `farmer.frases` in `web/public/data/jocotan.json`. The phrases change with each plot's states, numbers and options (for example, Olopa's options phrase says that all three options come out even), so a full script also needs the phrases of the other four plots, in their own JSON files. Camotán and Zacapa have no future phrase: their options are gray.

| id | Spanish | English | Ch'orti' (to be filled by a native speaker) |
|---|---|---|---|
| parcela | Parcela de Jocotán. Le habla una voz de computadora. | Jocotán plot. A computer voice is reading this. | |
| suelo | En marzo y abril, su tierra suele quedar sin plantas que la cubran. Lo vio el satélite de 2021 a 2025. | In March and April, your land is usually left with no plants covering it. The satellite saw it from 2021 to 2025. | |
| quema | En 3 de los últimos 15 años hubo quemas a menos de medio kilómetro de su parcela, en abril y mayo. | In 3 of the last 15 years there were fires within half a kilometer of your plot, in April and May. | |
| canicula | En 2 de los últimos 25 años, la canícula dejó más de 15 días seguidos casi sin lluvia. | In 2 of the last 25 years, the midsummer drought brought more than 15 days in a row with almost no rain. | |
| este_anio | Este año, en julio y agosto, llovió solo la cuarta parte de lo normal (24 %). Es menos que en 2018, el año más seco desde 1991. Es un dato preliminar. | This year, July and August got only a quarter of the normal rain (24 %). That is less than in 2018, the driest year since 1991. It is a preliminary figure. | |
| opciones | Hoy hay dos opciones parejas: maíz con canavalia o sorgo con caupí. | Today there are two even options: maize with jack bean or sorghum with cowpea. | |
| futuro | La NASA calcula 33 climas posibles para 2041 a 2060. Si siembra como hoy, maíz con frijol, le alcanza el agua en 3 de 33. Maíz con canavalia: en 3. Sorgo con caupí: en los 33. | NASA computes 33 possible climates for 2041 to 2060. Planting as today, maize with beans has enough water in 3 of 33. Maize with jack bean: in 3. Sorghum with cowpea: in all 33. | |
| cierre | No es un aviso oficial: platíquelo con su técnico. | This is not an official notice: talk it over with your extension worker. | |

The first phrase says “A computer voice is reading this” because today's audio is synthetic. A recording by a person would need its own first phrase, without that label.

The words of the four states (`data/umbrales_semaforo.yaml` → `estados`):

| State | Spanish | English | Ch'orti' (to be filled by a native speaker) |
|---|---|---|---|
| Green | Bien | Good | |
| Yellow | Ponga atención | Watch out | |
| Red | Pasa seguido | Happens often | |
| Gray | El satélite no ve bien aquí | The satellite can't see well here | |

A name the speakers may want to use: **Kuxur Rum**, “my humid land” in Ch'orti', the no-burn agroforestry system with permanent cover that FAO and Guatemala's Ministry of Agriculture have promoted in Chiquimula since 2000 (https://openknowledge.fao.org/server/api/core/bitstreams/1800c8af-a373-462f-a231-21dbf734ca18/content).

## How to record

- One phrase per track, mp3, mono.
- Name each file with the plot and the phrase id, for example `jocotan.suelo.mp3`, so it can be matched to the table above.
- A quiet room and a phone held at the same distance for every track are enough.
- Record the four state words as separate tracks too.

## Whom to ask

- ALMG, Academy of Mayan Languages of Guatemala: https://almg.org.gt/idioma_chorti/
- Radio Chortí – FM Tierra, in Jocotán: https://www.fger.org/chorti/

## The rule

- Nothing machine-generated: no machine translation and no synthetic Ch'orti' voice.
- Whatever arrives is labelled “draft reviewed by one speaker” until the ALMG validates it.
- Apart from the name Kuxur Rum, quoted from FAO, no Ch'orti' word goes into this repository until a speaker provides it.
