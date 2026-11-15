"""Frases cortas de la vista «Para el agricultor» y de su audio por frases (paso 4 del plan).

Salen del bloque `farmer` ya calculado (estados de los 3 hechos y regla de empate) y de los nombres
cortos de las rotaciones (data/rotaciones.yaml). Cada frase va en español y en inglés.

Regla «nada solo en audio»: el mp3 corto lee solo `texto_audio(frases)`, es decir, el español de estas
mismas frases, que están en el JSON como texto visible. Las cifras son las de los hechos (validador de
números de motor/redaccion.py); los números de estructura van con letra («dos opciones»).
Sin la palabra «alerta»: el cierre dice que no es un aviso oficial.
"""
from __future__ import annotations

import re

NUM_ES = {2: "dos", 3: "tres"}
NUM_EN = {2: "two", 3: "three"}
# El audio dura de 20 a 75 s: frases completas que se entienden solas (qué pasó, cuándo y cada cuánto).
NOMBRE_HECHO = {"suelo": ("Suelo", "Soil"), "quema": ("Quema", "Burning"),
                "canicula": ("Canícula", "Midsummer drought")}
# Por qué la confianza es baja, dicho corto (criterios de motor/confianza.py).
RAZON_CONFIANZA = {
    "Humedad del suelo SMAP": ("falta la humedad del suelo de SMAP", "SMAP soil moisture is missing"),
    "Lluvia POWER contra CHIRPS en julio-agosto": ("dos fuentes de lluvia no coinciden", "two rain sources disagree"),
    "Calidad del píxel MODIS": ("hay pocas imágenes buenas del satélite", "there are few good satellite images"),
    "Prueba de la sequía de 2018": ("la prueba de la sequía de 2018 no dio señal suficiente",
                                    "the 2018 drought test did not show enough signal"),
}
RAZON_GENERICA = ("la confianza es baja", "confidence is low")
CIERRE = ("No es un aviso oficial: platíquelo con su técnico.",
          "This is not an official notice: talk it over with your extension worker.")


def _lista(items: list[str], conj: str) -> str:
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + f" {conj} " + items[-1]


def _min(s: str) -> str:
    return s[:1].lower() + s[1:]


def _plural(n: int, uno: str, varios: str) -> str:
    return uno if n == 1 else varios


def _frase(fid: str, hecho: str | None, es: str, en: str) -> dict:
    return {"id": fid, "hecho": hecho, "es": es, "en": en, "caa": None, "inicio_s": None, "fin_s": None}


def _palabras(umbrales: dict, estado: str) -> tuple[str, str]:
    e = umbrales["estados"][estado]
    return _min(e["es"]), _min(e["en"])


MESES_ES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre",
            "noviembre", "diciembre")
MESES_EN = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
            "November", "December")


def _meses(ms: list[int]) -> tuple[str, str]:
    return _lista([MESES_ES[m - 1] for m in ms], "y"), _lista([MESES_EN[m - 1] for m in ms], "and")


def _periodo(p: str | None) -> tuple[str, str] | None:
    m = re.match(r"(\d{4})\D+(\d{4})", p or "")
    return (m.group(1), m.group(2)) if m else None


# Cada frase dice qué pasó, cuándo y cada cuánto, con palabras de todos los días (el equipo, 15 nov 2026: «decirle
# solo "suelo: se repite", ¿qué le estamos diciendo?»). El estado del semáforo queda en la tarjeta, con su forma.
def _suelo(h: dict, umbrales: dict) -> tuple[str, str]:
    nes, nen = NOMBRE_HECHO["suelo"]
    pes, pen = _palabras(umbrales, h["estado"])
    if h["estado"] == "gris":
        return f"{nes}: {pes}.", f"{nen}: {pen}."
    per = _periodo(h.get("periodo"))
    cola_es = f". Lo vio el satélite de {per[0]} a {per[1]}." if per else ". Lo vio el satélite."
    cola_en = f". The satellite saw it from {per[0]} to {per[1]}." if per else ". The satellite saw it."
    desnudos, poca = list(h.get("meses") or []), list(h.get("meses_poca_cobertura") or [])
    if h["estado"] == "verde" or (not desnudos and not poca):
        return "Su tierra estuvo cubierta de plantas todo el año" + cola_es, "Your land stayed covered with plants all year" + cola_en
    if not desnudos:
        mes, men = _meses(poca)
        return (f"En {mes}, su tierra suele quedar con pocas plantas que la cubran" + cola_es,
                f"In {men}, your land usually has little plant cover" + cola_en)
    mes, men = _meses(desnudos)
    es, en = f"En {mes}, su tierra suele quedar sin plantas que la cubran", f"In {men}, your land is usually left with no plants covering it"
    if h["estado"] == "amarillo" and poca:
        pes_, pen_ = _meses(poca)
        es += f"; en {pes_}, con pocas"
        en += f"; in {pen_}, with little cover"
    return es + cola_es, en + cola_en


