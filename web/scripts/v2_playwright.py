"""Prueba de las piezas de la versión interactiva (v2) en Evidence, con Playwright y Edge.

Uso (después de `npm run build`):
    cd web && python scripts/v2_playwright.py

Levanta `vite preview` en 127.0.0.1:4179 y, a 390 px en español y a 1280 px en inglés, usa cada pieza como lo
haría una persona y comprueba lo que se ve:
- huellas: el interruptor dibuja las 6 en el mapa y en la lista; «De la parcela al satélite» avanza y se detiene;
- comparador: los dos pares (época seca y lluvias; agosto 2025 y 2026) piden sus teselas guardadas, la división
  se mueve con las flechas y se cierra;
- relieve: la capa sombreada pide sus teselas; la vista 3D (solo a 1280 px) dibuja su lienzo y se cierra;
- gráficas: la canícula cambia de reparto, la nube de modelos cambia de opción, la curva de agua cambia de año,
  la biblioteca cambia de plantilla, y julio-agosto 2026 dice la cifra del JSON;
- sin scroll horizontal con todo abierto y sin errores de JavaScript.
Sale con código 1 si algo falla. No deja procesos en el puerto.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

WEB = Path(__file__).resolve().parent.parent
PUERTO = 4179
URL = f"http://127.0.0.1:{PUERTO}/"
resultados: list[tuple[bool, str]] = []


def anota(ok: bool, texto: str) -> None:
    resultados.append((bool(ok), texto))
    print(("OK  " if ok else "NO  ") + texto)


def servidor() -> subprocess.Popen:
    npx = "npx.cmd" if sys.platform == "win32" else "npx"
    p = subprocess.Popen([npx, "vite", "preview", "--port", str(PUERTO), "--strictPort", "--host", "127.0.0.1"], cwd=WEB,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(80):
        try:
            urllib.request.urlopen(URL, timeout=2)
            return p
        except Exception:
            time.sleep(0.25)
    raise SystemExit("vite preview no respondió")


def apagar(p: subprocess.Popen) -> None:
    if sys.platform == "win32":
        subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"], capture_output=True)
    else:
        p.kill()


def resumen(pg, sel: str) -> str:
    return pg.locator(sel).first.inner_text().strip()


def prueba(nav, ancho: int, idioma: str) -> None:
    pre = f"v2 {ancho} px, {idioma}"
    ctx = nav.new_context(viewport={"width": ancho, "height": 900})
    pg = ctx.new_page()
    errores: list[str] = []
    pedidas: list[str] = []
    pg.on("pageerror", lambda e: errores.append(str(e)))
    pg.on("request", lambda r: pedidas.append(r.url))
    pg.goto(URL)
    pg.evaluate(f"() => localStorage.setItem('milpa-locale', '{idioma}')")
    pg.goto(URL + "#evidence")
    pg.reload()
    pg.wait_for_selector(".leaflet-container")
    pg.wait_for_selector(".canicula-svg", timeout=15000)
    datos = json.loads((WEB / "public/data/explorar/jocotan.json").read_text(encoding="utf-8"))

    # Huellas
    pg.locator(".mapa-check input").check()
    pg.wait_for_timeout(400)
    en_mapa = pg.locator(".leaflet-huellas-pane path").count()
    en_lista = pg.locator(".huellas-lista li").count()
    anota(en_mapa == 6 and en_lista == 6, f"{pre}: huellas en el mapa y en la lista · {en_mapa} y {en_lista}")
    pg.locator(".mapa-botones button").first.click()
    pg.wait_for_timeout(2600)
    activa = pg.locator(".huella.activa").count()
    pg.locator(".mapa-botones button").first.click()
    pg.wait_for_timeout(300)
    anota(activa == 1 and pg.locator(".huella.activa").count() == 0, f"{pre}: «De la parcela al satélite» avanza y se detiene")
    pg.locator(".mapa-check input").uncheck()

    # Comparador
    botones = pg.locator(".mapa-botones button[aria-pressed]")
    textos = botones.all_inner_texts()
    i_est = next(i for i, x in enumerate(textos) if "rainy" in x or "lluvias" in x)
    botones.nth(i_est).click()
    pg.wait_for_timeout(1500)
    division = pg.locator(".cmp-division")
    izq0 = division.get_attribute("style")
    pg.locator("#cmp-pos").focus()
    for _ in range(10):
        pg.keyboard.press("ArrowLeft")
    izq1 = division.get_attribute("style")
    anota(division.count() == 1 and izq0 != izq1, f"{pre}: la división se mueve con las flechas · {izq0} → {izq1}")
    anota(any("/capas/ndvi_seca/" in u for u in pedidas) and any("/capas/ndvi_lluvia/" in u for u in pedidas),
          f"{pre}: época seca y lluvias piden sus teselas guardadas")
    textos = botones.all_inner_texts()
    i_ago = next(i for i, x in enumerate(textos) if "2025" in x)
    botones.nth(i_ago).click()
    pg.wait_for_timeout(1500)
    anota(any("/capas/ndvi_ago_2025/" in u for u in pedidas) and any("/capas/ndvi_ago_2026/" in u for u in pedidas),
          f"{pre}: agosto 2025 y 2026 piden sus teselas guardadas")
    anota(pg.locator(".mapa-rango .nota").count() >= 2, f"{pre}: el par de agosto lleva su nota de cautela")
    pg.locator(".mapa-rango .enlace").click()
    pg.wait_for_timeout(300)
    anota(pg.locator(".cmp-division").count() == 0, f"{pre}: el comparador se cierra")

    # Relieve en 2D
    pg.locator(".leaflet-control-layers").hover()
    pg.wait_for_timeout(300)
    etiqueta = "Relieve (SRTM, sombreado)" if idioma == "es" else "Relief (SRTM, shaded)"
    pg.get_by_label(etiqueta).check()
    pg.wait_for_timeout(1500)
    anota(any("/capas/relieve/" in u for u in pedidas), f"{pre}: la capa de relieve pide sus teselas guardadas")
    pg.get_by_label(etiqueta).uncheck()
    pg.mouse.move(2, 2)

    # Vista 3D (solo en escritorio: WebGL por software es lento en un teléfono emulado)
    if ancho >= 1000:
        if pg.locator(".boton-3d").count():
            pg.locator(".boton-3d").click()
            pg.wait_for_selector(".relieve3d canvas", timeout=40000)
            pg.wait_for_timeout(3000)
            anota(pg.locator(".relieve3d canvas").count() == 1 and any("/relieve3d/" in u for u in pedidas),
                  f"{pre}: la vista 3D dibuja su lienzo y pide el relieve guardado")
            anota(bool(resumen(pg, ".relieve3d .resumen-grafica")), f"{pre}: la vista 3D tiene su texto · «{resumen(pg, '.relieve3d .resumen-grafica')[:60]}»")
            pg.locator(".boton-3d").click()
            pg.wait_for_timeout(500)
            anota(pg.locator(".relieve3d").count() == 0, f"{pre}: la vista 3D se cierra")
        else:
            anota(False, f"{pre}: no aparece el botón de la vista 3D")

    # Canícula
    antes = resumen(pg, "#canicula-dias-titulo ~ .resumen-grafica")
    pg.locator(".explorar-panel .selector-chips button").nth(1).click()
    despues = resumen(pg, "#canicula-dias-titulo ~ .resumen-grafica")
    anota(antes != despues and "ERA5" in despues, f"{pre}: la canícula cambia de reparto · «{despues[:70]}»")
    largos = sum(1 for x in datos["canicula"]["rnl"] if x["racha_dias"] > datos["canicula"]["umbral_racha_dias"])
    anota(despues.startswith(str(largos)), f"{pre}: el conteo con ERA5 es el del JSON ({largos})")

    # Julio y agosto
    total = f"{datos['lluvia_jul_ago']['total_2026_mm']}"
    anota(total in resumen(pg, "#lluvia-jul-ago-titulo ~ .resumen-grafica"), f"{pre}: julio-agosto 2026 dice {total} mm, como el JSON")

    # Curva de agua
    agua = pg.locator("#agua-ciclo-titulo").locator("xpath=..")
    antes = agua.locator(".resumen-grafica").inner_text()
    agua.locator(".curva-agua .selector-chips button").nth(1).click()
    despues = agua.locator(".resumen-grafica").inner_text()
    anota(antes != despues, f"{pre}: la curva de agua cambia de año · «{despues[:60]}»")

    # Biblioteca
    bib = pg.locator("#biblioteca-titulo").locator("xpath=..")
    antes = bib.locator(".biblioteca-ficha h3").inner_text()
    bib.locator(".selector-chips").first.locator("button").nth(2).click()
    despues = bib.locator(".biblioteca-ficha h3").inner_text()
    anota(antes != despues, f"{pre}: la biblioteca cambia de plantilla · «{despues[:50]}»")

    # Nube de modelos
    nube = pg.locator(".nube-modelos")
    antes = nube.locator(".resumen-grafica").inner_text()
    nube.locator(".selector-chips button").nth(1).click()
    despues = nube.locator(".resumen-grafica").inner_text()
    anota(antes != despues, f"{pre}: la nube de modelos cambia de opción · «{despues[:60]}»")

    pg.evaluate("() => document.querySelectorAll('.app details').forEach((d) => { d.open = true })")
    pg.wait_for_timeout(300)
    sw = pg.evaluate("() => document.documentElement.scrollWidth")
    anota(sw <= ancho + 1, f"{pre}: sin scroll horizontal con todo abierto · {sw} px")
    anota(not errores, f"{pre}: sin errores de JavaScript · {errores[:2]}")
    ctx.close()


def main() -> int:
    srv = servidor()
    try:
        with sync_playwright() as p:
            nav = p.chromium.launch(channel="msedge")
            try:
                prueba(nav, 390, "es")
                prueba(nav, 1280, "en")
            finally:
                nav.close()
    finally:
        apagar(srv)
    ok = sum(1 for r, _ in resultados if r)
    print(f"\n{ok} de {len(resultados)} comprobaciones pasan")
    return 0 if ok == len(resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
