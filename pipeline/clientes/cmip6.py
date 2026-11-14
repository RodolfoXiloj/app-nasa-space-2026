"""NASA NEX-GDDP-CMIP6: cambios proyectados por cada modelo para las 5 parcelas.

El cálculo pesado lo hace Earth Engine (pipeline/gee/cmip6_cambios.js), porque el conjunto pesa
38 TB. Este cliente solo convierte el CSV que exporta Earth Engine en la caché del repo, con su
procedencia, igual que los demás clientes.

    python -m pipeline.clientes.cmip6 ruta/a/milpa_cmip6_cambios.csv

Para cada parcela, escenario (SSP2-4.5, SSP5-8.5) y modelo guarda:
    lluvia_pct           cambio % de la lluvia media de mayo a octubre, 2041-2060 contra 1995-2014
    lluvia_canicula_pct  igual, solo junio a agosto
    temp_c               cambio de la temperatura media de mayo a octubre (°C)

Es el método delta: cada modelo se compara contra su propio pasado, así su sesgo se cancela.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

from motor import datos
from pipeline import cache

SALIDA = datos.CACHE / "cmip6" / "cambios.json"
ESCENARIOS = ("ssp245", "ssp585")


def convertir(ruta_csv: str | Path) -> dict:
    filas: dict[tuple[str, str, str], dict] = {}
    with open(ruta_csv, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            filas[(r["parcela"], r["modelo"], r["escenario"])] = {
                "pr": float(r["pr_may_oct_mm_dia"]), "pr_can": float(r["pr_jun_ago_mm_dia"]), "tas": float(r["tas_may_oct_c"])}

    parcelas: dict[str, dict] = {}
    for (pid, modelo, esc), fut in filas.items():
        if esc not in ESCENARIOS:
            continue
        hist = filas.get((pid, modelo, "historical"))
        if not hist or hist["pr"] <= 0 or hist["pr_can"] <= 0:
            continue
        parcelas.setdefault(pid, {}).setdefault(esc, []).append({
            "modelo": modelo,
            "lluvia_pct": round(100 * (fut["pr"] / hist["pr"] - 1), 1),
            "lluvia_canicula_pct": round(100 * (fut["pr_can"] / hist["pr_can"] - 1), 1),
            "temp_c": round(fut["tas"] - hist["tas"], 2),
        })
    for esc_d in parcelas.values():
        for lista in esc_d.values():
            lista.sort(key=lambda m: m["modelo"])

    proc = cache.procedencia(
        "https://developers.google.com/earth-engine/datasets/catalog/NASA_GDDP-CMIP6",
        "NASA Earth Exchange Global Daily Downscaled Projections (NEX-GDDP-CMIP6), 0.25°, vía Google Earth Engine",
        version="NASA/GDDP-CMIP6",
        nota="Medias de mayo-octubre y junio-agosto, 2041-2060 contra 1995-2014, por modelo (método delta). "
             "Precalculado sin conexión con pipeline/gee/cmip6_cambios.js; nada llama a Earth Engine en vivo. "
             "HadGEM3-GC31-MM no tiene SSP2-4.5 en el conjunto.",
    )
    return {"procedencia": proc,
            "datos": {"periodo_base": "1995-2014", "periodo_futuro": "2041-2060", "parcelas": parcelas}}


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(__doc__)
        return 1
    obj = convertir(argv[0])
    cache.guardar(SALIDA, obj["datos"], obj["procedencia"])
    n = {pid: {e: len(v) for e, v in d.items()} for pid, d in obj["datos"]["parcelas"].items()}
    print(f"Escrito {SALIDA}: modelos por parcela y escenario {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
