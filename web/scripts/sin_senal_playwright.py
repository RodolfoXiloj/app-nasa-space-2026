"""Prueba de uso sin señal (service worker, dist/sw.js) con Playwright y Edge.

Uso (después de `npm run build`):
    cd web && python scripts/sin_senal_playwright.py

Levanta `vite preview` en 127.0.0.1:4178 y, en español y en inglés:
1. abre la vista del agricultor con el servidor arriba y espera al service worker;
2. comprueba que todavía no hay audio guardado (la primera pantalla no descarga audio, docs/peso.md);
3. toca «Guardar para usar sin señal» del kit y espera el «Guardado: … kB»;
4. APAGA el servidor y recarga: la vista debe abrir con los tres hechos, Escuchar debe sonar con subtítulos y
   el hecho que nombra la voz debe quedar marcado;
5. abre Evidence sin servidor: como no se guardó, debe decir qué pasó (role="alert"), sin pantalla en blanco.
Sale con código 1 si algo falla. No deja procesos en el puerto.
"""
from __future__ import annotations

import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

WEB = Path(__file__).resolve().parent.parent
PUERTO = 4178
URL = f"http://127.0.0.1:{PUERTO}/"
resultados: list[tuple[bool, str]] = []


def anota(ok: bool, texto: str) -> None:
    resultados.append((ok, texto))
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
    apagar(p)
    raise SystemExit("vite preview no respondió")


def apagar(p: subprocess.Popen) -> None:
    if sys.platform == "win32":
        subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"], capture_output=True)
    else:
        p.kill()
    p.wait(timeout=10)
    for _ in range(40):
        try:
            urllib.request.urlopen(URL, timeout=1)
            time.sleep(0.25)
        except Exception:
            return


def prueba(navegador, idioma: str) -> None:
    pre = f"Sin señal, {idioma}"
    srv = servidor()
    try:
        ctx = navegador.new_context(viewport={"width": 390, "height": 844})
        pg = ctx.new_page()
        errores: list[str] = []
        pg.on("pageerror", lambda e: errores.append(str(e)))
        pg.goto(URL)
        pg.evaluate(f"() => localStorage.setItem('milpa-locale', '{idioma}')")
        pg.reload()
        pg.wait_for_selector(".agr-lista-hechos [data-hecho]")
        controlada = pg.evaluate("""async () => {
            const reg = await navigator.serviceWorker.ready;
            for (let i = 0; i < 40 && !navigator.serviceWorker.controller; i++) await new Promise((r) => setTimeout(r, 100));
            return !!reg.active && !!navigator.serviceWorker.controller }""")
        anota(controlada, f"{pre}: el service worker controla la página")
        audio_antes = pg.evaluate("""async () => { const out = [];
            for (const k of await caches.keys()) for (const r of await (await caches.open(k)).keys()) if (r.url.includes('/audio/')) out.push(r.url);
            return out }""")
        anota(not audio_antes, f"{pre}: antes de tocar «Guardar» no hay audio guardado", )
        pg.locator(".kit-guardar").click()
        pg.wait_for_function("() => /Guardado|Saved/.test(document.querySelector('.kit-sin-senal').textContent)", timeout=60000)
        texto = pg.locator(".kit-sin-senal p").inner_text()
        anota(True, f"{pre}: {texto}")
    finally:
        apagar(srv)
    try:
        urllib.request.urlopen(URL, timeout=2)
        anota(False, f"{pre}: el servidor sigue respondiendo")
    except Exception:
        anota(True, f"{pre}: servidor apagado")
    pg.reload()
    pg.wait_for_selector(".agr-lista-hechos [data-hecho]", timeout=15000)
    n = pg.locator(".agr-lista-hechos [data-hecho]").count()
    anota(n == 3, f"{pre}: la vista abre sin servidor con los tres hechos ({n})")
    pg.wait_for_selector(".agr-escuchar-boton", timeout=10000)
    pg.locator(".agr-escuchar-boton").click()
    pg.wait_for_timeout(5500)
    estado = pg.evaluate("""() => { const a = document.querySelector('#agr-audio');
        return { t: a.currentTime, error: a.error ? a.error.code : null,
                 sub: (document.querySelector('.agr-subtitulos') || {}).textContent || '',
                 marcado: [...document.querySelectorAll('.agr-lista-hechos [data-hablando]')].map((e) => e.getAttribute('data-hecho')) } }""")
    anota(estado["t"] > 3 and estado["error"] is None, f"{pre}: Escuchar suena sin servidor · {estado['t']:.1f} s, error={estado['error']}")
    anota(bool(estado["sub"].strip()), f"{pre}: subtítulos sin servidor · «{estado['sub'].strip()[:50]}»")
    anota(estado["marcado"] == ["suelo"], f"{pre}: la voz marca el hecho que lee · {estado['marcado']}")
    pg.evaluate("() => { const a = document.querySelector('#agr-audio'); a.pause() }")
    pg.locator(".agr-evidencia").click()
    pg.wait_for_timeout(2500)
    alerta = pg.locator("[role=alert]").count()
    anota(alerta > 0, f"{pre}: Evidence sin guardar ni servidor dice qué pasó (role=alert)")
    anota(not errores, f"{pre}: sin errores de JavaScript · {errores[:2]}")
    ctx.close()


def main() -> int:
    with sync_playwright() as p:
        navegador = p.chromium.launch(channel="msedge")
        try:
            for idioma in ("es", "en"):
                prueba(navegador, idioma)
        finally:
            navegador.close()
    ok = sum(1 for r, _ in resultados if r)
    print(f"\n{ok} de {len(resultados)} comprobaciones pasan")
    return 0 if ok == len(resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
