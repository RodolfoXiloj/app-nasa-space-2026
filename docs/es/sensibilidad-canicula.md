# Sensibilidad de la canícula al reparto diario de CHIRPS

Generado por `python -m pipeline.validacion.sensibilidad_canicula` el 2026-11-14T22:34:41Z (UTC). **No editar a mano:** se regenera desde `data/cache/`. Versión en inglés: [canicula-sensitivity.md](../canicula-sensitivity.md).

## Qué se probó

El hecho «canícula» del semáforo cuenta los años con una racha de más de 15 días con menos de 2 mm entre el 15 de junio y el 31 de agosto, con CHIRPS v3 diario «sat» (cada péntada de CHIRPS repartida por días con NASA IMERG). El Climate Hazards Center advierte que las rachas secas pueden cambiar mucho con «rnl» (la misma péntada repartida con ERA5) y pide probar con las dos (https://data.chc.ucsb.edu/products/CHIRPS/v3.0/daily/readme.txt). Aquí se arma la serie del motor dos veces por parcela, cambiando solo la caché diaria, con las mismas funciones y los mismos cortes.

## Resumen

Con el reparto de ERA5 («rnl») los años con racha seca de más de 15 días son Jocotán 3, Camotán 1, Olopa 1, San Juan Ermita 3, Zacapa 6 (de 25), frente a Jocotán 2, Camotán 2, Olopa 0, San Juan Ermita 1, Zacapa 3 con el reparto de IMERG («sat») que usa el motor: 14 años-parcela contra 8. Las dos versiones coinciden en 7 de los 15 años-parcela que marca alguna (1 solo «sat», 7 solo «rnl») y el color del semáforo cambia en 3 de 5 parcelas (Jocotán amarillo→rojo, Olopa verde→amarillo, San Juan Ermita amarillo→rojo).

## Por parcela (2001-2025, 25 años)

| Parcela | «sat»: años (estado) | «rnl»: años (estado) | Coinciden | Solo «sat» | Solo «rnl» | Racha mediana sat / rnl (días) | Misma racha (años) | Diferencia media (días) |
|---|---|---|---|---|---|---|---|---|
| Jocotán | 2 (amarillo) | 3 (rojo) | 2015, 2018 | — | 2021 | 7 / 7 | 4 de 25 | 2.5 |
| Camotán | 2 (amarillo) | 1 (amarillo) | 2015 | 2018 | — | 7 / 6 | 2 de 25 | 2.0 |
| Olopa | 0 (verde) | 1 (amarillo) | — | — | 2021 | 7 / 5 | 8 de 25 | 1.8 |
| San Juan Ermita | 1 (amarillo) | 3 (rojo) | 2018 | — | 2015, 2021 | 8 / 8 | 4 de 25 | 2.3 |
| Zacapa | 3 (rojo) | 6 (rojo) | 2015, 2018, 2025 | — | 2001, 2004, 2013 | 9 / 10 | 6 de 25 | 2.2 |

Estado con los cortes de `data/umbrales_semaforo.yaml`: verde 0 años, amarillo 1 o 2, rojo 3 o más.

## Racha más larga de cada año (días, «sat» / «rnl»)

En negrita, más de 15 días.

| Año | Jocotán | Camotán | Olopa | San Juan Ermita | Zacapa |
|---|---|---|---|---|---|
| 2001 | 10 / 13 | 7 / 9 | 10 / 11 | 11 / 14 | 11 / **17** |
| 2002 | 11 / 10 | 11 / 10 | 11 / 10 | 11 / 10 | 11 / 10 |
| 2003 | 8 / 6 | 8 / 6 | 8 / 3 | 8 / 6 | 15 / 12 |
| 2004 | 8 / 8 | 8 / 6 | 5 / 5 | 8 / 8 | 14 / **18** |
| 2005 | 7 / 13 | 5 / 11 | 8 / 9 | 7 / 13 | 12 / 13 |
| 2006 | 8 / 8 | 5 / 6 | 7 / 5 | 8 / 8 | 8 / 8 |
| 2007 | 7 / 5 | 7 / 5 | 6 / 5 | 6 / 5 | 9 / 5 |
| 2008 | 4 / 5 | 4 / 5 | 4 / 2 | 4 / 5 | 5 / 5 |
| 2009 | 9 / 9 | 9 / 10 | 5 / 8 | 9 / 9 | 6 / 10 |
| 2010 | 4 / 5 | 3 / 5 | 2 / 2 | 3 / 5 | 8 / 5 |
| 2011 | 4 / 4 | 4 / 2 | 3 / 2 | 3 / 4 | 6 / 6 |
| 2012 | 7 / 6 | 9 / 6 | 7 / 7 | 7 / 7 | 10 / 9 |
| 2013 | 7 / 5 | 8 / 5 | 7 / 5 | 7 / 5 | 8 / **16** |
| 2014 | 7 / 9 | 7 / 7 | 9 / 8 | 9 / 10 | 9 / 12 |
| 2015 | **19** / **20** | **19** / **20** | 10 / 11 | 14 / **20** | **23** / **20** |
| 2016 | 8 / 7 | 8 / 7 | 5 / 5 | 8 / 9 | 10 / 11 |
| 2017 | 8 / 5 | 8 / 8 | 5 / 5 | 10 / 6 | 10 / 11 |
| 2018 | **17** / **27** | **17** / 13 | 11 / 15 | **28** / **27** | **21** / **21** |
| 2019 | 6 / 8 | 6 / 7 | 8 / 5 | 7 / 8 | 9 / 8 |
| 2020 | 4 / 6 | 4 / 5 | 4 / 4 | 4 / 6 | 7 / 7 |
| 2021 | 11 / **17** | 5 / 7 | 8 / **16** | 11 / **17** | 8 / 13 |
| 2022 | 6 / 4 | 6 / 3 | 12 / 5 | 13 / 5 | 7 / 4 |
| 2023 | 7 / 5 | 6 / 5 | 5 / 5 | 7 / 8 | 7 / 9 |
| 2024 | 8 / 2 | 8 / 2 | 4 / 1 | 5 / 2 | 9 / 9 |
| 2025 | 6 / 13 | 11 / 14 | 9 / 9 | 9 / 13 | **18** / **20** |

## Comprobaciones

- Con «sat» salen los conteos que publica el sitio (Jocotán 2, Camotán 2, Olopa 0, San Juan Ermita 1, Zacapa 3, de 25 años) y la misma racha año por año que `web/public/data/`; si no, el script no escribe nada.
- Las dos versiones reparten la misma péntada: la lluvia de cada mes de junio a agosto difiere como mucho 0.05 mm entre «sat» y «rnl» (redondeo de los valores diarios). Confirma que se leyó el mismo píxel y el mismo periodo.
- Años con alguna racha de 14 a 17 días (a uno o dos días del corte): Jocotán 2018, 2021; Camotán 2018, 2025; Olopa 2018, 2021; San Juan Ermita 2001, 2015, 2021; Zacapa 2001, 2003, 2004, 2013.

## Límites

- «sat» y «rnl» no son independientes: las dos reparten el mismo total de cada péntada de CHIRPS y solo difieren en cómo lo reparten entre los días (readme del CHC). Coincidir no valida la racha seca; solo dice que no depende del reparto elegido.
- Ninguna de las dos es una medición diaria en tierra. ERA5 (~0.25°) e IMERG (0.1°) se interpolan a la malla de 0.05°: el reparto diario no tiene detalle de 5 km.
- Cuando ERA5 o IMERG marcan cero en toda la péntada y CHIRPS no, el CHC reparte el total por igual entre los días; eso puede crear días húmedos artificiales que cortan una racha seca.
- Los días van en hora UTC, no en hora de Guatemala. El corte (> 15 días con < 2 mm, 15 jun-31 ago) es el del motor y no se tocó para esta prueba.
- Solo cambia la lluvia de junio a agosto; el resto del año y la temperatura son los mismos en las dos series. El resultado no entra en ningún puntaje, ni en la confianza ni en el audio: el semáforo publicado sigue usando «sat».
- Las parcelas son puntos de ejemplo elegidos con satélite, no verificados en campo.

## Cómo reproducirlo

```
# 1. Bajar CHIRPS v3 diario 'rnl' de junio-agosto 2001-2025 (lectura por rangos; los extractos por
#    día quedan en data/raw_big/chirps_diario_rnl/, fuera del repo)
MILPA_ONLINE=1 python -m pipeline.clientes.chirps --diario --version rnl
# 2. Comprobar ('sat' debe dar los conteos publicados) y escribir el JSON y los dos documentos, sin red
python -m pipeline.validacion.sensibilidad_canicula --verificar
python -m pipeline.validacion.sensibilidad_canicula
```

Fuentes: «sat» https://data.chc.ucsb.edu/products/CHIRPS/v3.0/daily/final/sat/AAAA/chirps-v3.0.sat.AAAA.MM.DD.tif (bajado 2026-11-13T18:54:19Z); «rnl» https://data.chc.ucsb.edu/products/CHIRPS/v3.0/daily/final/rnl/AAAA/chirps-v3.0.rnl.AAAA.MM.DD.tif (bajado 2026-11-14T22:33:34Z).

## Frase para el formulario (inglés)

> Dry-spell counts depend on this split, so we compared them with the ERA5-based “rnl” version: with “rnl” the 5 plots have 14 years with a dry spell of more than 15 days in 2001-2025 against 8 with “sat” (plot-years), the two agree on 7 of the 15 plot-years either one flags, and the traffic-light colour changes in 3 of 5 plots (Jocotán yellow→red, Olopa green→yellow, San Juan Ermita yellow→red).
