"""Toma 1 del video: la Tierra gira y baja hasta los píxeles MODIS de la parcela de Olopa.

Uso (desde la raíz del repo, con internet la primera vez):
    python video/pitch/scripts/picada.py

1. Descarga de NASA GIBS (WMS, EPSG:4326, sin cuenta) a video/pitch/assets/nasa/:
   - Blue Marble Next Generation del mundo (8192 x 4096) y de Centroamérica (4096 x 4096);
   - MODIS Terra Corrected Reflectance, color real, 21 feb 2026, alrededor de Chiquimula,
     pedido justo en la malla nativa de 250 m de GIBS (0.5625/256 grados por píxel): cada
     píxel de la imagen es un píxel del satélite.
2. Dibuja cada cuadro con una proyección ortográfica (la Tierra vista desde lejos) y un
   acercamiento exponencial hasta que un píxel MODIS mide 137 px en pantalla.
3. Escribe video/pitch/assets/dive/picada.mp4 (30 fps), final.png (el último cuadro, sin
   desenfoque) y final.json (dónde caen en pantalla la malla de píxeles, el píxel de la
   parcela y un cuadro de 0.35 ha centrado en el punto de la parcela).
"""
from __future__ import annotations

import json
import math
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image

PITCH = Path(__file__).resolve().parent.parent
NASA = PITCH / "assets" / "nasa"
SALIDA = PITCH / "assets" / "dive"

WMS = ("https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?SERVICE=WMS&REQUEST=GetMap"
       "&VERSION=1.3.0&CRS=EPSG:4326&STYLES=")
PASO = 0.5625 / 256                      # grados por píxel en la malla de 250 m de GIBS
MODIS_BBOX = (13.89990234375, -90.301025390625, 15.49951171875, -88.301513671875)  # s, w, n, e
MODIS_W, MODIS_H = 910, 728
FECHA_MODIS = "2026-02-21"
CA_BBOX = (9.0, -95.0, 21.0, -83.0)

IMAGENES = {
    "mundo.jpg": f"{WMS}&FORMAT=image/jpeg&LAYERS=BlueMarble_NextGeneration&BBOX=-90,-180,90,180&WIDTH=8192&HEIGHT=4096",
    "centroamerica.jpg": (f"{WMS}&FORMAT=image/jpeg&LAYERS=BlueMarble_NextGeneration"
                          f"&BBOX={CA_BBOX[0]},{CA_BBOX[1]},{CA_BBOX[2]},{CA_BBOX[3]}&WIDTH=4096&HEIGHT=4096"),
    "modis.png": (f"{WMS}&FORMAT=image/png&LAYERS=MODIS_Terra_CorrectedReflectance_TrueColor&TIME={FECHA_MODIS}"
                  f"&BBOX={MODIS_BBOX[0]},{MODIS_BBOX[1]},{MODIS_BBOX[2]},{MODIS_BBOX[3]}"
                  f"&WIDTH={MODIS_W}&HEIGHT={MODIS_H}"),
}

FPS = 30
N = 150                                   # 5 s
T_FIN = (N - 1) / FPS
W, H = 1920, 1080
CX, CY = 900.0, 470.0                     # dónde queda el punto de la parcela en pantalla
OLOPA = (14.66563, -89.29358)
INICIO = (8.0, -72.0)                     # centro de la vista al empezar
R_TIERRA_M = 6371000.0
R0 = 620.0                                # radio de la Tierra en px en el cuadro 0
PX_POR_PIXEL = 137.0                      # tamaño final de un píxel MODIS de 250 m
R1 = PX_POR_PIXEL / (250.0 / R_TIERRA_M)
ESPACIO = np.array([5, 8, 13], np.float32) / 255.0
GAMMA = 0.9


def descargar() -> None:
    NASA.mkdir(parents=True, exist_ok=True)
    for nombre, url in IMAGENES.items():
        ruta = NASA / nombre
        if ruta.exists() and ruta.stat().st_size > 10000:
            continue
        print("descargando", nombre)
        req = urllib.request.Request(url, headers={"User-Agent": "milpa-resiliente-video"})
        with urllib.request.urlopen(req, timeout=300) as r:
            ruta.write_bytes(r.read())


def cargar(nombre: str) -> np.ndarray:
    a = np.asarray(Image.open(NASA / nombre).convert("RGB"), np.float32) / 255.0
    return a ** GAMMA


