"""Relieve de la zona de las parcelas, para el mapa de Evidence: sombreado (Leaflet) y vista 3D (MapLibre).

    MILPA_ONLINE=1 python -m pipeline.clientes.terreno     # baja lo que falte; sin red, rehace lo demás

Baja teselas Terrarium de AWS Terrain Tiles (Tilezen/Mapzen, Open Data, sin clave) para la caja de las 5
parcelas y los zooms 8 a 11 (el 11 tiene unos 74 m por píxel a esta latitud); más arriba MapLibre las estira,
para que el sitio pese poco. Según la documentación de Tilezen (docs/data-sources.md), en tierra y desde el
zoom 7 la fuente es SRTM; cada tesela lo confirma en la cabecera x-amz-meta-x-imagery-sources
(aquí: srtm/N14W090.tif), que se guarda en la procedencia. Crédito que piden: «SRTM data courtesy of the U.S.
Geological Survey» y Mapzen. En Terrarium, altura en metros = R*256 + G + B/256 - 32768.

Guarda:
- data/cache/terreno/{z}/{x}/{y}.png: las teselas Terrarium tal cual, con procedencia.json (la caché).
- web/public/relieve3d/{z}/{x}/{y}.png: las mismas alturas recodificadas para la vista 3D, ver abajo.
- web/public/capas/relieve/{z}/{x}/{y}.png: sombreado calculado aquí (sol al noroeste, 45°), gris con
  transparencia, para ponerlo sobre el mapa de Leaflet sin WebGL.
- web/public/relieve3d/relieve3d.json: procedencia y codificación.

**Por qué se recodifica.** MapLibre lee la altura de los píxeles de la imagen. Algunos navegadores de teléfono
alteran un poco los píxeles al leerlos (ruido «anti huella digital» en el canvas) y, si su ruta alterna
(VideoFrame) no funciona, MapLibre usa esos píxeles alterados. En Terrarium, una unidad de rojo son 256 m: un
error de ±1 hace picos de cientos de metros (lo vio Rodolfo en su Android el 14 nov 2026). Aquí cada canal lleva
un tercio de la altura en pasos de 4 m: altura = (R + G + B) × 4 m. Un error de ±1 en un canal es de 4 m. El
rango va de 0 a 3060 m (más de lo que hay en la caja); la resolución, 4 m (el error de redondeo, hasta 2 m).
Sin red, el sitio sigue funcionando: si faltan las teselas, Evidence no ofrece el relieve.
"""
from __future__ import annotations

import io
import json
import math
import shutil
import sys

from PIL import Image

from pipeline import cache

URL = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"
ZOOMS = range(8, 12)
CACHE = cache.RAIZ / "data" / "cache" / "terreno"
DESTINO = cache.RAIZ / "web" / "public" / "relieve3d"
RELIEVE = cache.RAIZ / "web" / "public" / "capas" / "relieve"
VIEJO = cache.RAIZ / "web" / "public" / "terreno"  # donde estaban las Terrarium antes del 14 nov 2026, 22:50
CIRCUNF = 40075016.686
AZIMUT, ALTURA_SOL = 315.0, 45.0
PASO_M = 4.0
MAXIMO = 3 * 255


def tesela(lat: float, lon: float, z: int) -> tuple[int, int]:
    n = 2 ** z
    return int((lon + 180) / 360 * n), int((1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n)


def lat_de(y: float, z: int) -> float:
    return math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / 2 ** z))))


def alturas(png: bytes) -> list[list[float]]:
    """Alturas en metros de una tesela Terrarium."""
    im = Image.open(io.BytesIO(png)).convert("RGB")
    w, h = im.size
    px = im.load()
    return [[px[i, j][0] * 256 + px[i, j][1] + px[i, j][2] / 256 - 32768 for i in range(w)] for j in range(h)]


def canales(altura_m: float) -> tuple[int, int, int]:
    """Altura -> (R, G, B) con R + G + B = altura / 4 m redondeada; los tres canales difieren a lo más en 1."""
    v = min(MAXIMO, max(0, round(altura_m / PASO_M)))
    q, r = divmod(v, 3)
    return q + (1 if r >= 1 else 0), q + (1 if r >= 2 else 0), q


def decodificar(rgb: tuple[int, int, int]) -> float:
    return (rgb[0] + rgb[1] + rgb[2]) * PASO_M


