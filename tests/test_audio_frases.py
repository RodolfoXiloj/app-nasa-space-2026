"""Audio corto por frases (paso 4): frases en dos idiomas, tiempos, subtítulos y la regla «nada solo en audio».

Las pruebas de los archivos publicados leen web/public/data y web/public/audio; las demás no usan red.
"""
import copy
import json
import re

import pytest

from motor import audio_frases, audio_id3, contrato, datos, exportar, farmer, frases
from motor.recomendar import recomendar

U = datos.umbrales_semaforo()
WEB = datos.RAIZ / "web" / "public"
AUDIO_FALSO = b"\xff\xf3\x44\xc4" + bytes(range(256)) * 8  # basta para probar las etiquetas: no se decodifica


# ---------------------------------------------------------------- frases
def test_seis_frases_en_orden_y_en_dos_idiomas(resultado_sintetico):
    fr = resultado_sintetico["farmer"]["frases"]
    assert [f["id"] for f in fr] == ["parcela", "suelo", "quema", "canicula", "opciones", "cierre"]
    assert [f["hecho"] for f in fr] == [None, "suelo", "quema", "canicula", None, None]
    for f in fr:
        assert f["es"].strip() and f["en"].strip() and f["es"] != f["en"]
        assert f["caa"] is None and f["inicio_s"] is None and f["fin_s"] is None   # sin mp3, sin tiempos
    assert "voz de computadora" in fr[0]["es"] and "computer voice" in fr[0]["en"]


def test_las_frases_pasan_el_validador_y_no_dicen_alerta(resultado_sintetico):
    assert contrato.errores_textos(resultado_sintetico) == []
    texto = json.dumps(resultado_sintetico["farmer"]["frases"], ensure_ascii=False).lower()
    assert "alerta" not in texto and "alert" not in texto and "pronóstico" not in texto and "forecast" not in texto


def test_el_audio_solo_lee_las_frases(resultado_sintetico):
    fr = resultado_sintetico["farmer"]["frases"]
    assert frases.texto_audio(fr) == " ".join(f["es"] for f in fr)
    assert frases.texto_audio(fr, "en") == " ".join(f["en"] for f in fr)


def test_sin_umbrales_no_hay_frases(resultado_sintetico):
    assert farmer.bloque(resultado_sintetico, None)["frases"] == []


# Las frases dicen qué pasó, cuándo y cada cuánto (15 nov 2026: «Suelo: se repite» no le dice nada a nadie). La
# palabra del semáforo queda solo en el gris, donde es el mensaje.
@pytest.mark.parametrize("estado, meses, poca, dice", [
    ("verde", [], [], "su tierra estuvo cubierta de plantas todo el año. lo vio el satélite de 2021 a 2025."),
    ("amarillo", [], [3, 4], "en marzo y abril, su tierra suele quedar con pocas plantas que la cubran."),
    ("amarillo", [4], [1, 2, 3, 5], "en abril, su tierra suele quedar sin plantas que la cubran; en enero, febrero, marzo y mayo, con pocas."),
    ("rojo", [2, 3, 4], [1, 5], "en febrero, marzo y abril, su tierra suele quedar sin plantas que la cubran."),
    ("gris", [], [], "suelo: el satélite no ve bien aquí."),
])
def test_frase_del_suelo_por_estado(resultado_sintetico, estado, meses, poca, dice):
    h = dict(resultado_sintetico["farmer"]["hechos"][0], estado=estado, valor=len(meses), meses=meses,
             meses_poca_cobertura=poca, periodo="2021-2025")
    es, en = frases._suelo(h, U)
    assert dice in es.lower()
    assert "se repite" not in es.lower() and "repeats" not in en.lower()
    if estado == "gris":
        assert en.startswith("Soil: ") and U["estados"]["gris"]["en"].lower() in en.lower()
    else:
        assert "the satellite saw it from 2021 to 2025." in en.lower()


@pytest.mark.parametrize("estado, valor, meses, dice", [
    ("verde", 0, [], "en los últimos 15 años, el satélite no vio quemas a menos de medio kilómetro de su parcela."),
    ("amarillo", 2, [3], "en 2 de los últimos 15 años hubo quemas a menos de medio kilómetro de su parcela, en marzo."),
    ("rojo", 3, [4, 5], "en 3 de los últimos 15 años hubo quemas a menos de medio kilómetro de su parcela, en abril y mayo."),
    ("gris", 0, [], "quema: el satélite no ve bien aquí.")])
