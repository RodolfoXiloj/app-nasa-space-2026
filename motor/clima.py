"""Paso 2a — clima: ET0 (Hargreaves, FAO-56), demanda del cultivo, déficit por ciclo y canícula.

Supuestos declarados (valores iniciales, se revisan el sábado):
- Lluvia efectiva = 80 % de la lluvia de POWER.
- Balance hídrico diario con una reserva de 50 mm en el suelo (agua fácilmente aprovechable),
  que arranca a la mitad al sembrar. Lo que sobra se escurre o se infiltra hondo.
  Déficit del ciclo = 1 - agua que el cultivo pudo usar / agua que pidió (ETc = Kc x ET0).
  Con reserva, la lluvia de septiembre no tapa el hueco de julio: así se ve la canícula.
- Canícula: racha seca más larga entre el 15 de junio y el 31 de agosto. Día seco < 2 mm:
  el plan (4.3) decía 1 mm y subir a 2 mm si POWER muestra llovizna constante. En Jocotán, con
  1 mm la racha mediana fue de 4 días (13 nov 2026): se aplicó la regla, no se ajustó para 2018.
- Periodo: 2001-2025. La lluvia de POWER en Jocotán cambia de nivel antes de 2001
  (1991-1996 entre 357 y 834 mm/año; 2001-2025 entre 910 y 2931 mm/año), posiblemente por un
  cambio de fuente del dato. TODO(Mario): confirmarlo en la documentación de POWER y contra CHIRPS.
- La ET0 se calcula por Hargreaves porque solo usa temperatura; FAO-56 la acepta cuando faltan
  radiación, humedad y viento medidos.
- Lluvia corregida con CHIRPS (decisión del 13 nov, regla 5.1 del plan): si hay caché de CHIRPS
  v3 mensual (~5 km), cada día de POWER se multiplica por CHIRPS_mes / POWER_mes de ese año y mes.
  Así el total de cada mes es el de CHIRPS (que separa las parcelas que comparten celda de POWER)
  y los días con lluvia siguen el reparto de POWER. Si POWER marca menos de 1 mm en el mes, la
  lluvia de CHIRPS se reparte igual entre los días. La temperatura sigue siendo de POWER.
  En junio-agosto (canícula) se usa CHIRPS v3 diario 'sat', que reparte cada péntada de CHIRPS con el
  reparto diario de NASA IMERG; el resto del año, el reparto diario es el de POWER.
"""
from __future__ import annotations

import math
import statistics
from datetime import date, timedelta

SUPUESTOS = {
    "lluvia_efectiva": 0.80,
    "reserva_suelo_mm": 50.0,
    "reserva_inicial": 0.5,
    "dia_seco_mm": 2.0,
    "racha_larga_dias": 15,
    "canicula_ini": (6, 15),
    "canicula_fin": (8, 31),
    "anio_inicio": 2001,
}


def ra_mm(lat: float, doy: int) -> float:
    """Radiación extraterrestre (FAO-56, ec. 21-25) en mm/día equivalentes."""
    phi = math.radians(lat)
    dr = 1 + 0.033 * math.cos(2 * math.pi * doy / 365)
    delta = 0.409 * math.sin(2 * math.pi * doy / 365 - 1.39)
    ws = math.acos(max(-1.0, min(1.0, -math.tan(phi) * math.tan(delta))))
    ra_mj = (24 * 60 / math.pi) * 0.0820 * dr * (ws * math.sin(phi) * math.sin(delta)
                                                 + math.cos(phi) * math.cos(delta) * math.sin(ws))
    return 0.408 * ra_mj


def et0_hargreaves(tmax: float, tmin: float, ra: float) -> float:
    """FAO-56, ec. 52. ra en mm/día."""
    tmed = (tmax + tmin) / 2
    return max(0.0, 0.0023 * ra * (tmed + 17.8) * math.sqrt(max(tmax - tmin, 0.0)))


def preparar(power_diario: dict) -> dict[date, tuple[float | None, float | None, float | None, float | None]]:
    """{fecha: (lluvia_mm, tmax, tmin, gwetroot)} desde la caché de POWER diario."""
    col = power_diario["datos"]["columnas"]
    i_p, i_tx, i_tn, i_gw = (col.index(c) for c in ("PRECTOTCORR", "T2M_MAX", "T2M_MIN", "GWETROOT"))
    out = {}
    for f in power_diario["datos"]["filas"]:
        k = f[0]
        out[date(int(k[:4]), int(k[4:6]), int(k[6:8]))] = (f[i_p], f[i_tx], f[i_tn], f[i_gw])
    return out


def chirps_mensual(chirps_cache: dict | None) -> dict[tuple[int, int], float]:
    """{(año, mes): mm} desde la caché de CHIRPS (sin meses nulos)."""
    if not chirps_cache:
        return {}
    return {(a, m): mm for a, m, mm in chirps_cache["datos"]["filas"] if mm is not None}


