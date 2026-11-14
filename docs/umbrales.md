# Umbrales del semáforo de 3 hechos: CONFIRMADOS

**Estado: Confirmado por Rodolfo, sáb 14 nov.** Se confirmó la propuesta tal cual: gris por hecho, empate si dos opciones difieren 3 puntos o menos, Olopa con las tres opciones sin orden, y las palabras «Bien», «Atención» y «Se repite» ("Good", "Watch", "Repeats"). El motor los aplica desde `data/umbrales_semaforo.yaml` y `motor/farmer.py`, con `farmer.umbrales.estado` en `"confirmado"`. Aplicarlos no cambió ningún puntaje: al regenerar los JSON de las 5 parcelas, los totales siguen iguales.

Escrita el sábado 14 nov 2026. Todas las cifras salen de `data/cache/`: se corrió `motor.recomendar.recomendar()` en memoria para las 5 parcelas (maíz con frijol, prioridad agua), sin escribir archivos. Coinciden con los JSON de `web/public/data/`.

**Aviso de honestidad:** estos cortes se proponen después de ver los conteos de las 5 parcelas, no antes. Se declara así en la web y en las slides. El agrónomo los revisa (`docs/es/revision-plan.md`, sección 3.2).

## Qué mide el semáforo

Tres hechos observados, no un riesgo ni un pronóstico. El semáforo **no usa el puntaje total**: los totales van de 73 a 92 y casi todo saldría verde.

| Hecho | Qué cuenta | Fuente y período | Regla del motor que ya existe |
|---|---|---|---|
| Suelo | Meses con NDVI mediano < 0.35 (suelo desnudo) y meses de 0.35 a 0.45 (poca cobertura) | MODIS MOD13Q1, 250 m, 2021-2025 | `motor/deteccion.py` → `UMBRALES` |
| Quema | Años con al menos un foco VIIRS de confianza nominal o alta a 500 m o menos, de enero a mayo | FIRMS VIIRS S-NPP, 375 m, 2012-2026 (15 años; de 2026 solo cuenta enero-mayo, del producto estándar de S-NPP) | `motor/deteccion.py` → `detectar_quemas` |
| Canícula | Años con una racha de más de 15 días con menos de 2 mm por día, del 15 jun al 31 ago | CHIRPS v3 diario (reparto con IMERG), 2001-2025 (25 años) | `motor/clima.py` → `SUPUESTOS` |

## Los conteos reales

| Parcela | Suelo desnudo (de 12 meses) | Poca cobertura | Quema (de 15 años) | Canícula larga (de 25 años) | Compuestos NDVI válidos | Confianza |
|---|---|---|---|---|---|---|
| Jocotán | 2 (mar, abr) | 2 (feb, may) | 3 | 2 | 95.7 % | alta |
| Camotán | 0 | 2 (mar, abr) | 3 | 2 | 80.9 % | baja: la celda de SMAP no tiene dato de calidad recomendada |
| Olopa | 0 | 2 (mar, abr) | 1 | 0 | 93.0 % | media: POWER se desvía 22.1 % de CHIRPS |
| San Juan Ermita | 3 (feb, mar, abr) | 2 (ene, may) | 2 | 1 | 95.7 % | alta |
| Zacapa | 1 (abr) | 4 (ene, feb, mar, may) | 0 | 3 | 93.9 % | baja: POWER se desvía 55.4 % de CHIRPS |

## Propuesta de umbrales

| Hecho | Verde | Amarillo | Rojo | Gris |
|---|---|---|---|---|
| Suelo | 0 meses desnudos y 0 de poca cobertura | 1 mes desnudo, o 0 desnudos con algún mes de poca cobertura | 2 meses desnudos o más | Menos de 60 % de compuestos NDVI válidos, o algún mes sin mediana |
| Quema | 0 años | 1 o 2 años | 3 años o más | Sin datos de FIRMS (0 años observados) |
| Canícula | 0 años | 1 o 2 años | 3 años o más | La lluvia de junio-agosto no viene de CHIRPS diario (solo POWER) |

### Por qué cada cifra

