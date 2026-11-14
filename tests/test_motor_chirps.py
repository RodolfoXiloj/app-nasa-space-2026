"""Motor con CHIRPS, clase de poca cobertura y regla 5.1 de la validación (datos sintéticos)."""
import json
import shutil
from pathlib import Path

import pytest

from motor import contrato, deteccion
from motor.recomendar import recomendar


@pytest.fixture()
def base_chirps(base_sintetica, tmp_path) -> str:
    """Copia de la base sintética con CHIRPS = mitad de la lluvia de POWER cada mes."""
    base = tmp_path / "data"
    shutil.copytree(base_sintetica, base)
    power = json.loads((base / "cache" / "power" / "sint_diario.json").read_text(encoding="utf-8"))
    totales: dict[tuple[int, int], float] = {}
    for k, p, *_ in power["datos"]["filas"]:
        clave = (int(k[:4]), int(k[4:6]))
        totales[clave] = totales.get(clave, 0.0) + p
    filas = [[a, m, round(v / 2, 2)] for (a, m), v in sorted(totales.items())]
    (base / "cache" / "chirps").mkdir(parents=True, exist_ok=True)
    (base / "cache" / "chirps" / "sint.json").write_text(json.dumps(
        {"procedencia": {"url": "sintetico", "fecha_descarga": "2026-11-13T00:00:00Z"},
         "datos": {"filas": filas, "lat": 14.5, "lon": -89.5}}), encoding="utf-8")
    return str(base)


def test_motor_usa_la_lluvia_de_chirps(base_sintetica, base_chirps):
    sin = recomendar("sint", base=base_sintetica)
    con = recomendar("sint", base=base_chirps)
    assert "CHIRPS" in con["clima"]["fuente_lluvia"]
    assert "chirps" in con["clima"]["fuente_ids"]
    # la lluvia normal es la mitad y el déficit sube
    assert sum(con["clima"]["lluvia_mensual_normal_mm"]) < 0.55 * sum(sin["clima"]["lluvia_mensual_normal_mm"])
    assert con["rotaciones"][0]["deficit"]["mediana_pct"] >= sin["rotaciones"][0]["deficit"]["mediana_pct"]
    ja = con["clima"]["power_vs_chirps"]["jul_ago"]
    assert ja["sesgo_pct"] == 100.0  # POWER da el doble que CHIRPS
    # con +100 % de diferencia, el criterio de lluvia falla y la confianza es baja
    crit = {c["criterio"]: c for c in con["rotaciones"][0]["confianza"]["criterios"]}
    assert crit["Lluvia POWER contra CHIRPS en julio-agosto"]["cumple"] is False
    assert contrato.errores_esquema(con) == []
    assert contrato.errores_textos(con) == []
    assert any("CHIRPS" in v for v in con["rotaciones"][0]["vacios"])


def test_regla_5_1_baja_la_confianza(base_chirps):
    ruta = Path(base_chirps) / "cache" / "validacion" / "resumen.json"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps({"datos": {"regla_5_1": {"parcelas_con_senal_2018": 1, "minimo": 3, "se_activa": True}}}),
                    encoding="utf-8")
    res = recomendar("sint", base=base_chirps)
    for r in res["rotaciones"]:
        assert r["confianza"]["nivel"] == "baja"
        assert "2018" in r["confianza"]["motivo"]


def test_clase_poca_cobertura():
    filas = []
    valores = {1: 0.40, 2: 0.42, 3: 0.30, 4: 0.33, 5: 0.5, 6: 0.7, 7: 0.8, 8: 0.7, 9: 0.75, 10: 0.8, 11: 0.7, 12: 0.5}
    for anio in range(2021, 2026):
        for mes in range(1, 13):
            filas.append([f"{anio}-{mes:02d}-01", valores[mes], 0])
            filas.append([f"{anio}-{mes:02d}-17", valores[mes], 0])
    det = deteccion.detectar({"datos": {"filas": filas}}, None)
    assert det["meses_desnudos"] == [3, 4]
    assert det["meses_poca_cobertura"] == [1, 2]
    assert det["umbral_poca_cobertura_ndvi"] == 0.45
