// Textos de la vista «Para el agricultor», en inglés (en) y español (es). Las dos ramas tienen las
// mismas claves. Las cifras nunca van escritas aquí: llegan del bloque `farmer` del JSON y se
// insertan con las funciones de abajo.

// Nombres de los meses: los mismos de los pictogramas (web/src/pictos/textos.js), una sola copia.
import { MESES } from '../pictos/textos.js'

// El idioma activo vive en web/src/i18n/store.js (uno solo para toda la web, inglés por defecto).
// Empate en cadena: las opciones parejas no están todas a `margen` puntos o menos entre sí (en Olopa,
// 87/90/92: la práctica actual y el ICTA B-5 se separan 5, pero la canavalia empata con las dos).
export function empateEnCadena(ids, porId, margen) {
  const totales = ids.map((id) => ((porId[id] || {}).puntajes || {}).total).filter((x) => typeof x === 'number')
  return totales.length > 1 && Math.max(...totales) - Math.min(...totales) > margen
}

export const IDIOMAS = ['en', 'es']
export const NOMBRE_IDIOMA = { en: 'English', es: 'Español' }

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

// Años con el hecho visto: misma frase para la quema y para la canícula.
const anios = {
  en: (v, de) => (v === 0 ? `Not seen in ${de} years` : `Seen in ${v} of ${de} years`),
  es: (v, de) => (v === 0 ? `No se vio en ${de} años` : `Se vio en ${v} de ${de} años`),
}

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
      sinResumen: 'Not in this data file yet',
    },
    explicaEstado: {
      verde: 'The satellite did not see the problem in this period.',
      amarillo: 'It saw it a few times.',
      rojo: 'It saw it often.',
      gris: 'Data from this source is missing, so we do not guess.',
    },
    conteo: {
      suelo: (v, de) => (v === 0 ? `Not seen in any of the ${de} months of the year` : `Seen in ${v} of the ${de} months of the year`),
      quema: anios.en,
      canicula: anios.en,
    },
    detalleMeses: {
      suelo: (ms) => `Bare: ${meses('en', ms)}.`,
      pocaCobertura: (ms) => `Little plant cover: ${meses('en', ms)}.`,
      quema: (ms) => `Months with fire: ${meses('en', ms)}.`,
      canicula: () => 'Between June and August.',
    },
    fuente: (ids, periodo) => `Source: ${fuentes('en', ids)}, ${periodoEntero(periodo)}.`,
    motivoGris: 'Reason:',
    opcionesTitulo: 'Options to talk over with your technician',
    tipos: {
      actual: 'What you do today',
      leguminosa_cobertura: 'Legume or cover crop',
      tolerante_sequia: 'Drought-tolerant crop',
    },
    sinOrden: 'In no particular order.',
    opciones: {
      empate: (n, margen, enCadena) =>
        enCadena
          ? `${n === 2 ? 'Two' : n === 3 ? 'Three' : n} options come out even: each is within ${margen} points of another, so none stands out.`
          : `${n === 2 ? 'Two' : n === 3 ? 'Three' : n} options come out even: their scores are ${margen} points or less apart. None stands out.`,
      una_destaca: 'One option stands out from the others:',
      gris: 'We do not compare the options here because confidence is low.',
      sinComparar: 'This data file does not compare the options.',
    },
    confianzaTitulo: 'How sure we are',
    confianza: { alta: 'High', media: 'Medium', baja: 'Low' },
    motivo: 'Why:',
    aviso: 'This is not an official alert; talk to your technician.',
    escuchar: {
      boton: 'Listen',
      detalle: 'Short audio: Spanish voice, English subtitles',
      subtitulos: 'Subtitles',
      fallo: 'The audio did not load. Check the connection and try again.',
    },
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
      sinResumen: 'Aún no está en este archivo de datos',
    },
    explicaEstado: {
      verde: 'El satélite no vio el problema en el período.',
      amarillo: 'Lo vio pocas veces.',
      rojo: 'Lo vio seguido.',
      gris: 'Faltan datos de esta fuente; no se adivina.',
    },
    conteo: {
      suelo: (v, de) => (v === 0 ? `No se vio en ninguno de los ${de} meses del año` : `Se vio en ${v} de los ${de} meses del año`),
      quema: anios.es,
      canicula: anios.es,
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
      empate: (n, margen, enCadena) =>
        enCadena
          ? `${n === 2 ? 'Dos' : n === 3 ? 'Tres' : n} opciones quedan parejas: cada una está a ${margen} puntos o menos de otra; ninguna se separa lo suficiente.`
          : `${n === 2 ? 'Dos' : n === 3 ? 'Tres' : n} opciones quedan parejas: sus puntajes se separan ${margen} puntos o menos. Ninguna se separa lo suficiente.`,
      una_destaca: 'Una opción se separa de las demás:',
      gris: 'Aquí no comparamos las opciones porque la confianza es baja.',
      sinComparar: 'Este archivo de datos no compara las opciones.',
    },
    confianzaTitulo: 'Qué tan seguros estamos',
    confianza: { alta: 'Alta', media: 'Media', baja: 'Baja' },
    motivo: 'Por qué:',
    aviso: 'Esto no es una alerta oficial; hable con su técnico.',
    escuchar: {
      boton: 'Escuchar',
      detalle: 'Audio corto, con subtítulos',
      subtitulos: 'Subtítulos',
      fallo: 'No se cargó el audio. Revise la conexión e intente otra vez.',
    },
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
