# Traffic-light thresholds for the 3 facts: confirmed

English version of [umbrales.md](umbrales.md). The Spanish file is the one the engine and the tests point to.

**Status: confirmed by Rodolfo on Saturday 14 Nov 2026.** The proposal was confirmed as written: gray per fact, a tie when two options differ by 3 points or less, Olopa with its three options in no order, and the words "Good", "Watch" and "Repeats" («Bien», «Atención», «Se repite»). The engine applies them from `data/umbrales_semaforo.yaml` and `motor/farmer.py`, with `farmer.umbrales.estado` set to `"confirmado"`. Applying them changed no score: after regenerating the JSON files of the 5 plots, the totals are the same.

Every figure comes from `data/cache/`: `motor.recomendar.recomendar()` was run in memory for the 5 plots (maize with beans, water priority), without writing files. The figures match the JSON files in `web/public/data/`.

**Honesty note:** these cut-offs were proposed after seeing the counts of the 5 plots, not before. The web and the slides say so. An agronomist still has to review them ([es/revision-plan.md](es/revision-plan.md), section 3.2).

## What the traffic light measures

Three observed facts. It is not a risk score and not a forecast. The traffic light **does not use the total score**: totals range from 73 to 92, and almost everything would come out green.

| Fact | What it counts | Source and period | Engine rule |
|---|---|---|---|
| Soil | Months with median NDVI < 0.35 (bare soil) and months from 0.35 to 0.45 (little cover) | MODIS MOD13Q1, 250 m, 2021-2025 | `motor/deteccion.py` → `UMBRALES` |
| Fire | Years with at least one VIIRS hotspot of nominal or high confidence within 500 m, January to May | FIRMS VIIRS S-NPP, 375 m, 2012-2026 (15 years; 2026 counts January to May only, from the S-NPP standard product) | `motor/deteccion.py` → `detectar_quemas` |
| Canícula | Years with a run of more than 15 days under 2 mm per day, 15 June to 31 August | CHIRPS v3 daily (split with IMERG), 2001-2025 (25 years) | `motor/clima.py` → `SUPUESTOS` |

## The real counts

| Plot | Bare soil (of 12 months) | Little cover | Fire (of 15 years) | Long canícula (of 25 years) | Valid NDVI composites | Confidence |
|---|---|---|---|---|---|---|
| Jocotán | 2 (Mar, Apr) | 2 (Feb, May) | 3 | 2 | 95.7 % | high |
| Camotán | 0 | 2 (Mar, Apr) | 3 | 2 | 80.9 % | low: its SMAP cell has no data of recommended quality |
| Olopa | 0 | 2 (Mar, Apr) | 1 | 0 | 93.0 % | medium: POWER deviates 22.1 % from CHIRPS |
| San Juan Ermita | 3 (Feb, Mar, Apr) | 2 (Jan, May) | 2 | 1 | 95.7 % | high |
| Zacapa | 1 (Apr) | 4 (Jan, Feb, Mar, May) | 0 | 3 | 93.9 % | low: POWER deviates 55.4 % from CHIRPS |

## Thresholds

| Fact | Green | Yellow | Red | Gray |
|---|---|---|---|---|
| Soil | 0 bare months and 0 months of little cover | 1 bare month, or 0 bare with some month of little cover | 2 bare months or more | Under 60 % valid NDVI composites, or some month without a median |
| Fire | 0 years | 1 or 2 years | 3 years or more | No FIRMS data (0 years observed) |
| Canícula | 0 years | 1 or 2 years | 3 years or more | June-August rain does not come from daily CHIRPS (POWER only) |

### Why each figure

- **Soil, red with 2 bare months or more.**
  - It reuses the NDVI thresholds of `motor/deteccion.py` (0.35 and 0.45) unchanged. They were calibrated before the 2018 test and are written in [validation.md](validation.md).
  - A single month under 0.35 can be the gap between harvest and planting; two or more mean bare soil for much of the dry season. This is a team assumption for the agronomist to review.
  - "Little cover" alone gives yellow, not red: in the soil score it weighs half a bare month (`motor/puntaje.py`, 3 points against 6), and on slopes the 250 m pixel mixes the milpa with trees.
- **Fire, red with 3 years or more out of 15.**
  - 3 of 15 is 1 year in 5: fire in different years, not a single event.
  - One or two years can be a neighbour's fire: the 500 m radius and the 375 m VIIRS pixel include the land next door.
  - Green says "no fire was seen", not "there was no fire": VIIRS passes a few times a day and misses short fires or fires under clouds (note in `detectar_quemas`).
  - 2026 counts only January to May, from the standard product of Suomi NPP. All FIRMS data in the record are Suomi NPP.
