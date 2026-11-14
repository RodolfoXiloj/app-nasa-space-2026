# Validación (Mario, sábado 14 nov 2026, 13:00–18:00)

Actualización documental: 14 nov 2026, 09:00 (Guatemala, UTC−6).

Plan, sección 5. Un solo comando debe regenerar `web/public/data/validacion.json` y las cifras de `docs/validacion.md` desde `data/cache/`.

- `sequia_2018.py`: con datos hasta 2017, ¿el motor marca 2018 como riesgo alto? Anomalía de NDVI julio-septiembre 2018 contra 2001-2017 (hace falta el NDVI 2001-2025 de las 5 parcelas), anomalía de SMAP, puesto de 2018 entre 25 años, aciertos y falsas alarmas en 2014, 2015, 2018 y 2019, Spearman con n.
- `power_vs_chirps.py`: sesgo, error absoluto medio y Pearson por municipio, todos los meses y julio-agosto aparte. Escribe también `data/cache/chirps/{parcela}.json` con `dif_jul_ago_pct`: el motor ya lo lee para la confianza.

Regla fijada antes de ver el resultado: no se ajustan umbrales para que 2018 salga bien. Ver `docs/es/estado.md` (POWER pone 4 de las 5 parcelas en la misma celda).
