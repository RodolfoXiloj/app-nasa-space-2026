# Revisión del video de 30 s (14 nov 2026)

## Decisiones

- Guion **A. De la órbita a la parcela** (elegido por el equipo). No se hicieron B (un día de una agricultora: habría que actuarla o dibujarla) ni C (tipografía sola: muestra poco del producto).
- Una sola parcela recorre todo el video: **Olopa**. Su 22 % abre el video y vuelve a verse en la pantalla real del teléfono; su audio dice «Soil: watch.»; sus futuros dan 9 y 33 de 33.
- Un solo objeto lleva la vista: el cuadro amarillo. Marca Olopa en el globo, se vuelve el píxel MODIS de verdad, se abre en el mundo del sitio y cierra como marca junto al nombre.
- El píxel contra la parcela (6.25 ha contra 0.35 ha) es un límite que el proyecto ya declara; en el video se presenta como lo que ve el satélite, no como algo que la herramienta resuelva.
- Olopa sale empatada en puntaje en el sitio: el video no nombra ganadora, solo cuenta futuros.

## Qué se midió y qué solo se miró

- `npx hyperframes check`: 0 errores. Queda 1 aviso a propósito: `timeline_track_too_dense` en `captions.html` (los 18 subtítulos van juntos en una pista, como pide la guía de subtítulos).
- Render: 29.8 s, 1920 × 1080, 30 fps, H.264 + AAC 48 kHz. Sonido medido, **no escuchado**: −15.9 LUFS integrados, pico real −1.3 dBTP.
- Se miraron cuadros de cada toma y de cada corte (`snapshot --review`) y un pliego de 16 cuadros del MP4 final. Nadie vio el video completo a velocidad normal todavía: falta que lo vea una persona del equipo, con sonido.
- Las cifras en pantalla se tomaron de los JSON del sitio y de capturas del build actual; Mario puede revisarlas contra `web/public/data/` igual que las del sitio.

## La toma más débil

El cierre «For the farmer / For the extension worker»: las dos pantallas quedan chicas y el panel no se lee a ese tamaño (solo se reconoce). Con más tiempo: mostrar las dos pantallas más grandes, una tras otra, o enseñar en las dos el mismo dato (el 22 %) resaltado.

## Pendiente o a decidir

- Que una persona lo vea y lo escuche entero (ritmo, voz, efectos).
- El nombre en la voz: Kokoro lo dice a la inglesa; la transcripción lo reconoce como «Milpa Resiliente», pero nadie de habla hispana lo ha oído.
- Qué enlace va en «Link to Project Demo» del formulario: el video o el PDF de las diapositivas (decisión del equipo).
