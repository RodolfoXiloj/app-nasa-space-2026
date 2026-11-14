"""Inglés de los textos que la web muestra. El español no cambia y ninguna cifra cambia.

Convención para la web: cada objeto con texto visible lleva dos subobjetos con los mismos campos,
`es` y `en`. La web lee `obj[idioma]?.campo` y, si falta, el campo de siempre (`obj.campo`, en español).

De dónde sale cada inglés:
- Textos de las rotaciones (por qué, beneficios, vacíos, riesgos): plantillas paralelas a las de
  motor/redaccion.py, con el mismo contexto y las mismas cifras.
- Textos de data/*.yaml (rotaciones, glosario, fuentes, parcelas, cultivos, ZARC): su bloque `en`.
- Textos fijos del motor: diccionario TEXTOS (español exacto -> inglés) y PATRONES para los que llevan
  una cifra. Si falta una traducción, `t()` devuelve None y la prueba tests/test_ingles.py lo marca.
- validacion.json (lo escribe pipeline/validacion/validar.py, fuera del carril A): `validacion()` lo
  completa con plantillas que toman las cifras del propio texto; motor/exportar.py lo llama al exportar.
Sin «alert», «alerta» ni «forecast» en los textos propios.
"""
from __future__ import annotations

import re

MESES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
         "November", "December"]

AVISO = ("Milpa Resiliente supports, and does not replace, the extension worker or the farmer. The figures come from "
         "satellites and models with limits that are explained in each option. Check it with your extension worker.")

