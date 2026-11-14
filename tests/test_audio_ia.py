"""Declaración de IA de los mp3: etiquetas ID3 propias, audio intacto y mp3 enlazado solo si coincide el texto."""
from __future__ import annotations

import json

from motor import audio_id3, datos, exportar

AUDIO_FALSO = b"\xff\xfb\x90\x64" + bytes(range(256)) * 8  # basta para probar: no se decodifica


def test_escribe_y_lee_la_etiqueta_sin_tocar_el_audio(tmp_path):
    ruta = tmp_path / "a.mp3"
    ruta.write_bytes(AUDIO_FALSO)
    exportar.etiquetar(ruta, "Jocotán", "es-GT-MartaNeural", "texto de la tarjeta")
    info = audio_id3.leer(ruta)
    assert ruta.read_bytes()[:3] == b"ID3"
    assert audio_id3.quitar_id3(ruta.read_bytes()) == AUDIO_FALSO
    assert "Jocotán" in info["TIT2"] and "IA" in info["TPE1"]
    assert "No es una persona" in info["COMM"]
    assert info["TXXX"][audio_id3.MARCA_IA].startswith("true")
    assert info["TXXX"][audio_id3.CLAVE_HASH] == audio_id3.hash_texto("texto de la tarjeta")


def test_volver_a_etiquetar_no_duplica_la_etiqueta(tmp_path):
    ruta = tmp_path / "a.mp3"
    ruta.write_bytes(AUDIO_FALSO)
    for _ in range(3):
        exportar.etiquetar(ruta, "Zacapa", "es-GT-MartaNeural", "otro texto")
    datos_ = ruta.read_bytes()
    assert datos_.count(b"ID3") == 1
    assert audio_id3.quitar_id3(datos_) == AUDIO_FALSO


def test_texto_fuera_de_latin1_usa_utf16(tmp_path):
    ruta = tmp_path / "a.mp3"
    ruta.write_bytes(AUDIO_FALSO)
    audio_id3.escribir(ruta, "título ✓", "voz", "álbum", "2026", "comentario ✓", {"CLAVE ✓": "valor ✓"})
    info = audio_id3.leer(ruta)
    assert info["TIT2"] == "título ✓" and info["COMM"] == "comentario ✓" and info["TXXX"]["CLAVE ✓"] == "valor ✓"


def test_mp3_solo_se_enlaza_si_coincide_el_texto_y_declara_ia(tmp_path):
    ruta = tmp_path / "a.mp3"
    ruta.write_bytes(AUDIO_FALSO)
    assert exportar.mp3_vigente(ruta, "texto") is None  # sin etiqueta de IA
    exportar.etiquetar(ruta, "Olopa", "es-GT-MartaNeural", "texto")
    assert exportar.mp3_vigente(ruta, "texto") is not None
    assert exportar.mp3_vigente(ruta, "texto distinto") is None  # el texto cambió: audio desactualizado
    assert exportar.mp3_vigente(tmp_path / "no_existe.mp3", "texto") is None


def test_los_mp3_publicados_declaran_ia_y_coinciden_con_su_json():
    web = datos.RAIZ / "web" / "public"
    for p in datos.parcelas():
        ruta_json = web / "data" / f"{p['id']}.json"
        if not ruta_json.exists():
            continue
        a = json.loads(ruta_json.read_text(encoding="utf-8"))["audio"]
        if not a.get("mp3"):
            continue
        assert a["ia"]["generado_con_ia"] is True and "IA" in a["ia"]["declaracion"]
        assert exportar.mp3_vigente(web / a["mp3"], a["texto"]) is not None, p["id"]


def test_la_tarjeta_en_ingles_tiene_su_mp3_con_etiqueta_de_ia():
    """audio.en: mp3 de la tarjeta en inglés, voz en-US, hash del texto en inglés y comentario ID3 en «eng»."""
    web = datos.RAIZ / "web" / "public"
    vistos = 0
    for p in datos.parcelas():
        ruta_json = web / "data" / f"{p['id']}.json"
        if not ruta_json.exists():
            continue
        res = json.loads(ruta_json.read_text(encoding="utf-8"))
        a = res["audio"]
        assert a["es"]["texto"] == a["texto"] and a["en"]["texto"] == res["en"]["texto_tarjeta"]
        if not a["en"]["mp3"]:
            continue
        vistos += 1
        assert a["en"]["ia"]["generado_con_ia"] is True and "AI-generated" in a["en"]["ia"]["declaracion"]
        assert a["en"]["voz"].startswith("en-US-")
        info = exportar.mp3_vigente(web / a["en"]["mp3"], a["en"]["texto"])
        assert info is not None, p["id"]
        assert info["TXXX"][audio_id3.MARCA_IA].startswith("true;") and "AI-generated" in info["COMM"]
        cab = (web / a["en"]["mp3"]).read_bytes()[:4096]
        i = cab.index(b"COMM")
        assert cab[i + 11:i + 14] == b"eng"   # 10 bytes de cabecera del marco + 1 de codificación
    assert vistos == 5


def test_el_comentario_id3_lleva_el_idioma(tmp_path):
    ruta = tmp_path / "x.mp3"
    ruta.write_bytes(AUDIO_FALSO)
    audio_id3.escribir(ruta, "t", "a", "al", "2026", "AI-generated synthetic voice", {}, idioma="eng")
    datos_mp3 = ruta.read_bytes()
    assert b"eng" in datos_mp3[:200] and audio_id3.leer(ruta)["COMM"] == "AI-generated synthetic voice"