def test_frase_de_la_quema_por_estado(estado, valor, meses, dice):
    es, en = frases._quema({"estado": estado, "valor": valor, "de": 15, "meses": meses}, U)
    assert dice in es.lower()
    assert ("burning: " in en.lower()) == (estado == "gris")


@pytest.mark.parametrize("estado, valor, dice", [
    ("verde", 0, "en los últimos 25 años, la canícula nunca dejó más de 15 días seguidos casi sin lluvia."),
    ("amarillo", 1, "en 1 de los últimos 25 años, la canícula dejó más de 15 días seguidos casi sin lluvia."),
    ("rojo", 3, "en 3 de los últimos 25 años, la canícula dejó más de 15 días seguidos casi sin lluvia."),
    ("gris", 0, "canícula: el satélite no ve bien aquí.")])
def test_frase_de_la_canicula_por_estado(estado, valor, dice):
    es, en = frases._canicula({"estado": estado, "valor": valor, "de": 25}, U, 15)
    assert dice in es.lower()
    assert ("midsummer drought: " in en.lower()) == (estado == "gris")


@pytest.mark.parametrize("pct, dice", [(24, "solo la cuarta parte"), (26, "solo la cuarta parte"), (20, "solo la quinta parte"),
                                       (22, "solo la quinta parte"), (35, "solo la tercera parte"), (50, "la mitad"),
                                       (100, "más o menos lo normal"), (130, "más de lo normal")])
def test_lluvia_de_este_anio_en_palabras_sin_exagerar(pct, dice):
    assert frases.parte_de_lo_normal(pct)[0].startswith(dice)


def test_frase_de_este_anio_compara_con_el_anio_mas_seco():
    e = {"pct_de_la_mediana": 24, "desde": 1991, "total_2026_mm": 79, "anio_mas_seco": 2018, "total_mas_seco_mm": 138}
    es, en = frases._este_anio(e)
    assert es == ("Este año, en julio y agosto, llovió solo la cuarta parte de lo normal (24 %). Es menos que en 2018, "
                  "el año más seco desde 1991. Es un dato preliminar.")
    assert en.startswith("This year, July and August got only a quarter of the normal rain (24 %).")
    es2, _ = frases._este_anio(dict(e, total_2026_mm=150))   # más que el año más seco: no se compara
    assert "2018" not in es2 and es2.endswith("Es un dato preliminar.")


def test_jocotan_publicado_tiene_este_anio_y_el_futuro():
    """Con los archivos que publica el sitio, Jocotán dice la lluvia de este año y los 33 futuros, y todo pasa el
    validador de cifras."""
    res = recomendar("jocotan")
    f = res["farmer"]
    assert f["este_anio"]["pct_de_la_mediana"] == 24 and f["este_anio"]["anio_mas_seco"] == 2018
    fu = f["futuros"]
    assert fu["n_modelos"] == 33 and (fu["desde"], fu["hasta"]) == (2041, 2060)
    aguantan = {r["id"]: r["aguantan"] for r in fu["rotaciones"]}
    assert aguantan == {"actual_maiz_frijol": 3, "leguminosa_canavalia": 3, "tolerante_sorgo_caupi": 33}
    assert all(sum(r["por_modelo"]) == r["aguantan"] and len(r["por_modelo"]) == 33 for r in fu["rotaciones"])
    ids = [x["id"] for x in f["frases"]]
    assert ids == ["parcela", "suelo", "quema", "canicula", "este_anio", "opciones", "futuro", "cierre"]
    futuro = next(x for x in f["frases"] if x["id"] == "futuro")
    assert futuro["es"] == ("La NASA calcula 33 climas posibles para 2041 a 2060. Si siembra como hoy, maíz con frijol, "
                            "le alcanza el agua en 3 de 33. Maíz con canavalia: en 3. Sorgo con caupí: en los 33.")
    assert contrato.errores_textos(res) == []


def test_con_confianza_baja_no_se_dice_el_futuro():
    """Camotán tiene las opciones en gris (falta SMAP de calidad): no se dice qué aguanta mejor en el futuro."""
    f = recomendar("camotan")["farmer"]
    assert f["opciones"]["estado"] == "gris"
    assert "futuro" not in [x["id"] for x in f["frases"]]


