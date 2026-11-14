"""Textos de la tarjeta con plantillas deterministas + validadores.

- validar_numeros(): rechaza un texto con una cifra que no esté en el JSON del motor (plan, 1.6).
  Si en el futuro un LLM reescribe los textos al exportar, su salida pasa por aquí y, si falla,
  se vuelve a la plantilla.
- fechas_no_citadas(): detecta fechas o semanas de siembra que no vengan de ZARC (plan, 4.4.6).

Regla de estilo: los textos no llevan cifras sueltas que no estén en el JSON; los números de
estructura se escriben con letra («tres opciones»).
"""
from __future__ import annotations

import re

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre",
         "octubre", "noviembre", "diciembre"]

AVISO = ("Milpa Resiliente apoya, no reemplaza, al técnico ni al agricultor. Las cifras vienen de satélites "
         "y modelos con límites que se explican en cada opción. Verifíquelo con su extensionista.")

# ---------------------------------------------------------------- validador de números
_SEP = re.compile(r"[\s()\[\]{}:;\"«»¿?¡!/]+")
_NUM = re.compile(r"[-−+]?\d+(?:\.\d+)?%?")
_RANGO = re.compile(r"([-−+]?\d+(?:\.\d+)?)[-–]([-−+]?\d+(?:\.\d+)?)%?")

# Campos que son texto redactado (se validan) o series crudas (no cuentan como respaldo).
CAMPOS_TEXTO = {"por_que", "beneficios", "vacios", "riesgos", "texto_tarjeta", "texto", "motivo", "aviso",
                "glosario", "trazabilidad", "detalle", "nota", "nota_escenario", "cita", "descripcion"}
CAMPOS_CRUDOS = {"serie", "por_anio", "detecciones", "lluvia_anual_mm"}


def numeros_en(texto: str) -> list[str]:
    out = []
    for tok in _SEP.split(texto):
        tok = tok.strip(".,'")
        if not tok:
            continue
        if _NUM.fullmatch(tok):
            out.append(tok.rstrip("%"))
        else:
            m = _RANGO.fullmatch(tok)
            if m:
                out += [m.group(1), m.group(2)]
    return out


def _a_float(s: str) -> float:
    return float(s.replace("−", "-").replace("+", ""))


def numeros_permitidos(obj, _clave: str | None = None, out: set | None = None) -> set[float]:
    """Todos los números del JSON del motor, salvo los que están dentro de textos redactados."""
    out = set() if out is None else out
    if _clave in CAMPOS_TEXTO or _clave in CAMPOS_CRUDOS:
        return out
    if isinstance(obj, bool) or obj is None:
        return out
    if isinstance(obj, (int, float)):
        out.add(float(obj))
    elif isinstance(obj, str):
        out.update(_a_float(n) for n in numeros_en(obj))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            numeros_permitidos(v, k, out)
    elif isinstance(obj, list):
        for v in obj:
            numeros_permitidos(v, _clave, out)
    return out


def validar_numeros(texto: str, permitidos: set[float]) -> list[str]:
    """Devuelve las cifras del texto que NO están respaldadas por el JSON (lista vacía = ok)."""
    redondeados = {}
    malas = []
    for n in numeros_en(texto):
        dec = len(n.split(".")[1]) if "." in n else 0
        if dec not in redondeados:
            redondeados[dec] = {round(v, dec) for v in permitidos} | {round(abs(v), dec) for v in permitidos}
        v = _a_float(n)
        if round(v, dec) not in redondeados[dec] and round(abs(v), dec) not in redondeados[dec]:
            malas.append(n)
    return malas


# ---------------------------------------------------------------- fechas y semanas (ZARC)
_MESES_RE = "|".join(MESES + ["setiembre"])
_FECHA = re.compile(
    rf"\b\d{{1,2}}\s+(?:de\s+)?(?:{_MESES_RE})\b"
    rf"|\bsemanas?\s+\d+\b"
    rf"|\b\d{{1,2}}/\d{{1,2}}(?:/\d{{2,4}})?\b"
    rf"|\b(?:primera|segunda|tercera|cuarta|última|ultima)\s+semana\s+de\s+(?:{_MESES_RE})\b"
    rf"|\b(?:inicios?|mediados|finales?)\s+de\s+(?:{_MESES_RE})\b",
    re.IGNORECASE,
)


