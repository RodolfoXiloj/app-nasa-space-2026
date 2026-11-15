// Textos del explorador de Evidence (versión interactiva). Llegan con Evidence, no con la primera pantalla.
// Las cifras no viven aquí: vienen de data/explorar/{pid}.json (python -m motor.explorar) y de futuros_nasa.json.
import { useMemo } from 'react'
import { useLocale } from './useT.js'

const en = {
  huellas: {
    titulo: 'What each satellite sees',
    intro:
      'Around the selected plot: an average family plot and the cell or radius each product measures. The tool describes this land around the plot, not the plot.',
    mostrar: 'Show the outlines on the map',
    recorrido: 'From the plot to the satellite',
    detener: 'Stop',
    ver: 'Zoom to it',
    nombres: {
      parcela: 'Average family plot in the Dry Corridor (0.35 ha, FAO/WFP 2010), drawn as a circle: a size reference, not the boundary',
      modis: 'MODIS pixel (“250 m”: {lado} m a side): bare soil and plant cover',
      firms: 'Fire radius: detections within {r} m count',
      chirps: 'CHIRPS cell (0.05°): the rain',
      smap: 'SMAP cell (9 km): surface soil moisture',
      power: 'NASA POWER cell (0.5° × 0.625°): temperature and evaporation',
    },
    sinSmap: 'no recommended-quality data in this cell',
    lista: 'Outlines as a list ({n})',
  },
  capas: {
    opacidad: 'NDVI layer opacity',
    comparar: 'Compare dry and rainy season',
    compararAgosto: 'Compare mid-August 2025 and 2026',
    izquierdaAgosto: '2025: NDVI from {fecha}',
    derechaAgosto: '2026: NDVI from {fecha}',
    notaAgosto:
      'Same 16-day composite (from 13 August) in two years. In 2026 July and August had 20 % to 26 % of normal rain at the five plots. Paler means less green; clouds and the 16-day composite also change the picture: a preliminary observation, not proof of crop loss.',
    cerrarComparar: 'Close the comparison',
    izquierda: 'Dry season: NDVI of {fecha}',
    derecha: 'Rainy season: NDVI of {fecha}',
    divisor: 'Move the divider between the two dates',
    nota: 'MODIS NDVI, 16-day composites at 250 m, stored in the site: the landscape of the area, not the plot. Green: more plant cover; brown: less.',
  },
  nube: {
    titulo: 'Each NASA model, one dot',
    sub:
      'Change in May–October rain and in mean temperature for {futuro} against {base}. Filled circle: the option keeps today’s water score in that future. Cross: it does not.',
    rotacion: 'Option',
    ejeX: 'Rain change, May–October (%)',
    ejeY: 'Temperature change (°C)',
    resumen: '{rot}: holds in {k} of {n} models ({esc}).',
    tabla: 'Models as a table',
    modelo: 'Model',
    lluvia: 'Rain May–Oct',
    lluviaCan: 'Rain Jun–Aug',
    temp: 'Temperature',
    aguanta: 'Holds',
    mediana: 'median',
    si: 'yes',
    no: 'no',
  },
  curva: {
    titulo: 'The water of the primera cycle, added up day by day',
    sub:
      '{cultivo}, sown on {fecha}, {dias} days. Blue: rain. Brown: water the crop asks for (FAO-56). Green: water the crop could take from the soil in the engine’s water balance. The gap between brown and green is the deficit.',
    opcion: 'Option',
    tipico: 'Typical year ({anio})',
    dificil: 'Hardest year ({anio})',
    resumen: 'In {anio}, the crop asked for {demanda} mm and could take {usada} mm: deficit {deficit} %.',
    lluvia: 'Rain',
    demanda: 'Water asked for',
    usada: 'Water taken',
    deficit: 'Deficit',
    dia: 'Day {d}',
    ejeX: 'Days after sowing',
    canicula: 'Canícula',
    etapa: 'Flowering and grain fill',
    leyendaBandas: 'Shaded bands: the canícula (15 June to 31 August) and the mid-season stage of the crop (FAO-56), when it flowers and fills the grain.',
    nota:
      'Typical year: the year with the median deficit for this option, 2001–2025. Hardest: the year with the largest deficit. Same balance as the scores (motor/clima.py); only the primera cycle is drawn.',
    porQue:
      'Why can it rain more than the crop asks for and still leave a deficit? In the engine the soil holds up to {reserva} mm and {efectiva} % of the rain counts: a heavy rain overflows, and in a dry spell the soil empties.',
    sinCurva: 'No water curve for this option: its crop has no FAO-56 crop coefficient.',
  },
  canicula: {
    titulo: 'The canícula day by day, 2001–2025',
    sub:
      'Each row is a year, from 15 June to 31 August. Dark square: a dry day (under {mm} mm). A thick outline marks a year with a dry spell longer than {dias} days.',
    reparto: 'Daily split of CHIRPS',
    sat: 'NASA IMERG (used by the engine)',
    rnl: 'ERA5 (comparison)',
    resumen: '{k} of {n} years with a dry spell longer than {dias} days ({reparto}).',
    satCorto: 'NASA IMERG split',
    rnlCorto: 'ERA5 split',
    anio: '{anio}: longest dry spell {racha} days',
    nota:
      'Both splits share the same CHIRPS 5-day totals and only change which day the rain falls on. The engine uses IMERG; ERA5 is shown to see how much the count depends on that choice.',
    tabla: 'Years as a list',
    seco: 'Dry day',
    lluvia: 'Day with rain',
  },
  lluvia: {
    titulo: 'July and August: 2026 against other years',
    anio2026: '2026',
    mediana: 'Median {periodo}',
    seco: 'Driest before 2026 ({anio})',
    julio: 'July',
    agosto: 'August',
    resumen: 'July and August rain: 2026, {t26} mm; median {periodo}, {med} mm; {anio}, {seco} mm.',
    nota: '2026 is a preliminary observation and does not enter the scores. CHIRPS v3, final monthly product.',
  },
  biblioteca: {
    titulo: 'Try another option from the library',
    sub:
      'For the extension worker: every template that fits maize with beans, with the engine’s scores in the base scenario (no rain or temperature change) and the priority chosen above. The farmer view keeps three options.',
    elegir: 'Template',
    hoy: 'Today',
    enOpciones: 'Shown in the options',
    agua: 'Water',
    suelo: 'Soil',
    plagas: 'Pests',
    total: 'Total',
    deficit: 'Median deficit',
    meses: 'Months with a crop',
    desnudos: 'Bare months left',
    ninguno: 'none',
    quema: 'Burning',
    conQuema: 'yes',
    sinQuema: 'no',
    beneficios: 'Benefits',
    riesgos: 'Risks',
    comparada: 'Next to what they do today',
    fuente: 'Source',
    revision: 'Rules not yet reviewed by an agronomist.',
  },
  ligero: {
    activo: 'Light version: no large layers or 3D view.',
    activar: 'Light version',
    desactivar: 'Full version',
  },
}

