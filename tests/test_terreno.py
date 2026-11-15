"""El relieve de la vista 3D (pipeline/clientes/terreno.py): las teselas recodificadas dicen la misma altura que las
originales de la caché, y un error de ±1 en un canal al leerlas mueve la altura 4 m, no cientos."""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

from pipeline.clientes import terreno

RAIZ = Path(__file__).resolve().parent.parent
WEB = RAIZ / "web" / "public" / "relieve3d"
CACHE = RAIZ / "data" / "cache" / "terreno"


def _pares():
    for web in sorted(WEB.rglob("*.png")):
        yield web, CACHE / web.relative_to(WEB)


def test_hay_teselas_y_cada_una_tiene_su_original():
    pares = list(_pares())
    assert len(pares) == 23
    assert all(original.exists() for _, original in pares)


def test_la_altura_recodificada_es_la_original():
    for web, original in _pares():
        z_m = terreno.alturas(original.read_bytes())
        px = Image.open(web).convert("RGB").load()
        for j in range(0, 256, 7):
            for i in range(0, 256, 7):
                h = min(max(z_m[j][i], 0), terreno.MAXIMO * terreno.PASO_M)
                assert abs(terreno.decodificar(px[i, j]) - h) <= terreno.PASO_M / 2 + 1e-9, (web, i, j)


def test_los_tres_canales_van_parejos():
    # Por eso un ±1 en cualquier canal es un error de 4 m: ningún canal carga más que otro.
    for web, _ in _pares():
        b = Image.open(web).convert("RGB").tobytes()
        assert all(max(b[k:k + 3]) - min(b[k:k + 3]) <= 1 for k in range(0, len(b), 3)), web


def test_maplibre_usa_la_misma_codificacion():
    info = json.loads((WEB / "relieve3d.json").read_text(encoding="utf-8"))
    m = info["codificacion"]["maplibre"]
    assert m == {"encoding": "custom", "redFactor": 4.0, "greenFactor": 4.0, "blueFactor": 4.0, "baseShift": 0}
    js = (RAIZ / "web/src/components/mapa/Relieve3D.jsx").read_text(encoding="utf-8")
    assert "encoding: 'custom', redFactor: 4, greenFactor: 4, blueFactor: 4, baseShift: 0" in js
    assert "relieve3d/{z}/{x}/{y}.png" in js and "terrarium" not in js
