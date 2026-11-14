# Milpa Resiliente

**NASA Space Apps Challenge 2026 · Guatemala · Challenge “Field Shift: Adapting Farms with NASA Data”** · Team “A dream”: Rodolfo Xiloj, Mario and Iván.

> The satellite already knows how your plot has been used. We show which crop rotation holds up better in the next *canícula* (mid-summer dry spell) and why, so the extension worker and the farmer can decide together.

Milpa Resiliente is a static website for farmers and agricultural extension workers in Guatemala's Dry Corridor. It covers five example plots in Chiquimula and Zacapa: Jocotán, Camotán, Olopa, San Juan Ermita and Zacapa. The whole site is in English and Spanish, with an EN/ES selector; English is the default.

It supports the extension worker and the farmer; it does not replace them. Planting dates are **quoted, never calculated**. They come from ZARC (Zonificación Agroclimática del Riesgo), a tool from FAO and Guatemala's Ministry of Agriculture (MAGA).

## What you see

### 1. The farmer view (first screen)

- **A traffic light of three facts** the satellite saw on the plot, always in the same order:
  - **Bare soil:** months with bare soil or little plant cover, from MODIS NDVI (Normalized Difference Vegetation Index, 250 m), 2021-2025.
  - **Fire near the plot:** years with a fire within 500 m, from FIRMS (Fire Information for Resource Management System), VIIRS sensor at 375 m, 2012-2026.
  - **Long dry spell (canícula):** years with more than 15 dry days in a row, from daily CHIRPS v3 split with NASA GPM IMERG, 2001-2025.
- **Four states that never rely on colour alone.** Each has a shape, a word and a pictogram: green circle “Good”, yellow triangle “Watch”, red square “Repeats”, and gray “The satellite can't see well here” when a source has no data. There is no orange and no word “alert”: in Guatemala those belong to official CONRED alerts. The thresholds were confirmed by the team ([docs/thresholds.md](docs/thresholds.md)).
- **Pictograms** drawn as SVG: bare or covered soil with a 12-month wheel, and fire or sun with one dot per year. They read the same in colour, in grey and on a black-and-white photocopy ([docs/pictos.md](docs/pictos.md)).
- **Options to talk over with the technician:** the current practice, the best legume or cover-crop option and the best drought-tolerant option. If two options are 3 points apart or less, the view says they are even and shows them in no order.
- **A “Listen” button:** a short audio in Spanish with subtitles in Spanish or English. The voice is synthetic and labelled as AI-generated.

### 2. Evidence (one tap away)

The technical view for the extension worker loads only when someone opens it:

- Map of the five plots with Sentinel-2 imagery and NASA GIBS layers that also work offline.
- What the satellite sees, the climate of the area, and the three rotations side by side. Each rotation carries the five fields the challenge asks for: why, evidence, benefits, information gaps and risks. Each also has water, soil and pest scores, a confidence level with its reason, and a 12-month calendar.
- Scenarios: rainfall at 0, −10, −20 or −30 % and temperature at +1.5 °C, recomputed in the browser from values the engine already calculated.
- A farmer card that can be played as audio and printed or saved as PDF.
- A “NASA product → decision” table, a “Where it fails” panel, the validation tab, and the glossary and sources.

**Preliminary observation, not a forecast:** in July and August 2026, the five plots got 20 % to 26 % of their 1991–2025 median rainfall. That's the lowest since 1991 (CHIRPS v3, final monthly product). The engine uses 2001–2025 and leaves 2026 out of every score ([docs/validation.md](docs/validation.md)).

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
| `pipeline/` | Data clients with cache: POWER, ORNL (NDVI), FIRMS, CHIRPS, SMAP (AppEEARS), SRTM, SoilGrids, GIBS | Mario |
| `motor/` | Detection, climate, scores, confidence, traffic light, ZARC, text templates in Spanish and English, phrase audio, export | Rodolfo |
| `web/` | Vite + React + react-leaflet + Recharts: farmer view, Evidence and pictograms | Team |
| `tests/` | Contract, number validator, ZARC, traffic light, English texts, phrase audio, engine with synthetic data, pipeline, validation | Everyone |
| `docs/` | Documentation in English, with the Spanish team notes in `docs/es/` ([docs/README.md](docs/README.md)) | Everyone |
| `api/` | Placeholder for an optional live API. Not built and not part of the submission | None |

## How to run it

Requirements: Python 3.11+ and Node 20+.

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
```

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
- ZARC doesn't publish planting windows by municipality.
- The audio voice is Spanish only; English listeners get English subtitles.

## NASA data

| Product | What it is used for |
|---|---|
| MODIS MOD13Q1 NDVI, 250 m (through ORNL DAAC) | Bare-soil months and crop cycles: the “soil” fact |
| FIRMS VIIRS S-NPP, 375 m | Fires near the plot: the “fire” fact |
| GPM IMERG | Splits CHIRPS pentads into days for the “canícula” fact |
| NASA POWER | Temperature, reference evapotranspiration and daily rain pattern; compared against CHIRPS in the validation |
| SMAP SPL3SMP_E (through AppEEARS) | Soil moisture: 2018 drought test, 2026 observation and confidence |
| SRTM | Slope of each plot |
| NASA GIBS | True-colour MODIS layer for the offline map |

## Other data and references

- **Data:** CHIRPS v3 (Climate Hazards Center), SoilGrids (ISRIC), Sentinel-2 cloudless (EOX), OpenStreetMap, FAO-56 and FAO-33 (crop coefficients and yield response), FAO-66, ZARC (FAO–MAGA), and the public reports cited in [docs/validation.md](docs/validation.md). Every source and its citation is in `data/fuentes.yaml` and in the glossary and sources tab of the site.
- **Software:** [React](https://react.dev/), [Leaflet](https://leafletjs.com/) with react-leaflet, [Recharts](https://recharts.org/), [Vite](https://vite.dev/), [edge-tts](https://github.com/rany2/edge-tts) for the synthetic voice and [PyYAML](https://pyyaml.org/).

## AI use

An AI coding agent wrote most of the code, the texts and the SVG pictograms under the team's direction and review. The team decided the scope, the thresholds and the validation. The audio uses a synthetic voice (edge-tts), labelled next to the player and in the ID3 tags of each mp3. Full declaration: [docs/ai-use.md](docs/ai-use.md).

## License

MIT, see [LICENSE](LICENSE). Data keep the license and citation of their source.
