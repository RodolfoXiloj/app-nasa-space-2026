"""Exporta las diapositivas docs/slides/index.html a docs/slides/milpa-resiliente.pdf (16:9, 1280 × 720 px).

Uso:
    cd web && python scripts/slides_capturas.py   # primero las capturas (necesita `npm run build`)
    cd web && python scripts/slides_pdf.py

Abre la página como archivo local (sin servidor ni red) en Chromium sin interfaz, o en Edge del sistema,
y la imprime a PDF con los fondos. Si python-pptx ya está instalado, además saca milpa-resiliente.pptx con
una imagen por diapositiva; si no está, lo dice y sigue (no se instala nada).
Sale con código 1 si el PDF pasa de 7 páginas.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parent.parent.parent
SLIDES = RAIZ / "docs" / "slides"
HTML = SLIDES / "index.html"
PDF = SLIDES / "milpa-resiliente.pdf"
PPTX = SLIDES / "milpa-resiliente.pptx"
ANCHO, ALTO = 1280, 720
TOPE = 7


def paginas_pdf(ruta: Path) -> int:
    """Cuenta los objetos /Type /Page (no /Pages) del PDF, sin dependencias."""
    return len(re.findall(rb"/Type\s*/Page(?![a-zA-Z])", ruta.read_bytes()))


def abrir_navegador(p):
    try:
        return p.chromium.launch()
    except Exception:  # sin el Chromium de Playwright: Edge del sistema
        return p.chromium.launch(channel="msedge")


def main() -> int:
    try:
        import pptx  # noqa: F401
        hay_pptx = True
    except ImportError:
        hay_pptx = False

    with sync_playwright() as p:
        navegador = abrir_navegador(p)
        try:
            pag = navegador.new_page(viewport={"width": ANCHO, "height": ALTO}, device_scale_factor=2)
            pag.goto(HTML.as_uri())
            pag.wait_for_load_state("load")
            rotas = pag.evaluate("Array.from(document.images).filter(i => !i.complete || !i.naturalWidth).map(i => i.src)")
            if rotas:
                print("NO  imágenes que no cargan: " + ", ".join(rotas))
                return 1
            pag.pdf(path=str(PDF), width=f"{ANCHO}px", height=f"{ALTO}px", print_background=True,
                    margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
            imagenes: list[bytes] = []
            if hay_pptx:
                pag.emulate_media(media="print")
                for el in pag.query_selector_all("section.slide"):
                    imagenes.append(el.screenshot())
        finally:
            navegador.close()

    n = paginas_pdf(PDF)
    print(f"{'OK ' if n <= TOPE else 'NO '} {PDF.relative_to(RAIZ).as_posix()}: {n} páginas (tope {TOPE})")
    if hay_pptx:
        from io import BytesIO

        from pptx import Presentation
        from pptx.util import Emu

        prs = Presentation()
        prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)  # 16:9
        for img in imagenes:
            hoja = prs.slides.add_slide(prs.slide_layouts[6])
            hoja.shapes.add_picture(BytesIO(img), 0, 0, prs.slide_width, prs.slide_height)
        prs.save(str(PPTX))
        print(f"OK  {PPTX.relative_to(RAIZ).as_posix()}: {len(imagenes)} diapositivas")
    else:
        print("--  python-pptx no está instalado: no se genera .pptx")
    return 0 if n <= TOPE else 1


if __name__ == "__main__":
    sys.exit(main())
