"""Validador de números: ninguna cifra del texto puede faltar en el JSON del motor."""
from motor import contrato, redaccion


def test_numero_inventado_se_rechaza():
    permitidos = {28.6, 2018.0, 15.0, -20.0}
    assert redaccion.validar_numeros("Con esta rotación ahorra 987.65 mm de agua.", permitidos) == ["987.65"]


def test_numeros_respaldados_pasan():
    permitidos = {28.6, 2018.0, 15.0, -20.0, 0.35}
    texto = "Pendiente de 28.6 % (29 redondeado). En 2018, con lluvia -20 %, la racha pasó de 15 días; umbral 0.35."
    assert redaccion.validar_numeros(texto, permitidos) == []


def test_rangos_y_periodos():
    assert redaccion.numeros_en("periodo 2001-2025, rango 20–35 %") == ["2001", "2025", "20", "35"]
    # Los nombres de productos no son cifras sueltas
    assert redaccion.numeros_en("FAO-56, MERRA-2 y MOD13Q1") == []


def test_salida_del_motor_sin_cifras_ni_fechas_inventadas(resultado_sintetico):
    assert contrato.errores_textos(resultado_sintetico) == []


def test_un_numero_inventado_en_la_salida_se_detecta(resultado_sintetico):
    import copy
    roto = copy.deepcopy(resultado_sintetico)
    roto["rotaciones"][0]["beneficios"].append("Rinde 987.65 quintales más por manzana.")
    errores = contrato.errores_textos(roto)
    assert any("987.65" in e for e in errores)


def test_lista_de_meses():
    assert redaccion.lista_meses([3, 1, 2]) == "enero, febrero y marzo"
    assert redaccion.lista_meses([4]) == "abril"
    assert redaccion.lista_meses([]) == "ninguno"