- **Suelo, rojo con 2 meses desnudos o más.**
  - Usa sin cambios los umbrales de NDVI de `motor/deteccion.py` (0.35 y 0.45), calibrados antes de la prueba de 2018 y escritos en `docs/validacion.md`.
  - Un solo mes por debajo de 0.35 puede ser el paso entre cosecha y siembra; dos o más ya son suelo descubierto durante buena parte de la época seca. Es un supuesto del equipo que revisa el agrónomo.
  - «Poca cobertura» sola da amarillo y no rojo: en el puntaje de suelo pesa la mitad que un mes desnudo (`motor/puntaje.py`, 3 puntos frente a 6), y en ladera el píxel de 250 m mezcla la milpa con árboles.
- **Quema, rojo con 3 años o más de 15.**
  - 3 de 15 es 1 de cada 5 años: quema en años distintos, no un solo evento.
  - Uno o dos años pueden ser una quema vecina: el radio de 500 m y el píxel de 375 m de VIIRS incluyen terreno de al lado.
  - El verde dice «no se vio quema», no «no hubo quema»: VIIRS pasa pocas veces al día y no ve quemas breves o bajo nubes (nota de `detectar_quemas`).
  - De 2026 solo cuenta enero-mayo, del producto estándar de Suomi NPP. Todos los datos de FIRMS del registro son de Suomi NPP.
