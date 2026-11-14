"""Funciones puras de la validación (pipeline/validacion/validar.py)."""
import math

from pipeline.validacion import validar


def test_spearman_perfecto_e_inverso():
    assert validar.spearman([1, 2, 3, 4, 5], [10, 20, 30, 40, 50]) == 1.0
    assert validar.spearman([1, 2, 3, 4, 5], [50, 40, 30, 20, 10]) == -1.0
    assert validar.spearman([1, 2, 3], [1, 2, 3]) is None          # menos de 4 pares


def test_spearman_con_empates_usa_rango_promedio():
    assert validar._rangos([10, 20, 20, 30]) == [1.0, 2.5, 2.5, 4.0]
    r = validar.spearman([1, 2, 2, 3, 4], [2, 1, 3, 4, 5])
    assert r is not None and 0 < r < 1


def test_anomalia_ndvi_solo_usa_anios_anteriores():
    filas = []
    for anio in range(2001, 2011):
        valor = 0.5 if anio == 2010 else 0.8 + 0.01 * (anio % 3)
        for mes in ("07", "08", "09"):
            filas.append([f"{anio}-{mes}-01", valor, 0])
            filas.append([f"{anio}-{mes}-17", valor, 0])
    anom = validar.anomalias_ndvi({"datos": {"filas": filas}}, [2007, 2010])
    assert anom[2010] < -3                    # 2010 muy por debajo de 2001-2009
    assert anom[2007] is not None and abs(anom[2007]) < 3   # 2007 tiene 6 años previos
    # 2003 y 2005 no tienen 5 años previos: sin anomalía
    assert validar.anomalias_ndvi({"datos": {"filas": filas}}, [2003, 2005]) == {2003: None, 2005: None}


def test_evidencia_publica_2018_trae_fuente_y_cifras():
    e = validar.EVIDENCIA_2018
    assert e["url"].startswith("https://www.fao.org/")
    assert e["guatemala_ha_perdidas"] == 175126 and "Chiquimula" in e["departamentos_mas_afectados"]
    assert not math.isnan(e["guatemala_personas_afectadas"])


# ---------------------------------------------------------------- observación de julio-agosto 2026
def _obs():
    import pytest
    o = validar.observacion_2026()
    if o is None:
        pytest.skip("falta data/cache/chirps_reciente/ (python -m pipeline.clientes.chirps --reciente 2026)")
    return o


def test_observacion_2026_sale_de_la_cache_y_no_se_llama_alerta():
    import json
    import statistics
    from motor import datos
    o = _obs()
    texto_propio = " ".join([o["titulo"], o["resumen"], *o["limites"]]).lower()
    assert "alerta" not in texto_propio and "preliminar" in o["titulo"].lower()
    assert "no un pronóstico" in texto_propio and "percentil" in texto_propio  # dice que no da percentil
    for x in o["lluvia_chirps"]:
        rec = json.loads((datos.CACHE / "chirps_reciente" / f"{x['id']}.json").read_text(encoding="utf-8"))["datos"]
        hist = json.loads((datos.CACHE / "chirps" / f"{x['id']}.json").read_text(encoding="utf-8"))["datos"]["filas"]
        total = round(rec["meses"]["7"] + rec["meses"]["8"], 1)
        ref: dict[int, float] = {}
        for a, m, v in hist:
            if m in (7, 8) and v is not None:
                ref[a] = ref.get(a, 0) + v
        assert x["mm_2026"] == total
        assert x["mediana_mm"] == round(statistics.median(ref.values()), 1)
        assert x["pct_de_la_mediana"] == round(100 * total / statistics.median(ref.values()))
        assert "prelim/" in rec["carpeta"] and all(f["last_modified"] for f in rec["archivos"])


def test_observacion_2026_cuenta_celdas_smap_no_parcelas():
    o = _obs()
    celdas = {(c["celda"]["linea"], c["celda"]["muestra"]) for c in o["smap_celdas"]}
    assert len(celdas) == len(o["smap_celdas"])                 # una fila por celda
    assert sum(len(c["parcelas"]) for c in o["smap_celdas"]) >= len(o["smap_celdas"])
    assert f"en {sum(c['es_el_mas_bajo'] for c in o['smap_celdas'])} de {len(o['smap_celdas'])} celdas" in o["resumen"]


def test_reportes_2026_con_ambito_y_sin_presentar_fews_como_independiente():
    rep = {e["id"]: e for e in validar.EVIDENCIA_2026}
    fews = rep["fews_net_2026_08"]
    assert fews["relacion"] == "coincide" and "no es una confirmación independiente" in fews["nota"]
    pl = rep["prensa_libre_2026_09_01"]
    assert "corredor seco guatemalteco" in pl["cita"] and "No se atribuye a Chiquimula" in pl["nota"]
    assert all(e["url"].startswith("https://") for e in rep.values())
