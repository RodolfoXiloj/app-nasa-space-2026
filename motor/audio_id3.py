"""Etiquetas ID3v2.3 mínimas para declarar que los mp3 son voz sintética generada con IA.

Sin dependencias: escribe y lee solo los marcos que usa el proyecto (TIT2, TPE1, TALB, TYER, COMM,
TXXX). Al escribir, quita cualquier etiqueta ID3v2 previa al inicio del archivo y deja el audio
intacto. El marco TXXX «MILPA_TEXTO_SHA256» guarda el hash del texto leído: la exportación solo
enlaza un mp3 si su hash coincide con el texto actual de la tarjeta.
"""
from __future__ import annotations

import hashlib
import struct
from pathlib import Path

MARCA_IA = "AI_GENERATED"
CLAVE_HASH = "MILPA_TEXTO_SHA256"


def hash_texto(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def _cod(s: str) -> tuple[bytes, bytes]:
    """(byte de codificación, texto codificado): Latin-1 si alcanza, si no UTF-16 con BOM."""
    try:
        return b"\x00", s.encode("latin-1")
    except UnicodeEncodeError:
        return b"\x01", s.encode("utf-16")


def _term(cod: bytes) -> bytes:
    return b"\x00" if cod == b"\x00" else b"\x00\x00"


def _marco(fid: str, datos: bytes) -> bytes:
    return fid.encode("ascii") + struct.pack(">I", len(datos)) + b"\x00\x00" + datos


def _texto(fid: str, s: str) -> bytes:
    c, b = _cod(s)
    return _marco(fid, c + b)


def _txxx(desc: str, valor: str) -> bytes:
    c, _ = _cod(desc + valor)
    enc = "latin-1" if c == b"\x00" else "utf-16"
    return _marco("TXXX", c + desc.encode(enc) + _term(c) + valor.encode(enc))


def _comm(texto: str, idioma: str = "spa") -> bytes:
    c, b = _cod(texto)
    return _marco("COMM", c + idioma.encode("ascii") + _term(c) + b)


def _sincro(n: int) -> bytes:
    return bytes([(n >> 21) & 0x7F, (n >> 14) & 0x7F, (n >> 7) & 0x7F, n & 0x7F])


def _de_sincro(b: bytes) -> int:
    return (b[0] << 21) | (b[1] << 14) | (b[2] << 7) | b[3]


def quitar_id3(datos: bytes) -> bytes:
    """Audio sin la etiqueta ID3v2 inicial (si la hay)."""
    if len(datos) >= 10 and datos[:3] == b"ID3":
        tam = _de_sincro(datos[6:10]) + 10 + (10 if datos[5] & 0x10 else 0)
        return datos[tam:]
    return datos


def escribir(ruta: Path, titulo: str, artista: str, album: str, anio: str, comentario: str,
             extra: dict[str, str]) -> None:
    ruta = Path(ruta)
    audio = quitar_id3(ruta.read_bytes())
    marcos = (_texto("TIT2", titulo) + _texto("TPE1", artista) + _texto("TALB", album) + _texto("TYER", anio)
              + _comm(comentario) + b"".join(_txxx(k, v) for k, v in extra.items()))
    relleno = b"\x00" * 64
    cab = b"ID3\x03\x00\x00" + _sincro(len(marcos) + len(relleno))
    ruta.write_bytes(cab + marcos + relleno + audio)


def _decodificar(cod: int, b: bytes) -> str:
    if cod == 0:
        return b.decode("latin-1").rstrip("\x00")
    return b.decode("utf-16").rstrip("\x00")


def leer(ruta: Path) -> dict:
    """Marcos de texto de la etiqueta ID3v2.3 del proyecto: {"TIT2": ..., "COMM": ..., "TXXX": {desc: valor}}."""
    datos = Path(ruta).read_bytes()
    if datos[:3] != b"ID3" or datos[3] != 3:
        return {}
    fin = 10 + _de_sincro(datos[6:10])
    i, out, txxx = 10, {}, {}
    while i + 10 <= fin:
        fid = datos[i:i + 4]
        if fid == b"\x00\x00\x00\x00":
            break
        tam = struct.unpack(">I", datos[i + 4:i + 8])[0]
        cuerpo = datos[i + 10:i + 10 + tam]
        i += 10 + tam
        cod, resto = cuerpo[0], cuerpo[1:]
        sep = b"\x00" if cod == 0 else b"\x00\x00"
        nombre = fid.decode("ascii", "replace")
        if nombre == "TXXX":
            k = _buscar_sep(resto, sep, cod)
            txxx[_decodificar(cod, resto[:k])] = _decodificar(cod, resto[k + len(sep):])
        elif nombre == "COMM":
            resto = resto[3:]
            k = _buscar_sep(resto, sep, cod)
            out["COMM"] = _decodificar(cod, resto[k + len(sep):])
        elif nombre.startswith("T"):
            out[nombre] = _decodificar(cod, resto)
    out["TXXX"] = txxx
    return out


def _buscar_sep(b: bytes, sep: bytes, cod: int) -> int:
    if cod == 0:
        return b.index(sep)
    k = 0
    while True:  # en UTF-16 el terminador va alineado a 2 bytes
        k = b.index(sep, k)
        if k % 2 == 0:
            return k
        k += 1
