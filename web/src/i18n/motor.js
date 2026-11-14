// Texto del motor en el idioma elegido: el JSON trae `es.campo` y `en.campo` (y, de antes, `campo` en
// español y `campo_en` en inglés). Si falta el inglés, va el español y `lang` dice "es" para marcarlo.
// Lo usan la vista del agricultor (TextoMotor) y la vista Evidence.
export function leerMotor(obj, campo, idioma) {
  const o = obj || {}
  const txt = (o[idioma] || {})[campo] || (idioma === 'en' ? o[campo + '_en'] : o[campo])
  return txt ? { txt, lang: idioma } : { txt: o[campo], lang: 'es' }
}
