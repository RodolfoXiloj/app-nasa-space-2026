"""Une todo: datos cacheados -> detección -> clima -> puntajes -> selección -> confianza -> ZARC
-> textos -> JSON del contrato (contracts/recomendacion.schema.json).

Uso:
    from motor.recomendar import recomendar
    res = recomendar("jocotan", cultivo="maiz_frijol", prioridad="agua")
"""
from __future__ import annotations

from datetime import datetime, timezone

from motor import VERSION, VERSION_CONTRATO, clima, confianza, datos, deteccion, puntaje, redaccion, zarc

LLUVIA_PCT = [0, -10, -20, -30]
TEMP_C = [0, 1.5]
CAMPOS_RETO = ("por_que", "evidencia", "beneficios", "vacios", "riesgos")


class ContratoIncompleto(ValueError):
    """A una rotación le falta alguno de los 5 campos que pide el reto."""


def id_escenario(lluvia: float, temp: float) -> str:
    return f"lluvia_{lluvia:g}_temp_{temp:g}"


def _fecha_cache(c: dict | None) -> str | None:
    return (c or {}).get("procedencia", {}).get("fecha_descarga")


def _meses_cultivo(rot: dict, cultivos: dict) -> dict[int, str]:
    """{mes: nombre del cultivo} para los ciclos con duración conocida."""
    out: dict[int, str] = {}
    for c in rot["ciclos"]:
        cult = cultivos[c["cultivo"]]
        v = clima.ventana_ciclo(c, cult)
        if not v:
            continue
        nombre = cult["nombre"] + "".join(f" + {cultivos[a]['nombre']}" for a in c.get("asociados", []))
        for m in clima.meses_de(*v):
            out.setdefault(m, nombre)
    return out


def _evaluar(rot: dict, ctx: dict, series: dict, actual_rot: dict | None) -> dict:
    """Puntajes de una rotación en todos los escenarios + datos para los textos."""
    cult = ctx["cultivos"]
    det = ctx["det"]
    meses_c = _meses_cultivo(rot, cult)
    poca_det = det.get("meses_poca_cobertura", [])
    if rot["tipo"] == "actual":
        meses_desn = list(det["meses_desnudos"])
        meses_poca = list(poca_det)
        frac_quema = (det["quemas"]["anios_con_quema"] / det["quemas"]["anios_observados"]
                      if det["quemas"]["anios_observados"] else 0.0)
    else:
        meses_act = set(_meses_cultivo(actual_rot, cult)) if actual_rot else set()
        cubre = set(rot.get("cubre_meses") or []) | (set(meses_c) - meses_act)
        meses_desn = [m for m in det["meses_desnudos"] if m not in cubre]
        meses_poca = [m for m in poca_det if m not in cubre]
        frac_quema = 0.0 if rot.get("quema") is False else frac_quema_actual(det)
    toca = [c for c in rot["ciclos"] if clima.toca_canicula(c, cult[c["cultivo"]])]
    ky_can = max([(cult[c["cultivo"]].get("ky") or 1.0) for c in toca], default=0.0)

    suelo_v, traza_suelo = puntaje.puntaje_suelo(len(meses_desn), ctx["pendiente_pct"], frac_quema, rot, len(meses_poca))
    plagas_v, traza_plagas = puntaje.puntaje_plagas(rot, cult)

    por_esc = {}
    base = None
    for (ll, tt), (serie, can) in series.items():
        bal = clima.balance_rotacion(serie, ctx["anios"], rot["ciclos"], cult)
        frac_can = can["anios_racha_larga"] / can["anios_total"] if can["anios_total"] else 0.0
        agua_v, deficit, traza_agua = puntaje.puntaje_agua(bal, frac_can, ky_can)
        perd = sorted(b["perdida"] for b in bal)
        deficit["perdida_mediana_pct"] = round(100 * clima.cuartiles(perd)[0])
        p = {"agua": agua_v, "suelo": suelo_v, "plagas": plagas_v}
        p["total"] = puntaje.total(p, ctx["prioridad"])
        por_esc[id_escenario(ll, tt)] = {"puntajes": p, "deficit": deficit, "traza_agua": traza_agua}
        if ll == 0 and tt == 0:
            base = por_esc[id_escenario(ll, tt)]
    assert base is not None
    return {
        "rot": rot, "meses_cultivo": meses_c, "meses_desnudos": meses_desn, "n_desnudos": len(meses_desn),
        "meses_poca": meses_poca, "n_poca": len(meses_poca),
        "frac_quema": frac_quema, "toca_canicula": bool(toca), "puntajes": base["puntajes"], "deficit": base["deficit"],
        "trazabilidad": {"agua": base["traza_agua"], "suelo": traza_suelo, "plagas": traza_plagas},
        "escenarios": por_esc,
    }


