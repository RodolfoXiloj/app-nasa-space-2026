"""Sensibilidad de la canícula al reparto diario de CHIRPS v3 ('sat' contra 'rnl'). Sin red:

    python -m pipeline.validacion.sensibilidad_canicula             # comprueba y, si pasa, escribe
    python -m pipeline.validacion.sensibilidad_canicula --verificar # solo comprueba; código 1 si falla

Por qué: el hecho «canícula» del semáforo cuenta los años con una racha de más de 15 días con menos de
2 mm entre el 15 de junio y el 31 de agosto, con CHIRPS v3 diario 'sat' (cada péntada de CHIRPS repartida
por días con NASA IMERG). El Climate Hazards Center advierte que las rachas secas pueden cambiar mucho
entre 'sat' y 'rnl' (la misma péntada repartida con el reanálisis ERA5) y pide probar con las dos
(https://data.chc.ucsb.edu/products/CHIRPS/v3.0/daily/readme.txt).

Qué hace: para cada parcela arma la serie dos veces con los mismos pasos que pipeline/validacion/validar.py
(POWER diario -> corregir_lluvia con CHIRPS mensual -> aplicar_chirps_diario -> serie_escenario base) y
cambia solo la caché de CHIRPS diario: data/cache/chirps_diario/ ('sat') o data/cache/chirps_diario_rnl/
('rnl'). Usa las funciones del motor tal cual (motor/clima.py) y los cortes de data/umbrales_semaforo.yaml
con motor/farmer.estado_conteo. El resultado no entra en ningún puntaje, ni en la confianza ni en el audio.

Comprobación interna: con 'sat' tienen que salir los conteos que publica el sitio (PUBLICADOS) y, si existe
web/public/data/{parcela}.json, la misma racha año por año. Si no salen, el script no escribe nada.

Escribe data/cache/validacion/sensibilidad_canicula.json, docs/canicula-sensitivity.md y
docs/es/sensibilidad-canicula.md (se regeneran; no editar a mano).
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from datetime import date, datetime, timezone

from motor import clima, datos, farmer

# Lo que publica el sitio (web/public/data/{parcela}.json, clima.canicula.anios_racha_larga, de 25 años).
PUBLICADOS = {"jocotan": 2, "camotan": 2, "olopa": 0, "san_juan_ermita": 1, "zacapa": 3}
ANIOS_ESPERADOS = 25
VERSIONES = {
    "sat": {"carpeta": "chirps_diario", "reparto": "NASA IMERG Late V07", "reparto_en": "NASA IMERG Late V07"},
    "rnl": {"carpeta": "chirps_diario_rnl", "reparto": "reanálisis ECMWF ERA5", "reparto_en": "ECMWF ERA5 reanalysis"},
}
URL_README = "https://data.chc.ucsb.edu/products/CHIRPS/v3.0/daily/readme.txt"
# Tolerancia para comparar la lluvia total de cada mes entre versiones: las dos reparten la misma péntada,
# así que los totales mensuales deben coincidir salvo redondeo (los valores diarios se guardan con 2 decimales).
TOLERANCIA_MES_MM = 0.5
CERCA_DEL_CORTE = (14, 17)  # rachas de 14 a 17 días: a uno o dos días del corte (> 15)


def _corte() -> dict:
    return datos.umbrales_semaforo()["hechos"]["canicula"]


def serie_version(p: dict, version: str) -> dict:
    """La canícula de una parcela con la caché diaria de esa versión, con los pasos de validar.py."""
    pid = p["id"]
    power_c = datos.cache(f"power/{pid}_diario.json", parcela_=p)
    chirps_c = datos.cache(f"chirps/{pid}.json", obligatorio=False, parcela_=p)
    chirps_d = datos.cache(f"{VERSIONES[version]['carpeta']}/{pid}.json", obligatorio=True, parcela_=p)
    diario = clima.preparar(power_c)
    diario, info = clima.corregir_lluvia(diario, chirps_c)
    diario, info = clima.aplicar_chirps_diario(diario, chirps_d, info)
    anios = clima.anios_completos(diario)
    serie = clima.serie_escenario(diario, p["lat"])
    can = clima.canicula(serie, anios)
    nulos = sum(1 for _f, mm in chirps_d["datos"]["filas"] if mm is None)
    mensual: dict[tuple[int, int], float] = {}
    for f, mm in chirps_d["datos"]["filas"]:
        if mm is not None:
            k = (int(f[:4]), int(f[5:7]))
            mensual[k] = mensual.get(k, 0.0) + mm
    ventana = {}
    for a in anios:
        d, fin, tot = date(a, *clima.SUPUESTOS["canicula_ini"]), date(a, *clima.SUPUESTOS["canicula_fin"]), 0.0
        while d <= fin:
            tot += serie[d][0] if d in serie else 0.0
            d = date.fromordinal(d.toordinal() + 1)
        ventana[a] = round(tot, 1)
    return {
        "canicula": can,
        "rachas": {x["anio"]: x["racha_dias"] for x in can["por_anio"]},
        "dias_chirps_diario": info.get("dias_chirps_diario", 0),
        "dias_nulos": nulos,
        "dias_cache": len(chirps_d["datos"]["filas"]),
        "mensual": mensual,
        "lluvia_ventana_mm": ventana,
        "procedencia": chirps_d.get("procedencia", {}),
        "pixel": chirps_d["datos"].get("pixel"),
    }


def comparar_parcela(p: dict) -> dict:
    corte = _corte()
    umbral = clima.SUPUESTOS["racha_larga_dias"]
    s, r = serie_version(p, "sat"), serie_version(p, "rnl")
    anios = sorted(set(s["rachas"]) & set(r["rachas"]))
    largos_s = [a for a in anios if s["rachas"][a] > umbral]
    largos_r = [a for a in anios if r["rachas"][a] > umbral]
    dif = [r["rachas"][a] - s["rachas"][a] for a in anios]
    meses = sorted(set(s["mensual"]) & set(r["mensual"]))
    dif_mes = max((abs(s["mensual"][k] - r["mensual"][k]) for k in meses), default=None)
    lo, hi = CERCA_DEL_CORTE
    por_version = {}
    for v, x in (("sat", s), ("rnl", r)):
        n = x["canicula"]["anios_racha_larga"]
        por_version[v] = {
            "anios_racha_larga": n, "de": x["canicula"]["anios_total"],
            "anios": [a for a in anios if x["rachas"][a] > umbral],
            "estado_semaforo": farmer.estado_conteo(n, corte),
            "racha_mediana_dias": x["canicula"]["racha_mediana_dias"],
            "racha_maxima_dias": max(x["rachas"].values()) if x["rachas"] else None,
            "dias_chirps_diario_aplicados": x["dias_chirps_diario"], "dias_nulos": x["dias_nulos"],
            "pixel": x["pixel"], "url": x["procedencia"].get("url"),
            "fecha_descarga": x["procedencia"].get("fecha_descarga"), "producto": x["procedencia"].get("producto"),
        }
    return {
        "id": p["id"], "municipio": p["municipio"], "lat": p["lat"], "lon": p["lon"],
        "sat": por_version["sat"], "rnl": por_version["rnl"],
        "coinciden": sorted(set(largos_s) & set(largos_r)),
        "solo_sat": sorted(set(largos_s) - set(largos_r)),
        "solo_rnl": sorted(set(largos_r) - set(largos_s)),
        "cambia_estado": por_version["sat"]["estado_semaforo"] != por_version["rnl"]["estado_semaforo"],
        "anios_misma_racha": sum(1 for d in dif if d == 0),
        "diferencia_media_abs_dias": round(statistics.mean(abs(d) for d in dif), 1) if dif else None,
        "diferencia_mediana_rnl_menos_sat_dias": statistics.median(dif) if dif else None,
        "anios_cerca_del_corte": [a for a in anios if lo <= s["rachas"][a] <= hi or lo <= r["rachas"][a] <= hi],
        "max_diferencia_lluvia_mensual_mm": round(dif_mes, 2) if dif_mes is not None else None,
        "por_anio": [{"anio": a, "racha_sat": s["rachas"][a], "racha_rnl": r["rachas"][a],
                      "lluvia_15jun_31ago_sat_mm": s["lluvia_ventana_mm"].get(a),
                      "lluvia_15jun_31ago_rnl_mm": r["lluvia_ventana_mm"].get(a)} for a in anios],
    }


# ---------------------------------------------------------------- comprobación
def verificar_sat() -> list[str]:
    """Con 'sat' deben salir los conteos publicados y, si está el JSON del sitio, la misma racha cada año."""
    errores = []
    parcelas = {p["id"]: p for p in datos.parcelas()}
    for pid, esperado in PUBLICADOS.items():
        if pid not in parcelas:
            errores.append(f"{pid}: no está en data/parcelas.yaml")
            continue
        try:
            s = serie_version(parcelas[pid], "sat")
        except datos.FaltaDato as e:
            errores.append(f"{pid}: {e}")
            continue
        can = s["canicula"]
        if can["anios_racha_larga"] != esperado or can["anios_total"] != ANIOS_ESPERADOS:
            errores.append(f"{pid}: con 'sat' salen {can['anios_racha_larga']} de {can['anios_total']} años; "
                           f"el sitio publica {esperado} de {ANIOS_ESPERADOS}")
        web = datos.RAIZ / "web" / "public" / "data" / f"{pid}.json"
        if web.exists():
            pub = json.loads(web.read_text(encoding="utf-8")).get("clima", {}).get("canicula", {})
            pub_r = {x["anio"]: x["racha_dias"] for x in pub.get("por_anio", [])}
            if pub_r and pub_r != s["rachas"]:
                malos = sorted(a for a in set(pub_r) | set(s["rachas"]) if pub_r.get(a) != s["rachas"].get(a))
                errores.append(f"{pid}: la racha por año no coincide con {web.name} en {malos}")
    return errores


def verificar_rnl() -> list[str]:
    """La caché 'rnl' está completa y sus totales mensuales son los de 'sat' (misma péntada de CHIRPS)."""
    errores = []
    for p in datos.parcelas():
        if p["id"] not in PUBLICADOS:
            continue
        try:
            s, r = serie_version(p, "sat"), serie_version(p, "rnl")
        except datos.FaltaDato as e:
            errores.append(f"{p['id']}: {e}")
            continue
        if r["dias_cache"] != s["dias_cache"] or r["dias_nulos"]:
            errores.append(f"{p['id']}: 'rnl' tiene {r['dias_cache']} días ({r['dias_nulos']} nulos); 'sat' tiene "
                           f"{s['dias_cache']}")
        if r["pixel"] != s["pixel"]:
            errores.append(f"{p['id']}: píxel distinto entre versiones ({s['pixel']} y {r['pixel']})")
        for k in sorted(set(s["mensual"]) | set(r["mensual"])):
            a, b = s["mensual"].get(k), r["mensual"].get(k)
            if a is None or b is None or abs(a - b) > TOLERANCIA_MES_MM:
                errores.append(f"{p['id']}: lluvia de {k[0]}-{k[1]:02d} distinta entre versiones ({a} y {b} mm)")
                break
    return errores


# ---------------------------------------------------------------- informe
def _lista(xs: list) -> str:
    return ", ".join(str(x) for x in xs) if xs else "—"


def _resumen(parcelas: list[dict]) -> dict:
    n_s = sum(x["sat"]["anios_racha_larga"] for x in parcelas)
    n_r = sum(x["rnl"]["anios_racha_larga"] for x in parcelas)
    coin = sum(len(x["coinciden"]) for x in parcelas)
    solo_s = sum(len(x["solo_sat"]) for x in parcelas)
    solo_r = sum(len(x["solo_rnl"]) for x in parcelas)
    union = coin + solo_s + solo_r
    cambian = [x for x in parcelas if x["cambia_estado"]]
    iguales = [x for x in parcelas if x["sat"]["anios_racha_larga"] == x["rnl"]["anios_racha_larga"]]
    conteos_s = ", ".join(f"{x['municipio']} {x['sat']['anios_racha_larga']}" for x in parcelas)
    conteos_r = ", ".join(f"{x['municipio']} {x['rnl']['anios_racha_larga']}" for x in parcelas)
    nombres_cambian = ", ".join(f"{x['municipio']} {x['sat']['estado_semaforo']}→{x['rnl']['estado_semaforo']}"
                                for x in cambian)
    color = {"verde": "green", "amarillo": "yellow", "rojo": "red"}
    nombres_cambian_en = ", ".join(f"{x['municipio']} {color[x['sat']['estado_semaforo']]}→"
                                   f"{color[x['rnl']['estado_semaforo']]}" for x in cambian)
    n_p = len(parcelas)
    es = (f"Con el reparto de ERA5 («rnl») los años con racha seca de más de 15 días son {conteos_r} (de 25), "
          f"frente a {conteos_s} con el reparto de IMERG («sat») que usa el motor: {n_r} años-parcela contra {n_s}. "
          f"Las dos versiones coinciden en {coin} de los {union} años-parcela que marca alguna ({solo_s} solo «sat», "
          f"{solo_r} solo «rnl») y el color del semáforo "
          + (f"cambia en {len(cambian)} de {n_p} parcelas ({nombres_cambian})." if cambian
             else f"es el mismo en las {n_p} parcelas."))
    en = (f"With the ERA5-based split (“rnl”) the years with a dry spell of more than 15 days are {conteos_r} "
          f"(out of 25), against {conteos_s} with the IMERG-based split (“sat”) that the engine uses: {n_r} plot-years "
          f"against {n_s}. The two versions agree on {coin} of the {union} plot-years that either one flags "
          f"({solo_s} only in “sat”, {solo_r} only in “rnl”), and the traffic-light colour "
          + (f"changes in {len(cambian)} of {n_p} plots ({nombres_cambian_en})." if cambian
             else f"is the same in all {n_p} plots."))
    formulario = (f"with “rnl” the 5 plots have {n_r} years with a dry spell of more than 15 days in 2001-2025 "
                  f"against {n_s} with “sat” (plot-years), the two agree on {coin} of the {union} plot-years either one flags, and "
                  + (f"the traffic-light colour changes in {len(cambian)} of {n_p} plots ({nombres_cambian_en})."
                     if cambian else f"the traffic-light colour is the same in all {n_p} plots."))
    return {"anios_parcela_sat": n_s, "anios_parcela_rnl": n_r, "coinciden": coin, "solo_sat": solo_s,
            "solo_rnl": solo_r, "union": union, "parcelas_mismo_conteo": len(iguales),
            "parcelas_cambia_estado": [x["id"] for x in cambian], "es": es, "en": en,
            "frase_formulario_en": ("Dry-spell counts depend on this split, so we compared them with the ERA5-based "
                                    "“rnl” version: " + formulario)}


LIMITES_ES = [
    "«sat» y «rnl» no son independientes: las dos reparten el mismo total de cada péntada de CHIRPS y solo "
    "difieren en cómo lo reparten entre los días (readme del CHC). Coincidir no valida la racha seca; solo dice "
    "que no depende del reparto elegido.",
    "Ninguna de las dos es una medición diaria en tierra. ERA5 (~0.25°) e IMERG (0.1°) se interpolan a la malla de "
    "0.05°: el reparto diario no tiene detalle de 5 km.",
    "Cuando ERA5 o IMERG marcan cero en toda la péntada y CHIRPS no, el CHC reparte el total por igual entre los "
    "días; eso puede crear días húmedos artificiales que cortan una racha seca.",
    "Los días van en hora UTC, no en hora de Guatemala. El corte (> 15 días con < 2 mm, 15 jun-31 ago) es el del "
    "motor y no se tocó para esta prueba.",
    "Solo cambia la lluvia de junio a agosto; el resto del año y la temperatura son los mismos en las dos series. "
    "El resultado no entra en ningún puntaje, ni en la confianza ni en el audio: el semáforo publicado sigue usando «sat».",
    "Las parcelas son puntos de ejemplo elegidos con satélite, no verificados en campo.",
]
LIMITES_EN = [
    "“sat” and “rnl” are not independent: both split the same CHIRPS pentad total and differ only in how they "
    "spread it across days (CHC readme). Agreement does not validate the dry spell; it only says the result does "
    "not depend on the split chosen.",
    "Neither is a daily ground measurement. ERA5 (~0.25°) and IMERG (0.1°) are interpolated to the 0.05° grid: "
    "the daily split has no 5 km detail.",
    "When ERA5 or IMERG is zero for the whole pentad and CHIRPS is not, the CHC spreads the total evenly across the "
    "days, which can create artificial wet days that break a dry spell.",
    "Days are UTC calendar days, not Guatemala local time. The cut-off (> 15 days under 2 mm, 15 Jun-31 Aug) is the "
    "engine's and was not changed for this test.",
    "Only June-August rainfall changes; the rest of the year and temperature are the same in both series. The "
    "result does not enter any score, the confidence or the audio: the published traffic light still uses “sat”.",
    "The plots are example points chosen with satellite data, not verified in the field.",
]


def escribir_docs(r: dict) -> None:
    est_en = {"verde": "green", "amarillo": "yellow", "rojo": "red"}
    ps = r["parcelas"]
    res = r["resumen"]
    cab_anios = "| Año | " + " | ".join(x["municipio"] for x in ps) + " |"
    cab_years = "| Year | " + " | ".join(x["municipio"] for x in ps) + " |"
    sep = "|---|" + "---|" * len(ps)
    filas_anio = []
    umbral = r["metodo"]["racha_larga_dias"]
    for i, fila in enumerate(ps[0]["por_anio"]):
        celdas = []
        for x in ps:
            y = x["por_anio"][i]
            cs = f"**{y['racha_sat']}**" if y["racha_sat"] > umbral else str(y["racha_sat"])
            cr = f"**{y['racha_rnl']}**" if y["racha_rnl"] > umbral else str(y["racha_rnl"])
            celdas.append(f"{cs} / {cr}")
        filas_anio.append(f"| {fila['anio']} | " + " | ".join(celdas) + " |")
    cmd_en = ["```", "# 1. Download CHIRPS v3 daily 'rnl' for June-August 2001-2025 (HTTP range reads; the",
              "#    per-day extracts go to data/raw_big/chirps_diario_rnl/, outside the repo)",
              "MILPA_ONLINE=1 python -m pipeline.clientes.chirps --diario --version rnl",
              "# 2. Check ('sat' must give the published counts), then write the JSON and both documents, offline",
              "python -m pipeline.validacion.sensibilidad_canicula --verificar",
              "python -m pipeline.validacion.sensibilidad_canicula", "```"]
    publicados = ", ".join(f"{x['municipio']} {PUBLICADOS[x['id']]}" for x in ps)
    cmd = ["```", "# 1. Bajar CHIRPS v3 diario 'rnl' de junio-agosto 2001-2025 (lectura por rangos; los extractos por",
           "#    día quedan en data/raw_big/chirps_diario_rnl/, fuera del repo)",
           "MILPA_ONLINE=1 python -m pipeline.clientes.chirps --diario --version rnl",
           "# 2. Comprobar ('sat' debe dar los conteos publicados) y escribir el JSON y los dos documentos, sin red",
           "python -m pipeline.validacion.sensibilidad_canicula --verificar",
           "python -m pipeline.validacion.sensibilidad_canicula", "```"]

    es = ["# Sensibilidad de la canícula al reparto diario de CHIRPS", "",
          f"Generado por `python -m pipeline.validacion.sensibilidad_canicula` el {r['generado']} (UTC). **No editar a "
          "mano:** se regenera desde `data/cache/`. Versión en inglés: [canicula-sensitivity.md](../canicula-sensitivity.md).", "",
          "## Qué se probó", "",
          "El hecho «canícula» del semáforo cuenta los años con una racha de más de 15 días con menos de 2 mm entre el "
          "15 de junio y el 31 de agosto, con CHIRPS v3 diario «sat» (cada péntada de CHIRPS repartida por días con "
          f"NASA IMERG). El Climate Hazards Center advierte que las rachas secas pueden cambiar mucho con «rnl» (la "
          f"misma péntada repartida con ERA5) y pide probar con las dos ({URL_README}). Aquí se arma la serie del "
          "motor dos veces por parcela, cambiando solo la caché diaria, con las mismas funciones y los mismos cortes.", "",
          "## Resumen", "", res["es"], "",
          "## Por parcela (2001-2025, 25 años)", "",
          "| Parcela | «sat»: años (estado) | «rnl»: años (estado) | Coinciden | Solo «sat» | Solo «rnl» | Racha mediana sat / rnl (días) | Misma racha (años) | Diferencia media (días) |",
          "|---|---|---|---|---|---|---|---|---|"]
    for x in ps:
        es.append(f"| {x['municipio']} | {x['sat']['anios_racha_larga']} ({x['sat']['estado_semaforo']}) | "
                  f"{x['rnl']['anios_racha_larga']} ({x['rnl']['estado_semaforo']}) | {_lista(x['coinciden'])} | "
                  f"{_lista(x['solo_sat'])} | {_lista(x['solo_rnl'])} | {x['sat']['racha_mediana_dias']} / "
                  f"{x['rnl']['racha_mediana_dias']} | {x['anios_misma_racha']} de {len(x['por_anio'])} | "
                  f"{x['diferencia_media_abs_dias']} |")
    es += ["", "Estado con los cortes de `data/umbrales_semaforo.yaml`: verde 0 años, amarillo 1 o 2, rojo 3 o más.", "",
           "## Racha más larga de cada año (días, «sat» / «rnl»)", "",
           f"En negrita, más de {umbral} días.", "", cab_anios, sep] + filas_anio
    es += ["", "## Comprobaciones", "",
           f"- Con «sat» salen los conteos que publica el sitio ({publicados}, "
           "de 25 años) y la misma racha año por año que `web/public/data/`; si no, el script no escribe nada.",
           f"- Las dos versiones reparten la misma péntada: la lluvia de cada mes de junio a agosto difiere como mucho "
           f"{max(x['max_diferencia_lluvia_mensual_mm'] for x in ps)} mm entre «sat» y «rnl» (redondeo de los "
           "valores diarios). Confirma que se leyó el mismo píxel y el mismo periodo.",
           f"- Años con alguna racha de {CERCA_DEL_CORTE[0]} a {CERCA_DEL_CORTE[1]} días (a uno o dos días del corte): "
           + "; ".join(f"{x['municipio']} {_lista(x['anios_cerca_del_corte'])}" for x in ps) + ".", "",
           "## Límites", ""] + [f"- {t}" for t in LIMITES_ES]
    es += ["", "## Cómo reproducirlo", ""] + cmd + ["", "Fuentes: " + "; ".join(
        f"«{v}» {r['fuentes'][v]['url']} (bajado {r['fuentes'][v]['fecha_descarga']})" for v in ("sat", "rnl")) + ".", "",
        "## Frase para el formulario (inglés)", "", f"> {res['frase_formulario_en']}", ""]

    en = ["# Sensitivity of the canícula fact to the CHIRPS daily split", "",
          f"Generated by `python -m pipeline.validacion.sensibilidad_canicula` on {r['generado']} (UTC). **Do not edit "
          "by hand:** it is regenerated from `data/cache/`. Spanish version: [es/sensibilidad-canicula.md](es/sensibilidad-canicula.md).", "",
          "## What was tested", "",
          "The traffic light's «canícula» (midsummer drought) fact counts the years with a run of more than 15 days "
          "under 2 mm between 15 June and 31 August, using CHIRPS v3 daily “sat” (each CHIRPS pentad split across days "
          "with NASA IMERG). The Climate Hazards Center warns that dry spells can differ substantially with “rnl” (the "
          f"same pentad split with ERA5) and asks users to test both ({URL_README}). Here the engine's series is built "
          "twice per plot, changing only the daily cache, with the same functions and the same cut-offs.", "",
          "## Summary", "", res["en"], "",
          "## By plot (2001-2025, 25 years)", "",
          "| Plot | “sat”: years (state) | “rnl”: years (state) | Both | Only “sat” | Only “rnl” | Median spell sat / rnl (days) | Same spell (years) | Mean difference (days) |",
          "|---|---|---|---|---|---|---|---|---|"]
    for x in ps:
        en.append(f"| {x['municipio']} | {x['sat']['anios_racha_larga']} ({est_en[x['sat']['estado_semaforo']]}) | "
                  f"{x['rnl']['anios_racha_larga']} ({est_en[x['rnl']['estado_semaforo']]}) | {_lista(x['coinciden'])} | "
                  f"{_lista(x['solo_sat'])} | {_lista(x['solo_rnl'])} | {x['sat']['racha_mediana_dias']} / "
                  f"{x['rnl']['racha_mediana_dias']} | {x['anios_misma_racha']} of {len(x['por_anio'])} | "
                  f"{x['diferencia_media_abs_dias']} |")
    en += ["", "State with the cut-offs in `data/umbrales_semaforo.yaml`: green 0 years, yellow 1 or 2, red 3 or more.", "",
           "## Longest spell of each year (days, “sat” / “rnl”)", "",
           f"In bold, more than {umbral} days.", "", cab_years, sep] + filas_anio
    en += ["", "## Checks", "",
           f"- With “sat” the script reproduces the counts the site publishes "
           f"({publicados}, of 25 years) and the same spell year by year as "
           "`web/public/data/`; otherwise it writes nothing.",
           f"- Both versions split the same pentad: each June-August month's rainfall differs by at most "
           f"{max(x['max_diferencia_lluvia_mensual_mm'] for x in ps)} mm between “sat” and “rnl” (rounding of the daily "
           "values). This confirms the same pixel and period were read.",
           f"- Years with a spell of {CERCA_DEL_CORTE[0]} to {CERCA_DEL_CORTE[1]} days in either version (one or two "
           "days from the cut-off): " + "; ".join(f"{x['municipio']} {_lista(x['anios_cerca_del_corte'])}" for x in ps) + ".", "",
           "## Limits", ""] + [f"- {t}" for t in LIMITES_EN]
    en += ["", "## How to reproduce", ""] + cmd_en + ["", "Sources: " + "; ".join(
        f"“{v}” {r['fuentes'][v]['url']} (downloaded {r['fuentes'][v]['fecha_descarga']})" for v in ("sat", "rnl")) + ".", "",
        "## Sentence for the submission form", "", f"> {res['frase_formulario_en']}", ""]

    (datos.RAIZ / "docs" / "es" / "sensibilidad-canicula.md").write_text("\n".join(es), encoding="utf-8")
    (datos.RAIZ / "docs" / "canicula-sensitivity.md").write_text("\n".join(en), encoding="utf-8")


def calcular() -> dict:
    parcelas = [comparar_parcela(p) for p in datos.parcelas() if p["id"] in PUBLICADOS]
    fuentes = {v: {"url": parcelas[0][v]["url"], "fecha_descarga": parcelas[0][v]["fecha_descarga"],
                   "producto": parcelas[0][v]["producto"]} for v in ("sat", "rnl")}
    return {
        "version": "1.0", "generado": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "metodo": {
            "ventana": "15 de junio a 31 de agosto", "dia_seco_mm": clima.SUPUESTOS["dia_seco_mm"],
            "racha_larga_dias": clima.SUPUESTOS["racha_larga_dias"], "periodo": "2001-2025",
            "cortes_semaforo": _corte(), "pasos": "motor.clima: preparar -> corregir_lluvia -> aplicar_chirps_diario "
            "-> anios_completos -> serie_escenario (base) -> canicula; estado con motor.farmer.estado_conteo",
            "readme_chc": URL_README, "entra_en_puntajes": False,
        },
        "fuentes": fuentes,
        "resumen": _resumen(parcelas),
        "parcelas": parcelas,
        "limites": LIMITES_ES, "limites_en": LIMITES_EN,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--verificar", action="store_true",
                    help="solo comprueba que 'sat' da los conteos publicados y que 'rnl' está completa; no escribe")
    a = ap.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")  # consolas de Windows sin UTF-8: que «→» no tumbe el script
    errores = verificar_sat()
    if errores:
        print("FALLA la comprobación con 'sat' (no se escribe nada):", *errores, sep="\n- ")
        return 1
    print("OK 'sat': " + ", ".join(f"{k} {v}" for k, v in PUBLICADOS.items()) + f" de {ANIOS_ESPERADOS} años")
    errores = verificar_rnl()
    if errores:
        print("FALLA la caché 'rnl' (no se escribe nada):", *errores, sep="\n- ")
        print("Para bajarla: MILPA_ONLINE=1 python -m pipeline.clientes.chirps --diario --version rnl")
        return 1
    print("OK 'rnl': caché completa; totales mensuales iguales a 'sat'")
    if a.verificar:
        return 0
    r = calcular()
    ruta = datos.CACHE / "validacion" / "sensibilidad_canicula.json"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    proc = {"producto": "pipeline/validacion/sensibilidad_canicula.py", "fecha": r["generado"],
            "fuentes": r["fuentes"], "readme_chc": URL_README}
    ruta.write_text(json.dumps({"procedencia": proc, "datos": r}, ensure_ascii=False, separators=(",", ":")),
                    encoding="utf-8")
    escribir_docs(r)
    print(r["resumen"]["es"])
    print(r["resumen"]["frase_formulario_en"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
