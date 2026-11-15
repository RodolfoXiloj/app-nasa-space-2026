# SPEC: Milpa Resiliente, pitch de 30 s

```text
GOAL:    the judge remembers "NASA pixels → three facts a farmer can hear → 9 vs 33 futures, same evidence for both".
OUTPUT:  HyperFrames 0.8.225, 1920 x 1080, 30 fps, MP4 with English captions burned in.
TIME:    29.8 s x 30 = 894 frames. No music; the voice is the clock.
LOOK:    world 1 = real NASA imagery (GIBS Blue Marble NG, MODIS Terra 21 Feb 2026, native 250 m grid), space #05080d.
         world 2 = the site: paper #ffffff on ground #f7f4ec, ink #000, wordmark green #1d5a2c,
         accent yellow #ffd200 only on the pixel square, the 22 % and the Listen button (the site's own yellow).
         Futures dots: grey #ddd7c8, green #3f7d3a (the site's colours).
         Type: Roboto 900 display (wordmark 150 px, hero number 220 px, -1 % tracking); Roboto 700/500 body 32-52 px.
         Cards and captions use the farmer view's own box: white, 4 px black border, no radius, no shadow.
OBJECTS: the Earth (orthographic, real texture); the MODIS pixel (yellow 5 px square with a 9 px black under-stroke);
         a 0.35 ha plot (white square, 3 px black border, to scale); a phone (black bezel 20 px, radius 56,
         real 2x screenshots of the live build); the Evidence futures panel (real 2x screenshot, dots rebuilt
         live at their measured positions with their real per-model state).
MOTION:  arrivals expo.out / power4.out 0.35-0.6 s; camera power2.inOut 0.45-0.6 s; zoom-through power3.in 0.35 s;
         exits 40-50 % of entries; words 0.067 s apart; dots 0.08 s (9) and 0.032 s (33) apart.
         Render-time motion blur on the root for the fast scrolls.
SHOTS:
  0.00-4.97   Earth turns and dives to Olopa (baked video). Right: "22 %" counts down from 100, "of normal rain,
              July-August 2026", "lowest since 1991 · CHIRPS v3". Yellow square appears on Olopa at 0.6 and becomes
              the real MODIS pixel. Sound: deep whoosh.
  4.97-8.05   Pixel hold: grid draws out; card "1 MODIS pixel / 250 m x 250 m = 6.25 ha" (pop); white 0.35 ha square
              and card "A family plot / about 0.35 ha (FAO/WFP)" (pop). Voice: "...one pixel at a time."
  8.05-8.55   The pixel fills white and grows to the frame (object becomes the world). Whoosh.
  8.55-10.0   "Milpa Resiliente" letter by letter on the voice's name.
  10.0-13.7   Wordmark shrinks into the real phone header; page scrolls through the three facts at 1.9x;
              back up to Listen on "and hear".
  13.7-15.95  Tap Listen (click), real UI state changes; the site's own voice: "Soil: watch."; scroll to
              "See the evidence".
  15.95-16.45 Tap, zoom through the green button.
  16.45-22.6  Futures panel settles from 1.15x; punch-in on "What you do today": 9 dots turn green; pan to
              "Short-cycle maize": 33 turn green; pull back, jack bean's 9.
  22.6-26.9   Panel moves right, phone enters left: "For the farmer" / "For the extension worker".
  26.9-29.8   End card: yellow square lands, wordmark wipes in, URL button, team line, credits. Riser into it.
BANNED:  defaults in spec.md; plus: invented UI or numbers, a winner claim for Olopa (the site calls it a tie),
         music, glow on the globe, stars, a logo in a corner, text over the caption band.
QA:      0.2 (globe + 22 % readable), 4.0 (square tracks pixel), 6.8 (both cards, plot square inside pixel),
         8.4 (white flood), 9.3 (wordmark), 11.9 (fact card readable >= 28 px), 14.5 (subtitle box + caption),
         16.2 (green zoom-through), 19.4 (9 green dots match the site), 21.9 (33 green), 24.5 (two views),
         28.5 (end card complete), every caption inside the 80 % title-safe box.
```
