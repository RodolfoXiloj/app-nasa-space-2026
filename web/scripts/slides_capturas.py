"""Capturas en inglés a 390 px de la vista del agricultor, para las diapositivas (docs/slides/).

Uso (después de `npm run build`):
    cd web && python scripts/slides_capturas.py

Levanta `vite preview` en 127.0.0.1:4177, abre Chromium sin interfaz (o Edge del sistema) a 390 × 844,
con el idioma en inglés, y guarda en docs/capturas/en/:
- farmer-390-jocotan.png       primera pantalla de Jocotán: semáforo con ícono y palabra
- farmer-390-jocotan-audio.png botón «Listen» con el audio pausado y su subtítulo en inglés
- farmer-390-olopa-tie.png     bloque de opciones de Olopa: empate de las tres, sin orden
- farmer-390-camotan-grey.png  bloque de opciones de Camotán: gris porque falta el dato de SMAP
Sale con código 1 si algo falla.
"""
from __future__ import annotations

import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

WEB = Path(__file__).resolve().parent.parent
SALIDA = WEB.parent / "docs" / "capturas" / "en"
PUERTO = 4177
URL = f"http://127.0.0.1:{PUERTO}/"
ANCHO, ALTO = 390, 844


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


def elegir_parcela(pag, pid: str) -> None:
    if pag.input_value("#agr-parcela") != pid:
        pag.select_option("#agr-parcela", pid)
    pag.wait_for_function(
        f"document.querySelector('#agr-audio')?.getAttribute('src')?.includes('{pid}.frases.')"
        f" || document.querySelector('.agr-escuchar') !== null",
        timeout=15000)
    pag.wait_for_function("document.querySelectorAll('.agr-hecho').length === 3", timeout=20000)
    pag.wait_for_selector(".agr-opciones", timeout=20000)
    pag.wait_for_timeout(400)


def capturar(navegador) -> list[Path]:
    ctx = navegador.new_context(viewport={"width": ANCHO, "height": ALTO}, device_scale_factor=2,
                                is_mobile=True, has_touch=True, locale="en-US")
    ctx.add_init_script("try { localStorage.setItem('milpa-locale', 'en') } catch (e) {}")
    pag = ctx.new_page()
    errores: list[str] = []
    pag.on("pageerror", lambda e: errores.append(str(e)))
    pag.goto(URL)
    pag.wait_for_function("document.querySelectorAll('.agr-hecho').length === 3", timeout=20000)
    hechas: list[Path] = []

    # 1) Jocotán, primera pantalla: semáforo con ícono y palabra.
    elegir_parcela(pag, "jocotan")
    ruta = SALIDA / "farmer-390-jocotan.png"
    pag.evaluate("window.scrollTo(0, 0)")
    pag.screenshot(path=str(ruta))
    hechas.append(ruta)

    # 2) Jocotán, audio: un toque en «Listen», pausa en la segunda frase con su subtítulo en inglés.
    pag.locator(".agr-escuchar-boton").tap()
    pag.wait_for_function(
        "(() => { const a = document.querySelector('#agr-audio'); return a && a.currentTime > 3.2 })()",
        timeout=15000)
    pag.evaluate("document.querySelector('#agr-audio').pause()")
    pag.wait_for_function("document.querySelector('.agr-subtitulos')?.textContent.length > 0", timeout=10000)
    ruta = SALIDA / "farmer-390-jocotan-audio.png"
    pag.locator(".agr-escuchar").screenshot(path=str(ruta))
    hechas.append(ruta)

    # 3) Olopa: las tres opciones empatan, sin orden.
    elegir_parcela(pag, "olopa")
    estado = pag.get_attribute(".agr-opciones", "data-opciones")
    if estado != "empate":
        raise RuntimeError(f"Olopa: se esperaba empate y vino {estado}")
    ruta = SALIDA / "farmer-390-olopa-tie.png"
    pag.locator(".agr-opciones").screenshot(path=str(ruta))
    hechas.append(ruta)

    # 4) Camotán: opciones en gris porque falta el dato de SMAP.
    elegir_parcela(pag, "camotan")
    estado = pag.get_attribute(".agr-opciones", "data-opciones")
    if estado != "gris":
        raise RuntimeError(f"Camotán: se esperaba gris y vino {estado}")
    ruta = SALIDA / "farmer-390-camotan-grey.png"
    pag.locator(".agr-opciones").screenshot(path=str(ruta))
    hechas.append(ruta)

    ancho_doc = pag.evaluate("document.documentElement.scrollWidth")
    if ancho_doc > ANCHO:
        raise RuntimeError(f"la página desborda a lo ancho: {ancho_doc} px")
    if errores:
        raise RuntimeError("errores de JavaScript: " + "; ".join(errores[:2]))
    ctx.close()
    return hechas


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
                hechas = capturar(navegador)
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
