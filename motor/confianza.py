"""Confianza alta, media o baja, siempre con su motivo (plan, 4.5).

- Alta: >= 80 % de compuestos NDVI válidos, POWER y CHIRPS difieren < 15 % en julio-agosto, y hay SMAP.
- Media: falla una de las tres.
- Baja: < 60 % de compuestos válidos, diferencia > 30 %, o sin SMAP.
Toda afirmación que dependa solo de POWER no pasa de media: si no hay comparación con CHIRPS,
ese criterio cuenta como fallado.

Cada detalle va en español (`detalle`, `motivo`) y en inglés (`detalle_en`, `motivo_en`), con las mismas
cifras: la web muestra el motivo en los dos idiomas (por ejemplo, en el bloque gris de las opciones).
"""
from __future__ import annotations

UMBRALES = {"validos_alta": 80.0, "validos_baja": 60.0, "dif_alta": 15.0, "dif_baja": 30.0}


def evaluar(pct_validos: float, dif_power_chirps_pct: float | None, hay_smap: bool,
            extras: list[str] | None = None, forzar_baja: str | None = None,
            detalle_smap: str | None = None, extras_en: list[str] | None = None,
            forzar_baja_en: str | None = None, detalle_smap_en: str | None = None) -> dict:
    """`forzar_baja`: motivo para bajar a «baja» sin importar lo demás (regla 5.1 de la validación).
    `detalle_smap`: por qué no hay SMAP (por ejemplo, la celda no tiene datos de calidad recomendada).
    Los parámetros `*_en` son los mismos textos en inglés; si faltan, se repite el texto en español."""
    u = UMBRALES
    if dif_power_chirps_pct is None:
        dif_es = "Aún sin comparar con CHIRPS: la lluvia viene solo de POWER (celda de ~50 km)"
        dif_en = "Not yet compared with CHIRPS: rain comes only from POWER (~50 km cell)"
    else:
        dif_es = f"POWER se desvía {abs(dif_power_chirps_pct)} % de CHIRPS (se pide menos de {u['dif_alta']:.0f} %)"
        dif_en = f"POWER differs {abs(dif_power_chirps_pct)} % from CHIRPS (less than {u['dif_alta']:.0f} % required)"
    if hay_smap:
        smap_es, smap_en = "Hay SMAP numérico", "Numeric SMAP data available"
    else:
        smap_es = (detalle_smap or "Sin SMAP numérico todavía: falta la descarga por AppEEARS").rstrip(".")
        smap_en = (detalle_smap_en or ("No numeric SMAP yet: the AppEEARS download is missing"
                                       if not detalle_smap else smap_es)).rstrip(".")
    criterios = [
        {"criterio": "Calidad del píxel MODIS", "cumple": pct_validos >= u["validos_alta"],
         "detalle": f"{pct_validos} % de compuestos NDVI válidos (se pide {u['validos_alta']:.0f} % o más)",
         "detalle_en": f"{pct_validos} % of NDVI composites are valid ({u['validos_alta']:.0f} % or more required)"},
        {"criterio": "Lluvia POWER contra CHIRPS en julio-agosto",
         "cumple": None if dif_power_chirps_pct is None else abs(dif_power_chirps_pct) < u["dif_alta"],
         "detalle": dif_es, "detalle_en": dif_en},
        {"criterio": "Humedad del suelo SMAP", "cumple": hay_smap, "detalle": smap_es, "detalle_en": smap_en},
    ]
    fallas = [c for c in criterios if c["cumple"] is not True]
    baja = (pct_validos < u["validos_baja"]
            or (dif_power_chirps_pct is not None and abs(dif_power_chirps_pct) > u["dif_baja"])
            or not hay_smap)
    if forzar_baja:
        criterios.append({"criterio": "Prueba de la sequía de 2018", "cumple": False, "detalle": forzar_baja,
                          "detalle_en": forzar_baja_en or forzar_baja})
        fallas.append(criterios[-1])
    if baja or forzar_baja or len(fallas) >= 2:
        nivel = "baja"
    elif len(fallas) == 1:
        nivel = "media"
    else:
        nivel = "alta"
    motivos = [c["detalle"] for c in fallas] or ["Las tres comprobaciones se cumplen"]
    motivos += extras or []
    motivos_en = [c["detalle_en"] for c in fallas] or ["All three checks pass"]
    motivos_en += extras_en if extras_en is not None else (extras or [])
    return {"nivel": nivel, "motivo": ". ".join(motivos) + ".", "motivo_en": ". ".join(motivos_en) + ".",
            "criterios": criterios}
