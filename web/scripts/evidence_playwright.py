"""Prueba de accesibilidad con Playwright de la vista Evidence a 360, 390 y 412 px, en español y en inglés.

Uso (después de `npm run build`):
    cd web && python scripts/evidence_playwright.py

Hermano de `agricultor_playwright.py` (usa sus ayudas). Levanta `vite preview` en 127.0.0.1:4177, abre
`#evidence` y recorre sus tres pestañas (Parcela, Validación, Glosario) con todos los <details> abiertos.
Por cada ancho e idioma comprueba (docs/accessibility.md, «Evidence view»):
- sin scroll horizontal: nada se sale por la orilla; las tablas anchas tienen su propio scroll dentro de un
  contenedor con role="region", aria-label y tabindex=0;
- cada botón, enlace, select y resumen plegable tiene nombre accesible;
- botones, selects, resúmenes y controles del mapa de 48 x 48 px o más (los enlaces dentro de una frase quedan
  fuera, como permite WCAG 2.5.8);
- cada gráfica tiene una alternativa en texto (role="img" con aria-label en el idioma activo) y el mapa una
  lista de parcelas en texto;
- los encabezados no se saltan niveles y hay un solo h1;
- foco visible (contorno de 2 px o más) en las primeras paradas de tabulación;
- con prefers-reduced-motion el mapa no anima el zoom ni el fundido;
- en inglés no queda texto en español en las tres pestañas (ni en aria-label), salvo citas rotuladas: un
  «…» en español o un título con su traducción entre corchetes; ningún elemento lang="es" fuera de esas citas;
- el pie lleva la línea visible de uso de IA, la tarjeta impresa también, y index.html su <meta>;
- el mp3 de la tarjeta está en el idioma de la interfaz (audio.en en inglés, audio.es en español).
Sale con código 1 si algo falla.
"""
from __future__ import annotations

import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from agricultor_playwright import ANCHOS_A11Y, abrir_navegador, anota, resultados  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

WEB = Path(__file__).resolve().parent.parent
PUERTO = 4177
URL = f"http://127.0.0.1:{PUERTO}/"
PESTANAS = ["parcela", "validacion", "glosario"]

JS_ABRIR_DETALLES = "() => document.querySelectorAll('.app details').forEach((d) => { d.open = true })"

# Lo que se sale por la orilla. Dentro de una tabla con scroll propio o del mapa no cuenta: ahí el ancho lo
# recorta su contenedor.
JS_SALIDOS = """(ancho) => [...document.querySelectorAll('body *')].filter((e) => {
    if (!e.getClientRects().length || e.closest('.sr-solo')) return false;
    const caja = e.parentElement && e.parentElement.closest('.tabla-scroll, .leaflet-container');
    if (caja) return false;
    const r = e.getBoundingClientRect();
    return r.width > 0 && (r.left < -0.5 || r.right > ancho + 0.5) })
  .slice(0, 4).map((e) => e.tagName.toLowerCase() + '.' + String(e.className.baseVal ?? e.className).split(' ').pop()
    + ' «' + (e.textContent || '').trim().slice(0, 30) + '»')"""

# Tablas más anchas que su contenedor: deben estar en una región con nombre y enfocable.
JS_TABLAS = """() => [...document.querySelectorAll('.app table')].filter((t) => t.getClientRects().length).map((t) => {
    const c = t.closest('.tabla-scroll');
    const ancha = t.scrollWidth > (c || t.parentElement).clientWidth + 1;
    const ok = !!c && c.getAttribute('role') === 'region' && (c.getAttribute('aria-label') || '').trim() !== ''
      && c.getAttribute('tabindex') === '0';
    return { ancha, ok, que: (t.querySelector('th') || {}).textContent || 'tabla' } })"""

# Nombre accesible aproximado: aria-label, aria-labelledby, <label>, title o el texto.
JS_NOMBRES = """() => [...document.querySelectorAll('button, a[href], select, input, summary, [role="button"]')]
  .filter((e) => e.getClientRects().length && !e.closest('[aria-hidden="true"]'))
  .map((e) => { const por = e.getAttribute('aria-labelledby');
    const nombre = (e.getAttribute('aria-label') || (por && por.split(' ').map((i) => (document.getElementById(i) || {}).textContent).join(' '))
      || (e.labels && e.labels[0] && e.labels[0].textContent) || e.textContent || e.getAttribute('title') || '').trim();
    return { que: e.tagName.toLowerCase() + (e.className ? '.' + String(e.className).split(' ').pop() : ''), nombre } })"""