def power_mensual(diario: dict) -> dict[tuple[int, int], float]:
    out: dict[tuple[int, int], float] = {}
    for d, (p, *_r) in diario.items():
        if p is not None:
            out[(d.year, d.month)] = out.get((d.year, d.month), 0.0) + p
    return out


def corregir_lluvia(diario: dict, chirps_cache: dict | None) -> tuple[dict, dict]:
    """Reescala la lluvia diaria de POWER al total mensual de CHIRPS. Devuelve (diario, info)."""
    ch = chirps_mensual(chirps_cache)
    if not ch:
        return diario, {"fuente": "NASA POWER", "meses_corregidos": 0}
    pw = power_mensual(diario)
    dias_mes: dict[tuple[int, int], int] = {}
    for d in diario:
        dias_mes[(d.year, d.month)] = dias_mes.get((d.year, d.month), 0) + 1
    out, factores, n = {}, [], 0
    for d, (p, tx, tn, gw) in diario.items():
        k = (d.year, d.month)
        if p is None or k not in ch:
            out[d] = (p, tx, tn, gw)
            continue
        if pw.get(k, 0.0) >= 1.0:
            f = ch[k] / pw[k]
            out[d] = (p * f, tx, tn, gw)
        else:
            out[d] = (ch[k] / dias_mes[k], tx, tn, gw)
    for k, mm in ch.items():
        if k in pw and pw[k] >= 1.0:
            factores.append(mm / pw[k])
            n += 1
    return out, {"fuente": "CHIRPS v3 mensual repartido por días con NASA POWER", "meses_corregidos": n,
                 "factor_mediano": round(statistics.median(factores), 2) if factores else None}


def aplicar_chirps_diario(diario: dict, chirps_diario_cache: dict | None, info: dict) -> tuple[dict, dict]:
    """En los días con CHIRPS v3 diario (junio-agosto), la lluvia pasa a ser la de CHIRPS.

    CHIRPS diario 'sat' reparte el total de cada péntada de CHIRPS con el reparto diario de NASA IMERG;
    así la racha seca de la canícula sale de un dato de ~5 km y no de la llovizna del modelo de POWER.
    """
    if not chirps_diario_cache:
        return diario, info
    dia = {}
    for f, mm in chirps_diario_cache["datos"]["filas"]:
        if mm is not None:
            dia[date(int(f[:4]), int(f[5:7]), int(f[8:10]))] = mm
    out = dict(diario)
    n = 0
    for d, mm in dia.items():
        if d in out and out[d][0] is not None:
            _p, tx, tn, gw = out[d]
            out[d] = (mm, tx, tn, gw)
            n += 1
    meses = sorted({d.month for d in dia})
    info = dict(info, dias_chirps_diario=n, meses_chirps_diario=meses,
                fuente=info.get("fuente", "NASA POWER") + "; junio-agosto con CHIRPS v3 diario (reparto con NASA IMERG)")
    return out, info


def comparar(diario: dict, chirps_cache: dict | None, desde: int, hasta: int) -> dict | None:
    """POWER contra CHIRPS por mes (plan 5.2): sesgo, error absoluto medio y Pearson, todo el año y julio-agosto."""
    ch = chirps_mensual(chirps_cache)
    if not ch:
        return None
    pw = power_mensual(diario)

    def metricas(claves):
        pares = [(pw[k], ch[k]) for k in claves if k in pw and k in ch]
        if len(pares) < 3:
            return None
        xs, ys = [a for a, _ in pares], [b for _, b in pares]
        mx, my = statistics.mean(xs), statistics.mean(ys)
        sx, sy = statistics.pstdev(xs), statistics.pstdev(ys)
        r = (sum((a - mx) * (b - my) for a, b in pares) / len(pares) / (sx * sy)) if sx > 0 and sy > 0 else None
        return {"n": len(pares), "power_mm_mes": round(mx, 1), "chirps_mm_mes": round(my, 1),
                "sesgo_mm_mes": round(mx - my, 1), "sesgo_pct": round(100 * (mx - my) / my, 1) if my > 0 else None,
                "eam_mm_mes": round(statistics.mean(abs(a - b) for a, b in pares), 1),
                "pearson_r": None if r is None else round(r, 2)}

    todos = [(a, m) for a in range(desde, hasta + 1) for m in range(1, 13)]
    return {"periodo": f"{desde}-{hasta}", "todos": metricas(todos),
            "jul_ago": metricas([k for k in todos if k[1] in (7, 8)])}


