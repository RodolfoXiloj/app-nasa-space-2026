# AI use in Milpa Resiliente

The Space Apps 2026 guide asks every team to say how it used AI (the form calls it "Super Intelligence", SI). This is our declaration. The Spanish working log it comes from is [es/uso-ia.md](es/uso-ia.md).

## In one paragraph

An AI coding agent wrote most of the code, most of the texts and the SVG code of the pictograms. It always worked under the direction of the team, and the team reviewed what it produced. The team decided the scope, the traffic-light thresholds, the tie rule, the five plots and how to validate the engine. The voice in the audio is synthetic (edge-tts). No AI produces any number that the farmer or the extension worker sees.

## What the AI did

| Tool | What it did | What the team did |
|---|---|---|
| Claude (Anthropic), coding agent | Wrote most of the code: data clients in `pipeline/`, the engine in `motor/`, the tests in `tests/` and the web in `web/` | Set the plan and the work lanes (`docs/es/carriles.md`), reviewed the changes and merged them into `main` |
| Claude (Anthropic), coding agent | Wrote most of the texts: the card templates, the English texts in `motor/ingles.py`, the web copy, the README and the docs | Read and corrected them; decided what the farmer view says and what it never says (no "alert", no forecast) |
| Claude (Anthropic), coding agent | Wrote the SVG code of the pictograms in `web/src/pictos/` | Chose what each drawing stands for and reviewed every drawing. The comprehension test with users is still pending (`docs/pictos.md`) |
| Claude (Anthropic), research subagent with web search | Found and read sources for crop coefficients (Kc), yield response (Ky), rotations, ZARC and the 2018 losses | Checked each quote against the source document; quotes that could not be checked are labelled "not verified" in `data/fuentes.yaml` |
| An AI assistant | Compared the project idea with five other ideas before we started building | Chose the idea and the challenge |
| edge-tts (Microsoft neural voice `es-GT-MartaNeural`) | Reads aloud the text the engine wrote: one mp3 per plot, in Spanish, with Spanish and English subtitles | Decided to label the voice as AI-generated everywhere it plays |

## What the team decided, not the AI

- **Scope:** five example plots in Chiquimula and Zacapa, three rotations per plot, a farmer view first and the Evidence view one tap away.
- **Thresholds:** the traffic-light cut-offs, gray per fact and the 3-point tie rule. Rodolfo confirmed them ([thresholds.md](thresholds.md)).
- **Validation:** the rule fixed before seeing the result (no tuning so that 2018 comes out right), POWER against CHIRPS, the 2018 drought test and the July-August 2026 observation ([validation.md](validation.md)).
- **What the tool must never do:** calculate planting dates (they are quoted from ZARC), show an official alert, or replace the extension worker.

## Rules that keep AI away from the numbers

- Every number comes from data (NASA and other cited sources) and from rules written in `motor/`.
- The texts come from deterministic templates. No language model rewrites them when the site is exported: `LLM_API_KEY` in `.env.example` is optional and unused.
- If a language model ever rewrites a text, a validator (`motor/redaccion.py`) rejects any number that is not in the engine's JSON and any planting date that does not come from ZARC, and the template is used instead.

## How the synthetic voice is labelled

- The web says next to the player that it is a synthetic, AI-generated voice.
- Each mp3 carries ID3 tags that say so (`TPE1`, `COMM` and `TXXX:AI_GENERATED`; `motor/audio_id3.py`).
- `npm run smoke` fails if an mp3 lacks the tag. An mp3 is linked only if it was generated from the card's current text.

## What a person still has to check

- An agronomist or extension worker has not reviewed the scoring rules and the eight rotation templates yet.
- The pictograms have not passed the comprehension test with users yet.
