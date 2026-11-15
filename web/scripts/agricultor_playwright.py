"""Prueba con Playwright de la vista «Para el agricultor» a 360, 390 y 412 px, y sus capturas.

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
- al cambiar de idioma con el audio sonando, suena el mp3 del idioma nuevo (es -> en y en -> es).
Accesibilidad (docs/accessibility.md), a 360, 390 y 412 px en es y en: sin scroll horizontal ni texto que se
salga por la orilla; botones principales de 48 x 48 px o más; <html lang> sigue al selector y el foco se queda
en el botón de idioma y en el selector de parcela; cada botón, enlace y select tiene nombre accesible; el
orden de tabulación es el de la pantalla y cada parada tiene foco visible.
Línea de julio-agosto 2026 (web/src/agricultor/Linea2026.jsx), a 360, 390 y 412 px en es y en: una por parcela,
con el porcentaje de la mediana 1991-2025 que trae public/data/validacion.json, «observado, no es un pronóstico» /
«observed, not a forecast», texto real con el lang del idioma activo y visible para el lector de pantalla, sin
«alerta»/«alert» y en tinta gris (nada naranja); sus textos no van en el JS inicial (llega con import()).
Y un caso del kit comunitario a 390 px (web/src/kit/): los botones «Imprimir hoja», «Descargar audio» y
«Compartir por WhatsApp» existen, la hoja impresa cabe en 1 página y el enlace de WhatsApp está bien formado.
Sale con código 1 si algo falla.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import time
import urllib.parse
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
ANCHOS_A11Y = [(360, 780), (390, 844), (412, 915)]

resultados: list[tuple[bool, str, str]] = []

# Porcentaje de la mediana de julio-agosto 2026 por parcela, del mismo JSON que sirve el sitio.
_OBS = json.loads((WEB / "public" / "data" / "validacion.json").read_text(encoding="utf-8"))["observacion_2026"]
PCT_2026 = {f["id"]: f["pct_de_la_mediana"] for f in _OBS["lluvia_chirps"]}
REF_2026 = {f["id"]: f["periodo_referencia"] for f in _OBS["lluvia_chirps"]}
NOTA_2026 = {"es": "Observado, no es un pronóstico.", "en": "Observed, not a forecast."}


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
    ok_src = src.endswith(".frases.mp3") or (idioma == "en" and src.endswith(".frases.en.mp3"))
    anota(bool(suena) and toques <= TOPE_TOQUES and ok_src,
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
    suena_mp3(pag, pre, otro)
    pag.locator(f".agr-idioma[lang='{idioma}']").tap()
    pag.wait_for_function(
        "(i) => document.querySelector('#agr-audio track')?.srclang === i", arg=idioma, timeout=10000)
    suena_mp3(pag, pre, idioma)
    pag.evaluate("document.querySelector('#agr-audio').pause()")
    anota(not errores, f"{pre}: sin errores de JavaScript", "; ".join(errores[:2]))

    if capturas:
        if pid_captura != pag.input_value("#agr-parcela"):
            pag.select_option("#agr-parcela", pid_captura)
            pag.wait_for_function(
                f"document.querySelector('#agr-audio')?.getAttribute('src')?.includes('{pid_captura}.frases.')",
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


def suena_mp3(pag, pre: str, idioma: str) -> None:
    """Después de cambiar de idioma con el audio sonando, suena el mp3 de ese idioma (no se queda en pausa)."""
    fin = ".frases.en.mp3" if idioma == "en" else ".frases.mp3"
    try:
        estado = pag.wait_for_function(
            """(fin) => { const a = document.querySelector('#agr-audio');
                 if (!a || a.paused || !a.currentSrc.endsWith(fin)) return null;
                 if (window.__src !== a.currentSrc) { window.__t0 = a.currentTime; window.__src = a.currentSrc; return null }
                 return a.currentTime > window.__t0 + 0.3 ? { src: a.currentSrc.split('/').pop(), t: a.currentTime } : null }""",
            arg=fin, timeout=15000, polling=200).json_value()
        anota(True, f"{pre}: al pasar a {idioma} suena el mp3 de {idioma}", f"{estado['src']} a {estado['t']:.1f} s")
    except Exception:
        src = pag.evaluate("(() => { const a = document.querySelector('#agr-audio'); return a.currentSrc + (a.paused ? ' (en pausa)' : '') })()")
        anota(False, f"{pre}: al pasar a {idioma} suena el mp3 de {idioma}", src.split("/")[-1])


# Botones principales que deben medir 48 x 48 px o más.
PRINCIPALES = [".agr-idioma", "#agr-parcela", ".agr-escuchar-boton", ".kit-boton", ".agr-evidencia"]

# Nombre accesible aproximado: aria-label, aria-labelledby, <label> o el texto. Lo oculto con aria-hidden no cuenta.
JS_NOMBRES = """() => [...document.querySelectorAll('button, a[href], select, input, audio[controls]')]
  .filter((e) => e.getClientRects().length && !e.closest('[aria-hidden="true"]'))
  .map((e) => { const por = e.getAttribute('aria-labelledby');
    const nombre = (e.getAttribute('aria-label') || (por && por.split(' ').map((i) => (document.getElementById(i) || {}).textContent).join(' '))
      || (e.labels && e.labels[0] && e.labels[0].textContent) || e.textContent || '').trim();
    return { que: e.tagName.toLowerCase() + (e.className ? '.' + String(e.className).split(' ').pop() : ''), nombre } })"""

# Elementos que se salen por la orilla de la pantalla o que recortan su texto.
JS_SALIDOS = """(ancho) => [...document.querySelectorAll('.agr *')].filter((e) => {
    if (!e.getClientRects().length || e.closest('.kit-hoja')) return false;
    const r = e.getBoundingClientRect(); const s = getComputedStyle(e);
    return r.width > 0 && (r.left < -0.5 || r.right > ancho + 0.5 || (s.overflowX === 'hidden' && e.scrollWidth > e.clientWidth + 1)) })
  .slice(0, 4).map((e) => e.tagName.toLowerCase() + '.' + String(e.className.baseVal ?? e.className).split(' ').pop() + ' «' + (e.textContent || '').slice(0, 30) + '»')"""


JS_LINEA = r"""() => { const e = document.querySelector('.agr-linea2026'); if (!e) return null;
    const s = getComputedStyle(e), r = e.getBoundingClientRect();
    let oculto = false;
    for (let a = e; a; a = a.parentElement) if (a.getAttribute('aria-hidden') === 'true' || a.hidden) oculto = true;
    return { pid: e.dataset.linea2026, pct: Number(e.dataset.pct), lang: e.lang, texto: e.innerText.replace(/\s+/g, ' ').trim(),
             crudo: e.textContent, oculto, ancho: r.width, derecha: r.right, n: document.querySelectorAll('.agr-linea2026').length,
             colores: [s.color, s.borderLeftColor, s.backgroundColor,
                       ...[...e.querySelectorAll('*')].map((h) => getComputedStyle(h).color)] } }"""


def _naranja(color: str) -> bool:
    """True si el color (rgb/rgba) tiene tono naranja o ámbar visible."""
    m = re.findall(r"[\d.]+", color)
    if len(m) < 3 or (len(m) > 3 and float(m[3]) == 0):
        return False
    r, g, b = (float(x) / 255 for x in m[:3])
    mx, mn = max(r, g, b), min(r, g, b)
    if mx - mn < 0.15:
        return False
    if mx == r:
        tono = (60 * ((g - b) / (mx - mn))) % 360
    elif mx == g:
        tono = 60 * ((b - r) / (mx - mn) + 2)
    else:
        tono = 60 * ((r - g) / (mx - mn) + 4)
    return 15 <= tono <= 50


def comprobar_linea(pag, pre: str, idioma: str, ancho: int) -> None:
    """La línea de julio-agosto 2026 de la parcela elegida, en el idioma activo."""
    pid = pag.input_value("#agr-parcela")
    pag.wait_for_function(
        "([p, l]) => { const e = document.querySelector('.agr-linea2026'); return e && e.dataset.linea2026 === p && e.lang === l }",
        arg=[pid, idioma], timeout=15000)
    li = pag.evaluate(JS_LINEA)
    pct = PCT_2026.get(pid)
    num = f"{pct} %"
    fallas = []
    if li["n"] != 1:
        fallas.append(f"{li['n']} líneas")
    if li["pct"] != pct or num not in li["crudo"]:
        fallas.append(f"cifra {li['pct']} en vez de {pct}")
    if REF_2026.get(pid) not in li["crudo"]:
        fallas.append("sin la mediana de referencia")
    if NOTA_2026[idioma] not in li["texto"]:
        fallas.append("sin «observado, no es un pronóstico»")
    if re.search(r"alert", li["texto"], re.I):
        fallas.append("dice alerta/alert")
    if li["lang"] != idioma or li["oculto"] or not li["texto"]:
        fallas.append(f"lang {li['lang']}, oculto {li['oculto']}")
    if li["derecha"] > ancho + 0.5:
        fallas.append(f"se sale por la orilla ({li['derecha']:.0f} px)")
    naranjas = [c for c in li["colores"] if _naranja(c)]
    if naranjas:
        fallas.append(f"color naranja {naranjas}")
    anota(not fallas, f"{pre}: línea julio-agosto 2026 de {pid}", "; ".join(fallas) or li["texto"])


def caso_a11y(navegador, ancho: int, alto: int, idioma: str) -> None:
    """Ancho, objetivos táctiles, nombres accesibles, lang, foco y tabulación de la vista del agricultor."""
    otro = "en" if idioma == "es" else "es"
    pre = f"A11y {ancho} px, {idioma}"
    ctx = navegador.new_context(viewport={"width": ancho, "height": alto}, device_scale_factor=2,
                                is_mobile=True, has_touch=True)
    ctx.add_init_script(f"try {{ localStorage.setItem('milpa-locale', '{idioma}') }} catch (e) {{}}")
    pag = ctx.new_page()
    errores: list[str] = []
    pag.on("pageerror", lambda e: errores.append(str(e)))
    pag.goto(URL)
    pag.wait_for_function("document.querySelectorAll('.agr-hecho').length === 3", timeout=20000)
    pag.wait_for_selector(".agr-escuchar-boton", timeout=20000)
    pag.wait_for_selector(".kit-imprimir", timeout=20000)
    comprobar_linea(pag, pre, idioma, ancho)

    ancho_doc = pag.evaluate("document.documentElement.scrollWidth")
    salidos = pag.evaluate(JS_SALIDOS, ancho)
    anota(ancho_doc <= ancho and not salidos, f"{pre}: sin scroll horizontal ni texto cortado",
          f"ancho {ancho_doc} px" + (f"; se salen: {salidos}" if salidos else ""))

    chicos = []
    for sel in PRINCIPALES:
        cajas = [pag.locator(sel).nth(i).bounding_box() for i in range(pag.locator(sel).count())]
        if not cajas:
            chicos.append(f"{sel} no está")
        chicos += [f"{sel} {c['width']:.0f}x{c['height']:.0f}" for c in cajas if c and (c["width"] < 48 or c["height"] < 48)]
    anota(not chicos, f"{pre}: botones principales de 48 x 48 px o más", "; ".join(chicos))

    sin_nombre = [n["que"] for n in pag.evaluate(JS_NOMBRES) if not n["nombre"]]
    anota(not sin_nombre, f"{pre}: cada botón, enlace y select tiene nombre accesible", ", ".join(sin_nombre))

    # Tabulación desde el principio: idiomas, parcela, Escuchar, kit y evidencia, cada uno con foco visible.
    pag.keyboard.press("Tab")
    paradas, sin_foco = [], []
    for _ in range(12):
        info = pag.evaluate("""() => { const e = document.activeElement; if (!e || e === document.body) return null;
            const s = getComputedStyle(e);
            return { que: e.id ? '#' + e.id : '.' + String(e.className).split(' ').pop(),
                     visible: s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) >= 2 } }""")
        if not info:
            break
        paradas.append(info["que"])
        if not info["visible"]:
            sin_foco.append(info["que"])
        if info["que"] == ".agr-evidencia":
            break
        pag.keyboard.press("Tab")
    esperado = [".agr-idioma", ".agr-idioma", "#agr-parcela", ".agr-escuchar-boton",
                ".kit-imprimir", ".kit-audio", ".kit-whatsapp", ".kit-imagen", ".agr-evidencia"]
    # «Guardar para usar sin señal» solo sale si el navegador registró el service worker (kit/sinSenal.js).
    if pag.locator(".kit-guardar").count():
        esperado.insert(-1, ".kit-guardar")
    anota(paradas == esperado and not sin_foco, f"{pre}: orden de tabulación lógico y foco visible en cada parada",
          " > ".join(paradas) + (f"; sin foco visible: {sin_foco}" if sin_foco else ""))

    # Cambiar de idioma con el teclado: <html lang> cambia y el foco se queda en el botón del idioma.
    lang0 = pag.evaluate("document.documentElement.lang")
    pag.focus(f".agr-idioma[lang='{otro}']")
    pag.keyboard.press("Enter")
    pag.wait_for_function("(o) => document.documentElement.lang === o", arg=otro, timeout=5000)
    comprobar_linea(pag, pre + f" -> {otro}", otro, ancho)
    foco = pag.evaluate("document.activeElement.getAttribute('lang') + '|' + document.activeElement.getAttribute('aria-pressed')")
    nombre_otro = pag.evaluate("document.querySelector('.agr-escuchar-boton b').textContent")
    pag.focus(f".agr-idioma[lang='{idioma}']")
    pag.keyboard.press("Enter")
    pag.wait_for_function("(i) => document.documentElement.lang === i", arg=idioma, timeout=5000)
    anota(lang0 == idioma and foco == f"{otro}|true" and nombre_otro == {"es": "Escuchar", "en": "Listen"}[otro],
          f"{pre}: <html lang> sigue al selector y el foco se queda en el botón",
          f"lang {lang0} -> {otro} -> {idioma}; foco en {foco}; botón «{nombre_otro}»")

    # Cambiar de parcela: el foco se queda en el selector mientras llegan los datos nuevos.
    pids = pag.eval_on_selector_all("#agr-parcela option", "os => os.map((o) => o.value)")
    actual = pag.input_value("#agr-parcela")
    nueva = next(p for p in pids if p != actual)
    pag.focus("#agr-parcela")
    pag.select_option("#agr-parcela", nueva)
    pag.wait_for_function(
        "(p) => (document.querySelector('#agr-audio')?.getAttribute('src') || '').includes(p + '.frases.')",
        arg=nueva, timeout=15000)
    foco = pag.evaluate("document.activeElement.id")
    comprobar_linea(pag, pre, idioma, ancho)
    anota(foco == "agr-parcela", f"{pre}: al cambiar de parcela el foco se queda en el selector",
          f"{actual} -> {nueva}; foco en #{foco}")

    pag.click(".agr-escuchar-boton")
    pag.wait_for_selector(".agr-subtitulos", timeout=10000)
    pag.evaluate("document.querySelector('#agr-audio').pause()")
    anota(pag.get_attribute(".agr-subtitulos", "aria-live") == "polite",
          f"{pre}: los subtítulos se anuncian (aria-live=polite)")
    anota(not errores, f"{pre}: sin errores de JavaScript", "; ".join(errores[:2]))
    ctx.close()


def caso_kit(navegador, ancho: int = 390, alto: int = 844) -> None:
    """Kit comunitario a 390 px, en español: botones, hoja de 1 página y enlace de WhatsApp."""
    pre = f"Kit {ancho} px, es"
    ctx = navegador.new_context(viewport={"width": ancho, "height": alto}, device_scale_factor=2,
                                is_mobile=True, has_touch=True)
    ctx.add_init_script("try { localStorage.setItem('milpa-locale', 'es') } catch (e) {}")
    pag = ctx.new_page()
    errores: list[str] = []
    pag.on("pageerror", lambda e: errores.append(str(e)))
    pag.goto(URL)
    pag.wait_for_selector(".kit-imprimir", timeout=20000)
    pid = pag.input_value("#agr-parcela")

    imprimir = pag.locator(".kit-imprimir")
    audio = pag.locator(".kit-audio")
    textos = [imprimir.inner_text(), audio.inner_text(), pag.inner_text(".kit-whatsapp")]
    ancho_doc = pag.evaluate("document.documentElement.scrollWidth")
    anota(textos == ["Imprimir hoja", "Descargar audio", "Compartir por WhatsApp"] and ancho_doc <= ancho,
          f"{pre}: los 3 botones del kit existen, sin desbordar a lo ancho", f"{textos}; ancho {ancho_doc} px")
    href_audio = audio.get_attribute("href") or ""
    anota(href_audio.endswith(f"audio/{pid}.frases.mp3") and audio.get_attribute("download") is not None,
          f"{pre}: «Descargar audio» enlaza al mp3 de la parcela con download", href_audio)

    # WhatsApp: https://wa.me/?text=<resumen + location.href>, sin depender del dominio.
    wa = pag.get_attribute(".kit-whatsapp", "href") or ""
    url_wa = urllib.parse.urlsplit(wa)
    texto = urllib.parse.parse_qs(url_wa.query).get("text", [""])[0]
    pagina = pag.evaluate("location.href")
    anota(url_wa.scheme == "https" and url_wa.netloc == "wa.me" and url_wa.path == "/" and list(urllib.parse.parse_qs(url_wa.query)) == ["text"]
          and texto.strip().endswith(pagina) and "no es un aviso oficial" in texto.lower() and texto.count("\n- ") == 3,
          f"{pre}: enlace de WhatsApp bien formado (wa.me, resumen de 3 hechos y la dirección)", texto.replace("\n", " / ")[:140])

    # Imprimir: el botón pone la clase y llama a print(); la hoja impresa cabe en una sola página.
    pag.evaluate("() => { window.__impreso = 0; window.print = () => { window.__impreso++ } }")
    imprimir.tap()
    clase = pag.evaluate("document.documentElement.classList.contains('kit-imprimiendo') && window.__impreso === 1")
    pag.emulate_media(media="print")
    hoja = pag.evaluate("""(() => { const h = document.querySelector('.kit-hoja'); if (!h || getComputedStyle(h).display === 'none') return null;
        return { hechos: h.querySelectorAll('.kit-hecho').length, formas: h.querySelectorAll('.agr-senal').length,
                 rueda: h.querySelectorAll('[data-picto^="rueda"], svg').length > 0, texto: h.innerText } })()""")
    pdf = pag.pdf(format="Letter", print_background=True)
    paginas = len(re.findall(rb"/Type\s*/Page[^s]", pdf))
    # Al terminar, la impresión dispara «afterprint» y la hoja se vuelve a esconder: otro toque para A4.
    vuelve = pag.evaluate("!document.documentElement.classList.contains('kit-imprimiendo')")
    pag.emulate_media(media="screen")
    imprimir.tap()
    pag.emulate_media(media="print")
    pdf_a4 = pag.pdf(format="A4", print_background=True)
    paginas_a4 = len(re.findall(rb"/Type\s*/Page[^s]", pdf_a4))
    anota(bool(clase) and bool(hoja) and hoja["hechos"] == 3 and hoja["formas"] >= 3 and "no es un aviso oficial" in hoja["texto"].lower()
          and "Opciones para platicar" in hoja["texto"],
          f"{pre}: «Imprimir hoja» muestra solo la hoja (3 hechos con forma, opciones y aviso)",
          f"{hoja['hechos']} hechos, {hoja['formas']} formas" if hoja else "la hoja no se ve al imprimir")
    anota(paginas == 1 and paginas_a4 == 1, f"{pre}: la hoja cabe en 1 página", f"carta {paginas}, A4 {paginas_a4}")
    anota(vuelve, f"{pre}: después de imprimir, la página vuelve a la vista normal")
    pag.emulate_media(media="screen")
    anota(not errores, f"{pre}: sin errores de JavaScript", "; ".join(errores[:2]))
    ctx.close()


def linea_fuera_del_js_inicial() -> None:
    """Los textos de la línea 2026 no van en los <script> que carga index.html: llegan con import()."""
    html = (WEB / "dist" / "index.html").read_text(encoding="utf-8")
    iniciales = re.findall(r'<script[^>]+src="[^"]*?(assets/[^"]+\.js)"', html)
    dentro = [a for a in iniciales if any(n in (WEB / "dist" / a).read_text(encoding="utf-8") for n in NOTA_2026.values())]
    anota(bool(iniciales) and not dentro, "Línea 2026 fuera del JS inicial (llega con import())",
          ", ".join(dentro) or ", ".join(iniciales))


def main() -> int:
    capturas = "--capturas" in sys.argv
    linea_fuera_del_js_inicial()
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
                for ancho, alto in ANCHOS_A11Y:
                    for idioma in ("es", "en"):
                        try:
                            caso_a11y(navegador, ancho, alto, idioma)
                        except Exception as e:
                            anota(False, f"A11y {ancho} px, {idioma}: el caso no terminó", str(e).splitlines()[0])
                try:
                    caso_kit(navegador)
                except Exception as e:
                    anota(False, "Kit 390 px: el caso no terminó", str(e).splitlines()[0])
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