def serie_escenario(diario: dict, lat: float, lluvia_pct: float = 0.0, temp_c: float = 0.0) -> dict[date, tuple[float, float]]:
    """{fecha: (lluvia_mm, et0_mm)} aplicando el escenario. Días sin dato se omiten."""
    factor = 1 + lluvia_pct / 100
    out = {}
    for d, (p, tx, tn, _gw) in diario.items():
        if p is None or tx is None or tn is None:
            continue
        out[d] = (p * factor, et0_hargreaves(tx + temp_c, tn + temp_c, ra_mm(lat, d.timetuple().tm_yday)))
    return out


def kc_dia(cultivo: dict, t: int) -> float:
    ki, km, kf = cultivo["kc"]["ini"], cultivo["kc"]["med"], cultivo["kc"]["fin"]
    a, b, c, d = cultivo["etapas_dias"]
    if t < a:
        return ki
    if t < a + b:
        return ki + (t - a) / b * (km - ki)
    if t < a + b + c:
        return km
    return km + (t - a - b - c) / d * (kf - km)


def duracion(cultivo: dict) -> int:
    return sum(cultivo["etapas_dias"])


def balance_ciclo(serie: dict, inicio: date, cultivo: dict) -> tuple[float, float] | None:
    """(demanda ETc, agua usada) del ciclo en mm. None si faltan días."""
    cap = SUPUESTOS["reserva_suelo_mm"]
    reserva = cap * SUPUESTOS["reserva_inicial"]
    demanda = usada = 0.0
    for t in range(duracion(cultivo)):
        d = inicio + timedelta(days=t)
        if d not in serie:
            return None
        p, et0 = serie[d]
        etc = kc_dia(cultivo, t) * et0
        reserva = min(cap, reserva + p * SUPUESTOS["lluvia_efectiva"])
        uso = min(reserva, etc)
        reserva -= uso
        demanda += etc
        usada += uso
    return demanda, usada


def balance_rotacion(serie: dict, anios: list[int], ciclos: list[dict], cultivos: dict) -> list[dict]:
    """Por año: déficit de la rotación (0-1) y pérdida relativa esperada (0-1).

    Pérdida relativa de rendimiento = Ky x déficit (FAO-33), por ciclo, ponderada por la demanda
    de cada ciclo. Ky desconocido -> 1.0 (neutral) y se declara como vacío.
    """
    out = []
    for anio in anios:
        dem = uso = perdida_pond = 0.0
        completo = True
        for c in ciclos:
            cult = cultivos[c["cultivo"]]
            if not cult.get("kc") or not cult.get("etapas_dias"):
                continue
            r = balance_ciclo(serie, date(anio, c["siembra_mes"], c["siembra_dia"]), cult)
            if r is None:
                completo = False
                break
            d_c, u_c = r
            ky = cult.get("ky") or 1.0
            dem += d_c
            uso += u_c
            perdida_pond += ky * (1 - u_c / d_c) * d_c if d_c > 0 else 0.0
        if completo and dem > 0:
            out.append({"anio": anio, "deficit": 1 - uso / dem, "perdida": min(1.0, perdida_pond / dem)})
    return out


def deficit_por_anio(serie: dict, anios: list[int], ciclos: list[dict], cultivos: dict) -> list[tuple[int, float]]:
    """Déficit de la rotación (0-1) por año."""
    return [(x["anio"], x["deficit"]) for x in balance_rotacion(serie, anios, ciclos, cultivos)]


def ventana_ciclo(c: dict, cultivo: dict) -> tuple[date, date] | None:
    """Inicio y fin del ciclo en un año cualquiera (2001) para calcular meses ocupados."""
    if not cultivo.get("etapas_dias"):
        return None
    ini = date(2001, c["siembra_mes"], c["siembra_dia"])
    return ini, ini + timedelta(days=duracion(cultivo) - 1)


def meses_de(ini: date, fin: date) -> list[int]:
    meses, d = [], date(ini.year, ini.month, 1)
    while d <= fin:
        meses.append(d.month)
        d = date(d.year + (d.month == 12), d.month % 12 + 1, 1)
    return meses


def toca_canicula(c: dict, cultivo: dict) -> bool:
    v = ventana_ciclo(c, cultivo)
    if v is None:
        return False
    (mi, di), (mf, df) = SUPUESTOS["canicula_ini"], SUPUESTOS["canicula_fin"]
    return v[0] <= date(2001, mf, df) and v[1] >= date(2001, mi, di)


def cuartiles(valores: list[float]) -> tuple[float, float, float]:
    if len(valores) < 4:
        m = statistics.median(valores)
        return m, min(valores), max(valores)
    q = statistics.quantiles(valores, n=4, method="inclusive")
    return q[1], q[0], q[2]