def frac_quema_actual(det: dict) -> float:
    q = det["quemas"]
    return q["anios_con_quema"] / q["anios_observados"] if q["anios_observados"] else 0.0


def _calendario(ev: dict, det: dict, es_actual: bool, clima_res: dict) -> list[dict]:
    rot = ev["rot"]
    cubre = set(rot.get("cubre_meses") or [])
    quema_meses = set(det["quemas"]["meses_con_quema"]) if es_actual else set()
    can = clima_res["canicula"]
    out = []
    for m in range(1, 13):
        alertas = []
        cultivo = ev["meses_cultivo"].get(m)
        if cultivo:
            estado = "cultivo"
            if m in det["meses_desnudos"] and es_actual:
                alertas.append("El satélite ve poco verde: siembra reciente o cultivo ralo.")
            if m in (7, 8) and ev["toca_canicula"] and can["anios_racha_larga"]:
                alertas.append("Canícula: vigile la racha seca.")
        elif m in quema_meses:
            estado = "quema"
            alertas.append("Quema cercana detectada por VIIRS en este mes.")
        elif m in cubre:
            estado = "cobertura" if rot.get("cobertura") else "rastrojo"
        elif m in ev["meses_desnudos"]:
            estado = "desnudo"
            alertas.append("Suelo desnudo: expuesto al sol y a la erosión.")
        else:
            estado = "rastrojo"
            if m in ev.get("meses_poca", []):
                alertas.append("Poca cobertura: el satélite ve el suelo casi descubierto.")
        out.append({"mes": m, "estado": estado, "cultivo": cultivo, "alertas": alertas})
    return out


