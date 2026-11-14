# Milpa Resiliente

**NASA Space Apps Challenge 2026 · Guatemala · Challenge "Field Shift: Adapting Farms with NASA Data"** · Team "A dream"

> The satellite already knows how your plot has been used. We show which crop rotation holds up better in the next *canícula* (mid-summer dry spell) and why, so the extension worker and the farmer can decide together.

Milpa Resiliente is a static website for agricultural extension workers in Guatemala's Dry Corridor. It covers five plots in Chiquimula and Zacapa: Jocotán, Camotán, Olopa, San Juan Ermita and Zacapa. For each plot it shows:

1. **What the satellite sees.** Months of bare soil and crop cycles from MODIS NDVI (250 m), and nearby fires from FIRMS (VIIRS, 375 m).
2. **Three rotations side by side.** The current practice, the best legume or cover-crop option, and the best drought-tolerant option.
   Each one carries the five fields the challenge asks for: why, evidence, benefits, information gaps and risks. Each one also has water, soil and pest scores, a confidence level with its reason, and a 12-month calendar.
3. **Scenarios.** Rainfall at 0, −10, −20 or −30 % and temperature at +1.5 °C. The browser recomputes them from values the engine already calculated.
4. **A card for the farmer.** It can be played as audio (a synthetic voice, labelled as AI-generated) and printed or saved as PDF.

It supports the extension worker and the farmer; it does not replace them. Planting dates are **quoted from ZARC (FAO–MAGA), never calculated**.

**Preliminary observation, not a forecast:** in July–August 2026, rainfall at the five plots was 20 % to 26 % of the 1991–2025 median, the lowest since 1991 (CHIRPS v3, final monthly product). The engine uses 2001–2025 and does not use 2026 in any score.

## How it works

```
parcelas.yaml → pipeline/precargar → data/cache/ → motor/recomendar → motor/exportar → web/public/data → static site
```

- **Static first.** The site needs no server, keys or third-party network to show the plots. Only the base map (OpenStreetMap) and the Sentinel-2 image need internet. The NASA GIBS layers are stored in the site, and without internet the map switches to the stored layer by itself.
- **One engine in plain Python** (standard library plus PyYAML), with no network. It returns the JSON defined in `contracts/recomendacion.schema.json`.
- **Cache inside the repo** (`data/cache/`). Each file records its provenance: URL, download date, product and version. The pipeline uses the network only with `MILPA_ONLINE=1`.
- **AI does not write numbers.** Texts come from deterministic templates. A validator rejects any number that is not in the engine's JSON and any planting date that does not come from ZARC.

| Folder | Contents | Owner |
|---|---|---|
| `contracts/` | JSON schema (contract v1) and a hand-written example | Rodolfo |
| `data/` | Plots, rotations, crops (FAO-56 Kc), ZARC quotes, glossary, sources and cache | Iván (YAML) · Mario (cache) |
| `pipeline/` | Data clients with cache: POWER, ORNL (NDVI), FIRMS, CHIRPS, SMAP (AppEEARS), SRTM, SoilGrids, GIBS | Mario |
| `motor/` | Detection, climate, scores, confidence, ZARC, text templates, export | Rodolfo |
| `web/` | Vite + React + react-leaflet + Recharts | Team |
| `tests/` | Contract, number validator, ZARC, engine with synthetic data, pipeline, validation | Everyone |
| `docs/` | Status, test log, validation, AI use (in Spanish for now) | Everyone |
| `api/` | Placeholder for an optional live API. Not built and not part of the submission | — |

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

The exported JSON files in `web/public/data/` are already in the repo, so the web runs without downloading anything. To rebuild them from the cache (no network):

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
MILPA_ONLINE=1 python -m motor.exportar --audio                   # also the mp3 files, with edge-tts
```

In PowerShell, use `$env:MILPA_ONLINE='1'; python ...` instead of `MILPA_ONLINE=1 python ...`.

Keys (`FIRMS_MAP_KEY`, `EARTHDATA_USERNAME`, `EARTHDATA_PASSWORD`) go in a local `.env` copied from `.env.example`. `.env` is in `.gitignore`. The pipeline reads the keys without printing them. The engine and the static site need none.

## Status and what is pending

Working today, with every real test run logged in `docs/pruebas.md`:

- Cached data for the five plots, the engine, the contract and the validation (`docs/validacion.md`).
- The technical web view, in Spanish: map, satellite panel, three rotations, scenarios, farmer card with audio and PDF, validation tab, glossary and sources.

Pending:

- **Website in English.** The web, the docs and the audio are in Spanish today.
- **"For the farmer" view** as the first screen: a three-fact traffic light, pictograms, a short audio with subtitles, and a printable sheet. The traffic-light thresholds are a proposal waiting for the team's confirmation (`docs/umbrales.md`).
- **Review by an agronomist** of the scoring rules and the eight rotation templates. Not done yet.
- **Comprehension test** with adult users. Not done yet.
- **Test on a real phone**, including TalkBack (`docs/prueba-telefono.md`). Not done yet.
- **Field check of the five points.** They were chosen from NDVI and Sentinel-2 imagery and have not been verified on the ground.
- **Public deployment.** The site is not deployed yet.

Known limits: Camotán has no SMAP value with recommended quality; NASA POWER puts four of the five plots in the same ~50 km cell; ZARC does not publish planting windows by municipality.

## Data sources

All sources and their citations are in `data/fuentes.yaml` and in the "Glosario y fuentes" tab of the site. NASA data: MODIS MOD13Q1 (via ORNL DAAC), FIRMS VIIRS, NASA POWER, SMAP SPL3SMP_E (via AppEEARS), SRTM, NASA GIBS and GPM IMERG. Other sources: CHIRPS v3, SoilGrids, Sentinel-2 cloudless, FAO-56 and FAO-33, ZARC (FAO–MAGA) and OpenStreetMap.

## AI use

The audio uses a synthetic voice (edge-tts). It is labelled next to the player and in the ID3 tags of each mp3. AI use by the team is declared in `docs/uso-ia.md`.

## License

MIT, see `LICENSE`. Data keep the license and citation of their source.

---

## En español

Milpa Resiliente es una web estática para el extensionista agrícola del Corredor Seco de Guatemala. Muestra cinco parcelas de Chiquimula y Zacapa. Para cada una compara tres rotaciones con datos de satélite de la NASA y otras fuentes citadas. Apoya al técnico y al agricultor; no los reemplaza.

- **Cómo correrla:** `pip install -r requirements.txt`, luego `python -m pytest`. Para la web: `cd web`, `npm install` y `npm run dev`.
- **Qué falta:** la web en inglés, la vista «Para el agricultor», la revisión de un agrónomo, la prueba de comprensión, la prueba en un teléfono real y el despliegue público.
- **Documentación del equipo:** `docs/estado.md`, `docs/pruebas.md` y `docs/memoria/` (empiece por `Inicio.md`).
