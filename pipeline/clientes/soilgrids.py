"""SoilGrids 2.0 (ISRIC), 250 m: arcilla, carbono orgánico y pH en el punto. Sin cuenta.

Ruta principal: API REST https://rest.isric.org/soilgrids/v2.0/properties/query
  (el 13 nov 2026 en la mañana no respondía; a las 9:38 volvió, lenta).
Respaldo automático (probado el 13 nov 2026): WCS 2.0.1 de https://maps.isric.org/mapserv
  GetCoverage en EPSG:4326 de una ventanita de ~0.005° alrededor del punto -> GeoTIFF de 2x2
  enteros que se lee con Pillow (sin rasterio). Arcilla 0-5 cm en Jocotán (14.79, -89.37):
  319 g/kg = 31.9 %, igual que la consulta REST del plan original (28 oct).
Si fallan los dos: el motor declara el suelo como vacío de información (no inventa valores).
  El WMS GetFeatureInfo NO sirve: no expone el valor del raster. El WebDAV files.isric.org no
  respondió (timeout).

Factores de conversión de SoilGrids (unidades mapeadas -> convencionales):
  clay: g/kg -> % dividir entre 10 ; soc: dg/kg -> g/kg dividir entre 10 ; phh2o: pH*10 -> pH dividir entre 10
"""
from __future__ import annotations

import argparse
import io
import statistics
import sys

from pipeline import cache

URL = "https://rest.isric.org/soilgrids/v2.0/properties/query"
WCS = "https://maps.isric.org/mapserv"
PROPIEDADES = {"clay": ("arcilla_pct", 10), "soc": ("carbono_organico_g_kg", 10), "phh2o": ("ph", 10)}
PROFUNDIDADES = ["0-5cm", "5-15cm"]
MEDIA_VENTANA = 0.0025


def _por_rest(p: dict) -> tuple[dict, str]:
    params = [("lon", p["lon"]), ("lat", p["lat"]), ("value", "mean")]
    params += [("property", k) for k in PROPIEDADES] + [("depth", d) for d in PROFUNDIDADES]
    r = cache.get(URL, params=params, timeout=90, intentos=2)
    valores: dict[str, dict[str, float | None]] = {}
    for capa in r.json()["properties"]["layers"]:
        nombre, factor = PROPIEDADES[capa["name"]]
        for d in capa["depths"]:
            v = d["values"].get("mean")
            valores.setdefault(d["label"], {})[nombre] = None if v is None else round(v / factor, 2)
    return valores, r.url


def valor_wcs(lat: float, lon: float, propiedad: str, profundidad: str) -> float | None:
    """Mediana de la ventanita de ~2x2 píxeles alrededor del punto, en unidades mapeadas."""
    from PIL import Image

    m = MEDIA_VENTANA
    params = [("map", f"/map/{propiedad}.map"), ("SERVICE", "WCS"), ("VERSION", "2.0.1"), ("REQUEST", "GetCoverage"),
              ("COVERAGEID", f"{propiedad}_{profundidad}_mean"), ("FORMAT", "image/tiff"),
              ("SUBSET", f"X({lon - m},{lon + m})"), ("SUBSET", f"Y({lat - m},{lat + m})"),
              ("SUBSETTINGCRS", "http://www.opengis.net/def/crs/EPSG/0/4326"),
              ("OUTPUTCRS", "http://www.opengis.net/def/crs/EPSG/0/4326")]
    r = cache.get(WCS, params=params, timeout=90, intentos=2)
    im = Image.open(io.BytesIO(r.content))
    vals = [im.getpixel((x, y)) for y in range(im.size[1]) for x in range(im.size[0])]
    vals = [v for v in vals if isinstance(v, (int, float)) and v > 0 and v != 32767]
    return statistics.median(vals) if vals else None


def _por_wcs(p: dict) -> tuple[dict, str]:
    valores: dict[str, dict[str, float | None]] = {}
    for prop, (nombre, factor) in PROPIEDADES.items():
        for d in PROFUNDIDADES:
            v = valor_wcs(p["lat"], p["lon"], prop, d)
            valores.setdefault(d, {})[nombre] = None if v is None else round(v / factor, 2)
    return valores, f"{WCS}?SERVICE=WCS&REQUEST=GetCoverage (EPSG:4326, ventana de {2 * MEDIA_VENTANA}°)"


def descargar(pid: str) -> dict:
    p = cache.parcela(pid)
    via = "REST"
    try:
        valores, url = _por_rest(p)
    except Exception as e:  # noqa: BLE001 - la API REST se cae seguido; se usa el WCS
        print(f"[suelo {pid}] REST falló ({type(e).__name__}); se usa el WCS de maps.isric.org", flush=True)
        valores, url = _por_wcs(p)
        via = "WCS"
    datos = {"por_profundidad": valores, "resolucion": "250 m", "via": via, "lat": p["lat"], "lon": p["lon"]}
    proc = cache.procedencia(url=url, producto="SoilGrids 2.0 (ISRIC)", version="2.0",
                             nota=f"Consulta por {via}" + ("; respaldo porque la API REST no respondió" if via == "WCS" else ""))
    ruta = cache.guardar(cache.CACHE / "suelo" / f"{pid}.json", datos, proc)
    print(f"[suelo {pid}] ({via}) {valores} -> {ruta}")
    return {"procedencia": proc, "datos": datos}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("parcelas", nargs="*")
    ap.add_argument("--wcs", action="store_true", help="forzar el respaldo WCS")
    a = ap.parse_args()
    try:
        for pid in a.parcelas or [q["id"] for q in cache.cargar_parcelas()]:
            if a.wcs:
                q = cache.parcela(pid)
                v, u = _por_wcs(q)
                print(pid, v)
            else:
                descargar(pid)
    except cache.SinRed as e:
        sys.exit(str(e))