const es = {
  huellas: {
    titulo: 'Lo que ve cada satélite',
    intro:
      'Alrededor de la parcela elegida: una parcela familiar promedio y la celda o el radio que mide cada producto. La herramienta describe esta tierra alrededor de la parcela, no la parcela.',
    mostrar: 'Mostrar los bordes en el mapa',
    recorrido: 'De la parcela al satélite',
    detener: 'Detener',
    ver: 'Acercar',
    nombres: {
      parcela: 'Parcela familiar promedio del Corredor Seco (0.35 ha, FAO/PMA 2010), dibujada como un círculo: una referencia de tamaño, no el lindero',
      modis: 'Píxel de MODIS («250 m»: {lado} m de lado): suelo desnudo y cobertura',
      firms: 'Radio de quema: cuentan las detecciones a menos de {r} m',
      chirps: 'Celda de CHIRPS (0.05°): la lluvia',
      smap: 'Celda de SMAP (9 km): humedad del suelo en superficie',
      power: 'Celda de NASA POWER (0.5° × 0.625°): temperatura y evaporación',
    },
    sinSmap: 'sin datos de calidad recomendada en esta celda',
    lista: 'Los bordes en una lista ({n})',
  },
  capas: {
    opacidad: 'Opacidad de las capas NDVI',
    comparar: 'Comparar época seca y época de lluvias',
    compararAgosto: 'Comparar mediados de agosto de 2025 y 2026',
    izquierdaAgosto: '2025: NDVI desde el {fecha}',
    derechaAgosto: '2026: NDVI desde el {fecha}',
    notaAgosto:
      'El mismo compuesto de 16 días (desde el 13 de agosto) en dos años. En 2026 julio y agosto tuvieron entre el 20 % y el 26 % de la lluvia normal en las cinco parcelas. Más pálido es menos verde; las nubes y el compuesto de 16 días también cambian la imagen: es una observación preliminar, no prueba de pérdida de cosecha.',
    cerrarComparar: 'Cerrar la comparación',
    izquierda: 'Época seca: NDVI del {fecha}',
    derecha: 'Época de lluvias: NDVI del {fecha}',
    divisor: 'Mover la división entre las dos fechas',
    nota: 'NDVI de MODIS, compuestos de 16 días a 250 m, guardados en el sitio: el paisaje de la zona, no la parcela. Verde: más cobertura; café: menos.',
  },
  nube: {
    titulo: 'Cada modelo de NASA, un punto',
    sub:
      'Cambio de la lluvia de mayo a octubre y de la temperatura media en {futuro} frente a {base}. Círculo lleno: la opción mantiene su puntaje de agua de hoy en ese futuro. Cruz: no lo mantiene.',
    rotacion: 'Opción',
    ejeX: 'Cambio de lluvia, mayo-octubre (%)',
    ejeY: 'Cambio de temperatura (°C)',
    resumen: '{rot}: aguanta en {k} de {n} modelos ({esc}).',
    tabla: 'Los modelos en una tabla',
    modelo: 'Modelo',
    lluvia: 'Lluvia may-oct',
    lluviaCan: 'Lluvia jun-ago',
    temp: 'Temperatura',
    aguanta: 'Aguanta',
    mediana: 'mediana',
    si: 'sí',
    no: 'no',
  },
  curva: {
    titulo: 'El agua del ciclo de primera, sumada día a día',
    sub:
      '{cultivo}, sembrado el {fecha}, {dias} días. Azul: la lluvia. Café: el agua que pide el cultivo (FAO-56). Verde: el agua que el cultivo pudo tomar del suelo en el balance del motor. La distancia entre el café y el verde es el déficit.',
    opcion: 'Opción',
    tipico: 'Año típico ({anio})',
    dificil: 'Año más difícil ({anio})',
    resumen: 'En {anio}, el cultivo pidió {demanda} mm y pudo tomar {usada} mm: déficit de {deficit} %.',
    lluvia: 'Lluvia',
    demanda: 'Agua que pide',
    usada: 'Agua que tomó',
    deficit: 'Déficit',
    dia: 'Día {d}',
    ejeX: 'Días después de la siembra',
    canicula: 'Canícula',
    etapa: 'Floración y llenado',
    leyendaBandas: 'Franjas sombreadas: la canícula (15 de junio a 31 de agosto) y la etapa media del cultivo (FAO-56), cuando florece y llena el grano.',
    nota:
      'Año típico: el del déficit mediano de esta opción, 2001-2025. Más difícil: el de mayor déficit. Es el mismo balance de los puntajes (motor/clima.py); solo se dibuja el ciclo de primera.',
    porQue:
      '¿Por qué puede llover más de lo que pide el cultivo y aun así faltar agua? En el motor el suelo guarda hasta {reserva} mm y cuenta el {efectiva} % de la lluvia: un aguacero rebalsa y en una racha seca el suelo se vacía.',
    sinCurva: 'Esta opción no tiene curva de agua: su cultivo no tiene coeficiente de cultivo en FAO-56.',
  },
  canicula: {
    titulo: 'La canícula día por día, 2001-2025',
    sub:
      'Cada fila es un año, del 15 de junio al 31 de agosto. Cuadro oscuro: un día seco (menos de {mm} mm). El borde grueso marca un año con una racha seca de más de {dias} días.',
    reparto: 'Reparto diario de CHIRPS',
    sat: 'NASA IMERG (el que usa el motor)',
    rnl: 'ERA5 (para comparar)',
    resumen: '{k} de {n} años con una racha seca de más de {dias} días ({reparto}).',
    satCorto: 'reparto con NASA IMERG',
    rnlCorto: 'reparto con ERA5',
    anio: '{anio}: racha seca más larga de {racha} días',
    nota:
      'Los dos repartos usan los mismos totales de 5 días de CHIRPS y solo cambian el día en que cae la lluvia. El motor usa IMERG; ERA5 se muestra para ver cuánto depende el conteo de esa elección.',
    tabla: 'Los años en una lista',
    seco: 'Día seco',
    lluvia: 'Día con lluvia',
  },
  lluvia: {
    titulo: 'Julio y agosto: 2026 frente a otros años',
    anio2026: '2026',
    mediana: 'Mediana {periodo}',
    seco: 'El más seco antes de 2026 ({anio})',
    julio: 'Julio',
    agosto: 'Agosto',
    resumen: 'Lluvia de julio y agosto: 2026, {t26} mm; mediana {periodo}, {med} mm; {anio}, {seco} mm.',
    nota: '2026 es una observación preliminar y no entra en los puntajes. CHIRPS v3, producto mensual final.',
  },
  biblioteca: {
    titulo: 'Probar otra opción de la biblioteca',
    sub:
      'Para el extensionista: todas las plantillas que sirven para maíz con frijol, con los puntajes del motor en el escenario base (sin cambio de lluvia ni de temperatura) y la prioridad elegida arriba. La vista del agricultor se queda con tres opciones.',
    elegir: 'Plantilla',
    hoy: 'Hoy',
    enOpciones: 'Sale en las opciones',
    agua: 'Agua',
    suelo: 'Suelo',
    plagas: 'Plagas',
    total: 'Total',
    deficit: 'Déficit mediano',
    meses: 'Meses con cultivo',
    desnudos: 'Meses que quedan desnudos',
    ninguno: 'ninguno',
    quema: 'Quema',
    conQuema: 'sí',
    sinQuema: 'no',
    beneficios: 'Beneficios',
    riesgos: 'Riesgos',
    comparada: 'Junto a lo que hace hoy',
    fuente: 'Fuente',
    revision: 'Reglas sin revisar por un agrónomo.',
  },
  ligero: {
    activo: 'Versión ligera: sin capas grandes ni vista 3D.',
    activar: 'Versión ligera',
    desactivar: 'Versión completa',
  },
}

const DIC = { en, es }

function leer(obj, ruta) {
  return ruta.split('.').reduce((o, k) => (o == null ? undefined : o[k]), obj)
}

export function useTx() {
  const loc = useLocale()
  return useMemo(() => {
    const d = DIC[loc] || en
    const tx = (clave, vars) => {
      const s = leer(d, clave) ?? leer(en, clave) ?? clave
      return vars && typeof s === 'string' ? s.replace(/\{(\w+)\}/g, (_, k) => (vars[k] != null ? String(vars[k]) : `{${k}}`)) : s
    }
    tx.loc = loc
    tx.num = (x, dec = 0) => Number(x).toLocaleString(loc === 'es' ? 'es-GT' : 'en-US', { maximumFractionDigits: dec, minimumFractionDigits: 0 })
    return tx
  }, [loc])
}
