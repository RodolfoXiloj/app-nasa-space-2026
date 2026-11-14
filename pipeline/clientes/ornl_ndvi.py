"""MODIS MOD13Q1 v061 (NDVI 250 m, 16 días) por punto, desde la API de ORNL DAAC. Sin cuenta.

Docs: https://modis.ornl.gov/data/modis_webservice.html
- /MOD13Q1/dates?latitude=&longitude=  -> fechas válidas
- /MOD13Q1/subset?...&band=&startDate=&endDate=&kmAboveBelow=0&kmLeftRight=0
  máximo 10 fechas por petición (verificado el 13 nov 2026 con 10).

Se bajan dos bandas: NDVI (escala 0.0001, relleno -3000) y pixel_reliability
(0 bueno, 1 marginal, 2 nieve/hielo, 3 nube, -1 sin dato).

Los trozos se guardan en data/raw_big/ornl/{parcela}/ (fuera del repo) para poder
reanudar; la serie unida va a data/cache/ndvi/{parcela}.json.
"""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

from pipeline import cache

BASE = "https://modis.ornl.gov/rst/api/v1"
PRODUCTO = "MOD13Q1"
BANDA_NDVI = "250m_16_days_NDVI"
BANDA_CAL = "250m_16_days_pixel_reliability"
POR_PETICION = 10


def fechas(lat: float, lon: float) -> list[dict]:
    r = cache.get(f"{BASE}/{PRODUCTO}/dates", params={"latitude": lat, "longitude": lon},
                  headers={"Accept": "application/json"})
    return r.json()["dates"]


def _trozo(pid: str, lat: float, lon: float, banda: str, ini: str, fin: str) -> list[dict]:
    # La carpeta lleva la coordenada: si se mueve el punto, no se reusan trozos viejos.
    ruta = cache.RAW_BIG / "ornl" / f"{pid}_{lat}_{lon}" / banda / f"{ini}_{fin}.json"
    if ruta.exists():
        return json.loads(ruta.read_text(encoding="utf-8"))
    r = cache.get(f"{BASE}/{PRODUCTO}/subset", headers={"Accept": "application/json"}, timeout=180, params={
        "latitude": lat, "longitude": lon, "band": banda, "startDate": ini, "endDate": fin,
        "kmAboveBelow": 0, "kmLeftRight": 0,
    })
    sub = [{"modis_date": s["modis_date"], "calendar_date": s["calendar_date"], "valor": s["data"][0]}
           for s in r.json()["subset"]]
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(sub), encoding="utf-8")
    return sub


def descargar(pid: str, anio_ini: int = 2001, anio_fin: int = 2025, hilos: int = 2) -> dict:
    p = cache.parcela(pid)
    lat, lon = p["lat"], p["lon"]
    todas = [d for d in fechas(lat, lon) if anio_ini <= int(d["calendar_date"][:4]) <= anio_fin]
    grupos = [todas[i:i + POR_PETICION] for i in range(0, len(todas), POR_PETICION)]
    tareas = [(banda, g[0]["modis_date"], g[-1]["modis_date"]) for banda in (BANDA_NDVI, BANDA_CAL) for g in grupos]

    resultados: dict[str, dict[str, int]] = {BANDA_NDVI: {}, BANDA_CAL: {}}
    hechas = 0
    with ThreadPoolExecutor(max_workers=hilos) as ex:
        futuros = {ex.submit(_trozo, pid, lat, lon, b, i, f): b for b, i, f in tareas}
        for fut in as_completed(futuros):
            banda = futuros[fut]
            for s in fut.result():
                resultados[banda][s["calendar_date"]] = s["valor"]
            hechas += 1
            if hechas % 10 == 0 or hechas == len(tareas):
                print(f"[ndvi {pid}] {hechas}/{len(tareas)} peticiones", flush=True)

    filas = []
    for d in todas:
        f = d["calendar_date"]
        bruto = resultados[BANDA_NDVI].get(f)
        cal = resultados[BANDA_CAL].get(f)
        ndvi = None if bruto is None or bruto <= -2000 else round(bruto * 0.0001, 4)
        filas.append([f, ndvi, cal])

    datos = {"columnas": ["fecha", "ndvi", "pixel_reliability"], "filas": filas,
             "lat": lat, "lon": lon, "resolucion": "250 m", "compuesto": "16 días"}
    proc = cache.procedencia(
        url=f"{BASE}/{PRODUCTO}/subset", producto="MODIS/Terra MOD13Q1 (NDVI 16 días, 250 m)", version="061",
        nota="API de subconjuntos de ORNL DAAC; escala 0.0001 aplicada; relleno -3000 -> null",
        periodo=f"{anio_ini}-{anio_fin}", bandas=[BANDA_NDVI, BANDA_CAL],
    )
    ruta = cache.guardar(cache.CACHE / "ndvi" / f"{pid}.json", datos, proc)
    print(f"[ndvi {pid}] {len(filas)} compuestos -> {ruta}")
    return {"procedencia": proc, "datos": datos}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("parcela")
    ap.add_argument("--desde", type=int, default=2001)
    ap.add_argument("--hasta", type=int, default=2025)
    a = ap.parse_args()
    try:
        descargar(a.parcela, a.desde, a.hasta)
    except cache.SinRed as e:
        sys.exit(str(e))
