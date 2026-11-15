"""Bloque `farmer` del contrato: lo que pinta la vista «Para el agricultor».

Solo reordena cifras que el motor ya calculó en `deteccion`, `clima` y `rotaciones`; no calcula
puntajes ni trae cifras propias. La vista del agricultor y la vista «Evidence» leen el mismo JSON.

Los tres hechos van siempre en este orden: suelo (MODIS), quema (FIRMS) y canícula (lluvia diaria).

Semáforo y regla de empate: umbrales confirmados por Rodolfo el sáb 14 nov 2026 (docs/umbrales.md),
escritos en data/umbrales_semaforo.yaml.
- Cada hecho sale verde, amarillo, rojo o gris. El gris es por hecho: solo si falla su propia fuente.
- Opciones: si dos opciones difieren `margen_empate` puntos o menos en el total (escenario base), no hay
  ganadora. Vale entre alternativas y contra la práctica actual, y se aplica en cadena.
- Con confianza baja, el bloque de opciones va en gris con el motivo, en español y en inglés.
- Frases cortas en español e inglés (motor/frases.py): la vista las muestra y el audio corto lee solo
  esas frases. Sus tiempos (`inicio_s`, `fin_s`) y la ranura `audio.es` los llena motor/exportar.py
  cuando hay un mp3 vigente.
Si el YAML dice `estado: pendiente` (o no se pasa), cada `estado` queda en None, `opciones.estado` es
"pendiente" y la web no inventa un estado.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from motor import datos as _datos
from motor import frases as _frases_mod

VERSION = "1"
ORDEN = ("suelo", "quema", "canicula")
DOCUMENTO_UMBRALES = "docs/umbrales.md"
IDIOMAS = ("es", "en", "caa")  # caa: ch'orti' (ISO 639-3); sin grabación queda en None
ESTADOS = ("verde", "amarillo", "rojo", "gris")

# Por qué un hecho sale gris. Sin cifras: los cortes están en `umbrales.cortes` y en docs/umbrales.md.
MOTIVOS_GRIS = {
    "suelo_validos": {"es": "Hay pocas imágenes MODIS válidas en este píxel, por nubes o mala calidad",
                      "en": "There are too few valid MODIS images for this pixel, because of clouds or poor quality"},
    "suelo_sin_mediana": {"es": "Algún mes no tiene ninguna imagen MODIS válida",
                          "en": "Some month has no valid MODIS image"},
    "quema": {"es": "No hay datos de FIRMS para esta parcela",
              "en": "There is no FIRMS data for this plot"},
    "canicula": {"es": "La lluvia de junio a agosto viene solo de NASA POWER, una celda grande, y no de CHIRPS diario",
                 "en": "June to August rain comes only from NASA POWER, a coarse cell, and not from CHIRPS daily"},
}


def confirmados(umbrales: dict | None) -> bool:
    return bool(umbrales) and umbrales.get("estado") == "confirmado"


def _fuentes_canicula(cl: dict) -> list[str]:
    """La canícula (15 jun-31 ago) usa la lluvia diaria de junio-agosto: CHIRPS diario si se aplicó."""
    if "CHIRPS v3 diario" in (cl.get("fuente_lluvia") or ""):
        return ["chirps_diario", "imerg"]
    return [f for f in cl["fuente_ids"] if f != "fao56"]


# ---------------------------------------------------------------- semáforo de 3 hechos
def estado_conteo(valor: int, corte: dict) -> str:
    """Quema y canícula: verde con 0 años, amarillo desde `amarillo_desde`, rojo desde `rojo_desde`."""
    if valor >= corte["rojo_desde"]:
        return "rojo"
    if valor >= corte["amarillo_desde"]:
        return "amarillo"
    return "verde"


def estado_suelo(desnudos: int, poca_cobertura: int, corte: dict) -> str:
    """Rojo con `rojo_desde` meses desnudos o más; amarillo con `amarillo_desde` mes desnudo, o 0 desnudos
    y algún mes de poca cobertura; verde sin meses desnudos ni de poca cobertura."""
    if desnudos >= corte["rojo_desde"]:
        return "rojo"
    if desnudos >= corte["amarillo_desde"] or poca_cobertura > 0:
        return "amarillo"
    return "verde"


def gris_suelo(det: dict, corte: dict) -> dict | None:
    if det["calidad"]["pct_validos"] < corte["gris_pct_validos_menor_que"]:
        return MOTIVOS_GRIS["suelo_validos"]
    if any(m["mediana"] is None for m in det["ndvi_mensual"]):
        return MOTIVOS_GRIS["suelo_sin_mediana"]
    return None


def gris_quema(q: dict) -> dict | None:
    return MOTIVOS_GRIS["quema"] if not q["anios_observados"] else None


def gris_canicula(fuente_ids: list[str]) -> dict | None:
    return None if "chirps_diario" in fuente_ids else MOTIVOS_GRIS["canicula"]


def _con_estado(hecho: dict, estado: str, gris: dict | None) -> dict:
    if gris:
        return dict(hecho, estado="gris", motivo_gris=gris["es"], motivo_gris_en=gris["en"])
    return dict(hecho, estado=estado)


def _hechos(res: dict, umbrales: dict | None) -> list[dict]:
    det = res["deteccion"]
    q = det["quemas"]
    cl = res["clima"]
    can = cl["canicula"]
    fuentes_can = _fuentes_canicula(cl)
    poca = list(det.get("meses_poca_cobertura", []))
    hechos = [
        {"id": "suelo", "estado": None, "valor": len(det["meses_desnudos"]), "de": 12, "unidad": "meses",
         "meses": list(det["meses_desnudos"]), "meses_poca_cobertura": poca,
         "periodo": det["periodo"], "fuente_ids": ["modis_mod13q1"], "motivo_gris": None, "motivo_gris_en": None},
        {"id": "quema", "estado": None, "valor": q["anios_con_quema"], "de": q["anios_observados"], "unidad": "anios",
         "meses": list(q["meses_con_quema"]),
         "periodo": q["periodo"], "fuente_ids": ["firms_viirs"], "motivo_gris": None, "motivo_gris_en": None},
        {"id": "canicula", "estado": None, "valor": can["anios_racha_larga"], "de": can["anios_total"], "unidad": "anios",
         "periodo": cl["periodo"], "fuente_ids": fuentes_can, "motivo_gris": None, "motivo_gris_en": None},
    ]
    if not confirmados(umbrales):
        return hechos
    c = umbrales["hechos"]
    suelo, quema, canicula = hechos
    return [
        _con_estado(suelo, estado_suelo(suelo["valor"], len(poca), c["suelo"]), gris_suelo(det, c["suelo"])),
        _con_estado(quema, estado_conteo(quema["valor"], c["quema"]), gris_quema(q)),
        _con_estado(canicula, estado_conteo(canicula["valor"], c["canicula"]), gris_canicula(fuentes_can)),
    ]


# ---------------------------------------------------------------- opciones y regla de empate
def empatadas(totales: dict[str, float], margen: float) -> list[str]:
    """Opciones parejas con la de mayor total, unidas en cadena.

    Se parte de la opción con el total más alto y se suma toda opción que quede a `margen` puntos o
    menos de alguna ya sumada. Así en Olopa (87, 90 y 92) la canavalia empata con la práctica actual y
    con el maíz ICTA B-5, y las tres quedan juntas aunque el B-5 supere a la actual por 5 puntos.
    Devuelve los ids en el orden de entrada (práctica actual y luego alternativas), que no es un ranking.
    """
    ids = list(totales)
    grupo = {max(ids, key=lambda i: totales[i])}
    sumo = True
    while sumo:
        sumo = False
        for i in ids:
            if i not in grupo and any(abs(totales[i] - totales[j]) <= margen + 1e-9 for j in grupo):
                grupo.add(i)
                sumo = True
    return [i for i in ids if i in grupo]


def _opciones(res: dict, umbrales: dict | None) -> dict:
    rots = res["rotaciones"]
    actual = next(r for r in rots if r["es_actual"])
    conf = actual["confianza"]
    out = {
        "estado": "pendiente",
        "actual": actual["id"],
        "alternativas": [r["id"] for r in rots if not r["es_actual"]],
        "destaca": None,
        "empatadas": [],
        "regla_puntaje": None,
        "confianza": {"nivel": conf["nivel"], "motivo": conf["motivo"], "motivo_en": conf.get("motivo_en")},
        "motivo_gris": None,
        "motivo_gris_en": None,
    }
    if not confirmados(umbrales):
        return out
    orden = [actual] + [r for r in rots if not r["es_actual"]]
    grupo = empatadas({r["id"]: r["puntajes"]["total"] for r in orden}, umbrales["opciones"]["margen_empate"])
    regla = "empate" if len(grupo) > 1 else "una_destaca"
    out.update(empatadas=grupo if regla == "empate" else [], regla_puntaje=regla)
    if conf["nivel"] == "baja":
        # Con confianza baja no se destaca ninguna: el bloque va en gris con el motivo.
        out.update(estado="gris", motivo_gris=conf["motivo"], motivo_gris_en=conf.get("motivo_en") or conf["motivo"])
    elif regla == "empate":
        out.update(estado="empate")
    else:
        out.update(estado="una_destaca", destaca=grupo[0])
    return out


def _umbrales(umbrales: dict | None) -> dict:
    if not confirmados(umbrales):
        return {"estado": "pendiente", "documento": DOCUMENTO_UMBRALES}
    return {
        "estado": "confirmado",
        "documento": umbrales.get("documento", DOCUMENTO_UMBRALES),
        "confirmado_por": umbrales.get("confirmado_por"),
        "margen_empate": umbrales["opciones"]["margen_empate"],
        "cortes": umbrales["hechos"],
        "estados": umbrales["estados"],
    }


# ---------------------------------------------------------------- este año y el futuro, para el agricultor
WEB_DATA = _datos.RAIZ / "web" / "public" / "data"


def _leer(ruta: Path) -> dict | None:
    try:
        return json.loads(ruta.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def este_anio(pid: str, web: Path = WEB_DATA) -> dict | None:
    """Lluvia de julio y agosto de 2026 frente a lo normal (mediana 1991-2025) y frente al año más seco, de los
    archivos que ya publica el sitio: data/validacion.json (pipeline/validacion/validar.py, la cifra de la línea
    2026) y data/explorar/{pid}.json (motor/explorar.py, los milímetros). Es una observación preliminar: no entra
    en puntajes ni en la confianza. None si falta alguno: no se adivina."""
    v = _leer(web / "validacion.json") or {}
    fila = next((x for x in ((v.get("observacion_2026") or {}).get("lluvia_chirps") or []) if x.get("id") == pid), None)
    lj = (_leer(web / "explorar" / f"{pid}.json") or {}).get("lluvia_jul_ago") or {}
    if not fila or not isinstance(fila.get("pct_de_la_mediana"), (int, float)) or lj.get("total_2026_mm") is None:
        return None
    ref = lj.get("periodo_referencia") or fila.get("periodo_referencia") or ""
    return {
        "pct_de_la_mediana": fila["pct_de_la_mediana"], "periodo_referencia": ref, "desde": int(ref[:4]) if ref[:4].isdigit() else None,
        "total_2026_mm": round(lj["total_2026_mm"]), "mediana_mm": round(lj["mediana_jul_ago_mm"]),
        "anio_mas_seco": lj.get("anio_mas_seco"),
        "total_mas_seco_mm": round(lj["total_mas_seco_mm"]) if lj.get("total_mas_seco_mm") is not None else None,
        "preliminar": True, "fuente_ids": ["chirps"],
    }


def futuros(pid: str, web: Path = WEB_DATA) -> dict | None:
    """Las rotaciones en los futuros de la NASA (NEX-GDDP-CMIP6, SSP2-4.5, 2041-2060) de data/futuros_nasa.json
    (motor/futuros.py): en cuántos le alcanza el agua a cada una, y en cuáles. None si la parcela no está."""
    f = _leer(web / "futuros_nasa.json") or {}
    e = (((f.get("parcelas") or {}).get(pid) or {}).get("escenarios") or {}).get("ssp245")
    m = re.match(r"(\d{4})\D+(\d{4})", f.get("periodo_futuro") or "")
    if not e or not m:
        return None
    rots = []
    for r in e["rotaciones"]:
        por_modelo = [bool((x.get("aguanta") or {}).get(r["id"])) for x in e["modelos"]]
        assert sum(por_modelo) == r["futuros_que_aguanta"], (pid, r["id"])
        rots.append({"id": r["id"], "aguantan": r["futuros_que_aguanta"], "de": e["n_modelos"], "por_modelo": por_modelo})
    return {
        "escenario": "ssp245", "desde": int(m.group(1)), "hasta": int(m.group(2)), "n_modelos": e["n_modelos"],
        "modelos": [x["modelo"] for x in e["modelos"]], "rotaciones": rots, "fuente_ids": ["nex_gddp_cmip6"],
    }


def bloque(res: dict, umbrales: dict | None = None, pid: str | None = None, web: Path = WEB_DATA) -> dict:
    """Bloque `farmer` a partir del JSON ya armado por motor.recomendar.recomendar().

    `umbrales`: contenido de data/umbrales_semaforo.yaml (motor.datos.umbrales_semaforo). Sin él, o con
    `estado: pendiente`, no hay estados. Con `pid`, suma «este año» y «el futuro» si el sitio ya publica sus datos."""
    hechos = _hechos(res, umbrales)
    opciones = _opciones(res, umbrales)
    anio = este_anio(pid, web) if pid else None
    fut = futuros(pid, web) if pid else None
    if fut and {r["id"] for r in res["rotaciones"]} - {x["id"] for x in fut["rotaciones"]}:
        fut = None  # los futuros se calcularon para las rotaciones de otro cultivo declarado: no se mezclan
    return {
        "version": VERSION,
        "umbrales": _umbrales(umbrales),
        "hechos": hechos,
        "opciones": opciones,
        "este_anio": anio,
        "futuros": fut,
        "frases": _frases_mod.construir(res, hechos, opciones, umbrales, anio, fut) if confirmados(umbrales) else [],
        "audio": {lang: None for lang in IDIOMAS},
    }
