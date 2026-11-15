"""Capturas reales del sitio en inglés para el video de 30 s (video/pitch/assets/ui/).

Uso (después de `npm run build` en web/):
    python video/pitch/scripts/capturas.py

Levanta `vite preview` de web/ en 127.0.0.1:4179 y guarda, a 2x:
- farmer-before.png  vista del agricultor de Olopa, primera pantalla, antes de tocar «Listen»
- farmer-listen.png  la misma pantalla después de tocar «Listen», pausada en «Soil: watch...»
- farmer-full.png    la página entera en ese mismo estado (los tres hechos)
- farmer-full-before.png  la página entera antes de tocar «Listen»
- futures-olopa.png  vista Evidence de Olopa: la sección de los futuros de NASA
- ui.json            cajas (px CSS) de los elementos que el video anima: botones, hechos, subtítulo,
                     tarjetas de rotación y cada punto de los 33 futuros, con su estado real
Sale con código 1 si algo falla.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

PITCH = Path(__file__).resolve().parent.parent
WEB = PITCH.parent.parent / "web"
SALIDA = PITCH / "assets" / "ui"
PUERTO = 4179
URL = f"http://127.0.0.1:{PUERTO}/"
CAJAS: dict = {}

CAJA_JS = """(sel) => [...document.querySelectorAll(sel)].map((e) => { const r = e.getBoundingClientRect();
  return {x: r.x + scrollX, y: r.y + scrollY, w: r.width, h: r.height, cls: e.className || ''} })"""


def esperar_servidor(seg: float = 30) -> None:
    fin = time.time() + seg
    while time.time() < fin:
        try:
            with urllib.request.urlopen(URL, timeout=2) as r:
                if r.status == 200:
                    return
        except OSError:
            time.sleep(0.3)
    raise RuntimeError("vite preview no respondió")


def abrir_navegador(p):
    try:
        return p.chromium.launch(args=["--mute-audio"])
    except Exception:
        return p.chromium.launch(channel="msedge", args=["--mute-audio"])


def contexto(navegador, ancho: int, alto: int, movil: bool):
    ctx = navegador.new_context(viewport={"width": ancho, "height": alto}, device_scale_factor=2,
                                is_mobile=movil, has_touch=movil, locale="en-US")
    ctx.add_init_script("try { localStorage.setItem('milpa-locale', 'en') } catch (e) {}")
    return ctx


def agricultor(navegador) -> None:
    ctx = contexto(navegador, 412, 915, True)
    pag = ctx.new_page()
    pag.goto(URL)
    pag.wait_for_function("document.querySelectorAll('.agr-hecho').length === 3", timeout=20000)
    pag.select_option("#agr-parcela", "olopa")
    pag.wait_for_function("document.querySelector('.agr-escuchar') !== null", timeout=15000)
    pag.wait_for_function("document.querySelectorAll('.agr-hecho').length === 3", timeout=20000)
    pag.wait_for_timeout(600)
    pag.evaluate("window.scrollTo(0, 0)")
    pag.screenshot(path=str(SALIDA / "farmer-before.png"))
    pag.screenshot(path=str(SALIDA / "farmer-full-before.png"), full_page=True)
    CAJAS["antes"] = {k: pag.evaluate(CAJA_JS, sel) for k, sel in {
        "marca": ".agr-marca", "escuchar": ".agr-escuchar-boton", "hechos": ".agr-hecho",
        "evidencia": ".agr-evidencia", "linea2026": ".agr-linea2026"}.items()}
    CAJAS["antes"]["alto"] = pag.evaluate("document.documentElement.scrollHeight")

    pag.locator(".agr-escuchar-boton").tap()
    pag.wait_for_function(
        "(() => { const a = document.querySelector('#agr-audio'); return a && a.currentTime > 3.3 })()",
        timeout=15000)
    pag.evaluate("document.querySelector('#agr-audio').pause()")
    pag.wait_for_function("document.querySelector('.agr-subtitulos')?.textContent.length > 0", timeout=10000)
    pag.wait_for_timeout(300)
    pag.evaluate("window.scrollTo(0, 0)")
    pag.screenshot(path=str(SALIDA / "farmer-listen.png"))
    pag.screenshot(path=str(SALIDA / "farmer-full.png"), full_page=True)
    CAJAS["despues"] = {k: pag.evaluate(CAJA_JS, sel) for k, sel in {
        "escuchar": ".agr-escuchar-boton", "subtitulos": ".agr-subtitulos", "hechos": ".agr-hecho",
        "evidencia": ".agr-evidencia"}.items()}
    CAJAS["despues"]["alto"] = pag.evaluate("document.documentElement.scrollHeight")
    ctx.close()


def futuros(navegador) -> None:
    ctx = contexto(navegador, 1100, 900, False)
    pag = ctx.new_page()
    pag.goto(URL + "#evidence")
    pag.wait_for_selector(".rotaciones", timeout=30000)
    pag.select_option(".controles select >> nth=0", "olopa")
    pag.wait_for_function(
        "document.querySelector('.tarjeta-acciones audio')?.getAttribute('src')?.includes('/olopa.')"
        " && document.querySelectorAll('.rotacion').length === 3", timeout=20000)
    pag.wait_for_selector(".futuros-nasa", timeout=20000)
    pag.wait_for_timeout(500)
    pag.locator(".futuros-nasa").scroll_into_view_if_needed()
    pag.wait_for_timeout(300)
    pag.locator(".futuros-nasa").screenshot(path=str(SALIDA / "futures-olopa.png"))
    base = pag.evaluate(CAJA_JS, ".futuros-nasa")[0]
    rel = lambda cs: [{**c, "x": c["x"] - base["x"], "y": c["y"] - base["y"]} for c in cs]
    CAJAS["futuros"] = {"caja": base,
                        "tarjetas": rel(pag.evaluate(CAJA_JS, ".futuro-rot")),
                        "titulos": rel(pag.evaluate(CAJA_JS, ".futuro-rot h3")),
                        "cifras": rel(pag.evaluate(CAJA_JS, ".futuro-cifra")),
                        "puntos": [rel(pag.evaluate(CAJA_JS, f".futuro-rot:nth-child({i}) .puntos i")) for i in (1, 2, 3)]}
    ctx.close()


def main() -> int:
    SALIDA.mkdir(parents=True, exist_ok=True)
    vite = subprocess.Popen([
        "node", "node_modules/vite/bin/vite.js", "preview", "--host", "127.0.0.1", "--port", str(PUERTO), "--strictPort",
    ], cwd=WEB, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        esperar_servidor()
        with sync_playwright() as p:
            navegador = abrir_navegador(p)
            try:
                agricultor(navegador)
                futuros(navegador)
            finally:
                navegador.close()
        (SALIDA / "ui.json").write_text(json.dumps(CAJAS, indent=1), encoding="utf-8")
    except Exception as e:
        print(f"NO  {str(e).splitlines()[0]}")
        return 1
    finally:
        vite.terminate()
    for f in sorted(SALIDA.glob("*.png")):
        print("OK ", f.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
