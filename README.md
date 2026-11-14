# Milpa Resiliente

**NASA Space Apps Challenge 2026 · Guatemala · Challenge “Field Shift: Adapting Farms with NASA Data”** · Team “A dream”: Rodolfo Xiloj, Mario and Iván.

> NASA satellite records turned into three facts a farmer can see and hear, for the milpa in Guatemala’s Dry Corridor.

Milpa Resiliente is a static website for farmers and agricultural extension workers in Guatemala's Dry Corridor. Next to the three facts, it shows three crop rotations to talk over with the extension worker, with the evidence and its limits in plain sight. It covers five example plots in Chiquimula and Zacapa: Jocotán, Camotán, Olopa, San Juan Ermita and Zacapa. The whole site is in English and Spanish, with an EN/ES selector; English is the default.

It supports the extension worker and the farmer; it does not replace them. Planting dates are **quoted, never calculated**. They come from ZARC (Zonificación Agroclimática del Riesgo), a tool from FAO and Guatemala's Ministry of Agriculture (MAGA).

## What you see

### 1. The farmer view (first screen)

- **A traffic light of three facts** the satellite saw around the plot, always in the same order:
  - **Bare soil:** months with bare soil or little plant cover in the 250 m cell around the plot, from MODIS NDVI (Normalized Difference Vegetation Index), 2021-2025.
  - **Fire near the plot:** years with a satellite fire detection within 500 m, January to May, from FIRMS (Fire Information for Resource Management System), VIIRS sensor at 375 m, 2012-2026.
  - **Long dry spell (canícula):** years with more than 15 dry days in a row, from daily CHIRPS v3 split with NASA GPM IMERG, 2001-2025.
- **Four states that never rely on colour alone.** Each has a shape, a word and a pictogram: green circle “Good”, yellow triangle “Watch”, red square “Repeats”, and gray “The satellite can't see well here” when a source has no data. The view avoids orange and the word “alert”, so it is not mistaken for CONRED's public alert levels (green, yellow, orange and red); every state also carries a shape and a word, so it never relies on colour. The thresholds were confirmed by the team ([docs/thresholds.md](docs/thresholds.md)).
- **Pictograms** drawn as SVG: bare or covered soil with a 12-month wheel, and fire or sun with one dot per year. They are designed to read the same in colour, in grey and on a black-and-white photocopy; the photocopy check is still pending ([docs/pictos.md](docs/pictos.md)).
- **Options to talk over with the extension worker:** the current practice, the best legume or cover-crop option and the best drought-tolerant option. Options within 3 points of one another are shown as even, in no order, instead of naming a winner; the rule works as a chain, so in Olopa (87, 90 and 92) all three count as even.
- **A “Listen” button:** a short audio in Spanish or English, to match the screen, with subtitles. The voice is synthetic and labelled as AI-generated.

### 2. Evidence (one tap away)

The technical view for the extension worker loads only when someone opens it:

- Map of the five plots with NASA GIBS true-colour layers stored in the site for offline use, plus Sentinel-2 imagery when there is a connection.
- What the satellite sees, the climate of the area, and the three rotations side by side. Each rotation carries the five fields the challenge asks for: why, evidence, benefits, information gaps and risks. Each also has water, soil and pest scores, a confidence level with its reason, and a 12-month calendar.
- Scenarios: rainfall at 0, −10, −20 or −30 % and temperature at +1.5 °C, recomputed in the browser from values the engine already calculated.
- NASA climate futures: the three rotations tested against the rain and temperature change that each NASA NEX-GDDP-CMIP6 model projects for 2041–2060 (33 models in SSP2-4.5, 34 in SSP5-8.5), with the same water balance. At the five plots, today's maize and beans keeps today's water score in only 2 to 9 futures; the drought-tolerant option holds in 32 to 34.
- A farmer card that can be played as audio and printed or saved as PDF.
- A “NASA product → decision” table, a “Where it fails” panel, the validation tab, and the glossary and sources.

**Preliminary observation, not a forecast:** in July and August 2026, the five plots got 20 % to 26 % of their 1991–2025 median rainfall. That's the lowest since 1991 (CHIRPS v3, final monthly product). The 2026 rain and soil-moisture figures are an observation only: the climate record the engine scores with is 2001–2025. The one place 2026 does enter is the fire record, where detections from January to May 2026 count ([docs/validation.md](docs/validation.md)).

## How it works

```
parcelas.yaml → pipeline/precargar → data/cache/ → motor/recomendar → motor/exportar → web/public/data → static site
```

- **Static first:** the site needs no server, keys or third-party network to show the plots. Only the base map (OpenStreetMap) and the Sentinel-2 image need internet. The NASA GIBS layers are stored in the site, and without internet the map switches to the stored layer by itself.
- **One engine in plain Python:** standard library plus PyYAML, with no network. It returns the JSON defined in `contracts/recomendacion.schema.json`, including the `farmer` block with the traffic light.
- **Cache inside the repo:** `data/cache/`. Each file records its provenance: URL, download date, product and version. The pipeline uses the network only with `MILPA_ONLINE=1`.
- **AI doesn't write numbers:** texts in both languages come from deterministic templates. A validator rejects any number that is not in the engine's JSON and any planting date that does not come from ZARC.

