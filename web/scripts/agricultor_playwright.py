"""Prueba con Playwright de la vista «Para el agricultor» a 390 y 412 px, y sus capturas.

Uso (después de `npm run build`):
    cd web && python scripts/agricultor_playwright.py              # solo las comprobaciones
    cd web && python scripts/agricultor_playwright.py --capturas   # además, docs/capturas/agricultor-*.png

Levanta `vite preview` en 127.0.0.1:4176 y abre Chromium sin interfaz, con el sonido apagado
(--mute-audio: el audio corre igual, pero la laptop no suena). Por cada ancho:
- la primera pantalla tiene los 3 hechos en orden, sin desbordar a lo ancho;
- el botón «Escuchar / Listen» está a la vista sin desplazarse, y antes de tocarlo no se pidió ni el mp3 ni
  los subtítulos (preload="none");
- un toque (tope: 2) y el audio corto de la parcela suena;
- carga la <track> del idioma activo (.frases.es.vtt o .frases.en.vtt, con sus frases) y no la del otro;
  los subtítulos se ven debajo del botón;
- al cambiar de idioma con el audio abierto, se carga la pista del otro idioma.
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
CAPTURAS = WEB.parent / "docs" / "capturas"
PUERTO = 4176
URL = f"http://127.0.0.1:{PUERTO}/"
TOPE_TOQUES = 2
# (ancho, alto, idioma, parcela de la captura): los mismos de las capturas de docs/capturas/
CASOS = [(390, 844, "es", "jocotan"), (412, 915, "en", "olopa")]

resultados: list[tuple[bool, str, str]] = []


def anota(ok: bool, que: str, detalle: str = "") -> None:
    resultados.append((ok, que, detalle))
    print(f"{'OK ' if ok else 'NO '} {que}{' · ' + detalle if detalle else ''}")


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


def caso(navegador, ancho: int, alto: int, idioma: str, pid_captura: str, capturas: bool) -> None:
    otro = "en" if idioma == "es" else "es"
    pre = f"{ancho} px, {idioma}"
    ctx = navegador.new_context(viewport={"width": ancho, "height": alto}, device_scale_factor=2,
                                is_mobile=True, has_touch=True)
    ctx.add_init_script(f"try {{ localStorage.setItem('milpa-locale', '{idioma}') }} catch (e) {{}}")
    pag = ctx.new_page()
    pedidos: list[str] = []
    pag.on("request", lambda r: pedidos.append(r.url))
    errores: list[str] = []
    pag.on("pageerror", lambda e: errores.append(str(e)))
    pag.goto(URL)
    pag.wait_for_function("document.querySelectorAll('.agr-hecho').length === 3", timeout=20000)

    orden = pag.eval_on_selector_all(".agr-hecho", "els => els.map(e => e.dataset.hecho).join(',')")
    ancho_doc = pag.evaluate("document.documentElement.scrollWidth")
    anota(orden == "suelo,quema,canicula" and ancho_doc <= ancho,
          f"{pre}: 3 hechos en orden, sin desbordar a lo ancho", f"{orden}; ancho {ancho_doc} px")

    boton = pag.locator(".agr-escuchar-boton")
    caja = boton.bounding_box() if boton.count() == 1 else None
    texto = boton.inner_text().split("\n")[0] if caja else ""
    esperado = {"es": "Escuchar", "en": "Listen"}[idioma]
    anota(bool(caja) and caja["y"] + caja["height"] <= alto and texto == esperado,
          f"{pre}: botón «{esperado}» en la primera pantalla, sin desplazarse",
          f"abajo en {round(caja['y'] + caja['height']) if caja else '?'} de {alto} px" if caja else "no está")
    antes = [u for u in pedidos if ".frases." in u]
    anota(not antes, f"{pre}: antes de tocar no se pide audio ni subtítulos (preload=none)", ", ".join(antes))

    # Desde la primera pantalla hasta oír el audio: se cuentan los toques.
    toques = 0
    boton.tap()
    toques += 1
    suena = pag.wait_for_function(
        "(() => { const a = document.querySelector('#agr-audio'); return a && !a.paused && a.currentTime > 0.3 })()",
        timeout=15000)
    t_audio = pag.evaluate("document.querySelector('#agr-audio').currentTime")
    src = pag.evaluate("document.querySelector('#agr-audio').currentSrc")
    anota(bool(suena) and toques <= TOPE_TOQUES and src.endswith(".frases.mp3"),
          f"{pre}: el audio suena en {toques} toque(s) (tope {TOPE_TOQUES})", f"{src.split('/')[-1]} a {t_audio:.1f} s")

    pista = pag.wait_for_function(
        """(idioma) => { const el = document.querySelector('#agr-audio track');
             if (!el || el.readyState !== 2 || !el.track.cues || !el.track.cues.length) return null;
             return { lang: el.srclang, src: el.src.split('/').pop(), cues: el.track.cues.length, modo: el.track.mode,
                      textos: Array.from(el.track.cues, (c) => c.text) } }""",
        arg=idioma, timeout=10000).json_value()
    anota(pista["lang"] == idioma and pista["src"].endswith(f".frases.{idioma}.vtt"),
          f"{pre}: carga la <track> del idioma activo", f"{pista['src']}, {pista['cues']} frases, modo {pista['modo']}")
    pag.wait_for_function("document.querySelector('.agr-subtitulos')?.textContent.length > 0", timeout=10000)
    sub = pag.inner_text(".agr-subtitulos")
    anota(sub in pista["textos"], f"{pre}: subtítulos visibles debajo del botón", f"«{sub}»")
    otros = [u for u in pedidos if u.endswith(f".frases.{otro}.vtt")]
    anota(not otros, f"{pre}: no se pide la pista del otro idioma", ", ".join(otros))

    # Cambiar de idioma con el audio abierto: se carga la pista del otro idioma y sigue sonando.
    pag.locator(f".agr-idioma[lang='{otro}']").tap()
    nueva = pag.wait_for_function(
        """(otro) => { const el = document.querySelector('#agr-audio track');
             return el && el.srclang === otro && el.readyState === 2 && el.track.cues.length ? el.src.split('/').pop() : null }""",
        arg=otro, timeout=10000).json_value()
    anota(nueva.endswith(f".frases.{otro}.vtt"), f"{pre}: al cambiar a {otro} carga su pista", nueva)
    pag.locator(f".agr-idioma[lang='{idioma}']").tap()
    pag.wait_for_function(
        "(i) => document.querySelector('#agr-audio track')?.srclang === i", arg=idioma, timeout=10000)
    pag.evaluate("document.querySelector('#agr-audio').pause()")
    anota(not errores, f"{pre}: sin errores de JavaScript", "; ".join(errores[:2]))

    if capturas:
        if pid_captura != pag.input_value("#agr-parcela"):
            pag.select_option("#agr-parcela", pid_captura)
            pag.wait_for_function(
                f"document.querySelector('#agr-audio')?.getAttribute('src')?.includes('{pid_captura}.frases.mp3')",
                timeout=15000)
        # Captura con el audio abierto en la segunda frase (el suelo), pausado, y su subtítulo a la vista.
        pag.locator(".agr-escuchar-boton").tap()
        pag.wait_for_function(
            "(() => { const a = document.querySelector('#agr-audio'); return a.currentTime > 3.2 })()", timeout=15000)
        pag.evaluate("document.querySelector('#agr-audio').pause()")
        pag.wait_for_function("document.querySelector('.agr-subtitulos')?.textContent.length > 0")
        ruta = CAPTURAS / f"agricultor-{ancho}-{idioma}-{pid_captura}.png"
        pag.screenshot(path=str(ruta), full_page=True)
        print(f"    captura: {ruta.relative_to(WEB.parent)}")
    ctx.close()


def main() -> int:
    capturas = "--capturas" in sys.argv
    vite = subprocess.Popen([
        "node", "node_modules/vite/bin/vite.js", "preview", "--host", "127.0.0.1", "--port", str(PUERTO), "--strictPort",
    ], cwd=WEB, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        esperar_servidor()
        with sync_playwright() as p:
            navegador = abrir_navegador(p)
            try:
                for ancho, alto, idioma, pid in CASOS:
                    try:
                        caso(navegador, ancho, alto, idioma, pid, capturas)
                    except Exception as e:  # una espera vencida cuenta como falla del caso
                        anota(False, f"{ancho} px, {idioma}: el caso no terminó", str(e).splitlines()[0])
            finally:
                navegador.close()
    finally:
        vite.terminate()
        try:
            vite.wait(timeout=10)
        except subprocess.TimeoutExpired:
            vite.kill()
    fallos = sum(1 for ok, _, _ in resultados if not ok)
    print(f"\n{len(resultados) - fallos} de {len(resultados)} comprobaciones pasan")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