TEXTOS = {
    # motor/redaccion.py y motor/recomendar.py
    "Salida del motor con datos cacheados en data/cache/": "Engine output with cached data in data/cache/",
    "SMAP: se muestra el respaldo GWETROOT de POWER (modelo MERRA-2, no SMAP)":
        "SMAP: the POWER GWETROOT fallback is shown (MERRA-2 model, not SMAP)",
    "CHIRPS: aún sin comparar con POWER; la confianza no pasa de media":
        "CHIRPS: not yet compared with POWER; confidence stays at medium at most",
    "Lluvia diaria: junio-agosto con CHIRPS v3 diario (péntadas repartidas con NASA IMERG); "
    "resto del año, totales mensuales de CHIRPS repartidos con los días de POWER":
        "Daily rain: June-August from CHIRPS v3 daily (pentads split with NASA IMERG); rest of the year, monthly "
        "CHIRPS totals split over the POWER days",
    "Lluvia diaria: totales mensuales de CHIRPS repartidos con los días de POWER (CHIRPS diario pendiente)":
        "Daily rain: monthly CHIRPS totals split over the POWER days (daily CHIRPS pending)",
    "Suelo: sin datos de SoilGrids": "Soil: no SoilGrids data",
    "ZARC: sin cita para este municipio; se remite al extensionista":
        "ZARC: no citation for this municipality; refer to the extension worker",
    "Rotaciones: plantillas iniciales sin revisión agronómica": "Rotations: initial templates without agronomic review",
    "FIRMS 2026: sin datos del año en curso; se usan años completos 2012-2025":
        "FIRMS 2026: no data for the current year; full years 2012-2025 are used",
    "Coordenada provisional: falta validar que el píxel sea agrícola":
        "Provisional coordinate: still to check that the pixel is farmland",
    # suelo (SoilGrids)
    "Consulta por REST": "Queried via REST",
    "Sin datos de suelo: la API de SoilGrids no respondió. Vacío de información.":
        "No soil data: the SoilGrids API did not respond. Information gap.",
    # quemas (motor/deteccion.py)
    "Quema cercana = foco VIIRS de confianza nominal o alta a 500 m o menos, entre enero y mayo. Sin detección no "
    "significa que no hubo quema: el satélite pasa pocas veces al día y no ve quemas breves o bajo nubes.":
        "Nearby burning = a VIIRS fire detection of nominal or high confidence within 500 m, between January and May. "
        "No detection does not mean there was no burning: the satellite passes a few times a day and does not see "
        "brief fires or fires under clouds.",
    # clima (motor/clima.py)
    "NASA POWER": "NASA POWER",
    "CHIRPS v3 mensual repartido por días con NASA POWER": "CHIRPS v3 monthly, split by day with NASA POWER",
    "CHIRPS v3 mensual repartido por días con NASA POWER; junio-agosto con CHIRPS v3 diario (reparto con NASA IMERG)":
        "CHIRPS v3 monthly, split by day with NASA POWER; June-August from CHIRPS v3 daily (split with NASA IMERG)",
    "lluvia: CHIRPS v3 (0.05°, ~5 km), diaria en junio-agosto (reparto con NASA IMERG) y mensual repartida con los "
    "días de POWER el resto del año; temperatura: POWER (0.5° x 0.625°, ~50 km). Es la zona cercana, no la parcela":
        "rain: CHIRPS v3 (0.05°, ~5 km), daily in June-August (split with NASA IMERG) and monthly split over the POWER "
        "days for the rest of the year; temperature: POWER (0.5° x 0.625°, ~50 km). It is the nearby area, not the plot",
    "lluvia: CHIRPS v3 (0.05°, ~5 km) repartida por días con POWER; temperatura: POWER (0.5° x 0.625°, ~50 km). "
    "Es la zona cercana, no la parcela":
        "rain: CHIRPS v3 (0.05°, ~5 km) split by day with POWER; temperature: POWER (0.5° x 0.625°, ~50 km). "
        "It is the nearby area, not the plot",
    "0.5° x 0.625° (~50 km): es la zona, no la parcela": "0.5° x 0.625° (~50 km): it is the area, not the plot",
    "15 de junio a 31 de agosto": "15 June to 31 August",
    # SMAP (motor/recomendar.py)
    "SMAP SPL3SMP_E por AppEEARS.": "SMAP SPL3SMP_E via AppEEARS.",
    "modelo MERRA-2 vía NASA POWER, no es SMAP": "MERRA-2 model via NASA POWER, not SMAP",
    "fracción 0-1": "fraction 0-1",
    # calendario
    "El satélite ve poco verde: siembra reciente o cultivo ralo.": "The satellite sees little green: recent sowing or a sparse crop.",
    "Canícula: vigile la racha seca.": "Canícula: watch the dry spell.",
    "Quema cercana detectada por VIIRS en este mes.": "Nearby burning detected by VIIRS in this month.",
    "Suelo desnudo: expuesto al sol y a la erosión.": "Bare soil: exposed to the sun and to erosion.",
    "Poca cobertura: el satélite ve el suelo casi descubierto.": "Little cover: the satellite sees the soil almost uncovered.",
    # evidencia
    "Meses de suelo desnudo detectados": "Months of bare soil detected",
    "Meses de suelo desnudo esperados con esta práctica": "Months of bare soil expected with this practice",
    "Meses con poca cobertura": "Months with little cover",
    "Meses con poca cobertura esperados con esta práctica": "Months with little cover expected with this practice",
    "Ciclos de verdor por año (mediana)": "Greenness cycles per year (median)",
    "Compuestos NDVI válidos": "Valid NDVI composites",
    "Déficit de agua mediano del ciclo": "Median water deficit of the cycle",
    "Pérdida de cosecha esperada por falta de agua (mediana, Ky x déficit)":
        "Expected harvest loss from lack of water (median, Ky x deficit)",
    "Pendiente del terreno": "Terrain slope",
    "Humedad del suelo julio-agosto (SMAP, mediana)": "July-August soil moisture (SMAP, median)",
    "Diferencia de lluvia julio-agosto: POWER frente a CHIRPS": "July-August rain difference: POWER against CHIRPS",
    "Arcilla del suelo (0-5 cm)": "Soil clay (0-5 cm)",
    "Humedad de raíz julio-agosto (modelo, no SMAP)": "July-August root-zone moisture (model, not SMAP)",
    "meses": "months", "ciclos": "cycles", "%": "%", "m3/m3": "m3/m3",
    "MODIS MOD13Q1 (NDVI) vía ORNL DAAC": "MODIS MOD13Q1 (NDVI) via ORNL DAAC",
    "FIRMS VIIRS S-NPP": "FIRMS VIIRS S-NPP",
    "MODIS MOD13Q1 pixel_reliability": "MODIS MOD13Q1 pixel_reliability",
    "CHIRPS (lluvia) + NASA POWER (temperatura) + ET0 Hargreaves y Kc (FAO-56)":
        "CHIRPS (rain) + NASA POWER (temperature) + ET0 Hargreaves and Kc (FAO-56)",
    "NASA POWER + ET0 Hargreaves y Kc (FAO-56)": "NASA POWER + ET0 Hargreaves and Kc (FAO-56)",
    "CHIRPS + NASA POWER + FAO-33": "CHIRPS + NASA POWER + FAO-33",
    "NASA POWER + FAO-33": "NASA POWER + FAO-33",
    "NASA POWER diario reescalado con CHIRPS mensual": "NASA POWER daily rescaled with monthly CHIRPS",
    "NASA POWER diario": "NASA POWER daily",
    "SRTM 90 m": "SRTM 90 m",
    "SMAP L3 mejorado (SPL3SMP_E) vía AppEEARS": "SMAP Enhanced L3 (SPL3SMP_E) via AppEEARS",
    "NASA POWER y CHIRPS v3": "NASA POWER and CHIRPS v3",
    "SoilGrids 2.0 (ISRIC)": "SoilGrids 2.0 (ISRIC)",
    "NASA POWER GWETROOT (MERRA-2)": "NASA POWER GWETROOT (MERRA-2)",
    "250 m": "250 m", "375 m": "375 m", "90 m": "90 m", "9 km": "9 km", "~50 km": "~50 km",
    "~5 km (lluvia), ~50 km (temperatura)": "~5 km (rain), ~50 km (temperature)",
    "~50 km y ~5 km": "~50 km and ~5 km",
    # confianza
    "Calidad del píxel MODIS": "MODIS pixel quality",
    "Lluvia POWER contra CHIRPS en julio-agosto": "POWER rain against CHIRPS in July-August",
    "Humedad del suelo SMAP": "SMAP soil moisture",
    "Prueba de la sequía de 2018": "2018 drought test",
    # ZARC (motor/zarc.py)
    "La fecha de ZARC no cambia con el escenario; consulte la versión vigente.":
        "The ZARC date does not change with the scenario; check the current version.",
    "Fecha de siembra: consúltela en ZARC (FAO–MAGA) con su extensionista.":
        "Planting date: check it in ZARC (FAO–MAGA) with your extension worker.",
    # validacion.json (pipeline/validacion/validar.py)
    "Ninguno.": "None.",
    "La confianza de las recomendaciones de agua baja a «baja».":
        "Confidence of the water recommendations drops to «low».",
    "CHIRPS no es medición en tierra: mezcla satélite y estaciones. Las estaciones de INSIVUMEH quedan como vacío.":
        "CHIRPS is not a ground measurement: it blends satellite and stations. INSIVUMEH stations remain a gap.",
    "POWER: celda de 0.5° x 0.625° (~50 km). CHIRPS: 0.05° (~5 km).":
        "POWER: 0.5° x 0.625° cell (~50 km). CHIRPS: 0.05° (~5 km).",
    "La lluvia del motor es el total mensual de CHIRPS repartido con los días de POWER.":
        "The engine's rain is the monthly CHIRPS total split over the POWER days.",
    "Riesgo alto = déficit del año mayor que el percentil 75 de los años anteriores (desde 2001).":
        "High risk = a year's deficit above percentile 75 of the previous years (since 2001).",
    "Señal de NDVI = anomalía de julio-septiembre de -1 desviación estándar o menos.":
        "NDVI signal = a July-September anomaly of -1 standard deviation or less.",
    "FAO GIEWS Update – Central America, 27 de agosto de 2018": "FAO GIEWS Update – Central America, 27 August 2018",
    "Estimación del MAGA del 13 ago 2018 citada por FAO GIEWS; no hay porcentaje de pérdida solo para Guatemala.":
        "MAGA estimate of 13 Aug 2018 cited by FAO GIEWS; there is no loss percentage for Guatemala alone.",
    "Las parcelas son puntos de ejemplo elegidos con satélite, no verificados en campo.":
        "The plots are example points chosen by satellite, not verified in the field.",
    "monthly/latam: producto final (el preliminar está en la carpeta prelim/)":
        "monthly/latam: final product (the preliminary one is in the prelim/ folder)",
    "coincide": "agrees",
    "independiente: encuesta de hogares": "independent: household survey",
    "independiente: conteo oficial de familias afectadas": "independent: official count of affected families",
    "FEWS NET, Guatemala: actualización de la perspectiva de seguridad alimentaria, agosto 2026":
        "FEWS NET, Guatemala: food security outlook update, August 2026",
    "Prensa Libre, 1 sep 2026, sobre una evaluación de Oxfam, Acción contra el Hambre y organizaciones socias":
        "Prensa Libre, 1 Sep 2026, on an assessment by Oxfam, Action Against Hunger and partner organizations",
    "Canal Antigua, 25 sep 2026": "Canal Antigua, 25 Sep 2026",
    "Coincide con CHIRPS, pero no es una confirmación independiente: el informe no dice de qué producto sale la cifra "
    "y su mapa de lluvia (figura 1) es del Climate Hazards Center, el mismo grupo que produce CHIRPS. Se refiere solo "
    "a agosto y a todo el Corredor Seco.":
        "It agrees with CHIRPS, but it is not an independent confirmation: the report does not say which product the "
        "figure comes from, and its rain map (figure 1) is from the Climate Hazards Center, the same group that produces "
        "CHIRPS. It refers only to August and to the whole Dry Corridor.",
    "Ámbito según la nota: el corredor seco de Guatemala, sin lista de departamentos ni municipios. La nota no aclara "
    "si son hogares evaluados o una estimación; el estudio completo abarca Guatemala, Honduras y El Salvador. No se "
    "atribuye a Chiquimula ni a Zacapa.":
        "Scope according to the article: Guatemala's dry corridor, with no list of departments or municipalities. The "
        "article does not say whether these are assessed households or an estimate; the full study covers Guatemala, "
        "Honduras and El Salvador. It is not attributed to Chiquimula or Zacapa.",
    "Ámbito según la nota: «15 municipios de Chiquimula y Jutiapa, bajo alerta roja por la sequía». No da cifras de Zacapa.":
        "Scope according to the article, quoted in Spanish: «15 municipios de Chiquimula y Jutiapa, bajo alerta roja por "
        "la sequía» (municipalities of Chiquimula and Jutiapa at the top drought level). It gives no figures for Zacapa.",
    # citas en español de los reportes de 2026 (traducción propia, rotulada)
    "Entre el 01 y el 31 de agosto, el Corredor Seco recibió entre el 5 y el 25 por ciento de las lluvias en comparación "
    "con los valores normales":
        "Between 01 and 31 August, the Dry Corridor received between 5 and 25 percent of normal rainfall (our translation)",
    "En el corredor seco guatemalteco, 36 mil 431 hogares reportan serios daños en sus cosechas de maíz, según una "
    "evaluación de Oxfam, organizaciones socias y Acción contra el Hambre.":
        "In Guatemala's dry corridor, 36 thousand 431 households report serious damage to their maize harvests, according "
        "to an assessment by Oxfam, partner organizations and Action Against Hunger (our translation).",
    "se contabilizan 113 mil 825 familias afectadas": "113 thousand 825 affected families are counted (our translation)",
}

