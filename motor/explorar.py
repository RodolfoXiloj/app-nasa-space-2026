"""Datos del explorador de Evidence (versión interactiva): un archivo por parcela, aparte del contrato.

    python -m motor.explorar            # todas las parcelas con caché -> web/public/data/explorar/{pid}.json

Sin red. Cada cifra sale de las mismas funciones del motor (motor/clima.py, motor/recomendar.py) y de la
caché con procedencia; la web solo dibuja. El contrato v1 y los JSON de cada parcela no cambian.

Contenido por parcela:
- huellas: el borde o el radio de lo que ve cada producto (motor/huellas.py).
- canicula: día por día del 15 de junio al 31 de agosto de cada año, con el reparto diario de CHIRPS que
  usa el motor ('sat', NASA IMERG) y con el otro ('rnl', ERA5), y la racha seca más larga de cada año.
- lluvia_jul_ago: julio y agosto de 2026, la mediana 1991-2025 y el año más seco antes de 2026 (CHIRPS v3).
- biblioteca: todas las plantillas que aplican (maíz con frijol), con los puntajes del motor en el escenario
  base y la curva de agua del ciclo de primera en un año típico y en el año más difícil.
"""
from __future__ import annotations

import json
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

from motor import clima, datos, deteccion, huellas
from motor import recomendar as rec

DESTINO = datos.RAIZ / "web" / "public" / "data" / "explorar"
CULTIVO = "maiz_frijol"
PASO_DIAS = 5


def _serie(p: dict, carpeta: str, base: str | None = None) -> tuple[dict, list[int]]:
    pid = p["id"]
    power_c = datos.cache(f"power/{pid}_diario.json", base=base, parcela_=p)
    chirps_c = datos.cache(f"chirps/{pid}.json", obligatorio=False, base=base, parcela_=p)
    chirps_d = datos.cache(f"{carpeta}/{pid}.json", obligatorio=False, base=base, parcela_=p)
    diario = clima.preparar(power_c)
    diario, info = clima.corregir_lluvia(diario, chirps_c)
    diario, info = clima.aplicar_chirps_diario(diario, chirps_d, info)
    anios = clima.anios_completos(diario)
    return clima.serie_escenario(diario, p["lat"]), anios


def canicula_dias(serie: dict, anios: list[int]) -> list[dict]:
    """Por año: '1' día seco, '0' día con lluvia, '?' sin dato, del 15 de junio al 31 de agosto."""
    umbral = clima.SUPUESTOS["dia_seco_mm"]
    out = []
    for a in anios:
        d, fin, dias = date(a, *clima.SUPUESTOS["canicula_ini"]), date(a, *clima.SUPUESTOS["canicula_fin"]), []
        while d <= fin:
            dias.append("?" if d not in serie else ("1" if serie[d][0] < umbral else "0"))
            d += timedelta(days=1)
        out.append({"anio": a, "dias": "".join(dias), "racha_dias": clima.racha_seca(serie, a)})
    return out


def curva_ciclo(serie: dict, inicio: date, cultivo: dict) -> dict | None:
    """Agua acumulada del ciclo con el mismo balance que clima.balance_ciclo, un punto cada PASO_DIAS."""
    cap = clima.SUPUESTOS["reserva_suelo_mm"]
    reserva = cap * clima.SUPUESTOS["reserva_inicial"]
    lluvia = demanda = usada = 0.0
    n = clima.duracion(cultivo)
    puntos = []
    for t in range(n):
        d = inicio + timedelta(days=t)
        if d not in serie:
            return None
        p, et0 = serie[d]
        etc = clima.kc_dia(cultivo, t) * et0
        reserva = min(cap, reserva + p * clima.SUPUESTOS["lluvia_efectiva"])
        uso = min(reserva, etc)
        reserva -= uso
        lluvia += p
        demanda += etc
        usada += uso
        if t % PASO_DIAS == 0 or t == n - 1:
            puntos.append([t + 1, round(lluvia, 1), round(demanda, 1), round(usada, 1)])
    return {"puntos": puntos, "demanda_mm": round(demanda, 1), "usada_mm": round(usada, 1),
            "deficit_pct": round(100 * (1 - usada / demanda)) if demanda > 0 else 0}


