"""Lo que ve cada satélite alrededor de una parcela: el borde de la celda o el radio de cada producto.

Geometría de las mallas, sin red y con la biblioteca estándar:
- MODIS MOD13Q1: malla sinusoidal de MODIS (esfera de radio 6 371 007.181 m), píxel de 231.656 m.
- SMAP SPL3SMP_E: EASE-Grid 2.0 global de 9 km (cilíndrica de áreas iguales sobre WGS84, paralelo 30°).
- CHIRPS v3: malla regular de 0.05°.
- NASA POWER: malla de MERRA-2, 0.5° de latitud por 0.625° de longitud.
- FIRMS: el radio que usa el motor para contar quemas (deteccion.quemas.radio_m).
- La parcela familiar promedio del Corredor Seco: 0.35 ha (FAO/PMA 2010), dibujada como un círculo de
  la misma superficie alrededor del punto. Es una referencia de tamaño, no los linderos de la parcela.
"""
from __future__ import annotations

import math

# MODIS: malla sinusoidal (MODLAND).
R_MODIS = 6371007.181
TESELA_MODIS = 1111950.5196666666
PIXEL_MODIS = TESELA_MODIS / 4800  # 231.656 m
X0_MODIS, Y0_MODIS = -20015109.354, 10007554.677

# EASE-Grid 2.0 global, 9 km (EPSG:6933).
A_WGS84 = 6378137.0
E2_WGS84 = 0.0066943799901413165
CELDA_EASE = 9008.055210146
COLS_EASE, FILAS_EASE = 3856, 1624

CHIRPS_GRADOS = 0.05
POWER_LAT, POWER_LON = 0.5, 0.625
PARCELA_FAMILIAR_HA = 0.35
R_TIERRA = 6371008.8  # radio medio, para superficies de celdas en grados


def _r(x: float) -> float:
    return round(x, 6)


# ---------------- MODIS
def celda_modis(lat: float, lon: float) -> dict:
    x = R_MODIS * math.radians(lon) * math.cos(math.radians(lat))
    y = R_MODIS * math.radians(lat)
    col = math.floor((x - X0_MODIS) / PIXEL_MODIS)
    fila = math.floor((Y0_MODIS - y) / PIXEL_MODIS)

    def a_geo(xx: float, yy: float) -> list[float]:
        la = math.degrees(yy / R_MODIS)
        lo = math.degrees(xx / (R_MODIS * math.cos(math.radians(la))))
        return [_r(la), _r(lo)]

    xa, ya = X0_MODIS + col * PIXEL_MODIS, Y0_MODIS - fila * PIXEL_MODIS
    xb, yb = xa + PIXEL_MODIS, ya - PIXEL_MODIS
    return {"fila": fila, "col": col, "lado_m": round(PIXEL_MODIS, 2),
            "area_ha": round(PIXEL_MODIS ** 2 / 1e4, 2),
            "poligono": [a_geo(xa, ya), a_geo(xb, ya), a_geo(xb, yb), a_geo(xa, yb)]}


# ---------------- EASE-Grid 2.0
_E = math.sqrt(E2_WGS84)


def _q(phi: float) -> float:
    s = math.sin(phi)
    return (1 - E2_WGS84) * (s / (1 - E2_WGS84 * s * s) - (1 / (2 * _E)) * math.log((1 - _E * s) / (1 + _E * s)))


_K0 = math.cos(math.radians(30)) / math.sqrt(1 - E2_WGS84 * math.sin(math.radians(30)) ** 2)
X0_EASE = -COLS_EASE / 2 * CELDA_EASE
Y0_EASE = FILAS_EASE / 2 * CELDA_EASE


def _ease_xy(lat: float, lon: float) -> tuple[float, float]:
    return A_WGS84 * _K0 * math.radians(lon), A_WGS84 * _q(math.radians(lat)) / (2 * _K0)


def _ease_geo(x: float, y: float) -> list[float]:
    q = 2 * _K0 * y / A_WGS84
    lo, hi = -math.pi / 2, math.pi / 2
    for _ in range(80):  # bisección: _q crece con la latitud
        mid = (lo + hi) / 2
        if _q(mid) < q:
            lo = mid
        else:
            hi = mid
    return [_r(math.degrees((lo + hi) / 2)), _r(math.degrees(x / (A_WGS84 * _K0)))]