def _quema(h: dict, umbrales: dict) -> tuple[str, str]:
    nes, nen = NOMBRE_HECHO["quema"]
    pes, pen = _palabras(umbrales, h["estado"])
    v, d = h["valor"], h["de"]
    if h["estado"] == "gris":
        return f"{nes}: {pes}.", f"{nen}: {pen}."
    if h["estado"] == "verde" or not v:
        return (f"En los últimos {d} años, el satélite no vio quemas a menos de medio kilómetro de su parcela.",
                f"In the last {d} years, the satellite saw no fires within half a kilometer of your plot.")
    es = f"En {v} de los últimos {d} años hubo quemas a menos de medio kilómetro de su parcela"
    en = f"In {v} of the last {d} years there were fires within half a kilometer of your plot"
    if h.get("meses"):
        mes, men = _meses(h["meses"])
        es, en = es + f", en {mes}", en + f", in {men}"
    return es + ".", en + "."


def _canicula(h: dict, umbrales: dict, umbral_dias: int) -> tuple[str, str]:
    nes, nen = NOMBRE_HECHO["canicula"]
    pes, pen = _palabras(umbrales, h["estado"])
    v, d, u = h["valor"], h["de"], umbral_dias
    if h["estado"] == "gris":
        return f"{nes}: {pes}.", f"{nen}: {pen}."
    if h["estado"] == "verde" or not v:
        return (f"En los últimos {d} años, la canícula nunca dejó más de {u} días seguidos casi sin lluvia.",
                f"In the last {d} years, the midsummer drought never brought more than {u} days in a row with almost no rain.")
    return (f"En {v} de los últimos {d} años, la canícula dejó más de {u} días seguidos casi sin lluvia.",
            f"In {v} of the last {d} years, the midsummer drought brought more than {u} days in a row with almost no rain.")


def parte_de_lo_normal(pct: float) -> tuple[str, str]:
    """La lluvia frente a lo normal, en palabras de todos los días; la fracción más cercana a la cifra, sin exagerar."""
    if pct < 18:
        return "casi nada de lo normal", "almost none of the normal rain"
    if pct <= 22:
        return "solo la quinta parte de lo normal", "only a fifth of the normal rain"
    if pct <= 28:
        return "solo la cuarta parte de lo normal", "only a quarter of the normal rain"
    if pct <= 38:
        return "solo la tercera parte de lo normal", "only a third of the normal rain"
    if pct < 47:
        return "menos de la mitad de lo normal", "less than half the normal rain"
    if pct <= 55:
        return "la mitad de lo normal", "half the normal rain"
    if pct < 90:
        return "menos de lo normal", "less than the normal rain"
    if pct <= 110:
        return "más o menos lo normal", "about the normal rain"
    return "más de lo normal", "more than the normal rain"


def _este_anio(e: dict) -> tuple[str, str]:
    """Lluvia de julio y agosto de este año frente a lo normal (CHIRPS, preliminar), y frente al año más seco."""
    pes, pen = parte_de_lo_normal(e["pct_de_la_mediana"])
    es = f"Este año, en julio y agosto, llovió {pes} ({e['pct_de_la_mediana']} %)."
    en = f"This year, July and August got {pen} ({e['pct_de_la_mediana']} %)."
    if e.get("anio_mas_seco") and e.get("total_mas_seco_mm") is not None and e["total_2026_mm"] < e["total_mas_seco_mm"]:
        es += f" Es menos que en {e['anio_mas_seco']}, el año más seco desde {e['desde']}."
        en += f" That is less than in {e['anio_mas_seco']}, the driest year since {e['desde']}."
    return es + " Es un dato preliminar.", en + " It is a preliminary figure."


def nombre_hoy(res: dict) -> tuple[str, str]:
    """El cultivo de hoy con su nombre («maíz con frijol»), sacado del nombre largo de la rotación actual."""
    r = next(x for x in res["rotaciones"] if x["es_actual"])
    es = re.sub(r"^.*?:\s*", "", r.get("nombre") or "").split(" en primera")[0].strip() or (r.get("nombre_corto") or "")
    en_n = (r.get("en") or {}).get("nombre") or ""
    en = re.sub(r"^.*?:\s*", "", en_n).split(" in primera")[0].strip() or ((r.get("en") or {}).get("nombre_corto") or es)
    return es, en


def _futuro(res: dict, fu: dict) -> tuple[str, str]:
    """Las rotaciones en los climas posibles de la NASA: en cuántos le alcanza el agua (al menos como hoy)."""
    nombres = nombres_cortos(res)
    n, a, b = fu["n_modelos"], fu["desde"], fu["hasta"]
    hoy_es, hoy_en = nombre_hoy(res)
    por_id = {x["id"]: x for x in fu["rotaciones"]}
    actual = next(r for r in res["rotaciones"] if r["es_actual"])["id"]
    k = por_id[actual]["aguantan"]
    es = (f"La NASA calcula {n} climas posibles para {a} a {b}. Si siembra como hoy, {hoy_es}, le alcanza el agua en "
          f"{k} de {n}.")
    en = f"NASA computes {n} possible climates for {a} to {b}. Planting as today, {hoy_en} has enough water in {k} of {n}."
    for r in res["rotaciones"]:
        if r["es_actual"] or r["id"] not in por_id:
            continue
        k2 = por_id[r["id"]]["aguantan"]
        n_es, n_en = nombres[r["id"]]
        cuantos_es = f"en los {n}" if k2 == n else f"en {k2}"
        cuantos_en = f"in all {n}" if k2 == n else f"in {k2}"
        es += f" {n_es[:1].upper() + n_es[1:]}: {cuantos_es}."
        en += f" {n_en[:1].upper() + n_en[1:]}: {cuantos_en}."
    return es, en


