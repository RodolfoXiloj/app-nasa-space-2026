# Google Earth Engine: phase-two integration guide

**Status: first product done (NEX-GDDP-CMIP6 climate futures, 14 Nov 2026).** SMAP L4 and land cover below are still not implemented. Nothing in the repo imports or calls Earth Engine: the futures were precomputed in the Earth Engine Code Editor with `pipeline/gee/cmip6_cambios.js`, the exported CSV is in `data/cache/cmip6/`, and `python -m pipeline.clientes.cmip6` turns it into `data/cache/cmip6/cambios.json` with `cache.guardar`. No dependency, key or project ID was added.

### Done: NASA NEX-GDDP-CMIP6 climate futures

- **What:** for each plot, model and scenario (SSP2-4.5, SSP5-8.5), mean May-October rain, June-August rain and May-October mean temperature, 2041-2060 against 1995-2014 (`NASA/GDDP-CMIP6`, 0.25°). 33 models in SSP2-4.5 (HadGEM3-GC31-MM has no SSP2-4.5) and 34 in SSP5-8.5.
- **How it is used:** `python -m motor.futuros` applies each model's change to the observed daily series with `clima.serie_escenario`, the same as the fixed scenarios, and repeats the water balance of the 3 rotations. A rotation «holds» in a future if its water score is equal to or higher than today's rotation with today's climate. Output: `web/public/data/futuros_nasa.json`, shown in Evidence under the rotations (`FuturosNasa.jsx`). It does not change the contract, the `farmer` block, the card text or the audio.
- **Limits:** delta method on mean rain and temperature, not a change in the number of rainy days; Jocotán, Camotán and San Juan Ermita share one 0.25° cell, so they share the projected changes; the drought-tolerant rotation already starts with a higher water score, which favors it in the count.

The one fixed rule: **Earth Engine is never called live**, not from the web and not from the engine (`motor/`). It is only used offline, by the pipeline, to **precompute files in `data/cache/`**, the same way as every other source. The app must keep working with no network, and `npm run sin-red` must keep passing.

## 1. Why Earth Engine, and what it would improve

Earth Engine (GEE) hosts many ready-to-use collections and does the reduction on Google's servers, so one script can pull a point series for all 5 plots in one go, with no large rasters downloaded to `data/raw_big/`.

Two datasets would add something the cache does not have today:

| Dataset | GEE collection ID | What it adds |
|---|---|---|
| NASA SMAP L4 Global 3-hourly 9 km surface and root-zone soil moisture (SPL4SMGP, version 8) | `NASA/SMAP/SPL4SMGP/008` | Root-zone moisture, and a gap-free series |
| ESA WorldCover 10 m v200 (map of 2021, 11 classes) | `ESA/WorldCover/v200` | Land-cover class at the plot pixel |
| Dynamic World V1 (10 m, near real time since 2015, 9 classes with probabilities) | `GOOGLE/DYNAMICWORLD/V1` | Land-cover class through time, per season |

The IDs were checked against the public Earth Engine Data Catalog on 14 Nov 2026. `NASA/SMAP/SPL4SMGP/007` is retired in the catalog: use `008`. **Verify** before coding: the band names of version 8 (`sm_surface`, `sm_rootzone`, `sm_profile` in earlier versions) and the end date of the collection, which the catalog page states in two different ways.

### Compared with what `data/cache/smap/` uses today

Today `data/cache/smap/{plot}.json` comes from `pipeline/clientes/appeears_smap.py`: SMAP Enhanced L3 (`SPL3SMP_E.006`) through AppEEARS, daily, 9 km, surface layer only, recommended-quality retrievals only. That gives two known limits:

- **Camotán has no SMAP value.** Its 9 km cell never reaches recommended quality, so the engine falls back to the labeled MERRA-2 model value and confidence is «low».
- **Only the top ~5 cm.** L3 is a radiometer retrieval of surface moisture, not the root zone, which is what the crop uses.

SMAP L4 is a model with SMAP data assimilated. It has no quality gaps and gives root-zone moisture, so Camotán would get a value and every plot would get a root-zone series. Be honest about the limits in the card and in `docs/validation.md`:

- L4 is **still 9 km**. It does not separate plots that share a cell (Jocotán and San Juan Ermita share one today). It is not more precise per plot in space.
- L4 is a **model product**. It is not the same thing as an L3 retrieval and must be labeled that way, the same as the MERRA-2 fallback is labeled today.

The real gain in per-plot precision comes from **land cover at 10 m** (WorldCover or Dynamic World): a class for the exact plot pixel, to check that each point is cropland and to back up the «bare soil» and «low cover» months that today come only from 250 m NDVI.

## 2. What NOT to do

