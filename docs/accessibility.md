# Accessibility of the farmer view and the community kit

Audit of the first screen (`web/src/agricultor/`) and the kit (`web/src/kit/`) against WCAG 2.2 AA, done on 14 Nov 2026 on branch `entrega-a11y`. Evidence (the technical view) was not part of this pass.

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