def racha_seca(serie: dict, anio: int, umbral: float | None = None) -> int | None:
    umbral = SUPUESTOS["dia_seco_mm"] if umbral is None else umbral
    (mi, di), (mf, df) = SUPUESTOS["canicula_ini"], SUPUESTOS["canicula_fin"]
    d, fin = date(anio, mi, di), date(anio, mf, df)
    mejor = actual = 0
    while d <= fin:
        if d not in serie:
            return None
        if serie[d][0] < umbral:
            actual += 1
            mejor = max(mejor, actual)
        else:
            actual = 0
        d += timedelta(days=1)
    return mejor


def canicula(serie: dict, anios: list[int]) -> dict:
    por_anio = []
    for a in anios:
        r = racha_seca(serie, a)
        if r is not None:
            por_anio.append({"anio": a, "racha_dias": r})
    largas = sum(1 for x in por_anio if x["racha_dias"] > SUPUESTOS["racha_larga_dias"])
    return {
        "ventana": "15 de junio a 31 de agosto",
        "umbral_dia_seco_mm": SUPUESTOS["dia_seco_mm"],
        "umbral_racha_dias": SUPUESTOS["racha_larga_dias"],
        "anios_racha_larga": largas,
        "anios_total": len(por_anio),
        "racha_mediana_dias": statistics.median([x["racha_dias"] for x in por_anio]) if por_anio else 0,
        "por_anio": por_anio,
    }


def anios_completos(diario: dict, desde: int | None = None) -> list[int]:
    desde = SUPUESTOS["anio_inicio"] if desde is None else desde
    cuenta: dict[int, int] = {}
    for d, (p, tx, tn, _g) in diario.items():
        if p is not None and tx is not None and tn is not None:
            cuenta[d.year] = cuenta.get(d.year, 0) + 1
    return sorted(a for a, n in cuenta.items() if n >= 365 and a >= desde)


def resumen(diario: dict, serie_base: dict, anios: list[int], info_lluvia: dict | None = None,
            comparacion: dict | None = None) -> dict:
    """Normales mensuales, lluvia anual, año más seco y canícula (escenario base)."""
    con_chirps = bool(info_lluvia and info_lluvia.get("meses_corregidos"))
    lluvia_mes = {m: [] for m in range(1, 13)}
    et0_mes = {m: [] for m in range(1, 13)}
    tmax_mes = {m: [] for m in range(1, 13)}
    anual = []
    grupos: dict[tuple[int, int], list[date]] = {}
    for d in serie_base:
        grupos.setdefault((d.year, d.month), []).append(d)
    for a in anios:
        tot = 0.0
        for m in range(1, 13):
            dias = grupos.get((a, m), [])
            p = sum(serie_base[d][0] for d in dias)
            e = sum(serie_base[d][1] for d in dias)
            lluvia_mes[m].append(p)
            et0_mes[m].append(e)
            tmax_mes[m].extend(diario[d][1] for d in dias)
            tot += p
        anual.append({"anio": a, "mm": round(tot)})
    seco = min(anual, key=lambda x: x["mm"])
    return {
        "periodo": f"{anios[0]}-{anios[-1]}",
        "resolucion": (("lluvia: CHIRPS v3 (0.05°, ~5 km), diaria en junio-agosto (reparto con NASA IMERG) y "
                        "mensual repartida con los días de POWER el resto del año; " if (info_lluvia or {}).get("dias_chirps_diario")
                        else "lluvia: CHIRPS v3 (0.05°, ~5 km) repartida por días con POWER; ")
                       + "temperatura: POWER (0.5° x 0.625°, ~50 km). Es la zona cercana, no la parcela"
                       if con_chirps else "0.5° x 0.625° (~50 km): es la zona, no la parcela"),
        "fuente_lluvia": (info_lluvia or {}).get("fuente", "NASA POWER"),
        "factor_chirps_mediano": (info_lluvia or {}).get("factor_mediano"),
        "power_vs_chirps": comparacion,
        "lluvia_mensual_normal_mm": [round(statistics.mean(lluvia_mes[m])) for m in range(1, 13)],
        "et0_mensual_normal_mm": [round(statistics.mean(et0_mes[m])) for m in range(1, 13)],
        "tmax_mensual_normal_c": [round(statistics.mean(tmax_mes[m]), 1) for m in range(1, 13)],
        "lluvia_anual_mm": anual,
        "anio_mas_seco": dict(seco),
        "canicula": canicula(serie_base, anios),
        "fuente_ids": ["chirps", "nasa_power", "fao56"] if con_chirps else ["nasa_power", "fao56"],
    }


def gwetroot_jul_ago(diario: dict, desde: int = 2015) -> tuple[float | None, str]:
    vals = [g for d, (_p, _x, _n, g) in diario.items() if d.year >= desde and d.month in (7, 8) and g is not None]
    if not vals:
        return None, "sin datos"
    anios = sorted({d.year for d in diario if d.year >= desde})
    return round(statistics.median(vals), 2), f"{anios[0]}-{anios[-1]}"
