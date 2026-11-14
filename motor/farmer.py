"""Bloque `farmer` del contrato: lo que pinta la vista «Para el agricultor».

Solo reordena cifras que el motor ya calculó en `deteccion`, `clima` y `rotaciones`; no calcula
nada nuevo ni trae cifras propias. La vista del agricultor y la vista «Evidence» leen el mismo JSON.

Los tres hechos van siempre en este orden: suelo (MODIS), quema (FIRMS) y canícula (lluvia diaria).

Los estados del semáforo (verde, amarillo, rojo, gris) y la regla de empate dependen de los umbrales
propuestos en docs/umbrales.md. Mientras el equipo no los confirme, `umbrales.estado` es "pendiente",
cada `estado` queda en None y `opciones.estado` es "pendiente". La web no debe inventar un estado.
"""
from __future__ import annotations

VERSION = "1"
ORDEN = ("suelo", "quema", "canicula")
DOCUMENTO_UMBRALES = "docs/umbrales.md"
IDIOMAS = ("es", "en", "caa")  # caa: ch'orti' (ISO 639-3); sin grabación queda en None


def _fuentes_canicula(cl: dict) -> list[str]:
    """La canícula (15 jun-31 ago) usa la lluvia diaria de junio-agosto: CHIRPS diario si se aplicó."""
    if "CHIRPS v3 diario" in (cl.get("fuente_lluvia") or ""):
        return ["chirps_diario", "imerg"]
    return [f for f in cl["fuente_ids"] if f != "fao56"]


def _hechos(res: dict) -> list[dict]:
    det = res["deteccion"]
    q = det["quemas"]
    cl = res["clima"]
    can = cl["canicula"]
    return [
        {"id": "suelo", "estado": None, "valor": len(det["meses_desnudos"]), "de": 12, "unidad": "meses",
         "meses": list(det["meses_desnudos"]),
         "meses_poca_cobertura": list(det.get("meses_poca_cobertura", [])),
         "periodo": det["periodo"], "fuente_ids": ["modis_mod13q1"], "motivo_gris": None},
        {"id": "quema", "estado": None, "valor": q["anios_con_quema"], "de": q["anios_observados"], "unidad": "anios",
         "meses": list(q["meses_con_quema"]),
         "periodo": q["periodo"], "fuente_ids": ["firms_viirs"], "motivo_gris": None},
        {"id": "canicula", "estado": None, "valor": can["anios_racha_larga"], "de": can["anios_total"], "unidad": "anios",
         "periodo": cl["periodo"], "fuente_ids": _fuentes_canicula(cl), "motivo_gris": None},
    ]


def bloque(res: dict) -> dict:
    """Bloque `farmer` a partir del JSON ya armado por motor.recomendar.recomendar()."""
    rots = res["rotaciones"]
    actual = next(r for r in rots if r["es_actual"])
    return {
        "version": VERSION,
        "umbrales": {"estado": "pendiente", "documento": DOCUMENTO_UMBRALES},
        "hechos": _hechos(res),
        "opciones": {
            "estado": "pendiente",
            "actual": actual["id"],
            "alternativas": [r["id"] for r in rots if not r["es_actual"]],
            "confianza": {"nivel": actual["confianza"]["nivel"], "motivo": actual["confianza"]["motivo"]},
        },
        "frases": [],
        "audio": {lang: None for lang in IDIOMAS},
    }