# (patrón sobre el español, plantilla en inglés con los mismos grupos)
PATRONES = [
    (r"Años con quema a (\d+) m o menos \(enero-mayo\)", "Years with burning within {0} m (January-May)"),
    (r"Años con canícula de más de (\d+) días secos", "Years with a canícula of more than {0} dry days"),
    (r"de (\d+) años", "of {0} years"),
    (r"Observación preliminar: julio-agosto (\d{4})", "Preliminary observation: July-August {0}"),
    (r"Es una observación del pasado, no un pronóstico\. El motor usa (\d{4}-\d{4}): (\d{4}) no entra en los puntajes, "
     r"la confianza ni el audio\.",
     "It is an observation of the past, not a prediction. The engine uses {0}: {1} does not enter the scores, the "
     "confidence or the audio."),
    (r"Preliminar: el Climate Hazards Center recalcula CHIRPS cada mes y SMAP puede reprocesarse\. Los meses de (\d{4}) "
     r"vienen de la carpeta del producto final \(no de prelim/\); se guarda la fecha de cada archivo\.",
     "Preliminary: the Climate Hazards Center recomputes CHIRPS every month and SMAP may be reprocessed. The {0} months "
     "come from the final-product folder (not from prelim/); the date of each file is kept."),
    (r"En julio-agosto, NASA POWER se desvía (\S+) % de CHIRPS en (.+?) \(error medio de (\S+) mm/mes, r = (\S+), "
     r"n = (\d+) meses, (\d{4}-\d{4})\)\.",
     "In July-August, NASA POWER differs {0} % from CHIRPS in {1} (mean error {2} mm/month, r = {3}, n = {4} months, {5})."),
    (r"El motor, con lo que se sabía hasta (\d{4}), marca (\d{4}) como riesgo alto en (\d+) de (\d+) parcelas; alguna "
     r"señal \(motor, NDVI o SMAP\) lo muestra en (\d+)\.",
     "The engine, with what was known up to {0}, flags {1} as high risk in {2} of {3} plots; some signal (engine, NDVI or "
     "SMAP) shows it in {4}."),
]


