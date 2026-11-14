"""Propone un píxel agrícola cerca de cada parcela usando la amplitud estacional del NDVI.

Motivo: el punto del plan original en Jocotán (14.79, -89.37) tiene NDVI mediano >= 0.59 todo el
año (13 nov 2026): parece bosque o matorral, no milpa, y no se ven meses de suelo desnudo.

Método (filtro rápido, NO reemplaza mirar imagen de alta resolución):
- Ventana de +-3 km alrededor del punto, MOD13Q1 por ORNL (una petición trae todos los píxeles).
- Época seca: compuestos que empiezan entre el 6 de marzo y el 23 de abril (días 065-113).
  Época de lluvia: compuestos que empiezan entre el 29 de agosto y el 16 de octubre (días 241-289).
- Años 2022-2024. Solo compuestos con pixel_reliability 0 o 1.
- Un píxel "parece milpa" si NDVI seco < 0.35, NDVI lluvioso >= 0.60 y la diferencia >= 0.30.
- Se exige que al menos 6 de sus 9 vecinos (3x3) también lo cumplan: zona homogénea.
- Se elige el que cumple más cerca del punto original.

Salida: data/cache/puntos/{parcela}.json con el candidato elegido y el resumen. No modifica
data/parcelas.yaml: eso se hace a mano después de revisar (TODO Mario: confirmar con imagen).
"""
from __future__ import annotations

import argparse
import json
import math
import statistics
import sys

from pipeline import cache
from pipeline.clientes.firms import distancia_m

BASE = "https://modis.ornl.gov/rst/api/v1/MOD13Q1/subset"
R_SIN = 6371007.181
KM = 3
ANIOS = (2022, 2023, 2024)
SECA = ("065", "113")
LLUVIA = ("241", "289")
CRIT = {"seco_max": 0.35, "lluvia_min": 0.60, "amplitud_min": 0.30, "vecinos_min": 6}


def _pedir(lat, lon, banda, ini, fin, km=KM):
    ruta = cache.RAW_BIG / "ornl_area" / f"{lat}_{lon}_{km}" / f"{banda}_{ini}_{fin}.json"
    if ruta.exists():
        return json.loads(ruta.read_text(encoding="utf-8"))
    r = cache.get(BASE, headers={"Accept": "application/json"}, timeout=300, params={
        "latitude": lat, "longitude": lon, "band": banda, "startDate": ini, "endDate": fin,
        "kmAboveBelow": km, "kmLeftRight": km})
    j = r.json()
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(j), encoding="utf-8")
    return j


def _centro(j, i, k):
    """Centro geográfico del píxel en fila i, columna k (fila 0 = norte)."""
    cs = float(j["cellsize"])
    x = float(j["xllcorner"]) + (k + 0.5) * cs
    y = float(j["yllcorner"]) + (int(j["nrows"]) - i - 0.5) * cs
    lat = math.degrees(y / R_SIN)
    lon = math.degrees(x / (R_SIN * math.cos(math.radians(lat))))
    return round(lat, 5), round(lon, 5)