- **Canícula, rojo con 3 años o más de 25.**
  - El mismo corte que la quema, para que la regla se explique igual: «en tres años distintos o más».
  - La racha de más de 15 días y el día seco de 2 mm son los del plan (`motor/clima.py`). No se recalibraron.
  - El día seco (menos de 2 mm) y la racha de más de 15 días son decisiones del equipo, no una definición oficial. Como referencia, CONRED describe la canícula con una duración de 5 a 10 días en promedio (https://conred.gob.gt/que-es-la-canicula/); FEWS NET informó de 11 a 20 días seguidos sin lluvia en 2026 (https://fews.net/es/latin-america-and-caribbean/guatemala/actualizacion-de-la-perspectiva-de-seguridad-alimentaria/agosto-2026) y Oxfam, un promedio de 25 en 2019 (https://reliefweb.int/attachments/017ed79d-0dfa-3d24-a502-3474f5d9ddb7/Informe%20d%C3%A9fict%20de%20lluvias%202019.pdf).
  - El semáforo usa el registro observado (escenario base), no los escenarios de −10 a −30 %.
- **Gris, por hecho y no por parcela.** Cada hecho se pone gris solo si falla su propia fuente:
  - Suelo: el corte de 60 % de compuestos válidos es el que ya usa `motor/confianza.py` para la confianza baja.
  - Quema: sin datos de FIRMS no se puede decir nada.
  - Canícula: POWER es una celda de ~50 km y en julio-agosto se desvía de CHIRPS entre −22.1 % y +55.4 % en estas parcelas (`docs/validacion.md`).
  - Con los datos de hoy ningún hecho sale gris.

### Lo que daría con los datos de hoy

| Parcela | Suelo | Quema | Canícula |
|---|---|---|---|
| Jocotán | rojo (2) | rojo (3) | amarillo (2) |
| Camotán | amarillo (0 y 2 de poca cobertura) | rojo (3) | amarillo (2) |
| Olopa | amarillo (0 y 2 de poca cobertura) | amarillo (1) | verde (0) |
| San Juan Ermita | rojo (3) | amarillo (2) | amarillo (1) |
| Zacapa | amarillo (1) | verde (0) | rojo (3) |

Las 5 parcelas quedan distintas entre sí, que es lo que el puntaje total no logra.

## Los 4 estados

| Estado | Forma | Palabra (es / en) | Qué dice |
|---|---|---|---|
| Verde | Círculo | «Bien» / "Good" | El satélite no vio el problema en el período |
| Amarillo | Triángulo | «Atención» / "Watch" | Lo vio poco: un mes o uno o dos años |
| Rojo | Cuadrado | «Se repite» / "Repeats" | Lo vio seguido: dos meses o más, o tres años o más |
| Gris | Signo de interrogación, borde punteado | «El satélite no ve bien aquí» / "The satellite can't see well here" | Faltan datos de esa fuente; no se adivina |

- Nunca solo color: forma, palabra, ícono y posición fija (suelo, quema, canícula, siempre en ese orden).
- La vista evita el anaranjado y la palabra «alerta», para que no se confunda con los niveles de alerta públicos de CONRED (verde, amarillo, anaranjado y rojo; https://conred.gob.gt/conozca-los-niveles-de-alerta-y-su-significado/); cada estado lleva además una forma y una palabra, así que nunca depende solo del color. El esquema rechaza cualquier estado fuera de estos 4.
- La vista y el audio dicen: «esto no es una alerta oficial; hable con su técnico».

## Regla de empate (opciones)

**Propuesta: si dos opciones difieren 3 puntos o menos en el total, no hay ganadora.** La vista dice «dos opciones para platicar con su técnico» y las muestra sin orden.

El motor aplica el margen en cadena (`motor/farmer.py` → `empatadas`): se parte de la opción con el total más alto y entra al grupo empatado toda opción a 3 puntos o menos de alguna que ya está en él. Por eso en Olopa (87, 90 y 92) las tres quedan parejas.

Por qué 3 puntos:

1. **3 puntos son uno o dos meses de suelo desnudo.** Con prioridad agua (la de la web), cada mes desnudo resta 1.5 puntos del total, o 2.25 si la pendiente pasa de 15 % (6 o 9 puntos de suelo × 25 %, `motor/puntaje.py`). Es una diferencia del tamaño de uno o dos meses medidos en un píxel de 250 m que mezcla la parcela con lo de al lado. Además, los totales se redondean a enteros.
2. **Los escenarios ya mueven la diferencia hasta 3 puntos.** Entre las dos alternativas, en los 8 escenarios:
   - Jocotán va de 0 a 2.
   - Camotán, de 0 a 1.
   - Olopa, de −2 a −1.
   - San Juan Ermita, de 1 a 3.
   - En Zacapa el orden se invierte, de +1 a −2.

Con los datos de hoy (escenario base):

| Parcela | Actual | Leguminosa o cobertura | Tolerante a sequía | Diferencia entre alternativas | Resultado |
|---|---|---|---|---|---|
| Jocotán | 80 | 88 | 87 | 1 | empate |
| Camotán | 84 | 90 | 89 | 1 | empate (y confianza baja) |
| Olopa | 87 | 90 | 92 | 2 | empate; la de leguminosa también empata con la actual (3) |
| San Juan Ermita | 80 | 88 | 86 | 2 | empate |
| Zacapa | 73 | 81 | 80 | 1 | empate (y confianza baja) |

- En las 5 parcelas las dos alternativas quedan empatadas entre sí.
- La regla también se aplica entre una alternativa y la práctica actual. Las alternativas superan a la actual por 5 a 8 puntos, salvo en Olopa: maíz con canavalia (90) queda a 3 puntos de la práctica actual (87), así que empata con ella. En Olopa la vista diría que la práctica actual y la canavalia quedan parejas, y que el maíz de ciclo corto ICTA B-5 (92) también queda parejo con la canavalia.
- **Confianza baja (Camotán y Zacapa):** el bloque de opciones va en gris, con el motivo. Los 3 hechos no se ponen grises, porque su confianza baja viene de SMAP o de la lluvia de POWER, que ninguno de los 3 hechos usa.

## Lo que Rodolfo decide

1. Confirmar o cambiar los cortes de la tabla «Propuesta de umbrales».
2. Gris por hecho (esta propuesta) o gris para toda la parcela con confianza baja (la idea del plan). Con la segunda opción, Camotán y Zacapa quedarían con los 3 hechos en gris.
3. Confirmar el margen de empate de 3 puntos.
4. Cómo mostrar Olopa: ahí el empate no es transitivo. La canavalia empata con la práctica actual y con el maíz ICTA B-5, pero el B-5 supera a la actual por 5 puntos. Propuesta: mostrar las tres sin orden y decir que ninguna se separa lo suficiente.
5. Las palabras de cada estado («Bien», «Atención», «Se repite») son un borrador; Iván las revisa con la prueba de comprensión.

Después de confirmar, el carril A pasa estos valores al motor (`farmer.umbrales.estado = "confirmado"`), regenera los datos y corre la prueba de regresión.