def _resumen_2026(es: str) -> str | None:
    m = re.fullmatch(r"En julio y agosto de (\d{4}) llovió entre el (\S+) % y el (\S+) % de lo normal \(mediana "
                     r"(\d{4}-\d{4})\) en las (\d+) parcelas, según CHIRPS v3; es lo menos desde (\d{4}) en (\d+) de "
                     r"(\d+)\.(?: SMAP registra la humedad del suelo de julio-agosto más baja de sus (\d+) años en (\d+) "
                     r"de (\d+) celdas de 9 km con dato\.)?", es)
    if not m:
        return None
    g = m.groups()
    out = (f"In July and August {g[0]} it rained between {g[1]} % and {g[2]} % of normal (median {g[3]}) at the {g[4]} "
           f"plots, according to CHIRPS v3; it is the lowest since {g[5]} at {g[6]} of {g[7]}.")
    if g[8]:
        out += (f" SMAP records the lowest July-August soil moisture of its {g[8]} years in {g[9]} of {g[10]} 9 km "
                f"cells with data.")
    return out


def _limite_smap(es: str) -> str | None:
    m = re.fullmatch(r"SMAP: (\d+) celdas de 9 km con dato \((\d+) parcelas((?:; [^;()]+ comparten celda)*)\)"
                     r"(?:; sin dato de calidad recomendada: ([^.]+))?\. Con (\d+) años, «el más bajo» es todo lo que "
                     r"se puede decir; no se da percentil\.", es)
    if not m:
        return None
    celdas, parcelas, comparten, sin, anios = m.groups()
    pares = "".join(f"; {p.replace(' y ', ' and ')} share a cell"
                    for p in re.findall(r"; ([^;()]+) comparten celda", comparten or ""))
    return (f"SMAP: {celdas} 9 km cells with data ({parcelas} plots{pares})"
            + (f"; no recommended-quality data: {sin}" if sin else "")
            + f". With {anios} years, «the lowest» is all that can be said; no percentile is given.")


