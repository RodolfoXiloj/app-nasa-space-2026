"""Paso 2b — puntajes de 0 a 100 por rotación (agua, suelo, plagas) y total según la prioridad.

Todos los pesos y puntos son VALORES INICIALES, escritos aquí para que se puedan discutir y
revisar con un agrónomo. Cada puntaje guarda en `trazabilidad` qué dato lo produjo.
"""
from __future__ import annotations

import statistics

from motor import clima

PESOS = {
    "agua": {"agua": 0.50, "suelo": 0.25, "plagas": 0.25},
    "suelo": {"agua": 0.25, "suelo": 0.50, "plagas": 0.25},
    "plagas": {"agua": 0.25, "suelo": 0.25, "plagas": 0.50},
}

PUNTOS = {
    # agua
    "canicula_max": 20.0,          # resta máxima si todos los años tuvieran canícula larga, con Ky de maíz
    "ky_referencia": 1.25,         # Ky del maíz (FAO-33)
    # suelo
    "por_mes_desnudo": 6.0,
    "por_mes_poca_cobertura": 3.0,  # la mitad que un mes desnudo
    "factor_pendiente": 1.5,       # multiplica la resta por mes desnudo si la pendiente es fuerte
    "pendiente_fuerte_pct": 15.0,
    "quema_max": 30.0,             # resta si hubo quema todos los años observados
    "leguminosa": 5.0,
    "cobertura": 10.0,
    "rastrojo_en_pie": 10.0,
    # plagas
    "plagas_base": 40.0,
    "alterna_familias": 30.0,
    "asociacion": 10.0,
    "cobertura_plagas": 10.0,
    "monocultivo": -20.0,
}


def _acotar(x: float) -> float:
    return round(max(0.0, min(100.0, x)))


def puntaje_agua(balance: list[dict], frac_canicula: float, ky_canicula: float) -> tuple[float, dict, list[str]]:
    perdidas = [b["perdida"] for b in balance]
    deficits = [b["deficit"] for b in balance]
    perdida_med = statistics.median(perdidas)
    d_med, d25, d75 = clima.cuartiles(deficits)
    resta_can = PUNTOS["canicula_max"] * frac_canicula * (ky_canicula / PUNTOS["ky_referencia"])
    valor = _acotar(100 * (1 - perdida_med) - resta_can)
    deficit = {"mediana_pct": round(100 * d_med), "p25_pct": round(100 * d25), "p75_pct": round(100 * d75)}
    traza = [
        f"Déficit de agua mediano {deficit['mediana_pct']} % (entre {deficit['p25_pct']} y {deficit['p75_pct']} % la mitad de los años), "
        f"balance diario con NASA POWER {balance[0]['anio']}-{balance[-1]['anio']} y ET0 de Hargreaves (FAO-56)",
        f"Pérdida relativa esperada = Ky x déficit (FAO-33): mediana {round(100 * perdida_med)} %",
        f"Resta por canícula larga: {round(resta_can, 1)} puntos (frecuencia {round(100 * frac_canicula)} %, Ky {ky_canicula})",
    ]
    return valor, deficit, traza


def puntaje_suelo(meses_desnudos: int, pendiente_pct: float | None, frac_quema: float, rot: dict,
                  meses_poca: int = 0) -> tuple[float, list[str]]:
    fuerte = pendiente_pct is not None and pendiente_pct > PUNTOS["pendiente_fuerte_pct"]
    factor = PUNTOS["factor_pendiente"] if fuerte else 1.0
    por_mes = PUNTOS["por_mes_desnudo"] * factor
    por_mes_poca = PUNTOS["por_mes_poca_cobertura"] * factor
    v = 100 - por_mes * meses_desnudos - por_mes_poca * meses_poca - PUNTOS["quema_max"] * frac_quema
    traza = [f"{meses_desnudos} meses de suelo desnudo x {por_mes} puntos"
             + (f" (pendiente fuerte: {pendiente_pct} %)" if fuerte else ""),
             f"{meses_poca} meses de poca cobertura x {por_mes_poca} puntos",
             f"Quema: resta {round(PUNTOS['quema_max'] * frac_quema, 1)} puntos"]
    for bandera in ("leguminosa", "cobertura", "rastrojo_en_pie"):
        if rot.get(bandera):
            v += PUNTOS[bandera]
            traza.append(f"Suma {PUNTOS[bandera]} por {bandera.replace('_', ' ')}")
    return _acotar(v), traza


def puntaje_plagas(rot: dict, cultivos: dict) -> tuple[float, list[str]]:
    fam_principal = [cultivos[c["cultivo"]]["familia"] for c in rot["ciclos"]]
    v = PUNTOS["plagas_base"]
    traza = [f"Base {PUNTOS['plagas_base']}"]
    if len(fam_principal) > 1 and any(a != b for a, b in zip(fam_principal, fam_principal[1:])):
        v += PUNTOS["alterna_familias"]
        traza.append(f"Suma {PUNTOS['alterna_familias']}: alterna familias entre ciclos ({' -> '.join(fam_principal)})")
    cultivos_todos = [c["cultivo"] for c in rot["ciclos"]]
    if len(set(cultivos_todos)) == 1 and not any(c.get("asociados") for c in rot["ciclos"]):
        v += PUNTOS["monocultivo"]
        traza.append(f"Resta {abs(PUNTOS['monocultivo'])}: el mismo cultivo cada año sin asociación")
    for c in rot["ciclos"]:
        fam = cultivos[c["cultivo"]]["familia"]
        if any(cultivos[a]["familia"] != fam for a in c.get("asociados", [])):
            v += PUNTOS["asociacion"]
            traza.append(f"Suma {PUNTOS['asociacion']}: asocia familias distintas en {c['temporada']}")
            break
    if rot.get("cobertura"):
        v += PUNTOS["cobertura_plagas"]
        traza.append(f"Suma {PUNTOS['cobertura_plagas']}: cobertura que rompe el ciclo de plagas")
    return _acotar(v), traza


def total(p: dict, prioridad: str) -> float:
    w = PESOS[prioridad]
    return round(sum(w[k] * p[k] for k in ("agua", "suelo", "plagas")))
