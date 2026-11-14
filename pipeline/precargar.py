"""Precarga de la caché para las parcelas de data/parcelas.yaml. Exige MILPA_ONLINE=1.

    MILPA_ONLINE=1 python -m pipeline.precargar                        # todo, todas las parcelas
    MILPA_ONLINE=1 python -m pipeline.precargar jocotan --fuentes power,srtm
    MILPA_ONLINE=1 python -m pipeline.precargar --ndvi-desde 2019      # NDVI corto (rápido)

Fuentes: power (mensual y diario), srtm, firms, suelo (SoilGrids), ndvi (ORNL, lento:
~13 s por petición; la serie 2001-2025 son 116 peticiones por parcela, unos 15 min con 2 hilos).
Cada fuente falla por separado: un error se reporta y la precarga sigue con lo demás.
Las descargas son reanudables (trozos en data/raw_big/).
"""
from __future__ import annotations

import argparse
import sys
import traceback

from pipeline import cache
from pipeline.clientes import firms, ornl_ndvi, power, soilgrids, srtm

TODAS = ["power", "srtm", "firms", "suelo", "ndvi"]


def precargar(pids: list[str], fuentes: list[str], ndvi_desde: int = 2001, ndvi_hasta: int = 2025) -> list[str]:
    cache.exigir_red()
    errores = []
    for pid in pids:
        for f in fuentes:
            try:
                if f == "power":
                    power.descargar(pid, "mensual")
                    power.descargar(pid, "diario", inicio=1991)
                elif f == "srtm":
                    srtm.descargar(pid)
                elif f == "firms":
                    firms.recortar(pid)
                elif f == "suelo":
                    soilgrids.descargar(pid)
                elif f == "ndvi":
                    ornl_ndvi.descargar(pid, ndvi_desde, ndvi_hasta)
                else:
                    raise ValueError(f"Fuente desconocida: {f}")
            except Exception as e:  # noqa: BLE001 - se reporta y se sigue
                msg = f"[{f} {pid}] FALLÓ: {type(e).__name__}: {e}"
                print(msg, file=sys.stderr, flush=True)
                traceback.print_exc(limit=1)
                errores.append(msg)
    return errores


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("parcelas", nargs="*")
    ap.add_argument("--fuentes", default=",".join(TODAS))
    ap.add_argument("--ndvi-desde", type=int, default=2001)
    ap.add_argument("--ndvi-hasta", type=int, default=2025)
    a = ap.parse_args()
    try:
        pids = a.parcelas or [p["id"] for p in cache.cargar_parcelas()]
        errs = precargar(pids, a.fuentes.split(","), a.ndvi_desde, a.ndvi_hasta)
    except cache.SinRed as e:
        sys.exit(str(e))
    print(f"\nPrecarga terminada con {len(errs)} errores.")
    for e in errs:
        print("  -", e)