def t(es: str | None) -> str | None:
    """Inglés de un texto fijo del motor o de la validación; None si no hay traducción."""
    if es is None:
        return None
    if es in TEXTOS:
        return TEXTOS[es]
    for patron, plantilla in PATRONES:
        m = re.fullmatch(patron, es)
        if m:
            return plantilla.format(*m.groups())
    return _resumen_2026(es) or _limite_smap(es)


def bilingue(obj: dict | None, campos: dict[str, object]) -> None:
    """Pone obj["es"] y obj["en"] con los campos dados: {campo: inglés}. El español es el del propio objeto."""
    if not obj:
        return
    obj.setdefault("es", {}).update({c: obj.get(c) for c in campos})
    obj.setdefault("en", {}).update(campos)


def _t_campos(obj: dict | None, campos: tuple[str, ...]) -> None:
    if obj:
        bilingue(obj, {c: (t(obj[c]) if isinstance(obj.get(c), str) else
                           [t(x) for x in obj[c]] if isinstance(obj.get(c), list) else None)
                       for c in campos if c in obj})


# ---------------------------------------------------------------- textos de las rotaciones
def lista_meses(ms: list[int]) -> str:
    nombres = [MESES[m - 1] for m in sorted(ms)]
    if not nombres:
        return "none"
    if len(nombres) == 1:
        return nombres[0]
    return ", ".join(nombres[:-1]) + " and " + nombres[-1]


def _plural(n: float, uno: str, varios: str) -> str:
    return uno if n == 1 else varios


