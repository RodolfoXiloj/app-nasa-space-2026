# Test log

English version of [es/pruebas.md](es/pruebas.md). If the two ever differ, the Spanish log wins.

Only real runs are logged: each one with the date and time it ran (Guatemala, UTC−6), the command and the result as printed.

**Correction of 14 Nov 2026:** an earlier version of this file had rows with times on Saturday 14 Nov 2026 (from 09:17 to 21:58). Those were planned times, not tests that ran, and they were removed. They remain in the git history (commit `d84918b` and earlier) only as a record of the plan, not as results.

Key: ✅ passed · ❌ failed · Pending: cannot be done yet.

## Branch `entrega-impacto-6` on top of `main` (`5a5d6d3`): Saturday 14 Nov 2026

This branch's changes: the `perdidas_documentadas` block in `validacion.json` and in `docs/validacion.md`, the 2026 limit and the SMAP, CHIRPS and Prensa Libre notes with their English, the Evidence card mp3 in the interface language, the slide screenshots and PDF regenerated, and new tests in `tests/test_validacion.py` and `tests/test_slides.py`. `sin-red.mjs` now requires `audio/{plot}.en.mp3` on the card when Evidence is in English (it used to require the Spanish mp3 in both languages); `evidence_playwright.py` checks the card mp3 in each language. Before this, the data were regenerated offline with `python -m pipeline.validacion.validar` and `python -m motor.exportar` (no `--audio`): `puntajes`, `farmer.hechos`, `farmer.opciones` and `texto_tarjeta` stayed identical in the 15 plot JSON files. Same laptop: Windows 11, Python 3.11.9 (pytest 9.0.2), Node v24.15.0, npm 11.12.1, Playwright 1.58.0; `web/node_modules` from `npm ci`. Times from `date` (UTC−6).

| Time | What | Command | Result |
|---|---|---|---|
| 17:05:14 to 17:05:24 | Automated tests | `python -m pytest -q` | ✅ only dots, up to "[100%]", no failure; exit 0 |
| 17:05:24 to 17:05:34 | Automated tests with the total | `python -m pytest -p no:cacheprovider -o addopts=''` | ✅ "237 passed in 9.43s"; exit 0 |
| 17:05:35 to 17:05:36 | Web smoke test | `cd web && npm run smoke` | ✅ 16 JSON files "ok", "audio de la tarjeta en inglés con etiqueta de IA: 5 mp3", "ok futuros_nasa (5 parcelas)"; "Prueba de humo de la web: sin fallas"; exit 0 |
| 17:05:36 to 17:05:42 | Web build | `cd web && npm run build` | ✅ "525 modules transformed", "built in 4.48s"; first-load JS `index` 171.54 kB (gzip 56.81 kB), Evidence JS 673.19 kB (gzip 190.72 kB); exit 0 |
| 17:05:42 to 17:05:55 | Offline test | `cd web && npm run sin-red -- <temp folder outside the repo>` | ✅ "23 de 23 comprobaciones pasan"; each plot's card plays `{plot}.en.mp3`; exit 0 |
| 17:05:55 to 17:06:04 | Farmer view and kit at 360, 390 and 412 px | `python web/scripts/agricultor_playwright.py` | ✅ "77 de 77 comprobaciones pasan"; exit 0 |
| 17:06:04 to 17:06:19 | Evidence view at 360, 390 and 412 px | `python web/scripts/evidence_playwright.py` | ✅ "143 de 143 comprobaciones pasan"; exit 0 |
| 17:06:19 to 17:06:21 | Slides PDF | `cd web && python scripts/slides_pdf.py` | ✅ "docs/slides/milpa-resiliente.pdf: 7 páginas (tope 7)"; "python-pptx no está instalado: no se genera .pptx"; exit 0 |
| 17:06:21 to 17:06:22 | Canícula sensitivity | `python -m pipeline.validacion.sensibilidad_canicula --verificar` | ✅ "OK 'sat': jocotan 2, camotan 2, olopa 0, san_juan_ermita 1, zacapa 3 de 25 años"; "OK 'rnl': caché completa; totales mensuales iguales a 'sat'"; exit 0 |

Before this run, the same battery had two failures, which were fixed:

