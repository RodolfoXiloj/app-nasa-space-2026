# Milpa Resiliente

**NASA Space Apps Challenge 2026 · Guatemala · reto «Field Shift: Adapting Farms with NASA Data»** · Equipo «A dream»

**Prototipo local de referencia** (decisión del 14 nov 2026): no se entrega ni se publica; funciona en esta computadora y en la red local (`docs/prueba-telefono.md`).

> El satélite ya sabe cómo ha usado su parcela; le mostramos qué rotación aguanta mejor la próxima canícula y por qué, para que el técnico y el agricultor decidan.

Una web con mapa para el extensionista agrícola del Corredor Seco. Para cada parcela:

1. **Lo que ve el satélite**: meses de suelo desnudo y ciclos de cultivo con el NDVI de MODIS (250 m), quemas cercanas con FIRMS (VIIRS 375 m).
2. **Tres rotaciones comparadas**: la actual, la mejor de leguminosa o cobertura y la mejor tolerante a sequía. Cada una trae los 5 campos que pide el reto (por qué, evidencia, beneficios, vacíos de información y riesgos), puntajes de agua, suelo y plagas, confianza con su motivo y un calendario de 12 meses.
3. **Escenarios**: lluvia 0, −10, −20 o −30 % y temperatura +1.5 °C, recalculados en el navegador con valores que ya calculó el motor.
4. **Tarjeta para el agricultor**: se escucha y se imprime o se guarda en PDF.

Apoya, no reemplaza, al técnico ni al agricultor. La fecha de siembra **se cita de ZARC (FAO–MAGA), nunca se calcula**.

## Cómo está hecho

```
parcelas.yaml → pipeline/precargar → data/cache/ → motor/recomendar → motor/exportar → web/public/data → sitio estático
```

- **Estático primero.** La web desplegada no necesita servidor, claves ni red de terceros para mostrar las parcelas. Solo el mapa base (OpenStreetMap) y la imagen Sentinel-2 usan internet; las capas de NASA GIBS están guardadas en el sitio, y sin internet el mapa pasa solo a la capa guardada.
- **Un solo motor en Python puro** (biblioteca estándar + PyYAML), sin red. Devuelve el JSON del contrato `contracts/recomendacion.schema.json`.
- **Caché dentro del repo** (`data/cache/`), cada archivo con su procedencia (URL, fecha de descarga, producto y versión). La red solo se usa con `MILPA_ONLINE=1`.
- **La IA no pone cifras.** Los textos salen de plantillas deterministas; un validador rechaza cualquier número que no esté en el JSON del motor y cualquier fecha de siembra que no venga de ZARC.

| Carpeta | Qué hay | Dueño |
|---|---|---|
| `contracts/` | Esquema del JSON (congelado el 14 nov 2026) y ejemplo | Rodolfo |
| `data/` | Parcelas, rotaciones, cultivos (Kc FAO-56), citas ZARC, glosario, fuentes y caché | Iván (YAML) · Mario (caché) |
| `pipeline/` | Clientes de datos con caché: POWER, ORNL (NDVI), FIRMS, SRTM, SoilGrids | Mario |
| `motor/` | Detección, clima, puntajes, confianza, ZARC, redacción, exportación | Rodolfo |
| `web/` | Vite + React + react-leaflet + Recharts | Team |
| `tests/` | Contrato, validador de números, ZARC, motor con datos sintéticos | Todos |
| `docs/` | Estado, decisiones, uso de IA | Todos |

## Uso

Requisitos: Python 3.11+ y Node 20+.

```bash
pip install -r requirements.txt

# 1. Bajar datos (solo con red). Sin claves: POWER, ORNL (NDVI), FIRMS por país, CHIRPS v3, SRTM, SoilGrids, GIBS.
MILPA_ONLINE=1 python -m pipeline.precargar                     # POWER, SRTM, FIRMS, suelo y NDVI 2001-2025 (lento)
MILPA_ONLINE=1 python -m pipeline.clientes.chirps               # lluvia CHIRPS v3 mensual 1991-2025, lectura por rangos
MILPA_ONLINE=1 python -m pipeline.clientes.chirps --diario      # CHIRPS v3 diario junio-agosto (canícula), reparto con NASA IMERG
MILPA_ONLINE=1 python -m pipeline.clientes.firms --reciente 2026  # quemas 2026: necesita FIRMS_MAP_KEY en .env
MILPA_ONLINE=1 python -m pipeline.clientes.appeears_smap todo   # SMAP: necesita EARTHDATA_USERNAME y _PASSWORD
MILPA_ONLINE=1 python -m pipeline.capas                         # teselas de GIBS para el mapa sin red

# Elegir y revisar puntos agrícolas
MILPA_ONLINE=1 python -m pipeline.elegir_punto jocotan --km 6
MILPA_ONLINE=1 python -m pipeline.imagen_punto 14.81146 -89.39433 revisar.png

# 2. Validación (sin red): POWER contra CHIRPS y sequía de 2018 -> web/public/data/validacion.json
python -m pipeline.validacion.validar

# 3. Motor y exportación a la web (sin red)
python -m motor.exportar                                        # agregue --audio (con red) para los mp3 con edge-tts

# 4. Pruebas
python -m pytest

# 5. Web
cd web
npm install
npm run dev        # desarrollo
npm run build      # sitio estático en web/dist
npm run smoke      # renderiza cada componente con cada JSON exportado; exige la etiqueta de IA de cada mp3
npm run sin-red    # tras el build: la web en Edge sin acceso a internet (5 parcelas, audio, mapa, PDF)
```

En PowerShell, en vez de `MILPA_ONLINE=1 python ...` use `$env:MILPA_ONLINE='1'; python ...`.

Las claves (`FIRMS_MAP_KEY`, `EARTHDATA_USERNAME`, `EARTHDATA_PASSWORD`) van en un `.env` local copiado de `.env.example`, que está en `.gitignore`. El pipeline las lee sin imprimirlas. El motor y el sitio desplegado no necesitan ninguna.

## Documentación del equipo

- `docs/estado.md`: qué funciona, qué es respaldo y qué falta.
- `docs/pruebas.md`: registro de cada prueba con comando, resultado y hora.
- `docs/memoria/`: decisiones, hallazgos y fuentes en notas estilo Obsidian con `[[enlaces]]`. Empiece por `Inicio.md`.
- `graphify-out/GRAPH_REPORT.md` y `graph.json`: grafo del código, se regenera con `graphify update .`.
- `docs/uso-ia.md`: uso de IA declarado.

## Fuentes

Todas las fuentes, con su cita, están en `data/fuentes.yaml` y en la pestaña «Glosario y fuentes» de la web: MODIS MOD13Q1 (vía ORNL DAAC), FIRMS VIIRS, NASA POWER, SRTM, NASA GIBS, SMAP (cliente listo, datos pendientes), SoilGrids, CHIRPS v3 (lluvia del motor y validación), Sentinel-2 cloudless (revisión de puntos), FAO-56 y FAO-33, ZARC (FAO–MAGA) y OpenStreetMap.

## Estado

Ver `docs/estado.md`: qué funciona, qué es respaldo o ejemplo y qué falta.

## Licencia

MIT, ver `LICENSE`. Los datos conservan la licencia y la cita de su fuente.