def fechas_no_citadas(texto: str, citas_zarc: list[str]) -> list[str]:
    limpio = texto
    for c in citas_zarc:
        if c:
            limpio = limpio.replace(c, " ")
    return [m.group(0) for m in _FECHA.finditer(limpio)]


# ---------------------------------------------------------------- plantillas
def lista_meses(ms: list[int]) -> str:
    nombres = [MESES[m - 1] for m in sorted(ms)]
    if not nombres:
        return "ninguno"
    if len(nombres) == 1:
        return nombres[0]
    return ", ".join(nombres[:-1]) + " y " + nombres[-1]


def plural(n: float, uno: str, varios: str) -> str:
    return uno if n == 1 else varios


def por_que(tipo: str, ctx: dict) -> str:
    det, ev, act = ctx["det"], ctx["ev"], ctx["ev_actual"]
    q = det["quemas"]
    if tipo == "actual":
        n = ev["n_desnudos"]
        if n:
            vista = (f"El satélite MODIS ({det['periodo']}) ve el suelo desnudo en {n} "
                     f"{plural(n, 'mes', 'meses')} del año: {lista_meses(ev['meses_desnudos'])}.")
        elif ev.get("n_poca"):
            vista = (f"El satélite MODIS ({det['periodo']}) no ve el suelo del todo desnudo, pero sí con poca "
                     f"cobertura en {ev['n_poca']} {plural(ev['n_poca'], 'mes', 'meses')}: {lista_meses(ev['meses_poca'])}.")
        else:
            vista = (f"El satélite MODIS ({det['periodo']}) no ve ningún mes con suelo desnudo: "
                     f"el verdor mediano no baja de {det['umbral_desnudo_ndvi']}.")
        ciclos = det["ciclos"]["mediana"]
        txt = (f"Es lo que hace hoy. {vista} Cuenta {ciclos} {plural(ciclos, 'ciclo', 'ciclos')} de verdor por año. "
               f"Hubo quema cercana en {q['anios_con_quema']} de {q['anios_observados']} años observados con VIIRS.")
        return txt
    if tipo == "leguminosa_cobertura":
        if ev["n_desnudos"] == act["n_desnudos"] and ev.get("n_poca", 0) < act.get("n_poca", 0):
            return (f"Cuida el suelo: con cobertura y rastrojo en pie, los meses de poca cobertura bajarían de "
                    f"{act['n_poca']} a {ev['n_poca']}, sin quema. La leguminosa aporta nitrógeno y materia orgánica.")
        if ev["n_desnudos"] < act["n_desnudos"]:
            inicio = (f"Cuida el suelo: con cobertura y rastrojo en pie, los meses de suelo desnudo bajarían de "
                      f"{act['n_desnudos']} a {ev['n_desnudos']}, sin quema.")
        else:
            inicio = ("El satélite no ve más meses desnudos de los que esta práctica puede cubrir; "
                      "su ventaja aquí es dejar de quemar y devolverle materia orgánica al suelo.")
        return inicio + " La leguminosa aporta nitrógeno y materia orgánica."
    pa, pc = ev["deficit"]["perdida_mediana_pct"], act["deficit"]["perdida_mediana_pct"]
    seco = ctx.get("escenario_seco")
    cola = ""
    if seco:
        cola = (f" En el escenario más seco (lluvia {seco['lluvia_pct']} % y +{seco['temp_c']} °C) el déficit de agua "
                f"sería de {seco['alt']} % frente a {seco['act']} %.")
    if pa < pc:
        return (f"Aguanta mejor la falta de agua. Con el clima de {ctx['clima']['periodo']}, la pérdida de cosecha esperada "
                f"por falta de agua sería de {pa} % en un año típico, frente a {pc} % de lo que hace hoy." + cola)
    return (f"Es la opción más tolerante a sequía de la biblioteca, pero con el clima de {ctx['clima']['periodo']} "
            f"la pérdida esperada por falta de agua es parecida a la de hoy ({pa} % frente a {pc} %)." + cola)


def beneficios(rot: dict, ctx: dict) -> list[str]:
    ev, act = ctx["ev"], ctx["ev_actual"]
    out = list(rot.get("beneficios") or [])
    if not ctx["es_actual"]:
        if ev["n_desnudos"] < act["n_desnudos"]:
            out.append(f"Menos meses de suelo desnudo: {ev['n_desnudos']} en vez de {act['n_desnudos']}.")
        if ev["puntajes"]["agua"] > act["puntajes"]["agua"]:
            out.append(f"Mejor puntaje de agua: {ev['puntajes']['agua']} frente a {act['puntajes']['agua']}.")
    return out or ["Sin beneficio claro frente a lo que hace hoy con los datos disponibles."]


