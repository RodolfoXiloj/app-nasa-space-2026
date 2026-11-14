"""Lectura de data/*.yaml y data/cache/ (solo disco, nunca red)."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
CACHE = DATA / "cache"


class FaltaDato(FileNotFoundError):
    """Falta un archivo de caché obligatorio para la parcela."""


@lru_cache(maxsize=None)
def yaml_de(nombre: str, base: str | None = None) -> dict:
    ruta = Path(base or DATA) / nombre
    with ruta.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def parcelas(base: str | None = None) -> list[dict]:
    return yaml_de("parcelas.yaml", base)["parcelas"]


def parcela(pid: str, base: str | None = None) -> dict:
    for p in parcelas(base):
        if p["id"] == pid:
            return p
    raise KeyError(pid)


def rotaciones(base: str | None = None) -> list[dict]:
    return yaml_de("rotaciones.yaml", base)["rotaciones"]


def cultivos(base: str | None = None) -> dict:
    return yaml_de("cultivos.yaml", base)["cultivos"]


def zarc(base: str | None = None) -> dict:
    return yaml_de("zarc_citas.yaml", base)


def glosario(base: str | None = None) -> list[dict]:
    return yaml_de("glosario.yaml", base)["glosario"]


def fuentes(base: str | None = None) -> list[dict]:
    return yaml_de("fuentes.yaml", base)["fuentes"]


TOLERANCIA_GRADOS = 1e-4


def coordenada_de(obj: dict) -> tuple[float, float] | None:
    """Coordenada con la que se bajó una caché (None si el archivo no la guarda)."""
    d = obj.get("datos", {}) if isinstance(obj, dict) else {}
    if isinstance(d, dict) and "lat" in d and "lon" in d:
        return d["lat"], d["lon"]
    if isinstance(d, dict) and d.get("puntos"):
        return d["puntos"][0][0], d["puntos"][0][1]
    return None


def coincide(obj: dict, parcela_: dict | None) -> bool:
    if parcela_ is None:
        return True
    c = coordenada_de(obj)
    return c is None or (abs(c[0] - parcela_["lat"]) <= TOLERANCIA_GRADOS and abs(c[1] - parcela_["lon"]) <= TOLERANCIA_GRADOS)


def cache(rel: str, obligatorio: bool = True, base: str | None = None, parcela_: dict | None = None) -> dict | None:
    """Lee una caché. Con `parcela_`, rechaza la que se bajó para otra coordenada (punto movido)."""
    ruta = (Path(base) / "cache" if base else CACHE) / rel
    if not ruta.exists():
        if obligatorio:
            raise FaltaDato(f"Falta {ruta}. Corra la precarga: MILPA_ONLINE=1 python -m pipeline.precargar")
        return None
    with ruta.open(encoding="utf-8") as f:
        obj = json.load(f)
    if not coincide(obj, parcela_):
        if obligatorio:
            raise FaltaDato(f"{ruta} es de otra coordenada {coordenada_de(obj)}; la parcela está en "
                            f"({parcela_['lat']}, {parcela_['lon']}). Vuelva a correr la precarga.")
        return None
    return obj


def disponibilidad(pid: str, base: str | None = None) -> dict[str, bool]:
    """Qué cachés existen y corresponden a la coordenada actual de la parcela."""
    raiz = Path(base) / "cache" if base else CACHE
    try:
        p = parcela(pid, base)
    except KeyError:
        p = None
    out = {}
    for clave, rel in (("power_diario", f"power/{pid}_diario.json"), ("ndvi", f"ndvi/{pid}.json"),
                       ("firms", f"firms/{pid}.json"), ("srtm", f"srtm/{pid}.json"), ("suelo", f"suelo/{pid}.json"),
                       ("chirps", f"chirps/{pid}.json"), ("chirps_diario", f"chirps_diario/{pid}.json"),
                       ("smap", f"smap/{pid}.json")):
        ruta = raiz / rel
        if not ruta.exists():
            out[clave] = False
            continue
        with ruta.open(encoding="utf-8") as f:
            out[clave] = coincide(json.load(f), p)
    return out
