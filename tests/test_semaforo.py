"""Semáforo de 3 hechos, gris por hecho y regla de empate (umbrales confirmados el 14 nov 2026).

Los cortes salen de data/umbrales_semaforo.yaml, que copia docs/umbrales.md. Las pruebas con la caché
real fijan la tabla «Lo que daría con los datos de hoy» y los totales de la regresión de cifras.
"""
import copy

import pytest

from motor import confianza, contrato, datos, farmer

U = datos.umbrales_semaforo()
SUELO, QUEMA, CANICULA = (U["hechos"][k] for k in farmer.ORDEN)


def test_umbrales_confirmados_tal_cual_docs():
    assert U["estado"] == "confirmado"
    assert U["documento"] == "docs/umbrales.md"
    assert (SUELO["amarillo_desde"], SUELO["rojo_desde"], SUELO["gris_pct_validos_menor_que"]) == (1, 2, 60)
    assert (QUEMA["amarillo_desde"], QUEMA["rojo_desde"]) == (1, 3)
    assert (CANICULA["amarillo_desde"], CANICULA["rojo_desde"]) == (1, 3)
    assert U["opciones"]["margen_empate"] == 3
    # el gris de suelo usa el mismo corte que la confianza baja
    assert SUELO["gris_pct_validos_menor_que"] == confianza.UMBRALES["validos_baja"]
    assert {k: (v["es"], v["en"]) for k, v in U["estados"].items()} == {
        "verde": ("Bien", "Good"), "amarillo": ("Atención", "Watch"), "rojo": ("Se repite", "Repeats"),
        "gris": ("El satélite no ve bien aquí", "The satellite can't see well here")}


def test_el_bloque_lleva_los_umbrales_confirmados(resultado_sintetico):
    u = resultado_sintetico["farmer"]["umbrales"]
    assert u["estado"] == "confirmado" and u["margen_empate"] == 3
    assert u["cortes"] == U["hechos"] and u["estados"] == U["estados"]
    assert set(u["estados"]) == set(farmer.ESTADOS)


# ---------------------------------------------------------------- cada estado
@pytest.mark.parametrize("desnudos, poca, esperado", [
    (0, 0, "verde"),
    (0, 2, "amarillo"),   # Camotán y Olopa: solo poca cobertura
    (1, 0, "amarillo"),
    (1, 4, "amarillo"),   # Zacapa
    (2, 2, "rojo"),       # Jocotán
    (3, 2, "rojo"),       # San Juan Ermita
    (12, 0, "rojo"),
])
def test_estado_suelo(desnudos, poca, esperado):
    assert farmer.estado_suelo(desnudos, poca, SUELO) == esperado


@pytest.mark.parametrize("corte", [QUEMA, CANICULA], ids=["quema", "canicula"])
@pytest.mark.parametrize("anios, esperado", [(0, "verde"), (1, "amarillo"), (2, "amarillo"), (3, "rojo"), (15, "rojo")])
def test_estado_quema_y_canicula(corte, anios, esperado):
    assert farmer.estado_conteo(anios, corte) == esperado


def test_estados_del_resultado_sintetico(resultado_sintetico):
    suelo, quema, canicula = resultado_sintetico["farmer"]["hechos"]
    assert (suelo["valor"], suelo["estado"]) == (4, "rojo")        # enero-abril bajo 0.35
    assert (quema["valor"], quema["estado"]) == (2, "amarillo")    # 2020 y 2022
    # la base sintética no tiene CHIRPS diario: la canícula sale gris con su motivo
    assert canicula["estado"] == "gris"
    assert canicula["motivo_gris"] == farmer.MOTIVOS_GRIS["canicula"]["es"]
    assert canicula["motivo_gris_en"] == farmer.MOTIVOS_GRIS["canicula"]["en"]
    assert suelo["motivo_gris"] is None and quema["motivo_gris"] is None


# ---------------------------------------------------------------- gris por hecho
def _con_chirps_diario(res: dict) -> dict:
    out = copy.deepcopy(res)
    out["clima"]["fuente_lluvia"] += "; junio-agosto con CHIRPS v3 diario (reparto con NASA IMERG)"
    return out


def _estados(res: dict) -> dict:
    return {h["id"]: h["estado"] for h in farmer.bloque(res, U)["hechos"]}


def test_con_chirps_diario_la_canicula_tiene_color(resultado_sintetico):
    res = _con_chirps_diario(resultado_sintetico)
    hechos = farmer.bloque(res, U)["hechos"]
    assert hechos[2]["fuente_ids"] == ["chirps_diario", "imerg"]
    assert hechos[2]["estado"] in ("verde", "amarillo", "rojo")
    assert all(h["motivo_gris"] is None and h["motivo_gris_en"] is None for h in hechos)


