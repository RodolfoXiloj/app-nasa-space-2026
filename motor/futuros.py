"""Las 3 rotaciones de cada parcela probadas en los futuros de NASA (NEX-GDDP-CMIP6, 2041-2060).

    python -m motor.futuros              # escribe web/public/data/futuros_nasa.json

Para cada modelo, el cambio de lluvia (%) y de temperatura (°C) que proyecta para la parcela se aplica
a la serie diaria observada, igual que los escenarios fijos del motor (clima.serie_escenario), y se
recalcula el balance de agua de cada rotación con las mismas reglas.

Una rotación «aguanta» en un futuro si su puntaje de agua en ese futuro es igual o mayor que el de la
rotación actual con el clima de hoy: deja a la familia igual o mejor que ahora en agua.

No toca el contrato ni la tarjeta: es un archivo aparte que la web lee si existe.
"""
from __future__ import annotations

import json
import statistics
import sys
from datetime import datetime, timezone

from motor import datos
from motor.recomendar import id_escenario, recomendar

SALIDA = datos.RAIZ / "web" / "public" / "data" / "futuros_nasa.json"
ESCENARIOS = {"ssp245": "Emisiones intermedias (SSP2-4.5)", "ssp585": "Emisiones altas (SSP5-8.5)"}


def _cuantil(xs: list[float], q: float) -> float:
    xs = sorted(xs)
    i = (len(xs) - 1) * q
    lo, hi = int(i), min(int(i) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (i - lo)


def futuros_parcela(pid: str, cambios: dict, cultivo: str = "maiz_frijol", prioridad: str = "agua",
                    base: str | None = None) -> dict:
    pares = sorted({(round(m["lluvia_pct"], 1), round(m["temp_c"], 1)) for lista in cambios.values() for m in lista})
    res = recomendar(pid, cultivo=cultivo, prioridad=prioridad, base=base, escenarios_extra=pares)
    extra = res["escenarios_extra"]
    actual = next(r for r in res["rotaciones"] if r["es_actual"])
    agua_hoy = actual["puntajes"]["agua"]

    out = {"agua_actual_hoy": agua_hoy, "escenarios": {}}
    for esc, lista in cambios.items():
        modelos, por_rot = [], {r["id"]: {"aguanta": 0, "agua": [], "deficit": []} for r in res["rotaciones"]}
        for m in lista:
            e = extra[id_escenario(round(m["lluvia_pct"], 1), round(m["temp_c"], 1))]
            fila = dict(m, aguanta={})
            for rid, v in e["rotaciones"].items():
                ok = v["puntajes"]["agua"] >= agua_hoy
                por_rot[rid]["aguanta"] += ok
                por_rot[rid]["agua"].append(v["puntajes"]["agua"])
                por_rot[rid]["deficit"].append(v["deficit_mediano_pct"])
                fila["aguanta"][rid] = ok
            modelos.append(fila)
        lluvias = [m["lluvia_pct"] for m in lista]
        canic = [m["lluvia_canicula_pct"] for m in lista]
        temps = [m["temp_c"] for m in lista]
        out["escenarios"][esc] = {
            "nombre": ESCENARIOS.get(esc, esc),
            "n_modelos": len(lista),
            "lluvia_pct": {"mediana": round(statistics.median(lluvias), 1),
                           "p10": round(_cuantil(lluvias, 0.1), 1), "p90": round(_cuantil(lluvias, 0.9), 1)},
            "lluvia_canicula_pct": {"mediana": round(statistics.median(canic), 1),
                                    "p10": round(_cuantil(canic, 0.1), 1), "p90": round(_cuantil(canic, 0.9), 1)},
            "temp_c": {"mediana": round(statistics.median(temps), 1),
                       "p10": round(_cuantil(temps, 0.1), 1), "p90": round(_cuantil(temps, 0.9), 1)},
            "modelos_mas_secos": sum(1 for x in lluvias if x < 0),
            "rotaciones": [{
                "id": r["id"], "nombre": r["nombre"], "nombre_en": (r.get("en") or {}).get("nombre"), "es_actual": r["es_actual"],
                "futuros_que_aguanta": por_rot[r["id"]]["aguanta"],
                "agua_mediana": round(statistics.median(por_rot[r["id"]]["agua"])),
                "deficit_mediano_pct": round(statistics.median(por_rot[r["id"]]["deficit"])),
            } for r in res["rotaciones"]],
            "modelos": modelos,
        }
    return out


def main() -> int:
    c = datos.cache("cmip6/cambios.json", obligatorio=False)
    if not c:
        print("Falta data/cache/cmip6/cambios.json: corra pipeline/gee/cmip6_cambios.js en Earth Engine y "
              "luego python -m pipeline.clientes.cmip6 <csv>")
        return 1
    parcelas = {}
    for pid, cambios in c["datos"]["parcelas"].items():
        try:
            parcelas[pid] = futuros_parcela(pid, cambios)
        except datos.FaltaDato as e:
            print(f"{pid}: sin datos ({e})")
    obj = {
        "generado": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "fuente": c["procedencia"],
        "periodo_base": c["datos"]["periodo_base"], "periodo_futuro": c["datos"]["periodo_futuro"],
        "regla_aguanta": "puntaje de agua en ese futuro igual o mayor que el de la rotación actual con el clima de hoy",
        "parcelas": parcelas,
    }
    SALIDA.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    for pid, d in parcelas.items():
        resumen = {e: {r["id"]: f"{r['futuros_que_aguanta']}/{v['n_modelos']}" for r in v["rotaciones"]}
                   for e, v in d["escenarios"].items()}
        print(pid, resumen)
    return 0


if __name__ == "__main__":
    sys.exit(main())
