"""Exportación estática: corre el motor para cada parcela con caché y escribe el JSON en la web.

    python -m motor.exportar                 # todas las parcelas con caché
    python -m motor.exportar jocotan         # una sola
    MILPA_ONLINE=1 python -m motor.exportar --audio   # además, mp3 con edge-tts
    python -m motor.exportar --etiquetar     # solo pone las etiquetas ID3 de IA a los mp3 vigentes

Audio: cada mp3 es voz sintética generada con IA. Se declara en el JSON (audio.ia, que la web muestra
junto al reproductor) y en las etiquetas ID3 del archivo (motor/audio_id3.py). Un mp3 solo se
enlaza si el hash del texto guardado en su etiqueta coincide con el texto actual.
Hay dos audios por parcela (cultivo por defecto):
    audio/{parcela}.mp3          la tarjeta completa (~70 s), en `audio`
    audio/{parcela}.frases.mp3      frases cortas en español (20 a 30 s, mono a 32 kbps), en `farmer.audio.es`
    audio/{parcela}.frases.en.mp3   las mismas frases en inglés, en `farmer.audio.en`; subtítulos
                                    audio/{parcela}.frases.{es,en}.vtt; tiempos en `farmer.frases`
                                    (motor/audio_frases.py)

Escribe:
    web/public/data/{parcela}.json            cultivo declarado por defecto (maíz + frijol)
    web/public/data/{parcela}.{cultivo}.json  maiz_solo y sorgo
    web/public/data/parcelas.json             índice para el mapa (también las parcelas sin datos)
    web/public/data/ejemplo.json              copia del contrato de ejemplo escrito a mano

Falla (código 1) si un JSON no cumple el contrato, si a una rotación le falta uno de los 5 campos
del reto, o si un texto trae una cifra o una fecha de siembra sin respaldo.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from motor import audio_frases, audio_id3, contrato, datos, frases, ingles
from motor.recomendar import ContratoIncompleto, recomendar

WEB_DATA = datos.RAIZ / "web" / "public" / "data"
WEB_AUDIO = datos.RAIZ / "web" / "public" / "audio"
VOCES = ["es-GT-MartaNeural", "es-MX-DaliaNeural"]  # plan: voz es-GT, respaldo es-MX
VOCES_EN = ["en-US-JennyNeural", "en-US-AriaNeural"]
RATE = "-5%"
RATE_EN = "-5%"
MAX_BYTES_FRASES = 120_000
ALBUM = "Milpa Resiliente"
CULTIVOS = ["maiz_frijol", "maiz_solo", "sorgo"]
PRIORIDAD = "agua"
HERRAMIENTA_VOZ = "edge-tts, texto a voz neural de Microsoft"


def declaracion_ia(voz: str) -> dict:
    """Lo que la web muestra junto al reproductor y lo que va en la etiqueta del mp3."""
    d = {"generado_con_ia": True, "herramienta": HERRAMIENTA_VOZ, "voz": voz,
         "declaracion": (f"Voz sintética generada con IA ({HERRAMIENTA_VOZ}; voz {voz}) a partir del texto que "
                         "redactó el motor con plantillas. No es una persona.")}
    ingles.bilingue(d, {"declaracion": ingles.declaracion_ia(voz, ingles.HERRAMIENTA_EN),
                        "herramienta": ingles.HERRAMIENTA_EN})
    return d


def etiquetar(ruta: Path, municipio: str, voz: str, texto: str, tiempos: dict | None = None, *,
              en: bool = False) -> None:
    """Etiqueta ID3 de IA. Con `tiempos` es el audio corto por frases: guarda el inicio y fin de cada frase."""
    herramienta = ingles.HERRAMIENTA_EN if en else HERRAMIENTA_VOZ
    d = declaracion_ia(voz) if not en else {"declaracion": ingles.declaracion_ia(voz, herramienta)}
    comentario = d["declaracion"]
    titulo = (f"Milpa Resiliente: {municipio}, short phrase audio (synthetic voice)" if en and tiempos else
              f"Milpa Resiliente: {municipio}, audio corto por frases (voz sintética)" if tiempos else
              f"Milpa Resiliente: tarjeta de {municipio} (voz sintética)")
    artista = (f"AI-generated synthetic voice: {voz}" if en else
               f"Voz sintética generada con IA: {voz}")
    extra = {audio_id3.MARCA_IA: f"true; {herramienta}; voz {voz}",
             "MILPA_VOZ": voz, audio_id3.CLAVE_HASH: audio_id3.hash_texto(texto)}
    if tiempos:
        extra[audio_frases.CLAVE_TIEMPOS] = json.dumps(tiempos, separators=(",", ":"))
    audio_id3.escribir(ruta, titulo=titulo, artista=artista, album=ALBUM,
                       anio="2026", comentario=comentario, extra=extra)


def declaracion_ia_bloque(voz: str, en: bool = False) -> dict:
    """Metadatos de IA para farmer.audio.es o farmer.audio.en."""
    if not en:
        return declaracion_ia(voz)
    decl_en = ingles.declaracion_ia(voz, ingles.HERRAMIENTA_EN)
    decl_es = (f"Voz sintética generada con IA ({HERRAMIENTA_VOZ}; voz {voz}) a partir del texto que "
               "redactó el motor con plantillas. No es una persona.")
    return {
        "generado_con_ia": True, "herramienta": ingles.HERRAMIENTA_EN, "voz": voz, "declaracion": decl_en,
        "es": {"declaracion": decl_es, "herramienta": HERRAMIENTA_VOZ},
        "en": {"declaracion": decl_en, "herramienta": ingles.HERRAMIENTA_EN},
    }


def mp3_vigente(ruta: Path, texto: str) -> dict | None:
    """Etiqueta del mp3 si existe, declara IA y fue generado con este mismo texto; si no, None."""
    if not ruta.exists():
        return None
    info = audio_id3.leer(ruta)
    tx = info.get("TXXX", {})
    if audio_id3.MARCA_IA in tx and tx.get(audio_id3.CLAVE_HASH) == audio_id3.hash_texto(texto):
        return info
    return None


def etiquetar_existentes(destino: Path = WEB_DATA) -> list[str]:
    """Etiqueta los mp3 ya generados con el texto y la voz de su JSON actual (sin volver a generarlos)."""
    hechos = []
    for p in datos.parcelas():
        ruta_json, ruta_mp3 = destino / f"{p['id']}.json", WEB_AUDIO / f"{p['id']}.mp3"
        if not (ruta_json.exists() and ruta_mp3.exists()):
            continue
        a = json.loads(ruta_json.read_text(encoding="utf-8")).get("audio") or {}
        if not a.get("mp3") or not a.get("texto"):
            continue
        voz = (a.get("voz") or VOCES[0]).split(" ")[0]
        etiquetar(ruta_mp3, p["municipio"], voz, a["texto"])
        hechos.append(p["id"])
    return hechos


def _escribir(ruta: Path, obj: dict) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def generar_audio(texto: str, ruta: Path) -> str | None:
    """mp3 de la tarjeta con edge-tts (voz neural de Microsoft, sin cuenta). Devuelve la voz usada o None.

    Solo se envía el texto de la tarjeta (sin datos personales). Exige MILPA_ONLINE=1. Si falla, la web
    usa la voz del navegador.
    """
    import asyncio
    import os

    if os.environ.get("MILPA_ONLINE") != "1":
        return None
    try:
        import edge_tts
    except ImportError:
        return None
    ruta.parent.mkdir(parents=True, exist_ok=True)
    for voz in VOCES:
        try:
            asyncio.run(edge_tts.Communicate(texto, voz, rate=RATE).save(str(ruta)))
            if ruta.exists() and ruta.stat().st_size > 1000:
                return voz
        except Exception as e:  # noqa: BLE001
            print(f"[audio] {voz} falló: {type(e).__name__}", file=sys.stderr)
    return None


def audio_corto(res: dict, pid: str, municipio: str, generar: bool) -> str | None:
    """Enlaza (y con `generar`, crea) el mp3 corto de las frases del bloque farmer.

    Llena `farmer.frases[].inicio_s/fin_s` y `farmer.audio.es`, y escribe los subtítulos WebVTT en español e
    inglés. Si no hay mp3 vigente para el texto actual, deja los tiempos en None y la ranura en None.
    Devuelve un aviso o None."""
    f = res["farmer"]
    if not f["frases"]:
        return None
    ruta = WEB_AUDIO / f"{pid}.frases.mp3"
    texto = frases.texto_audio(f["frases"])
    if generar:
        r = audio_frases.sintetizar([x["es"] for x in f["frases"]], ruta, VOCES, RATE)
        if r:
            etiquetar(ruta, municipio, r["voz"], texto, {"tiempos": r["tiempos"], "duracion_s": r["duracion_s"]})
    info = mp3_vigente(ruta, texto)
    t = audio_frases.tiempos_de_etiqueta(info) if info else None
    if not t or len(t["tiempos"]) != len(f["frases"]):
        return (f"{pid}: el mp3 corto no existe o no coincide con las frases actuales; no se enlaza "
                "(corra con --audio)") if ruta.exists() or generar else None
    for x, (a, b) in zip(f["frases"], t["tiempos"]):
        x["inicio_s"], x["fin_s"] = a, b
    subs = {}
    for lang in ("es", "en"):
        rel = f"audio/{pid}.frases.{lang}.vtt"
        (WEB_AUDIO / f"{pid}.frases.{lang}.vtt").write_text(frases.vtt(f["frases"], lang), encoding="utf-8")
        subs[lang] = rel
    voz = info["TXXX"].get("MILPA_VOZ") or VOCES[0]
    f["audio"]["es"] = {
        "mp3": f"audio/{pid}.frases.mp3", "subtitulos": subs["es"], "subtitulos_en": subs["en"],
        "voz": f"{voz} (edge-tts, voz neural sintética)", "ia": declaracion_ia(voz),
        "duracion_s": round(t["duracion_s"], 1), "bytes": ruta.stat().st_size, "kbps": audio_frases.KBPS,
    }
    texto_en = frases.texto_audio(f["frases"], "en")
    ruta_en = WEB_AUDIO / f"{pid}.frases.en.mp3"
    r_en = None
    if generar:
        for kbps in (audio_frases.KBPS, 28, 24):
            r_try = audio_frases.sintetizar([x["en"] for x in f["frases"]], ruta_en, VOCES_EN, RATE_EN, kbps)
            if not r_try:
                continue
            tiempos_en = {"tiempos": t["tiempos"], "duracion_s": r_try["duracion_s"]}
            etiquetar(ruta_en, municipio, r_try["voz"], texto_en, tiempos_en, en=True)
            if ruta_en.stat().st_size <= MAX_BYTES_FRASES:
                r_en = r_try
                break
            print(f"[exportar] {pid}: mp3 corto en inglés a {kbps} kbps pesa {ruta_en.stat().st_size} B "
                  f"(máximo {MAX_BYTES_FRASES})", file=sys.stderr)
            ruta_en.unlink(missing_ok=True)
    info_en = mp3_vigente(ruta_en, texto_en)
    if info_en:
        voz_en = info_en["TXXX"].get("MILPA_VOZ") or VOCES_EN[0]
        kbps_en = (r_en or {}).get("kbps") or audio_frases.cabecera_mp3(ruta_en.read_bytes())["kbps"]
        f["audio"]["en"] = {
            "mp3": f"audio/{pid}.frases.en.mp3", "subtitulos": subs["en"], "subtitulos_es": subs["es"],
            "voz": f"{voz_en} (edge-tts, neural synthetic voice)", "ia": declaracion_ia_bloque(voz_en, en=True),
            "duracion_s": round(audio_frases.tiempos_de_etiqueta(info_en)["duracion_s"], 1),
            "bytes": ruta_en.stat().st_size, "kbps": kbps_en,
        }
    else:
        f["audio"]["en"] = None
    return None


def exportar(pids: list[str] | None = None, destino: Path = WEB_DATA, validar_esquema: bool = True,
             audio: bool = False) -> dict:
    destino.mkdir(parents=True, exist_ok=True)
    indice = []
    errores: list[str] = []
    for p in datos.parcelas():
        if pids and p["id"] not in pids:
            continue
        disp = datos.disponibilidad(p["id"])
        faltan = [k for k in ("ndvi", "power_diario") if not disp[k]]
        entrada = {"id": p["id"], "nombre": p["nombre"], "municipio": p["municipio"], "departamento": p["departamento"],
                   "lat": p["lat"], "lon": p["lon"], "provisional": bool(p.get("provisional")),
                   "disponible": not faltan, "faltan": faltan, "archivos": {}, "fuentes_en_cache": disp}
        if not faltan:
            for cultivo in CULTIVOS:
                try:
                    res = recomendar(p["id"], cultivo=cultivo, prioridad=PRIORIDAD)
                except ContratoIncompleto as e:
                    errores.append(f"{p['id']}/{cultivo}: {e}")
                    continue
                errs = contrato.errores_textos(res)
                if validar_esquema:
                    errs += contrato.errores_esquema(res)
                if errs:
                    errores += [f"{p['id']}/{cultivo}: {x}" for x in errs]
                    continue
                if cultivo == CULTIVOS[0]:
                    ruta_mp3 = WEB_AUDIO / f"{p['id']}.mp3"
                    voz = generar_audio(res["audio"]["texto"], ruta_mp3) if audio else None
                    if voz:
                        etiquetar(ruta_mp3, p["municipio"], voz, res["audio"]["texto"])
                    info = mp3_vigente(ruta_mp3, res["audio"]["texto"])
                    if info:
                        voz_mp3 = info["TXXX"].get("MILPA_VOZ") or voz or VOCES[0]
                        res["audio"]["mp3"] = f"audio/{p['id']}.mp3"
                        res["audio"]["voz"] = f"{voz_mp3} (edge-tts, voz neural sintética)"
                        res["audio"]["ia"] = declaracion_ia(voz_mp3)
                    elif ruta_mp3.exists():
                        print(f"[exportar] {p['id']}: el mp3 no coincide con el texto actual o no declara IA; "
                              "no se enlaza (corra con --audio)", file=sys.stderr)
                    aviso = audio_corto(res, p["id"], p["municipio"], generar=audio)
                    if aviso:
                        print(f"[exportar] {aviso}", file=sys.stderr)
                nombre = f"{p['id']}.json" if cultivo == CULTIVOS[0] else f"{p['id']}.{cultivo}.json"
                _escribir(destino / nombre, res)
                entrada["archivos"][cultivo] = f"data/{nombre}"
                if cultivo == CULTIVOS[0]:
                    entrada["resumen"] = {
                        "meses_desnudos": res["deteccion"]["meses_desnudos"],
                        "anios_con_quema": res["deteccion"]["quemas"]["anios_con_quema"],
                        "confianza": res["rotaciones"][0]["confianza"]["nivel"],
                    }
            print(f"[exportar] {p['id']}: {len(entrada['archivos'])} archivos")
        else:
            print(f"[exportar] {p['id']}: sin caché de {', '.join(faltan)} (aparece en el mapa como pendiente)")
        indice.append(entrada)
    if contrato.EJEMPLO.exists():
        shutil.copyfile(contrato.EJEMPLO, destino / "ejemplo.json")
    _escribir(destino / "parcelas.json", {"version_contrato": "1.0", "parcelas": ingles.parcelas_indice(indice)})
    # validacion.json lo escribe pipeline/validacion/validar.py; aquí solo se le agregan los textos en inglés
    ruta_val = destino / "validacion.json"
    if ruta_val.exists():
        _escribir(ruta_val, ingles.validacion(json.loads(ruta_val.read_text(encoding="utf-8"))))
    return {"indice": indice, "errores": errores}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("parcelas", nargs="*")
    ap.add_argument("--audio", action="store_true", help="genera mp3 con edge-tts (requiere MILPA_ONLINE=1)")
    ap.add_argument("--etiquetar", action="store_true", help="solo etiqueta (ID3, IA) los mp3 ya generados")
    a = ap.parse_args()
    if a.etiquetar:
        print("[exportar] etiquetados:", ", ".join(etiquetar_existentes()) or "ninguno")
        sys.exit(0)
    r = exportar(a.parcelas or None, audio=a.audio)
    if r["errores"]:
        print("\nLa exportación FALLÓ:", file=sys.stderr)
        for e in r["errores"]:
            print("  -", e, file=sys.stderr)
        sys.exit(1)
    print("[exportar] listo")
