"""Bloque `farmer` del contrato: forma, compatibilidad con v1 y que no traiga cifras nuevas."""
import copy
import json

import pytest

from motor import contrato, farmer, redaccion


def test_el_motor_agrega_el_bloque_y_cumple_el_esquema(resultado_sintetico):
    assert "farmer" in resultado_sintetico
    assert contrato.errores_esquema(resultado_sintetico) == []


def test_un_json_v1_sin_farmer_sigue_siendo_valido(resultado_sintetico):
    sin = copy.deepcopy(resultado_sintetico)
    del sin["farmer"]
    assert contrato.errores_esquema(sin) == []
    ejemplo = json.loads(contrato.EJEMPLO.read_text(encoding="utf-8"))
    assert "farmer" not in ejemplo
    assert contrato.errores_esquema(ejemplo) == []
    assert resultado_sintetico["version_contrato"] == "1.0"


def test_tres_hechos_en_orden_fijo(resultado_sintetico):
    hechos = resultado_sintetico["farmer"]["hechos"]
    assert [h["id"] for h in hechos] == list(farmer.ORDEN) == ["suelo", "quema", "canicula"]


def test_los_hechos_copian_las_cifras_del_motor(resultado_sintetico):
    res = resultado_sintetico
    suelo, quema, canicula = res["farmer"]["hechos"]
    det, can = res["deteccion"], res["clima"]["canicula"]
    assert (suelo["valor"], suelo["de"], suelo["meses"]) == (len(det["meses_desnudos"]), 12, det["meses_desnudos"])
    assert suelo["meses_poca_cobertura"] == det["meses_poca_cobertura"]
    assert (quema["valor"], quema["de"]) == (det["quemas"]["anios_con_quema"], det["quemas"]["anios_observados"])
    assert quema["meses"] == det["quemas"]["meses_con_quema"]
    assert (canicula["valor"], canicula["de"]) == (can["anios_racha_larga"], can["anios_total"])
    assert canicula["periodo"] == res["clima"]["periodo"]


def test_fuente_de_la_canicula():
    con_diario = {"fuente_lluvia": "CHIRPS v3 mensual repartido por días con NASA POWER; junio-agosto con "
                                   "CHIRPS v3 diario (reparto con NASA IMERG)", "fuente_ids": ["chirps", "nasa_power", "fao56"]}
    assert farmer._fuentes_canicula(con_diario) == ["chirps_diario", "imerg"]
    solo_power = {"fuente_lluvia": "NASA POWER", "fuente_ids": ["nasa_power", "fao56"]}
    assert farmer._fuentes_canicula(solo_power) == ["nasa_power"]


def test_el_bloque_no_trae_cifras_nuevas(resultado_sintetico):
    con_farmer = redaccion.numeros_permitidos(resultado_sintetico)
    sin_farmer = redaccion.numeros_permitidos({k: v for k, v in resultado_sintetico.items() if k != "farmer"})
    assert con_farmer == sin_farmer


@pytest.mark.parametrize("umbrales", [None, {"estado": "pendiente"}])
def test_sin_umbrales_confirmados_no_hay_estados(resultado_sintetico, umbrales):
    f = farmer.bloque(resultado_sintetico, umbrales)
    assert f["umbrales"] == {"estado": "pendiente", "documento": "docs/umbrales.md"}
    assert all(h["estado"] is None and h["motivo_gris"] is None for h in f["hechos"])
    assert f["opciones"]["estado"] == "pendiente"
    assert f["opciones"]["destaca"] is None and f["opciones"]["empatadas"] == []
    con = copy.deepcopy(resultado_sintetico)
    con["farmer"] = f
    assert contrato.errores_esquema(con) == []


def test_opciones_y_confianza_salen_de_las_rotaciones(resultado_sintetico):
    rots = resultado_sintetico["rotaciones"]
    op = resultado_sintetico["farmer"]["opciones"]
    assert op["actual"] == rots[0]["id"] and rots[0]["es_actual"]
    assert op["alternativas"] == [r["id"] for r in rots[1:]]
    c = rots[0]["confianza"]
    assert op["confianza"] == {"nivel": c["nivel"], "motivo": c["motivo"], "motivo_en": c["motivo_en"]}


def test_ranura_por_idioma_con_chorti(resultado_sintetico):
    assert resultado_sintetico["farmer"]["audio"] == {"es": None, "en": None, "caa": None}


@pytest.mark.parametrize("estado", ["anaranjado", "naranja", "alerta", "verde_claro"])
def test_esquema_rechaza_estados_que_no_existen(resultado_sintetico, estado):
    roto = copy.deepcopy(resultado_sintetico)
    roto["farmer"]["hechos"][0]["estado"] = estado
    assert contrato.errores_esquema(roto)


@pytest.mark.parametrize("estado", ["verde", "amarillo", "rojo", "gris"])
def test_esquema_acepta_los_cuatro_estados(resultado_sintetico, estado):
    ok = copy.deepcopy(resultado_sintetico)
    for h in ok["farmer"]["hechos"]:
        h["estado"] = estado
        # gris siempre lleva su motivo en los dos idiomas; los demás no
        h["motivo_gris"], h["motivo_gris_en"] = (("Faltan datos de la fuente", "The source has no data")
                                                 if estado == "gris" else (None, None))
    assert contrato.errores_esquema(ok) == []


def test_esquema_rechaza_hechos_faltantes_o_desordenados(resultado_sintetico):
    falta = copy.deepcopy(resultado_sintetico)
    falta["farmer"]["hechos"].pop()
    assert contrato.errores_esquema(falta)
    desorden = copy.deepcopy(resultado_sintetico)
    desorden["farmer"]["hechos"].reverse()
    assert contrato.errores_esquema(desorden)
    sobra = copy.deepcopy(resultado_sintetico)
    sobra["farmer"]["hechos"].append(copy.deepcopy(sobra["farmer"]["hechos"][0]))
    assert contrato.errores_esquema(sobra)


def test_las_frases_pasan_el_validador_de_numeros(resultado_sintetico):
    res = copy.deepcopy(resultado_sintetico)
    n = res["farmer"]["hechos"][0]["valor"]
    res["farmer"]["frases"] = [{"id": "suelo", "hecho": "suelo",
                                "es": f"El satélite vio {n} meses de suelo pelado.",
                                "en": f"The satellite saw {n} months of bare soil."}]
    assert contrato.errores_esquema(res) == []
    assert contrato.errores_textos(res) == []
    res["farmer"]["frases"][0]["en"] = "The satellite saw 4321 months of bare soil."
    errores = contrato.errores_textos(res)
    assert len(errores) == 1 and errores[0].startswith("farmer.frases[0].en")
