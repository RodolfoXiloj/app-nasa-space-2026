"""Validación del JSON contra el contrato y de los textos (cifras y fechas)."""
from __future__ import annotations

import json
from functools import lru_cache

from motor import datos, redaccion

ESQUEMA = datos.RAIZ / "contracts" / "recomendacion.schema.json"
EJEMPLO = datos.RAIZ / "contracts" / "recomendacion.ejemplo.json"


@lru_cache(maxsize=1)
def esquema() -> dict:
    return json.loads(ESQUEMA.read_text(encoding="utf-8"))


def errores_esquema(res: dict) -> list[str]:
    """Lista de errores de JSON Schema (requiere jsonschema, que solo se usa al exportar y en pruebas)."""
    import jsonschema  # import diferido: el motor no lo necesita para calcular

    v = jsonschema.Draft202012Validator(esquema())
    return [f"{'/'.join(map(str, e.path))}: {e.message}" for e in v.iter_errors(res)]


def textos(res: dict) -> list[tuple[str, str]]:
    """(ruta, texto) de todo lo redactado por el motor."""
    out = [("texto_tarjeta", res["texto_tarjeta"]), ("audio.texto", res["audio"]["texto"])]
    for i, r in enumerate(res["rotaciones"]):
        out.append((f"rotaciones[{i}].por_que", r["por_que"]))
        for campo in ("beneficios", "vacios", "riesgos"):
            out += [(f"rotaciones[{i}].{campo}[{j}]", t) for j, t in enumerate(r[campo])]
    return out


def errores_textos(res: dict) -> list[str]:
    permitidos = redaccion.numeros_permitidos(res)
    citas = [r.get("texto_literal", "") for r in res["zarc"].get("registros", [])]
    if res["zarc"].get("referencia_departamento"):
        citas.append(res["zarc"]["referencia_departamento"]["texto_literal"])
    errores = []
    for ruta, t in textos(res):
        malas = redaccion.validar_numeros(t, permitidos)
        if malas:
            errores.append(f"{ruta}: cifras sin respaldo en el JSON {malas}")
        fechas = redaccion.fechas_no_citadas(t, citas)
        if fechas:
            errores.append(f"{ruta}: fechas o semanas que no vienen de ZARC {fechas}")
    return errores
