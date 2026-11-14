// Textos de los pictogramas en español e inglés. Viven aquí para que el carril de pictogramas
// no dependa del diccionario de la web (web/src/i18n/, otro carril). Al unir se pueden mover.

export const IDIOMAS = ['es', 'en']

export const TITULOS = {
  sueloDesnudo: { es: 'Suelo desnudo', en: 'Bare soil' },
  sueloCubierto: { es: 'Suelo cubierto', en: 'Covered soil' },
  fuego: { es: 'Quema', en: 'Fire' },
  sol: { es: 'Sol fuerte, días sin lluvia', en: 'Strong sun, days without rain' },
  lluvia: { es: 'Lluvia', en: 'Rain' },
  gota: { es: 'Agua', en: 'Water' },
  maiz: { es: 'Maíz', en: 'Maize' },
  frijol: { es: 'Frijol', en: 'Beans' },
  satelite: { es: 'Satélite', en: 'Satellite' },
  platicar: { es: 'Platicar con su técnico', en: 'Talk with your extension worker' },
}

export const MESES = {
  es: ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'],
  en: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
}

export const INICIALES = {
  es: ['E', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'],
  en: ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'],
}

export const COBERTURA = {
  desnudo: { es: 'Suelo desnudo', en: 'Bare soil' },
  poca: { es: 'Poca cobertura', en: 'Little cover' },
  cubierto: { es: 'Cubierto', en: 'Covered' },
}

const lista = (items, lang) => {
  if (items.length === 0) return lang === 'en' ? 'none' : 'ninguno'
  if (items.length === 1) return items[0]
  const y = lang === 'en' ? ' and ' : ' y '
  return items.slice(0, -1).join(', ') + y + items[items.length - 1]
}

export const frases = {
  rueda(lang, desnudos, poca, total) {
    const m = MESES[lang]
    const nd = desnudos.map((x) => m[x - 1])
    const np = poca.map((x) => m[x - 1])
    const cuales = nd.length ? ` (${lista(nd, lang)})` : ''
    return lang === 'en'
      ? `${desnudos.length} of ${total} months with bare soil${cuales}. Little cover: ${lista(np, lang)}.`
      : `${desnudos.length} de ${total} meses con suelo desnudo${cuales}. Poca cobertura: ${lista(np, lang)}.`
  },
  ruedaCentro(lang, total) {
    return lang === 'en' ? `of ${total} months` : `de ${total} meses`
  },
  anios(lang, tipo, marcados, total) {
    if (tipo === 'quema') {
      return lang === 'en'
        ? `${marcados} of ${total} years with a fire seen nearby`
        : `${marcados} de ${total} años con quema vista cerca`
    }
    return lang === 'en'
      ? `${marcados} of ${total} years with a long canícula (midsummer dry spell)`
      : `${marcados} de ${total} años con canícula larga`
  },
  pixel(lang, ladoM, ha, manzanas) {
    const f = (n, d) => n.toLocaleString(lang === 'en' ? 'en-US' : 'es-GT', { maximumFractionDigits: d })
    return lang === 'en'
      ? `The satellite sees a square of ${f(ladoM, 0)} m by ${f(ladoM, 0)} m: about ${f(manzanas, 0)} manzanas (${f(ha, 2)} ha), not only your plot.`
      : `El satélite ve un cuadro de ${f(ladoM, 0)} m por ${f(ladoM, 0)} m: unas ${f(manzanas, 0)} manzanas (${f(ha, 2)} ha), no solo su parcela.`
  },
  unaManzana() {
    return '1 manzana'
  },
}
