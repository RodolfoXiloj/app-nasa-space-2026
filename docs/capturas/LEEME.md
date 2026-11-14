# Capturas del prototipo

Fecha y hora de las capturas: sin registro real (la hora 21:56 que figuraba era planeada); están en el repo desde el commit `f614691` (14 nov 2026). Según el plan, se toman con Edge sin interfaz sobre la web compilada (`npm run build`), servida con `npx vite preview --host 0.0.0.0 --port 4173`, como indica `docs/prueba-telefono.md`.
- **En línea:** contra la IP local de la laptop.
- **Sin internet:** contra `127.0.0.1`, con un proxy inexistente.

Hay dos tamaños: escritorio (1366 × 768) y teléfono (390 × 844). Cada captura es una pantalla visible, no la página entera.

| N.º | Vista | Escritorio | Teléfono |
|---|---|---|---|
| 01 | Primera pantalla, con la observación preliminar de julio-agosto 2026 | `escritorio-01-primera-pantalla-observacion-2026.png` | `telefono-01-primera-pantalla-observacion-2026.png` |
| 02 | Mapa con las 5 parcelas (un nivel de zoom más lejos) y controles | `escritorio-02-mapa-5-parcelas.png` | `telefono-02-mapa-5-parcelas.png` |
| 03 | «Lo que ve el satélite» y «Clima de la zona» | `escritorio-03-satelite-y-clima.png` | `telefono-03-satelite-y-clima.png` |
| 04-08 | Tarjeta para el agricultor con el reproductor de audio, una por parcela: Jocotán, Camotán, Olopa, San Juan Ermita, Zacapa | `escritorio-04-tarjeta-jocotan.png` … `escritorio-08-tarjeta-zacapa.png` | `telefono-04-tarjeta-jocotan.png` … `telefono-08-tarjeta-zacapa.png` |
| 09 | Comparación de las 3 rotaciones (Jocotán) | `escritorio-09-rotaciones-jocotan.png` | `telefono-09-rotaciones-jocotan.png` |
| 10 | Pestaña Validación | `escritorio-10-validacion.png` | `telefono-10-validacion.png` |
| 11 | Detalle de la observación de julio-agosto 2026 | `escritorio-11-observacion-2026-detalle.png` | `telefono-11-observacion-2026-detalle.png` |
| 12 | Glosario y fuentes | `escritorio-12-glosario-y-fuentes.png` | `telefono-12-glosario-y-fuentes.png` |
| 13 | Sin internet: el mapa pasa solo a la capa guardada «Color real MODIS», con su aviso | `escritorio-13-sin-internet-mapa-capa-guardada.png` | `telefono-13-sin-internet-mapa-capa-guardada.png` |

**Detalles visuales que se buscaban al rehacerlas** (sin medición ni hora real registradas; revisarlos en las PNG):
- la tabla de la tarjeta cabe entera en teléfono, a 360 y 390 px;
- el eje de NDVI marca cada año una vez;
- las fechas de Fuentes y de Validación ya no se parten;
- los decimales de la tabla de 2026 son uniformes;
- los botones del teléfono tienen un área de toque de 40 px o más.
