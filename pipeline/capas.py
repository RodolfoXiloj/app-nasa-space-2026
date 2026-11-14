"""Teselas de respaldo del mapa (plan: «PNG guardados por parcela como respaldo»).

Baja de NASA GIBS (WMTS, sin clave) las teselas de la zona de las parcelas para que el mapa
muestre color real y NDVI aunque no haya internet en la demo. Se guardan en
web/public/capas/{capa}/{z}/{x}/{y}.{ext} (unos cientos de KB).
No se bajan teselas de OpenStreetMap: su política prohíbe la descarga masiva.

    MILPA_ONLINE=1 python -m pipeline.capas
"""
from __future__ import annotations

import json
import math
import sys

from pipeline import cache

GIBS = "https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/{capa}/default/{fecha}/GoogleMapsCompatible_Level{nivel}/{z}/{y}/{x}.{ext}"
CAPAS = {
    "color_real_seca": ("MODIS_Terra_CorrectedReflectance_TrueColor", "2026-03-15", "jpg", 9),
    "ndvi_seca": ("MODIS_Terra_L3_NDVI_16Day", "2026-03-22", "png", 9),
    "ndvi_lluvia": ("MODIS_Terra_L3_NDVI_16Day", "2026-09-14", "png", 9),
}
ZOOMS = range(7, 10)
DESTINO = cache.RAIZ / "web" / "public" / "capas"


def tesela(lat: float, lon: float, z: int) -> tuple[int, int]:
    n = 2 ** z
    return int((lon + 180) / 360 * n), int((1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n)


def bajar(margen: float = 0.08) -> dict:
    ps = cache.cargar_parcelas()
    oeste, este = min(p["lon"] for p in ps) - margen, max(p["lon"] for p in ps) + margen
    sur, norte = min(p["lat"] for p in ps) - margen, max(p["lat"] for p in ps) + margen
    total = 0
    for nombre, (capa, fecha, ext, nivel) in CAPAS.items():
        for z in ZOOMS:
            x0, y0 = tesela(norte, oeste, z)
            x1, y1 = tesela(sur, este, z)
            for x in range(x0, x1 + 1):
                for y in range(y0, y1 + 1):
                    ruta = DESTINO / nombre / str(z) / str(x) / f"{y}.{ext}"
                    if ruta.exists():
                        continue
                    r = cache.get(GIBS.format(capa=capa, fecha=fecha, nivel=nivel, z=z, x=x, y=y, ext=ext), timeout=60)
                    ruta.parent.mkdir(parents=True, exist_ok=True)
                    ruta.write_bytes(r.content)
                    total += 1
    info = {"capas": {k: {"capa_gibs": v[0], "fecha": v[1], "formato": v[2]} for k, v in CAPAS.items()},
            "zooms": list(ZOOMS), "caja": [round(oeste, 3), round(sur, 3), round(este, 3), round(norte, 3)],
            "fuente": "NASA GIBS (WMTS EPSG:3857)", "fecha_descarga": cache.ahora_utc()}
    (DESTINO / "capas.json").write_text(json.dumps(info, ensure_ascii=False), encoding="utf-8")
    print(f"[capas] {total} teselas nuevas en {DESTINO}")
    return info


if __name__ == "__main__":
    try:
        bajar()
    except cache.SinRed as e:
        sys.exit(str(e))
