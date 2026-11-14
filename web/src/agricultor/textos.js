// Textos de la vista «Para el agricultor», en inglés (en) y español (es). Las dos ramas tienen las
// mismas claves. Las cifras nunca van escritas aquí: llegan del bloque `farmer` del JSON y se
// insertan con las funciones de abajo.

// El idioma activo vive en web/src/i18n/store.js (uno solo para toda la web, inglés por defecto).
export const IDIOMAS = ['en', 'es']
export const NOMBRE_IDIOMA = { en: 'English', es: 'Español' }

const MESES = {
  en: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
    'November', 'December'],
  es: ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre',
    'noviembre', 'diciembre'],
}

// Nombres propios de las fuentes de cada hecho; iguales en los dos idiomas.
export const FUENTES = {
  modis_mod13q1: 'MODIS (NASA)',
  firms_viirs: 'VIIRS (NASA FIRMS)',
  chirps_diario: 'CHIRPS',
  chirps: 'CHIRPS',
  imerg: 'IMERG (NASA)',
  power_diario: 'NASA POWER',
}

function unir(items, y) {
  if (items.length <= 1) return items.join('')
  if (items.length === 2) return `${items[0]} ${y} ${items[1]}`
  return `${items.slice(0, -1).join(', ')}${y === 'and' ? ',' : ''} ${y} ${items[items.length - 1]}`
}

function meses(idioma, ms) {
  return unir([...ms].sort((a, b) => a - b).map((m) => MESES[idioma][m - 1]), idioma === 'en' ? 'and' : 'y')
}

// Guion que no se parte: «2012‑2026» queda en una sola línea.
const periodoEntero = (p) => String(p).replace(/-/g, '‑')

function fuentes(idioma, ids) {
  return unir(ids.map((id) => FUENTES[id] || id), idioma === 'en' ? 'and' : 'y')
}