def test_suelo_gris_con_pocos_compuestos_validos(resultado_sintetico):
    res = _con_chirps_diario(resultado_sintetico)
    res["deteccion"]["calidad"]["pct_validos"] = 59.9
    e = _estados(res)
    assert e["suelo"] == "gris"
    assert e["quema"] != "gris" and e["canicula"] != "gris"   # gris por hecho, no por parcela
    res["deteccion"]["calidad"]["pct_validos"] = 60.0
    assert _estados(res)["suelo"] == "rojo"


def test_suelo_gris_si_un_mes_no_tiene_mediana(resultado_sintetico):
    res = _con_chirps_diario(resultado_sintetico)
    res["deteccion"]["ndvi_mensual"][5]["mediana"] = None
    suelo = farmer.bloque(res, U)["hechos"][0]
    assert suelo["estado"] == "gris" and suelo["motivo_gris"] == farmer.MOTIVOS_GRIS["suelo_sin_mediana"]["es"]


def test_quema_gris_sin_datos_de_firms(resultado_sintetico):
    res = _con_chirps_diario(resultado_sintetico)
    res["deteccion"]["quemas"].update(anios_con_quema=0, anios_observados=0, periodo="sin datos", meses_con_quema=[])
    e = _estados(res)
    assert e["quema"] == "gris"                  # 0 años observados no es verde
    assert e["suelo"] != "gris" and e["canicula"] != "gris"


def test_los_motivos_grises_van_en_dos_idiomas_y_sin_cifras():
    from motor import redaccion
    for m in farmer.MOTIVOS_GRIS.values():
        assert set(m) == {"es", "en"} and all(len(t) > 10 for t in m.values())
        assert not redaccion.numeros_en(m["es"]) and not redaccion.numeros_en(m["en"])


# ---------------------------------------------------------------- regla de empate
@pytest.mark.parametrize("totales, esperado", [
    ({"actual": 80, "leg": 88, "tol": 87}, ["leg", "tol"]),            # Jocotán: alternativas empatadas
    ({"actual": 80, "leg": 88, "tol": 85}, ["leg", "tol"]),            # 3 puntos justos: empate
    ({"actual": 80, "leg": 88, "tol": 84}, ["leg"]),                   # 4 puntos: la leguminosa destaca
    ({"actual": 87, "leg": 90, "tol": 92}, ["actual", "leg", "tol"]),  # Olopa: en cadena, las tres
    ({"actual": 90, "leg": 86, "tol": 80}, ["actual"]),                # la práctica actual destaca
    ({"actual": 88, "leg": 86, "tol": 80}, ["actual", "leg"]),         # empate contra la práctica actual
    ({"actual": 85, "leg": 85, "tol": 85}, ["actual", "leg", "tol"]),
])
def test_regla_de_empate(totales, esperado):
    assert farmer.empatadas(totales, U["opciones"]["margen_empate"]) == esperado


def test_empatadas_va_en_orden_fijo_no_por_puntaje():
    assert farmer.empatadas({"actual": 87, "leg": 90, "tol": 92}, 3) == ["actual", "leg", "tol"]
    assert farmer.empatadas({"actual": 87, "tol": 92, "leg": 90}, 3) == ["actual", "tol", "leg"]


def _con_totales(res: dict, totales: list[float], nivel: str = "alta") -> dict:
    out = copy.deepcopy(res)
    for r, t in zip(out["rotaciones"], totales):
        r["puntajes"]["total"] = t
        r["confianza"]["nivel"] = nivel
    return out


def test_opciones_empate_sin_ganadora(resultado_sintetico):
    op = farmer.bloque(_con_totales(resultado_sintetico, [80, 88, 87]), U)["opciones"]
    alts = resultado_sintetico["farmer"]["opciones"]["alternativas"]
    assert op["estado"] == op["regla_puntaje"] == "empate"
    assert op["destaca"] is None and op["empatadas"] == alts
    assert op["motivo_gris"] is None


def test_opciones_una_destaca(resultado_sintetico):
    op = farmer.bloque(_con_totales(resultado_sintetico, [80, 88, 84]), U)["opciones"]
    assert op["estado"] == "una_destaca" and op["destaca"] == op["alternativas"][0] and op["empatadas"] == []


def test_opciones_olopa_muestra_las_tres_sin_orden(resultado_sintetico):
    res = _con_totales(resultado_sintetico, [87, 90, 92], nivel="media")
    op = farmer.bloque(res, U)["opciones"]
    assert op["estado"] == "empate" and op["destaca"] is None
    assert op["empatadas"] == [op["actual"]] + op["alternativas"]


def test_confianza_baja_pone_las_opciones_en_gris_con_motivo(resultado_sintetico):
    res = _con_totales(resultado_sintetico, [80, 88, 84], nivel="baja")
    op = farmer.bloque(res, U)["opciones"]
    c = res["rotaciones"][0]["confianza"]
    assert op["estado"] == "gris"
    assert op["destaca"] is None                  # aunque la regla daría una ganadora
    assert op["regla_puntaje"] == "una_destaca"
    assert (op["motivo_gris"], op["motivo_gris_en"]) == (c["motivo"], c["motivo_en"])
    # la confianza baja no pone grises los 3 hechos: viene de SMAP o de POWER, que ellos no usan
    hechos = farmer.bloque(_con_chirps_diario(res), U)["hechos"]
    assert all(h["estado"] != "gris" for h in hechos)


