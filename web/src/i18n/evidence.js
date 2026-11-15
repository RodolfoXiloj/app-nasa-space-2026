// Step 6: product → decision and unified limits (figures from validation JSON, docs/umbrales.md, docs/es/estado.md).

export const OBS_LIMITES = {
  en: [
    "It is an observation of the past, not a prediction. The 2026 rain and soil moisture do not enter the scores or the confidence: the engine's climate is 2001-2025. The July-August 2026 rain is told in the farmer view and its short audio, as a preliminary figure. Fire detections from January to May 2026 do count in the fire fact.",
    'Preliminary: the Climate Hazards Center revises CHIRPS monthly and SMAP may be reprocessed. 2026 months come from the final product folder (not prelim/); each file date is recorded.',
    'SMAP: 3 cells with data (4 plots; Jocotán and San Juan Ermita share a cell); no recommended-quality data: Camotán. With 12 years, “lowest” is all we state—we do not report a percentile.',
    'Plots are example points chosen from space—not verified in the field.',
  ],
}

export const OBS_2026 = {
  en: {
    titulo: 'Preliminary observation: July–August 2026',
    resumen:
      'In July and August 2026, rainfall was 20% to 26% of normal (1991–2025 median) at all 5 plots, per CHIRPS v3—the lowest since 1991 in 5 of 5. SMAP shows the lowest July–August surface soil moisture (top 5 cm) in 12 years at 3 of 3 9 km cells with data.',
  },
  es: {
    titulo: 'Observación preliminar: julio-agosto 2026',
    resumen:
      'En julio y agosto de 2026 llovió entre el 20 % y el 26 % de lo normal (mediana 1991-2025) en las 5 parcelas, según CHIRPS v3; es lo menos desde 1991 en 5 de 5. SMAP registra la humedad del suelo de julio-agosto más baja de sus 12 años en 3 de 3 celdas de 9 km con dato.',
  },
}