def _evidencia(ev: dict, ctx: dict, es_actual: bool) -> list[dict]:
    det, cl = ctx["det"], ctx["clima"]
    q = det["quemas"]
    e = []
    e.append({"dato": "Meses de suelo desnudo" + (" detectados" if es_actual else " esperados con esta práctica"),
              "valor": ev["n_desnudos"], "unidad": "meses", "fuente": "MODIS MOD13Q1 (NDVI) vía ORNL DAAC",
              "fuente_id": "modis_mod13q1", "resolucion": "250 m", "periodo": det["periodo"]})
    e.append({"dato": "Meses con poca cobertura" + ("" if es_actual else " esperados con esta práctica"),
              "valor": ev["n_poca"], "unidad": "meses", "fuente": "MODIS MOD13Q1 (NDVI) vía ORNL DAAC",
              "fuente_id": "modis_mod13q1", "resolucion": "250 m", "periodo": det["periodo"]})
    if es_actual:
        e.append({"dato": "Ciclos de verdor por año (mediana)", "valor": det["ciclos"]["mediana"], "unidad": "ciclos",
                  "fuente": "MODIS MOD13Q1 (NDVI) vía ORNL DAAC", "fuente_id": "modis_mod13q1", "resolucion": "250 m",
                  "periodo": det["periodo"]})
        e.append({"dato": f"Años con quema a {int(q['radio_m'])} m o menos (enero-mayo)", "valor": q["anios_con_quema"],
                  "unidad": f"de {q['anios_observados']} años", "fuente": "FIRMS VIIRS S-NPP", "fuente_id": "firms_viirs",
                  "resolucion": "375 m", "periodo": q["periodo"]})
        e.append({"dato": "Compuestos NDVI válidos", "valor": det["calidad"]["pct_validos"], "unidad": "%",
                  "fuente": "MODIS MOD13Q1 pixel_reliability", "fuente_id": "modis_mod13q1", "resolucion": "250 m",
                  "periodo": det["periodo"]})
    e.append({"dato": "Déficit de agua mediano del ciclo", "valor": ev["deficit"]["mediana_pct"], "unidad": "%",
              "fuente": ("CHIRPS (lluvia) + NASA POWER (temperatura) + ET0 Hargreaves y Kc (FAO-56)"
                         if ctx["con_chirps"] else "NASA POWER + ET0 Hargreaves y Kc (FAO-56)"),
              "fuente_id": "chirps" if ctx["con_chirps"] else "nasa_power",
              "resolucion": "~5 km (lluvia), ~50 km (temperatura)" if ctx["con_chirps"] else "~50 km",
              "periodo": cl["periodo"]})
    e.append({"dato": "Pérdida de cosecha esperada por falta de agua (mediana, Ky x déficit)",
              "valor": ev["deficit"]["perdida_mediana_pct"], "unidad": "%", "fuente": ("CHIRPS + NASA POWER + FAO-33" if ctx["con_chirps"] else "NASA POWER + FAO-33"),
              "fuente_id": "fao33", "resolucion": "~50 km", "periodo": cl["periodo"]})
    can = cl["canicula"]
    e.append({"dato": f"Años con canícula de más de {can['umbral_racha_dias']} días secos", "valor": can["anios_racha_larga"],
              "unidad": f"de {can['anios_total']} años", "fuente": ("NASA POWER diario reescalado con CHIRPS mensual" if ctx["con_chirps"] else "NASA POWER diario"),
              "fuente_id": "nasa_power",
              "resolucion": "~50 km", "periodo": cl["periodo"]})
    if ctx["pendiente_pct"] is not None:
        e.append({"dato": "Pendiente del terreno", "valor": ctx["pendiente_pct"], "unidad": "%", "fuente": "SRTM 90 m",
                  "fuente_id": "srtm", "resolucion": "90 m", "periodo": None})
    if es_actual and ctx["smap"]["disponible"]:
        s = ctx["smap"]
        e.append({"dato": "Humedad del suelo julio-agosto (SMAP, mediana)", "valor": s["humedad_jul_ago_m3m3"],
                  "unidad": "m3/m3", "fuente": "SMAP L3 mejorado (SPL3SMP_E) vía AppEEARS", "fuente_id": "smap",
                  "resolucion": "9 km", "periodo": s["periodo"]})
    cmp_ = (cl.get("power_vs_chirps") or {}).get("jul_ago")
    if es_actual and cmp_ and cmp_.get("sesgo_pct") is not None:
        e.append({"dato": "Diferencia de lluvia julio-agosto: POWER frente a CHIRPS", "valor": cmp_["sesgo_pct"],
                  "unidad": "%", "fuente": "NASA POWER y CHIRPS v3", "fuente_id": "chirps",
                  "resolucion": "~50 km y ~5 km", "periodo": cl["power_vs_chirps"]["periodo"]})
    suelo = ctx.get("suelo") or {}
    if es_actual and suelo.get("disponible") and suelo.get("arcilla_pct") is not None:
        e.append({"dato": "Arcilla del suelo (0-5 cm)", "valor": suelo["arcilla_pct"], "unidad": "%",
                  "fuente": "SoilGrids 2.0 (ISRIC)", "fuente_id": "soilgrids", "resolucion": "250 m", "periodo": None})
    if es_actual and ctx["smap"]["respaldo"]:
        r = ctx["smap"]["respaldo"]
        e.append({"dato": "Humedad de raíz julio-agosto (modelo, no SMAP)", "valor": r["jul_ago_mediana"],
                  "unidad": r["unidad"], "fuente": "NASA POWER GWETROOT (MERRA-2)", "fuente_id": "nasa_power",
                  "resolucion": "~50 km", "periodo": r["periodo"]})
    return e


def _ciclos_contrato(rot: dict, cultivos: dict) -> list[dict]:
    out = []
    for c in rot["ciclos"]:
        cult = cultivos[c["cultivo"]]
        v = clima.ventana_ciclo(c, cult)
        out.append({"temporada": c["temporada"],
                    "cultivos": [cult["nombre"]] + [cultivos[a]["nombre"] for a in c.get("asociados", [])],
                    "meses": clima.meses_de(*v) if v else [], "siembra_mes_supuesto": c["siembra_mes"],
                    "duracion_dias": clima.duracion(cult) if cult.get("etapas_dias") else 0})
    return out


def verificar_campos_reto(res: dict) -> None:
    """La exportación falla si a una rotación le falta alguno de los 5 campos del reto."""
    for r in res["rotaciones"]:
        for k in CAMPOS_RETO:
            v = r.get(k)
            if not v or (isinstance(v, list) and not all(v)):
                raise ContratoIncompleto(f"La rotación {r.get('id')} no tiene '{k}'")