# ---------------------------------------------------------------- contrato
def test_esquema_pide_motivo_si_un_hecho_es_gris(resultado_sintetico):
    roto = copy.deepcopy(resultado_sintetico)
    roto["farmer"]["hechos"][2].update(motivo_gris=None, motivo_gris_en=None)
    assert contrato.errores_esquema(roto)


def test_esquema_no_acepta_ganadora_en_empate_ni_en_gris(resultado_sintetico):
    for estado in ("empate", "gris"):
        roto = copy.deepcopy(resultado_sintetico)
        roto["farmer"]["opciones"].update(estado=estado, destaca=roto["farmer"]["opciones"]["alternativas"][0],
                                          empatadas=roto["farmer"]["opciones"]["alternativas"],
                                          motivo_gris="Confianza baja.", motivo_gris_en="Low confidence.")
        assert contrato.errores_esquema(roto), estado
    sin_motivo = copy.deepcopy(resultado_sintetico)
    sin_motivo["farmer"]["opciones"].update(estado="gris", destaca=None, motivo_gris=None, motivo_gris_en=None)
    assert contrato.errores_esquema(sin_motivo)


def test_esquema_no_acepta_un_estado_anaranjado_en_la_leyenda(resultado_sintetico):
    roto = copy.deepcopy(resultado_sintetico)
    roto["farmer"]["umbrales"]["estados"]["anaranjado"] = {"forma": "circulo", "es": "Alerta", "en": "Alert"}
    assert contrato.errores_esquema(roto)


def test_el_bloque_no_usa_la_palabra_alerta(resultado_sintetico):
    import json
    texto = json.dumps(resultado_sintetico["farmer"], ensure_ascii=False).lower()
    assert "alerta" not in texto and "alert" not in texto and "anaranjado" not in texto


# ---------------------------------------------------------------- las 5 parcelas con la caché real
HOY = {  # docs/umbrales.md, «Lo que daría con los datos de hoy» y tabla de la regla de empate
    "jocotan": ((80, 88, 87), ("rojo", "rojo", "amarillo"), "empate", "alternativas"),
    "camotan": ((84, 90, 89), ("amarillo", "rojo", "amarillo"), "gris", "alternativas"),
    "olopa": ((87, 90, 92), ("amarillo", "amarillo", "verde"), "empate", "las_tres"),
    "san_juan_ermita": ((80, 88, 86), ("rojo", "amarillo", "amarillo"), "empate", "alternativas"),
    "zacapa": ((73, 81, 80), ("amarillo", "verde", "rojo"), "gris", "alternativas"),
}


@pytest.fixture(scope="module")
def reales():
    from motor.recomendar import recomendar
    out = {}
    for pid in HOY:
        if not all(datos.disponibilidad(pid)[k] for k in ("ndvi", "power_diario", "firms", "chirps_diario")):
            pytest.skip(f"falta la caché de {pid}")
        out[pid] = recomendar(pid)
    return out


@pytest.mark.parametrize("pid", list(HOY))
def test_parcela_real(reales, pid):
    totales, estados, opciones, grupo = HOY[pid]
    res = reales[pid]
    f = res["farmer"]
    # regresión de cifras: el semáforo no mueve ningún puntaje
    assert tuple(r["puntajes"]["total"] for r in res["rotaciones"]) == totales
    assert tuple(h["estado"] for h in f["hechos"]) == estados
    assert all(h["motivo_gris"] is None for h in f["hechos"])   # con los datos de hoy ningún hecho sale gris
    op = f["opciones"]
    assert op["estado"] == opciones and op["regla_puntaje"] == "empate" and op["destaca"] is None
    assert op["empatadas"] == ([op["actual"]] + op["alternativas"] if grupo == "las_tres" else op["alternativas"])
    if opciones == "gris":
        assert op["motivo_gris"] == res["rotaciones"][0]["confianza"]["motivo"]
        assert op["motivo_gris_en"] and op["motivo_gris_en"] != op["motivo_gris"]
    assert contrato.errores_esquema(res) == [] and contrato.errores_textos(res) == []


def test_olopa_real_las_tres_opciones_sin_orden(reales):
    op = reales["olopa"]["farmer"]["opciones"]
    assert op["empatadas"] == ["actual_maiz_frijol", "leguminosa_canavalia", "tolerante_maiz_corto"]
    assert op["destaca"] is None and op["estado"] == "empate"
    assert reales["olopa"]["farmer"]["opciones"]["confianza"]["nivel"] == "media"
