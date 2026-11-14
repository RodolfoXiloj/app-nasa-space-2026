"""NASA POWER (comunidad AG), punto de la parcela. Sin cuenta.

Docs: https://power.larc.nasa.gov/docs/services/api/
- Mensual: /api/temporal/monthly/point  (claves AAAAMM; AAAA13 = anual)
- Diario:  /api/temporal/daily/point    (claves AAAAMMDD)
Valor -999 = sin dato.

Variables:
  PRECTOTCORR  lluvia corregida (mm/día)
  T2M_MAX, T2M_MIN, T2M  temperatura a 2 m (°C)
  GWETROOT     humedad de la zona de raíces (0-1), modelo MERRA-2 (no es SMAP)

Límite que se declara en la tarjeta: celda de unos 50 km (0.5° x 0.625°).
"""
from __future__ import annotations

import argparse
import sys

from pipeline import cache

BASE = "https://power.larc.nasa.gov/api/temporal"
PARAMS = ["PRECTOTCORR", "T2M_MAX", "T2M_MIN", "T2M", "GWETROOT"]


def _a_filas(param_dict: dict[str, dict[str, float]]) -> tuple[list[str], list[list]]:
    claves = sorted(next(iter(param_dict.values())).keys())
    filas = []
    for k in claves:
        fila: list = [k]
        for p in PARAMS:
            v = param_dict.get(p, {}).get(k)
            fila.append(None if v is None or v <= -999 else v)
        filas.append(fila)
    return ["clave"] + PARAMS, filas


def descargar(pid: str, frecuencia: str, inicio: int = 1991, fin: int = 2025) -> dict:
    p = cache.parcela(pid)
    if frecuencia == "mensual":
        url = f"{BASE}/monthly/point"
        start, end = str(inicio), str(fin)
    elif frecuencia == "diario":
        url = f"{BASE}/daily/point"
        start, end = f"{inicio}0101", f"{fin}1231"
    else:
        raise ValueError(frecuencia)
    params = {"parameters": ",".join(PARAMS), "community": "AG", "longitude": p["lon"], "latitude": p["lat"],
              "start": start, "end": end, "format": "JSON"}
    r = cache.get(url, params=params, timeout=300)
    j = r.json()
    columnas, filas = _a_filas(j["properties"]["parameter"])
    datos = {"columnas": columnas, "filas": filas, "unidades": {
        "PRECTOTCORR": "mm/día", "T2M_MAX": "°C", "T2M_MIN": "°C", "T2M": "°C", "GWETROOT": "fracción 0-1"},
        "lat": p["lat"], "lon": p["lon"], "resolucion": "0.5° x 0.625° (~50 km)",
        "elevacion_celda_m": j.get("geometry", {}).get("coordinates", [None, None, None])[2]}
    version = (j.get("header") or {}).get("api", {}).get("version") if isinstance(j.get("header"), dict) else None
    proc = cache.procedencia(url=r.url, producto=f"NASA POWER {frecuencia} (comunidad AG)", version=version,
                             nota="-999 convertido a null; MERRA-2 y GPM/IMERG según la variable")
    ruta = cache.guardar(cache.CACHE / "power" / f"{pid}_{frecuencia}.json", datos, proc)
    print(f"[power {pid}] {frecuencia}: {len(filas)} filas -> {ruta}")
    return {"procedencia": proc, "datos": datos}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("parcela")
    ap.add_argument("--frecuencia", choices=["mensual", "diario", "ambas"], default="ambas")
    a = ap.parse_args()
    try:
        for fr in (["mensual", "diario"] if a.frecuencia == "ambas" else [a.frecuencia]):
            descargar(a.parcela, fr)
    except cache.SinRed as e:
        sys.exit(str(e))