def recodificar(z_m: list[list[float]]) -> Image.Image:
    h, w = len(z_m), len(z_m[0])
    im = Image.new("RGB", (w, h))
    im.putdata([canales(z_m[j][i]) for j in range(h) for i in range(w)])
    return im


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


def _leer_json(ruta) -> dict:
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {}


def bajar(margen: float = 0.08) -> dict:
    ps = cache.cargar_parcelas()
    oeste, este = min(p["lon"] for p in ps) - margen, max(p["lon"] for p in ps) + margen
    sur, norte = min(p["lat"] for p in ps) - margen, max(p["lat"] for p in ps) + margen
    previo = _leer_json(CACHE / "procedencia.json") or _leer_json(VIEJO / "terreno.json")
    nuevas = 0
    for z in ZOOMS:
        x0, y0 = tesela(norte, oeste, z)
        x1, y1 = tesela(sur, este, z)
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                original = CACHE / str(z) / str(x) / f"{y}.png"
                if not original.exists():
                    viejo = VIEJO / str(z) / str(x) / f"{y}.png"
                    original.parent.mkdir(parents=True, exist_ok=True)
                    if viejo.exists():
                        shutil.move(str(viejo), str(original))
                    else:
                        original.write_bytes(cache.get(URL.format(z=z, x=x, y=y), timeout=60).content)
                        nuevas += 1
                z_m = alturas(original.read_bytes())
                sombra = RELIEVE / str(z) / str(x) / f"{y}.png"
                if not sombra.exists():
                    lat = lat_de(y + 0.5, z)
                    metros_px = CIRCUNF * math.cos(math.radians(lat)) / (256 * 2 ** z)
                    sombra.parent.mkdir(parents=True, exist_ok=True)
                    sombreado(z_m, metros_px).save(sombra, optimize=True)
                destino = DESTINO / str(z) / str(x) / f"{y}.png"
                destino.parent.mkdir(parents=True, exist_ok=True)
                recodificar(z_m).save(destino, optimize=True)
    if VIEJO.exists():
        shutil.rmtree(VIEJO)  # ya está todo en la caché; la vista 3D lee relieve3d/
    # Fuente declarada por una tesela del zoom mayor (cabecera de S3).
    zm = max(ZOOMS)
    xm, ym = tesela((sur + norte) / 2, (oeste + este) / 2, zm)
    fuentes = None
    try:
        r = cache.get(URL.format(z=zm, x=xm, y=ym), timeout=60)
        fuentes = r.headers.get("x-amz-meta-x-imagery-sources")
    except Exception:  # noqa: BLE001 - sin red o sin cabecera: se deja la anterior
        pass
    procedencia = {
        "url": URL, "codificacion": "terrarium", "zooms": list(ZOOMS),
        "caja": [round(oeste, 3), round(sur, 3), round(este, 3), round(norte, 3)],
        "fecha_descarga": cache.ahora_utc() if nuevas or not previo.get("fecha_descarga") else previo["fecha_descarga"],
        "producto": "AWS Terrain Tiles (Tilezen/Mapzen), formato Terrarium",
        "fuente_datos": fuentes or previo.get("fuente_datos"),
        "credito": "SRTM data courtesy of the U.S. Geological Survey; Terrain Tiles by Mapzen (AWS Open Data)",
    }
    (CACHE / "procedencia.json").write_text(json.dumps(procedencia, ensure_ascii=False), encoding="utf-8")
    web = dict(procedencia, codificacion={
        "tipo": "custom", "formula": "altura_m = (R + G + B) * 4", "paso_m": PASO_M, "rango_m": [0, MAXIMO * PASO_M],
        "maplibre": {"encoding": "custom", "redFactor": PASO_M, "greenFactor": PASO_M, "blueFactor": PASO_M, "baseShift": 0},
        "motivo": "Un error de ±1 en un canal es de 4 m (en Terrarium, de 256 m en el rojo).",
    }, original="data/cache/terreno/",
        sombreado={"azimut": AZIMUT, "altura_sol": ALTURA_SOL, "ruta": "capas/relieve/{z}/{x}/{y}.png"})
    (DESTINO / "relieve3d.json").write_text(json.dumps(web, ensure_ascii=False), encoding="utf-8")
    print(f"[terreno] {nuevas} teselas nuevas; recodificadas en {DESTINO}; sombreado en {RELIEVE}")
    return web


if __name__ == "__main__":
    try:
        bajar()
    except cache.SinRed as e:
        sys.exit(str(e))
