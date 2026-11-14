"""Caché en disco con procedencia.

Todo archivo de data/cache/ tiene la forma:
    {"procedencia": {...}, "datos": ...}
con la URL, la fecha de descarga, el producto y su versión. Así cualquier cifra de la
tarjeta se puede rastrear hasta su origen.
"""
from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
import yaml

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
CACHE = DATA / "cache"
RAW_BIG = DATA / "raw_big"

AGENTE = "milpa-resiliente/0.1 (NASA Space Apps 2026; uso academico)"


def cargar_env(ruta: Path | None = None) -> None:
    """Lee el .env de la raíz (gitignored) sin pisar variables ya definidas en el entorno.

    Solo el pipeline usa claves; el motor nunca lee .env. Los valores no se imprimen ni se
    guardan en la caché.
    """
    ruta = ruta or (RAIZ / ".env")
    if not ruta.exists():
        return
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        k, v = linea.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v


def secreto(nombre: str) -> str | None:
    """Valor de una clave del entorno o del .env; None si falta o está vacía."""
    cargar_env()
    v = os.environ.get(nombre, "").strip()
    return v or None


def ocultar(texto: str, *secretos: str | None) -> str:
    """Reemplaza las claves por *** para que no aparezcan en logs, errores ni caché."""
    for s in secretos:
        if s:
            texto = texto.replace(s, "***")
    return texto


class SinRed(RuntimeError):
    """Se intentó bajar datos sin MILPA_ONLINE=1."""


def online() -> bool:
    return os.environ.get("MILPA_ONLINE", "0") == "1"


def exigir_red() -> None:
    if not online():
        raise SinRed("La red está apagada. Use MILPA_ONLINE=1 para bajar datos.")


def ahora_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def procedencia(url: str, producto: str, version: str | None = None, nota: str | None = None, **extra: Any) -> dict:
    p = {"url": url, "fecha_descarga": ahora_utc(), "producto": producto, "version": version}
    if nota:
        p["nota"] = nota
    p.update(extra)
    return p


def guardar(ruta: Path, datos: Any, proc: dict) -> Path:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    tmp = ruta.with_suffix(ruta.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump({"procedencia": proc, "datos": datos}, f, ensure_ascii=False, separators=(",", ":"))
    tmp.replace(ruta)
    return ruta


def leer(ruta: Path) -> dict:
    with ruta.open(encoding="utf-8") as f:
        return json.load(f)


def get(url: str, params: dict | None = None, headers: dict | None = None, timeout: int = 120,
        intentos: int = 4, espera: float = 5.0) -> requests.Response:
    """GET con reintentos y espera creciente. Exige MILPA_ONLINE=1."""
    exigir_red()
    h = {"User-Agent": AGENTE}
    if headers:
        h.update(headers)
    ultimo: Exception | None = None
    for i in range(intentos):
        try:
            r = requests.get(url, params=params, headers=h, timeout=timeout)
            if r.status_code == 429 or r.status_code >= 500:
                raise requests.HTTPError(f"HTTP {r.status_code}", response=r)
            r.raise_for_status()
            return r
        except (requests.RequestException,) as e:  # noqa: PERF203
            ultimo = e
            if isinstance(e, requests.HTTPError) and e.response is not None and 400 <= e.response.status_code < 500 \
                    and e.response.status_code != 429:
                raise
            time.sleep(espera * (2 ** i))
    assert ultimo is not None
    raise ultimo


def cargar_parcelas() -> list[dict]:
    with (DATA / "parcelas.yaml").open(encoding="utf-8") as f:
        return yaml.safe_load(f)["parcelas"]


def parcela(pid: str) -> dict:
    for p in cargar_parcelas():
        if p["id"] == pid:
            return p
    raise KeyError(f"No existe la parcela {pid!r} en data/parcelas.yaml")