- **Canícula, red with 3 years or more out of 25.**
  - The same cut as fire, so the rule is explained the same way: "in three different years or more".
  - The run of more than 15 days and the 2 mm dry day are the plan's. They were not recalibrated.
  - The dry day (under 2 mm) and the run of more than 15 days are team decisions, not an official definition. For reference, CONRED describes the canícula as lasting 5 to 10 days on average (https://conred.gob.gt/que-es-la-canicula/); FEWS NET reported 11 to 20 consecutive dry days in 2026 (https://fews.net/es/latin-america-and-caribbean/guatemala/actualizacion-de-la-perspectiva-de-seguridad-alimentaria/agosto-2026) and Oxfam an average of 25 in 2019 (https://reliefweb.int/attachments/017ed79d-0dfa-3d24-a502-3474f5d9ddb7/Informe%20d%C3%A9fict%20de%20lluvias%202019.pdf).
  - The traffic light uses the observed record (base scenario), not the −10 to −30 % scenarios.
- **Gray per fact, not per plot.** A fact turns gray only if its own source fails:
  - Soil: the 60 % valid-composite cut is the one `motor/confianza.py` already uses for low confidence.
  - Fire: with no FIRMS data nothing can be said.
  - Canícula: POWER is a ~50 km cell, and in July-August it deviates from CHIRPS between −22.1 % and +55.4 % at these plots ([validation.md](validation.md)).
  - With today's data no fact is gray.

### What today's data give

| Plot | Soil | Fire | Canícula |
|---|---|---|---|
| Jocotán | red (2) | red (3) | yellow (2) |
| Camotán | yellow (0, and 2 of little cover) | red (3) | yellow (2) |
| Olopa | yellow (0, and 2 of little cover) | yellow (1) | green (0) |
| San Juan Ermita | red (3) | yellow (2) | yellow (1) |
| Zacapa | yellow (1) | green (0) | red (3) |

The 5 plots all come out different, which the total score does not achieve.

## The 4 states

| State | Shape | Word (en / es) | What it says |
|---|---|---|---|
| Green | Circle | "Good" / «Bien» | The satellite did not see the problem in the period |
| Yellow | Triangle | "Watch" / «Atención» | It saw it a little: one month, or one or two years |
| Red | Square | "Repeats" / «Se repite» | It saw it often: two months or more, or three years or more |
| Gray | Question mark, dotted border | "The satellite can't see well here" / «El satélite no ve bien aquí» | Data from that source are missing; nothing is guessed |

- Never colour alone: shape, word, icon and a fixed position (soil, fire, canícula, always in that order).
- The view avoids orange and the word "alert", so it is not mistaken for CONRED's public alert levels (green, yellow, orange and red; https://conred.gob.gt/conozca-los-niveles-de-alerta-y-su-significado/); every state also carries a shape and a word, so it never relies on colour. The schema rejects any state outside these 4.
- The view and the audio say: "this is not an official alert; talk with your extension worker".

## Tie rule (options)

**If two options differ by 3 points or less in the total, there is no winner.** The view says "two options to talk over with your extension worker" and shows them in no order.

The engine applies the margin as a chain (`motor/farmer.py` → `empatadas`): starting from the option with the highest total, any option within 3 points of one already in the even group joins it. That is why in Olopa (87, 90 and 92) all three count as even.

Why 3 points:

1. **3 points are one or two months of bare soil.** With water priority (the web's), each bare month takes 1.5 points off the total, or 2.25 if the slope is over 15 % (6 or 9 soil points × 25 %, `motor/puntaje.py`). That is the size of one or two months measured in a 250 m pixel that mixes the plot with its surroundings. Totals are also rounded to whole numbers.
2. **The scenarios already move the difference by up to 3 points.** Between the two alternatives, across the 8 scenarios:
   - Jocotán goes from 0 to 2.
   - Camotán, from 0 to 1.
   - Olopa, from −2 to −1.
   - San Juan Ermita, from 1 to 3.
   - In Zacapa the order flips, from +1 to −2.

With today's data (base scenario):

| Plot | Current | Legume or cover crop | Drought-tolerant | Difference between alternatives | Result |
|---|---|---|---|---|---|
| Jocotán | 80 | 88 | 87 | 1 | tie |
| Camotán | 84 | 90 | 89 | 1 | tie (and low confidence) |
| Olopa | 87 | 90 | 92 | 2 | tie; the legume option also ties with the current practice (3) |
| San Juan Ermita | 80 | 88 | 86 | 2 | tie |
| Zacapa | 73 | 81 | 80 | 1 | tie (and low confidence) |

- At all 5 plots the two alternatives tie with each other.
- The rule also applies between an alternative and the current practice. The alternatives beat the current practice by 5 to 8 points, except in Olopa: maize with jack bean (90) is 3 points from the current practice (87), so it ties with it. In Olopa the view says that the current practice and jack bean are even, and that short-cycle maize ICTA B-5 (92) is also even with jack bean.
- **Low confidence (Camotán and Zacapa):** the options block is gray, with the reason. The 3 facts do not turn gray, because their low confidence comes from SMAP or from POWER rain, which none of the 3 facts uses.

## What was decided

1. The cut-offs in the "Thresholds" table: confirmed as written.
2. Gray per fact, not gray for the whole plot when confidence is low.
3. The 3-point tie margin: confirmed.
4. Olopa, where the tie is not transitive: the three options are shown in no order, saying that none stands out enough.
5. The words for each state ("Good", "Watch", "Repeats") are kept; Iván reviews them in the comprehension test.
