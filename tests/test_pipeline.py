"""Pruebas del pipeline que NO usan red: LZW de CHIRPS, corrección de lluvia, .env, AppEEARS, coordenadas."""
import io
import json
import os
import random
import struct
from datetime import date, timedelta

import pytest

from motor import clima, datos
from pipeline import cache
from pipeline.clientes import appeears_smap, chirps


# ---------------------------------------------------------------- CHIRPS: decodificador LZW
def _tiff_lzw_float(ancho: int, alto: int, valores: list[float]) -> bytes:
    from PIL import Image

    im = Image.new("F", (ancho, alto))
    im.putdata(valores)
    buf = io.BytesIO()
    im.save(buf, format="TIFF", compression="tiff_lzw")
    return buf.getvalue()


def _franjas(tif: bytes) -> list[bytes]:
    """Franjas comprimidas de un TIFF (para probar el decodificador sin red)."""
    orden = "<" if tif[:2] == b"II" else ">"
    ifd = struct.unpack(orden + "I", tif[4:8])[0]
    n = struct.unpack(orden + "H", tif[ifd:ifd + 2])[0]
    et = {}
    for k in range(n):
        tag, tipo, cuenta = struct.unpack(orden + "HHI", tif[ifd + 2 + 12 * k:ifd + 10 + 12 * k])
        et[tag] = (tipo, cuenta, tif[ifd + 10 + 12 * k:ifd + 14 + 12 * k])

    def arreglo(tag):
        tipo, cuenta, v = et[tag]
        f = "H" if tipo == 3 else "I"
        if cuenta * struct.calcsize(f) <= 4:
            return list(struct.unpack(orden + f * cuenta, v[:cuenta * struct.calcsize(f)]))
        p = struct.unpack(orden + "I", v)[0]
        return list(struct.unpack(orden + f * cuenta, tif[p:p + cuenta * struct.calcsize(f)]))

    return [tif[o:o + c] for o, c in zip(arreglo(273), arreglo(279))]


def test_lzw_igual_que_pillow():
    random.seed(7)
    ancho, alto = 37, 5
    valores = [round(random.uniform(0, 400), 2) if random.random() > 0.2 else 0.0 for _ in range(ancho * alto)]
    tif = _tiff_lzw_float(ancho, alto, valores)
    crudo = b"".join(chirps.lzw_decodificar(f) for f in _franjas(tif))
    decod = struct.unpack("<" + "f" * (ancho * alto), crudo[:4 * ancho * alto])
    assert all(abs(a - b) < 1e-3 for a, b in zip(decod, valores))


def test_lzw_con_muchos_codigos():
    # Suficientes datos distintos para pasar de 9 a 12 bits y forzar códigos Clear.
    random.seed(3)
    valores = [random.uniform(0, 1000) for _ in range(64 * 64)]
    tif = _tiff_lzw_float(64, 64, valores)
    crudo = b"".join(chirps.lzw_decodificar(f) for f in _franjas(tif))
    assert len(crudo) == 4 * 64 * 64


def test_fila_columna_de_chirps():
    assert chirps.fila_col(14.81146, -89.39433) == (403, 612)
    lat, lon = chirps.centro(403, 612)
    assert abs(lat - 14.825) < 1e-9 and abs(lon - -89.375) < 1e-9


# ---------------------------------------------------------------- corrección de lluvia con CHIRPS
def _diario(p_mm: float = 3.0) -> dict:
    d, out = date(2001, 1, 1), {}
    while d.year <= 2002:
        out[d] = (p_mm, 30.0, 18.0, 0.5)
        d += timedelta(days=1)
    return out


def test_correccion_respeta_el_total_mensual_de_chirps():
    diario = _diario()
    ch = {"datos": {"filas": [[2001, 7, 31.0], [2001, 8, None], [2002, 1, 0.0]]}}
    corr, info = clima.corregir_lluvia(diario, ch)
    julio = sum(corr[d][0] for d in corr if d.year == 2001 and d.month == 7)
    assert abs(julio - 31.0) < 1e-6                     # 3 mm x 31 días -> 31 mm (factor 1/3)
    assert corr[date(2001, 8, 5)][0] == 3.0             # mes sin CHIRPS: queda POWER
    assert corr[date(2002, 1, 5)][0] == 0.0
    assert corr[date(2001, 7, 5)][1:] == (30.0, 18.0, 0.5)  # la temperatura no cambia
    assert info["meses_corregidos"] == 2


