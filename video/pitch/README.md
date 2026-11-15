# Video de 30 s: «De la órbita a la parcela»

El video de demostración de Milpa Resiliente para NASA Space Apps 2026: 29.8 s, 1920 × 1080, 30 fps, narración en inglés con subtítulos en inglés quemados en la imagen.

- **Video publicado:** `web/public/video/milpa-resiliente-30s.mp4` (en el sitio: https://milpa-resiliente.onrender.com/video/milpa-resiliente-30s.mp4), con sus subtítulos aparte en `milpa-resiliente-30s.en.vtt`.
- **Guion elegido y descartados:** `STORYLINES.md`. **Dirección (números, tomas, prohibiciones):** `SPEC.md`. **Revisión y límites:** `REVIEW.md`.

## Qué es real en el video

Todo lo que dice ser el producto es el producto:

| Toma | De dónde sale |
|---|---|
| La Tierra y la caída | NASA GIBS: Blue Marble Next Generation y MODIS Terra color real del 21 feb 2026, pedido en la malla nativa de 250 m (`scripts/picada.py`). Los cuadros del final son píxeles MODIS de verdad. |
| «22 %» | `web/public/data/validacion.json` → `observacion_2026.lluvia_chirps`, Olopa: 106.4 mm contra una mediana de 475.1 mm (1991-2025), lo menos desde 1991. La misma frase sale en la pantalla del sitio. |
| 6.25 ha y 0.35 ha | El píxel MODIS de 250 m y el promedio de la evaluación FAO/PMA de 2010 (`docs/impact.md`). El cuadro blanco está a escala. |
| Teléfono | Capturas a 2x del sitio compilado, Olopa, inglés (`scripts/capturas.py`). El toque en «Listen» cambia de una captura a otra: son los dos estados reales de la página. |
| «Soil: watch.» | El audio del propio sitio, `web/public/audio/olopa.frases.en.mp3`, de 2.90 a 4.30 s. |
| 33 futuros | Captura de la vista Evidence de Olopa. Los puntos se redibujan encima en la posición medida y con el estado de cada modelo de `web/public/data/futuros_nasa.json` (SSP2-4.5): 9 de 33 para lo de hoy, 33 de 33 para el maíz de ciclo corto, 9 de 33 para la canavalia. |

El sitio presenta las tres opciones de Olopa como empate de puntaje; el video no dice que haya una ganadora, solo cuenta los futuros.

## Voz y sonido

- **Narración:** Kokoro-82M corrido en esta computadora (`npx hyperframes tts`, voz `am_michael`, velocidad 1.1). Es voz de IA y el cierre lo dice. Para que lea bien el nombre, el texto que recibe la voz escribe «Milpa Reseelyentay»; los subtítulos dicen «Milpa Resiliente».
- **Tiempos de los subtítulos:** cada frase se transcribió con faster-whisper `small.en` para sacar el tiempo de cada palabra.
- **Efectos:** 8 sonidos CC0 de Openverse, con créditos en `assets/sfx/CREDITS.md`. Sin música.
- Volumen: cada voz normalizada a −17 LUFS con pico de −1.5 dBTP (`ffmpeg loudnorm`).

## Rehacerlo

Desde la raíz del repo, con internet la primera vez:

```bash
cd web && npm run build && cd ..
python video/pitch/scripts/capturas.py        # capturas reales y cajas medidas (ui.json)
python video/pitch/scripts/picada.py          # imágenes de GIBS y la caída (assets/dive/), unos 10 min
cd video/pitch
npx hyperframes@0.8.225 check                 # revisión automática
npx hyperframes@0.8.225 preview               # editar en el navegador (Studio)
npx hyperframes@0.8.225 render -o renders/milpa-resiliente-30s.mp4 --video-frame-format png
```

`picada.py` y `capturas.py` piden Python con `numpy`, `Pillow` y `playwright`. La voz necesita `kokoro-onnx` y `soundfile` en un Python aparte (`HYPERFRAMES_PYTHON=<ese python>`); los WAV ya están en `assets/voz/`, así que solo hace falta para cambiar el texto.

No se guardan en el repo (se regeneran): las imágenes de GIBS (`assets/nasa/`), la caída (`assets/dive/picada.mp4`) y los renders.
