"""El contrato JSON: esquema, los 5 campos del reto y los archivos exportados a la web."""
import copy
import json
from pathlib import Path

import pytest

from motor import contrato
from motor.recomendar import CAMPOS_RETO, ContratoIncompleto, verificar_campos_reto

RAIZ = Path(__file__).resolve().parent.parent
WEB_DATA = RAIZ / "web" / "public" / "data"


def test_ejemplo_cumple_el_esquema():
    ejemplo = json.loads(contrato.EJEMPLO.read_text(encoding="utf-8"))
    assert ejemplo["meta"]["tipo"] == "ejemplo"
    assert contrato.errores_esquema(ejemplo) == []


def test_salida_del_motor_cumple_el_esquema(resultado_sintetico):
    assert contrato.errores_esquema(resultado_sintetico) == []
    assert resultado_sintetico["meta"]["tipo"] == "calculado"


def test_tres_rotaciones_con_los_cinco_campos(resultado_sintetico):
    rots = resultado_sintetico["rotaciones"]
    assert [r["tipo"] for r in rots] == ["actual", "leguminosa_cobertura", "tolerante_sequia"]
    for r in rots:
        for campo in CAMPOS_RETO:
            assert r[campo], f"{r['id']} sin {campo}"
        assert len(r["calendario"]) == 12
        assert r["confianza"]["motivo"]


def test_falta_un_campo_y_la_exportacion_falla(resultado_sintetico):
    for campo in CAMPOS_RETO:
        roto = copy.deepcopy(resultado_sintetico)
        roto["rotaciones"][1][campo] = [] if isinstance(roto["rotaciones"][1][campo], list) else ""
        with pytest.raises(ContratoIncompleto):
            verificar_campos_reto(roto)


def test_esquema_rechaza_rotacion_sin_vacios(resultado_sintetico):
    roto = copy.deepcopy(resultado_sintetico)
    del roto["rotaciones"][2]["vacios"]
    assert contrato.errores_esquema(roto)


def test_ocho_escenarios_con_las_tres_rotaciones(resultado_sintetico):
    esc = resultado_sintetico["escenarios"]
    assert len(esc["lista"]) == 8
    ids = {r["id"] for r in resultado_sintetico["rotaciones"]}
    for e in esc["lista"]:
        assert set(e["rotaciones"]) == ids


def test_menos_lluvia_no_mejora_el_agua(resultado_sintetico):
    lista = {e["id"]: e for e in resultado_sintetico["escenarios"]["lista"]}
    for rid in lista["lluvia_0_temp_0"]["rotaciones"]:
        base = lista["lluvia_0_temp_0"]["rotaciones"][rid]["puntajes"]["agua"]
        seco = lista["lluvia_-30_temp_1.5"]["rotaciones"][rid]["puntajes"]["agua"]
        assert seco <= base


def test_aviso_de_que_no_reemplaza_al_tecnico(resultado_sintetico):
    assert "no reemplaza" in resultado_sintetico["aviso"]
    assert "no reemplaza" in resultado_sintetico["texto_tarjeta"]


@pytest.mark.parametrize("ruta", sorted(p for p in WEB_DATA.glob("*.json") if p.name not in ("parcelas.json", "validacion.json")),
                         ids=lambda p: p.name)
def test_cada_json_exportado_cumple_el_esquema(ruta):
    obj = json.loads(ruta.read_text(encoding="utf-8"))
    assert contrato.errores_esquema(obj) == []
    if obj["meta"]["tipo"] == "calculado":
        assert contrato.errores_textos(obj) == []


def test_validacion_json_tiene_la_regla_y_las_parcelas():
    ruta = WEB_DATA / "validacion.json"
    if not ruta.exists():
        pytest.skip("aún no se corrió python -m pipeline.validacion.validar")
    v = json.loads(ruta.read_text(encoding="utf-8"))
    assert {"regla_5_1", "parcelas", "titular_2018", "notas"} <= set(v)
    assert v["regla_5_1"]["minimo"] == 3
    for p in v["parcelas"]:
        assert {"power_vs_chirps", "sequia_2018"} <= set(p)
