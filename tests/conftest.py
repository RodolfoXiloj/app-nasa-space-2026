"""Datos sintéticos para probar el motor sin red y sin depender de la caché real."""
from __future__ import annotations

import json
import shutil
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

# NDVI mensual de una milpa típica: suelo desnudo enero-abril, dos picos (primera y postrera).
NDVI_MES = {1: 0.30, 2: 0.25, 3: 0.20, 4: 0.22, 5: 0.36, 6: 0.60, 7: 0.75, 8: 0.55,
            9: 0.60, 10: 0.72, 11: 0.60, 12: 0.40}


def _ndvi_cache() -> dict:
    filas = []
    for anio in range(2019, 2026):
        d = date(anio, 1, 1)
        while d.year == anio:
            cal = 3 if (d.month == 6 and d.day < 17 and anio % 2) else 0  # algunas nubes
            filas.append([d.isoformat(), NDVI_MES[d.month], cal])
            d += timedelta(days=16)
    return {"procedencia": {"url": "sintetico", "fecha_descarga": "2026-11-13T00:00:00Z", "producto": "prueba"},
            "datos": {"columnas": ["fecha", "ndvi", "pixel_reliability"], "filas": filas}}


def _firms_cache() -> dict:
    det = [
        {"fecha": "2020-03-10", "hora": "1900", "lat": 14.5, "lon": -89.5, "distancia_m": 300.0, "confianza": "n", "frp": 3.0, "tipo": 0},
        {"fecha": "2022-04-02", "hora": "1900", "lat": 14.5, "lon": -89.5, "distancia_m": 450.0, "confianza": "h", "frp": 5.0, "tipo": 0},
        {"fecha": "2023-03-01", "hora": "1900", "lat": 14.5, "lon": -89.5, "distancia_m": 800.0, "confianza": "n", "frp": 2.0, "tipo": 0},
        {"fecha": "2024-03-01", "hora": "1900", "lat": 14.5, "lon": -89.5, "distancia_m": 100.0, "confianza": "n", "frp": 9.0, "tipo": 1},
        {"fecha": "2021-07-15", "hora": "1900", "lat": 14.5, "lon": -89.5, "distancia_m": 200.0, "confianza": "n", "frp": 2.0, "tipo": 0},
        {"fecha": "2019-02-11", "hora": "1900", "lat": 14.5, "lon": -89.5, "distancia_m": 250.0, "confianza": "l", "frp": 1.0, "tipo": 0},
    ]
    return {"procedencia": {"url": "sintetico", "fecha_descarga": "2026-11-13T00:00:00Z", "producto": "prueba"},
            "datos": {"anios_observados": list(range(2012, 2026)), "detecciones": det}}


def _power_cache() -> dict:
    filas = []
    d = date(2001, 1, 1)
    while d.year <= 2025:
        if 5 <= d.month <= 10:
            p = 7.0
            # canícula larga (25 días sin lluvia) uno de cada tres años
            if d.year % 3 == 0 and (date(d.year, 7, 5) <= d <= date(d.year, 7, 29)):
                p = 0.0
        else:
            p = 0.3
        filas.append([d.strftime("%Y%m%d"), p, 32.0, 20.0, 26.0, 0.5])
        d += timedelta(days=1)
    return {"procedencia": {"url": "sintetico", "fecha_descarga": "2026-11-13T00:00:00Z", "producto": "prueba"},
            "datos": {"columnas": ["clave", "PRECTOTCORR", "T2M_MAX", "T2M_MIN", "T2M", "GWETROOT"], "filas": filas}}


@pytest.fixture(scope="session")
def base_sintetica(tmp_path_factory) -> str:
    base = tmp_path_factory.mktemp("data")
    for y in ("rotaciones.yaml", "cultivos.yaml", "zarc_citas.yaml", "glosario.yaml", "fuentes.yaml"):
        shutil.copyfile(RAIZ / "data" / y, base / y)
    (base / "parcelas.yaml").write_text(
        "parcelas:\n  - {id: sint, nombre: Parcela sintética, municipio: Jocotán, departamento: Chiquimula,"
        " lat: 14.5, lon: -89.5, provisional: true, nota: prueba}\n", encoding="utf-8")
    cache = base / "cache"
    for rel, obj in {"ndvi/sint.json": _ndvi_cache(), "firms/sint.json": _firms_cache(),
                     "power/sint_diario.json": _power_cache(),
                     "srtm/sint.json": {"procedencia": {"url": "sintetico", "fecha_descarga": "2026-11-13T00:00:00Z"},
                                        "datos": {"altitud_m": 800, "pendiente_pct": 20.0}}}.items():
        (cache / rel).parent.mkdir(parents=True, exist_ok=True)
        (cache / rel).write_text(json.dumps(obj), encoding="utf-8")
    return str(base)


@pytest.fixture(scope="session")
def resultado_sintetico(base_sintetica) -> dict:
    from motor.recomendar import recomendar
    return recomendar("sint", base=base_sintetica)
