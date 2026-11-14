"""CHIRPS v3.0 mensual (región latam, 0.05° ≈ 5 km) en los píxeles de las parcelas. Sin cuenta.

Por qué: NASA POWER pone 4 de las 5 parcelas en la misma celda de ~50 km. CHIRPS (satélite +
estaciones, de UCSB/CHC; no es NASA) tiene celdas de ~5 km y las separa. También es la
referencia independiente de la validación (plan, 5.2).

Archivo: https://data.chc.ucsb.edu/products/CHIRPS/v3.0/monthly/latam/tifs/chirps-v3.0.AAAA.MM.tif
Verificado el 13 nov 2026: GeoTIFF de 1720 x 1900, float32 (mm/mes), compresión LZW, UNA FILA POR
FRANJA (strip), esquina superior izquierda en (-120, 35), píxel de 0.05°. El servidor acepta
peticiones por rango, así que por cada mes se leen solo: la cabecera, el IFD, la parte de las
tablas de franjas que toca y las ~6 filas donde caen las parcelas (unos 25 KB en vez de 4.3 MB).
No hace falta rasterio ni GDAL: el decodificador LZW de TIFF está aquí abajo y se prueba contra
Pillow en tests/test_chirps.py.

Salida: data/cache/chirps/{parcela}.json con la serie mensual 1991-2025 del píxel de la parcela.
Los extractos por mes quedan en data/raw_big/chirps/ (fuera del repo) para reanudar.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

from pipeline import cache

URL = "https://data.chc.ucsb.edu/products/CHIRPS/v3.0/monthly/latam/tifs/chirps-v3.0.{anio}.{mes:02d}.tif"
ORIGEN_LON, ORIGEN_LAT, PASO = -120.0, 35.0, 0.05
NODATA = -9999.0


# ---------------------------------------------------------------- LZW de TIFF
def lzw_decodificar(datos: bytes, max_salida: int | None = None) -> bytes:
    """Decodificador LZW de TIFF (MSB primero, con 'early change'), como libtiff.

    `max_salida`: para en cuanto haya esa cantidad de bytes (solo se necesitan las columnas de las
    parcelas, que están al inicio de la fila global; ahorra ~75 % del trabajo en Python puro).
    """
    tabla = [bytes([i]) for i in range(256)] + [b"", b""]
    salida = bytearray()
    bits_total = len(datos) * 8
    pos, ancho, previo = 0, 9, None
    relleno = datos + b"\x00\x00\x00\x00"
    while pos + ancho <= bits_total:
        i = pos >> 3
        bloque = int.from_bytes(relleno[i:i + 4], "big")
        codigo = (bloque >> (32 - (pos & 7) - ancho)) & ((1 << ancho) - 1)
        pos += ancho
        if codigo == 256:  # Clear
            tabla = tabla[:258]
            ancho, previo = 9, None
            continue
        if codigo == 257:  # EOI
            break
        if previo is None:
            entrada = tabla[codigo]
        elif codigo < len(tabla):
            entrada = tabla[codigo]
            tabla.append(previo + entrada[:1])
        else:
            entrada = previo + previo[:1]
            tabla.append(entrada)
        salida += entrada
        if max_salida is not None and len(salida) >= max_salida:
            break
        previo = entrada
        if len(tabla) + 1 >= (1 << ancho) and ancho < 12:
            ancho += 1
    return bytes(salida)


def fila_col(lat: float, lon: float) -> tuple[int, int]:
    return int(math.floor((ORIGEN_LAT - lat) / PASO)), int(math.floor((lon - ORIGEN_LON) / PASO))


def centro(fila: int, col: int) -> tuple[float, float]:
    return round(ORIGEN_LAT - (fila + 0.5) * PASO, 3), round(ORIGEN_LON + (col + 0.5) * PASO, 3)


# ---------------------------------------------------------------- lectura por rangos
def _rango(url: str, a: int, b: int) -> bytes:
    r = cache.get(url, headers={"Range": f"bytes={a}-{b}"}, timeout=120)
    if r.status_code != 206 and len(r.content) != b - a + 1:
        raise RuntimeError(f"El servidor no respetó el rango {a}-{b} en {url}")
    return r.content


class _Lector:
    """Lee rangos de un TIFF remoto; la cola del archivo (IFD y tablas de franjas) se pide una sola vez."""

    COLA = 32768

    def __init__(self, url: str):
        self.url = url
        r = cache.get(url, headers={"Range": f"bytes=-{self.COLA}"}, timeout=120)
        total = int(r.headers.get("Content-Range", "/0").split("/")[-1] or 0)
        self.cola = r.content
        self.inicio_cola = total - len(self.cola) if total else None

    def leer(self, a: int, b: int) -> bytes:
        if self.inicio_cola is not None and a >= self.inicio_cola:
            return self.cola[a - self.inicio_cola: b - self.inicio_cola + 1]
        return _rango(self.url, a, b)


def leer_geo(url: str) -> tuple[float, float, float]:
    """(lon_origen, lat_origen, paso) desde ModelTiepoint y ModelPixelScale del TIFF."""
    cab = _rango(url, 0, 7)
    orden = "<" if cab[:2] == b"II" else ">"
    ifd = struct.unpack(orden + "I", cab[4:8])[0]
    n = struct.unpack(orden + "H", _rango(url, ifd, ifd + 1))[0]
    bruto = _rango(url, ifd + 2, ifd + 2 + 12 * n - 1)
    geo = {}
    for k in range(n):
        tag, tipo, cuenta = struct.unpack(orden + "HHI", bruto[12 * k:12 * k + 8])
        if tag in (33550, 33922):
            pnt = struct.unpack(orden + "I", bruto[12 * k + 8:12 * k + 12])[0]
            geo[tag] = struct.unpack(orden + "d" * cuenta, _rango(url, pnt, pnt + 8 * cuenta - 1))
    return geo[33922][3], geo[33922][4], geo[33550][0]


def leer_filas(url: str, filas: list[int], max_col: int | None = None) -> dict[int, list[float]]:
    """Devuelve {fila: [valores de la fila]} leyendo solo lo necesario del TIFF (unas 3 peticiones)."""
    lector = _Lector(url)
    _rango_l = lector.leer
    cab = _rango(url, 0, 7)
    orden = "<" if cab[:2] == b"II" else ">"
    if struct.unpack(orden + "H", cab[2:4])[0] != 42:
        raise RuntimeError("No es un TIFF clásico")
    ifd = struct.unpack(orden + "I", cab[4:8])[0]
    n = struct.unpack(orden + "H", _rango_l(ifd, ifd + 1))[0]
    bruto = _rango_l(ifd + 2, ifd + 2 + 12 * n - 1)
    etiquetas = {}
    for k in range(n):
        tag, tipo, cuenta = struct.unpack(orden + "HHI", bruto[12 * k:12 * k + 8])
        etiquetas[tag] = (tipo, cuenta, bruto[12 * k + 8:12 * k + 12])

    def escalar(tag):
        tipo, _c, v = etiquetas[tag]
        return struct.unpack(orden + ("H" if tipo == 3 else "I"), v[:2] if tipo == 3 else v)[0]

    ancho_img = escalar(256)
    alto = escalar(257)
    if escalar(259) != 5 or escalar(278) != 1 or escalar(258) != 32 or escalar(339) != 3:
        raise RuntimeError("Formato inesperado: se esperaba float32, LZW y una fila por franja")
    if 317 in etiquetas and escalar(317) != 1:
        raise RuntimeError("Predictor no soportado")
    p_off = struct.unpack(orden + "I", etiquetas[273][2])[0]
    p_cnt = struct.unpack(orden + "I", etiquetas[279][2])[0]
    f0, f1 = min(filas), max(filas)
    if f0 < 0 or f1 >= alto:
        raise ValueError("Fila fuera del raster")
    offs = struct.unpack(orden + "I" * (f1 - f0 + 1), _rango_l(p_off + 4 * f0, p_off + 4 * f1 + 3))
    cnts = struct.unpack(orden + "I" * (f1 - f0 + 1), _rango_l(p_cnt + 4 * f0, p_cnt + 4 * f1 + 3))
    a, b = min(offs), max(o + c for o, c in zip(offs, cnts)) - 1
    datos = _rango_l(a, b)
    out = {}
    for k, fila in enumerate(range(f0, f1 + 1)):
        if fila not in filas:
            continue
        n = ancho_img if max_col is None else min(ancho_img, max_col + 1)
        crudo = lzw_decodificar(datos[offs[k] - a: offs[k] - a + cnts[k]], max_salida=4 * n)
        out[fila] = list(struct.unpack(orden + "f" * n, crudo[:4 * n]))
    return out


def leer_columnas_ligero(url: str, filas: list[int], max_col: int) -> dict[int, list[float]]:
    """Como leer_filas, pero bajando el mínimo de bytes (el servidor limita el ancho de banda).

    Pide: cabecera (8 B), IFD (~360 B), las entradas de las tablas de franjas de esas filas (unos 40 B)
    y, de cada fila, solo el tramo comprimido que alcanza hasta `max_col` (si no alcanza, la fila entera).
    """
    cab = _rango(url, 0, 7)
    orden = "<" if cab[:2] == b"II" else ">"
    ifd = struct.unpack(orden + "I", cab[4:8])[0]
    bloque = _rango(url, ifd, ifd + 2 + 12 * 32 - 1)
    n = struct.unpack(orden + "H", bloque[:2])[0]
    et = {}
    for k in range(n):
        tag, tipo, cuenta = struct.unpack(orden + "HHI", bloque[2 + 12 * k:10 + 12 * k])
        et[tag] = (tipo, bloque[10 + 12 * k:14 + 12 * k])

    def escalar(tag):
        tipo, v = et[tag]
        return struct.unpack(orden + ("H" if tipo == 3 else "I"), v[:2] if tipo == 3 else v)[0]

    ancho = escalar(256)
    if escalar(259) != 5 or escalar(278) != 1 or escalar(258) != 32 or escalar(339) != 3:
        raise RuntimeError("Formato inesperado: se esperaba float32, LZW y una fila por franja")
    p_off = struct.unpack(orden + "I", et[273][1])[0]
    p_cnt = struct.unpack(orden + "I", et[279][1])[0]
    f0, f1 = min(filas), max(filas)
    # Las dos tablas (offsets y tamaños) en UNA petición: el servidor atiende pocas conexiones por IP y
    # cada petición cuesta ~1 s, así que conviene pedir menos veces aunque se bajen algunos KB más.
    a_t = min(p_off + 4 * f0, p_cnt + 4 * f0)
    b_t = max(p_off + 4 * f1 + 3, p_cnt + 4 * f1 + 3)
    tablas = _rango(url, a_t, b_t)
    offs = struct.unpack(orden + "I" * (f1 - f0 + 1), tablas[p_off + 4 * f0 - a_t: p_off + 4 * f1 + 4 - a_t])
    cnts = struct.unpack(orden + "I" * (f1 - f0 + 1), tablas[p_cnt + 4 * f0 - a_t: p_cnt + 4 * f1 + 4 - a_t])
    necesarios = 4 * (max_col + 1)
    parciales = [min(c, int(c * (max_col + 1) / ancho * 1.6) + 1024) for c in cnts]
    idx = [k for k, fila in enumerate(range(f0, f1 + 1)) if fila in filas]
    a_d = min(offs[k] for k in idx)
    b_d = max(offs[k] + parciales[k] for k in idx) - 1
    datos = _rango(url, a_d, b_d)  # las filas vecinas están juntas en el archivo: una sola petición
    out = {}
    for k in idx:
        fila = f0 + k
        crudo = lzw_decodificar(datos[offs[k] - a_d: offs[k] - a_d + parciales[k]], max_salida=necesarios)
        if len(crudo) < necesarios and parciales[k] < cnts[k]:
            crudo = lzw_decodificar(_rango(url, offs[k], offs[k] + cnts[k] - 1), max_salida=necesarios)
        out[fila] = list(struct.unpack(orden + "f" * (max_col + 1), crudo[:necesarios]))
    return out


def extraer_mes(anio: int, mes: int, pixeles: list[tuple[int, int]]) -> dict[str, float | None]:
    """{"fila,col": mm} para los píxeles pedidos; guarda el extracto en raw_big para reanudar."""
    clave = "_".join(f"{f}-{c}" for f, c in sorted(set(pixeles)))
    ruta = cache.RAW_BIG / "chirps" / f"{anio}{mes:02d}_{hashlib.md5(clave.encode()).hexdigest()[:8]}.json"
    if ruta.exists():
        return json.loads(ruta.read_text(encoding="utf-8"))
    filas = leer_filas(URL.format(anio=anio, mes=mes), sorted({f for f, _ in pixeles}), max_col=max(c for _, c in pixeles))
    res = {}
    for f, c in pixeles:
        v = filas[f][c]
        res[f"{f},{c}"] = None if (v is None or v <= NODATA + 1 or math.isnan(v)) else round(v, 2)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(res), encoding="utf-8")
    return res


URL_DIARIO = ("https://data.chc.ucsb.edu/products/CHIRPS/v3.0/daily/final/sat/{anio}/"
              "chirps-v3.0.sat.{anio}.{mes:02d}.{dia:02d}.tif")
GEO_DIARIO = (-180.0, 60.0, 0.05)  # verificado el 13 nov 2026 en el TIFF diario global (7200 x 2400)


def extraer_dia(fecha: str, pixeles: list[tuple[int, int]]) -> dict[str, float | None]:
    """{"fila,col": mm} de un día de CHIRPS v3 diario 'sat' (péntada de CHIRPS repartida con NASA IMERG)."""
    clave = "_".join(f"{f}-{c}" for f, c in sorted(set(pixeles)))
    ruta = cache.RAW_BIG / "chirps_diario" / f"{fecha}_{hashlib.md5(clave.encode()).hexdigest()[:8]}.json"
    if ruta.exists():
        return json.loads(ruta.read_text(encoding="utf-8"))
    a, m, d = (int(x) for x in fecha.split("-"))
    filas = leer_columnas_ligero(URL_DIARIO.format(anio=a, mes=m, dia=d), sorted({f for f, _ in pixeles}),
                                 max_col=max(c for _, c in pixeles))
    res = {}
    for f, c in pixeles:
        v = filas[f][c]
        res[f"{f},{c}"] = None if (v is None or v <= NODATA + 1 or math.isnan(v)) else round(v, 2)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(res), encoding="utf-8")
    return res


def descargar_diario(pids: list[str] | None = None, anio_ini: int = 2001, anio_fin: int = 2025,
                     meses: tuple[int, ...] = (6, 7, 8), hilos: int = 4) -> None:
    """CHIRPS v3 diario 'sat' en junio-agosto (la canícula) -> data/cache/chirps_diario/{parcela}.json.

    Advertencia del propio CHC (readme): el diario no es un producto independiente; reparte el total de
    la péntada de CHIRPS con el reparto diario de NASA IMERG Late V07.
    """
    from datetime import date, timedelta

    lon0, lat0, paso = GEO_DIARIO
    parcelas = [p for p in cache.cargar_parcelas() if not pids or p["id"] in pids]
    pix = {p["id"]: (int(math.floor((lat0 - p["lat"]) / paso)), int(math.floor((p["lon"] - lon0) / paso)))
           for p in parcelas}
    lista = sorted(set(pix.values()))
    fechas = []
    for anio in range(anio_ini, anio_fin + 1):
        d = date(anio, min(meses), 1)
        while d.year == anio and d.month <= max(meses):
            if d.month in meses:
                fechas.append(d.isoformat())
            d += timedelta(days=1)
    resultados: dict[str, dict] = {}
    with ThreadPoolExecutor(max_workers=hilos) as ex:
        fut = {ex.submit(extraer_dia, f, lista): f for f in fechas}
        for k, f in enumerate(as_completed(fut), 1):
            resultados[fut[f]] = f.result()
            if k % 200 == 0 or k == len(fechas):
                print(f"[chirps diario] {k}/{len(fechas)} días", flush=True)
    for p in parcelas:
        f, c = pix[p["id"]]
        filas = [[fe, resultados[fe].get(f"{f},{c}")] for fe in fechas]
        datos = {"columnas": ["fecha", "mm"], "filas": filas, "meses": list(meses), "lat": p["lat"], "lon": p["lon"],
                 "pixel": {"fila": f, "col": c}, "resolucion": "0.05° (~5 km), diario"}
        proc = cache.procedencia(url=URL_DIARIO.format(anio="AAAA", mes=0, dia=0).replace(".00.00", ".MM.DD"),
                                 producto="CHIRPS v3.0 diario 'sat' (péntada de CHIRPS repartida con NASA IMERG Late V07)",
                                 version="3.0", periodo=f"{anio_ini}-{anio_fin}, meses {list(meses)}",
                                 nota="No es un producto diario independiente (readme del CHC); lectura por rangos")
        ruta = cache.guardar(cache.CACHE / "chirps_diario" / f"{p['id']}.json", datos, proc)
        print(f"[chirps diario {p['id']}] {len(filas)} días -> {ruta}")


def descargar(pids: list[str] | None = None, anio_ini: int = 1991, anio_fin: int = 2025, hilos: int = 3) -> dict:
    parcelas = [p for p in cache.cargar_parcelas() if not pids or p["id"] in pids]
    pix = {p["id"]: fila_col(p["lat"], p["lon"]) for p in parcelas}
    lista = sorted(set(pix.values()))
    meses = [(a, m) for a in range(anio_ini, anio_fin + 1) for m in range(1, 13)]
    resultados: dict[tuple[int, int], dict] = {}
    with ThreadPoolExecutor(max_workers=hilos) as ex:
        fut = {ex.submit(extraer_mes, a, m, lista): (a, m) for a, m in meses}
        for k, f in enumerate(as_completed(fut), 1):
            resultados[fut[f]] = f.result()
            if k % 60 == 0 or k == len(meses):
                print(f"[chirps] {k}/{len(meses)} meses", flush=True)
    for p in parcelas:
        f, c = pix[p["id"]]
        filas = [[a, m, resultados[(a, m)].get(f"{f},{c}")] for a, m in meses]
        lat_c, lon_c = centro(f, c)
        compartida = sorted(q for q, v in pix.items() if v == (f, c) and q != p["id"])
        datos = {"columnas": ["anio", "mes", "mm"], "filas": filas, "pixel": {"fila": f, "col": c, "lat_centro": lat_c,
                 "lon_centro": lon_c}, "comparte_pixel_con": compartida, "resolucion": "0.05° (~5 km)",
                 "lat": p["lat"], "lon": p["lon"]}
        proc = cache.procedencia(url=URL.format(anio="AAAA", mes=0).replace(".00.", ".MM."),
                                 producto="CHIRPS v3.0 mensual, región latam", version="3.0",
                                 nota="Lectura por rangos de las filas del píxel; mm/mes; -9999 -> null",
                                 periodo=f"{anio_ini}-{anio_fin}")
        ruta = cache.guardar(cache.CACHE / "chirps" / f"{p['id']}.json", datos, proc)
        print(f"[chirps {p['id']}] píxel {f},{c} ({lat_c}, {lon_c}) -> {ruta}")
    return {"pixeles": pix}


CARPETA_FINAL = "monthly/latam: producto final (el preliminar está en la carpeta prelim/)"


def descargar_reciente(anio: int = 2026, meses: tuple[int, ...] = (7, 8), pids: list[str] | None = None) -> dict:
    """Meses recientes de CHIRPS v3 mensual final, para la observación de 2026 de la validación.

    Va en data/cache/chirps_reciente/, aparte de data/cache/chirps/ (1991-2025): el motor no usa estos
    meses. Guarda la fecha Last-Modified de cada TIF porque el CHC recalcula sus productos finales cada
    mes (README de CHIRPS v3): la cifra puede cambiar. Exige MILPA_ONLINE=1.
    """
    cache.exigir_red()
    import requests

    parcelas = [p for p in cache.cargar_parcelas() if not pids or p["id"] in pids]
    pix = {p["id"]: fila_col(p["lat"], p["lon"]) for p in parcelas}
    lista = sorted(set(pix.values()))
    archivos, valores = [], {}
    for m in meses:
        url = URL.format(anio=anio, mes=m)
        r = requests.head(url, timeout=60, headers={"User-Agent": cache.AGENTE})
        r.raise_for_status()
        archivos.append({"mes": m, "url": url, "last_modified": r.headers.get("Last-Modified")})
        valores[m] = extraer_mes(anio, m, lista)
    for p in parcelas:
        f, c = pix[p["id"]]
        lat_c, lon_c = centro(f, c)
        datos = {"anio": anio, "meses": {str(m): valores[m].get(f"{f},{c}") for m in meses}, "unidad": "mm/mes",
                 "pixel": {"fila": f, "col": c, "lat_centro": lat_c, "lon_centro": lon_c}, "archivos": archivos,
                 "carpeta": CARPETA_FINAL, "lat": p["lat"], "lon": p["lon"]}
        proc = cache.procedencia(url=URL.format(anio=anio, mes=0).replace(".00.", ".MM."),
                                 producto="CHIRPS v3.0 mensual final, región latam", version="3.0",
                                 nota="Meses recientes para la observación de 2026; el motor no los usa",
                                 periodo=f"{anio}, meses {', '.join(str(m) for m in meses)}")
        ruta = cache.guardar(cache.CACHE / "chirps_reciente" / f"{p['id']}.json", datos, proc)
        print(f"[chirps reciente {p['id']}] {datos['meses']} -> {ruta}")
    return {"archivos": archivos}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("parcelas", nargs="*")
    ap.add_argument("--desde", type=int, default=1991)
    ap.add_argument("--hasta", type=int, default=2025)
    ap.add_argument("--diario", action="store_true", help="CHIRPS diario 'sat' de junio a agosto, 2001-2025")
    ap.add_argument("--reciente", type=int, metavar="AÑO", help="julio y agosto de ese año, aparte (observación 2026)")
    a = ap.parse_args()
    try:
        if a.reciente:
            descargar_reciente(a.reciente, pids=a.parcelas or None)
        elif a.diario:
            descargar_diario(a.parcelas or None)
        else:
            descargar(a.parcelas or None, a.desde, a.hasta)
    except cache.SinRed as e:
        sys.exit(str(e))