- `evidence_playwright.py` (no time logged): "137 de 143". The 6 failures were in "Validación", "sin scroll horizontal" (width 419 to 420 px), caused by the CHIRPS README URL in the new note. `.lista-compacta li` was added to the `overflow-wrap: anywhere` rule in `evidence.css`; then "143 de 143".
- `npm run sin-red`, 16:58:38 to 17:00:05: "18 de 23", exit 1. The 5 "Parcela …: 3 rotaciones, tarjeta y audio mp3" checks expected `audio/{plot}.mp3` with Evidence in English, which now plays `audio/{plot}.en.mp3`. The check now requires the mp3 of the active language; then "23 de 23".

## Branch `entrega-impacto-1` on top of `main` (`4fdf64f`): Saturday 14 Nov 2026

While this branch was in progress, `main` gained three commits (`61bf817`, `b69bcd1` and `4fdf64f`: English card audio, slides and sources). The branch was rebased onto `4fdf64f`, with no file in common, and every command was run again on the rebased branch with this branch's changes. Same laptop and versions as the next section; `web/node_modules` comes from the `npm ci` logged there. Times from `date` (UTC−6).

| Time | What | Command | Result |
|---|---|---|---|
| 16:11:47 to 16:11:57 | Automated tests | `python -m pytest -q` | ✅ only dots, up to "[100%]", no failure; exit 0 |
| 16:11:57 to 16:12:06 | Web smoke test | `cd web && npm run smoke` | ✅ 16 JSON files "ok", `observacion_2026` "ok" and "audio de la tarjeta en inglés con etiqueta de IA: 5 mp3"; "Prueba de humo de la web: sin fallas"; exit 0 |
| 16:12:06 to 16:12:14 | Web build | `cd web && npm run build` | ✅ "523 modules transformed", "built in 6.11s"; first-load JS `index` 170.90 kB (gzip 56.50 kB), Evidence JS 657.80 kB (gzip 184.77 kB); exit 0 |
| 16:12:14 to 16:12:28 | Offline test | `cd web && npm run sin-red -- <temp folder outside the repo>` | ✅ "23 de 23 comprobaciones pasan"; exit 0 |
| 16:12:28 to 16:12:37 | Farmer view and kit at 360, 390 and 412 px | `python web/scripts/agricultor_playwright.py` | ✅ "77 de 77 comprobaciones pasan"; exit 0 |
| 16:12:37 to 16:12:49 | Evidence view at 390 and 412 px | `python web/scripts/evidence_playwright.py` | ✅ "109 de 109 comprobaciones pasan"; exit 0 |
| 16:12:49 to 16:12:50 | Slides PDF | `cd web && python scripts/slides_pdf.py` | ✅ "docs/slides/milpa-resiliente.pdf: 7 páginas (tope 7)"; "python-pptx no está instalado: no se genera .pptx"; exit 0. The rewritten PDF was restored with `git checkout` |
| Right after, before 16:13:17 | Automated tests with the total | `python -m pytest` | ✅ "226 passed in 9.53s" |
| Right after, before 16:13:17 | The same in the clean environment outside the repo | `python -m pytest -q` (with the clean environment's Python) | ✅ exit 0 |

## Branch `entrega-impacto-1`, first pass on `eed0b1f`: Saturday 14 Nov 2026

This branch changes only documents, `requirements.txt` and `render.yaml`. The web and browser runs below were made on the branch at commit `eed0b1f` (the same as `main`), before those changes; the last three rows ran after them. Same laptop: Windows 11, Python 3.11.9 (pytest 9.0.2), Node v24.15.0, npm 11.12.1, Playwright 1.58.0. The worktree had no `web/node_modules`, so `npm ci` ran first. Times are the ones `date` printed at the start and end of each command (UTC−6).

| Time | What | Command | Result |
|---|---|---|---|
| 15:57:47 to 15:57:56 | Install the web dependencies | `cd web && npm ci` | ✅ "added 108 packages, and audited 109 packages in 8s"; "found 0 vulnerabilities"; exit 0 |
| 15:57:56 to 15:58:15 | Automated tests | `python -m pytest -q` | ✅ only dots, up to "[100%]", no failure; with `addopts = "-q"` in `pyproject.toml` this command prints no total; exit 0 |
| 15:58:15 to 15:58:19 | Web smoke test | `cd web && npm run smoke` | ✅ 16 JSON files "ok" and `observacion_2026` "ok"; "Prueba de humo de la web: sin fallas"; exit 0 |
| 15:58:19 to 15:58:27 | Web build | `cd web && npm run build` | ✅ vite v6.4.6, "523 modules transformed", "built in 5.98s"; first-load JS `index` 170.90 kB (gzip 56.50 kB), Evidence JS 657.80 kB (gzip 184.77 kB); exit 0 |
| 15:58:27 to 15:58:46 | Offline test | `cd web && npm run sin-red -- <temp folder outside the repo>` | ❌ "21 de 23 comprobaciones pasan"; exit 1. The two checks marked "NO": the San Juan Ermita card audio ("suena 0.0 s de 67 s"), and "Español elegido en Evidence sigue al volver a la vista del agricultor" (it printed "en: What the satellite saw on this plot") |
| 16:01:02 to 16:01:16 | Offline test, repeated with nothing changed | `cd web && npm run sin-red -- <another temp folder>` | ✅ "23 de 23 comprobaciones pasan"; exit 0. The cause of the two failures in the first run was not found |
| 15:58:46 to 15:58:57 | Farmer view and kit at 360, 390 and 412 px | `python web/scripts/agricultor_playwright.py` | ✅ "77 de 77 comprobaciones pasan"; exit 0 |
| 15:58:57 to 15:59:09 | Evidence view at 390 and 412 px | `python web/scripts/evidence_playwright.py` | ✅ "109 de 109 comprobaciones pasan"; exit 0 |
| 15:59:09 to 15:59:11 | Slides PDF | `cd web && python scripts/slides_pdf.py` | ✅ "docs/slides/milpa-resiliente.pdf: 7 páginas (tope 7)"; "python-pptx no está instalado: no se genera .pptx"; exit 0. The command rewrote `docs/slides/milpa-resiliente.pdf`; it was restored with `git checkout` |
| 15:59:48 to 16:00:46 | Clean environment outside the repo | `python -m venv <temp folder>`, `pip install -r requirements.txt`, `python -m pytest -q` | ✅ installed PyYAML 6.0.3, requests 2.34.2, pytest 9.2.0, jsonschema 4.26.0 and Pillow 13.0.0; only dots, up to "[100%]", no failure |
| 16:08:43 to 16:08:52 | Automated tests, after this branch's changes | `python -m pytest -q` | ✅ only dots, up to "[100%]", no failure; exit 0 |
| 16:08:52 to 16:09:01 | The same, in the clean environment | `python -m pytest -q` (with the clean environment's Python) | ✅ only dots, up to "[100%]", no failure; exit 0 |
| Right after (no time logged) | Automated tests with the total | `python -m pytest` | ✅ "222 passed in 8.10s" |

Before the clean-environment row, a first clean environment without Pillow (no time logged) failed 3 tests in `tests/test_pipeline.py` (`test_lzw_igual_que_pillow`, `test_lzw_con_muchos_codigos`, `test_lector_ligero_lee_solo_hasta_la_columna`) with "ModuleNotFoundError: No module named 'PIL'". That is why Pillow is now a required line in `requirements.txt`.

## English Listen audio merged into `main`: Saturday 14 Nov 2026

The `entrega-audio-en` branch merged as one commit onto `main` (with the kit, the docs and the slides). The short phrase audio now has an English voice (`audio/{plot}.frases.en.mp3`, en-US-JennyNeural) that Listen plays when the locale is English. The longer card audio in Evidence is still the Spanish voice (es-GT-MartaNeural). Merge changes: the kit's "Download audio" offers the English mp3 when the locale is English (Spanish if it is missing); Listen no longer resets when the language changes and, if it was playing, continues with the new language's mp3. Same laptop and versions. Times from `date`.

| Time | What | Command | Result |
|---|---|---|---|
| 14:30:05 to 14:30:13 | Automated tests | `python -m pytest -q` | ✅ 222 pass; exit 0 |
| 14:30:13 to 14:30:15 | Web smoke test | `cd web && npm run smoke` | ✅ "Prueba de humo de la web: sin fallas" |
| 14:30:15 to 14:30:20 | Web build | `cd web && npm run build` | ✅ 523 modules; first-load JS 173.37 kB (gzip 57.27 kB), see [peso.md](peso.md) |
| 14:30:20 to 14:30:33 | Offline test | `cd web && npm run sin-red -- <temp folder>` | ✅ 23 of 23; Listen plays `jocotan.frases.en.mp3` with `.frases.en.vtt`; the kit downloads `jocotan.frases.en.mp3` (200 audio/mpeg) |
| 14:30:33 to 14:30:37 | Farmer view at 390 and 412 px | `python web/scripts/agricultor_playwright.py` | ✅ 25 of 25 |
| 14:30:37 to 14:30:39 | Slides PDF | `python web/scripts/slides_pdf.py` | ✅ 7 pages (limit 7) |

## Short English audio (branch `entrega-audio-en`, before the commit of this delivery)

Setup: Windows 11, Python 3.11.9 (pytest 9.0.2), Node v24.15.0, npm 11.12.1. `npm ci` in `web/` (the repo's lockfile). mp3 generation: `MILPA_ONLINE=1 python -m motor.exportar --audio` and then `python -m motor.exportar` to link the JSON files.

**What Evidence plays in English:** the interface (menus, rotations, card, validation) is in English, but the longer card audio of each plot is still `audio/{plot}.mp3` with the **es-GT-MartaNeural** voice (the same file as in Spanish). The short English audio (`audio/{plot}.frases.en.mp3`, en-US-JennyNeural voice) is used only by the farmer view, with the **Listen** button on the first screen.

| What | Command | Result |
|---|---|---|
| Automated tests | `python -m pytest -q` | ✅ 217 pass; exit 0 |
| Web smoke test | `cd web && npm run smoke` | ✅ 16 JSON files + `observacion_2026`; no failures |
| Build | `cd web && npm run build` | ✅ vite v6.4.6, 519 modules, ~3.5 s |
| Offline test | `cd web && npm run sin-red -- <temp folder>` | ✅ 20 of 20; Listen with `jocotan.frases.en.mp3` and `.frases.en.vtt` subtitles; Jocotán totals 80/88/87 unchanged |

## Step 0 baseline: Saturday 14 Nov 2026 (commit `15c5130`)

After adding the `farmer` block to the contract, the border contrast and the non-breaking spaces in `Controles.jsx`. No data were regenerated: the JSON files and mp3s in `web/public/` are the same as in the previous baseline. Same laptop and versions (Python 3.11.9, pytest 9.0.2, Node v24.15.0, npm 11.12.1). Times are the ones `date` printed at the start and end of each command.

| Date and time | What | Command | Result |
|---|---|---|---|
| 14 Nov 2026, 12:58:16 to 12:58:21 | Automated tests | `python -m pytest -rs` | ✅ 98 pass, 0 fail, 0 skipped (3.83 s); exit 0. The previous 79 plus 19 new ones in `tests/test_farmer.py` |
| 14 Nov 2026, 12:58:25 to 12:58:56 | Web smoke test | `cd web && npm run smoke` | ✅ 16 of 16 JSON "ok" and `observacion_2026` "ok"; "Prueba de humo de la web: sin fallas"; exit 0 |
| 14 Nov 2026, 12:58:56 to 12:59:07 | Web build | `cd web && npm run build` | ✅ vite v6.4.6, 498 modules, "built in 10.00s"; JS 770.39 kB (220.58 kB gzip) and CSS 24.99 kB; exit 0 |
| 14 Nov 2026, 12:59:11 to 12:59:23 | Offline test (headless Edge, on the previous build) | `cd web && npm run sin-red -- <temp folder outside the repo>` | ✅ "14 de 14 comprobaciones pasan"; exit 0. The same 14 checks listed below; audio 71 to 73 s and PDF 61 KB |
| 14 Nov 2026, 12:59:29 | Processes after the tests | `Get-NetTCPConnection` (ports 4173, 4174 and 9334) + search for headless Edge and vite processes + `git status --short` | ✅ no port listening, no headless Edge or vite process; clean working tree |

Before this baseline, on the same day (no time logged), `motor.recomendar.recomendar()` was run in memory for the 5 plots without writing files: the `farmer` block meets the schema and `contrato.errores_textos` reports no errors for any plot. Those runs give the figures in [thresholds.md](thresholds.md).

## Baseline: Saturday 14 Nov 2026 (commit `d84918b`)

Setup: Windows 11 laptop, Python 3.11.9 (pytest 9.0.2), Node v24.15.0 and npm 11.12.1. Nothing was installed: `web/node_modules` was already present. Times are the ones `date` printed at the start and end of each command.

| Date and time | What | Command | Result |
|---|---|---|---|
| 14 Nov 2026, 12:09:41 to 12:09:47 | Automated tests | `python -m pytest -rs` | ✅ 79 pass, 0 fail, 0 skipped (3.91 s); exit 0 |
| 14 Nov 2026, 12:09:51 to 12:10:22 | Web smoke test | `cd web && npm run smoke` | ✅ 16 of 16 JSON "ok" (per the script, each with 6 components × 3 scenarios and its mp3 with the AI tag) and `observacion_2026` "ok"; "Prueba de humo de la web: sin fallas"; exit 0 |
| 14 Nov 2026, 12:10:29 to 12:10:39 | Web build | `cd web && npm run build` | ✅ vite v6.4.6, 498 modules, "built in 9.38s"; JS 770.39 kB (220.58 kB gzip) and CSS 24.94 kB; exit 0 |
| 14 Nov 2026, 12:10:45 to 12:10:56 | Offline test (headless Edge with a non-existent proxy, on the previous build) | `cd web && npm run sin-red -- <temp folder outside the repo>` | ✅ "14 de 14 comprobaciones pasan"; exit 0. Details below |
| 14 Nov 2026, 12:11 | Processes and working tree after the tests | `Get-NetTCPConnection` (ports 4173, 4174 and 9334) + search for headless Edge and vite processes + `git status --short` | ✅ no port listening, no headless Edge or vite process; clean working tree |

The 14 checks of `npm run sin-red`, as printed:

1. No internet: the request to `tile.openstreetmap.org` failed ("Failed to fetch").
2. The page opens (title).
3. The 2026 observation is on the first screen, without "alert".
4. to 8. The 5 plots (Jocotán, Camotán, Olopa, San Juan Ermita, Zacapa): 3 rotations, card and an mp3 that plays (71 to 73 s long), with the AI label.
9. The map switches by itself to the "MODIS true colour (offline)" layer: 4 local tiles, with a notice and the layer control checked.
10. Validation tab with the 2026 details.
11. Glossary and sources tab (cites IMERG).
12. Print or save as PDF: 61 KB.
13. Local requests: 20, all answered. The browser aborted 6 mp3 downloads after they answered (206, `net::ERR_ABORTED`); the script does not count that as a failure.
14. External requests: 19 (`tile.openstreetmap.org`); none got through.

No test failed in this run.

These two baselines were run before the farmer view, the pictograms and the phrase audio were merged into `main`.

## Pending

These cannot be done yet, so they have no time or result:

| Test | Status |
|---|---|
| Real phone (Android or iPhone), with the checklist in [es/prueba-telefono.md](es/prueba-telefono.md) | Pending |
| TalkBack (Android screen reader) on the phone | Pending |
| Review of the scoring rules and the 8 templates with an agronomist or extension worker | Pending |
| Comprehension test with users (card, pictograms and audio) | Pending |

## No real run logged

The earlier log also listed these tests and tasks as done, with planned times. They were not run in this baseline, so they have no result:

- Online queries and downloads: POWER, ORNL, FIRMS, CHIRPS, SoilGrids (REST and its WCS fallback), SMAP through AppEEARS, GIBS and Sentinel-2.
- `python -m pipeline.validacion.validar` and `python -m motor.exportar` (with or without `--audio` or `--etiquetar`).
- Cross-check of card figures against `data/cache/` (plan 12.6). The script is not in the repo.
- The web served on the local network (`npx vite preview --host 0.0.0.0`) and opened through the laptop's IP.
- The web with internet in headless Edge (no proxy).
- The screenshots in `docs/capturas/` and their checks (audio, console, card overflow at 360, 390 and 1366 px).
- The negative test of the smoke test's audio check (remove an mp3 and see it fail).