export function productDecisions(loc) {
  const en = [
    {
      product: 'MODIS MOD13Q1 (250 m cell around the plot, 16-day)',
      decision: 'Bare-soil months, low-cover months, greenness cycles → soil score and “What the satellite sees”',
      source: 'motor/deteccion.py · web/public/data/*.json',
    },
    {
      product: 'VIIRS S-NPP active fire (FIRMS, 375 m)',
      decision: 'Fire years within 500 m (Jan–May) → Fire fact and soil score (burning lowers it)',
      source: 'motor/deteccion.py → detectar_quemas',
    },
    {
      product: 'CHIRPS v3 monthly (~5 km)',
      decision: 'Monthly rain, water deficit, drought-year ranking, 2018 validation',
      source: 'motor/clima.py · pipeline/validacion/',
    },
    {
      product: 'CHIRPS v3 daily “sat” (IMERG’s daily split arrives inside it; IMERG is not downloaded directly)',
      decision: 'Canícula dry spells (>15 days, <2 mm/day, 15 Jun–31 Aug)',
      source: 'motor/clima.py → SUPUESTOS',
    },
    {
      product: 'NASA POWER (~50 km cell)',
      decision: 'Temperature and ET0; daily rain split outside JJA; POWER vs CHIRPS bias',
      source: 'motor/clima.py · validacion.json',
    },
    {
      product: 'SMAP SPL3SMP_E (9 km, top 5 cm) or MERRA-2 GWETROOT fallback',
      decision: 'July–August soil moisture context; low-confidence flag when SMAP missing',
      source: 'motor/confianza.py · observacion_2026 in validacion.json',
    },
    {
      product: 'SRTM GL3 (90 m)',
      decision: 'Slope % of the 90 m cell → soil score multiplier above 15%',
      source: 'motor/puntaje.py',
    },
    {
      product: 'SoilGrids 250 m',
      decision: 'Soil properties for rotation templates (not re-scored live)',
      source: 'data/cache/soilgrids/',
    },
    {
      product: 'NASA GIBS tiles (MODIS, cached)',
      decision: 'Offline map layers when the network fails',
      source: 'web/public/capas/ · pipeline/capas.py',
    },
    {
      product: 'ZARC (cited, not computed)',
      decision: 'Planting window text on the farmer card → extensionist',
      source: 'motor/zarc.py · empty registry',
    },
  ]
  const es = [
    {
      product: 'MODIS MOD13Q1 (celda de 250 m alrededor de la parcela, cada 16 días)',
      decision: 'Meses de suelo desnudo, poca cobertura, ciclos de verdor → puntaje de suelo y panel del satélite',
      source: 'motor/deteccion.py · web/public/data/*.json',
    },
    {
      product: 'VIIRS S-NPP focos activos (FIRMS, 375 m)',
      decision: 'Años con quema a ≤500 m (ene–may) → hecho de quema y puntaje de suelo (la quema lo baja)',
      source: 'motor/deteccion.py → detectar_quemas',
    },
    {
      product: 'CHIRPS v3 mensual (~5 km)',
      decision: 'Lluvia mensual, déficit de agua, ranking de años secos, validación 2018',
      source: 'motor/clima.py · pipeline/validacion/',
    },
    {
      product: 'CHIRPS v3 diario “sat” (el reparto diario de IMERG viene dentro; IMERG no se descarga aparte)',
      decision: 'Rachas de canícula (>15 días, <2 mm/día, 15 jun–31 ago)',
      source: 'motor/clima.py → SUPUESTOS',
    },
    {
      product: 'NASA POWER (celda ~50 km)',
      decision: 'Temperatura y ET0; reparto diario fuera de JJA; sesgo POWER vs CHIRPS',
      source: 'motor/clima.py · validacion.json',
    },
    {
      product: 'SMAP SPL3SMP_E (9 km, primeros 5 cm) o respaldo MERRA-2 GWETROOT',
      decision: 'Contexto de humedad jul–ago; confianza baja cuando falta SMAP',
      source: 'motor/confianza.py · observacion_2026 en validacion.json',
    },
    {
      product: 'SRTM GL3 (90 m)',
      decision: 'Pendiente % de la celda de 90 m → multiplicador de suelo arriba de 15 %',
      source: 'motor/puntaje.py',
    },
    {
      product: 'SoilGrids 250 m',
      decision: 'Propiedades de suelo para plantillas de rotación (sin repuntaje en vivo)',
      source: 'data/cache/soilgrids/',
    },
    {
      product: 'Teselas NASA GIBS (MODIS, en caché)',
      decision: 'Capas del mapa sin red cuando falla internet',
      source: 'web/public/capas/ · pipeline/capas.py',
    },
    {
      product: 'ZARC (citado, no calculado)',
      decision: 'Texto de ventana de siembra en la tarjeta → extensionista',
      source: 'motor/zarc.py · registro vacío',
    },
  ]
  return loc === 'es' ? es : en
}