def bilineal(img: np.ndarray, x: np.ndarray, y: np.ndarray) -> np.ndarray:
    h, w = img.shape[:2]
    x = x - 0.5
    y = y - 0.5
    x0 = np.floor(x).astype(np.int32)
    y0 = np.floor(y).astype(np.int32)
    fx = (x - x0)[..., None].astype(np.float32)
    fy = (y - y0)[..., None].astype(np.float32)
    xa, xb = np.clip(x0, 0, w - 1), np.clip(x0 + 1, 0, w - 1)
    ya, yb = np.clip(y0, 0, h - 1), np.clip(y0 + 1, 0, h - 1)
    arriba = img[ya, xa] * (1 - fx) + img[ya, xb] * fx
    abajo = img[yb, xa] * (1 - fx) + img[yb, xb] * fx
    return arriba * (1 - fy) + abajo * fy


def cercano(img: np.ndarray, x: np.ndarray, y: np.ndarray) -> np.ndarray:
    h, w = img.shape[:2]
    return img[np.clip(np.floor(y).astype(np.int32), 0, h - 1), np.clip(np.floor(x).astype(np.int32), 0, w - 1)]


def suave(u):
    return 0.5 - 0.5 * np.cos(np.pi * np.clip(u, 0.0, 1.0))


def slerp(a, b, f):
    def vec(p):
        la, lo = math.radians(p[0]), math.radians(p[1])
        return np.array([math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la)])
    va, vb = vec(a), vec(b)
    om = math.acos(max(-1.0, min(1.0, float(va @ vb))))
    if om < 1e-9:
        v = va
    else:
        v = (math.sin((1 - f) * om) * va + math.sin(f * om) * vb) / math.sin(om)
    return math.degrees(math.asin(v[2])), math.degrees(math.atan2(v[1], v[0]))


def camara(t: float):
    """Radio de la Tierra en px y centro de la vista (lat, lon) en el tiempo t."""
    z = float(suave((t - 0.3) / (T_FIN - 0.3)))
    r = math.exp(math.log(R0) + z * (math.log(R1) - math.log(R0)))
    f = float(suave(t / 2.0))
    return r, slerp(INICIO, OLOPA, f)


def inversa(r, centro, xs, ys):
    u = (xs - CX) / r
    v = (CY - ys) / r
    rho = np.hypot(u, v)
    c = np.arcsin(np.clip(rho, 0.0, 1.0))
    sc, cc = np.sin(c), np.cos(c)
    f0 = math.radians(centro[0])
    with np.errstate(invalid="ignore", divide="ignore"):
        k = np.where(rho > 0, v * sc / np.where(rho > 0, rho, 1.0), 0.0)
        lat = np.degrees(np.arcsin(np.clip(cc * math.sin(f0) + k * math.cos(f0), -1.0, 1.0)))
        lon = centro[1] + np.degrees(np.arctan2(u * sc, rho * cc * math.cos(f0) - v * sc * math.sin(f0)))
    lon = (lon + 180.0) % 360.0 - 180.0
    return lat, lon, rho


def directa(r, centro, lat, lon):
    f0, l0 = math.radians(centro[0]), math.radians(centro[1])
    f, l = math.radians(lat), math.radians(lon)
    x = r * math.cos(f) * math.sin(l - l0)
    y = r * (math.cos(f0) * math.sin(f) - math.sin(f0) * math.cos(f) * math.cos(l - l0))
    return CX + x, CY - y


def peso_borde(lat, lon, bbox, ancho):
    s, w, n, e = bbox
    d = np.minimum.reduce([lat - s, n - lat, lon - w, e - lon])
    return np.clip(d / ancho, 0.0, 1.0)[..., None].astype(np.float32) ** 1.0