def nombres_cortos(res: dict) -> dict[str, tuple[str, str]]:
    """{id de rotación: (nombre corto en español, en inglés)}."""
    out = {}
    for r in res["rotaciones"]:
        es = r.get("nombre_corto") or r["nombre"]
        en = (r.get("en") or {}).get("nombre_corto") or es
        out[r["id"]] = (es, en)
    return out


def _opciones(res: dict, op: dict) -> tuple[str, str]:
    nombres = nombres_cortos(res)
    if op["estado"] == "gris":
        conf = next(r for r in res["rotaciones"] if r["es_actual"])["confianza"]
        razones = [RAZON_CONFIANZA.get(c["criterio"], RAZON_GENERICA) for c in conf.get("criterios", [])
                   if c.get("cumple") is not True]
        razones = list(dict.fromkeys(razones)) or [RAZON_GENERICA]
        return (f"No podemos decir qué opción conviene más: {_lista([r[0] for r in razones], 'y')}.",
                f"We can't say which option is best: {_lista([r[1] for r in razones], 'and')}.")
    if op["estado"] == "una_destaca":
        es, en = nombres[op["destaca"]]
        return f"Hoy, la opción que mejor sale es {es}.", f"Today, the option that comes out best is {en}."
    grupo = op["empatadas"]
    es_n, en_n = [nombres[i][0] for i in grupo], [nombres[i][1] for i in grupo]
    if op["actual"] in grupo:
        cuantas_es = "Las tres" if len(grupo) == 3 else NUM_ES[len(grupo)].capitalize()
        cuantas_en = "All three" if len(grupo) == 3 else NUM_EN[len(grupo)].capitalize()
        return (f"Hoy, {_min(cuantas_es)} opciones quedan parejas: {_lista(es_n, 'y')}.",
                f"Today, {_min(cuantas_en)} options come out even: {_lista(en_n, 'and')}.")
    return (f"Hoy hay {NUM_ES[len(grupo)]} opciones parejas: {_lista(es_n, 'o')}.",
            f"Today there are {NUM_EN[len(grupo)]} even options: {_lista(en_n, 'or')}.")


def construir(res: dict, hechos: list[dict], opciones: dict, umbrales: dict, este_anio: dict | None = None,
              futuros: dict | None = None) -> list[dict]:
    """Frases de la vista y del audio, en orden: parcela, suelo, quema, canícula, este año (si hay la cifra de
    julio-agosto), opciones, el futuro (si hay los futuros de la NASA para la parcela) y cierre."""
    m = res["parcela"]["municipio"]
    suelo, quema, canicula = hechos
    u = res["clima"]["canicula"]["umbral_racha_dias"]
    out = [
        _frase("parcela", None, f"Parcela de {m}. Le habla una voz de computadora.",
               f"{m} plot. A computer voice is reading this."),
        _frase("suelo", "suelo", *_suelo(suelo, umbrales)),
        _frase("quema", "quema", *_quema(quema, umbrales)),
        _frase("canicula", "canicula", *_canicula(canicula, umbrales, u)),
    ]
    if este_anio:
        out.append(_frase("este_anio", None, *_este_anio(este_anio)))
    out.append(_frase("opciones", None, *_opciones(res, opciones)))
    if futuros and opciones.get("estado") != "gris":
        out.append(_frase("futuro", None, *_futuro(res, futuros)))
    out.append(_frase("cierre", None, *CIERRE))
    return out


def texto_audio(frases: list[dict], idioma: str = "es") -> str:
    """Texto que lee el mp3 corto: las frases en el idioma pedido («es» o «en»), en orden."""
    return " ".join(f[idioma] for f in frases)


def _marca(s: float) -> str:
    ms = round(s * 1000)
    h, ms = divmod(ms, 3_600_000)
    mi, ms = divmod(ms, 60_000)
    se, ms = divmod(ms, 1000)
    return f"{h:02d}:{mi:02d}:{se:02d}.{ms:03d}"


def vtt(frases: list[dict], idioma: str) -> str:
    """Subtítulos WebVTT de las frases con tiempos (idioma: «es» o «en»)."""
    lineas = ["WEBVTT", ""]
    for i, f in enumerate(frases, 1):
        if f.get("inicio_s") is None or f.get("fin_s") is None:
            raise ValueError(f"La frase {f['id']} no tiene tiempos")
        lineas += [str(i), f"{_marca(f['inicio_s'])} --> {_marca(f['fin_s'])}", f[idioma], ""]
    return "\n".join(lineas)