def recomendar(pid: str, cultivo: str = "maiz_frijol", prioridad: str = "agua", base: str | None = None) -> dict:
    p = datos.parcela(pid, base)
    cultivos = datos.cultivos(base)
    rotaciones = datos.rotaciones(base)

    # ---- caché
    ndvi_c = datos.cache(f"ndvi/{pid}.json", base=base, parcela_=p)
    power_c = datos.cache(f"power/{pid}_diario.json", base=base, parcela_=p)
    firms_c = datos.cache(f"firms/{pid}.json", obligatorio=False, base=base, parcela_=p)
    srtm_c = datos.cache(f"srtm/{pid}.json", obligatorio=False, base=base, parcela_=p)
    suelo_c = datos.cache(f"suelo/{pid}.json", obligatorio=False, base=base, parcela_=p)
    chirps_c = datos.cache(f"chirps/{pid}.json", obligatorio=False, base=base, parcela_=p)
    smap_c = datos.cache(f"smap/{pid}.json", obligatorio=False, base=base, parcela_=p)

    # ---- paso 1: satélite
    det = deteccion.detectar(ndvi_c, firms_c)

    # ---- paso 2: clima en todos los escenarios
    diario_power = clima.preparar(power_c)
    diario, info_lluvia = clima.corregir_lluvia(diario_power, chirps_c)
    chirps_d = datos.cache(f"chirps_diario/{pid}.json", obligatorio=False, base=base, parcela_=p)
    diario, info_lluvia = clima.aplicar_chirps_diario(diario, chirps_d, info_lluvia)
    anios = clima.anios_completos(diario)
    series = {}
    for ll in LLUVIA_PCT:
        for tt in TEMP_C:
            s = clima.serie_escenario(diario, p["lat"], ll, tt)
            series[(ll, tt)] = (s, clima.canicula(s, anios))
    comparacion = clima.comparar(diario_power, chirps_c, anios[0], anios[-1])
    clima_res = clima.resumen(diario, series[(0, 0)][0], anios, info_lluvia, comparacion)
    con_chirps = bool(info_lluvia.get("meses_corregidos"))

    gw, gw_periodo = clima.gwetroot_jul_ago(diario)
    smap_d = (smap_c or {}).get("datos", {})
    hay_smap = smap_d.get("jul_ago_mediana") is not None
    motivo_smap = None if hay_smap else (smap_d.get("motivo") or
                                         "Sin SMAP numérico todavía: falta la descarga por AppEEARS.")
    smap_res = {
        "disponible": hay_smap,
        "fuente_id": "smap" if hay_smap else None,
        "humedad_jul_ago_m3m3": (smap_c or {}).get("datos", {}).get("jul_ago_mediana") if hay_smap else None,
        "percentil": (smap_c or {}).get("datos", {}).get("percentil") if hay_smap else None,
        "anio_ultimo": smap_d.get("anio_ultimo") if hay_smap else None,
        # puesto del último año entre los años con SMAP, de menor a mayor humedad (1 = el más seco)
        "puesto_ultimo": (sorted(smap_d["por_anio_jul_ago"].values()).index(
            smap_d["por_anio_jul_ago"][str(smap_d["anio_ultimo"])]) + 1) if hay_smap and smap_d.get("por_anio_jul_ago") else None,
        "n_anios": len(smap_d.get("por_anio_jul_ago") or {}) if hay_smap else None,
        "mediciones_sin_calidad_recomendada": smap_d.get("mediciones_sin_calidad_recomendada"),
        "periodo": (smap_c or {}).get("datos", {}).get("periodo") if hay_smap else None,
        "respaldo": None if hay_smap else {
            "variable": "GWETROOT", "etiqueta": "modelo MERRA-2 vía NASA POWER, no es SMAP",
            "jul_ago_mediana": gw, "unidad": "fracción 0-1", "periodo": gw_periodo, "fuente_id": "nasa_power"},
        "nota": ("SMAP SPL3SMP_E por AppEEARS." if hay_smap else
                 motivo_smap + " Se muestra la humedad de raíz del modelo MERRA-2 rotulada como modelo."),
    }

    terreno = (srtm_c or {}).get("datos", {})
    pendiente = terreno.get("pendiente_pct")
    # ---- suelo
    suelo_d = (suelo_c or {}).get("datos", {}).get("por_profundidad", {}).get("0-5cm", {})
    suelo = {"disponible": bool(suelo_d), "arcilla_pct": suelo_d.get("arcilla_pct"),
             "carbono_organico_g_kg": suelo_d.get("carbono_organico_g_kg"), "ph": suelo_d.get("ph"),
             "profundidad": "0-5 cm", "fuente_id": "soilgrids" if suelo_d else None,
             "nota": ((suelo_c or {}).get("procedencia", {}).get("nota") or "SoilGrids 2.0") if suelo_d
             else "Sin datos de suelo: la API de SoilGrids no respondió. Vacío de información."}
    ctx = {"cultivos": cultivos, "det": det, "clima": clima_res, "anios": anios, "prioridad": prioridad,
           "con_chirps": con_chirps, "suelo": suelo,
           "pendiente_pct": pendiente, "smap": smap_res, "hay_smap": hay_smap,
           "smap_sin_calidad": bool(smap_c) and not hay_smap}

    # ---- puntajes y selección
    actual_rot = next((r for r in rotaciones if r["tipo"] == "actual" and r.get("cultivo_declarado") == cultivo), None)
    if actual_rot is None:
        raise ValueError(f"No hay plantilla 'actual' para el cultivo {cultivo!r} en data/rotaciones.yaml")
    evals = {r["id"]: _evaluar(r, ctx, series, actual_rot) for r in rotaciones
             if r["tipo"] != "actual" or r["id"] == actual_rot["id"]}
    ev_act = evals[actual_rot["id"]]
    elegidas = [ev_act]
    for tipo in ("leguminosa_cobertura", "tolerante_sequia"):
        cands = [e for e in evals.values() if e["rot"]["tipo"] == tipo]
        if not cands:
            raise ValueError(f"No hay plantillas de tipo {tipo}")
        elegidas.append(max(cands, key=lambda e: (e["puntajes"]["total"], e["puntajes"]["agua"])))

    # ---- confianza (común a la parcela; extras por rotación)
    dif = ((comparacion or {}).get("jul_ago") or {}).get("sesgo_pct")
    zarc_res = zarc.buscar(datos.zarc(base), p["municipio"],
                           [(c["cultivo"].split("_")[0], c["temporada"]) for c in actual_rot["ciclos"]],
                           departamento=p.get("departamento"))

    # Regla 5.1 (fijada antes de ver el resultado): si la prueba de 2018 no encontró señal en 3 o más
    # parcelas, la confianza de las recomendaciones de agua baja a «baja».
    val = datos.cache("validacion/resumen.json", obligatorio=False, base=base)
    r51 = ((val or {}).get("datos") or {}).get("regla_5_1") or {}
    regla_2018 = (f"La prueba de la sequía de 2018 solo mostró señal en {r51['parcelas_con_senal_2018']} parcelas "
                  f"(se pedían {r51['minimo']}): regla 5.1 del plan") if r51.get("se_activa") else None
    ciclos_decl = len(actual_rot["ciclos"])
    ciclos_vistos = det["ciclos"]["mediana"]
    id_seco = id_escenario(min(LLUVIA_PCT), max(TEMP_C))
    rot_out = []
    for ev in elegidas:
        rot = ev["rot"]
        es_actual = rot["tipo"] == "actual"
        sin_ky = sorted({cultivos[c["cultivo"]]["nombre"] for c in rot["ciclos"] if cultivos[c["cultivo"]].get("ky") is None})
        seco = {"lluvia_pct": min(LLUVIA_PCT), "temp_c": max(TEMP_C),
                "alt": ev["escenarios"][id_seco]["deficit"]["mediana_pct"],
                "act": ev_act["escenarios"][id_seco]["deficit"]["mediana_pct"]}
        tctx = dict(ctx, ev=ev, ev_actual=ev_act, es_actual=es_actual, cultivos_sin_ky=sin_ky, escenario_seco=seco,
                    ciclos_discrepan=(ciclos_vistos is not None and ciclos_vistos != ciclos_decl))
        extras = []
        if "supuesto" in str(rot.get("fuente", "")):
            extras.append("Reglas de la opción sin revisar por un agrónomo")
        conf = confianza.evaluar(det["calidad"]["pct_validos"], dif, hay_smap, extras, forzar_baja=regla_2018,
                                 detalle_smap=ctx["smap"]["nota"].split(" Se muestra")[0] if not hay_smap else None)
        rot_out.append({
            "id": rot["id"], "nombre": rot["nombre"], "tipo": rot["tipo"], "es_actual": es_actual,
            "descripcion": rot.get("fuente", ""),
            "ciclos": _ciclos_contrato(rot, cultivos),
            "por_que": redaccion.por_que(rot["tipo"], tctx),
            "evidencia": _evidencia(ev, ctx, es_actual),
            "beneficios": redaccion.beneficios(rot, tctx),
            "vacios": redaccion.vacios(rot, tctx),
            "riesgos": redaccion.riesgos(rot, tctx),
            "puntajes": ev["puntajes"],
            "deficit": ev["deficit"],
            "confianza": conf,
            "calendario": _calendario(ev, det, es_actual, clima_res),
            "trazabilidad": ev["trazabilidad"],
        })

    # ---- escenarios
    lista = []
    for ll in LLUVIA_PCT:
        for tt in TEMP_C:
            eid = id_escenario(ll, tt)
            lista.append({
                "id": eid, "lluvia_pct": ll, "temp_c": tt,
                "canicula_anios_racha_larga": series[(ll, tt)][1]["anios_racha_larga"],
                "rotaciones": {ev["rot"]["id"]: {"puntajes": ev["escenarios"][eid]["puntajes"],
                                                 "deficit_mediano_pct": ev["escenarios"][eid]["deficit"]["mediana_pct"]}
                               for ev in elegidas},
            })


    # ---- fuentes con fecha de consulta
    fechas = {"nasa_power": _fecha_cache(power_c), "modis_mod13q1": _fecha_cache(ndvi_c),
              "ornl_subsets": _fecha_cache(ndvi_c), "firms_viirs": _fecha_cache(firms_c),
              "srtm": _fecha_cache(srtm_c), "soilgrids": _fecha_cache(suelo_c), "chirps": _fecha_cache(chirps_c),
              "smap": _fecha_cache(smap_c)}
    fuentes = [dict(f, fecha_consulta=fechas.get(f["id"])) for f in datos.fuentes(base)]

    pendientes = []
    if not hay_smap:
        pendientes.append("SMAP: se muestra el respaldo GWETROOT de POWER (modelo MERRA-2, no SMAP)")
    if dif is None:
        pendientes.append("CHIRPS: aún sin comparar con POWER; la confianza no pasa de media")
    if con_chirps:
        if info_lluvia.get("dias_chirps_diario"):
            pendientes.append("Lluvia diaria: junio-agosto con CHIRPS v3 diario (péntadas repartidas con NASA IMERG); "
                              "resto del año, totales mensuales de CHIRPS repartidos con los días de POWER")
        else:
            pendientes.append("Lluvia diaria: totales mensuales de CHIRPS repartidos con los días de POWER (CHIRPS diario pendiente)")
    if not suelo_d:
        pendientes.append("Suelo: sin datos de SoilGrids")
    if not zarc_res["encontrado"]:
        pendientes.append("ZARC: sin cita para este municipio; se remite al extensionista")
    if any("supuesto" in str(e["rot"].get("fuente", "")) for e in elegidas):
        pendientes.append("Rotaciones: plantillas iniciales sin revisión agronómica")
    if 2026 not in ((firms_c or {}).get("datos", {}).get("anios_observados") or []):
        pendientes.append("FIRMS 2026: sin datos del año en curso; se usan años completos 2012-2025")
    if p.get("provisional"):
        pendientes.append("Coordenada provisional: falta validar que el píxel sea agrícola")

    res = {
        "version_contrato": VERSION_CONTRATO,
        "meta": {"tipo": "calculado", "generado": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                 "motor_version": VERSION, "nota": "Salida del motor con datos cacheados en data/cache/",
                 "datos_de_ejemplo": pendientes},
        "aviso": redaccion.AVISO,
        "parcela": {"id": p["id"], "nombre": p["nombre"], "municipio": p["municipio"], "departamento": p["departamento"],
                    "lat": p["lat"], "lon": p["lon"], "provisional": bool(p.get("provisional")), "nota": p.get("nota", ""),
                    "cultivo_declarado": cultivo, "prioridad": prioridad,
                    "terreno": {"altitud_m": terreno.get("altitud_m"), "pendiente_pct": pendiente, "fuente_id": "srtm"},
                    "suelo": suelo},
        "deteccion": det,
        "clima": clima_res,
        "smap": smap_res,
        "rotaciones": rot_out,
        "zarc": zarc_res,
        "escenarios": {"base": id_escenario(0, 0), "lluvia_pct": LLUVIA_PCT, "temp_c": TEMP_C, "lista": lista},
        "pesos": {"prioridad": prioridad, "por_prioridad": puntaje.PESOS},
        "fuentes": fuentes,
        "glosario": datos.glosario(base),
        "texto_tarjeta": "",
        "audio": {"mp3": None, "voz": None, "texto": ""},
    }
    res["texto_tarjeta"] = redaccion.texto_tarjeta(res)
    res["audio"]["texto"] = res["texto_tarjeta"]
    verificar_campos_reto(res)
    return res