def por_que(tipo: str, ctx: dict) -> str:
    """Igual que motor.redaccion.por_que, en inglés y con las mismas cifras."""
    det, ev, act = ctx["det"], ctx["ev"], ctx["ev_actual"]
    q = det["quemas"]
    if tipo == "actual":
        n = ev["n_desnudos"]
        if n:
            vista = (f"The MODIS satellite ({det['periodo']}) sees bare soil in {n} {_plural(n, 'month', 'months')} of "
                     f"the year: {lista_meses(ev['meses_desnudos'])}.")
        elif ev.get("n_poca"):
            vista = (f"The MODIS satellite ({det['periodo']}) does not see fully bare soil, but it sees little cover in "
                     f"{ev['n_poca']} {_plural(ev['n_poca'], 'month', 'months')}: {lista_meses(ev['meses_poca'])}.")
        else:
            vista = (f"The MODIS satellite ({det['periodo']}) sees no month with bare soil: median greenness does not "
                     f"drop below {det['umbral_desnudo_ndvi']}.")
        ciclos = det["ciclos"]["mediana"]
        return (f"This is what you do today. {vista} It counts {ciclos} {_plural(ciclos, 'cycle', 'cycles')} of greenness "
                f"per year. There was burning nearby in {q['anios_con_quema']} of {q['anios_observados']} years observed "
                f"with VIIRS.")
    if tipo == "leguminosa_cobertura":
        if ev["n_desnudos"] == act["n_desnudos"] and ev.get("n_poca", 0) < act.get("n_poca", 0):
            return (f"It protects the soil: with cover and standing stubble, months with little cover would drop from "
                    f"{act['n_poca']} to {ev['n_poca']}, without burning. The legume adds nitrogen and organic matter.")
        if ev["n_desnudos"] < act["n_desnudos"]:
            inicio = (f"It protects the soil: with cover and standing stubble, months of bare soil would drop from "
                      f"{act['n_desnudos']} to {ev['n_desnudos']}, without burning.")
        else:
            inicio = ("The satellite does not see more bare months than this practice can cover; its advantage here is "
                      "to stop burning and give organic matter back to the soil.")
        return inicio + " The legume adds nitrogen and organic matter."
    pa, pc = ev["deficit"]["perdida_mediana_pct"], act["deficit"]["perdida_mediana_pct"]
    seco = ctx.get("escenario_seco")
    cola = ""
    if seco:
        cola = (f" In the driest scenario (rain {seco['lluvia_pct']} % and +{seco['temp_c']} °C) the water deficit "
                f"would be {seco['alt']} % against {seco['act']} %.")
    if pa < pc:
        return (f"It copes better with water shortage. With the {ctx['clima']['periodo']} climate, the expected harvest "
                f"loss from lack of water would be {pa} % in a typical year, against {pc} % for what you do today." + cola)
    return (f"It is the most drought-tolerant option in the library, but with the {ctx['clima']['periodo']} climate the "
            f"expected loss from lack of water is similar to today's ({pa} % against {pc} %)." + cola)


def beneficios(rot: dict, ctx: dict) -> list[str]:
    ev, act = ctx["ev"], ctx["ev_actual"]
    out = list((rot.get("en") or {}).get("beneficios") or [])
    if not ctx["es_actual"]:
        if ev["n_desnudos"] < act["n_desnudos"]:
            out.append(f"Fewer months of bare soil: {ev['n_desnudos']} instead of {act['n_desnudos']}.")
        if ev["puntajes"]["agua"] > act["puntajes"]["agua"]:
            out.append(f"Better water score: {ev['puntajes']['agua']} against {act['puntajes']['agua']}.")
    return out or ["No clear benefit over what you do today with the available data."]


def vacios(rot: dict, ctx: dict) -> list[str]:
    out = list((rot.get("en") or {}).get("vacios") or [])
    if ctx.get("con_chirps"):
        out.append("Rain comes from CHIRPS, in cells of ~5 km, and temperature from NASA POWER, in cells of ~50 km: "
                   "they describe the nearby area, not your exact plot.")
    else:
        out.append("Rain comes from NASA POWER, a cell of ~50 km: it describes the area, not your plot.")
    if ctx.get("smap_sin_calidad"):
        out.append("SMAP has no good-quality measurements for this area; soil moisture comes from a model (MERRA-2).")
    elif not ctx["hay_smap"]:
        out.append("We do not have SMAP-measured soil moisture yet; for now a model (MERRA-2) is used.")
    if "supuesto" in str(rot.get("fuente", "")):
        out.append("The rules for this option are an initial assumption: they still need review by an agronomist.")
    nombres = {c["nombre"]: (c.get("en") or {}).get("nombre", c["nombre"]) for c in ctx["cultivos"].values()}
    for c in ctx["cultivos_sin_ky"]:
        out.append(f"{nombres.get(c, c).capitalize()} has no yield response factor to water in FAO-33: a neutral value "
                   "was used.")
    if ctx["es_actual"]:
        out.append("The MODIS pixel is 250 m: it may mix your plot with the neighboring ones.")
        out.append("There are no verified prices per crop: we do not compare income.")
        if ctx["ciclos_discrepan"]:
            out.append("The satellite counts a different number of cycles than you declared: confirm it with the farmer.")
    return out