export const TEXTOS = {
  en: {
    marca: 'Milpa Resiliente',
    idioma: 'Language',
    parcela: 'Plot',
    parcelaEjemplo: 'Example plot',
    ubicacionProvisional: 'Location still to be confirmed',
    titulo: 'What the satellite saw on this plot',
    entradilla: 'Three facts from past years, always in the same order. They are records, not a forecast.',
    hechos: { suelo: 'Bare soil', quema: 'Fire near the plot', canicula: 'Long dry spell (canícula)' },
    estados: {
      verde: 'Good',
      amarillo: 'Watch',
      rojo: 'Repeats',
      gris: "The satellite can't see well here",
      pendiente: 'No color yet',
      sinResumen: 'Not in this data file yet',
    },
    explicaEstado: {
      verde: 'The satellite did not see the problem in this period.',
      amarillo: 'It saw it a few times.',
      rojo: 'It saw it often.',
      gris: 'Data from this source is missing, so we do not guess.',
      pendiente: 'No color yet: the traffic-light cut-offs are not applied to this data file.',
    },
    conteo: {
      suelo: (v, de) => (v === 0 ? `Not seen in any of the ${de} months of the year` : `Seen in ${v} of the ${de} months of the year`),
      quema: (v, de) => (v === 0 ? `Not seen in ${de} years` : `Seen in ${v} of ${de} years`),
      canicula: (v, de) => (v === 0 ? `Not seen in ${de} years` : `Seen in ${v} of ${de} years`),
    },
    detalleMeses: {
      suelo: (ms) => `Bare: ${meses('en', ms)}.`,
      pocaCobertura: (ms) => `Little plant cover: ${meses('en', ms)}.`,
      quema: (ms) => `Months with fire: ${meses('en', ms)}.`,
      canicula: () => 'Between June and August.',
    },
    fuente: (ids, periodo) => `Source: ${fuentes('en', ids)}, ${periodoEntero(periodo)}.`,
    motivoGris: 'Reason (in Spanish):',
    opcionesTitulo: 'Options to talk over with your technician',
    tipos: {
      actual: 'What you do today',
      leguminosa_cobertura: 'Legume or cover crop',
      tolerante_sequia: 'Drought-tolerant crop',
    },
    sinOrden: 'In no particular order.',
    opciones: {
      pendiente: 'The tie rule is not applied to this data file yet, so no option is marked as the best.',
      empate: (n) => `${n === 2 ? 'Two' : n === 3 ? 'Three' : n} options come out even. None stands out enough.`,
      una_destaca: 'One option stands out from the others:',
      gris: 'We do not compare the options here because confidence is low.',
    },
    confianzaTitulo: 'How sure we are',
    confianza: { alta: 'High', media: 'Medium', baja: 'Low' },
    motivo: 'Why (in Spanish):',
    aviso: 'This is not an official alert; talk to your technician.',
    evidencia: 'See the evidence',
    evidenciaDetalle: 'Map, charts, sources and limits',
    volver: 'Back to the farmer view',
    cargando: 'Loading…',
    cargandoEvidencia: 'Loading the map and charts…',
    errorDatos: 'The data for this plot did not load. Check the connection and reload the page.',
    errorEvidencia: 'The evidence view did not load. Check the connection and try again.',
    reintentar: 'Try again',
    sinResumen: 'This data file does not have the farmer summary yet. The evidence view has every figure.',
    noDisponible: 'This plot has no data yet. Open the evidence view to see what is missing.',
    ejemplo: 'Example data for development. This is not a recommendation.',
  },
  es: {
    marca: 'Milpa Resiliente',
    idioma: 'Idioma',
    parcela: 'Parcela',
    parcelaEjemplo: 'Parcela de ejemplo',
    ubicacionProvisional: 'Ubicación por confirmar',
    titulo: 'Lo que el satélite vio en esta parcela',
    entradilla: 'Tres hechos de años pasados, siempre en el mismo orden. Son registros, no un pronóstico.',
    hechos: { suelo: 'Suelo desnudo', quema: 'Quema cerca de la parcela', canicula: 'Canícula larga' },
    estados: {
      verde: 'Bien',
      amarillo: 'Atención',
      rojo: 'Se repite',
      gris: 'El satélite no ve bien aquí',
      pendiente: 'Sin color todavía',
      sinResumen: 'Aún no está en este archivo de datos',
    },
    explicaEstado: {
      verde: 'El satélite no vio el problema en el período.',
      amarillo: 'Lo vio pocas veces.',
      rojo: 'Lo vio seguido.',
      gris: 'Faltan datos de esta fuente; no se adivina.',
      pendiente: 'Sin color todavía: los cortes del semáforo aún no están aplicados en este archivo de datos.',
    },
    conteo: {
      suelo: (v, de) => (v === 0 ? `No se vio en ninguno de los ${de} meses del año` : `Se vio en ${v} de los ${de} meses del año`),
      quema: (v, de) => (v === 0 ? `No se vio en ${de} años` : `Se vio en ${v} de ${de} años`),
      canicula: (v, de) => (v === 0 ? `No se vio en ${de} años` : `Se vio en ${v} de ${de} años`),
    },
    detalleMeses: {
      suelo: (ms) => `Desnudo: ${meses('es', ms)}.`,
      pocaCobertura: (ms) => `Poca cobertura: ${meses('es', ms)}.`,
      quema: (ms) => `Meses con quema: ${meses('es', ms)}.`,
      canicula: () => 'Entre junio y agosto.',
    },
    fuente: (ids, periodo) => `Fuente: ${fuentes('es', ids)}, ${periodoEntero(periodo)}.`,
    motivoGris: 'Motivo:',
    opcionesTitulo: 'Opciones para platicar con su técnico',
    tipos: {
      actual: 'Lo que hace hoy',
      leguminosa_cobertura: 'Leguminosa o cobertura',
      tolerante_sequia: 'Cultivo tolerante a sequía',
    },
    sinOrden: 'Sin orden.',
    opciones: {
      pendiente: 'La regla de empate aún no está aplicada en este archivo de datos; por eso ninguna opción se marca como la mejor.',
      empate: (n) => `${n === 2 ? 'Dos' : n === 3 ? 'Tres' : n} opciones quedan parejas. Ninguna se separa lo suficiente.`,
      una_destaca: 'Una opción se separa de las demás:',
      gris: 'Aquí no comparamos las opciones porque la confianza es baja.',
    },
    confianzaTitulo: 'Qué tan seguros estamos',
    confianza: { alta: 'Alta', media: 'Media', baja: 'Baja' },
    motivo: 'Por qué:',
    aviso: 'Esto no es una alerta oficial; hable con su técnico.',
    evidencia: 'Ver la evidencia',
    evidenciaDetalle: 'Mapa, gráficas, fuentes y límites',
    volver: 'Volver a la vista del agricultor',
    cargando: 'Cargando…',
    cargandoEvidencia: 'Cargando el mapa y las gráficas…',
    errorDatos: 'No se cargaron los datos de esta parcela. Revise la conexión y vuelva a cargar la página.',
    errorEvidencia: 'No se cargó la vista de evidencia. Revise la conexión e intente otra vez.',
    reintentar: 'Intentar otra vez',
    sinResumen: 'Este archivo de datos todavía no trae el resumen para el agricultor. La vista de evidencia tiene todas las cifras.',
    noDisponible: 'Esta parcela todavía no tiene datos. Abra la vista de evidencia para ver qué falta.',
    ejemplo: 'Datos de ejemplo para desarrollar. No es una recomendación.',
  },
}
