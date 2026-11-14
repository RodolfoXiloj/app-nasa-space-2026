"""SMAP numérico por AppEEARS (NASA LP DAAC), extracción por punto. Requiere Earthdata Login.

API: https://appeears.earthdatacloud.nasa.gov/api/
  POST /login (usuario y contraseña Earthdata, básica) -> token; POST /task (tipo point);
  GET /task/{id} hasta 'done'; GET /bundle/{id} y /bundle/{id}/{file_id}; POST /logout.
Producto: SPL3SMP_E.006 (SMAP L3 mejorado, 9 km, diario), capas AM y PM de humedad superficial
(m3/m3) y su bandera retrieval_qual_flag (bit 0 = 0 -> calidad recomendada). Verificado en el
catálogo público /api/product el 13 nov 2026.

Credenciales: EARTHDATA_USERNAME y EARTHDATA_PASSWORD del entorno o del .env (gitignored).
La contraseña nunca se imprime, no se guarda en disco y se tapa en los mensajes de error.

    MILPA_ONLINE=1 python -m pipeline.clientes.appeears_smap enviar
    MILPA_ONLINE=1 python -m pipeline.clientes.appeears_smap esperar <task_id>
    python -m pipeline.clientes.appeears_smap procesar <ruta.csv>     # sin red

Salida: data/cache/smap/{parcela}.json con la mediana de julio-agosto, su percentil y la
anomalía de 2018. El motor ya lee ese archivo (confianza y tarjeta).
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
import time
from pathlib import Path

import requests

from pipeline import cache

API = "https://appeears.earthdatacloud.nasa.gov/api"
PRODUCTO = "SPL3SMP_E.006"
CAPAS = [
    "Soil_Moisture_Retrieval_Data_AM_soil_moisture",
    "Soil_Moisture_Retrieval_Data_AM_retrieval_qual_flag",
    "Soil_Moisture_Retrieval_Data_PM_soil_moisture_pm",
    "Soil_Moisture_Retrieval_Data_PM_retrieval_qual_flag_pm",
]
INICIO = "03-31-2015"


def _credenciales() -> tuple[str, str]:
    u, p = cache.secreto("EARTHDATA_USERNAME"), cache.secreto("EARTHDATA_PASSWORD")
    if not u or not p:
        raise RuntimeError("Faltan EARTHDATA_USERNAME o EARTHDATA_PASSWORD (entorno o .env).")
    return u, p


def login() -> str:
    cache.exigir_red()
    u, p = _credenciales()
    try:
        r = requests.post(f"{API}/login", auth=(u, p), timeout=60, headers={"User-Agent": cache.AGENTE})
        r.raise_for_status()
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(cache.ocultar(f"Login de AppEEARS falló: {type(e).__name__}: {e}", p)) from None
    return r.json()["token"]


def logout(token: str) -> None:
    try:
        requests.post(f"{API}/logout", headers={"Authorization": f"Bearer {token}"}, timeout=30)
    except requests.RequestException:
        pass


def _h(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "User-Agent": cache.AGENTE}


def enviar(token: str, fin: str, nombre: str = "milpa_smap_l3e") -> str:
    puntos = [{"id": p["id"], "category": "parcela", "latitude": p["lat"], "longitude": p["lon"]}
              for p in cache.cargar_parcelas()]
    cuerpo = {"task_type": "point", "task_name": nombre, "params": {
        "dates": [{"startDate": INICIO, "endDate": fin}],
        "layers": [{"product": PRODUCTO, "layer": c} for c in CAPAS],
        "coordinates": puntos}}
    r = requests.post(f"{API}/task", json=cuerpo, headers=_h(token), timeout=120)
    if r.status_code >= 400:
        raise RuntimeError(f"AppEEARS rechazó la tarea: {r.status_code} {r.text[:300]}")
    tid = r.json()["task_id"]
    (cache.RAW_BIG / "appeears").mkdir(parents=True, exist_ok=True)
    (cache.RAW_BIG / "appeears" / f"{tid}.json").write_text(json.dumps({"task_id": tid, "cuerpo": cuerpo}), encoding="utf-8")
    print(f"[appeears] tarea enviada {tid} con {len(puntos)} puntos, {INICIO} a {fin}")
    return tid


def estado(token: str, tid: str) -> str:
    r = requests.get(f"{API}/task/{tid}", headers=_h(token), timeout=60)
    r.raise_for_status()
    return r.json().get("status", "?")


def esperar(token: str, tid: str, max_min: int = 90, cada_s: int = 30) -> str:
    t0 = time.time()
    while True:
        s = estado(token, tid)
        print(f"[appeears] {tid}: {s} ({int(time.time() - t0)} s)", flush=True)
        if s in ("done", "error", "expired", "deleted"):
            return s
        if time.time() - t0 > max_min * 60:
            return s
        time.sleep(cada_s)


def bajar(token: str, tid: str) -> list[Path]:
    r = requests.get(f"{API}/bundle/{tid}", headers=_h(token), timeout=60)
    r.raise_for_status()
    destino = cache.RAW_BIG / "appeears" / tid
    destino.mkdir(parents=True, exist_ok=True)
    rutas = []
    for f in r.json()["files"]:
        nombre = Path(f["file_name"]).name
        if not nombre.endswith(".csv"):
            continue
        d = requests.get(f"{API}/bundle/{tid}/{f['file_id']}", headers=_h(token), timeout=300, allow_redirects=True)
        d.raise_for_status()
        ruta = destino / nombre
        ruta.write_bytes(d.content)
        rutas.append(ruta)
        print(f"[appeears] bajado {ruta}")
    return rutas


def _col(campos: list[str], capa: str) -> str:
    for c in campos:
        if c.endswith(capa):
            return c
    raise KeyError(capa)


def procesar(ruta_csv: Path, tid: str | None = None) -> dict:
    """CSV de AppEEARS -> data/cache/smap/{parcela}.json. Solo calidad recomendada (bit 0 = 0)."""
    with Path(ruta_csv).open(encoding="utf-8") as fh:
        filas = list(csv.DictReader(fh))
    campos = list(filas[0].keys())
    pares = [(_col(campos, CAPAS[0]), _col(campos, CAPAS[1])), (_col(campos, CAPAS[2]), _col(campos, CAPAS[3]))]
    por_parcela: dict[str, dict[str, list[float]]] = {}
    coord: dict[str, tuple[float, float]] = {}
    celda: dict[str, dict] = {}  # fila y columna de la grilla EASE de 9 km: parcelas en la misma celda
    c_linea = next((c for c in campos if "Line_Y" in c), None)
    c_muestra = next((c for c in campos if "Sample_X" in c), None)
    intentos: dict[str, int] = {}  # días con humedad calculada pero sin calidad recomendada
    for f in filas:
        pid, fecha = f["ID"], f["Date"][:10]
        por_parcela.setdefault(pid, {})
        try:
            coord.setdefault(pid, (float(f["Latitude"]), float(f["Longitude"])))
        except (KeyError, TypeError, ValueError):
            pass
        if c_linea and c_muestra and pid not in celda:
            try:
                celda[pid] = {"linea": int(float(f[c_linea])), "muestra": int(float(f[c_muestra])),
                              "grilla": "EASE-Grid 2.0, 9 km"}
            except (TypeError, ValueError):
                pass
        vals = []
        for c_sm, c_q in pares:
            try:
                sm, q = float(f[c_sm]), int(float(f[c_q]))
            except (TypeError, ValueError):
                continue
            if sm >= 0 and q != 65534 and (q & 1):
                intentos[pid] = intentos.get(pid, 0) + 1
            if sm < 0 or q == 65534 or (q & 1):
                continue
            vals.append(sm)
        if vals:
            por_parcela[pid][fecha] = vals
    salida = {}
    proc = cache.procedencia(url=f"{API}/task (point)", producto="SMAP L3 mejorado SPL3SMP_E vía AppEEARS",
                             version="006", nota=f"Tarea {tid or '?'}; humedad AM y PM promediadas por día")
    for pid, dias in por_parcela.items():
        diario = {d: statistics.mean(v) for d, v in sorted(dias.items())}
        anual: dict[int, list[float]] = {}
        for d, v in diario.items():
            if d[5:7] in ("07", "08"):
                anual.setdefault(int(d[:4]), []).append(v)
        med_anio = {a: round(statistics.median(v), 3) for a, v in anual.items() if len(v) >= 10}
        if not med_anio:
            # Se guarda igual, rotulado: el motor debe decir por qué no hay SMAP, no «falta la descarga».
            datos = {"jul_ago_mediana": None, "unidad": "m3/m3", "dias_validos": len(diario),
                     "mediciones_sin_calidad_recomendada": intentos.get(pid, 0), "resolucion": "9 km",
                     "motivo": ("La celda de 9 km de SMAP no tiene ningún dato con calidad recomendada "
                                + ("en todo el registro" if not diario else "en julio-agosto")
                                + f" ({intentos.get(pid, 0)} mediciones descartadas por la bandera de calidad).")}
            if pid in coord:
                datos["lat"], datos["lon"] = round(coord[pid][0], 5), round(coord[pid][1], 5)
            if pid in celda:
                datos["celda"] = celda[pid]
            cache.guardar(cache.CACHE / "smap" / f"{pid}.json", datos, proc)
            salida[pid] = datos
            print(f"[smap {pid}] {datos['motivo']}")
            continue
        valores = sorted(med_anio.values())
        ultimo = max(med_anio)
        percentil = round(100 * sum(1 for v in valores if v <= med_anio[ultimo]) / len(valores))
        otros = [v for a, v in med_anio.items() if a != 2018]
        anom = None
        if 2018 in med_anio and len(otros) >= 3 and statistics.pstdev(otros) > 0:
            anom = round((med_anio[2018] - statistics.mean(otros)) / statistics.pstdev(otros), 2)
        datos = {"jul_ago_mediana": round(statistics.median([v for vs in anual.values() for v in vs]), 3),
                 "unidad": "m3/m3", "por_anio_jul_ago": med_anio, "anio_ultimo": ultimo, "percentil": percentil,
                 "anomalia_2018_de": anom, "periodo": f"{min(med_anio)}-{max(med_anio)}",
                 "dias_validos": len(diario), "resolucion": "9 km", "calidad": "retrieval_qual_flag bit 0 = 0 (recomendada)"}
        if pid in coord:
            datos["lat"], datos["lon"] = round(coord[pid][0], 5), round(coord[pid][1], 5)
        if pid in celda:
            datos["celda"] = celda[pid]
        cache.guardar(cache.CACHE / "smap" / f"{pid}.json", datos, proc)
        salida[pid] = datos
        print(f"[smap {pid}] jul-ago mediana {datos['jul_ago_mediana']} m3/m3, percentil {percentil} ({ultimo}), "
              f"anomalía 2018 {anom} DE, {len(diario)} días válidos")
    return salida


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("accion", choices=["enviar", "esperar", "procesar", "todo"])
    ap.add_argument("arg", nargs="?")
    ap.add_argument("--fin", default=time.strftime("%m-%d-%Y"))
    a = ap.parse_args()
    try:
        if a.accion == "procesar":
            procesar(Path(a.arg))
            sys.exit(0)
        tok = login()
        try:
            if a.accion in ("enviar", "todo"):
                tid = enviar(tok, a.fin)
            else:
                tid = a.arg
            if a.accion in ("esperar", "todo"):
                if esperar(tok, tid) == "done":
                    for ruta in bajar(tok, tid):
                        if PRODUCTO.replace(".", "-") in ruta.name or "results" in ruta.name:
                            procesar(ruta, tid)
        finally:
            logout(tok)
    except (cache.SinRed, RuntimeError) as e:
        sys.exit(str(e))