| Folder | Contents | Owner |
|---|---|---|
| `contracts/` | JSON schema (contract v1) and a hand-written example | Rodolfo |
| `data/` | Plots, rotations, crops (FAO-56 Kc), ZARC quotes, traffic-light thresholds, glossary, sources and cache | Iván (YAML) · Mario (cache) |
| `pipeline/` | Data clients with cache: POWER, ORNL (NDVI), FIRMS, CHIRPS (monthly, and daily “sat”, which carries IMERG's daily split), SMAP (AppEEARS), SRTM, SoilGrids, GIBS | Mario |
| `motor/` | Detection, climate, scores, confidence, traffic light, ZARC, text templates in Spanish and English, phrase audio, export | Rodolfo |
| `web/` | Vite + React + react-leaflet + Recharts: farmer view, Evidence and pictograms | Rodolfo Xiloj |
| `tests/` | Contract, number validator, ZARC, traffic light, English texts, phrase audio, engine with synthetic data, pipeline, validation | Everyone |
| `docs/` | Documentation in English, with the Spanish team notes in `docs/es/` ([docs/README.md](docs/README.md)) | Everyone |
| `api/` | Placeholder for an optional live API. Not built and not part of the submission | None |

## How to run it

Requirements: Python 3.11+ and Node 20+. The browser scripts in `web/scripts/*.py` also need Playwright, and the audio is only regenerated with edge-tts; both are optional and listed in [requirements.txt](requirements.txt).

```bash
pip install -r requirements.txt

# Tests (no network)
python -m pytest

# Web
cd web
npm install
npm run dev        # development server
npm run build      # static site in web/dist
npm run smoke      # renders every component with every exported JSON; checks the AI label of each mp3
npm run sin-red    # after the build: opens the site in Edge with no internet access
```

The exported JSON, mp3 and subtitle files in `web/public/` are already in the repo, so the web runs without downloading anything. To rebuild the JSON from the cache (no network):

```bash
python -m pipeline.validacion.validar   # POWER vs CHIRPS, 2018 drought test, 2026 observation -> web/public/data/validacion.json
python -m motor.exportar                # engine -> web/public/data/*.json
python -m motor.futuros                 # NASA NEX-GDDP-CMIP6 futures -> web/public/data/futuros_nasa.json
```

The climate futures were precomputed offline in the Earth Engine Code Editor with `pipeline/gee/cmip6_cambios.js` (nothing calls Earth Engine live). To rebuild the cache from the exported CSV: `python -m pipeline.clientes.cmip6 data/cache/cmip6/milpa_cmip6_cambios.csv`. See [docs/earth-engine.md](docs/earth-engine.md).

To download the data again (network needed; slow):

```bash
MILPA_ONLINE=1 python -m pipeline.precargar                       # POWER, SRTM, FIRMS, soil and NDVI 2001-2025
MILPA_ONLINE=1 python -m pipeline.clientes.chirps                 # CHIRPS v3 monthly 1991-2025
MILPA_ONLINE=1 python -m pipeline.clientes.chirps --diario        # CHIRPS v3 daily, June-August (canícula)
MILPA_ONLINE=1 python -m pipeline.clientes.firms --reciente 2026  # 2026 fires: needs FIRMS_MAP_KEY in .env
MILPA_ONLINE=1 python -m pipeline.clientes.appeears_smap todo     # SMAP: needs EARTHDATA_USERNAME and _PASSWORD
MILPA_ONLINE=1 python -m pipeline.capas                           # GIBS tiles for the offline map
MILPA_ONLINE=1 python -m motor.exportar --audio                   # also the mp3 and subtitle files, with edge-tts
```

In PowerShell, use `$env:MILPA_ONLINE='1'; python ...` instead of `MILPA_ONLINE=1 python ...`.

Keys (`FIRMS_MAP_KEY`, `EARTHDATA_USERNAME`, `EARTHDATA_PASSWORD`) go in a local `.env` copied from `.env.example`. `.env` is in `.gitignore`. The pipeline reads the keys without printing them. The engine and the static site need none.

## Status

Done (test runs are logged in [docs/tests.md](docs/tests.md)):

- Cached data for the five plots, the engine, the contract and the validation.
- The farmer view as the first screen: three-fact traffic light with confirmed thresholds, pictograms, options with the tie rule, and the Listen button with subtitles.
- Evidence in English and Spanish: map, satellite panel, three rotations, scenarios, farmer card with audio and PDF, product-to-decision table, “Where it fails” panel, validation, glossary and sources.
- Offline map layers and an automated offline test.

Still to do:

- **Agronomist review** of the scoring rules and the eight rotation templates.
- **Comprehension test** of the pictograms, the traffic-light words and the audio with adult users.
- **Real phone test**, including TalkBack (Android's screen reader).
- **Field check of the five points:** they were chosen from NDVI and Sentinel-2 imagery and have not been verified on the ground.
- **Public deployment** of the static site.

Known limits:

- Camotán has no SMAP value of recommended quality.
- NASA POWER puts four of the five plots in the same ~50 km cell.
- ZARC computes the best planting week by municipality inside MAGA-DIGEGR, but those windows are not published; we quote the public departmental reference.
- Scale: a Dry Corridor family farms about 0.35 ha on average, while one MODIS pixel covers 6.25 ha, a SMAP cell 9 km and an SRTM cell 90 m. The tool describes the land around the plot, not the plot.
- Sensor continuity: Suomi NPP stopped delivering new data in early November 2026 and Terra is being retired, so updates would move to VIIRS on NOAA-20 and NOAA-21 (and to VIIRS vegetation indices for NDVI).

## NASA data

| Product | What it is used for |
|---|---|
| MODIS MOD13Q1 NDVI v061, 250 m, every 16 days (through ORNL DAAC) | Bare-soil or low-cover months in the 250 m cell around the plot (the “soil” fact) and the NDVI signal in the 2018 test. Terra is being retired; the method transfers to VIIRS vegetation indices |
| FIRMS VIIRS 375 m active fires (Suomi NPP, 2012-2026) | Years with a detection within 500 m, January to May (the “fire” fact). Each detection is the centre of a ~375 m pixel; small or short fires can be missed. S-NPP stopped delivering new data in early November 2026 |
| GPM IMERG Late V07 (0.1°) | Used through CHIRPS v3 daily “sat”, which splits each pentad into days with IMERG's pattern; not downloaded directly. Dry-spell counts depend on this split, so we compared them with the ERA5-based “rnl” version: with “rnl” the 5 plots have 14 years with a dry spell of more than 15 days in 2001-2025 against 8 with “sat” (plot-years), the two agree on 7 of the 15 plot-years either one flags, and the traffic-light colour changes in 3 of 5 plots (Jocotán yellow→red, Olopa green→yellow, San Juan Ermita yellow→red) |
| NASA POWER (about 50 km) | Temperature, reference evapotranspiration and the daily pattern that splits monthly CHIRPS rain outside June-August; compared against CHIRPS in the validation |
| SMAP SPL3SMP_E v6 (9 km, daily, top 0-5 cm; through AppEEARS) | Separate soil-moisture check next to the 2018 test (not part of the “up to 2017” run), the 2026 observation and the confidence level. It describes the ~9 km landscape, not the plot |
| SRTM GL3 (90 m) | Slope of the 90 m cell that contains each plot |
| NASA GIBS | True-colour MODIS layer stored in the site for the offline map |
| NASA NEX-GDDP-CMIP6 (0.25°, daily, bias-corrected; precomputed offline in Google Earth Engine) | Change in May-October rain, June-August rain and mean temperature for 2041-2060 against 1995-2014 in each model (33 under SSP2-4.5, 34 under SSP5-8.5): how many of those futures each rotation holds, in Evidence. Each model is compared only with its own past; it changes mean rain and temperature, not the number of rainy days |

## Other data and references

- **Data:** CHIRPS v3 (Climate Hazards Center, UC Santa Barbara; Funk et al., 2026, Scientific Data 13, 718, doi:10.1038/s41597-026-07096-4), SoilGrids (ISRIC), Sentinel-2 cloudless (EOX), OpenStreetMap, FAO-56 and FAO-33 (crop coefficients and yield response), FAO-66, ZARC (FAO–MAGA), and the public reports cited in [docs/validation.md](docs/validation.md). The impact figures and their URLs are in [docs/impact.md](docs/impact.md); the tools that already exist, in [docs/existing-tools.md](docs/existing-tools.md); the Ch'orti' recording script, in [docs/chorti.md](docs/chorti.md). Every source and its citation is in `data/fuentes.yaml` and in the glossary and sources tab of the site.
- **Software:** [React](https://react.dev/), [Leaflet](https://leafletjs.com/) with react-leaflet, [Recharts](https://recharts.org/), [Vite](https://vite.dev/), [edge-tts](https://github.com/rany2/edge-tts) for the synthetic voice and [PyYAML](https://pyyaml.org/).

## AI use

An AI coding agent wrote most of the code, the texts and the SVG pictograms under the team's direction and review. The team decided the scope, the thresholds and the validation. The audio uses a synthetic voice (edge-tts), labelled next to the player and in the ID3 tags of each mp3. Full declaration: [docs/ai-use.md](docs/ai-use.md).

## License

MIT, see [LICENSE](LICENSE). Data keep the license and citation of their source.
