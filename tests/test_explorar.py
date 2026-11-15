"""El explorador de Evidence (motor/explorar.py, motor/huellas.py) dice lo mismo que el motor y la validación.

Usa la caché real del repo (sin red). Cada bloque se compara con la cifra que ya publica el sitio.
"""
from __future__ import annotations

import json
from datetime import date

import pytest

from motor import clima, datos, explorar, huellas
from motor import recomendar as rec

RAIZ = datos.RAIZ
WEB = RAIZ / "web" / "public" / "data"
PIDS = [p["id"] for p in datos.parcelas() if (WEB / "explorar" / f"{p['id']}.json").exists()]


def _json(ruta):
    return json.loads(ruta.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def exportados():
    return {pid: _json(WEB / "explorar" / f"{pid}.json") for pid in PIDS}


@pytest.fixture(scope="module")
def motor_res():
    return {pid: rec.recomendar(pid, cultivo="maiz_frijol") for pid in PIDS}


def _dentro(punto, poligono) -> bool:
    """Punto dentro de un cuadrilátero (lat, lon), por cruce de rayos."""
    y, x = punto
    dentro = False
    for i in range(len(poligono)):
        y1, x1 = poligono[i]
        y2, x2 = poligono[(i + 1) % len(poligono)]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            dentro = not dentro
    return dentro


def test_hay_un_archivo_por_parcela():
    assert len(PIDS) == 5


def test_los_archivos_estan_al_dia(exportados):
    for pid in PIDS:
        nuevo = explorar.explorar_parcela(pid)
        viejo = dict(exportados[pid])
        nuevo.pop("generado"), viejo.pop("generado")
        assert json.loads(json.dumps(nuevo)) == viejo, f"{pid}: corra python -m motor.explorar"


def test_cada_celda_contiene_su_punto(exportados):
    for pid, d in exportados.items():
        for h in d["huellas"]:
            if h["forma"] == "poligono":
                assert _dentro((d["lat"], d["lon"]), h["poligono"]), f"{pid}: {h['id']}"


def test_pixel_modis_mide_231_m():
    c = huellas.celda_modis(14.81146, -89.39433)
    assert c["lado_m"] == pytest.approx(231.66, abs=0.01)
    assert c["area_ha"] == pytest.approx(5.37, abs=0.01)


def test_celda_chirps_es_la_del_cache(exportados):
    for pid in PIDS:
        pix = datos.cache(f"chirps/{pid}.json")["datos"]["pixel"]
        c = huellas.celda_chirps(exportados[pid]["lat"], exportados[pid]["lon"])
        assert (c["lat_centro"], c["lon_centro"]) == (pix["lat_centro"], pix["lon_centro"]), pid


def test_ease_grid_cubre_el_mundo():
    # El borde oeste de la malla está en -180° y el norte cerca de 85.04°, como en la definición de EASE-Grid 2.0.
    assert huellas._ease_geo(huellas.X0_EASE, 0)[1] == pytest.approx(-180, abs=1e-6)
    assert huellas._ease_geo(0, huellas.Y0_EASE)[0] == pytest.approx(85.0445, abs=1e-3)


def test_cuatro_de_cinco_parcelas_comparten_la_celda_de_power(exportados):
    # README: «NASA POWER puts four of the five plots in the same ~50 km cell».
    celdas = [tuple(map(tuple, next(h for h in d["huellas"] if h["id"] == "power")["poligono"])) for d in exportados.values()]
    assert max(celdas.count(c) for c in celdas) == 4


def test_radio_de_quema_es_el_del_motor(exportados, motor_res):
    for pid in PIDS:
        firms = next(h for h in exportados[pid]["huellas"] if h["id"] == "firms")
        assert firms["radio_m"] == motor_res[pid]["deteccion"]["quemas"]["radio_m"]


def test_canicula_dia_a_dia_da_las_rachas_del_motor(exportados, motor_res):
    for pid in PIDS:
        can = exportados[pid]["canicula"]
        rachas = {x["anio"]: x["racha_dias"] for x in motor_res[pid]["clima"]["canicula"]["por_anio"]}
        assert {x["anio"]: x["racha_dias"] for x in can["sat"]} == rachas, pid
        for x in can["sat"] + can.get("rnl", []):
            mas_larga = max((len(t) for t in x["dias"].split("0")), default=0)
            assert "?" not in x["dias"] and mas_larga == x["racha_dias"], (pid, x["anio"])
            assert len(x["dias"]) == (date(2001, 8, 31) - date(2001, 6, 15)).days + 1


def test_reparto_rnl_coincide_con_la_sensibilidad(exportados):
    sens = {p["id"]: p for p in datos.cache("validacion/sensibilidad_canicula.json")["datos"]["parcelas"]}
    umbral = clima.SUPUESTOS["racha_larga_dias"]
    for pid in PIDS:
        for version in ("sat", "rnl"):
            largos = [x["anio"] for x in exportados[pid]["canicula"][version] if x["racha_dias"] > umbral]
            assert largos == sens[pid][version]["anios"], (pid, version)


def test_lluvia_jul_ago_coincide_con_la_validacion(exportados):
    obs = {x["id"]: x for x in _json(WEB / "validacion.json")["observacion_2026"]["lluvia_chirps"]}
    for pid in PIDS:
        ll, o = exportados[pid]["lluvia_jul_ago"], obs[pid]
        assert ll["total_2026_mm"] == pytest.approx(o["mm_2026"], abs=0.1)
        assert ll["mediana_jul_ago_mm"] == pytest.approx(o["mediana_mm"], abs=0.1)
        assert ll["total_mas_seco_mm"] == pytest.approx(o["minimo_anterior_mm"], abs=0.1)
        assert ll["anio_mas_seco"] == o["anio_minimo_anterior"]
        assert ll["periodo_referencia"] == o["periodo_referencia"]


def test_biblioteca_repite_los_puntajes_de_las_opciones_elegidas(exportados, motor_res):
    for pid in PIDS:
        bib = {b["id"]: b for b in exportados[pid]["biblioteca"]}
        elegidas = motor_res[pid]["rotaciones"]
        assert {r["id"] for r in elegidas} == {b["id"] for b in bib.values() if b["elegida"]}
        for r in elegidas:
            b = bib[r["id"]]
            assert b["puntajes"] == {k: r["puntajes"][k] for k in ("agua", "suelo", "plagas")}, (pid, r["id"])
            assert b["deficit"] == r["deficit"], (pid, r["id"])


def test_curva_de_agua_cierra_con_el_balance_del_motor(exportados):
    cultivos = datos.cultivos()
    for pid in PIDS:
        p = datos.parcela(pid)
        serie, _ = explorar._serie(p, "chirps_diario")
        for b in exportados[pid]["biblioteca"]:
            cur = b["curva_agua"]
            assert cur is not None, (pid, b["id"])
            mes, dia = map(int, cur["siembra"].split("-"))
            for clave, x in cur["anios"].items():
                demanda, usada = clima.balance_ciclo(serie, date(x["anio"], mes, dia), cultivos[cur["cultivo"]])
                assert x["demanda_mm"] == pytest.approx(demanda, abs=0.06), (pid, b["id"], clave)
                assert x["usada_mm"] == pytest.approx(usada, abs=0.06), (pid, b["id"], clave)
                ultimo = x["puntos"][-1]
                assert ultimo[0] == cur["dias"] and ultimo[2] == x["demanda_mm"] and ultimo[3] == x["usada_mm"]
                assert all(a[k] <= c[k] for a, c in zip(x["puntos"], x["puntos"][1:]) for k in (1, 2, 3))
                assert x["deficit_pct"] == round(100 * (1 - usada / demanda))


def test_totales_de_la_biblioteca_son_los_del_motor(exportados, motor_res):
    from motor import puntaje
    for pid in PIDS:
        elegidas = {r["id"]: r for r in motor_res[pid]["rotaciones"]}
        for b in exportados[pid]["biblioteca"]:
            assert b["totales"] == {pr: puntaje.total(b["puntajes"], pr) for pr in puntaje.PESOS}, (pid, b["id"])
            if b["id"] in elegidas:
                assert b["totales"]["agua"] == elegidas[b["id"]]["puntajes"]["total"], (pid, b["id"])


def test_celda_smap_es_la_del_cache():
    probadas = 0
    for p in datos.parcelas():
        celda = ((datos.cache(f"smap/{p['id']}.json", obligatorio=False) or {}).get("datos") or {}).get("celda")
        if not celda:
            continue
        c = huellas.celda_smap(p["lat"], p["lon"])
        assert (c["fila"], c["col"]) == (celda["linea"], celda["muestra"]), p["id"]
        probadas += 1
    assert probadas >= 4
