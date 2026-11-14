# Test log

English version of [es/pruebas.md](es/pruebas.md). If the two ever differ, the Spanish log wins.

Only real runs are logged: each one with the date and time it ran (Guatemala, UTC−6), the command and the result as printed.

**Correction of 14 Nov 2026:** an earlier version of this file had rows with times on Saturday 14 Nov 2026 (from 09:17 to 21:58). Those were planned times, not tests that ran, and they were removed. They remain in the git history (commit `d84918b` and earlier) only as a record of the plan, not as results.

Key: ✅ passed · ❌ failed · Pending: cannot be done yet.

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
- `graphify update .` and the review of the `[[links]]` in `docs/es/memoria/`.
