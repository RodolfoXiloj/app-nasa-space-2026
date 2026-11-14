"""Futuros de NASA (NEX-GDDP-CMIP6): conversión del CSV de Earth Engine y conteo por rotación."""
import csv

from motor import futuros
from motor.recomendar import recomendar
from pipeline.clientes import cmip6


def _csv(tmp_path, filas):
    ruta = tmp_path / "cambios.csv"
    with ruta.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["parcela", "modelo", "escenario", "pr_may_oct_mm_dia", "pr_jun_ago_mm_dia", "tas_may_oct_c"])
        w.writerows(filas)
    return ruta


def test_convertir_calcula_cambios_contra_el_pasado_del_mismo_modelo(tmp_path):
    ruta = _csv(tmp_path, [
        ["jocotan", "M1", "historical", 8.0, 6.0, 24.0],
        ["jocotan", "M1", "ssp245", 7.2, 4.8, 25.5],
        ["jocotan", "M2", "historical", 10.0, 9.0, 23.0],
        ["jocotan", "M2", "ssp585", 11.0, 9.0, 25.0],
        ["jocotan", "M3", "ssp245", 5.0, 4.0, 26.0],  # sin histórico: se descarta
    ])
    d = cmip6.convertir(ruta)["datos"]["parcelas"]["jocotan"]
    assert d["ssp245"] == [{"modelo": "M1", "lluvia_pct": -10.0, "lluvia_canicula_pct": -20.0, "temp_c": 1.5}]
    assert d["ssp585"][0]["lluvia_pct"] == 10.0 and d["ssp585"][0]["temp_c"] == 2.0


def test_escenarios_extra_no_cambian_el_contrato_ni_la_tarjeta():
    a = recomendar("jocotan")
    b = recomendar("jocotan", escenarios_extra=[(-15.0, 2.0)])
    assert "escenarios_extra" not in a
    assert b["texto_tarjeta"] == a["texto_tarjeta"]
    assert b["escenarios"] == a["escenarios"]
    assert [r["puntajes"] for r in b["rotaciones"]] == [r["puntajes"] for r in a["rotaciones"]]


def test_futuro_igual_a_hoy_aguanta_y_uno_muy_seco_no():
    cambios = {"ssp245": [
        {"modelo": "igual", "lluvia_pct": 0.0, "lluvia_canicula_pct": 0.0, "temp_c": 0.0},
        {"modelo": "muy_seco", "lluvia_pct": -45.0, "lluvia_canicula_pct": -60.0, "temp_c": 3.0},
    ]}
    d = futuros.futuros_parcela("jocotan", cambios)
    e = d["escenarios"]["ssp245"]
    actual = next(r for r in e["rotaciones"] if r["es_actual"])
    filas = {m["modelo"]: m for m in e["modelos"]}
    assert filas["igual"]["aguanta"][actual["id"]] is True  # hoy contra hoy: igual, aguanta
    assert filas["muy_seco"]["aguanta"][actual["id"]] is False
    assert all(0 <= r["futuros_que_aguanta"] <= e["n_modelos"] for r in e["rotaciones"])
    assert e["n_modelos"] == 2 and e["modelos_mas_secos"] == 1
