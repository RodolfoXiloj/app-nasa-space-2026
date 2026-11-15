# AI use in Milpa Resiliente

The Space Apps 2026 guide asks every team to say how it used AI (the form calls it "Super Intelligence", SI). This is our declaration. The Spanish working log it comes from is [es/uso-ia.md](es/uso-ia.md).

## In one paragraph

An AI coding agent (Claude, by Anthropic) wrote most of the code, most of the texts in both languages and the SVG code of the pictograms, always under the team's direction and review. A research agent with web search found the agronomic sources and, on 14 November, the impact figures and the status of each sensor; every figure we use carries its URL, and the ones that could not be confirmed were left out. Before building, an AI assistant compared this idea with five others; the team chose. The team decided the scope, the five plots, the traffic-light thresholds, the tie rule and the validation rule. The audio uses synthetic voices (edge-tts: es-GT-MartaNeural and en-US-JennyNeural), labelled as AI-generated next to the player and in each mp3's tags. No AI produces any number the user sees: numbers come from the data and from rules in code, and texts come from fixed templates checked by a validator that rejects any number that is not in the engine's output. It is the same text as the SI field of the submission form ([project-page-en.md](project-page-en.md)).

## What the AI did

| Tool | What it did | What the team did |
|---|---|---|
| Claude (Anthropic), coding agent | Wrote most of the code: data clients in `pipeline/`, the engine in `motor/`, the tests in `tests/` and the web in `web/` | Set the plan and the work lanes (`docs/es/carriles.md`), reviewed the changes and merged them into `main` |
| Claude (Anthropic), coding agent | Wrote most of the texts: the card templates, the English texts in `motor/ingles.py`, the web copy, the README and the docs | Read and corrected them; decided what the farmer view says and what it never says (no "alert", no forecast) |
| Claude (Anthropic), coding agent | Wrote the SVG code of the pictograms in `web/src/pictos/` | Chose what each drawing stands for and reviewed every drawing. A first comprehension test with 3 adults who are not farmers ran on 15 Nov 2026; the test with farmers is still pending (`docs/pictos.md`) |
| Claude (Anthropic), research subagent with web search | Found and read sources for crop coefficients (Kc), yield response (Ky), rotations, ZARC and the 2018 losses | Checked each quote against the source document; quotes that could not be checked are labelled "not verified" in `data/fuentes.yaml` |
| Claude (Anthropic), research agent with web search (14 Nov 2026) | Found the impact figures, the tools that already exist and the status of each sensor (Suomi NPP, Terra, CHIRPS v3, POWER) | Decided which figures to use; the ones the agent marked as uncertain were left out. Each figure has its URL in [impact.md](impact.md) |
| An AI assistant | Compared the project idea with five other ideas before we started building | Chose the idea and the challenge |
| Claude (Anthropic), coding agent (14 Nov 2026) | Reviewed the documents for consistency with the code and the data and drafted the corrections | Rodolfo approves each merge into `main` |
| Claude (Anthropic), coding agent (14 Nov 2026) | Wrote and rendered the 30-second demo video in `video/pitch/` with HyperFrames: the script, the scenes, the captions and the scripts that capture the real site and the NASA GIBS imagery | Chose the storyline, English narration and sound effects without music. A person still has to watch and hear the whole video |
| Claude (Anthropic), coding agent (15 Nov 2026) | Rewrote the farmer-view sentences in plain words (what the satellite saw, when and how often), changed the state words to "Watch out" and "Happens often", added the "This year" and "The future" cards, generated the audio of the 5 plots again and made the plot saved for use without signal open first | Rodolfo asked for sentences anyone can understand and approved the change; the numbers still come from the engine and the validator checks each one |
| Claude (Anthropic), coding agent (15 Nov 2026) | Built the final 30-second demo video with HyperFrames from real screens of the site and our data: the scenes, the captions and the 2018 Jocotán card (17 days in a row with almost no rain in our CHIRPS data; Prensa Libre, 1 Oct 2018) | Rodolfo approved the script line by line before any voice was generated, chose the real 2018 case and approved the final video |
| Kokoro-82M (open voice model, run on our computer) and faster-whisper `small.en` | Kokoro reads the demo video's English narration; faster-whisper gives each word's time for the captions | The video's end card labels the narration as an AI voice |
| ElevenLabs (synthetic voice "Brian", model `eleven_multilingual_v2`) | Reads the narration of the final 30-second demo video | The video's end card labels the narration as an AI voice |
| edge-tts (Microsoft neural voices `es-GT-MartaNeural` and `en-US-JennyNeural`) | Reads aloud the text the engine wrote: a short phrase mp3 per plot in Spanish and another in English, each with subtitles; and a longer card mp3 per plot in Spanish and in English (the Evidence page plays the one that matches the interface language) | Decided to label the voice as AI-generated everywhere it plays |

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
- Nobody has listened yet to the 10 new phrase mp3s of 15 November (Spanish and English), nor checked the new sentences and the two new cards with a farmer (`docs/es/preguntas-agricultor.md`, block 6).
- A person has not yet re-opened every page behind the impact figures added on 14 November.