def _res_opciones(res: dict, totales: list[float], nivel: str = "alta") -> dict:
    out = copy.deepcopy(res)
    for r, t in zip(out["rotaciones"], totales):
        r["puntajes"]["total"] = t
        r["confianza"]["nivel"] = nivel
    out["farmer"] = farmer.bloque(out, U)
    return out


def test_frase_de_opciones_en_empate_no_nombra_ganadora(resultado_sintetico):
    res = _res_opciones(resultado_sintetico, [80, 88, 87])
    es = res["farmer"]["frases"][4]["es"]
    assert es.startswith("Hoy hay dos opciones parejas: ") and " o " in es and "mejor" not in es


def test_frase_de_opciones_olopa_nombra_las_tres_sin_ganadora(resultado_sintetico):
    res = _res_opciones(resultado_sintetico, [87, 90, 92], nivel="media")
    f = res["farmer"]["frases"][4]
    assert f["es"].startswith("Hoy, las tres opciones quedan parejas: lo que siembra hoy, ")
    assert f["en"].startswith("Today, all three options come out even: what you plant today, ")
    assert "mejor" not in f["es"]


def test_frase_de_opciones_cuando_una_destaca(resultado_sintetico):
    res = _res_opciones(resultado_sintetico, [80, 88, 84])
    nombre = resultado_sintetico["rotaciones"][1]["nombre_corto"]
    assert res["farmer"]["frases"][4]["es"] == f"Hoy, la opción que mejor sale es {nombre}."


def test_frase_de_opciones_en_gris_dice_por_que(resultado_sintetico):
    res = _res_opciones(resultado_sintetico, [80, 88, 84], nivel="baja")
    f = res["farmer"]["frases"][4]
    assert f["es"].startswith("No podemos decir qué opción conviene más: ")
    assert "mejor sale" not in f["es"]