# Controles que deben medir 48 x 48 px. Los enlaces dentro de una frase no cuentan (WCAG 2.5.8, excepción «en línea»).
JS_CHICOS = """() => [...document.querySelectorAll('.app button, .app select, .app summary, .leaflet-control a, .fuentes small a')]
  .filter((e) => e.getClientRects().length && !e.closest('.leaflet-control-attribution'))
  .map((e) => { const r = e.getBoundingClientRect();
    return { que: e.tagName.toLowerCase() + ' «' + (e.getAttribute('aria-label') || e.textContent || '').trim().slice(0, 25) + '»',
             w: Math.round(r.width), h: Math.round(r.height) } })
  .filter((c) => c.w < 48 || c.h < 48).slice(0, 5)"""

JS_GRAFICAS = """() => [...document.querySelectorAll('.recharts-wrapper')].map((g) => {
    const alt = g.closest('[role="img"]'); return alt ? (alt.getAttribute('aria-label') || '').trim() : '' })"""

JS_ENCABEZADOS = """() => [...document.querySelectorAll('h1, h2, h3, h4, h5, h6')].filter((h) => h.getClientRects().length)
  .map((h) => Number(h.tagName[1]))"""

JS_FOCO = """() => { const e = document.activeElement; if (!e || e === document.body) return null;
    const s = getComputedStyle(e);
    return { que: e.tagName.toLowerCase() + (e.className ? '.' + String(e.className).split(' ').pop() : ''),
             visible: s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) >= 2 } }"""


# Texto en español que queda en la vista en inglés. Se cuentan palabras que solo usa el español; dos o más en un
# mismo texto lo delatan. Antes se quitan las citas rotuladas («…» y «título [traducción]»), los nombres propios
# y las rutas o claves de archivo (camotan.json meta.datos_de_ejemplo).
# Un elemento con lang="es" solo vale si es una cita (.cita) o el botón «Español» del selector de idioma.
JS_ESPANOL = r"""() => {
  const PAL = new Set(['de', 'la', 'el', 'que', 'los', 'las', 'con', 'para', 'por', 'del', 'una', 'sin', 'más',
    'según', 'también', 'está', 'como', 'pero', 'cuando', 'hasta', 'entre', 'sobre', 'años', 'meses', 'suelo',
    'lluvia', 'parcela', 'hace', 'hoy', 'muy', 'se', 'su', 'sus', 'lo', 'datos', 'fuera', 'humedad', 'cultivo'])
  const PROPIOS = [/La Estrella de Panamá/g, /de Sousa/g]
  const limpia = (t) => PROPIOS.reduce((a, re) => a.replace(re, ''), t)
    .replace(/«[^»]*»/g, '').replace(/[^.:;\[\]]*\[[^\]]*\]/g, '').replace(/\S*[_/]\S*/g, '')
  const espanol = (t) => (limpia(t).toLowerCase().match(/[a-záéíóúñü]+/g) || []).filter((w) => PAL.has(w)).length >= 2
  const permitido = (e) => { const l = e.closest('[lang]'); return l && l.getAttribute('lang') === 'es'
    && (l.classList.contains('cita') || l.textContent.trim() === 'Español') }
  const visible = (e) => e.getClientRects().length > 0 || e.closest('.sr-solo')
  const malos = []
  const w = document.createTreeWalker(document.querySelector('.app'), NodeFilter.SHOW_TEXT)
  let n
  while ((n = w.nextNode())) {
    const e = n.parentElement
    if (!e || /^(SCRIPT|STYLE)$/.test(e.tagName) || !visible(e) || permitido(e)) continue
    if (e.closest('a[href]') && /^https?:/.test(n.textContent.trim())) continue
    if (espanol(n.textContent)) malos.push('texto «' + n.textContent.trim().slice(0, 50) + '»')
  }
  document.querySelectorAll('.app [aria-label]').forEach((e) => {
    if (espanol(e.getAttribute('aria-label'))) malos.push('aria-label «' + e.getAttribute('aria-label').slice(0, 50) + '»')
  })
  document.querySelectorAll('.app [lang="es"]').forEach((e) => {
    if (visible(e) && !permitido(e)) malos.push('lang=es «' + e.textContent.trim().slice(0, 50) + '»')
  })
  return [...new Set(malos)]
}"""


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


