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


# ---------------------------------------------------------------- años con pérdidas documentadas
def _val():
    import json
    import pytest
    from motor import datos
    ruta = datos.RAIZ / "web" / "public" / "data" / "validacion.json"
    if not ruta.exists():
        pytest.skip("sin validacion.json (python -m pipeline.validacion.validar)")
    return json.loads(ruta.read_text(encoding="utf-8"))


def test_perdidas_documentadas_lista_de_7_anios_con_fuente():
    import yaml
    from motor import datos
    anios = [x["anio"] for x in validar.PERDIDAS_DOCUMENTADAS]
    assert anios == [2009, 2010, 2015, 2016, 2018, 2019, 2023]
    fuentes = {f["id"]: f for f in yaml.safe_load((datos.DATA / "fuentes.yaml").read_text(encoding="utf-8"))["fuentes"]}
    for a in _val()["perdidas_documentadas"]["anios"]:
        assert a["que_documenta"] and a["ambito"] and a["fuentes"]
        for f in a["fuentes"]:
            assert f["url"] == fuentes[f["id"]]["url"] and f["url"].startswith("https://")
        assert a["en"]["que_documenta"] and a["en"]["ambito"]


def test_perdidas_documentadas_cifras_por_parcela():
    pd = _val()["perdidas_documentadas"]
    por = {x["id"]: x for x in pd["parcelas"]}
    assert len(por) == 5
    for pid, x in por.items():
        assert x["aciertos"] == (4 if pid == "san_juan_ermita" else 3), pid
        assert x["aciertos"] == len(x["anios_aciertos"]) and x["fallos"] == len(x["anios_fallos"])
        assert x["falsas_alarmas"] == len(x["anios_falsas_alarmas"]) and x["n_anios"] == 20
        assert x["aciertos"] + x["falsas_alarmas"] == len(x["anios_marcados"])
        assert x["aciertos"] + x["fallos"] == 7
    assert por["san_juan_ermita"]["anios_aciertos"] == [2009, 2010, 2015, 2018]
    assert pd["anios_sin_marcar_en_ninguna_parcela"] == [2016, 2019, 2023]
    for a in (2016, 2019, 2023):
        assert all(a not in x["anios_marcados"] for x in por.values())


def test_perdidas_documentadas_salen_de_las_marcas_del_motor():
    v = _val()
    por = {x["id"]: x for x in v["perdidas_documentadas"]["parcelas"]}
    for p in v["parcelas"]:
        marcados = [m["anio"] for m in p["sequia_2018"]["anios"] if m["riesgo_alto"]]
        assert por[p["id"]]["anios_marcados"] == marcados


def test_perdidas_documentadas_en_docs_validacion():
    from motor import datos
    md = (datos.RAIZ / "docs" / "validacion.md").read_text(encoding="utf-8")
    assert "### Aciertos y fallos contra los años con pérdidas documentadas" in md
    assert "El motor no marca 2016, 2019 ni 2023 en ninguna parcela." in md
    assert "| San Juan Ermita | 2009, 2010, 2014, 2015, 2018, 2025 | 4 (2009, 2010, 2015, 2018) |" in md


def test_limite_2026_y_notas_nuevas():
    v = _val()
    lim = v["observacion_2026"]["limites"][0]
    assert lim == ("Es una observación del pasado, no un pronóstico. La lluvia y la humedad de 2026 no entran en los "
                   "puntajes, la confianza ni el audio: el clima del motor es 2001-2025. Los focos de enero a mayo de "
                   "2026 sí cuentan en el hecho de quema.")
    pl = next(e for e in v["observacion_2026"]["reportes_publicos"] if e["id"] == "prensa_libre_2026_09_01")
    assert ("Según la nota, el estudio incorporó 4260 participantes, representativos de unos 91 121 hogares: los "
            "36 431 hogares son una estimación representativa, no un conteo.") in pl["nota"]
    assert validar.NOTA_SMAP_2018 in v["notas"]
    assert any("CHIRPS v3 ya mezcla estaciones de INSIVUMEH" in n and "comparación independiente" in n for n in v["notas"])
    assert len(v["en"]["notas"]) == len(v["notas"]) and all(v["en"]["notas"])


def test_limite_2026_en_ingles_igual_en_json_y_en_evidence():
    from motor import datos
    en = _val()["observacion_2026"]["en"]["limites"][0]
    js = (datos.RAIZ / "web" / "src" / "i18n" / "evidence.js").read_text(encoding="utf-8")
    assert en in js


def test_sensibilidad_canicula_verificar_pasa():
    import subprocess
    import sys
    from motor import datos
    r = subprocess.run([sys.executable, "-m", "pipeline.validacion.sensibilidad_canicula", "--verificar"],
                       cwd=datos.RAIZ, capture_output=True)
    assert r.returncode == 0, r.stdout.decode("utf-8", "replace") + r.stderr.decode("utf-8", "replace")