# ---------------------------------------------------------------- tiempos y subtítulos
def test_unir_da_tiempos_crecientes_con_pausa():
    tasa = audio_frases.TASA_HZ
    pcm, tiempos, dur = audio_frases.unir([b"\x01\x00" * tasa, b"\x01\x00" * (tasa // 2)])
    assert tiempos == [[0.0, 1.0], [1.0 + audio_frases.PAUSA_S, 1.5 + audio_frases.PAUSA_S]]
    assert dur == 1.5 + audio_frases.PAUSA_S and len(pcm) == round(dur * tasa) * 2


def test_recortar_quita_el_silencio_de_los_bordes():
    tasa = audio_frases.TASA_HZ
    silencio, voz = b"\x00\x00" * tasa, b"\x10\x27" * tasa   # 1 s de silencio, 1 s de amplitud 10000
    out = audio_frases.recortar(silencio + voz + silencio)
    margen = int(audio_frases.MARGEN_S * tasa)
    assert len(out) == 2 * (tasa + 2 * margen)


def test_vtt_con_tiempos_y_sin_tiempos(resultado_sintetico):
    fr = copy.deepcopy(resultado_sintetico["farmer"]["frases"])
    with pytest.raises(ValueError):
        frases.vtt(fr, "es")
    for i, f in enumerate(fr):
        f["inicio_s"], f["fin_s"] = i * 4.0, i * 4.0 + 3.5
    v = frases.vtt(fr, "en")
    assert v.startswith("WEBVTT\n\n1\n00:00:00.000 --> 00:00:03.500\n" + fr[0]["en"])
    assert "00:00:20.000 --> 00:00:23.500" in v


def test_audio_corto_se_enlaza_solo_si_coinciden_las_frases(resultado_sintetico, tmp_path, monkeypatch):
    monkeypatch.setattr(exportar, "WEB_AUDIO", tmp_path)
    res = copy.deepcopy(resultado_sintetico)
    fr = res["farmer"]["frases"]
    ruta = tmp_path / "sint.frases.mp3"
    ruta.write_bytes(AUDIO_FALSO)
    tiempos = {"tiempos": [[i * 4.0, i * 4.0 + 3.5] for i in range(len(fr))], "duracion_s": 23.5}
    exportar.etiquetar(ruta, "Jocotán", "es-GT-MartaNeural", frases.texto_audio(fr), tiempos)
    assert exportar.audio_corto(res, "sint", "Jocotán", generar=False) is None
    a = res["farmer"]["audio"]["es"]
    assert a["mp3"] == "audio/sint.frases.mp3" and a["ia"]["generado_con_ia"] is True
    assert a["bytes"] == ruta.stat().st_size and a["duracion_s"] == 23.5
    assert [(f["inicio_s"], f["fin_s"]) for f in fr] == [tuple(t) for t in tiempos["tiempos"]]
    assert (tmp_path / "sint.frases.es.vtt").read_text(encoding="utf-8").count("-->") == len(fr)
    assert contrato.errores_esquema(res) == []
    # si cambia una frase, el mp3 ya no corresponde y no se enlaza
    otro = copy.deepcopy(resultado_sintetico)
    otro["farmer"]["frases"][1]["es"] = "Suelo: otra cosa."
    assert exportar.audio_corto(otro, "sint", "Jocotán", generar=False)
    assert otro["farmer"]["audio"]["es"] is None and otro["farmer"]["frases"][1]["inicio_s"] is None


def _cues(ruta) -> list[dict]:
    """Cues de un .vtt: [{"inicio": s, "fin": s, "texto": str}]."""
    def seg(m: str) -> float:
        h, mi, se = m.split(":")
        return int(h) * 3600 + int(mi) * 60 + float(se)
    out = []
    for bloque in ruta.read_text(encoding="utf-8").strip().split("\n\n")[1:]:
        _, marcas, texto = bloque.split("\n", 2)
        a, b = marcas.split(" --> ")
        out.append({"inicio": seg(a), "fin": seg(b), "texto": texto})
    return out


def _pcm_frase(seg_voz: float, pausa_interna: float) -> bytes:
    """Frase sintética ya recortada: margen bajo el umbral, voz, una pausa natural en cero, voz y margen."""
    tasa = audio_frases.TASA_HZ
    margen = b"\x64\x00" * int(audio_frases.MARGEN_S * tasa)       # amplitud 100: bajo UMBRAL_SILENCIO
    voz = b"\x10\x27" * int(seg_voz * tasa)
    return margen + voz + b"\x00\x00" * int(pausa_interna * tasa) + voz + margen


def test_tiempos_de_pcm_halla_las_uniones_y_no_las_pausas_naturales():
    # pausas naturales de 0.9, 0.2 y 0.33 s (comas y puntos) dentro de las frases: no son uniones
    pcms = [_pcm_frase(1.0, 0.9), _pcm_frase(0.7, 0.2), _pcm_frase(1.3, 0.33)]
    pcm, tiempos, dur = audio_frases.unir(pcms)
    t = audio_frases.tiempos_de_pcm(pcm, 3)
    assert t["duracion_s"] == dur
    for (a, b), (x, y) in zip(t["tiempos"], tiempos):
        assert abs(a - x) <= 0.002 and abs(b - y) <= 0.002
    assert audio_frases.tiempos_de_pcm(pcm, 4) is None       # con otro número de frases no inventa uniones


def test_tiempos_ingles_usa_la_etiqueta_si_termina_con_el_audio(tmp_path):
    ruta = tmp_path / "x.frases.en.mp3"
    ruta.write_bytes(AUDIO_FALSO)
    bien = {"tiempos": [[0.0, 2.0], [2.25, 5.0]], "duracion_s": 5.0}
    assert exportar.tiempos_ingles(ruta, {"TXXX": {audio_frases.CLAVE_TIEMPOS: json.dumps(bien)}}, 2) == bien
    # la etiqueta con los tiempos del español (terminan 0.5 s antes que el audio) no se usa
    mal = {"tiempos": [[0.0, 2.0], [2.25, 4.5]], "duracion_s": 5.0}
    assert exportar.tiempos_ingles(ruta, {"TXXX": {audio_frases.CLAVE_TIEMPOS: json.dumps(mal)}}, 2) != mal


# ---------------------------------------------------------------- archivos publicados
def _publicados():
    out = []
    for p in datos.parcelas():
        ruta = WEB / "data" / f"{p['id']}.json"
        if ruta.exists():
            res = json.loads(ruta.read_text(encoding="utf-8"))
            if ((res.get("farmer") or {}).get("audio") or {}).get("es"):
                out.append((p["id"], res))
    return out


PUBLICADOS = _publicados()


@pytest.mark.skipif(not PUBLICADOS, reason="sin audio corto publicado")
@pytest.mark.parametrize("pid, res", PUBLICADOS, ids=[p for p, _ in PUBLICADOS])
def test_nada_solo_en_audio(pid, res):
    """Cada frase del mp3 corto existe como texto visible en el JSON, en español y en inglés."""
    f = res["farmer"]
    a = f["audio"]["es"]
    ruta = WEB / a["mp3"]
    info = audio_id3.leer(ruta)
    # el mp3 se generó con exactamente el español de las frases del JSON (hash en la etiqueta)
    assert info["TXXX"][audio_id3.CLAVE_HASH] == audio_id3.hash_texto(frases.texto_audio(f["frases"]))
    t = audio_frases.tiempos_de_etiqueta(info)
    assert len(t["tiempos"]) == len(f["frases"])
    fin_anterior = -1.0
    for fr, (ini, fin) in zip(f["frases"], t["tiempos"]):
        assert fr["es"].strip() and fr["en"].strip()
        assert (fr["inicio_s"], fr["fin_s"]) == (ini, fin) and fin_anterior <= ini < fin <= t["duracion_s"]
        fin_anterior = fin
    # los subtítulos dicen lo mismo que las frases, en el mismo orden; los del español con los tiempos del
    # mp3 en español (los del inglés siguen su propio mp3: ver test_ultimo_subtitulo_termina_con_su_mp3)
    assert (WEB / a["subtitulos"]).read_text(encoding="utf-8") == frases.vtt(f["frases"], "es")
    for lang, clave in (("es", "subtitulos"), ("en", "subtitulos_en")):
        assert [c["texto"] for c in _cues(WEB / a[clave])] == [fr[lang] for fr in f["frases"]]
    assert contrato.errores_textos(res) == []


@pytest.mark.skipif(not PUBLICADOS, reason="sin audio corto publicado")
@pytest.mark.parametrize("pid, res", PUBLICADOS, ids=[p for p, _ in PUBLICADOS])
def test_audio_corto_dura_de_20_a_75_s_mono_y_declara_ia(pid, res):
    a = res["farmer"]["audio"]["es"]
    ruta = WEB / a["mp3"]
    assert 20 <= a["duracion_s"] <= 75
    assert a["bytes"] == ruta.stat().st_size
    c = audio_frases.cabecera_mp3(ruta.read_bytes())
    assert c["mono"] and 24 <= c["kbps"] <= 32 and c["kbps"] == a["kbps"] and c["capa"] == 3
    info = audio_id3.leer(ruta)
    assert info["TXXX"][audio_id3.MARCA_IA].startswith("true") and "No es una persona" in info["COMM"]
    assert a["ia"]["generado_con_ia"] is True and a["voz"].startswith(info["TXXX"]["MILPA_VOZ"])
    assert "prototipo" not in info["TALB"]


@pytest.mark.skipif(not PUBLICADOS, reason="sin audio corto publicado")
@pytest.mark.parametrize("pid, res", PUBLICADOS, ids=[p for p, _ in PUBLICADOS])
def test_mp3_corto_en_mono_y_kbps(pid, res):
    a = res["farmer"]["audio"]["en"]
    c = audio_frases.cabecera_mp3((WEB / a["mp3"]).read_bytes())
    assert c["mono"] and c["kbps"] == a["kbps"] and 24 <= a["kbps"] <= 32


def test_los_mp3_largos_ya_no_dicen_prototipo_local():
    for ruta in sorted((WEB / "audio").glob("*.mp3")):
        assert "prototipo" not in audio_id3.leer(ruta).get("TALB", ""), ruta.name


@pytest.mark.skipif(not PUBLICADOS, reason="sin audio corto publicado")
@pytest.mark.parametrize("pid, res", PUBLICADOS, ids=[p for p, _ in PUBLICADOS])
def test_mp3_corto_en_ingles_publicado(pid, res):
    """Cada parcela con audio en español lleva el mp3 en inglés, con IA y hasta 300 kB."""
    a = res["farmer"]["audio"]["en"]
    assert a and a["mp3"].endswith(".frases.en.mp3")
    assert a["bytes"] <= exportar.MAX_BYTES_FRASES
    ruta = WEB / a["mp3"]
    assert a["bytes"] == ruta.stat().st_size
    info = audio_id3.leer(ruta)
    assert info["TXXX"][audio_id3.MARCA_IA].startswith("true")
    assert "not a person" in info["COMM"].lower()
    assert info["TXXX"][audio_id3.CLAVE_HASH] == audio_id3.hash_texto(
        frases.texto_audio(res["farmer"]["frases"], "en"))
    assert a["ia"]["generado_con_ia"] is True


def test_la_tarjeta_respeta_la_regla_de_empate():
    for p in datos.parcelas():
        ruta = WEB / "data" / f"{p['id']}.json"
        if not ruta.exists():
            continue
        res = json.loads(ruta.read_text(encoding="utf-8"))
        op = res["farmer"]["opciones"]
        if op["estado"] in ("empate", "gris"):
            assert "mejor sale" not in res["texto_tarjeta"], p["id"]
        if op["estado"] == "empate":
            assert "quedan parejas" in res["texto_tarjeta"]
        assert not re.search(r"\balerta\b", res["texto_tarjeta"], re.I)


@pytest.mark.skipif(not PUBLICADOS, reason="sin audio corto publicado")
@pytest.mark.parametrize("pid, res", PUBLICADOS, ids=[p for p, _ in PUBLICADOS])
def test_ultimo_subtitulo_termina_con_su_mp3(pid, res):
    """El último cue de cada .frases.{es,en}.vtt termina a menos de 0.15 s del final de su mp3.

    La duración se cuenta por cuadros del mp3 (sin la etiqueta ni ffmpeg); incluye el relleno del codificador,
    unos 0.06 s. Los cues van en orden y sin cruzarse."""
    a = res["farmer"]["audio"]
    for bloque in (a["es"], a["en"]):
        dur = audio_frases.duracion_mp3((WEB / bloque["mp3"]).read_bytes())
        cues = _cues(WEB / bloque["subtitulos"])
        assert len(cues) == len(res["farmer"]["frases"])
        assert abs(cues[-1]["fin"] - dur) <= 0.15, (bloque["subtitulos"], cues[-1]["fin"], round(dur, 3))
        assert abs(cues[-1]["fin"] - bloque["duracion_s"]) <= 0.05
        fin = -1.0
        for c in cues:
            assert fin <= c["inicio"] < c["fin"]
            fin = c["fin"]


@pytest.mark.skipif(not PUBLICADOS or not audio_frases.ffmpeg(), reason="sin audio corto publicado o sin ffmpeg")
@pytest.mark.parametrize("pid, res", PUBLICADOS, ids=[p for p, _ in PUBLICADOS])
def test_las_uniones_del_mp3_dan_los_tiempos_de_la_etiqueta(pid, res):
    """Control del método: en el mp3 en español, cuyos tiempos guardó el exportador al generarlo, las uniones
    halladas en el audio dan esos mismos tiempos (±10 ms). En el inglés dan los del .en.vtt publicado."""
    n = len(res["farmer"]["frases"])
    ruta_es = WEB / res["farmer"]["audio"]["es"]["mp3"]
    etiqueta = audio_frases.tiempos_de_etiqueta(audio_id3.leer(ruta_es))
    assert etiqueta and len(etiqueta["tiempos"]) == n
    hallados = audio_frases.tiempos_de_mp3(ruta_es, n)
    # Con frases completas (15 nov 2026) puede haber una pausa dentro de una frase tan larga como una unión (Olopa): el
    # método de respaldo no cuadra y devuelve None. No se usa: cada mp3 trae sus tiempos exactos en la etiqueta.
    if hallados:
        for (a, b), (x, y) in zip(hallados["tiempos"], etiqueta["tiempos"]):
            assert abs(a - x) <= 0.01 and abs(b - y) <= 0.01
    en = res["farmer"]["audio"]["en"]
    et_en = audio_frases.tiempos_de_etiqueta(audio_id3.leer(WEB / en["mp3"]))
    assert et_en and len(et_en["tiempos"]) == n
    # El .en.vtt usa los tiempos que guardó el exportador en la etiqueta del mp3 en inglés (desde el 15 nov 2026 cada
    # mp3 en inglés trae los suyos); las uniones halladas en el audio, cuando cuadran, los confirman (±10 ms).
    cues = [[c["inicio"], c["fin"]] for c in _cues(WEB / en["subtitulos"])]
    assert cues == et_en["tiempos"]
    t_en = audio_frases.tiempos_de_mp3(WEB / en["mp3"], n)
    if t_en:
        for (a, b), (x, y) in zip(cues, t_en["tiempos"]):
            assert abs(a - x) <= 0.01 and abs(b - y) <= 0.01
