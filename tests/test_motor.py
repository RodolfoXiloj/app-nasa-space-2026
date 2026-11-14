"""Detección satelital, clima y puntajes con datos sintéticos de resultado conocido."""
import math
from datetime import date, timedelta

from motor import clima, confianza, deteccion


# ---------------------------------------------------------------- detección
def test_meses_desnudos_ciclos_y_calidad(resultado_sintetico):
    det = resultado_sintetico["deteccion"]
    assert det["meses_desnudos"] == [1, 2, 3, 4]
    assert det["ciclos"]["mediana"] == 2
    assert det["periodo"] == "2021-2025"
    assert 80 < det["calidad"]["pct_validos"] < 100  # hay nubes en junio de los años impares


def test_quemas_solo_cuentan_vegetacion_cercana_en_enero_mayo(resultado_sintetico):
    q = resultado_sintetico["deteccion"]["quemas"]
    # Cuentan 2020 (300 m) y 2022 (450 m). No cuentan: 800 m, volcán, julio, confianza baja.
    assert q["anios_con_quema"] == 2
    assert q["anios_observados"] == 14
    assert q["meses_con_quema"] == [3, 4]
    assert sum(d["cuenta"] for d in q["detecciones"]) == 2


def test_prominencias_como_scipy():
    # dos picos: 0.75 (prominencia 0.75-0.30) y 0.72 (prominencia 0.72-0.55)
    v = [0.22, 0.36, 0.60, 0.75, 0.55, 0.60, 0.72, 0.60, 0.40, 0.30]
    p = dict(deteccion.prominencias(v))
    assert math.isclose(p[3], 0.45, abs_tol=1e-9)
    assert math.isclose(p[6], 0.17, abs_tol=1e-9)


# ---------------------------------------------------------------- clima
def test_hargreaves_da_valores_razonables():
    ra = clima.ra_mm(14.8, 172)  # junio, trópico: ~15-16 mm/día
    assert 14 < ra < 17
    et0 = clima.et0_hargreaves(32, 20, ra)
    assert 4 < et0 < 6


def test_kc_sigue_las_etapas_de_fao56():
    maiz = {"kc": {"ini": 0.3, "med": 1.2, "fin": 0.35}, "etapas_dias": [20, 35, 40, 25]}
    assert clima.kc_dia(maiz, 0) == 0.3
    assert math.isclose(clima.kc_dia(maiz, 20 + 17.5), 0.75)
    assert clima.kc_dia(maiz, 60) == 1.2
    assert math.isclose(clima.kc_dia(maiz, 119), 1.2 + 24 / 25 * (0.35 - 1.2))


def _serie(p_mm: float, anio: int = 2010) -> dict:
    d, s = date(anio, 1, 1), {}
    while d.year == anio:
        s[d] = (p_mm, 5.0)
        d += timedelta(days=1)
    return s


def test_balance_sin_lluvia_y_con_mucha_lluvia():
    maiz = {"kc": {"ini": 0.3, "med": 1.2, "fin": 0.35}, "etapas_dias": [20, 35, 40, 25], "ky": 1.25}
    ciclo = [{"cultivo": "maiz", "siembra_mes": 5, "siembra_dia": 25}]
    seco = clima.balance_rotacion(_serie(0.0), [2010], ciclo, {"maiz": maiz})[0]
    mojado = clima.balance_rotacion(_serie(20.0), [2010], ciclo, {"maiz": maiz})[0]
    assert seco["deficit"] > 0.85          # solo la reserva inicial de 25 mm
    assert seco["perdida"] == 1.0          # Ky x déficit, acotado a 1
    assert mojado["deficit"] == 0.0


def test_racha_seca_de_la_canicula():
    s = _serie(5.0)
    for k in range(20):
        s[date(2010, 7, 1) + timedelta(days=k)] = (0.0, 5.0)
    assert clima.racha_seca(s, 2010) == 20


def test_canicula_sintetica(resultado_sintetico):
    can = resultado_sintetico["clima"]["canicula"]
    assert can["anios_total"] == 25
    assert can["anios_racha_larga"] == 9   # años divisibles entre 3 de 2001 a 2025: 2001, 2004, ..., 2025


# ---------------------------------------------------------------- puntajes y selección
def test_la_leguminosa_cubre_meses_desnudos(resultado_sintetico):
    act, leg, _tol = resultado_sintetico["rotaciones"]
    n = {r["id"]: next(e["valor"] for e in r["evidencia"] if e["dato"].startswith("Meses de suelo desnudo"))
         for r in (act, leg)}
    assert n[act["id"]] == 4
    assert n[leg["id"]] < n[act["id"]]    # la mejor leguminosa o cobertura cubre parte de la época seca
    assert leg["puntajes"]["suelo"] > act["puntajes"]["suelo"]


def test_tolerante_a_sequia_pierde_menos_por_agua(resultado_sintetico):
    act, _leg, tol = resultado_sintetico["rotaciones"]
    assert tol["deficit"]["perdida_mediana_pct"] <= act["deficit"]["perdida_mediana_pct"]


def test_total_respeta_la_prioridad(resultado_sintetico):
    pesos = resultado_sintetico["pesos"]["por_prioridad"]["agua"]
    for r in resultado_sintetico["rotaciones"]:
        p = r["puntajes"]
        assert p["total"] == round(pesos["agua"] * p["agua"] + pesos["suelo"] * p["suelo"] + pesos["plagas"] * p["plagas"])


# ---------------------------------------------------------------- confianza
def test_confianza_niveles():
    assert confianza.evaluar(90, 5, True)["nivel"] == "alta"
    assert confianza.evaluar(90, 20, True)["nivel"] == "media"
    assert confianza.evaluar(90, None, True)["nivel"] == "media"   # solo POWER: no pasa de media
    assert confianza.evaluar(90, 5, False)["nivel"] == "baja"      # sin SMAP
    assert confianza.evaluar(50, 5, True)["nivel"] == "baja"
    assert confianza.evaluar(90, 35, True)["nivel"] == "baja"
    assert "SMAP" in confianza.evaluar(90, 5, False)["motivo"]
    m = confianza.evaluar(90, 5, False, detalle_smap="La celda de 9 km de SMAP no tiene ningún dato con calidad recomendada.")
    assert m["nivel"] == "baja" and "calidad recomendada" in m["motivo"] and "falta la descarga" not in m["motivo"]