def test_sin_chirps_no_cambia_nada():
    diario = _diario()
    corr, info = clima.corregir_lluvia(diario, None)
    assert corr is diario and info["meses_corregidos"] == 0


def test_comparar_power_chirps():
    diario = _diario(2.0)  # 62 mm en julio
    ch = {"datos": {"filas": [[a, m, 50.0] for a in (2001, 2002) for m in range(1, 13)]}}
    c = clima.comparar(diario, ch, 2001, 2002)
    assert c["jul_ago"]["n"] == 4
    assert c["jul_ago"]["sesgo_mm_mes"] == 12.0
    assert c["jul_ago"]["sesgo_pct"] == 24.0


# ---------------------------------------------------------------- .env y secretos
def test_env_no_pisa_el_entorno(tmp_path, monkeypatch):
    env = tmp_path / ".env"
    env.write_text("# comentario\nPRUEBA_MILPA_A=desde_env\nPRUEBA_MILPA_B='con comillas'\n", encoding="utf-8")
    monkeypatch.setenv("PRUEBA_MILPA_A", "ya_definida")
    monkeypatch.delenv("PRUEBA_MILPA_B", raising=False)
    cache.cargar_env(env)
    assert os.environ["PRUEBA_MILPA_A"] == "ya_definida"
    assert os.environ["PRUEBA_MILPA_B"] == "con comillas"


def test_ocultar_tapa_la_clave():
    assert cache.ocultar("https://x/api/area/csv/ABC123/VIIRS", "ABC123") == "https://x/api/area/csv/***/VIIRS"
    assert cache.ocultar("sin clave", None) == "sin clave"


def test_env_no_esta_en_git():
    import subprocess

    r = subprocess.run(["git", "check-ignore", "-q", ".env"], cwd=datos.RAIZ)
    assert r.returncode == 0, ".env debe estar en .gitignore"


# ---------------------------------------------------------------- AppEEARS (SMAP) sin red
def test_procesar_csv_de_appeears(tmp_path, monkeypatch):
    monkeypatch.setattr(cache, "CACHE", tmp_path / "cache")
    pre = "SPL3SMP_E_006_"
    cols = ["ID", "Latitude", "Longitude", "Date", pre + appeears_smap.CAPAS[0], pre + appeears_smap.CAPAS[1],
            pre + appeears_smap.CAPAS[2], pre + appeears_smap.CAPAS[3]]
    filas = []
    for anio in range(2015, 2022):
        base = 0.20 if anio == 2018 else 0.30
        for dia in range(1, 31):
            for mes in (7, 8):
                filas.append(["sint", "14.5", "-89.5", f"{anio}-{mes:02d}-{dia:02d}", str(base), "0", str(base), "0"])
    filas.append(["sint", "14.5", "-89.5", "2016-07-31", "0.9", "1", "-9999", "65534"])  # mala calidad: se descarta
    csvp = tmp_path / "r.csv"
    csvp.write_text("\n".join(",".join(f) for f in [cols] + filas), encoding="utf-8")
    out = appeears_smap.procesar(csvp, "prueba")
    d = out["sint"]
    assert d["por_anio_jul_ago"][2018] == 0.2
    assert d["jul_ago_mediana"] == 0.3
    assert d["anomalia_2018_de"] is None or d["anomalia_2018_de"] < 0
    guardado = json.loads((tmp_path / "cache" / "smap" / "sint.json").read_text(encoding="utf-8"))
    assert "EARTHDATA" not in json.dumps(guardado)


