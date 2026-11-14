"""FIRMS: detecciones de fuego activo (quemas) cerca de cada parcela.

Histórico SIN CLAVE: CSV anual por país (verificado el 13 nov 2026):
  https://firms.modaps.eosdis.nasa.gov/data/country/viirs-snpp/{AAAA}/viirs-snpp_{AAAA}_Guatemala.csv
  (VIIRS S-NPP 375 m desde 2012; también existe modis/{AAAA}/modis_{AAAA}_Guatemala.csv desde 2000)
Columnas: latitude, longitude, bright_ti4, scan, track, acq_date, acq_time, satellite, instrument,
          confidence (l/n/h), version, bright_ti5, frp, daynight, type
type: 0 = presunto fuego de vegetación, 1 = volcán activo, 2 = otra fuente fija, 3 = mar adentro.

Reciente (2026) CON CLAVE: /api/area/csv/{MAP_KEY}/{VIIRS_SNPP_SP|VIIRS_SNPP_NRT}/{oeste,sur,este,norte}/{días}/{fecha}
  La clave se lee de FIRMS_MAP_KEY en .env (gitignored) y nunca se escribe en la caché ni en logs.
  `python -m pipeline.clientes.firms --reciente 2026` baja el año; luego `recortar` lo une.

El CSV nacional queda en data/raw_big/firms/ (fuera del repo). Al repo va
data/cache/firms/{parcela}.json con las detecciones a 1 km o menos.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import sys

from pipeline import cache

URL_PAIS = "https://firms.modaps.eosdis.nasa.gov/data/country/{sensor}/{anio}/{sensor}_{anio}_Guatemala.csv"
RADIO_CACHE_M = 1000.0


def distancia_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371008.8
    f1, f2 = math.radians(lat1), math.radians(lat2)
    df, dl = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(df / 2) ** 2 + math.cos(f1) * math.cos(f2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def csv_nacional(sensor: str, anio: int) -> str:
    ruta = cache.RAW_BIG / "firms" / f"{sensor}_{anio}_Guatemala.csv"
    if ruta.exists():
        return ruta.read_text(encoding="utf-8")
    r = cache.get(URL_PAIS.format(sensor=sensor, anio=anio), timeout=300)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(r.text, encoding="utf-8")
    return r.text


def recortar(pid: str, sensor: str = "viirs-snpp", anio_ini: int = 2012, anio_fin: int = 2025,
             anio_reciente: int | None = 2026) -> dict:
    p = cache.parcela(pid)
    detecciones = []
    anios_ok = []
    for anio in range(anio_ini, anio_fin + 1):
        texto = csv_nacional(sensor, anio)
        anios_ok.append(anio)
        for f in csv.DictReader(io.StringIO(texto)):
            lat, lon = float(f["latitude"]), float(f["longitude"])
            if abs(lat - p["lat"]) > 0.02 or abs(lon - p["lon"]) > 0.02:
                continue
            d = distancia_m(p["lat"], p["lon"], lat, lon)
            if d <= RADIO_CACHE_M:
                detecciones.append({
                    "fecha": f["acq_date"], "hora": f["acq_time"], "lat": lat, "lon": lon,
                    "distancia_m": round(d, 1), "confianza": f["confidence"], "frp": float(f["frp"] or 0),
                    "tipo": int(f.get("type") or 0), "satelite": f["satellite"], "instrumento": f["instrument"],
                })
    # Año en curso por la API con clave (si ya se bajó con descargar_reciente). Cuenta como año
    # observado solo si cubre toda la época de quema (enero a mayo).
    reciente = None
    if anio_reciente:
        filas, meta = _reciente(anio_reciente)
        if meta and meta["desde"] <= f"{anio_reciente}-01-01" and meta["hasta"] >= f"{anio_reciente}-05-31":
            anios_ok.append(anio_reciente)
            reciente = meta
            for f in filas:
                lat, lon = float(f["latitude"]), float(f["longitude"])
                d = distancia_m(p["lat"], p["lon"], lat, lon)
                if d <= RADIO_CACHE_M:
                    detecciones.append({
                        "fecha": f["acq_date"], "hora": f["acq_time"], "lat": lat, "lon": lon, "distancia_m": round(d, 1),
                        "confianza": f["confidence"], "frp": float(f["frp"] or 0), "tipo": 0,
                        "satelite": f["satellite"], "instrumento": f["instrument"], "fuente_api": f["fuente_api"]})
    detecciones.sort(key=lambda x: (x["fecha"], x["hora"]))
    datos = {"sensor": sensor, "anios_observados": anios_ok, "radio_m": RADIO_CACHE_M,
             "lat": p["lat"], "lon": p["lon"], "resolucion": "375 m (VIIRS)", "detecciones": detecciones,
             "reciente": reciente}
    proc = cache.procedencia(
        url=URL_PAIS.format(sensor=sensor, anio="{AAAA}"), producto="FIRMS VIIRS S-NPP 375 m, archivo anual por país",
        version="archivo estándar (SP) / NRT según el año; ver columna version",
        nota=(f"Recorte a {int(RADIO_CACHE_M)} m de la parcela; sin filtrar por tipo ni confianza (el motor filtra)"
              + (f". {anio_reciente}: API de área con FIRMS_MAP_KEY ({API}/area/csv/{{MAP_KEY}}/...), sin columna type"
                 if reciente else "")))
    ruta = cache.guardar(cache.CACHE / "firms" / f"{pid}.json", datos, proc)
    print(f"[firms {pid}] {len(detecciones)} detecciones a <= {int(RADIO_CACHE_M)} m en {len(anios_ok)} años -> {ruta}")
    return {"procedencia": proc, "datos": datos}


API = "https://firms.modaps.eosdis.nasa.gov/api"
COLUMNAS_API = ["latitude", "longitude", "acq_date", "acq_time", "satellite", "instrument", "confidence", "frp"]


def _api(ruta: str, clave: str) -> str:
    """GET a la API de FIRMS sin que la clave salga en errores ni en la caché."""
    try:
        r = cache.get(f"{API}/{ruta.replace('{KEY}', clave)}", timeout=180)
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(cache.ocultar(f"{type(e).__name__}: {e}", clave)) from None
    texto = r.text
    if texto.lstrip().lower().startswith(("invalid", "error")):
        raise RuntimeError(cache.ocultar(f"FIRMS respondió: {texto[:200]}", clave))
    return texto


def disponibilidad(clave: str) -> dict[str, tuple[str, str]]:
    """{fuente: (fecha_min, fecha_max)} según /api/data_availability."""
    out = {}
    for f in csv.DictReader(io.StringIO(_api("data_availability/csv/{KEY}/ALL", clave))):
        out[f["data_id"]] = (f["min_date"], f["max_date"])
    return out


def caja_parcelas(margen_grados: float = 0.06) -> tuple[float, float, float, float]:
    ps = cache.cargar_parcelas()
    return (round(min(p["lon"] for p in ps) - margen_grados, 3), round(min(p["lat"] for p in ps) - margen_grados, 3),
            round(max(p["lon"] for p in ps) + margen_grados, 3), round(max(p["lat"] for p in ps) + margen_grados, 3))


def descargar_reciente(anio: int = 2026, dias: int = 5) -> dict:
    """Detecciones VIIRS S-NPP de `anio` en la caja de las 5 parcelas, con FIRMS_MAP_KEY del .env.

    Usa el producto estándar (SP) hasta donde exista y NRT después. El CSV de la API no trae la
    columna `type` (volcán / fuente fija): la caja está a más de 100 km de los volcanes activos.
    Guarda data/raw_big/firms/reciente_{anio}.csv (fuera del repo) y un resumen sin la clave.
    """
    from datetime import date, timedelta

    clave = cache.secreto("FIRMS_MAP_KEY")
    if not clave:
        raise RuntimeError("Falta FIRMS_MAP_KEY en .env: 2026 queda como vacío declarado.")
    disp = disponibilidad(clave)
    fin_sp = disp.get("VIIRS_SNPP_SP", ("", ""))[1]
    fin_nrt = disp.get("VIIRS_SNPP_NRT", ("", ""))[1]
    caja = caja_parcelas()
    area = ",".join(str(x) for x in caja)
    ini = date(anio, 1, 1)
    ultimo = min(date(anio, 12, 31), date.fromisoformat(fin_nrt) if fin_nrt else date(anio, 12, 31))
    filas, tramos = [], []
    d = ini
    while d <= ultimo:
        fuente = "VIIRS_SNPP_SP" if fin_sp and d.isoformat() <= fin_sp else "VIIRS_SNPP_NRT"
        n = min(dias, (ultimo - d).days + 1)
        texto = _api(f"area/csv/{{KEY}}/{fuente}/{area}/{n}/{d.isoformat()}", clave)
        for f in csv.DictReader(io.StringIO(texto)):
            filas.append({k: f.get(k, "") for k in COLUMNAS_API} | {"fuente_api": fuente})
        tramos.append((d.isoformat(), n, fuente))
        d += timedelta(days=n)
    vistos, unicas = set(), []
    for f in filas:
        k = (f["latitude"], f["longitude"], f["acq_date"], f["acq_time"])
        if k not in vistos:
            vistos.add(k)
            unicas.append(f)
    ruta = cache.RAW_BIG / "firms" / f"reciente_{anio}.csv"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNAS_API + ["fuente_api"])
        w.writeheader()
        w.writerows(unicas)
    resumen = {"anio": anio, "caja": caja, "detecciones": len(unicas), "tramos": len(tramos),
               "desde": ini.isoformat(), "hasta": ultimo.isoformat(), "fin_sp": fin_sp, "fin_nrt": fin_nrt}
    (ruta.with_suffix(".json")).write_text(json.dumps(resumen), encoding="utf-8")
    print(f"[firms {anio}] {len(unicas)} detecciones en la caja {caja}, {ini} a {ultimo} ({len(tramos)} peticiones)")
    return resumen


def _reciente(anio: int) -> tuple[list[dict], dict | None]:
    ruta = cache.RAW_BIG / "firms" / f"reciente_{anio}.csv"
    meta = cache.RAW_BIG / "firms" / f"reciente_{anio}.json"
    if not ruta.exists() or not meta.exists():
        return [], None
    with ruta.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh)), json.loads(meta.read_text(encoding="utf-8"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("parcelas", nargs="*")
    ap.add_argument("--desde", type=int, default=2012)
    ap.add_argument("--hasta", type=int, default=2025)
    ap.add_argument("--reciente", type=int, default=None, help="baja ese año con la API y FIRMS_MAP_KEY")
    a = ap.parse_args()
    try:
        if a.reciente:
            descargar_reciente(a.reciente)
        for pid in a.parcelas or [p["id"] for p in cache.cargar_parcelas()]:
            recortar(pid, anio_ini=a.desde, anio_fin=a.hasta)
    except cache.SinRed as e:
        sys.exit(str(e))