- **No live calls.** The web and the engine never import `ee`, never reach `earthengine.googleapis.com`, and never wait on GEE. Only `pipeline/` talks to GEE, and only with `MILPA_ONLINE=1`.
- **Do not change the cache format the engine already reads.** Every file stays `{"procedencia": {...}, "datos": ...}`, written with `cache.guardar`. Do not overwrite `data/cache/smap/` with L4 data: the engine expects the L3 fields there (`jul_ago_mediana`, `percentil`, `calidad`...). L4 goes to a new folder (see section 4).
- **Do not commit credentials.** No service-account JSON, no OAuth token, no real Cloud project ID in the repo, in the cache, in `procedencia`, in logs or in docs. The user credentials that `ee.Authenticate()` stores live in the user's home folder, outside the repo.
- **The web never depends on GEE.** No GEE tiles, no `ee` JavaScript library, no map layer that needs a GEE token. If a GEE result is shown, it is a precomputed value or a precomputed PNG served from the repo.
- **Do not make GEE required.** A clean clone without `earthengine-api` must install, test and run exactly as today.

## 3. Setup (for the person who runs the precompute)

1. **Account and Cloud project.** A Google account with access to Earth Engine, and a Google Cloud project registered for Earth Engine (noncommercial or research use, as applicable). Note the project ID locally. Do not write it in the repo.
2. **Python package, optional.** Install it only on the machine that precomputes:

   ```bash
   pip install earthengine-api
   ```

   When phase two is done, put it in an optional extra or a separate file (for example `requirements-gee.txt`), never in the main requirements. **It is not added today.**
3. **Environment variable.** The project ID is read from `EE_PROJECT`, from the environment or from the gitignored `.env`, through `cache.secreto("EE_PROJECT")` like the other keys. When the client is written, add only the name to `.env.example`, empty:

   ```bash
   # Google Earth Engine (phase two, optional): Cloud project ID registered for Earth Engine.
   EE_PROJECT=
   ```

4. **Authenticate once, then initialize:**

   ```python
   import ee
   ee.Authenticate()                         # once per machine; opens a browser, stores the token outside the repo
   ee.Initialize(project=os.environ["EE_PROJECT"])
   ```

## 4. Integration design

### A new client: `pipeline/clientes/gee_*.py`

One file per product, next to the current clients, for example:

- `pipeline/clientes/gee_smap_l4.py` → `data/cache/smap_l4/{plot}.json`
- `pipeline/clientes/gee_cobertura.py` → `data/cache/cobertura/{plot}.json`

Each client follows the pattern of `appeears_smap.py` and `soilgrids.py`:

- calls `cache.exigir_red()` first, so it fails with `SinRed` when `MILPA_ONLINE` is not `1`;
- reads the plots with `cache.cargar_parcelas()` (`data/parcelas.yaml`);
- imports `ee` **inside** the function, so the module loads (and tests run) without the package;
- writes one file per plot with `cache.guardar(ruta, datos, proc)`, where `proc = cache.procedencia(url=..., producto=..., version=..., nota=...)`. That gives the same metadata as today: `url`, `fecha_descarga`, `producto`, `version`, plus `nota`;
- puts `"resolucion"` and `"lat"`/`"lon"` inside `datos`, like `smap` and `suelo` do (the engine rejects caches from another coordinate);
- hides the project ID with `cache.ocultar(...)` in any error message, and never puts it in `procedencia`.

Suggested `procedencia` for L4: `url="ee.ImageCollection('NASA/SMAP/SPL4SMGP/008')"`, `producto="SMAP L4 SPL4SMGP vía Google Earth Engine"`, `version="008"`.

### Register the source in `data/fuentes.yaml`

Every source the engine or the web uses must be cited there (NASA can withdraw awards for uncited sources). Add one entry per dataset with the same keys as the others: `id`, `nombre`, `cita`, `en: {nombre, resolucion, cita}`, `url`, `resolucion`, `es_nasa`. Use the citation and DOI given on each catalog page, and add one entry for Earth Engine itself as the extraction service, like `appeears` today. Dynamic World also requires attribution to Google, National Geographic Society and World Resources Institute (CC BY 4.0); WorldCover is CC BY 4.0 too.

### A flag in `pipeline/precargar.py`

Keep GEE **out of the default run**. Add the sources by name, but not to `TODAS`, so that a normal precompute never needs GEE:

```bash
MILPA_ONLINE=1 python -m pipeline.precargar --fuentes gee_smap_l4,gee_cobertura
```

Each GEE source fails on its own, like the other sources: an error (package missing, no `EE_PROJECT`, auth expired, quota) is reported and the precompute goes on.

### Fallback: the existing cache always wins when GEE is missing