def evaluar(pid: str, km: int = KM, crit: dict | None = None, sufijo: str = "") -> dict:
    c = dict(CRIT, **(crit or {}))
    p = cache.parcela(pid)
    lat0, lon0 = p.get("punto_original", {}).get("lat", p["lat"]), p.get("punto_original", {}).get("lon", p["lon"])
    seco: dict[int, list[float]] = {}
    lluvia: dict[int, list[float]] = {}
    ref = None
    for anio in ANIOS:
        for (ini, fin), destino in ((SECA, seco), (LLUVIA, lluvia)):
            a, b = f"A{anio}{ini}", f"A{anio}{fin}"
            nd = _pedir(lat0, lon0, "250m_16_days_NDVI", a, b, km)
            ca = _pedir(lat0, lon0, "250m_16_days_pixel_reliability", a, b, km)
            ref = nd
            cal = {s["calendar_date"]: s["data"] for s in ca["subset"]}
            for s in nd["subset"]:
                rel = cal.get(s["calendar_date"])
                for idx, v in enumerate(s["data"]):
                    if rel is None or rel[idx] not in (0, 1) or v <= -2000:
                        continue
                    destino.setdefault(idx, []).append(v * 0.0001)
    assert ref is not None
    nrows, ncols = int(ref["nrows"]), int(ref["ncols"])

    def ok(idx):
        s, l = seco.get(idx), lluvia.get(idx)
        if not s or not l or len(s) < 4 or len(l) < 4:
            return None
        ms, ml = statistics.median(s), statistics.median(l)
        return (ms < c["seco_max"] and ml >= c["lluvia_min"] and ml - ms >= c["amplitud_min"]), ms, ml

    candidatos = []
    centro_idx = None
    mejor_d = 1e18
    for i in range(nrows):
        for k in range(ncols):
            idx = i * ncols + k
            la, lo = _centro(ref, i, k)
            d = distancia_m(lat0, lon0, la, lo)
            if d < mejor_d:
                mejor_d, centro_idx = d, idx
            r = ok(idx)
            if not r or not r[0]:
                continue
            vecinos = sum(1 for di in (-1, 0, 1) for dk in (-1, 0, 1)
                          if 0 <= i + di < nrows and 0 <= k + dk < ncols
                          and (ok((i + di) * ncols + k + dk) or (False,))[0])
            if vecinos >= c["vecinos_min"]:
                candidatos.append({"lat": la, "lon": lo, "distancia_m": round(d), "ndvi_seco": round(r[1], 3),
                                   "ndvi_lluvia": round(r[2], 3), "vecinos_ok": vecinos})
    candidatos.sort(key=lambda c: c["distancia_m"])
    r0 = ok(centro_idx) if centro_idx is not None else None
    salida = {
        "punto_original": {"lat": lat0, "lon": lon0,
                           "ndvi_seco": round(r0[1], 3) if r0 else None, "ndvi_lluvia": round(r0[2], 3) if r0 else None,
                           "parece_milpa": bool(r0 and r0[0])},
        "criterios": c, "anios": list(ANIOS), "ventana_km": km, "pixeles": nrows * ncols,
        "candidatos": candidatos[:60], "elegido": candidatos[0] if candidatos else None,
        "nota": "Filtro por amplitud estacional de NDVI; confirmar con imagen de alta resolución antes de usar.",
    }
    proc = cache.procedencia(url=BASE, producto=f"MODIS/Terra MOD13Q1 (ventana de +-{km} km)", version="061")
    nombre = (f"{pid}.json" if km == KM else f"{pid}_km{km}.json").replace(".json", f"{sufijo}.json")
    cache.guardar(cache.CACHE / "puntos" / nombre, salida, proc)
    print(f"[punto {pid}] original seco/lluvia = {salida['punto_original']['ndvi_seco']}/"
          f"{salida['punto_original']['ndvi_lluvia']}; {len(candidatos)} candidatos; elegido = {salida['elegido']}", flush=True)
    return salida


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("parcelas", nargs="*")
    ap.add_argument("--km", type=int, default=KM, help="media ventana en km (por defecto 3)")
    ap.add_argument("--seco-max", type=float, default=CRIT["seco_max"])
    ap.add_argument("--amplitud-min", type=float, default=CRIT["amplitud_min"])
    a = ap.parse_args()
    crit = {"seco_max": a.seco_max, "amplitud_min": a.amplitud_min}
    sufijo = "" if crit == {k: CRIT[k] for k in crit} else f"_seco{a.seco_max}_amp{a.amplitud_min}"
    try:
        for pid in a.parcelas or [p["id"] for p in cache.cargar_parcelas()]:
            evaluar(pid, a.km, crit, sufijo)
    except cache.SinRed as e:
        sys.exit(str(e))