def test_smap_sin_calidad_recomendada_queda_rotulado(tmp_path, monkeypatch):
    """Caso real de Camotán: la celda tiene humedad calculada pero nunca con calidad recomendada (bandera 9)."""
    monkeypatch.setattr(cache, "CACHE", tmp_path / "cache")
    pre = "SPL3SMP_E_006_"
    cols = ["ID", "Latitude", "Longitude", "Date"] + [pre + c for c in appeears_smap.CAPAS]
    filas = [["mala", "14.86", "-89.37", f"2018-07-{d:02d}", "0.25", "9", "0.26", "9"] for d in range(1, 31)]
    filas += [["mala", "14.86", "-89.37", "2018-08-01", "-9999", "7", "-9999", "7"]]  # sin intento: no cuenta
    csvp = tmp_path / "r.csv"
    csvp.write_text(chr(10).join(",".join(f) for f in [cols] + filas), encoding="utf-8")
    d = appeears_smap.procesar(csvp, "prueba")["mala"]
    assert d["jul_ago_mediana"] is None
    assert d["mediciones_sin_calidad_recomendada"] == 60
    assert "calidad recomendada" in d["motivo"] and "todo el registro" in d["motivo"]
    guardado = json.loads((tmp_path / "cache" / "smap" / "mala.json").read_text(encoding="utf-8"))
    assert guardado["datos"]["jul_ago_mediana"] is None


# ---------------------------------------------------------------- coordenadas de la caché
def test_cache_de_otra_coordenada_se_rechaza(tmp_path):
    (tmp_path / "cache" / "ndvi").mkdir(parents=True)
    (tmp_path / "cache" / "ndvi" / "x.json").write_text(json.dumps({"datos": {"lat": 14.79, "lon": -89.37, "filas": []}}),
                                                         encoding="utf-8")
    p_ok = {"lat": 14.79, "lon": -89.37}
    p_movido = {"lat": 14.81146, "lon": -89.39433}
    assert datos.cache("ndvi/x.json", base=str(tmp_path), parcela_=p_ok) is not None
    assert datos.cache("ndvi/x.json", obligatorio=False, base=str(tmp_path), parcela_=p_movido) is None
    with pytest.raises(datos.FaltaDato):
        datos.cache("ndvi/x.json", base=str(tmp_path), parcela_=p_movido)


def test_chirps_diario_reemplaza_la_lluvia_de_esos_dias():
    diario = _diario(3.0)
    ch_d = {"datos": {"filas": [["2001-07-01", 0.0], ["2001-07-02", 12.5], ["2001-07-03", None]]}}
    out, info = clima.aplicar_chirps_diario(diario, ch_d, {"fuente": "X"})
    assert out[date(2001, 7, 1)][0] == 0.0
    assert out[date(2001, 7, 2)][0] == 12.5
    assert out[date(2001, 7, 3)][0] == 3.0          # sin dato de CHIRPS: queda lo que había
    assert out[date(2001, 7, 2)][1:] == (30.0, 18.0, 0.5)
    assert info["dias_chirps_diario"] == 2 and "IMERG" in info["fuente"]


def test_lector_ligero_lee_solo_hasta_la_columna(monkeypatch):
    """leer_columnas_ligero con un TIF LZW de una fila por franja servido desde memoria."""
    from PIL import Image, TiffImagePlugin

    random.seed(11)
    ancho, alto = 2000, 6
    valores = [round(random.uniform(0, 300), 3) for _ in range(ancho * alto)]
    im = Image.new("F", (ancho, alto))
    im.putdata(valores)
    monkeypatch.setattr(TiffImagePlugin, "STRIP_SIZE", 1)  # una fila por franja, como CHIRPS
    buf = io.BytesIO()
    im.save(buf, format="TIFF", compression="tiff_lzw")
    tif = buf.getvalue()
    pedidos = []

    def rango_falso(url, a, b):
        pedidos.append(b - a + 1)
        return tif[a:b + 1]

    monkeypatch.setattr(chirps, "_rango", rango_falso)
    out = chirps.leer_columnas_ligero("memoria://x.tif", [2, 4], max_col=499)
    for fila in (2, 4):
        assert len(out[fila]) == 500
        assert all(abs(out[fila][c] - valores[fila * ancho + c]) < 1e-3 for c in range(500))
    assert sum(pedidos) < len(tif) / 2   # bajó mucho menos que el archivo completo
