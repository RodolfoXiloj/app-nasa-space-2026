"""Recorte de imagen de alta resolución alrededor de un punto, para revisar a ojo el píxel MODIS.

Fuente: Sentinel-2 cloudless 2021 de EOX (10 m), https://s2maps.eu
  «Sentinel-2 cloudless - https://s2maps.eu by EOX IT Services GmbH (Contains modified Copernicus
  Sentinel data 2021)». Licencia CC BY-NC-SA 4.0: uso no comercial con atribución.
Se dibuja el cuadro de 250 m del píxel MODIS (aprox.) y una cruz en el punto.

    MILPA_ONLINE=1 python -m pipeline.imagen_punto 14.81146 -89.39433 salida.png
"""
from __future__ import annotations

import argparse
import io
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

from pipeline import cache

URL = "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2021_3857/default/g/{z}/{y}/{x}.jpg"
ATRIBUCION = "Sentinel-2 cloudless 2021 (EOX, s2maps.eu; Copernicus Sentinel data 2021), CC BY-NC-SA 4.0"


def _xy(lat: float, lon: float, z: int) -> tuple[float, float]:
    n = 2 ** z
    x = (lon + 180) / 360 * n
    y = (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n
    return x, y


def recorte(lat: float, lon: float, salida: Path, z: int = 15, radio_tiles: int = 1, etiqueta: str = "") -> Path:
    x, y = _xy(lat, lon, z)
    tx, ty = int(x), int(y)
    tam = 256
    lado = 2 * radio_tiles + 1
    img = Image.new("RGB", (lado * tam, lado * tam))
    for dy in range(-radio_tiles, radio_tiles + 1):
        for dx in range(-radio_tiles, radio_tiles + 1):
            r = cache.get(URL.format(z=z, x=tx + dx, y=ty + dy), timeout=60)
            img.paste(Image.open(io.BytesIO(r.content)).convert("RGB"), ((dx + radio_tiles) * tam, (dy + radio_tiles) * tam))
    px = (x - tx + radio_tiles) * tam
    py = (y - ty + radio_tiles) * tam
    m_por_px = 156543.03392 * math.cos(math.radians(lat)) / 2 ** z
    medio = 125 / m_por_px
    d = ImageDraw.Draw(img)
    d.rectangle([px - medio, py - medio, px + medio, py + medio], outline=(255, 230, 0), width=2)
    d.line([px - 6, py, px + 6, py], fill=(255, 0, 0), width=2)
    d.line([px, py - 6, px, py + 6], fill=(255, 0, 0), width=2)
    d.rectangle([0, img.height - 16, img.width, img.height], fill=(0, 0, 0))
    d.text((4, img.height - 14), f"{etiqueta} {lat},{lon} | cuadro amarillo = 250 m | {ATRIBUCION}"[:150], fill=(255, 255, 255))
    salida.parent.mkdir(parents=True, exist_ok=True)
    img.save(salida)
    return salida


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("lat", type=float)
    ap.add_argument("lon", type=float)
    ap.add_argument("salida", type=Path)
    ap.add_argument("--z", type=int, default=15)
    ap.add_argument("--etiqueta", default="")
    a = ap.parse_args()
    try:
        print(recorte(a.lat, a.lon, a.salida, a.z, etiqueta=a.etiqueta))
    except cache.SinRed as e:
        sys.exit(str(e))
