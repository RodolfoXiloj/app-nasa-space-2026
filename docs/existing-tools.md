# What already exists, and where Milpa fits

Spanish copy: [es/herramientas-existentes.md](es/herramientas-existentes.md).

Milpa Resiliente is not the first tool for drought and farming in Guatemala's Dry Corridor. This page lists the ones we know of, what each does and for whom, so it is clear what Milpa adds and what it does not try to do. Every URL was consulted on 14 November 2026.

## What exists vs. Milpa

| Tool | What it does | For whom | How Milpa relates | URL |
|---|---|---|---|---|
| ASIS (Agricultural Stress Index System) in Guatemala | Digital drought early-warning system used to reinforce agricultural monitoring | Government agricultural monitoring | Milpa is not an early-warning system: it shows the record of the past around one plot | https://guatemala.gob.gt/refuerzan-monitoreo-agricola-con-sistema-digital-de-alerta-temprana-ante-sequias/ |
| ZARC (Zonificación Agroclimática del Riesgo), FAO–MAGA | Computes the best planting week by municipality inside MAGA's DIGEGR, starting with Chiquimula; the municipal windows are not published | MAGA and its extension services | Milpa never calculates planting dates: it quotes the public departmental ZARC reference. It complements ZARC with what the satellite saw around the plot | https://www.maga.gob.gt/herramienta-digital-zarc-mejorara-decisiones-de-siembra/ |
| Agroclimatic Technical Boards (Mesas Técnicas Agroclimáticas) | Local boards that produce agroclimatic bulletins; in 2025 the bulletins went out in at least 35 WhatsApp groups. In Chimaltenango (n=26) more than 90 % found them clear; in Santa Rosa (n=13) autonomous comprehension was limited | Farmers and extension workers, through local boards | Milpa can add plot-level history to the conversation a board already has; the Santa Rosa result is a reminder that our own comprehension test is still pending | https://alliancebioversityciat.org/publications-data/design-action-evidence-implementation-and-scaling-agroclimatic-services-guatemala |
| FEWS NET and the IPC forecast (SESAN) | Food security outlooks and the IPC classification of how many people are in crisis or worse | Governments, humanitarian agencies and donors | Milpa uses their figures to explain the problem ([impact.md](impact.md)); it does not classify food security | https://fews.net/es/latin-america-and-caribbean/guatemala/actualizacion-de-la-perspectiva-de-seguridad-alimentaria/agosto-2026 · https://portal.sesan.gob.gt/2026/08/07/sesan-presenta-pronostico-de-inseguridad-alimentaria-para-el-periodo-2026-2027-y-acciones-de-respuesta/ |
| WFP anticipatory actions, 2023 | Anticipatory actions before the drought in Chiquimula: seed for 1,200 farmers and more than 10,000 SMS | Farmers in Chiquimula | Milpa does not deliver aid or messages; it gives the extension worker and the farmer the same evidence for one plot | https://es.wfp.org/noticias/guatemala-wfp-implementa-acciones-anticipatorias-ante-la-sequia-en-el-corredor-seco |
| NASA Harvest GLAM | Global agricultural monitoring of crop conditions from satellite data | Analysts and agricultural agencies | Milpa works at one plot and in the language of the farmer, not at national or global scale | https://glam.nasaharvest.org/info |
| Plantix | Phone app that diagnoses crop problems from a photo | Farmers with a smartphone | Milpa does not diagnose pests or diseases; it describes soil cover, fire and dry spells around the plot | https://agritechobservatory.review.fao.org/en/plantix-crop-doctor |
| OpenET Data Explorer (NASA, USGS, DRI, EDF, Google and others) | Satellite explorer of evapotranspiration (crop water use) at field scale | Farmers, water managers and researchers in the United States | OpenET does not cover Guatemala. Milpa works for rainfed milpa in the Dry Corridor. OpenET's field outlines, model breakdown and cumulative water curves are a design reference for Milpa's next version; the submitted site does not have them | https://explore.etdata.org/ |

A lesson on channels: in a 2023 usability test in Chiquimula, CGIAR got 43 % of surveys completed through WhatsApp against 3 % through an IVR phone call (https://www.cgiar.org/news-events/news/usability-testing-to-transform-research-impact-lessons-from-guatemala). The farmer kit already has a button to share the summary through WhatsApp. The CGIAR result is about survey completion, not about how many farmers use WhatsApp, and we give no figure for that.

## What Milpa does not claim

- It is not an early-warning system and not a forecast. It shows what satellites recorded in the past, and the 2026 figures are an observation only.
- It does not measure the plot. It describes the land around it: a 250 m MODIS cell, a 500 m radius for fire, a ~5 km CHIRPS cell and a 9 km SMAP cell.
- It does not replace ZARC, MAGA, INSIVUMEH or CONRED. It quotes ZARC's planting dates, and it avoids orange and the word “alert” so it is not mistaken for CONRED's alert levels.
- It has not been tested with farmers and its scoring rules have not been reviewed by an agronomist.
