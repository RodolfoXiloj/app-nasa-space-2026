"""Frases cortas de la vista «Para el agricultor» y de su audio por frases (paso 4 del plan).

Salen del bloque `farmer` ya calculado (estados de los 3 hechos y regla de empate) y de los nombres
cortos de las rotaciones (data/rotaciones.yaml). Cada frase va en español y en inglés.

Regla «nada solo en audio»: el mp3 corto lee solo `texto_audio(frases)`, es decir, el español de estas
mismas frases, que están en el JSON como texto visible. Las cifras son las de los hechos (validador de
números de motor/redaccion.py); los números de estructura van con letra («dos opciones»).
Sin la palabra «alerta»: el cierre dice que no es un aviso oficial.
"""
from __future__ import annotations

NUM_ES = {2: "dos", 3: "tres"}
NUM_EN = {2: "two", 3: "three"}
# El audio dura de 20 a 30 s: frases cortas, y el satélite se nombra una vez (en el suelo).
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


def _suelo(h: dict, umbrales: dict) -> tuple[str, str]:
    nes, nen = NOMBRE_HECHO["suelo"]
    pes, pen = _palabras(umbrales, h["estado"])
    n, p = h["valor"], len(h.get("meses_poca_cobertura") or [])
    if h["estado"] == "gris":
        return f"{nes}: {pes}.", f"{nen}: {pen}."
    if h["estado"] == "verde":
        return f"{nes}: {pes}. El satélite no vio suelo desnudo.", f"{nen}: {pen}. The satellite saw no bare soil."
    if n == 0:
        return (f"{nes}: {pes}. El satélite vio {p} {_plural(p, 'mes', 'meses')} con poca cobertura, ninguno desnudo.",
                f"{nen}: {pen}. The satellite saw {p} {_plural(p, 'month', 'months')} with little cover, none bare.")
    es = f"{nes}: {pes}. El satélite vio {n} {_plural(n, 'mes', 'meses')} de suelo desnudo"
    en = f"{nen}: {pen}. The satellite saw {n} {_plural(n, 'month', 'months')} of bare soil"
    if h["estado"] == "amarillo" and p:
        es += f" y {p} con poca cobertura"
        en += f" and {p} with little cover"
    return es + ".", en + "."


def _quema(h: dict, umbrales: dict) -> tuple[str, str]:
    nes, nen = NOMBRE_HECHO["quema"]
    pes, pen = _palabras(umbrales, h["estado"])
    v, d = h["valor"], h["de"]
    if h["estado"] == "gris":
        return f"{nes}: {pes}.", f"{nen}: {pen}."
    if h["estado"] == "verde":
        return f"{nes}: {pes}. No vio quemas cerca en {d} años.", f"{nen}: {pen}. No fires seen nearby in {d} years."
    return (f"{nes}: {pes}. Vio quemas cerca en {v} de {d} años.",
            f"{nen}: {pen}. Fires seen nearby in {v} of {d} years.")


def _canicula(h: dict, umbrales: dict, umbral_dias: int) -> tuple[str, str]:
    nes, nen = NOMBRE_HECHO["canicula"]
    pes, pen = _palabras(umbrales, h["estado"])
    v, d, u = h["valor"], h["de"], umbral_dias
    if h["estado"] == "gris":
        return f"{nes}: {pes}.", f"{nen}: {pen}."
    if h["estado"] == "verde":
        return (f"{nes}: {pes}. Ninguna racha seca pasó de {u} días en {d} años.",
                f"{nen}: {pen}. No dry spell went past {u} days in {d} years.")
    return (f"{nes}: {pes}. Racha seca de más de {u} días en {v} de {d} años.",
            f"{nen}: {pen}. Dry spells longer than {u} days in {v} of {d} years.")


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
        return f"La opción que mejor sale es {es}.", f"The option that comes out best is {en}."
    grupo = op["empatadas"]
    es_n, en_n = [nombres[i][0] for i in grupo], [nombres[i][1] for i in grupo]
    if op["actual"] in grupo:
        cuantas_es = "Las tres" if len(grupo) == 3 else NUM_ES[len(grupo)].capitalize()
        cuantas_en = "All three" if len(grupo) == 3 else NUM_EN[len(grupo)].capitalize()
        return (f"{cuantas_es} opciones quedan parejas: {_lista(es_n, 'y')}.",
                f"{cuantas_en} options come out even: {_lista(en_n, 'and')}.")
    return (f"Hay {NUM_ES[len(grupo)]} opciones parejas: {_lista(es_n, 'o')}.",
            f"There are {NUM_EN[len(grupo)]} even options: {_lista(en_n, 'or')}.")


def construir(res: dict, hechos: list[dict], opciones: dict, umbrales: dict) -> list[dict]:
    """Frases de la vista y del audio, en orden: parcela, suelo, quema, canícula, opciones y cierre."""
    m = res["parcela"]["municipio"]
    suelo, quema, canicula = hechos
    u = res["clima"]["canicula"]["umbral_racha_dias"]
    return [
        _frase("parcela", None, f"Parcela de {m}, con voz de computadora.",
               f"{m} plot, read by a computer voice."),
        _frase("suelo", "suelo", *_suelo(suelo, umbrales)),
        _frase("quema", "quema", *_quema(quema, umbrales)),
        _frase("canicula", "canicula", *_canicula(canicula, umbrales, u)),
        _frase("opciones", None, *_opciones(res, opciones)),
        _frase("cierre", None, *CIERRE),
    ]


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