def celda_smap(lat: float, lon: float) -> dict:
    x, y = _ease_xy(lat, lon)
    col = math.floor((x - X0_EASE) / CELDA_EASE)
    fila = math.floor((Y0_EASE - y) / CELDA_EASE)
    xa, ya = X0_EASE + col * CELDA_EASE, Y0_EASE - fila * CELDA_EASE
    xb, yb = xa + CELDA_EASE, ya - CELDA_EASE
    return {"fila": fila, "col": col, "lado_m": round(CELDA_EASE, 1), "area_ha": round(CELDA_EASE ** 2 / 1e4),
            "poligono": [_ease_geo(xa, ya), _ease_geo(xb, ya), _ease_geo(xb, yb), _ease_geo(xa, yb)]}


# ---------------- mallas regulares en grados
def _area_ha(sur: float, norte: float, oeste: float, este: float) -> float:
    return R_TIERRA ** 2 * math.radians(este - oeste) * (math.sin(math.radians(norte)) - math.sin(math.radians(sur))) / 1e4


def _rect(sur: float, norte: float, oeste: float, este: float) -> list[list[float]]:
    return [[_r(norte), _r(oeste)], [_r(norte), _r(este)], [_r(sur), _r(este)], [_r(sur), _r(oeste)]]


def celda_chirps(lat: float, lon: float) -> dict:
    sur = math.floor(lat / CHIRPS_GRADOS) * CHIRPS_GRADOS
    oeste = math.floor(lon / CHIRPS_GRADOS) * CHIRPS_GRADOS
    norte, este = sur + CHIRPS_GRADOS, oeste + CHIRPS_GRADOS
    return {"lat_centro": round(sur + CHIRPS_GRADOS / 2, 3), "lon_centro": round(oeste + CHIRPS_GRADOS / 2, 3),
            "area_ha": round(_area_ha(sur, norte, oeste, este)), "poligono": _rect(sur, norte, oeste, este)}


def celda_power(lat: float, lon: float) -> dict:
    lat_c = round(lat / POWER_LAT) * POWER_LAT
    lon_c = -180 + round((lon + 180) / POWER_LON) * POWER_LON
    sur, norte = lat_c - POWER_LAT / 2, lat_c + POWER_LAT / 2
    oeste, este = lon_c - POWER_LON / 2, lon_c + POWER_LON / 2
    return {"lat_centro": lat_c, "lon_centro": lon_c, "area_ha": round(_area_ha(sur, norte, oeste, este)),
            "poligono": _rect(sur, norte, oeste, este)}


def huellas(lat: float, lon: float, radio_firms_m: float, smap_disponible: bool) -> list[dict]:
    """Las huellas de una parcela, de la más chica a la más grande."""
    r_parcela = math.sqrt(PARCELA_FAMILIAR_HA * 1e4 / math.pi)
    modis, smap = celda_modis(lat, lon), celda_smap(lat, lon)
    chirps, power = celda_chirps(lat, lon), celda_power(lat, lon)
    return [
        {"id": "parcela", "forma": "circulo", "radio_m": round(r_parcela, 1), "area_ha": PARCELA_FAMILIAR_HA,
         "fuente_id": "fao_pma_2010"},
        {"id": "modis", "forma": "poligono", "poligono": modis["poligono"], "area_ha": modis["area_ha"],
         "lado_m": modis["lado_m"], "fuente_id": "modis_mod13q1"},
        {"id": "firms", "forma": "circulo", "radio_m": radio_firms_m,
         "area_ha": round(math.pi * radio_firms_m ** 2 / 1e4, 1), "fuente_id": "firms_viirs"},
        {"id": "chirps", "forma": "poligono", "poligono": chirps["poligono"], "area_ha": chirps["area_ha"],
         "fuente_id": "chirps"},
        {"id": "smap", "forma": "poligono", "poligono": smap["poligono"], "area_ha": smap["area_ha"],
         "lado_m": smap["lado_m"], "fuente_id": "smap", "con_datos": smap_disponible},
        {"id": "power", "forma": "poligono", "poligono": power["poligono"], "area_ha": power["area_ha"],
         "fuente_id": "nasa_power"},
    ]