def vacios(rot: dict, ctx: dict) -> list[str]:
    out = list(rot.get("vacios") or [])
    if ctx.get("con_chirps"):
        out.append("La lluvia viene de CHIRPS, en celdas de ~5 km, y la temperatura de NASA POWER, en celdas de ~50 km: "
                   "describen la zona cercana, no su parcela exacta.")
    else:
        out.append("La lluvia viene de NASA POWER, una celda de ~50 km: describe la zona, no su parcela.")
    if ctx.get("smap_sin_calidad"):
        out.append("SMAP no tiene mediciones de buena calidad para esta zona; la humedad del suelo sale de un modelo (MERRA-2).")
    elif not ctx["hay_smap"]:
        out.append("Aún no tenemos la humedad del suelo medida por SMAP; por ahora se usa un modelo (MERRA-2).")
    if "supuesto" in str(rot.get("fuente", "")):
        out.append("Las reglas de esta opción son un supuesto inicial: falta revisarlas con un agrónomo.")
    for c in ctx["cultivos_sin_ky"]:
        out.append(f"El {c} no tiene factor de respuesta al agua en FAO-33: se usó un valor neutro.")
    if ctx["es_actual"]:
        out.append("El píxel de MODIS mide 250 m: puede mezclar su parcela con las vecinas.")
        out.append("No hay precios verificados por cultivo: no comparamos ingresos.")
        if ctx["ciclos_discrepan"]:
            out.append("El satélite cuenta un número de ciclos distinto al que usted declaró: confírmelo con el agricultor.")
    return out


def riesgos(rot: dict, ctx: dict) -> list[str]:
    ev, det, cl = ctx["ev"], ctx["det"], ctx["clima"]
    out = list(rot.get("riesgos") or [])
    pend = ctx["pendiente_pct"]
    if pend is not None and pend > 15 and ev["n_desnudos"] > 0:
        out.append(f"Pendiente de {pend} %: en los meses sin cobertura la lluvia arrastra el suelo.")
    can = cl["canicula"]
    if can["anios_racha_larga"] and ev["toca_canicula"]:
        out.append(f"En {can['anios_racha_larga']} de {can['anios_total']} años la racha seca de la canícula "
                   f"pasó de {can['umbral_racha_dias']} días, cuando este cultivo está en el campo.")
    if ctx["es_actual"] and det["quemas"]["anios_con_quema"]:
        out.append("Quemar el rastrojo deja el suelo sin protección justo antes de las lluvias.")
    return out


def texto_tarjeta(res: dict) -> str:
    p, det, rots = res["parcela"], res["deteccion"], res["rotaciones"]
    act = rots[0]
    ev_n = next((e["valor"] for e in act["evidencia"] if e["dato"].startswith("Meses de suelo desnudo")), 0)
    poca = det.get("meses_poca_cobertura") or []
    if ev_n:
        vista = f"el suelo queda desnudo en {lista_meses(det['meses_desnudos'])}"
    elif poca:
        vista = f"el suelo queda con poca cobertura en {lista_meses(poca)}"
    else:
        vista = "no se ven meses con el suelo desnudo"
    ordinales = ["Opción uno, lo que hace hoy", "Opción dos", "Opción tres"]
    partes = [f"Parcela de {p['municipio']}, {p['departamento']}.",
              f"Lo que ve el satélite: {vista}.",
              "Comparamos tres opciones."]
    for o, r in zip(ordinales, rots):
        partes.append(f"{o}: {r['nombre'].replace('Lo que hace hoy: ', '')}. Puntaje {r['puntajes']['total']}.")
    mejor = max(rots, key=lambda r: r["puntajes"]["total"])
    partes.append(f"Según su prioridad, {p['prioridad']}, la que mejor sale es: "
                  f"{mejor['nombre'].replace('Lo que hace hoy: ', 'la de hoy, ')}.")
    partes.append(f"Confianza {act['confianza']['nivel']}.")
    partes.append(res["zarc"]["texto"])
    partes.append("Esta herramienta apoya, no reemplaza, a su técnico.")
    return " ".join(partes)
