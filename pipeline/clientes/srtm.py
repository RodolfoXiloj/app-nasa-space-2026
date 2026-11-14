"""Altitud y pendiente con SRTM 90 m vía OpenTopoData (sin cuenta, 1 petición por segundo).

Docs: https://www.opentopodata.org/datasets/srtm/
Pendiente: diferencias centradas con 4 puntos a ~0.001° (unos 110 m) del centro.
"""
from __future__ import annotations

import argparse
import math
import sys

from pipeline import cache

URL = "https://api.opentopodata.org/v1/srtm90m"
PASO = 0.001


def descargar(pid: str) -> dict:
    p = cache.parcela(pid)
    lat, lon = p["lat"], p["lon"]
    puntos = [(lat, lon), (lat + PASO, lon), (lat - PASO, lon), (lat, lon + PASO), (lat, lon - PASO)]
    r = cache.get(URL, params={"locations": "|".join(f"{a},{b}" for a, b in puntos)}, timeout=60)
    elev = [x["elevation"] for x in r.json()["results"]]
    c, n, s, e, o = elev
    dy = 2 * PASO * 110_574.0
    dx = 2 * PASO * 111_320.0 * math.cos(math.radians(lat))
    pend = None
    if None not in (n, s, e, o):
        pend = round(100 * math.hypot((e - o) / dx, (n - s) / dy), 1)
    datos = {"altitud_m": c, "pendiente_pct": pend, "puntos": [list(pt) + [z] for pt, z in zip(puntos, elev)],
             "resolucion": "90 m", "metodo": "diferencias centradas con 4 vecinos a 0.001°"}
    proc = cache.procedencia(url=r.url, producto="SRTM 90 m vía OpenTopoData (srtm90m)", version=None,
                             nota="TODO: confirmar versión exacta del dataset srtm90m en opentopodata.org")
    ruta = cache.guardar(cache.CACHE / "srtm" / f"{pid}.json", datos, proc)
    print(f"[srtm {pid}] altitud {c} m, pendiente {pend} % -> {ruta}")
    return {"procedencia": proc, "datos": datos}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("parcela")
    a = ap.parse_args()
    try:
        descargar(a.parcela)
    except cache.SinRed as e:
        sys.exit(str(e))
