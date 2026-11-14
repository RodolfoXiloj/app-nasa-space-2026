"""ZARC se cita, nunca se calcula."""
import copy

from motor import contrato, redaccion, zarc

REGISTRO = {"municipio": "Jocotán", "cultivo": "maiz", "temporada": "primera",
            "texto_literal": "TEXTO LITERAL DE PRUEBA 1 de junio", "documento": "Documento de prueba",
            "institucion": "FAO y MAGA", "anio": 2025, "url": "https://ejemplo.invalid/zarc", "pagina": "1",
            "fecha_consulta": "2026-11-14"}


def test_sin_registro_remite_al_extensionista():
    r = zarc.buscar({"registros": [], "enlace_general": "https://www.maga.gob.gt/x"}, "Jocotán", [("maiz", "primera")])
    assert r["encontrado"] is False
    assert r["texto"] == zarc.SIN_REGISTRO
    assert r["enlace"].startswith("https://")
    assert "no cambia con el escenario" in r["nota_escenario"]


def test_con_registro_copia_el_texto_literal():
    r = zarc.buscar({"registros": [REGISTRO]}, "jocotan", [("maiz", "primera"), ("frijol", "postrera")])
    assert r["encontrado"] is True
    assert "«TEXTO LITERAL DE PRUEBA 1 de junio»" in r["texto"]
    assert r["registros"] == [REGISTRO]


def test_no_busca_otro_municipio_ni_otra_temporada():
    assert zarc.buscar({"registros": [REGISTRO]}, "Olopa", [("maiz", "primera")])["encontrado"] is False
    assert zarc.buscar({"registros": [REGISTRO]}, "Jocotán", [("maiz", "postrera")])["encontrado"] is False


def test_detecta_fechas_que_no_vienen_de_zarc():
    assert redaccion.fechas_no_citadas("Siembre el 15 de mayo.", []) == ["15 de mayo"]
    assert redaccion.fechas_no_citadas("Siembre en la semana 21.", []) == ["semana 21"]
    assert redaccion.fechas_no_citadas("Siembre a mediados de mayo.", []) == ["mediados de mayo"]
    assert redaccion.fechas_no_citadas("Siembre el 15/05.", []) == ["15/05"]
    # La misma fecha dentro de la cita literal de ZARC sí se permite
    cita = "TEXTO LITERAL DE PRUEBA 1 de junio"
    assert redaccion.fechas_no_citadas(f"Según ZARC: «{cita}».", [cita]) == []
    # Meses sin día no son fechas de siembra
    assert redaccion.fechas_no_citadas("El suelo queda desnudo en marzo y abril.", []) == []


def test_referencia_por_departamento_se_cita_sin_reemplazar_al_extensionista():
    y = {"registros": [], "referencias_departamento": [
        {"departamentos": ["Chiquimula"], "texto_literal": "mover las fechas de siembra de mayo a junio",
         "fuente": "Nota de prensa", "url": "https://ejemplo.invalid"}]}
    r = zarc.buscar(y, "Jocotán", [("maiz", "primera")], departamento="Chiquimula")
    assert r["encontrado"] is False
    assert r["texto"].startswith(zarc.SIN_REGISTRO)
    assert "«mover las fechas de siembra de mayo a junio»" in r["texto"]
    assert zarc.buscar(y, "Esquipulas", [("maiz", "primera")], departamento="Izabal")["texto"] == zarc.SIN_REGISTRO


def test_salida_sin_fechas_de_siembra_propias(resultado_sintetico):
    assert resultado_sintetico["zarc"]["encontrado"] is False
    assert resultado_sintetico["zarc"]["texto"] in resultado_sintetico["texto_tarjeta"]
    roto = copy.deepcopy(resultado_sintetico)
    roto["rotaciones"][0]["riesgos"].append("Conviene sembrar el 20 de mayo.")
    assert any("20 de mayo" in e for e in contrato.errores_textos(roto))


def test_escenario_no_cambia_zarc(base_sintetica):
    from motor.recomendar import recomendar
    a = recomendar("sint", base=base_sintetica)
    b = recomendar("sint", prioridad="suelo", base=base_sintetica)
    assert a["zarc"] == b["zarc"]
