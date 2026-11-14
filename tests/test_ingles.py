"""Inglés de los textos visibles: ninguno falta, las cifras son las mismas y el español no cambia.

Convención: cada objeto con texto visible lleva `es` y `en` con los mismos campos (motor/ingles.py).
"""
import copy
import json
import re
from collections import Counter

import pytest

from motor import datos, ingles, redaccion

WEB = datos.RAIZ / "web" / "public" / "data"


def pares(obj, ruta=""):
    """(ruta, texto en español, texto en inglés) de todos los bloques `es`/`en` del objeto."""
    out = []
    if isinstance(obj, dict):
        es_b, en_b = obj.get("es"), obj.get("en")
        if isinstance(es_b, dict) and isinstance(en_b, dict) and es_b.get("mp3"):
            for slot in ("es", "en", "caa"):
                if isinstance(obj.get(slot), dict):
                    out += pares(obj[slot], f"{ruta}/{slot}")
        elif isinstance(es_b, dict) and isinstance(en_b, dict):
            for c, es in obj["es"].items():
                en = obj["en"].get(c)
                if isinstance(es, list) and es and isinstance(es[0], dict):   # filas (evidencia): campo por campo
                    out += [(f"{ruta}/{c}[{i}]/{k}", a[k], b.get(k)) for i, (a, b) in enumerate(zip(es, en or []))
                            for k in a if isinstance(a[k], str)]
                    if len(es) != len(en or []):
                        out.append((f"{ruta}/{c}", f"{len(es)} filas", f"{len(en or [])} filas"))
                elif isinstance(es, list):
                    out += [(f"{ruta}/{c}[{i}]", a, b) for i, (a, b) in enumerate(zip(es, en or []))]
                    if len(es) != len(en or []):
                        out.append((f"{ruta}/{c}", f"{len(es)} textos", f"{len(en or [])} textos"))
                else:
                    out.append((f"{ruta}/{c}", es, en))
        for k, v in obj.items():
            if k not in ("es", "en"):
                out += pares(v, f"{ruta}/{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += pares(v, f"{ruta}[{i}]")
    return out


def _cifras(texto) -> Counter:
    return Counter(redaccion._a_float(n) for n in redaccion.numeros_en(texto)) if isinstance(texto, str) else Counter()


def _sin_citas(texto: str) -> str:
    return re.sub(r"«[^»]*»", "", texto)


def revisar(obj) -> list[str]:
    errores = []
    for ruta, es, en in pares(obj):
        if es in (None, ""):
            continue
        if not en:
            errores.append(f"{ruta}: falta el inglés")
        elif _cifras(es) != _cifras(en):
            errores.append(f"{ruta}: cifras distintas {sorted(_cifras(es).elements())} / {sorted(_cifras(en).elements())}")
        elif re.search(r"\b(alerts?|alerta|forecasts?)\b", _sin_citas(en), re.I):
            errores.append(f"{ruta}: palabra prohibida en el inglés")
    return errores


def _sin_idiomas(v):
    """Filas de evidencia sin sus subbloques es/en, para compararlas con rot.es.evidencia."""
    if isinstance(v, list):
        return [{k: x for k, x in e.items() if k not in ("es", "en")} if isinstance(e, dict) else e for e in v]
    return v


def espanol_intacto(obj, ruta="") -> list[str]:
    """El bloque `es` repite el campo de siempre: el español no cambió."""
    out = []
    if isinstance(obj, dict):
        for c, v in (obj.get("es") or {}).items() if isinstance(obj.get("es"), dict) else []:
            if c in obj and _sin_idiomas(obj[c]) != v:
                out.append(f"{ruta}/{c}")
        for k, v in obj.items():
            if k not in ("es", "en"):
                out += espanol_intacto(v, f"{ruta}/{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += espanol_intacto(v, f"{ruta}[{i}]")
    return out


# ---------------------------------------------------------------- motor (datos sintéticos)
def test_el_json_sintetico_tiene_todo_en_ingles(resultado_sintetico):
    assert ingles.faltantes(resultado_sintetico) == []
    assert revisar(resultado_sintetico) == []
    assert espanol_intacto(resultado_sintetico) == []


def test_bloques_bilingues_principales(resultado_sintetico):
    r = resultado_sintetico
    assert r["en"]["aviso"] == ingles.AVISO and r["es"]["aviso"] == r["aviso"]
    rot = r["rotaciones"][0]
    assert set(rot["en"]) >= {"nombre", "nombre_corto", "por_que", "beneficios", "vacios", "riesgos"}
    assert len(rot["en"]["vacios"]) == len(rot["vacios"]) and rot["es"]["por_que"] == rot["por_que"]
    assert all(e["en"]["dato"] for e in rot["evidencia"])
    assert all("en" in m and len(m["en"]["alertas"]) == len(m["alertas"]) for m in rot["calendario"])
    assert rot["confianza"]["en"]["motivo"] == rot["confianza"]["motivo_en"]
    assert all(g["en"]["termino"] and g["en"]["definicion"] for g in r["glosario"])
    assert all(f["en"]["nombre"] and f["en"]["cita"] for f in r["fuentes"])
    assert r["zarc"]["en"]["texto"].startswith("Planting date:")


def test_rotaciones_traen_evidencia_y_descripcion_en_ingles(resultado_sintetico):
    """rot.en.evidencia: las mismas filas (valor, periodo, fuente_id) con los textos en inglés."""
    for r in resultado_sintetico["rotaciones"]:
        assert r["en"]["descripcion"] and r["es"]["descripcion"] == r["descripcion"], r["id"]
        assert len(r["en"]["evidencia"]) == len(r["evidencia"]) == len(r["es"]["evidencia"])
        for e, en in zip(r["evidencia"], r["en"]["evidencia"]):
            assert (en["valor"], en["periodo"], en["fuente_id"]) == (e["valor"], e["periodo"], e["fuente_id"])
            assert en["dato"] == e["en"]["dato"] and "es" not in en and "en" not in en
    assert set(ingles.DESCRIPCIONES) == {r["id"] for r in datos.rotaciones()}


def test_tarjeta_en_ingles_con_las_mismas_cifras(resultado_sintetico):
    r = resultado_sintetico
    en = r["en"]["texto_tarjeta"]
    assert r["es"]["texto_tarjeta"] == r["texto_tarjeta"]
    assert en.startswith("Plot in ") and en.endswith("does not replace, your extension worker.")
    assert _cifras(_sin_citas(en)) == _cifras(_sin_citas(r["texto_tarjeta"]))
    for rot in r["rotaciones"]:
        assert f"Score {rot['puntajes']['total']}." in en


def test_las_rotaciones_traducen_cada_texto(resultado_sintetico):
    """Las plantillas en inglés dan la misma cantidad de textos que las de español, con las mismas cifras."""
    for r in resultado_sintetico["rotaciones"]:
        for campo in ("beneficios", "vacios", "riesgos"):
            assert len(r["en"][campo]) == len(r[campo]), (r["id"], campo)


def test_t_devuelve_none_si_no_hay_traduccion():
    assert ingles.t("Un texto que nadie tradujo.") is None
    assert ingles.t("de 25 años") == "of 25 years"
    assert ingles.t(None) is None


def test_yaml_en_completo():
    for r in datos.rotaciones():
        for campo in ("beneficios", "vacios", "riesgos"):
            assert len(r["en"][campo]) == len(r[campo]), (r["id"], campo)
        assert r["en"]["nombre"] and r["en"]["nombre_corto"] and r["nombre_corto"]
    assert all(g["en"]["termino"] and g["en"]["definicion"] for g in datos.glosario())
    assert all(f["en"]["nombre"] for f in datos.fuentes())
    assert all(p["en"]["nombre"] and p["en"]["nota"] for p in datos.parcelas())
    assert all(c["en"]["nombre"] for c in datos.cultivos().values())


def test_validacion_es_idempotente():
    ruta = WEB / "validacion.json"
    if not ruta.exists():
        pytest.skip("sin validacion.json")
    v = json.loads(ruta.read_text(encoding="utf-8"))
    una = ingles.validacion(copy.deepcopy(v))
    dos = ingles.validacion(copy.deepcopy(una))
    assert una == dos


# ---------------------------------------------------------------- archivos publicados
# futuros_nasa.json (motor/futuros.py) no lleva bloques es/en: sus textos visibles salen de web/src/i18n.
PUBLICADOS = sorted(p.name for p in WEB.glob("*.json") if p.name not in ("ejemplo.json", "futuros_nasa.json")) if WEB.exists() else []


@pytest.mark.parametrize("nombre", PUBLICADOS)
def test_json_publicado_en_ingles_con_las_mismas_cifras(nombre):
    obj = json.loads((WEB / nombre).read_text(encoding="utf-8"))
    assert ingles.faltantes(obj) == []
    assert revisar(obj) == []
    assert espanol_intacto(obj) == []
    assert pares(obj), "el archivo no tiene bloques es/en"
