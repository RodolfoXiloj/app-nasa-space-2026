"""Audio corto por frases (paso 4 del plan): un mp3 de 20 a 30 s por parcela con las frases del bloque farmer.

Mismo método y voz que el audio de la tarjeta (motor/exportar.py --audio): edge-tts, voz es-GT-MartaNeural
con respaldo es-MX-DaliaNeural y velocidad -5 %. Exige MILPA_ONLINE=1, red y ffmpeg; si falta algo,
devuelve None y no se inventa nada: las frases y su texto quedan en el JSON sin mp3.

Cada frase se sintetiza aparte. ffmpeg la pasa a PCM, se recorta el silencio de los bordes, se unen con
una pausa corta y se codifica una sola vez en mp3 mono a 32 kbps (24 kHz). Así el inicio y el fin de cada
frase se conocen al milisegundo: van al JSON (farmer.frases), a los subtítulos WebVTT y a la etiqueta ID3
(MILPA_TIEMPOS), junto con el hash del texto leído.
"""
from __future__ import annotations

import asyncio
import json
import os
import shutil
import subprocess
import sys
import tempfile
from array import array
from pathlib import Path

KBPS = 32
TASA_HZ = 24000
PAUSA_S = 0.25
MARGEN_S = 0.06          # silencio que se deja en cada borde de la frase al recortar
UMBRAL_SILENCIO = 400    # amplitud de 16 bits por debajo de la cual se considera silencio
CLAVE_TIEMPOS = "MILPA_TIEMPOS"


def ffmpeg() -> str | None:
    return shutil.which("ffmpeg")


def recortar(pcm: bytes) -> bytes:
    """Quita el silencio del principio y del final (PCM 16 bits mono), dejando MARGEN_S en cada borde."""
    m = array("h")
    m.frombytes(pcm)
    if sys.byteorder == "big":
        m.byteswap()
    ini = next((i for i, v in enumerate(m) if abs(v) > UMBRAL_SILENCIO), None)
    if ini is None:
        return pcm
    fin = next(i for i in range(len(m) - 1, -1, -1) if abs(m[i]) > UMBRAL_SILENCIO)
    margen = int(MARGEN_S * TASA_HZ)
    a, b = max(0, ini - margen), min(len(m), fin + 1 + margen)
    return pcm[2 * a:2 * b]


def _a_pcm(ff: str, mp3: Path) -> bytes:
    return subprocess.run([ff, "-v", "error", "-i", str(mp3), "-ac", "1", "-ar", str(TASA_HZ), "-f", "s16le", "-"],
                          capture_output=True, check=True).stdout


def unir(pcms: list[bytes]) -> tuple[bytes, list[list[float]], float]:
    """PCM de todas las frases con una pausa entre ellas, (inicio, fin) de cada una y duración total en s."""
    pausa = b"\x00\x00" * int(PAUSA_S * TASA_HZ)
    partes, tiempos, n = [], [], 0
    for i, p in enumerate(pcms):
        if i:
            partes.append(pausa)
            n += len(pausa) // 2
        tiempos.append([round(n / TASA_HZ, 3), round((n + len(p) // 2) / TASA_HZ, 3)])
        partes.append(p)
        n += len(p) // 2
    return b"".join(partes), tiempos, round(n / TASA_HZ, 3)


def codificar(ff: str, pcm: bytes, ruta: Path) -> None:
    """mp3 mono CBR a KBPS, sin etiquetas propias de ffmpeg (las pone motor/audio_id3.py)."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([ff, "-v", "error", "-y", "-f", "s16le", "-ar", str(TASA_HZ), "-ac", "1", "-i", "-",
                    "-c:a", "libmp3lame", "-b:a", f"{KBPS}k", "-ac", "1", "-ar", str(TASA_HZ),
                    "-map_metadata", "-1", "-id3v2_version", "0", str(ruta)], input=pcm, check=True)


def sintetizar(frases_es: list[str], ruta: Path, voces: list[str], rate: str) -> dict | None:
    """Genera el mp3 de las frases. Devuelve {"voz", "tiempos", "duracion_s"} o None si no se pudo."""
    if os.environ.get("MILPA_ONLINE") != "1":
        return None
    ff = ffmpeg()
    if not ff:
        print("[audio corto] falta ffmpeg", file=sys.stderr)
        return None
    try:
        import edge_tts
    except ImportError:
        print("[audio corto] falta edge-tts", file=sys.stderr)
        return None
    with tempfile.TemporaryDirectory() as tmp:
        for voz in voces:
            try:
                pcms = []
                for i, texto in enumerate(frases_es):
                    mp3 = Path(tmp) / f"{voz}_{i}.mp3"
                    asyncio.run(edge_tts.Communicate(texto, voz, rate=rate).save(str(mp3)))
                    pcms.append(recortar(_a_pcm(ff, mp3)))
                pcm, tiempos, dur = unir(pcms)
                codificar(ff, pcm, ruta)
                return {"voz": voz, "tiempos": tiempos, "duracion_s": dur}
            except Exception as e:  # noqa: BLE001
                print(f"[audio corto] {voz} falló: {type(e).__name__}: {e}", file=sys.stderr)
    return None


def tiempos_de_etiqueta(info: dict) -> dict | None:
    """{"tiempos": [[inicio, fin], ...], "duracion_s": x} guardado en la etiqueta ID3, o None."""
    crudo = (info.get("TXXX") or {}).get(CLAVE_TIEMPOS)
    if not crudo:
        return None
    try:
        d = json.loads(crudo)
    except ValueError:
        return None
    return d if isinstance(d, dict) and d.get("tiempos") else None


def _cuadro(audio: bytes, i: int) -> dict:
    b1, b2, b3 = audio[i + 1], audio[i + 2], audio[i + 3]
    version = {3: 1, 2: 2, 0: 2.5}[(b1 >> 3) & 0x03]
    capa = 4 - ((b1 >> 1) & 0x03)
    tabla = ([0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320] if version == 1 else
             [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160])
    hz = {1: [44100, 48000, 32000], 2: [22050, 24000, 16000], 2.5: [11025, 12000, 8000]}[version][(b2 >> 2) & 0x03]
    kbps = tabla[b2 >> 4]
    largo = (144000 if version == 1 else 72000) * kbps // hz + ((b2 >> 1) & 0x01)
    return {"version": version, "capa": capa, "kbps": kbps, "hz": hz, "mono": (b3 >> 6) == 3, "largo": largo}


def cabecera_mp3(datos: bytes) -> dict:
    """Encabezado del primer cuadro de audio después de la etiqueta ID3: versión, kbps, Hz y canales.

    LAME escribe antes un cuadro «Info» (o «Xing») con su propio bitrate; ese se salta."""
    from motor import audio_id3

    audio = audio_id3.quitar_id3(datos)
    i = next(k for k in range(len(audio) - 4) if audio[k] == 0xFF and (audio[k + 1] & 0xE0) == 0xE0)
    c = _cuadro(audio, i)
    if b"Info" in audio[i:i + c["largo"]] or b"Xing" in audio[i:i + c["largo"]]:
        i += c["largo"]
        c = _cuadro(audio, i)
    return c