def saltos(niveles: list[int]) -> list[str]:
    malos = [f"h{a} → h{b}" for a, b in zip(niveles, niveles[1:]) if b > a + 1]
    if niveles.count(1) != 1:
        malos.append(f"{niveles.count(1)} h1")
    return malos


def abrir_pestana(pag, i: int) -> None:
    if i:
        pag.locator("nav.pestanas button").nth(i).click()
    selector = [".rotaciones", "#donde-falla", ".glosario"][i]
    pag.wait_for_selector(selector, timeout=20000)
    pag.evaluate(JS_ABRIR_DETALLES)
    pag.wait_for_timeout(250)


def caso(navegador, ancho: int, alto: int, idioma: str) -> None:
    pre = f"Evidence {ancho} px, {idioma}"
    ctx = navegador.new_context(viewport={"width": ancho, "height": alto}, device_scale_factor=2,
                                is_mobile=True, has_touch=True)
    ctx.add_init_script(f"try {{ localStorage.setItem('milpa-locale', '{idioma}') }} catch (e) {{}}")
    pag = ctx.new_page()
    errores: list[str] = []
    pag.on("pageerror", lambda e: errores.append(str(e)))
    pag.goto(URL + "#evidence")
    pag.wait_for_selector(".rotaciones", timeout=30000)

    # Foco visible en las primeras paradas de la pestaña Parcela (volver, pestañas, mapa, idioma, menús…).
    sin_foco, paradas = [], 0
    for _ in range(14):
        pag.keyboard.press("Tab")
        info = pag.evaluate(JS_FOCO)
        if not info:
            continue
        paradas += 1
        if not info["visible"]:
            sin_foco.append(info["que"])
    anota(paradas >= 10 and not sin_foco, f"{pre}: foco visible en las primeras {paradas} paradas de tabulación",
          f"sin foco visible: {sin_foco}" if sin_foco else "")

    lista_mapa = pag.locator(".mapa-texto li").count()
    anota(lista_mapa > 0, f"{pre}: el mapa tiene su lista de parcelas en texto", f"{lista_mapa} parcelas")

    for i, nombre in enumerate(PESTANAS):
        abrir_pestana(pag, i)
        p = f"{pre}, {nombre}"
        ancho_doc = pag.evaluate("document.documentElement.scrollWidth")
        salidos = pag.evaluate(JS_SALIDOS, ancho)
        tablas = pag.evaluate(JS_TABLAS)
        malas = [t["que"] for t in tablas if t["ancha"] and not t["ok"]]
        anota(ancho_doc <= ancho and not salidos and not malas, f"{p}: sin scroll horizontal",
              f"ancho {ancho_doc} px; {sum(t['ancha'] for t in tablas)} tablas con scroll propio"
              + (f"; se salen: {salidos}" if salidos else "") + (f"; tablas sin región: {malas}" if malas else ""))

        sin_nombre = [n["que"] for n in pag.evaluate(JS_NOMBRES) if not n["nombre"]]
        anota(not sin_nombre, f"{p}: cada botón, enlace, select y resumen tiene nombre accesible", ", ".join(sin_nombre))

        chicos = pag.evaluate(JS_CHICOS)
        anota(not chicos, f"{p}: botones, menús, resúmenes y controles del mapa de 48 x 48 px o más",
              "; ".join(f"{c['que']} {c['w']}x{c['h']}" for c in chicos))

        graficas = pag.evaluate(JS_GRAFICAS)
        anota(all(graficas), f"{p}: cada gráfica tiene alternativa en texto",
              f"{len(graficas)} gráficas" + (f"; sin texto: {graficas.count('')}" if not all(graficas) else ""))

        malos = saltos(pag.evaluate(JS_ENCABEZADOS))
        anota(not malos, f"{p}: encabezados en orden, un solo h1", ", ".join(malos))

        if idioma == "en":
            restos = pag.evaluate(JS_ESPANOL)
            anota(not restos, f"{p}: sin texto en español fuera de citas rotuladas",
                  f"{len(restos)}: " + "; ".join(restos[:4]) if restos else "")

    # Línea de IA visible en el pie y en la tarjeta impresa; nada de «Prototipo local de referencia».
    pag.locator("nav.pestanas button").nth(0).click()
    abrir_pestana(pag, 0)
    pie = pag.locator(".pie-ia")
    marca = "AI" if idioma == "en" else "IA"
    anota(pie.count() == 1 and pie.is_visible() and marca in pie.inner_text(),
          f"{pre}: el pie dice qué se hizo con {marca} (código, textos, pictogramas y voz)")
    pag.emulate_media(media="print")
    ia_hoja = pag.locator(".tarjeta .ia-tarjeta")
    anota(ia_hoja.count() == 1 and ia_hoja.is_visible(), f"{pre}: la tarjeta impresa lleva la línea de {marca}")
    pag.emulate_media(media="screen")
    anota("Prototipo local" not in pag.inner_text("body"), f"{pre}: sin «Prototipo local de referencia»")

    # El mp3 de la tarjeta va en el idioma de la interfaz: audio/{parcela}.en.mp3 en inglés y audio/{parcela}.mp3
    # en español, con su lang y su declaración de IA en ese idioma; el archivo se sirve.
    aud = pag.locator(".tarjeta-agricultor audio")
    src = (aud.first.get_attribute("src") or "") if aud.count() == 1 else ""
    lang_aud = aud.first.get_attribute("lang") if aud.count() == 1 else None
    if idioma == "en":
        ok_src = src.endswith(".en.mp3") and ".frases" not in src
    else:
        ok_src = src.endswith(".mp3") and not src.endswith(".en.mp3") and ".frases" not in src
    servido = bool(src) and pag.request.get(urllib.parse.urljoin(URL, src)).ok
    nota = pag.locator(".tarjeta-agricultor .nota-ia").inner_text() if aud.count() == 1 else ""
    voz_ok = ("en-US" in nota and "voice" in nota) if idioma == "en" else ("es-GT" in nota and "Voz" in nota)
    anota(ok_src and lang_aud == idioma and servido and voz_ok,
          f"{pre}: la tarjeta reproduce el mp3 en {'inglés' if idioma == 'en' else 'español'}",
          f"src={src} lang={lang_aud} servido={servido}; {nota[:70]}")

    anota(not errores, f"{pre}: sin errores de JavaScript", "; ".join(errores[:2]))
    ctx.close()


