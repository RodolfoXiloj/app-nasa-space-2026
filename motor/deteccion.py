"""Paso 1 — lo que ve el satélite: meses de suelo desnudo, ciclos por año, quemas y calidad.

Todos los umbrales son VALORES INICIALES; se calibran con las 5 parcelas y quedan escritos en
docs/validacion.md. Ver UMBRALES.

Calibración del 13 nov 2026 (antes de correr la prueba de 2018): en ladera el píxel de 250 m mezcla
la milpa con árboles y el NDVI seco no baja de 0.35 aunque la parcela esté desnuda. No se movió el
umbral de suelo desnudo (0.35); se agregó la clase «poca cobertura» (0.35 a 0.45), que cuenta la
mitad en el puntaje de suelo. En la literatura de NDVI, 0.2 a 0.4 corresponde a vegetación rala.
"""
from __future__ import annotations

import statistics
from collections import defaultdict

UMBRALES = {
    "ndvi_desnudo": 0.35,            # mes con NDVI mediano < 0.35 -> suelo desnudo
    "ndvi_poca_cobertura": 0.45,     # 0.35 <= NDVI < 0.45 -> poca cobertura (calibración del 13 nov, ver abajo)
    "anios_recientes": 5,            # ventana para meses desnudos y ciclos
    "calidad_valida": (0, 1),        # pixel_reliability de MOD13Q1: 0 bueno, 1 marginal
    "prominencia_pico": 0.15,        # prominencia mínima de un pico de NDVI para contar un ciclo
    "meses_ciclo": (5, 12),          # los picos se buscan entre mayo y diciembre
    "radio_quema_m": 500.0,          # quema "cercana"
    "meses_quema": (1, 2, 3, 4, 5),  # época de quema de rastrojo
    "confianza_viirs": ("n", "h"),   # nominal o alta
}


def _valido(ndvi, cal) -> bool:
    return ndvi is not None and cal in UMBRALES["calidad_valida"]


def periodo_reciente(filas: list[list], n: int | None = None) -> tuple[int, int]:
    """Últimos n años completos (con al menos 20 compuestos) en la serie."""
    n = n or UMBRALES["anios_recientes"]
    por_anio = defaultdict(int)
    for f, *_ in filas:
        por_anio[int(f[:4])] += 1
    completos = sorted(a for a, c in por_anio.items() if c >= 20)
    if not completos:
        raise ValueError("La serie NDVI no tiene ningún año completo")
    fin = completos[-1]
    return max(completos[0], fin - n + 1), fin


def prominencias(valores: list[float]) -> list[tuple[int, float]]:
    """Picos locales y su prominencia (misma definición que scipy.signal.peak_prominences)."""
    picos = []
    n = len(valores)
    for i in range(1, n - 1):
        v = valores[i]
        if not (v > valores[i - 1] and v >= valores[i + 1]):
            continue
        izq = v
        j = i - 1
        while j >= 0 and valores[j] <= v:
            izq = min(izq, valores[j])
            j -= 1
        der = v
        j = i + 1
        while j < n and valores[j] <= v:
            der = min(der, valores[j])
            j += 1
        picos.append((i, round(v - max(izq, der), 4)))
    return picos