def riesgos(rot: dict, ctx: dict) -> list[str]:
    ev, det, cl = ctx["ev"], ctx["det"], ctx["clima"]
    out = list((rot.get("en") or {}).get("riesgos") or [])
    pend = ctx["pendiente_pct"]
    if pend is not None and pend > 15 and ev["n_desnudos"] > 0:
        out.append(f"Slope of {pend} %: in the months without cover the rain washes the soil away.")
    can = cl["canicula"]
    if can["anios_racha_larga"] and ev["toca_canicula"]:
        out.append(f"In {can['anios_racha_larga']} of {can['anios_total']} years the canícula dry spell went past "
                   f"{can['umbral_racha_dias']} days while this crop is in the field.")
    if ctx["es_actual"] and det["quemas"]["anios_con_quema"]:
        out.append("Burning the stubble leaves the soil unprotected right before the rains.")
    return out


# ---------------------------------------------------------------- el resto del JSON de la parcela
def nombre_cultivos(texto: str, cultivos: dict) -> str:
    """«maíz + frijol» -> «maize + beans» con los nombres de data/cultivos.yaml."""
    nombres = {c["nombre"]: (c.get("en") or {}).get("nombre") for c in cultivos.values()}
    partes = [nombres.get(p) for p in texto.split(" + ")]
    return " + ".join(partes) if all(partes) else None


def zarc(z: dict, ref_yaml: dict | None) -> None:
    from motor import zarc as zarc_mod

    if z.get("encontrado"):
        en = " ".join(f"Planting recommended by ZARC ({r['institucion']}, {r['anio']}), {r['cultivo']} of "
                      f"{r['temporada']}: «{r['texto_literal']}»" for r in z["registros"])
    else:
        en = t(zarc_mod.SIN_REGISTRO)
        ref = z.get("referencia_departamento")
        if ref:
            ren = (ref_yaml or {}).get("en") or {}
            en += (f" Published reference for the department (not the municipality's window): «{ref['texto_literal']}» "
                   f"(our translation: «{ren.get('traduccion')}») ({ren.get('fuente')}).")
    bilingue(z, {"texto": en, "nota_escenario": t(z.get("nota_escenario"))})


def agregar(res: dict, base: str | None = None) -> dict:
    """Agrega los bloques `es`/`en` a todo el texto visible del JSON de la parcela (salvo las rotaciones, que
    motor/recomendar.py traduce con su contexto, y el bloque farmer, que ya trae sus dos idiomas)."""
    from motor import datos

    cultivos = datos.cultivos(base)
    p = datos.parcela(res["parcela"]["id"], base)
    bilingue(res, {"aviso": AVISO})
    bilingue(res["parcela"], {"nombre": (p.get("en") or {}).get("nombre"), "nota": (p.get("en") or {}).get("nota")})
    _t_campos(res["parcela"].get("suelo"), ("nota",))
    _t_campos(res["deteccion"]["quemas"], ("nota",))
    _t_campos(res["clima"], ("resolucion", "fuente_lluvia"))
    _t_campos(res["clima"]["canicula"], ("ventana",))
    _t_campos(res["smap"].get("respaldo"), ("etiqueta", "unidad"))
    _t_campos(res["meta"], ("nota", "datos_de_ejemplo"))
    refs = datos.zarc(base).get("referencias_departamento") or []
    zarc(res["zarc"], next((r for r in refs if r["texto_literal"] ==
                            (res["zarc"].get("referencia_departamento") or {}).get("texto_literal")), None))
    for r in res["rotaciones"]:
        for c in r["ciclos"]:
            bilingue(c, {"cultivos": [nombre_cultivos(x, cultivos) for x in c["cultivos"]]})
        for m in r["calendario"]:
            bilingue(m, {"cultivo": nombre_cultivos(m["cultivo"], cultivos) if m["cultivo"] else None,
                         "alertas": [t(a) for a in m["alertas"]]})
        for e in r["evidencia"]:
            _t_campos(e, ("dato", "unidad", "fuente", "resolucion"))
        conf = r["confianza"]
        bilingue(conf, {"motivo": conf.get("motivo_en")})
        for c in conf.get("criterios", []):
            bilingue(c, {"criterio": t(c["criterio"]), "detalle": c.get("detalle_en")})
    for f in res["fuentes"]:
        en = f.get("en") or {}
        f["en"] = {}
        bilingue(f, {"nombre": en.get("nombre"), "cita": en.get("cita", f.get("cita")),
                     "resolucion": en.get("resolucion", f.get("resolucion"))})
    res["glosario"] = [dict(g) for g in res["glosario"]]   # copia: no tocar el YAML en caché
    for g in res["glosario"]:
        en = g.get("en") or {}
        g["en"] = {}
        bilingue(g, {"termino": en.get("termino"), "definicion": en.get("definicion")})
    f = res.get("farmer")
    if f:  # el bloque farmer ya trae *_en; se agregan también `es`/`en` para seguir la misma convención
        for h in f["hechos"]:
            bilingue(h, {"motivo_gris": h.get("motivo_gris_en")})
        bilingue(f["opciones"], {"motivo_gris": f["opciones"].get("motivo_gris_en")})
        bilingue(f["opciones"]["confianza"], {"motivo": f["opciones"]["confianza"].get("motivo_en")})
    return res