def caso_movimiento(navegador) -> None:
    """Con prefers-reduced-motion el mapa salta sin animar el zoom ni el fundido de las teselas."""
    ctx = navegador.new_context(viewport={"width": 390, "height": 844}, reduced_motion="reduce")
    pag = ctx.new_page()
    pag.goto(URL + "#evidence")
    pag.wait_for_selector(".leaflet-container", timeout=30000)
    clases = pag.evaluate("document.querySelector('.leaflet-container').className")
    anota("leaflet-zoom-anim" not in clases and "leaflet-fade-anim" not in clases,
          "Evidence 390 px: con movimiento reducido el mapa no anima zoom ni fundido")
    meta = pag.evaluate("(document.querySelector('meta[name=\"ai-disclosure\"]') || {}).content || ''")
    anota("AI" in meta, "index.html: <meta name=\"ai-disclosure\"> declara el uso de IA")
    ctx.close()


def main() -> int:
    vite = subprocess.Popen([
        "node", "node_modules/vite/bin/vite.js", "preview", "--host", "127.0.0.1", "--port", str(PUERTO), "--strictPort",
    ], cwd=WEB, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        esperar_servidor()
        with sync_playwright() as p:
            navegador = abrir_navegador(p)
            try:
                for ancho, alto in ANCHOS_A11Y:
                    for idioma in ("es", "en"):
                        try:
                            caso(navegador, ancho, alto, idioma)
                        except Exception as e:  # una espera vencida cuenta como falla del caso
                            anota(False, f"Evidence {ancho} px, {idioma}: el caso no terminó", str(e).splitlines()[0])
                try:
                    caso_movimiento(navegador)
                except Exception as e:
                    anota(False, "Evidence: el caso de movimiento reducido no terminó", str(e).splitlines()[0])
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