export function whereItFails(loc) {
  const en = [
    {
      limit: 'Plot points are examples chosen from space—not verified in the field',
      figure: '5 of 5 plots labeled “example”',
      source: 'validacion.json → observacion_2026.limites · parcela.nota in JSON',
    },
    {
      limit: 'MODIS pixel mixes milpa with neighbors',
      figure: '250 m × 250 m ≈ 6.25 ha (~9 manzanas, the local land unit)',
      source: 'docs/umbrales.md · motor/deteccion.py',
    },
    {
      limit: 'Low NDVI–deficit agreement at Olopa',
      figure: 'Spearman ρ = 0.07 (n from motor)',
      source: 'validacion.json → parcelas[].sequia_2018.spearman_deficit_vs_ndvi',
    },
    {
      limit: 'Camotán has no recommended-quality SMAP cell',
      figure: 'Shows MERRA-2 GWETROOT fallback, not measured SMAP',
      source: 'web/public/data/camotan.json meta.datos_de_ejemplo · validacion.json',
    },
    {
      limit: 'Two plots with low recommendation confidence',
      figure: 'Camotán (SMAP cell) and Zacapa (POWER vs CHIRPS in JJA)',
      source: 'docs/umbrales.md conteos · confianza in parcel JSON',
    },
    {
      limit: 'NASA POWER rain shares one ~50 km cell',
      figure: 'Jocotán, Camotán, San Juan Ermita, Zacapa in same cell; JJA bias −22.1% to +55.4% vs CHIRPS',
      source: 'docs/es/estado.md · validacion.json titular_power_chirps',
    },
    {
      limit: 'Jocotán and San Juan Ermita share one SMAP 9 km cell',
      figure: '3 cells with data for 4 plots; Camotán without quality flag',
      source: 'validacion.json → observacion_2026.limites',
    },
    {
      limit: 'VIIRS misses brief or cloudy burns',
      figure: '≤500 m radius · few daily passes',
      source: 'motor/deteccion.py → detectar_quemas note · docs/umbrales.md',
    },
    {
      limit: 'Zacapa point may be dry forest, not milpa',
      figure: 'NDVI filter does not separate milpa from deciduous dry forest',
      source: 'web/public/data/zacapa.json → parcela.nota',
    },
    {
      limit: '2026 rain is observation only—not in scores',
      figure: 'Engine uses 2001–2025; CHIRPS final may be revised monthly',
      source: 'validacion.json observacion_2026 · pipeline/validacion/validar.py',
    },
    {
      limit: 'SMAP “lowest in 12 years” is not a percentile',
      figure: 'With 12 years, only rank “lowest” is stated—no percentile rank',
      source: 'validacion.json → observacion_2026.limites (3rd bullet)',
    },
    {
      limit: 'A family farms far less than one pixel',
      figure: 'About 0.35 ha per family on average (FAO/WFP 2010) against 6.25 ha for a MODIS pixel, 9 km for SMAP and 90 m for SRTM',
      source: 'https://www.fao.org/4/ak344s/ak344s00.htm',
    },
    {
      limit: 'Two sensors are being retired',
      figure: 'Suomi NPP (FIRMS VIIRS) stopped delivering new data in early November 2026; Terra (MODIS) is being switched off in late 2026–early 2027. The record stays valid; updates would use VIIRS on NOAA-20 and NOAA-21',
      source: 'NASA Earthdata notices (earthdata.nasa.gov/data/alerts-outages)',
    },
    {
      limit: 'Dry-spell counts depend on how CHIRPS splits rain by day',
      figure: 'The engine uses “sat” (IMERG split). With “rnl” (ERA5), 14 plot-years have a dry spell of more than 15 days in 2001–2025 against 8 with “sat”; the two agree on 7 of the 15 either one flags, and the colour changes in 3 of 5 plots (Jocotán yellow→red, Olopa green→yellow, San Juan Ermita yellow→red)',
      source: 'docs/canicula-sensitivity.md · data.chc.ucsb.edu/products/CHIRPS/v3.0/daily/readme.txt',
    },
    {
      limit: 'The drought rule misses years with documented losses',
      figure: 'It does not flag 2016, 2019 or 2023 at any plot; 2–3 false alarms in 20 test years',
      source: 'validacion.json → parcelas[].sequia_2018.anios',
    },
    {
      limit: 'A fire detection is a pixel centre, not the fire’s exact place',
      figure: '~375 m pixel against a 500 m radius',
      source: 'earthdata.nasa.gov/data/tools/firms/faq',
    },
    {
      limit: 'Not an early-warning system',
      figure: 'It complements ZARC and the Agroclimatic Technical Boards; planting dates are quoted, not computed',
      source: 'motor/zarc.py',
    },
  ]
  const es = [
    {
      limit: 'Los puntos son ejemplos elegidos con satélite—no verificados en campo',
      figure: '5 de 5 parcelas rotuladas como ejemplo',
      source: 'validacion.json → observacion_2026.limites · parcela.nota en JSON',
    },
    {
      limit: 'El píxel MODIS mezcla la milpa con lo de al lado',
      figure: '250 m × 250 m ≈ 6,25 ha (~9 manzanas)',
      source: 'docs/umbrales.md · motor/deteccion.py',
    },
    {
      limit: 'Poca concordancia déficit–NDVI en Olopa',
      figure: 'Spearman ρ = 0,07 (n del motor)',
      source: 'validacion.json → parcelas[].sequia_2018.spearman_deficit_vs_ndvi',
    },
    {
      limit: 'Camotán no tiene celda SMAP con calidad recomendada',
      figure: 'Muestra respaldo MERRA-2 GWETROOT, no SMAP medido',
      source: 'web/public/data/camotan.json meta.datos_de_ejemplo · validacion.json',
    },
    {
      limit: 'Dos parcelas con confianza baja en la recomendación',
      figure: 'Camotán (celda SMAP) y Zacapa (POWER vs CHIRPS en JJA)',
      source: 'docs/umbrales.md conteos · confianza en JSON de parcela',
    },
    {
      limit: 'La lluvia de NASA POWER comparte una celda ~50 km',
      figure: 'Jocotán, Camotán, San Juan Ermita y Zacapa en la misma celda; sesgo JJA −22,1 % a +55,4 % vs CHIRPS',
      source: 'docs/es/estado.md · validacion.json titular_power_chirps',
    },
    {
      limit: 'Jocotán y San Juan Ermita comparten una celda SMAP de 9 km',
      figure: '3 celdas con dato para 4 parcelas; Camotán sin bandera de calidad',
      source: 'validacion.json → observacion_2026.limites',
    },
    {
      limit: 'VIIRS no ve quemas breves o bajo nubes',
      figure: 'Radio ≤500 m · pocas pasadas al día',
      source: 'motor/deteccion.py → nota detectar_quemas · docs/umbrales.md',
    },
    {
      limit: 'El punto de Zacapa puede ser bosque seco, no milpa',
      figure: 'El filtro NDVI no separa milpa de bosque caducifolio seco',
      source: 'web/public/data/zacapa.json → parcela.nota',
    },
    {
      limit: 'La lluvia de 2026 es solo observación—no entra en puntajes',
      figure: 'Motor usa 2001–2025; CHIRPS final puede revisarse cada mes',
      source: 'validacion.json observacion_2026 · pipeline/validacion/validar.py',
    },
    {
      limit: '«El más bajo en 12 años» en SMAP no es un percentil',
      figure: 'Con 12 años solo se dice rango «el más bajo»; sin percentil',
      source: 'validacion.json → observacion_2026.limites (3er viñeta)',
    },
    {
      limit: 'Una familia siembra mucho menos que un píxel',
      figure: 'Unas 0,35 ha por familia en promedio (FAO/PMA 2010) frente a 6,25 ha de un píxel MODIS, 9 km de SMAP y 90 m de SRTM',
      source: 'https://www.fao.org/4/ak344s/ak344s00.htm',
    },
    {
      limit: 'Dos sensores se están retirando',
      figure: 'Suomi NPP (VIIRS de FIRMS) dejó de dar datos nuevos a inicios de noviembre de 2026; Terra (MODIS) se apaga entre fines de 2026 e inicios de 2027. El registro sigue valiendo; las actualizaciones usarían VIIRS de NOAA-20 y NOAA-21',
      source: 'Avisos de NASA Earthdata (earthdata.nasa.gov/data/alerts-outages)',
    },
    {
      limit: 'Las rachas secas dependen de cómo CHIRPS reparte la lluvia por día',
      figure: 'El motor usa “sat” (reparto IMERG). Con “rnl” (ERA5), 14 parcela-años tienen una racha seca de más de 15 días en 2001–2025, contra 8 con “sat”; coinciden en 7 de los 15 que marca alguna de las dos, y el color cambia en 3 de 5 parcelas (Jocotán amarillo→rojo, Olopa verde→amarillo, San Juan Ermita amarillo→rojo)',
      source: 'docs/es/sensibilidad-canicula.md · data.chc.ucsb.edu/products/CHIRPS/v3.0/daily/readme.txt',
    },
    {
      limit: 'La regla de sequía no marca años con pérdidas documentadas',
      figure: 'No marca 2016, 2019 ni 2023 en ninguna parcela; 2–3 falsas alarmas en 20 años de prueba',
      source: 'validacion.json → parcelas[].sequia_2018.anios',
    },
    {
      limit: 'Un foco de quema es el centro de un píxel, no el lugar exacto del fuego',
      figure: 'Píxel de ~375 m frente a un radio de 500 m',
      source: 'earthdata.nasa.gov/data/tools/firms/faq',
    },
    {
      limit: 'No es un sistema de alerta temprana',
      figure: 'Complementa a ZARC y a las Mesas Técnicas Agroclimáticas; las fechas de siembra se citan, no se calculan',
      source: 'motor/zarc.py',
    },
  ]
  return loc === 'es' ? es : en
}