def _ciclo_principal(rot: dict, cultivos: dict) -> dict | None:
    con_kc = [c for c in rot["ciclos"] if cultivos[c["cultivo"]].get("kc") and cultivos[c["cultivo"]].get("etapas_dias")]
    toca = [c for c in con_kc if clima.toca_canicula(c, cultivos[c["cultivo"]])]
    return (toca or con_kc or [None])[0]


def _curvas(rot: dict, serie: dict, anios: list[int], cultivos: dict) -> dict | None:
    c = _ciclo_principal(rot, cultivos)
    if c is None:
        return None
    cult = cultivos[c["cultivo"]]
    bal = sorted(clima.balance_rotacion(serie, anios, rot["ciclos"], cultivos), key=lambda b: (b["deficit"], b["anio"]))
    if not bal:
        return None
    tipico, dificil = bal[(len(bal) - 1) // 2]["anio"], bal[-1]["anio"]
    a, b, cc, _d = cult["etapas_dias"]
    ini = date(2001, c["siembra_mes"], c["siembra_dia"])
    can_ini = (date(2001, *clima.SUPUESTOS["canicula_ini"]) - ini).days + 1
    can_fin = (date(2001, *clima.SUPUESTOS["canicula_fin"]) - ini).days + 1
    out = {"cultivo": c["cultivo"], "nombre_cultivo": cult["nombre"], "nombre_cultivo_en": (cult.get("en") or {}).get("nombre"),
           "siembra": f"{c['siembra_mes']:02d}-{c['siembra_dia']:02d}", "dias": clima.duracion(cult),
           "etapa_media": [a + b + 1, a + b + cc], "canicula": [max(1, can_ini), can_fin],
           "reserva_suelo_mm": clima.SUPUESTOS["reserva_suelo_mm"],
           "lluvia_efectiva_pct": round(100 * clima.SUPUESTOS["lluvia_efectiva"]), "anios": {}}
    for clave, anio in (("tipico", tipico), ("dificil", dificil)):
        cur = curva_ciclo(serie, date(anio, c["siembra_mes"], c["siembra_dia"]), cult)
        if cur:
            out["anios"][clave] = dict(cur, anio=anio)
    return out


def _texto_yaml(rot: dict, campo: str, idioma: str) -> list[str]:
    if idioma == "es":
        return list(rot.get(campo) or [])
    return list((rot.get("en") or {}).get(campo) or [])


def biblioteca(pid: str, base: str | None = None, res: dict | None = None) -> list[dict]:
    """Todas las plantillas que aplican a maíz con frijol, evaluadas con rec._evaluar en el escenario base."""
    p = datos.parcela(pid, base)
    cultivos = datos.cultivos(base)
    rotaciones = datos.rotaciones(base)
    ndvi_c = datos.cache(f"ndvi/{pid}.json", base=base, parcela_=p)
    firms_c = datos.cache(f"firms/{pid}.json", obligatorio=False, base=base, parcela_=p)
    srtm_c = datos.cache(f"srtm/{pid}.json", obligatorio=False, base=base, parcela_=p)
    det = deteccion.detectar(ndvi_c, firms_c)
    serie, anios = _serie(p, "chirps_diario", base)
    can = clima.canicula(serie, anios)
    ctx = {"cultivos": cultivos, "det": det, "anios": anios, "prioridad": "agua",
           "pendiente_pct": ((srtm_c or {}).get("datos") or {}).get("pendiente_pct")}
    actual = next(r for r in rotaciones if r["tipo"] == "actual" and r.get("cultivo_declarado") == CULTIVO)
    elegidas = {r["id"] for r in (res or {}).get("rotaciones", [])}
    out = []
    for rot in rotaciones:
        if rot["tipo"] == "actual" and rot["id"] != actual["id"]:
            continue
        ev = rec._evaluar(rot, ctx, {(0, 0): (serie, can)}, actual)
        en = rot.get("en") or {}
        out.append({
            "id": rot["id"], "tipo": rot["tipo"], "es_actual": rot["id"] == actual["id"], "elegida": rot["id"] in elegidas,
            "nombre": rot["nombre"], "nombre_en": en.get("nombre"),
            "nombre_corto": rot.get("nombre_corto") or rot["nombre"], "nombre_corto_en": en.get("nombre_corto"),
            "puntajes": {k: ev["puntajes"][k] for k in ("agua", "suelo", "plagas")},
            "deficit": ev["deficit"], "meses_cultivo": sorted(ev["meses_cultivo"]),
            "meses_desnudos": sorted(ev["meses_desnudos"]), "quema": ev["frac_quema"] > 0,
            "toca_canicula": ev["toca_canicula"],
            "beneficios": _texto_yaml(rot, "beneficios", "es"), "beneficios_en": _texto_yaml(rot, "beneficios", "en"),
            "riesgos": _texto_yaml(rot, "riesgos", "es"), "riesgos_en": _texto_yaml(rot, "riesgos", "en"),
            "fuente": rot.get("fuente", ""),
            "curva_agua": _curvas(rot, serie, anios, cultivos),
        })
    return out


def lluvia_jul_ago(pid: str, base: str | None = None) -> dict | None:
    p = datos.parcela(pid, base)
    mensual = datos.cache(f"chirps/{pid}.json", obligatorio=False, base=base, parcela_=p)
    reciente = datos.cache(f"chirps_reciente/{pid}.json", obligatorio=False, base=base, parcela_=p)
    if not mensual or not reciente:
        return None
    por = {(int(a), int(m)): mm for a, m, mm in mensual["datos"]["filas"] if mm is not None}
    anios = sorted({a for a, m in por if 1991 <= a <= 2025 and (a, 7) in por and (a, 8) in por})
    suma = {a: por[(a, 7)] + por[(a, 8)] for a in anios}
    seco = min(anios, key=lambda a: suma[a])
    meses_2026 = reciente["datos"]["meses"]
    return {
        "periodo_referencia": f"{anios[0]}-{anios[-1]}", "n_anios": len(anios),
        "mediana": {"7": round(statistics.median(por[(a, 7)] for a in anios), 1),
                    "8": round(statistics.median(por[(a, 8)] for a in anios), 1)},
        "mediana_jul_ago_mm": round(statistics.median(suma.values()), 1),
        "anio_2026": {"7": round(meses_2026["7"], 1), "8": round(meses_2026["8"], 1)},
        "total_2026_mm": round(meses_2026["7"] + meses_2026["8"], 1),
        "anio_mas_seco": seco, "mas_seco": {"7": round(por[(seco, 7)], 1), "8": round(por[(seco, 8)], 1)},
        "total_mas_seco_mm": round(suma[seco], 1),
        "fuente_id": "chirps",
    }


def explorar_parcela(pid: str, base: str | None = None) -> dict:
    p = datos.parcela(pid, base)
    res = rec.recomendar(pid, cultivo=CULTIVO, base=base)
    radio = res["deteccion"]["quemas"]["radio_m"]
    serie_sat, anios_sat = _serie(p, "chirps_diario", base)
    can = {"ventana": [f"{m:02d}-{d:02d}" for m, d in (clima.SUPUESTOS["canicula_ini"], clima.SUPUESTOS["canicula_fin"])],
           "umbral_dia_seco_mm": clima.SUPUESTOS["dia_seco_mm"], "umbral_racha_dias": clima.SUPUESTOS["racha_larga_dias"],
           "sat": canicula_dias(serie_sat, anios_sat)}
    if datos.cache(f"chirps_diario_rnl/{pid}.json", obligatorio=False, base=base, parcela_=p):
        serie_rnl, anios_rnl = _serie(p, "chirps_diario_rnl", base)
        can["rnl"] = canicula_dias(serie_rnl, anios_rnl)
    return {
        "version": "1", "parcela": pid, "lat": p["lat"], "lon": p["lon"], "generado": res["meta"]["generado"],
        "huellas": huellas.huellas(p["lat"], p["lon"], radio, res["smap"]["disponible"]),
        "canicula": can,
        "lluvia_jul_ago": lluvia_jul_ago(pid, base),
        "biblioteca": biblioteca(pid, base, res),
    }


def main(argv: list[str] | None = None) -> int:
    pids = argv or [p["id"] for p in datos.parcelas()]
    DESTINO.mkdir(parents=True, exist_ok=True)
    for pid in pids:
        try:
            obj = explorar_parcela(pid)
        except FileNotFoundError as e:
            print(f"[explorar] {pid}: sin caché ({e})", file=sys.stderr)
            continue
        ruta = DESTINO / f"{pid}.json"
        ruta.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(f"[explorar] {pid}: {ruta.stat().st_size // 1000} kB")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