- If GEE is not installed or fails, **no cache file is touched**: write to a `.tmp` and replace only on success (`cache.guardar` already does this).
- The engine reads the new folders as **optional**. If `data/cache/smap_l4/{plot}.json` is missing, it behaves exactly as today (L3 from `data/cache/smap/`, then the labeled MERRA-2 fallback). If `data/cache/cobertura/{plot}.json` is missing, the card shows what it shows today.
- The committed cache files are what the deployed site and `sin-red` use. GEE is only a way to refresh them.

## 5. Code example (reference only, not in the repo)

Extracts the SMAP L4 series and the land-cover class at the points of `data/parcelas.yaml`. Band names and dates must be checked against the catalog (see section 1).

```python
import os
import ee
import yaml

ee.Initialize(project=os.environ["EE_PROJECT"])

with open("data/parcelas.yaml", encoding="utf-8") as f:
    parcelas = yaml.safe_load(f)["parcelas"]

puntos = ee.FeatureCollection([
    ee.Feature(ee.Geometry.Point([p["lon"], p["lat"]]), {"id": p["id"]}) for p in parcelas
])

# Land cover at the plot pixel (10 m).
worldcover = ee.ImageCollection("ESA/WorldCover/v200").first().select("Map")
clase = worldcover.sampleRegions(collection=puntos, scale=10, geometries=False).getInfo()
# -> [{"id": "jocotan", "Map": 40}, ...]   40 = cropland in WorldCover

# Dynamic World: most frequent label in the dry season of one year.
dw = (ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1")
      .filterBounds(puntos).filterDate("2025-02-01", "2025-05-01")
      .select("label").mode())
dw_seca = dw.sampleRegions(collection=puntos, scale=10, geometries=False).getInfo()

# SMAP L4: daily mean of the 3-hourly root-zone moisture, July-August of one year.
l4 = (ee.ImageCollection("NASA/SMAP/SPL4SMGP/008")
      .filterDate("2025-07-01", "2025-09-01")
      .select(["sm_surface", "sm_rootzone"]))        # verify band names for version 8

def por_imagen(img):
    fc = img.sampleRegions(collection=puntos, scale=9000, geometries=False)
    return fc.map(lambda f: f.set("fecha", img.date().format("YYYY-MM-dd")))

serie = l4.map(por_imagen).flatten().getInfo()["features"]
# Group by id and fecha in Python, average the 8 values per day, then write each plot with
# cache.guardar(cache.CACHE / "smap_l4" / f"{pid}.json", datos, proc).
```

For many years, run one request per year (or use `ee.batch.Export.table.toDrive`) to stay inside the interactive request limits, and keep the raw tables in `data/raw_big/gee/`, which is not committed.

## 6. How to verify

Run all of these before merging any phase-two change:

1. **Regenerate the cache** with the GEE flag, then run the normal processing so `web/public/data/` is rebuilt from the cache.
2. **`pytest`**: everything passes, including in an environment **without** `earthengine-api` installed.
3. **`npm run sin-red`** (in `web/`): all checks pass with the network off.
4. **Playwright** end-to-end tests: pass.
5. **Compare against the validation:** run `python -m pipeline.validacion.validar` and diff `docs/validacion.md` and `web/public/data/validacion.json` against the previous version. Check the confidence level of each plot (today: Jocotán and San Juan Ermita «high», Olopa «medium», Zacapa and Camotán «low»).
6. **If any number changes** (confidence, deficit, ranking, a card figure): say so and why in `docs/validation.md` (and regenerate the Spanish `docs/validacion.md`), and record in `docs/ai-use.md` (and `docs/es/uso-ia.md`) whatever was done with AI help. Log each test that really ran in `docs/tests.md` and `docs/es/pruebas.md`.
7. **Secret check:** `git grep` for the project ID and for `EE_PROJECT=` with a value; both must return nothing.

## 7. Current status

| Item | Status |
|---|---|
| GEE client (`pipeline/clientes/gee_*.py`) | Not written |
| `earthengine-api` dependency | Not added (optional extra planned) |
| `EE_PROJECT` in `.env.example` | Not added yet; add the name only, with the client |
| Entries in `data/fuentes.yaml` | Not added |
| Flag in `pipeline/precargar.py` | Not added |
| Engine reading `smap_l4` / `cobertura` | Not written |

Planned as phase two, only if there is time. Until then, the app uses the cache sources listed in `data/fuentes.yaml`.

## Sources

- [SPL4SMGP.008 in the Earth Engine Data Catalog](https://developers.google.com/earth-engine/datasets/catalog/NASA_SMAP_SPL4SMGP_008)
- [ESA WorldCover 10m v200 in the Earth Engine Data Catalog](https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v200)
- [Dynamic World V1 in the Earth Engine Data Catalog](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1)
- [Earth Engine Data Catalog release notes](https://developers.google.com/earth-engine/docs/data-catalog/release-notes) (version 007 of SPL4SMGP retired, 008 added)
