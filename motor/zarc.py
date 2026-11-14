"""ZARC se CITA, nunca se calcula (plan, 4.4).

El motor solo busca por municipio, cultivo y temporada en data/zarc_citas.yaml y copia el texto
literal. No hace aritmética con fechas y el escenario no cambia la cita.
"""
from __future__ import annotations

NOTA_ESCENARIO = "La fecha de ZARC no cambia con el escenario; consulte la versión vigente."
SIN_REGISTRO = "Fecha de siembra: consúltela en ZARC (FAO–MAGA) con su extensionista."


def _norm(s: str) -> str:
    return (s.lower().replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o")
            .replace("ú", "u").strip())


def buscar(zarc_yaml: dict, municipio: str, pares: list[tuple[str, str]], departamento: str | None = None) -> dict:
    """pares = [(cultivo, temporada)] de la rotación actual. Devuelve el bloque `zarc` del contrato."""
    registros = []
    for cultivo, temporada in pares:
        for r in zarc_yaml.get("registros") or []:
            if (_norm(r["municipio"]) == _norm(municipio) and _norm(r["cultivo"]) == _norm(cultivo)
                    and _norm(r["temporada"]) == _norm(temporada)):
                registros.append(r)
    enlace = zarc_yaml.get("enlace_general", "")
    if not registros:
        out = {"encontrado": False, "texto": SIN_REGISTRO, "enlace": enlace, "nota_escenario": NOTA_ESCENARIO,
               "registros": []}
        ref = next((r for r in zarc_yaml.get("referencias_departamento") or []
                    if departamento and _norm(departamento) in [_norm(d) for d in r["departamentos"]]), None)
        if ref:
            out["texto"] = (SIN_REGISTRO + f" Referencia publicada para el departamento (no es la ventana del municipio): "
                            f"«{ref['texto_literal']}» ({ref['fuente']}).")
            out["referencia_departamento"] = ref
        return out
    partes = [f"Siembra recomendada según ZARC ({r['institucion']}, {r['anio']}), {r['cultivo']} de {r['temporada']}: "
              f"«{r['texto_literal']}»" for r in registros]
    return {"encontrado": True, "texto": " ".join(partes), "enlace": registros[0].get("url") or enlace,
            "nota_escenario": NOTA_ESCENARIO, "registros": registros}
