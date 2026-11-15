"""Capturas en español de la vista Evidence, para docs/capturas/ (escritorio 1366 × 768 y teléfono 390 × 844).

Uso (después de `npm run build`):
    cd web && python scripts/evidence_capturas.py

Levanta `vite preview` en 127.0.0.1:4177, abre `#evidence` en Chromium sin interfaz (o Edge del sistema) con el
idioma en español y guarda 13 pantallas por tamaño. Cada captura es la pantalla visible, no la página entera:
    01 primera pantalla de Evidence, con la observación preliminar de julio-agosto 2026
    02 mapa con las 5 parcelas          03 «Lo que ve el satélite» y «Clima de la zona»
    04-08 tarjeta para el agricultor, una por parcela, con su reproductor de audio
    09 comparación de las 3 rotaciones (Jocotán)
    10 pestaña Validación               11 detalle de la observación de julio-agosto 2026
    12 glosario y fuentes
    13 sin internet: el mapa pasa solo a la capa guardada (se corta toda petición que no sea local)
Las capturas de la vista del agricultor las hace `agricultor_playwright.py --capturas` y las de las
diapositivas `slides_capturas.py`. Sale con código 1 si algo falla.
"""
from __future__ import annotations

import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

WEB = Path(__file__).resolve().parent.parent
SALIDA = WEB.parent / "docs" / "capturas"
PUERTO = 4177
URL = f"http://127.0.0.1:{PUERTO}/"
TAMANOS = [("escritorio", 1366, 768, False), ("telefono", 390, 844, True)]
PARCELAS = ["jocotan", "camotan", "olopa", "san_juan_ermita", "zacapa"]


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
    except Exception:  # sin el Chromium de Playwright: Edge del sistema
        return p.chromium.launch(channel="msedge", args=["--mute-audio"])


def contexto(navegador, ancho: int, alto: int, movil: bool):
    ctx = navegador.new_context(viewport={"width": ancho, "height": alto}, device_scale_factor=1,
                                is_mobile=movil, has_touch=movil, locale="es-GT")
    ctx.add_init_script("try { localStorage.setItem('milpa-locale', 'es') } catch (e) {}")
    return ctx


def arriba_de(pag, selector: str) -> None:
    """Deja el elemento en el borde superior de la pantalla."""
    pag.wait_for_selector(selector, timeout=20000)
    pag.evaluate("(s) => { const e = document.querySelector(s); "
                 "window.scrollTo(0, e.getBoundingClientRect().top + window.scrollY - 8) }", selector)
    pag.wait_for_timeout(500)


def elegir_parcela(pag, pid: str) -> None:
    pag.select_option(".controles select >> nth=0", pid)
    pag.wait_for_function(
        f"document.querySelector('.tarjeta-acciones audio')?.getAttribute('src')?.includes('/{pid}.')"
        " && document.querySelectorAll('.rotacion').length === 3", timeout=20000)
    pag.wait_for_timeout(400)


def capturar(navegador, prefijo: str, ancho: int, alto: int, movil: bool) -> list[Path]:
    hechas: list[Path] = []

    def foto(pag, nombre: str) -> None:
        ruta = SALIDA / f"{prefijo}-{nombre}.png"
        pag.screenshot(path=str(ruta))
        hechas.append(ruta)

    ctx = contexto(navegador, ancho, alto, movil)
    pag = ctx.new_page()
    errores: list[str] = []
    pag.on("pageerror", lambda e: errores.append(str(e)))
    pag.goto(URL + "#evidence")
    pag.wait_for_selector(".rotaciones", timeout=30000)
    pag.wait_for_selector(".banda-obs", timeout=20000)
    pag.wait_for_timeout(1500)                       # teselas del mapa

    pag.evaluate("window.scrollTo(0, 0)")
    foto(pag, "01-primera-pantalla-observacion-2026")
    arriba_de(pag, ".mapa")
    pag.wait_for_timeout(1200)
    foto(pag, "02-mapa-5-parcelas")
    arriba_de(pag, "section.panel")
    foto(pag, "03-satelite-y-clima")
    for i, pid in enumerate(PARCELAS, 4):
        elegir_parcela(pag, pid)
        arriba_de(pag, ".tarjeta-agricultor")
        foto(pag, f"{i:02d}-tarjeta-{pid}")
    elegir_parcela(pag, "jocotan")
    arriba_de(pag, ".rotaciones")
    foto(pag, "09-rotaciones-jocotan")

    pag.locator("nav.pestanas button").nth(1).click()
    pag.wait_for_selector("#donde-falla", timeout=20000)
    arriba_de(pag, "nav.pestanas")
    foto(pag, "10-validacion")
    arriba_de(pag, "#observacion-2026")
    foto(pag, "11-observacion-2026-detalle")

    pag.locator("nav.pestanas button").nth(2).click()
    pag.wait_for_selector(".glosario", timeout=20000)
    arriba_de(pag, "nav.pestanas")
    foto(pag, "12-glosario-y-fuentes")
    if errores:
        raise RuntimeError("errores de JavaScript: " + "; ".join(errores[:2]))
    ctx.close()

    # 13) Sin internet: solo responde el servidor local; el mapa pasa solo a la capa guardada.
    ctx = contexto(navegador, ancho, alto, movil)
    ctx.route("**/*", lambda ruta: ruta.continue_() if ruta.request.url.startswith(URL) else ruta.abort())
    pag = ctx.new_page()
    pag.goto(URL + "#evidence")
    pag.wait_for_selector(".rotaciones", timeout=30000)
    pag.wait_for_selector(".aviso-sin-red", timeout=30000)
    pag.wait_for_function("[...document.querySelectorAll('img.leaflet-tile')].some((i) => i.src.includes('/capas/')"
                          " && i.complete && i.naturalWidth > 0)", timeout=30000)
    arriba_de(pag, ".mapa")
    pag.wait_for_timeout(800)
    foto(pag, "13-sin-internet-mapa-capa-guardada")
    ctx.close()
    return hechas


def main() -> int:
    SALIDA.mkdir(parents=True, exist_ok=True)
    vite = subprocess.Popen([
        "node", "node_modules/vite/bin/vite.js", "preview", "--host", "127.0.0.1", "--port", str(PUERTO), "--strictPort",
    ], cwd=WEB, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    hechas: list[Path] = []
    try:
        esperar_servidor()
        with sync_playwright() as p:
            navegador = abrir_navegador(p)
            try:
                for prefijo, ancho, alto, movil in TAMANOS:
                    hechas += capturar(navegador, prefijo, ancho, alto, movil)
            finally:
                navegador.close()
    except Exception as e:
        print(f"NO  {str(e).splitlines()[0]}")
        return 1
    finally:
        vite.terminate()
        try:
            vite.wait(timeout=10)
        except subprocess.TimeoutExpired:
            vite.kill()
    for r in hechas:
        print(f"OK  {r.relative_to(WEB.parent).as_posix()}")
    print(f"{len(hechas)} capturas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