def detectar(ndvi_cache: dict, firms_cache: dict | None) -> dict:
    filas = ndvi_cache["datos"]["filas"]
    ini, fin = periodo_reciente(filas)
    recientes = [f for f in filas if ini <= int(f[0][:4]) <= fin]

    # Calidad
    validos = [f for f in recientes if _valido(f[1], f[2])]
    pct_validos = round(100 * len(validos) / len(recientes), 1) if recientes else 0.0

    # NDVI mediano por mes y meses desnudos
    por_mes: dict[int, list[float]] = defaultdict(list)
    for f, v, _c in validos:
        por_mes[int(f[5:7])].append(v)
    ndvi_mensual = []
    desnudos = []
    poca = []
    for m in range(1, 13):
        vals = por_mes.get(m, [])
        med = round(statistics.median(vals), 3) if vals else None
        ndvi_mensual.append({"mes": m, "mediana": med, "n": len(vals)})
        if med is not None and med < UMBRALES["ndvi_desnudo"]:
            desnudos.append(m)
        elif med is not None and med < UMBRALES["ndvi_poca_cobertura"]:
            poca.append(m)

    # Ciclos por año: picos con prominencia >= umbral entre mayo y diciembre
    m_ini, m_fin = UMBRALES["meses_ciclo"]
    por_anio = []
    for anio in range(ini, fin + 1):
        serie = [(f, v) for f, v, c in validos if int(f[:4]) == anio and m_ini <= int(f[5:7]) <= m_fin]
        # se agregan los bordes (abril y enero siguiente) para que un pico en mayo o diciembre tenga base
        antes = [(f, v) for f, v, c in validos if int(f[:4]) == anio and int(f[5:7]) == m_ini - 1]
        despues = [(f, v) for f, v, c in validos if int(f[:4]) == anio + 1 and int(f[5:7]) == 1]
        completa = antes[-1:] + serie + despues[:1]
        picos = [(completa[i][0], p) for i, p in prominencias([v for _, v in completa])
                 if p >= UMBRALES["prominencia_pico"] and m_ini <= int(completa[i][0][5:7]) <= m_fin
                 and int(completa[i][0][:4]) == anio]
        por_anio.append({"anio": anio, "ciclos": len(picos), "picos": [f for f, _ in picos]})
    ciclos_med = statistics.median([a["ciclos"] for a in por_anio]) if por_anio else None

    quemas = detectar_quemas(firms_cache)

    serie = [{"fecha": f, "ndvi": v, "valido": _valido(v, c)} for f, v, c in recientes]
    return {
        "periodo": f"{ini}-{fin}",
        "umbral_desnudo_ndvi": UMBRALES["ndvi_desnudo"],
        "meses_desnudos": desnudos,
        "umbral_poca_cobertura_ndvi": UMBRALES["ndvi_poca_cobertura"],
        "meses_poca_cobertura": poca,
        "ndvi_mensual": ndvi_mensual,
        "ciclos": {"mediana": ciclos_med, "prominencia_min": UMBRALES["prominencia_pico"], "por_anio": por_anio},
        "quemas": quemas,
        "calidad": {"compuestos": len(recientes), "validos": len(validos), "pct_validos": pct_validos},
        "serie": serie,
        "fuente_ids": ["modis_mod13q1", "ornl_subsets", "firms_viirs"],
    }


def detectar_quemas(firms_cache: dict | None) -> dict:
    radio = UMBRALES["radio_quema_m"]
    meses = list(UMBRALES["meses_quema"])
    nota = ("Quema cercana = foco VIIRS de confianza nominal o alta a 500 m o menos, entre enero y mayo. "
            "Sin detección no significa que no hubo quema: el satélite pasa pocas veces al día y no ve quemas breves o bajo nubes.")
    if not firms_cache:
        return {"radio_m": radio, "meses": meses, "anios_con_quema": 0, "anios_observados": 0, "periodo": "sin datos",
                "meses_con_quema": [], "detecciones_1km": 0, "detecciones": [],
                "nota": "Sin datos de FIRMS para esta parcela. " + nota}
    d = firms_cache["datos"]
    anios_obs = d["anios_observados"]
    dets = []
    anios_q, meses_q = set(), set()
    for x in d["detecciones"]:
        mes = int(x["fecha"][5:7])
        cuenta = (x.get("tipo", 0) == 0 and str(x["confianza"]).lower() in UMBRALES["confianza_viirs"]
                  and x["distancia_m"] <= radio and mes in UMBRALES["meses_quema"])
        if cuenta:
            anios_q.add(int(x["fecha"][:4]))
            meses_q.add(mes)
        dets.append({"fecha": x["fecha"], "lat": x["lat"], "lon": x["lon"], "distancia_m": x["distancia_m"],
                     "confianza": str(x["confianza"]), "frp": x.get("frp", 0.0), "cuenta": cuenta})
    return {
        "radio_m": radio, "meses": meses, "anios_con_quema": len(anios_q), "anios_observados": len(anios_obs),
        "periodo": f"{min(anios_obs)}-{max(anios_obs)}" if anios_obs else "sin datos",
        "meses_con_quema": sorted(meses_q), "detecciones_1km": len(dets), "detecciones": dets, "nota": nota,
    }