def declaracion_ia(voz: str, herramienta: str) -> str:
    return (f"AI-generated synthetic voice ({herramienta}; voice {voz}) from the text the engine wrote with templates. "
            "It is not a person.")


HERRAMIENTA_EN = "edge-tts, Microsoft neural text to speech"


# ---------------------------------------------------------------- validacion.json y parcelas.json
def validacion(v: dict, base: str | None = None) -> dict:
    """Completa web/public/data/validacion.json con `es`/`en`. Se puede correr más de una vez."""
    from motor import datos

    bilingue(v, {"titular_power_chirps": t(v.get("titular_power_chirps")), "titular_2018": t(v.get("titular_2018")),
                 "notas": [t(n) for n in v.get("notas", [])]})
    _t_campos(v.get("regla_5_1"), ("efecto",))
    _t_campos(v.get("evidencia_publica_2018"), ("fuente", "nota"))
    if v.get("evidencia_publica_2018"):
        v["evidencia_publica_2018"]["es"]["cita"] = v["evidencia_publica_2018"]["en"]["cita"] = \
            v["evidencia_publica_2018"]["cita"]   # la cita original ya está en inglés
    o = v.get("observacion_2026")
    if o:
        _t_campos(o, ("titulo", "resumen", "limites"))
        for x in o.get("lluvia_chirps", []):
            _t_campos(x, ("carpeta",))
        for x in o.get("reportes_publicos", []):
            _t_campos(x, ("fuente", "nota", "relacion", "cita"))
    nombres = {p["id"]: (p.get("en") or {}).get("nombre") for p in datos.parcelas(base)}
    for p in v.get("parcelas", []):
        bilingue(p, {"nombre": nombres.get(p.get("id"))})
        _t_campos(p.get("sequia_2018"), ("fuente_lluvia",))
    return v


def parcelas_indice(indice: list[dict], base: str | None = None) -> list[dict]:
    from motor import datos

    nombres = {p["id"]: (p.get("en") or {}).get("nombre") for p in datos.parcelas(base)}
    for e in indice:
        bilingue(e, {"nombre": nombres.get(e["id"])})
    return indice


# ---------------------------------------------------------------- comprobación
def faltantes(obj, ruta: str = "") -> list[str]:
    """Rutas de los bloques `en` con algún texto en None o vacío (traducción que falta)."""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "en" and isinstance(v, dict):
                for c, x in v.items():
                    vals = x if isinstance(x, list) else [x]
                    es = (obj.get("es") or {}).get(c)
                    es_vals = es if isinstance(es, list) else [es]
                    for i, (a, b) in enumerate(zip(vals, es_vals)):
                        if b not in (None, "") and not a:
                            out.append(f"{ruta}/en/{c}" + (f"[{i}]" if isinstance(x, list) else ""))
            else:
                out += faltantes(v, f"{ruta}/{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += faltantes(v, f"{ruta}[{i}]")
    return out
