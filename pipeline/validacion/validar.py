"""Validación pública (plan, sección 5). Un solo comando, sin red, desde data/cache/:

    python -m pipeline.validacion.validar

Escribe web/public/data/validacion.json y data/cache/validacion/resumen.json (el motor lee este
último para aplicar la regla de 5.1 a la confianza).

5.2 POWER contra CHIRPS: sesgo (mm/mes y %), error absoluto medio y Pearson, todos los meses y
    julio-agosto aparte; 2001-2025 (periodo del motor) y 1991-2000 (para mostrar el cambio de
    nivel de POWER).
5.1 Sequía de 2018: para cada año Y de 2006 a 2025 se calcula el déficit de agua de la rotación
    actual (maíz con frijol) con la lluvia corregida por CHIRPS. El motor marca «riesgo alto» si el
    déficit de Y supera el percentil 75 de los años anteriores (2001 a Y-1): solo usa lo que se
    sabía antes. Evidencia independiente del motor: anomalía de NDVI julio-septiembre de Y frente
    a 2001 a Y-1 (desviaciones estándar) y, si hay, anomalía de SMAP julio-agosto de 2018.
    Métricas: puesto de 2018 entre 25 años, parcelas que marcan 2018, aciertos y falsas alarmas
    sobre años secos conocidos (2014, 2015, 2018, 2019) y Spearman entre déficit y anomalía de NDVI.
REGLA FIJADA ANTES DE VER EL RESULTADO: no se ajustan umbrales para que 2018 salga bien. Si
ninguna señal (motor, NDVI, SMAP) muestra 2018 en 3 o más parcelas, se publica así y la confianza
de las recomendaciones de agua baja a «baja».

Observación de julio-agosto 2026 (aparte de 5.1 y 5.2): CHIRPS mensual final de 2026
(data/cache/chirps_reciente/) contra 1991-2025, y SMAP por celda de 9 km. Es una observación del
pasado, preliminar; el motor usa 2001-2025 y no la usa en puntajes, confianza ni audio.
"""
from __future__ import annotations

import json
import statistics
import sys
from datetime import datetime, timezone

from motor import clima, datos, deteccion

ANIOS_SECOS = [2014, 2015, 2018, 2019]
# Evidencia pública independiente de la sequía de 2018 (verificada el 13 nov 2026, fuente fao_giews_2018).
EVIDENCIA_2018 = {
    "fuente": "FAO GIEWS Update – Central America, 27 de agosto de 2018",
    "url": "https://www.fao.org/3/CA1321EN/ca1321en.pdf",
    "cita": ("As of 15 August 2018, the Governments of El Salvador, Guatemala and Honduras reported losses of "
             "282 000 hectares in maize and bean crops, resulting in an estimated 2.2 million people at risk of food insecurity."),
    "guatemala_ha_perdidas": 175126, "guatemala_personas_afectadas": 1290785,
    "departamentos_mas_afectados": ["Jutiapa", "Chiquimula", "El Progreso", "Jalapa", "Baja Verapaz"],
    "nota": "Estimación del MAGA del 13 ago 2018 citada por FAO GIEWS; no hay porcentaje de pérdida solo para Guatemala.",
}
# Reportes públicos de 2026, leídos en la página original el 13 nov 2026. Ninguno es la fuente de
# las cifras propias; se citan con su ámbito exacto y con lo que NO dicen.
EVIDENCIA_2026 = [
    {"id": "fews_net_2026_08", "relacion": "coincide",
     "fuente": "FEWS NET, Guatemala: actualización de la perspectiva de seguridad alimentaria, agosto 2026",
     "url": "https://fews.net/es/latin-america-and-caribbean/guatemala/actualizacion-de-la-perspectiva-de-seguridad-alimentaria/agosto-2026",
     "cita": ("Entre el 01 y el 31 de agosto, el Corredor Seco recibió entre el 5 y el 25 por ciento de las lluvias "
              "en comparación con los valores normales"),
     "nota": ("Coincide con CHIRPS, pero no es una confirmación independiente: el informe no dice de qué producto sale "
              "la cifra y su mapa de lluvia (figura 1) es del Climate Hazards Center, el mismo grupo que produce CHIRPS. "
              "Se refiere solo a agosto y a todo el Corredor Seco.")},
    {"id": "prensa_libre_2026_09_01", "relacion": "independiente: encuesta de hogares",
     "fuente": "Prensa Libre, 1 sep 2026, sobre una evaluación de Oxfam, Acción contra el Hambre y organizaciones socias",
     "url": "https://www.prensalibre.com/guatemala/comunitario/sequia-golpea-el-maiz-estudio-documenta-graves-perdidas-en-36-mil-hogares-del-corredor-seco/",
     "cita": ("En el corredor seco guatemalteco, 36 mil 431 hogares reportan serios daños en sus cosechas de maíz, "
              "según una evaluación de Oxfam, organizaciones socias y Acción contra el Hambre."),
     "nota": ("Ámbito según la nota: el corredor seco de Guatemala, sin lista de departamentos ni municipios. La nota "
              "no aclara si son hogares evaluados o una estimación; el estudio completo abarca Guatemala, Honduras y "
              "El Salvador. No se atribuye a Chiquimula ni a Zacapa.")},
    {"id": "canal_antigua_2026_09_25", "relacion": "independiente: conteo oficial de familias afectadas",
     "fuente": "Canal Antigua, 25 sep 2026",
     "url": "https://canalantigua.tv/2026/09/25/sequia-persiste-pese-a-alivio-temporal-de-lluvias-113-mil-familias-siguen-afectadas-en-chiquimula-y-jutiapa/",
     "cita": "se contabilizan 113 mil 825 familias afectadas",
     "nota": "Ámbito según la nota: «15 municipios de Chiquimula y Jutiapa, bajo alerta roja por la sequía». No da cifras de Zacapa."},
]
ANIO_OBSERVACION = 2026
MESES_OBSERVACION = (7, 8)
ANIO_INICIO_PRUEBA = 2006
ROTACION_ACTUAL = "actual_maiz_frijol"


