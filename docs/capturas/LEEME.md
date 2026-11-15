# Capturas del sitio

Todas salen de la web compilada (`npm run build` en `web/`), servida con `vite preview` en `127.0.0.1`, con Chromium sin interfaz (Playwright). Se rehicieron el sábado 14 nov 2026, de 18:26:02 a 18:26:46 (Guatemala, UTC−6), con la línea de julio-agosto 2026 en la vista del agricultor, el título en español «alrededor de esta parcela» y la tabla de pérdidas en Validación. Las capturas anteriores de esta carpeta eran del prototipo en español, de antes de la vista del agricultor, y se reemplazaron.

| Capturas | Qué muestran | Comando (en `web/`, después del build) |
|---|---|---|
| `escritorio-*.png` y `telefono-*.png` (26) | Vista Evidence en español, a 1366 × 768 y a 390 × 844 | `python scripts/evidence_capturas.py` |
| `agricultor-390-es-jocotan.png` y `agricultor-412-en-olopa.png` | Vista del agricultor, página entera | `python scripts/agricultor_playwright.py --capturas` |
| `en/farmer-390-*.png` (4) | Las pantallas en inglés que usan las diapositivas (`docs/slides/`) | `python scripts/slides_capturas.py` |
| `pictos.png` | Los pictogramas a 390 px (`docs/pictos.md`); no cambió desde el paso de los pictogramas | — |

## Vista Evidence

Cada captura es una pantalla visible, no la página entera.

| N.º | Vista | Escritorio | Teléfono |
|---|---|---|---|
| 01 | Primera pantalla de Evidence, con la observación preliminar de julio-agosto 2026 | `escritorio-01-primera-pantalla-observacion-2026.png` | `telefono-01-primera-pantalla-observacion-2026.png` |
| 02 | Mapa con las 5 parcelas | `escritorio-02-mapa-5-parcelas.png` | `telefono-02-mapa-5-parcelas.png` |
| 03 | «Lo que ve el satélite» y «Clima de la zona» | `escritorio-03-satelite-y-clima.png` | `telefono-03-satelite-y-clima.png` |
| 04-08 | Tarjeta para el agricultor con el reproductor de audio, una por parcela: Jocotán, Camotán, Olopa, San Juan Ermita, Zacapa | `escritorio-04-tarjeta-jocotan.png` … `escritorio-08-tarjeta-zacapa.png` | `telefono-04-tarjeta-jocotan.png` … `telefono-08-tarjeta-zacapa.png` |
| 09 | Comparación de las 3 rotaciones (Jocotán) | `escritorio-09-rotaciones-jocotan.png` | `telefono-09-rotaciones-jocotan.png` |
| 10 | Pestaña Validación | `escritorio-10-validacion.png` | `telefono-10-validacion.png` |
| 11 | Detalle de la observación de julio-agosto 2026 | `escritorio-11-observacion-2026-detalle.png` | `telefono-11-observacion-2026-detalle.png` |
| 12 | Glosario y fuentes | `escritorio-12-glosario-y-fuentes.png` | `telefono-12-glosario-y-fuentes.png` |
| 13 | Sin internet: el mapa pasa solo a la capa guardada «Color real MODIS», con su aviso | `escritorio-13-sin-internet-mapa-capa-guardada.png` | `telefono-13-sin-internet-mapa-capa-guardada.png` |

Las capturas 01 a 12 se toman con internet (mapa base de OpenStreetMap). En la 13 el script corta toda petición que no vaya al servidor local, y el mapa cambia solo a la capa guardada.

Son una foto del sitio, no una prueba: lo que se comprueba (desbordes, nombres accesibles, tamaños de toque, audio) está en `web/scripts/evidence_playwright.py`, `agricultor_playwright.py` y `sin-red.mjs`, y sus corridas en `docs/es/pruebas.md`.
