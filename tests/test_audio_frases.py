"""Audio corto por frases (paso 4): frases en dos idiomas, tiempos, subtítulos y la regla «nada solo en audio».

Las pruebas de los archivos publicados leen web/public/data y web/public/audio; las demás no usan red.
"""
import copy
import json
import re

import pytest

from motor import audio_frases, audio_id3, contrato, datos, exportar, farmer, frases

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


@pytest.mark.parametrize("estado, valor, poca, dice", [
    ("verde", 0, [], "no vio suelo desnudo"),
    ("amarillo", 0, [3, 4], "2 meses con poca cobertura, ninguno desnudo"),
    ("amarillo", 1, [1, 2, 3, 5], "1 mes de suelo desnudo y 4 con poca cobertura"),
    ("rojo", 3, [1, 5], "3 meses de suelo desnudo."),
    ("gris", 0, [], "el satélite no ve bien aquí"),
])
def test_frase_del_suelo_por_estado(resultado_sintetico, estado, valor, poca, dice):
    h = dict(resultado_sintetico["farmer"]["hechos"][0], estado=estado, valor=valor, meses_poca_cobertura=poca)
    es, en = frases._suelo(h, U)
    assert es.startswith("Suelo: ") and dice in es.lower()
    assert en.startswith("Soil: ")
    palabra = U["estados"][estado]
    assert palabra["es"].lower() in es.lower() and palabra["en"].lower() in en.lower()


@pytest.mark.parametrize("estado, valor, dice", [
    ("verde", 0, "no vio quemas cerca en 15 años"), ("amarillo", 2, "2 de 15 años"),
    ("rojo", 3, "3 de 15 años"), ("gris", 0, "no ve bien aquí")])
def test_frase_de_la_quema_por_estado(estado, valor, dice):
    es, en = frases._quema({"estado": estado, "valor": valor, "de": 15}, U)
    assert dice in es.lower() and en.startswith("Burning: ")


@pytest.mark.parametrize("estado, valor, dice", [
    ("verde", 0, "ninguna racha seca pasó de 15 días en 25 años"), ("amarillo", 1, "en 1 de 25 años"),
    ("rojo", 3, "en 3 de 25 años"), ("gris", 0, "no ve bien aquí")])
def test_frase_de_la_canicula_por_estado(estado, valor, dice):
    es, en = frases._canicula({"estado": estado, "valor": valor, "de": 25}, U, 15)
    assert dice in es.lower() and en.startswith("Midsummer drought: ")


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
    assert es.startswith("Hay dos opciones parejas: ") and " o " in es and "mejor" not in es


def test_frase_de_opciones_olopa_nombra_las_tres_sin_ganadora(resultado_sintetico):
    res = _res_opciones(resultado_sintetico, [87, 90, 92], nivel="media")
    f = res["farmer"]["frases"][4]
    assert f["es"].startswith("Las tres opciones quedan parejas: lo que siembra hoy, ")
    assert f["en"].startswith("All three options come out even: what you plant today, ")
    assert "mejor" not in f["es"]


def test_frase_de_opciones_cuando_una_destaca(resultado_sintetico):
    res = _res_opciones(resultado_sintetico, [80, 88, 84])
    nombre = resultado_sintetico["rotaciones"][1]["nombre_corto"]
    assert res["farmer"]["frases"][4]["es"] == f"La opción que mejor sale es {nombre}."


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
    # los subtítulos dicen lo mismo que las frases, en el mismo orden
    for lang, clave in (("es", "subtitulos"), ("en", "subtitulos_en")):
        vtt = (WEB / a[clave]).read_text(encoding="utf-8")
        assert vtt == frases.vtt(f["frases"], lang)
        cues = [b.split("\n")[2] for b in vtt.strip().split("\n\n")[1:]]
        assert cues == [fr[lang] for fr in f["frases"]]
    assert contrato.errores_textos(res) == []


@pytest.mark.skipif(not PUBLICADOS, reason="sin audio corto publicado")
@pytest.mark.parametrize("pid, res", PUBLICADOS, ids=[p for p, _ in PUBLICADOS])
def test_audio_corto_dura_de_20_a_30_s_mono_y_declara_ia(pid, res):
    a = res["farmer"]["audio"]["es"]
    ruta = WEB / a["mp3"]
    assert 20 <= a["duracion_s"] <= 30
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
    """Cada parcela con audio en español lleva el mp3 en inglés, con IA y hasta 120 kB."""
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
