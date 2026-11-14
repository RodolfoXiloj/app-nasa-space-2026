# Accessibility of the farmer view and the community kit

Audit of the first screen (`web/src/agricultor/`) and the kit (`web/src/kit/`) against WCAG 2.2 AA, done on 14 Nov 2026 on branch `entrega-a11y`. Evidence (the technical view) was not part of this pass; it has its own section, [Evidence view](#evidence-view), done the same day on branch `entrega-a11y-evidence`.

## What we checked

| Check | How | Result |
|---|---|---|
| No horizontal scroll or clipped text at 360, 390 and 412 px, in Spanish and English | Playwright: `scrollWidth` and every element's box against the screen edge | Pass |
| Text contrast ≥ 4.5:1, large text and semaphore shapes ≥ 3:1 | Real color pairs from `agricultor.css` and `kit.css` (table below) | Pass |
| Touch targets ≥ 48 × 48 px: language buttons, plot selector, Listen, kit buttons, See the evidence | Playwright bounding boxes | Pass |
| Visible focus and logical tab order | Playwright tabs from the top: English, Español, plot, Listen, Print, Download audio, WhatsApp, See the evidence; each stop has a 3 px outline | Pass |
| Focus kept when switching language or plot | Playwright: keyboard Enter on the language button, new plot in the selector | Pass, focus stays on the control |
| `<html lang>` follows the selector; other-language text carries `lang` | Playwright reads `document.documentElement.lang`; language buttons and engine texts carry their own `lang` | Pass |
| Every button, link, select and audio player has an accessible name in the active language | Playwright: `aria-label`, `<label>` or text | Pass |
| Listen keeps playing in the new language after a switch (es → en and en → es) | Playwright: `currentSrc` is the new mp3 and `currentTime` advances | Pass; the new mp3 starts from the beginning |

All of it runs in `python web/scripts/agricultor_playwright.py` (after `npm run build`).

## What we fixed

- **Listen subtitles are announced:** the subtitle line has `aria-live="polite"`, so TalkBack reads each phrase when it changes.
- **The audio player has a name** (`aria-label` "Listen" / "Escuchar") and a visible focus ring.
- **Listen no longer says "Spanish voice"** in English when the English mp3 exists. It says so only when English falls back to the Spanish audio.
- **Reduced motion:** a `prefers-reduced-motion: reduce` rule turns off any animation, transition or smooth scroll in the view. The view has none today; the rule keeps it that way.
- **`index.html` starts in English**, the default locale, instead of `lang="es"`. The locale store then sets `lang` on every switch.
- **First-load JavaScript back under budget:** Listen loads with `import()` after the first paint, 173.37 → 170.90 kB (see `docs/peso.md`).

Already in place and kept: language buttons with `aria-pressed` and their own `lang`; the semaphore shapes (`Senal.jsx`) are `aria-hidden` because the state word next to them says the same thing ("Good", "Watch", "Repeats", "The satellite can't see well here"); the month wheel and the year dots are `role="img"` with a title in the active language; the topic icons are decorative and hidden.

## Contrast ratios

| Pair | Ratio | Needs |
|---|---|---|
| Text `#000` on white `#fff` | 21.0 | 4.5 |
| Secondary text `#3b3b3b` on white | 11.2 | 4.5 |
| `#3b3b3b` on the green / yellow / red / grey tints (`#e6f2e6`, `#fff3bf`, `#fbe4e4`, `#f1f1f1`) | 9.7 / 10.0 / 9.2 / 9.9 | 4.5 |
| Brand title `#1d5a2c` on white (large) | 8.2 | 3.0 |
| White on "See the evidence" `#1d5a2c` (hover `#164a23`) | 8.2 (10.3) | 4.5 |
| Black on Listen yellow `#ffd200` (hover `#ffe14d`) | 14.5 (16.1) | 4.5 |
| White on the pressed language button `#000` | 21.0 | 4.5 |
| Semaphore shapes: black 3 px outline on their tint | 18.6 to 18.8 | 3.0 |
| Black outline against the shape fill: yellow / green / red | 14.5 / 4.1 / 3.7 | 3.0 |
| Green fill on its tint / red fill on its tint | 4.5 / 4.6 | 3.0 |
| "?" `#000` on the grey fill `#e4e4e4` | 16.5 | 3.0 |

The yellow and grey fills are close to their own tints (1.3 and 1.1), so these shapes rely on their black outline, which passes. Green and red fills are close to each other (1.1), as they are for anyone with red-green color blindness. That is why each state has a different shape (circle, triangle, square, dashed "?") and a word. We did not change the semaphore colors.

## Still to test on a real phone (with TalkBack)

- TalkBack reading order on the first screen: header, plot, Listen, the three facts, options, kit, Evidence.
- That each language button is read in its own voice ("English", "Español") and announced as on or off.
- That the subtitle phrases are read once each while the audio plays, and that they do not talk over the audio too much. If they do, consider announcing only when the audio is paused.
- That the native audio player controls are reachable and named.
- That the month wheel and the year dots read their title, in the active language.
- Download audio and Share on WhatsApp: what TalkBack says when they open the download or WhatsApp.
- Large system font (Android display size and font size at maximum): no clipped text at 360 px.

## Evidence view

Audit of the technical view (`web/src/components/`, opened with "See the evidence" or `#evidence`) with the same criteria, done on 14 Nov 2026 on branch `entrega-a11y-evidence`. Only the components, `evidence.css` and the `a11y` texts in `web/src/i18n/messages.js` changed. `App.jsx` and `styles.css` were left as they are: the rules that fix them live in `evidence.css`, which loads after `styles.css`.

### What we checked

| Check | How | Result |
|---|---|---|
| No horizontal scroll at 360, 390 and 412 px, in Spanish and English, on the three tabs with every `<details>` open | Playwright: `scrollWidth` and every element's box against the screen edge | Pass |
| Wide tables scroll on their own, inside a container with `role="region"`, `aria-label` and `tabindex="0"` | Playwright: every table wider than its box | Pass, 6 tables on Validation |
| Every button, link, select and `<summary>` has an accessible name in the active language | Playwright: `aria-label`, `<label>`, text or `title` | Pass |
| Buttons, selects, `<summary>`, map zoom and layers controls, and source links ≥ 48 × 48 px | Playwright bounding boxes | Pass |
| Each chart has a text alternative in es and en | Playwright: every Recharts chart sits in `role="img"` with an `aria-label` that lists the data | Pass, 5 charts |
| The map has a text alternative | Playwright: the "Plots on the map, as text" list | Pass |
| Headings in order, one `h1` | Playwright: no level jump | Pass |
| Visible focus | Playwright tabs through the first 14 stops; each has a 3 px outline | Pass |
| `prefers-reduced-motion` | Playwright with `reduced_motion="reduce"`: the map has no zoom or fade animation | Pass |

All of it runs in `python web/scripts/evidence_playwright.py` (after `npm run build`), 109 checks. It fails on the code before this pass (tabs at 40 px, charts without text, tables without a region, no focus ring).

### What we fixed

- **Charts:** the NDVI series, NDVI by month, climate, POWER vs CHIRPS and the 2018 drought chart are `role="img"` with an `aria-label` built from the data (dates, lows and highs, months per value, bare and low-cover months, points above and below the line, the high-risk years). The 2018 chart also says in visible text which years are the yellow bars, so the colour is not the only signal.
- **Map:** zoom buttons and the layers button are 48 px and named in the active language ("Zoom in" / "Acercar", "Map layers" / "Capas del mapa"; Leaflet only says "Layers"). Below the map, "Plots on the map, as text" lists each plot with its confidence, so the circle colour is not the only signal. Confidence levels are translated in the tooltip. With reduced motion the map jumps to the plot instead of flying, and zoom and fade animations are off.
- **Tables:** the six wide tables on Validation (2026 rain, SMAP cells, product → decision, where it fails, POWER vs CHIRPS, 2018) scroll inside a focusable region named after the table, in the active language.
- **12-month calendar:** it was `role="table"` with cells and no rows. It is now a list; each month reads its full name, state, crop and flags. Each state also has a texture (cover: light lines, stubble: vertical lines, bare soil: dots, burn: diagonal stripes; crop: plain), the legend swatches have a dark border, and the "!" flag is black on yellow.
- **Headings:** the card's title went from `h2` to `h3` (it sits under "Card for the farmer") and "Water / Soil / Pests" under "How the score was calculated" from `h5` to `h4`. They keep their size.
- **Language of parts:** in English, the engine texts that come in Spanish (rotation names, reasons, benefits, gaps, risks, evidence rows, the card's reason and planting window, the glossary) carry `lang="es"`, so a screen reader reads them with a Spanish voice.
- **Touch targets and focus:** tabs, language buttons, selects, scenario buttons, "See detail and limits", every `<summary>`, the ZARC link and the source URLs are 48 px tall. Every focusable element in Evidence and in the map has a 3 px dark outline.
- **Contrast:** see the table below.
- **Reduced motion:** a `prefers-reduced-motion: reduce` rule turns off animations and transitions in Evidence. Charts already had their animation off.

### Contrast ratios (Evidence)

| Pair | Before | After | Needs |
|---|---|---|---|
| Label text on light green (`.etiqueta`) | 4.2 (`#3f7d3a`) | 5.4 (`#2f6b33`) | 4.5 |
| "See detail and limits" on the 2026 band | 4.5 (`#3f7d3a`) | 5.8 (`#2f6b33`) | 4.5 |
| Month name on "crop" | 3.0 (white on `#6fa35f`) | 5.0 (`#1d2b1a`) | 4.5 |
| Month name on "bare soil" | 4.0 (white on `#a8754a`) | 5.9 (white on `#8a5a2b`) | 4.5 |
| Calendar "!" flag | 1.5 (yellow on green) | 7.6 (black on `#e0b43a`) | 4.5 |
| Monthly NDVI bars on white: covered / low cover / bare | 3.0 / 2.0 / 4.0 | 5.0 / 4.0 / 5.9 | 3.0 |
| Low-cover threshold line | 2.9 (`#b8913f`) | 4.8 (`#8f6d1f`) | 3.0 |
| 2018 chart, high-risk bars | 2.8 (`#c79100`) | 3.8 (`#a67c00`) | 3.0 |
| Legend swatches (stubble, crop) against white | 1.7, 3.0 | dark border 14.9 | 3.0 |
| Secondary text `#55624f` on white / page background | 6.5 / 5.9 | unchanged | 4.5 |
| Lines that already passed: NDVI `#3f7d3a`, bare-soil line `#8a5a2b`, ET0 `#c0622f`, rain `#5b8fb9`, 2018 bar `#b23c17` | 5.0, 5.9, 4.2, 3.5, 5.9 | unchanged | 3.0 |

### Exceptions we kept

- Links inside a sentence (public reports, "Open report", the Leaflet and OpenStreetMap attribution) are shorter than 48 px. WCAG 2.5.8 allows it for inline links.
- The map's tiles and circles are not keyboard targets: the plot list in text and the plot selector do the same job.

### Pending (outside this pass)

- `App.jsx` (not in scope) is in Spanish only: the header, the slogan, the tabs ("Parcela", "Validación", "Glosario y fuentes"), the tab bar name ("Secciones"), the example band and the footer. They need English texts.
- `App.jsx` scrolls to the 2026 observation with `behavior: 'smooth'`, which ignores reduced motion. It should check `prefers-reduced-motion` too.
- The engine data has English fields (`es` / `en` in each JSON); Evidence still shows the Spanish ones. Marking them `lang="es"` is the stopgap.
- The plot selector shows "Ejemplo (Jocotán)" in Spanish when there is no index.
- On a real phone with TalkBack: the reading of the long chart summaries, the table regions while scrolling sideways, the map controls, and the calendar list.
