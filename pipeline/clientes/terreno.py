"""Relieve de la zona de las parcelas, para el mapa de Evidence: sombreado (Leaflet) y vista 3D (MapLibre).

    MILPA_ONLINE=1 python -m pipeline.clientes.terreno

Baja teselas Terrarium de AWS Terrain Tiles (Tilezen/Mapzen, Open Data, sin clave) para la caja de las 5
parcelas y los zooms 8 a 11 (el 11 tiene unos 74 m por píxel a esta latitud); más arriba MapLibre las estira,
para que el sitio pese poco. Según la documentación de Tilezen (docs/data-sources.md), en tierra y desde el
zoom 7 la fuente es SRTM; cada tesela lo confirma en la cabecera x-amz-meta-x-imagery-sources
(aquí: srtm/N14W090.tif), que se guarda en terreno.json. Crédito que piden: «SRTM data courtesy of the U.S.
Geological Survey» y Mapzen. Altura en metros = R*256 + G + B/256 - 32768.

Guarda:
- web/public/terreno/{z}/{x}/{y}.png: las teselas tal cual (vista 3D).
- web/public/capas/relieve/{z}/{x}/{y}.png: sombreado calculado aquí (sol al noroeste, 45°), gris con
  transparencia, para ponerlo sobre el mapa de Leaflet sin WebGL.
- web/public/terreno/terreno.json: procedencia (URL, fecha de descarga, zooms, caja, fuente de los datos).
Sin red, el sitio sigue funcionando: si faltan las teselas, Evidence no ofrece el relieve.
"""
from __future__ import annotations

import io
import json
import math
import sys

from PIL import Image

from pipeline import cache

URL = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"
ZOOMS = range(8, 12)
TERRENO = cache.RAIZ / "web" / "public" / "terreno"
RELIEVE = cache.RAIZ / "web" / "public" / "capas" / "relieve"
CIRCUNF = 40075016.686
AZIMUT, ALTURA_SOL = 315.0, 45.0


def tesela(lat: float, lon: float, z: int) -> tuple[int, int]:
    n = 2 ** z
    return int((lon + 180) / 360 * n), int((1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n)


def lat_de(y: float, z: int) -> float:
    return math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / 2 ** z))))


def alturas(png: bytes) -> list[list[float]]:
    im = Image.open(io.BytesIO(png)).convert("RGB")
    w, h = im.size
    px = im.load()
    return [[px[i, j][0] * 256 + px[i, j][1] + px[i, j][2] / 256 - 32768 for i in range(w)] for j in range(h)]


def sombreado(z_m: list[list[float]], metros_px: float) -> Image.Image:
    """Sombreado clásico (Horn simplificado, diferencias centrales). Devuelve RGBA: sombra negra con alfa."""
    h, w = len(z_m), len(z_m[0])
    zen = math.radians(90 - ALTURA_SOL)
    azi = math.radians(360 - AZIMUT + 90)
    out = Image.new("RGBA", (w, h))
    px = out.load()
    for j in range(h):
        fa, fb = z_m[max(0, j - 1)], z_m[min(h - 1, j + 1)]
        f = z_m[j]
        for i in range(w):
            dzdx = (f[min(w - 1, i + 1)] - f[max(0, i - 1)]) / (2 * metros_px)
            dzdy = (fb[i] - fa[i]) / (2 * metros_px)
            pend = math.atan(math.hypot(dzdx, dzdy))
            asp = math.atan2(dzdy, -dzdx)
            luz = math.cos(zen) * math.cos(pend) + math.sin(zen) * math.sin(pend) * math.cos(azi - asp)
            luz = max(0.0, min(1.0, luz))
            # Solo sombra: lo iluminado queda transparente y la ladera en sombra se oscurece.
            sombra = max(0.0, math.cos(zen) - luz) / math.cos(zen)
            px[i, j] = (20, 24, 18, int(round(200 * sombra)))
    return out


def bajar(margen: float = 0.08) -> dict:
    ps = cache.cargar_parcelas()
    oeste, este = min(p["lon"] for p in ps) - margen, max(p["lon"] for p in ps) + margen
    sur, norte = min(p["lat"] for p in ps) - margen, max(p["lat"] for p in ps) + margen
    nuevas = 0
    for z in ZOOMS:
        x0, y0 = tesela(norte, oeste, z)
        x1, y1 = tesela(sur, este, z)
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                ruta = TERRENO / str(z) / str(x) / f"{y}.png"
                if not ruta.exists():
                    r = cache.get(URL.format(z=z, x=x, y=y), timeout=60)
                    ruta.parent.mkdir(parents=True, exist_ok=True)
                    ruta.write_bytes(r.content)
                    nuevas += 1
                sombra = RELIEVE / str(z) / str(x) / f"{y}.png"
                if not sombra.exists():
                    lat = lat_de(y + 0.5, z)
                    metros_px = CIRCUNF * math.cos(math.radians(lat)) / (256 * 2 ** z)
                    sombra.parent.mkdir(parents=True, exist_ok=True)
                    sombreado(alturas(ruta.read_bytes()), metros_px).save(sombra, optimize=True)
    # Fuente declarada por una tesela del zoom mayor (cabecera de S3).
    zm = max(ZOOMS)
    xm, ym = tesela((sur + norte) / 2, (oeste + este) / 2, zm)
    fuentes = None
    try:
        r = cache.get(URL.format(z=zm, x=xm, y=ym), timeout=60)
        fuentes = r.headers.get("x-amz-meta-x-imagery-sources")
    except Exception:  # noqa: BLE001 - sin cabecera, se deja la anterior
        pass
    previo = {}
    if (TERRENO / "terreno.json").exists():
        previo = json.loads((TERRENO / "terreno.json").read_text(encoding="utf-8"))
    info = {
        "url": URL, "codificacion": "terrarium", "zooms": list(ZOOMS),
        "caja": [round(oeste, 3), round(sur, 3), round(este, 3), round(norte, 3)],
        "fecha_descarga": cache.ahora_utc() if nuevas or not previo else previo.get("fecha_descarga"),
        "producto": "AWS Terrain Tiles (Tilezen/Mapzen), formato Terrarium",
        "fuente_datos": fuentes or previo.get("fuente_datos"),
        "credito": "SRTM data courtesy of the U.S. Geological Survey; Terrain Tiles by Mapzen (AWS Open Data)",
        "sombreado": {"azimut": AZIMUT, "altura_sol": ALTURA_SOL, "ruta": "capas/relieve/{z}/{x}/{y}.png"},
    }
    (TERRENO / "terreno.json").write_text(json.dumps(info, ensure_ascii=False), encoding="utf-8")
    print(f"[terreno] {nuevas} teselas nuevas; sombreado en {RELIEVE}")
    return info


if __name__ == "__main__":
    try:
        bajar()
    except cache.SinRed as e:
        sys.exit(str(e))