class Pintor:
    def __init__(self):
        self.mundo = cargar("mundo.jpg")
        self.ca = cargar("centroamerica.jpg")
        self.modis = cargar("modis.png")
        ys, xs = np.mgrid[0:H, 0:W].astype(np.float64)
        self.xs, self.ys = xs + 0.5, ys + 0.5

    def cuadro(self, t: float) -> np.ndarray:
        r, centro = camara(t)
        lat, lon, rho = inversa(r, centro, self.xs, self.ys)
        col = bilineal(self.mundo, (lon + 180.0) / 360.0 * self.mundo.shape[1], (90.0 - lat) / 180.0 * self.mundo.shape[0])
        s, w, n, e = CA_BBOX
        if r > 900:
            ca = bilineal(self.ca, (lon - w) / (e - w) * self.ca.shape[1], (n - lat) / (n - s) * self.ca.shape[0])
            p = peso_borde(lat, lon, CA_BBOX, 1.2)
            col = col * (1 - p) + ca * p
        if r > 6000:
            s, w, n, e = MODIS_BBOX
            mx = (lon - w) / PASO
            my = (n - lat) / PASO
            bloque = r * math.radians(PASO)          # px de pantalla por píxel MODIS
            m = float(np.clip((bloque - 7.0) / 23.0, 0.0, 1.0))
            md = bilineal(self.modis, mx, my) if m < 1 else 0
            if m > 0:
                md = md * (1 - m) + cercano(self.modis, mx, my) * m
            p = peso_borde(lat, lon, MODIS_BBOX, 0.3)
            col = col * (1 - p) + md * p
        borde = np.clip((1.0 - rho) * r + 0.5, 0.0, 1.0)[..., None].astype(np.float32)
        return col * borde + ESPACIO * (1 - borde)

    def cuadro_con_estela(self, t: float) -> np.ndarray:
        # obturador de 180°: tres muestras en 1/60 s
        dt = 1.0 / (FPS * 2)
        ts = [max(0.0, t - dt / 2), t, min(T_FIN, t + dt / 2)]
        return sum(self.cuadro(x) for x in ts) / len(ts)


def a_png(col: np.ndarray, ruta: Path) -> None:
    Image.fromarray((np.clip(col, 0, 1) * 255 + 0.5).astype(np.uint8)).save(ruta)


def datos_finales() -> dict:
    r, centro = camara(T_FIN)
    s, w, n, e = MODIS_BBOX
    lat_t, lon_t = OLOPA
    col = math.floor((lon_t - w) / PASO)
    fil = math.floor((n - lat_t) / PASO)
    x0, y0 = directa(r, centro, n - fil * PASO, w + col * PASO)
    x1, y1 = directa(r, centro, n - (fil + 1) * PASO, w + (col + 1) * PASO)
    xs, ys = [], []
    for k in range(col - 12, col + 14):
        x, _ = directa(r, centro, lat_t, w + k * PASO)
        if -2 <= x <= W + 2:
            xs.append(round(x, 2))
    for k in range(fil - 8, fil + 10):
        _, y = directa(r, centro, n - k * PASO, lon_t)
        if -2 <= y <= H + 2:
            ys.append(round(y, 2))
    lado = r * math.sqrt(3500.0) / R_TIERRA_M      # 0.35 ha = 3500 m²
    px_x = abs(x1 - x0)
    px_y = abs(y1 - y0)
    return {
        "camara": {"radio_px": r, "centro": centro, "cx": CX, "cy": CY},
        "pixel_parcela": {"x": round(min(x0, x1), 2), "y": round(min(y0, y1), 2),
                          "w": round(px_x, 2), "h": round(px_y, 2),
                          "m_ancho": round(PASO * 111320 * math.cos(math.radians(lat_t)), 1),
                          "m_alto": round(PASO * 110574, 1)},
        "parcela_035ha": {"x": round(CX - lado / 2, 2), "y": round(CY - lado / 2, 2), "lado": round(lado, 2)},
        "malla_x": xs,
        "malla_y": ys,
        "fuente": f"NASA GIBS, MODIS Terra Corrected Reflectance True Color, {FECHA_MODIS}, malla nativa de 250 m",
    }


def main() -> int:
    descargar()
    SALIDA.mkdir(parents=True, exist_ok=True)
    pintor = Pintor()
    tmp = Path(tempfile.mkdtemp(prefix="picada-"))
    try:
        for i in range(N):
            t = i / FPS
            col = pintor.cuadro(t) if i == N - 1 else pintor.cuadro_con_estela(t)
            a_png(col, tmp / f"f{i:04d}.png")
            if i % 15 == 0:
                print(f"cuadro {i}/{N}", flush=True)
        a_png(pintor.cuadro(T_FIN), SALIDA / "final.png")
        subprocess.run([
            "ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(tmp / "f%04d.png"),
            "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-g", "10", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", str(SALIDA / "picada.mp4"),
        ], check=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    (SALIDA / "final.json").write_text(json.dumps(datos_finales(), indent=2), encoding="utf-8")
    print("OK", SALIDA / "picada.mp4")
    return 0


if __name__ == "__main__":
    sys.exit(main())