def _rangos(xs: list[float]) -> list[float]:
    orden = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(orden):
        j = i
        while j + 1 < len(orden) and xs[orden[j + 1]] == xs[orden[i]]:
            j += 1
        for k in range(i, j + 1):
            r[orden[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(a: list[float], b: list[float]) -> float | None:
    if len(a) < 4:
        return None
    ra, rb = _rangos(a), _rangos(b)
    ma, mb = statistics.mean(ra), statistics.mean(rb)
    sa, sb = statistics.pstdev(ra), statistics.pstdev(rb)
    if sa == 0 or sb == 0:
        return None
    return round(sum((x - ma) * (y - mb) for x, y in zip(ra, rb)) / len(ra) / (sa * sb), 2)


def anomalias_ndvi(ndvi_c: dict, anios: list[int]) -> dict[int, float | None]:
    """Anomalía de NDVI julio-septiembre de cada año contra los años anteriores (desde 2001)."""
    por_anio: dict[int, list[float]] = {}
    for f, v, c in ndvi_c["datos"]["filas"]:
        if v is None or c not in deteccion.UMBRALES["calidad_valida"]:
            continue
        if f[5:7] in ("07", "08", "09"):
            por_anio.setdefault(int(f[:4]), []).append(v)
    med = {a: statistics.median(v) for a, v in por_anio.items() if len(v) >= 3}
    out = {}
    for y in anios:
        prev = [med[a] for a in med if a < y]
        if y not in med or len(prev) < 5 or statistics.pstdev(prev) == 0:
            out[y] = None
            continue
        out[y] = round((med[y] - statistics.mean(prev)) / statistics.pstdev(prev), 2)
    return out


def validar_parcela(p: dict) -> dict:
    pid = p["id"]
    power_c = datos.cache(f"power/{pid}_diario.json", parcela_=p)
    chirps_c = datos.cache(f"chirps/{pid}.json", obligatorio=False, parcela_=p)
    ndvi_c = datos.cache(f"ndvi/{pid}.json", obligatorio=False, parcela_=p)
    smap_c = datos.cache(f"smap/{pid}.json", obligatorio=False, parcela_=p)
    diario_power = clima.preparar(power_c)

    # ---- 5.2
    cmp_reciente = clima.comparar(diario_power, chirps_c, 2001, 2025)
    cmp_antiguo = clima.comparar(diario_power, chirps_c, 1991, 2000)
    pares = []
    if chirps_c:
        ch = clima.chirps_mensual(chirps_c)
        pw = clima.power_mensual(diario_power)
        pares = [[a, m, round(pw[(a, m)], 1), round(ch[(a, m)], 1)] for (a, m) in sorted(ch)
                 if (a, m) in pw and m in (7, 8) and a >= 2001]

    # ---- 5.1
    diario, info = clima.corregir_lluvia(diario_power, chirps_c)
    chirps_d = datos.cache(f"chirps_diario/{pid}.json", obligatorio=False, parcela_=p)
    diario, info = clima.aplicar_chirps_diario(diario, chirps_d, info)
    anios = clima.anios_completos(diario)
    serie = clima.serie_escenario(diario, p["lat"])
    rot = next(r for r in datos.rotaciones() if r["id"] == ROTACION_ACTUAL)
    deficit = dict(clima.deficit_por_anio(serie, anios, rot["ciclos"], datos.cultivos()))
    racha = {x["anio"]: x["racha_dias"] for x in clima.canicula(serie, anios)["por_anio"]}
    ch_ja = {}
    if chirps_c:
        ch = clima.chirps_mensual(chirps_c)
        ch_ja = {a: ch.get((a, 7), 0) + ch.get((a, 8), 0) for a in anios if (a, 7) in ch and (a, 8) in ch}

    marcas = []
    for y in [a for a in anios if a >= ANIO_INICIO_PRUEBA]:
        prev = [deficit[a] for a in deficit if a < y]
        if len(prev) < 5 or y not in deficit:
            continue
        p75 = statistics.quantiles(prev, n=4, method="inclusive")[2]
        marcas.append({"anio": y, "deficit_pct": round(100 * deficit[y]), "umbral_p75_previo_pct": round(100 * p75),
                       "riesgo_alto": deficit[y] > p75, "racha_canicula_dias": racha.get(y),
                       "lluvia_jul_ago_chirps_mm": round(ch_ja[y]) if y in ch_ja else None})
    anom = anomalias_ndvi(ndvi_c, [m["anio"] for m in marcas]) if ndvi_c else {}
    for m in marcas:
        m["anomalia_ndvi_jul_sep_de"] = anom.get(m["anio"])

    orden = sorted(deficit, key=lambda a: -deficit[a])
    puesto_2018 = orden.index(2018) + 1 if 2018 in deficit else None
    m2018 = next((m for m in marcas if m["anio"] == 2018), None)
    ac = sum(1 for m in marcas if m["riesgo_alto"] and m["anio"] in ANIOS_SECOS)
    fa = sum(1 for m in marcas if m["riesgo_alto"] and m["anio"] not in ANIOS_SECOS)
    fallos = sum(1 for m in marcas if not m["riesgo_alto"] and m["anio"] in ANIOS_SECOS)
    pares_sp = [(m["deficit_pct"], -m["anomalia_ndvi_jul_sep_de"]) for m in marcas if m["anomalia_ndvi_jul_sep_de"] is not None]
    rho = spearman([a for a, _ in pares_sp], [b for _, b in pares_sp]) if pares_sp else None
    smap_2018 = (smap_c or {}).get("datos", {}).get("anomalia_2018_de") if smap_c else None
    ndvi_2018 = m2018["anomalia_ndvi_jul_sep_de"] if m2018 else None
    senales = {
        "motor": bool(m2018 and m2018["riesgo_alto"]),
        "ndvi": ndvi_2018 is not None and ndvi_2018 <= -1.0,
        "smap": smap_2018 is not None and smap_2018 <= -1.0,
    }
    return {
        "id": pid, "nombre": p["nombre"], "municipio": p["municipio"], "lat": p["lat"], "lon": p["lon"],
        "pixel_chirps": (chirps_c or {}).get("datos", {}).get("pixel"),
        "power_vs_chirps": {"2001-2025": cmp_reciente, "1991-2000": cmp_antiguo, "pares_jul_ago": pares},
        "sequia_2018": {
            "anios": marcas, "puesto_2018_de": len(deficit), "puesto_2018": puesto_2018,
            "aciertos": ac, "falsas_alarmas": fa, "fallos": fallos, "n_anios": len(marcas),
            "anios_secos_conocidos": ANIOS_SECOS, "spearman_deficit_vs_ndvi": rho, "n_spearman": len(pares_sp),
            "anomalia_ndvi_2018_de": ndvi_2018, "anomalia_smap_2018_de": smap_2018, "senales_2018": senales,
            "fuente_lluvia": info.get("fuente"),
        },
    }


def observacion_2026(anio: int = ANIO_OBSERVACION, meses: tuple[int, ...] = MESES_OBSERVACION) -> dict | None:
    """Julio-agosto 2026 contra el registro: CHIRPS por parcela y SMAP por celda de 9 km. None si falta la caché."""
    lluvia = []
    for p in datos.parcelas():
        rec = datos.cache(f"chirps_reciente/{p['id']}.json", obligatorio=False, parcela_=p)
        hist = datos.cache(f"chirps/{p['id']}.json", obligatorio=False, parcela_=p)
        if not rec or not hist or rec["datos"].get("anio") != anio:
            continue
        mm = rec["datos"]["meses"]
        if any(mm.get(str(m)) is None for m in meses):
            continue
        total = round(sum(mm[str(m)] for m in meses), 1)
        por_anio: dict[int, list[float]] = {}
        for a, m, v in hist["datos"]["filas"]:
            if m in meses and v is not None:
                por_anio.setdefault(a, []).append(v)
        ref = {a: sum(v) for a, v in por_anio.items() if len(v) == len(meses)}
        if len(ref) < 10:
            continue
        med = statistics.median(ref.values())
        a_min = min(ref, key=ref.get)
        lluvia.append({"id": p["id"], "municipio": p["municipio"], "mm_2026": total,
                       "mm_por_mes": {str(m): mm[str(m)] for m in meses},
                       "mediana_mm": round(med, 1), "pct_de_la_mediana": round(100 * total / med),
                       "minimo_anterior_mm": round(ref[a_min], 1), "anio_minimo_anterior": a_min,
                       "anios_mas_secos_que_2026": sum(1 for v in ref.values() if v < total),
                       "periodo_referencia": f"{min(ref)}-{max(ref)}", "n_anios_referencia": len(ref),
                       "archivos": rec["datos"].get("archivos"), "carpeta": rec["datos"].get("carpeta")})
    if not lluvia:
        return None
    celdas: dict[tuple, dict] = {}
    sin_smap = []
    for p in datos.parcelas():
        s = datos.cache(f"smap/{p['id']}.json", obligatorio=False, parcela_=p)
        d = (s or {}).get("datos", {})
        pa = {int(a): v for a, v in (d.get("por_anio_jul_ago") or {}).items()}
        if anio not in pa or not d.get("celda"):
            sin_smap.append(p["municipio"])
            continue
        clave = (d["celda"]["linea"], d["celda"]["muestra"])
        c = celdas.setdefault(clave, {"celda": d["celda"], "parcelas": [], "por_anio": pa})
        c["parcelas"].append(p["municipio"])
    smap = []
    for c in celdas.values():
        pa = c["por_anio"]
        otros = {a: v for a, v in pa.items() if a != anio}
        a_min = min(otros, key=otros.get)
        smap.append({"parcelas": c["parcelas"], "celda": c["celda"], "m3m3_2026": pa[anio],
                     "minimo_anterior_m3m3": otros[a_min], "anio_minimo_anterior": a_min,
                     "es_el_mas_bajo": pa[anio] < otros[a_min], "n_anios": len(pa),
                     "periodo": f"{min(pa)}-{max(pa)}"})
    pcts = [x["pct_de_la_mediana"] for x in lluvia]
    minimos = sum(1 for x in lluvia if x["anios_mas_secos_que_2026"] == 0)
    n_smap_min = sum(1 for x in smap if x["es_el_mas_bajo"])
    n_anios_smap = max((x["n_anios"] for x in smap), default=0)
    ref_periodo = lluvia[0]["periodo_referencia"]
    resumen = (f"En julio y agosto de {anio} llovió entre el {min(pcts)} % y el {max(pcts)} % de lo normal (mediana "
               f"{ref_periodo}) en las {len(lluvia)} parcelas, según CHIRPS v3; es lo menos desde {ref_periodo[:4]} "
               f"en {minimos} de {len(lluvia)}.")
    if smap:
        resumen += (f" SMAP registra la humedad del suelo de julio-agosto más baja de sus {n_anios_smap} años en "
                    f"{n_smap_min} de {len(smap)} celdas de 9 km con dato.")
    return {
        "titulo": f"Observación preliminar: julio-agosto {anio}",
        "resumen": resumen,
        "limites": [
            f"Es una observación del pasado, no un pronóstico. El motor usa 2001-2025: {anio} no entra en los puntajes, "
            "la confianza ni el audio.",
            "Preliminar: el Climate Hazards Center recalcula CHIRPS cada mes y SMAP puede reprocesarse. Los meses de "
            f"{anio} vienen de la carpeta del producto final (no de prelim/); se guarda la fecha de cada archivo.",
            f"SMAP: {len(smap)} celdas de 9 km con dato ({sum(len(x['parcelas']) for x in smap)} parcelas"
            + "".join(f"; {' y '.join(x['parcelas'])} comparten celda" for x in smap if len(x["parcelas"]) > 1) + ")"
            + (f"; sin dato de calidad recomendada: {', '.join(sin_smap)}." if sin_smap else ".")
            + f" Con {n_anios_smap} años, «el más bajo» es todo lo que se puede decir; no se da percentil.",
            "Las parcelas son puntos de ejemplo elegidos con satélite, no verificados en campo.",
        ],
        "lluvia_chirps": lluvia,
        "smap_celdas": smap,
        "smap_sin_dato": sin_smap,
        "reportes_publicos": EVIDENCIA_2026,
    }


def validar() -> dict:
    parcelas = []
    for p in datos.parcelas():
        disp = datos.disponibilidad(p["id"])
        if not disp["power_diario"]:
            continue
        parcelas.append(validar_parcela(p))
    con_2018 = sum(1 for x in parcelas if any(x["sequia_2018"]["senales_2018"].values()))
    regla = con_2018 < 3
    jocotan = next((x for x in parcelas if x["id"] == "jocotan"), parcelas[0] if parcelas else None)
    titular = None
    if jocotan and jocotan["power_vs_chirps"]["2001-2025"]:
        ja = jocotan["power_vs_chirps"]["2001-2025"]["jul_ago"]
        titular = (f"En julio-agosto, NASA POWER se desvía {ja['sesgo_pct']} % de CHIRPS en {jocotan['municipio']} "
                   f"(error medio de {ja['eam_mm_mes']} mm/mes, r = {ja['pearson_r']}, n = {ja['n']} meses, 2001-2025).")
    marcan_motor = sum(1 for x in parcelas if x["sequia_2018"]["senales_2018"]["motor"])
    out = {
        "version": "1.0", "generado": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "titular_power_chirps": titular,
        "titular_2018": (f"El motor, con lo que se sabía hasta 2017, marca 2018 como riesgo alto en {marcan_motor} de "
                         f"{len(parcelas)} parcelas; alguna señal (motor, NDVI o SMAP) lo muestra en {con_2018}."),
        "regla_5_1": {"parcelas_con_senal_2018": con_2018, "minimo": 3, "se_activa": regla,
                      "efecto": "La confianza de las recomendaciones de agua baja a «baja»." if regla else "Ninguno."},
        "evidencia_publica_2018": EVIDENCIA_2018,
        "observacion_2026": observacion_2026(),
        "parcelas": parcelas,
        "notas": [
            "CHIRPS no es medición en tierra: mezcla satélite y estaciones. Las estaciones de INSIVUMEH quedan como vacío.",
            "POWER: celda de 0.5° x 0.625° (~50 km). CHIRPS: 0.05° (~5 km).",
            "La lluvia del motor es el total mensual de CHIRPS repartido con los días de POWER.",
            "Riesgo alto = déficit del año mayor que el percentil 75 de los años anteriores (desde 2001).",
            "Señal de NDVI = anomalía de julio-septiembre de -1 desviación estándar o menos.",
        ],
    }
    destino = datos.RAIZ / "web" / "public" / "data" / "validacion.json"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    resumen = datos.CACHE / "validacion" / "resumen.json"
    resumen.parent.mkdir(parents=True, exist_ok=True)
    resumen.write_text(json.dumps({"procedencia": {"producto": "pipeline/validacion/validar.py", "fecha": out["generado"]},
                                   "datos": {"regla_5_1": out["regla_5_1"]}}, ensure_ascii=False), encoding="utf-8")
    escribir_md(out)
    return out


def _s(v) -> str:
    return "—" if v is None else (f"+{v}" if isinstance(v, (int, float)) and v > 0 else str(v))


def escribir_md(v: dict) -> None:
    """docs/validacion.md con las mismas cifras que validacion.json (se regenera, no editar a mano)."""
    L = ["# Validación de Milpa Resiliente", "",
         f"Generado por `python -m pipeline.validacion.validar` el {v['generado']} (UTC). **No editar a mano:** se "
         "regenera desde `data/cache/` y da las mismas cifras que la pestaña Validación de la web.", "",
         "## Regla fijada antes de ver el resultado", "",
         "No se ajustan umbrales para que 2018 salga bien. Si ninguna señal (motor, NDVI o SMAP) muestra 2018 en 3 o "
         "más parcelas, se publica así y la confianza de las recomendaciones de agua baja a «baja».", "",
         f"**Resultado:** {v['regla_5_1']['parcelas_con_senal_2018']} parcelas con señal; la regla "
         f"{'SE ACTIVA' if v['regla_5_1']['se_activa'] else 'no se activa'}. {v['regla_5_1']['efecto']}", "",
         "## 5.2 Lluvia de NASA POWER contra CHIRPS", "", v.get("titular_power_chirps") or "", "",
         "| Parcela | Píxel CHIRPS | Todo el año 2001-2025: POWER / CHIRPS (mm/mes) | Sesgo | Julio-agosto: sesgo · error medio · r · n | Sesgo 1991-2000 |",
         "|---|---|---|---|---|---|"]
    for p in v["parcelas"]:
        a, b = p["power_vs_chirps"]["2001-2025"], p["power_vs_chirps"]["1991-2000"]
        px = p.get("pixel_chirps") or {}
        L.append(f"| {p['municipio']} | {px.get('lat_centro', '—')}, {px.get('lon_centro', '—')} | "
                 f"{a['todos']['power_mm_mes'] if a else '—'} / {a['todos']['chirps_mm_mes'] if a else '—'} | "
                 f"{_s(a['todos']['sesgo_pct']) if a else '—'} % | "
                 + (f"{_s(a['jul_ago']['sesgo_pct'])} % · {a['jul_ago']['eam_mm_mes']} mm · {a['jul_ago']['pearson_r']} · {a['jul_ago']['n']}" if a else "—")
                 + f" | {_s(b['todos']['sesgo_pct']) if b else '—'} % |")
    L += ["", "## 5.1 La sequía de 2018", "", v["titular_2018"], "",
          "Riesgo alto = déficit del año mayor que el percentil 75 de los años anteriores (desde 2001), con la lluvia "
          "de CHIRPS. Años secos conocidos: " + ", ".join(str(x) for x in ANIOS_SECOS) + ".", "",
          "| Parcela | Puesto de 2018 (déficit) | Motor marca 2018 | NDVI jul-sep 2018 | SMAP jul-ago 2018 | Aciertos · falsas alarmas · fallos (n) | Spearman déficit vs NDVI (n) |",
          "|---|---|---|---|---|---|---|"]
    for p in v["parcelas"]:
        s2 = p["sequia_2018"]
        L.append(f"| {p['municipio']} | {s2['puesto_2018']} de {s2['puesto_2018_de']} | "
                 f"{'sí' if s2['senales_2018']['motor'] else 'no'} | "
                 f"{_s(s2['anomalia_ndvi_2018_de'])} DE | {_s(s2['anomalia_smap_2018_de'])} DE | "
                 f"{s2['aciertos']} · {s2['falsas_alarmas']} · {s2['fallos']} ({s2['n_anios']}) | "
                 f"{_s(s2['spearman_deficit_vs_ndvi'])} ({s2['n_spearman']}) |")
    e = v.get("evidencia_publica_2018") or {}
    if e:
        L += ["", "### Evidencia pública de la sequía de 2018", "",
              f"{e['fuente']} ({e['url']}): «{e['cita']}» Guatemala: {e['guatemala_ha_perdidas']} ha perdidas y "
              f"{e['guatemala_personas_afectadas']} personas afectadas; departamentos más afectados: "
              + ", ".join(e["departamentos_mas_afectados"]) + f". {e['nota']}"]
    o = v.get("observacion_2026")
    if o:
        L += ["", f"## {o['titulo']}", "", o["resumen"], "",
              "| Parcela | Julio + agosto (mm) | Mediana de referencia (mm) | % de la mediana | Mínimo anterior (año) | Años más secos |",
              "|---|---|---|---|---|---|"]
        for x in o["lluvia_chirps"]:
            L.append(f"| {x['municipio']} | {x['mm_2026']} | {x['mediana_mm']} | {x['pct_de_la_mediana']} % | "
                     f"{x['minimo_anterior_mm']} ({x['anio_minimo_anterior']}) | {x['anios_mas_secos_que_2026']} de "
                     f"{x['n_anios_referencia']} |")
        L += ["", "| Celda SMAP (9 km) | Parcelas | Julio-agosto 2026 (m³/m³) | Mínimo anterior (año) | ¿El más bajo? | Años |",
              "|---|---|---|---|---|---|"]
        for x in o["smap_celdas"]:
            L.append(f"| {x['celda']['linea']}, {x['celda']['muestra']} | {', '.join(x['parcelas'])} | {x['m3m3_2026']} | "
                     f"{x['minimo_anterior_m3m3']} ({x['anio_minimo_anterior']}) | {'sí' if x['es_el_mas_bajo'] else 'no'} | "
                     f"{x['n_anios']} ({x['periodo']}) |")
        L += ["", "Reportes públicos (no son la fuente de las cifras de arriba):", ""]
        for e2 in o["reportes_publicos"]:
            L.append(f"- {e2['fuente']} ({e2['relacion']}): «{e2['cita']}». {e2['nota']} {e2['url']}")
        L += ["", "Límites:", ""] + [f"- {t}" for t in o["limites"]]
    L += ["", "## Notas y límites", ""] + [f"- {n}" for n in v["notas"]] + [
        "- SMAP: SPL3SMP_E.006 por AppEEARS, solo datos con calidad recomendada. Camotán no tiene ninguno; Jocotán y "
        "San Juan Ermita comparten la celda de 9 km.",
        "- Anomalía de SMAP de 2018 = julio-agosto de 2018 frente a los demás años con SMAP (desde 2015, incluidos años "
        "posteriores a 2018). SMAP no entra en la corrida «con lo que se sabía hasta 2017»: esa corrida solo usa el "
        "déficit de agua con la lluvia de CHIRPS.",
        "- Las 5 parcelas son puntos de ejemplo elegidos con NDVI e imagen Sentinel-2, no verificados en campo; ver docs/es/memoria/.", ""]
    ruta = datos.RAIZ / "docs" / "validacion.md"
    ruta.write_text(chr(10).join(L), encoding="utf-8")


if __name__ == "__main__":
    r = validar()
    print(r["titular_power_chirps"])
    print(r["titular_2018"])
    print("Regla 5.1:", r["regla_5_1"])
    for x in r["parcelas"]:
        s = x["sequia_2018"]
        c = x["power_vs_chirps"]["2001-2025"]
        print(f"- {x['id']}: 2018 puesto {s['puesto_2018']}/{s['puesto_2018_de']}, señales {s['senales_2018']}, "
              f"aciertos {s['aciertos']}, falsas alarmas {s['falsas_alarmas']}, fallos {s['fallos']} (n={s['n_anios']}), "
              f"Spearman {s['spearman_deficit_vs_ndvi']} (n={s['n_spearman']}); POWER-CHIRPS jul-ago "
              f"{(c or {}).get('jul_ago')}")
    sys.exit(0)
