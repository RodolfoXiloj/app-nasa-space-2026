# Project page draft (Space Apps 2026 form)

Draft of the submission form fields, in the order of the official Project Submission Guide. Paste each block into its field. Before sending, check the length limits in the form and replace every “TBD”.

Challenge: **Field Shift: Adapting Farms with NASA Data** · Team: **A dream** (Rodolfo Xiloj, Mario, Iván) · Guatemala.

## Project Name

Milpa Resiliente

## High-Level Project Summary

Milpa Resiliente turns NASA satellite records into a three-fact traffic light that a smallholder farmer in Guatemala's Dry Corridor can read in seconds: how many months the soil lies bare (MODIS NDVI), how many years there was fire near the plot (FIRMS VIIRS), and how many years the mid-summer dry spell, the *canícula*, ran long (CHIRPS daily split with GPM IMERG). Each fact has a shape, a word, a pictogram and a short Spanish audio with English or Spanish subtitles, so it does not depend on colour or on reading well. Behind that first screen, an Evidence view lets the extension worker compare three crop rotations for each plot under drier and hotter scenarios, with the sources, the validation and the limits in plain sight. It matters because these families lose maize and beans in the dry spell year after year, and the satellite already knows how their plots have been used. The tool does not decide for them: it gives the farmer and the technician the same evidence to decide together.

## Link to Project Demo

TBD: public URL

## Link to Final Project

TBD: public URL

## Detailed Project Description

**What it does.** Milpa Resiliente is a static website for five example plots in Chiquimula and Zacapa (Jocotán, Camotán, Olopa, San Juan Ermita and Zacapa). It has two views and works in English and Spanish.

- **Farmer view (first screen).** Three facts the satellite saw, always in the same order: bare soil, fire near the plot and long canícula. Each fact gets one of four states: green circle “Good”, yellow triangle “Watch”, red square “Repeats”, or gray “The satellite can't see well here” when a source has no data. The view never uses orange or the word “alert”, because in Guatemala those belong to official CONRED alerts. Pictograms show the quantities: a 12-month wheel for bare soil and one dot per year for fire and dry spells. Below, the options to talk over with the technician: the current practice, the best legume or cover-crop option and the best drought-tolerant option. If two options are 3 points apart or less, the view says they are even instead of naming a winner. A Listen button plays a short synthetic-voice audio with subtitles.
- **Evidence view (one tap away).** For the extension worker: a map with Sentinel-2 imagery and NASA GIBS layers that work offline, what the satellite sees, the climate of the area, the three rotations side by side with water, soil and pest scores and a 12-month calendar, rainfall scenarios of 0, −10, −20 and −30 % with +1.5 °C, a printable farmer card, a “NASA product → decision” table, a “Where it fails” panel, the validation and every source.

**How it works.** A Python pipeline downloads and caches the data for each plot, recording its URL, date, product and version. A rules engine in plain Python (standard library plus PyYAML) detects bare-soil months, fires and dry spells, runs an FAO-56 water balance with yield response factors, scores the rotations and writes one JSON file per plot that follows a JSON schema. The web (React, Leaflet, Recharts, built with Vite) reads only those files, so it needs no server and no keys. Texts in both languages come from deterministic templates, and a validator rejects any number that is not in the engine's JSON and any planting date that does not come from ZARC (FAO–MAGA). Planting dates are quoted, never calculated.

**How we checked it.** We fixed the rule before looking at the result: no threshold is tuned to make 2018 come out right. With data up to 2017, the engine flags the 2018 drought as high risk at 5 of 5 plots, and FAO GIEWS reported 175,126 ha of maize and beans lost in Guatemala that year. We also measured where NASA POWER rainfall fails at this scale (from −22 % to +55 % in July-August against CHIRPS) and replaced it with CHIRPS for rain. Separately, the site shows a preliminary observation, not a forecast: July-August 2026 got 20 % to 26 % of the 1991-2025 median rainfall at the five plots, the lowest since 1991.

**Benefits.** The farmer sees what happened on their own plot in a form that works without reading well and on a black-and-white photocopy. The extension worker gets the evidence, the confidence level and its reason for each option, and can show it offline in the field. Every claim links to its source and its limits.

**Limits we state openly.** The five points were chosen from NDVI and Sentinel-2 imagery and have not been checked on the ground. An agronomist has not reviewed the scoring rules yet. The pictograms still need a comprehension test with users. Camotán has no SMAP data of recommended quality. The audio voice is Spanish only.

**Tools.** Python 3.11, PyYAML, requests, pytest and jsonschema; JavaScript with React, Leaflet (react-leaflet), Recharts and Vite; edge-tts for the voice; a Windows laptop. No paid services.

## Use of Super Intelligence (SI)

An AI coding agent (Claude, by Anthropic) wrote most of the code, most of the texts in both languages and the SVG code of the pictograms, always under the team's direction and review. A research subagent with web search helped find agronomic sources; we checked every quote against its document and labelled the ones we could not check. The team decided the scope, the five plots, the traffic-light thresholds, the tie rule and the validation rule. The audio uses a synthetic voice (edge-tts), labelled as AI-generated next to the player and in each mp3's tags. No AI produces any number the user sees: numbers come from the data and from rules in code, and a validator rejects any number that is not in the engine's output. Full declaration: `docs/ai-use.md` in the repository.

## NASA Data

- **MODIS MOD13Q1 NDVI, 250 m, through ORNL DAAC:** months of bare soil and crop cycles (the “soil” fact) and the NDVI signal in the 2018 test.
- **FIRMS VIIRS S-NPP, 375 m:** fires within 500 m of each plot (the “fire” fact).
- **GPM IMERG:** splits CHIRPS pentads into daily rain for the “canícula” fact.
- **NASA POWER:** temperature and reference evapotranspiration for the water balance, and a daily rain pattern; also measured against CHIRPS to show where it fails.
- **SMAP SPL3SMP_E, through AppEEARS:** soil moisture for the 2018 test, the 2026 observation and the confidence level.
- **SRTM:** slope of each plot.
- **NASA GIBS:** true-colour MODIS layer stored in the site for the offline map.

## Space Agency Partner Data and Other References

- **Space agency partner data:** Sentinel-2 cloudless imagery (EOX, from ESA Copernicus Sentinel-2) for the base map and to choose the plot points.
- **Other data:** CHIRPS v3 (Climate Hazards Center, UC Santa Barbara), SoilGrids (ISRIC), OpenStreetMap, FAO-56, FAO-33 and FAO-66 (crop coefficients and yield response), ZARC (FAO–MAGA), FAO GIEWS Update of 27 August 2018, FEWS NET Guatemala update of August 2026, and the news reports cited in `docs/validation.md`.
- **Software:** React, Leaflet and react-leaflet, Recharts, Vite, edge-tts, PyYAML, requests, pytest, jsonschema.
- **Repository:** TBD: public URL
