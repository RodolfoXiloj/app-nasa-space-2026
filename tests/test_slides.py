"""Diapositivas de la demo (docs/slides/): 7 páginas o menos y cifras iguales a los JSON de la web.

El PDF lo genera web/scripts/slides_pdf.py; aquí solo se lee, sin navegador ni dependencias nuevas.
"""
from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
SLIDES = RAIZ / "docs" / "slides"
HTML = SLIDES / "index.html"
PDF = SLIDES / "milpa-resiliente.pdf"
DATOS = RAIZ / "web" / "public" / "data"
TOPE = 7


def paginas_pdf(ruta: Path) -> int:
    return len(re.findall(rb"/Type\s*/Page(?![a-zA-Z])", ruta.read_bytes()))


class Lector(HTMLParser):
    """Junta las diapositivas, las imágenes, los enlaces externos y el texto de cada data-dato."""

    def __init__(self) -> None:
        super().__init__()
        self.diapositivas = 0
        self.imagenes: list[str] = []
        self.externos: list[str] = []
        self.datos: list[tuple[str, str]] = []
        self._abiertos: list[list] = []  # [ruta, texto, profundidad]
        self._prof = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "section" and "slide" in (a.get("class") or "").split():
            self.diapositivas += 1
        if tag == "img":
            self.imagenes.append(a.get("src") or "")
        for k in ("src", "href"):
            if re.match(r"^(https?:)?//", a.get(k) or ""):
                self.externos.append(a[k])
        if tag in ("img", "br", "meta", "link", "path", "circle", "rect"):
            return
        self._prof += 1
        if "data-dato" in a:
            self._abiertos.append([a["data-dato"], "", self._prof])

    def handle_endtag(self, tag):
        if tag in ("img", "br", "meta", "link", "path", "circle", "rect"):
            return
        if self._abiertos and self._abiertos[-1][2] == self._prof:
            ruta, texto, _ = self._abiertos.pop()
            self.datos.append((ruta, texto.strip()))
        self._prof -= 1

    def handle_data(self, data):
        for abierto in self._abiertos:
            abierto[1] += data


@pytest.fixture(scope="module")
def lector() -> Lector:
    lec = Lector()
    lec.feed(HTML.read_text(encoding="utf-8"))
    return lec


def resolver(ref: str):
    """`archivo.json:a.b[id=x].c.0` → valor dentro de web/public/data/archivo.json."""
    archivo, ruta = ref.split(":", 1)
    valor = json.loads((DATOS / archivo).read_text(encoding="utf-8"))
    for parte in re.findall(r"[^.\[\]]+(?:\[id=[^\]]+\])?", ruta):
        m = re.fullmatch(r"([^\[]+)\[id=([^\]]+)\]", parte)
        if m:
            valor = next(x for x in valor[m.group(1)] if x.get("id") == m.group(2))
        elif isinstance(valor, list):
            valor = valor[int(parte)]
        else:
            valor = valor[parte]
    return valor


def test_pdf_tiene_7_paginas_o_menos():
    assert PDF.exists(), "falta docs/slides/milpa-resiliente.pdf: corra web/scripts/slides_pdf.py"
    n = paginas_pdf(PDF)
    assert 1 <= n <= TOPE, f"el PDF tiene {n} páginas (tope {TOPE})"


def test_html_tiene_7_diapositivas_o_menos(lector):
    assert 1 <= lector.diapositivas <= TOPE


def test_sin_recursos_externos_y_capturas_presentes(lector):
    assert not lector.externos, lector.externos
    assert lector.imagenes
    for src in lector.imagenes:
        assert "nasa" not in src.lower() or "capturas" in src, src  # sin logos
        assert (SLIDES / src).resolve().is_file(), src


def test_cada_cifra_coincide_con_los_json(lector):
    assert len(lector.datos) >= 20
    for ref, texto in lector.datos:
        esperado = resolver(ref)
        assert isinstance(esperado, (int, float)), (ref, esperado)
        assert float(texto.replace(",", "")) == pytest.approx(float(esperado)), (ref, texto, esperado)


def test_afirmaciones_sin_data_dato():
    """Lo que dicen las diapositivas sin una cifra marcada."""
    parcelas = ["jocotan", "camotan", "olopa", "san_juan_ermita", "zacapa"]
    jsons = {p: json.loads((DATOS / f"{p}.json").read_text(encoding="utf-8")) for p in parcelas}
    val = json.loads((DATOS / "validacion.json").read_text(encoding="utf-8"))
    # «No option wins at any of the 5 plots today.»
    assert all(j["farmer"]["opciones"]["destaca"] is None for j in jsons.values())
    # Olopa: las tres opciones empatadas, sin orden.
    assert len(jsons["olopa"]["farmer"]["opciones"]["empatadas"]) == 3
    # Grises: Camotán (SMAP) y Zacapa (POWER vs CHIRPS).
    assert jsons["camotan"]["farmer"]["opciones"]["estado"] == "gris"
    assert jsons["zacapa"]["farmer"]["opciones"]["estado"] == "gris"
    # «2018 back-test: high risk at 5 of 5 plots» y «2–3 false alarms and 1 miss».
    s18 = [p["sequia_2018"] for p in val["parcelas"]]
    assert all(s["senales_2018"]["motor"] for s in s18) and len(s18) == 5
    assert {s["falsas_alarmas"] for s in s18} == {2, 3} and {s["fallos"] for s in s18} == {1}
    # «20–26 % of normal rain at our 5 plots»: mínimo y máximo.
    pct = [x["pct_de_la_mediana"] for x in val["observacion_2026"]["lluvia_chirps"]]
    assert (min(pct), max(pct)) == (20, 26)
    # «under 30 seconds per plot»
    assert all(j["farmer"]["audio"]["es"]["duracion_s"] < 30 for j in jsons.values())
    # «Bare in Feb–Apr at San Juan Ermita»
    assert jsons["san_juan_ermita"]["farmer"]["hechos"][0]["meses"] == [2, 3, 4]
    # Chiquimula es el departamento de las parcelas citadas en la diapositiva 2.
    assert {jsons[p]["parcela"]["departamento"] for p in ("jocotan", "san_juan_ermita")} == {"Chiquimula"}
