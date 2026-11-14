// Textos del kit comunitario (hoja imprimible y botones para compartir), en inglés y en español.
// Los nombres de los hechos, las palabras del semáforo y el aviso salen de agricultor/textos.js.
export const TEXTOS_KIT = {
  en: {
    titulo: 'Share this plot',
    detalle: 'One black-and-white page to print, the short audio and a WhatsApp message.',
    imprimir: 'Print sheet',
    audio: 'Download audio',
    whatsapp: 'Share on WhatsApp',
    hoja: 'Plot sheet',
    hechos: 'What the satellite saw (past years, not a forecast)',
    formas: 'Shapes: circle = good, triangle = watch, square = repeats, ? = no data.',
    confianza: 'How sure we are:',
    web: 'Full page:',
    resumen: (lugar) => `Milpa Resiliente, ${lugar}`,
  },
  es: {
    titulo: 'Compartir esta parcela',
    detalle: 'Una hoja en blanco y negro para imprimir, el audio corto y un mensaje por WhatsApp.',
    imprimir: 'Imprimir hoja',
    audio: 'Descargar audio',
    whatsapp: 'Compartir por WhatsApp',
    hoja: 'Hoja de la parcela',
    hechos: 'Lo que vio el satélite (años pasados, no es pronóstico)',
    formas: 'Formas: círculo = bien, triángulo = atención, cuadrado = se repite, ? = sin dato.',
    confianza: 'Qué tan seguros estamos:',
    web: 'Página completa:',
    resumen: (lugar) => `Milpa Resiliente, ${lugar}`,
  },
}
