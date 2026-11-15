// K1: una imagen de la parcela para compartir por WhatsApp (1080 x 1440 px). Se dibuja en un <canvas> con
// lo mismo que la hoja impresa: por cada hecho, la forma del semáforo, la palabra, la cantidad como dibujo
// (rueda de 12 meses o puntos de años) y la frase del motor. Nada depende solo del color.
// Las cifras salen del bloque `farmer` (motor/farmer.py); aquí no se calcula nada.
import { TEXTOS } from '../agricultor/textos.js'
import { TEXTOS_KIT } from './textos.js'

const ANCHO = 1080
const ALTO = 1440
const ORDEN = ['suelo', 'quema', 'canicula']
const RELLENO = { verde: '#2e7d32', amarillo: '#ffd200', rojo: '#c62828', gris: '#e4e4e4' }
const TINTE = { verde: '#e6f2e6', amarillo: '#fff3bf', rojo: '#fbe4e4', gris: '#f1f1f1' }
const LETRA = "'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"

const estadoDe = (h) => (['verde', 'amarillo', 'rojo', 'gris'].includes(h.estado) ? h.estado : 'gris')

// Corta solo en espacios normales: el espacio duro ( ) mantiene juntas las parejas de la leyenda («? = sin dato»).
function lineas(ctx, texto, ancho) {
  const palabras = String(texto).split(/[ \t\r\n]+/)
  const out = []
  let actual = ''
  for (const p of palabras) {
    const prueba = actual ? `${actual} ${p}` : p
    if (ctx.measureText(prueba).width > ancho && actual) {
      out.push(actual)
      actual = p
    } else actual = prueba
  }
  if (actual) out.push(actual)
  return out
}

function parrafo(ctx, texto, x, y, ancho, alto) {
  for (const l of lineas(ctx, texto, ancho)) {
    ctx.fillText(l, x, y)
    y += alto
  }
  return y
}

// La frase de un hecho dentro de su caja: con 30 px caben 3 líneas; si pasa de ahí (la del suelo de Zacapa, desde
// las frases claras del 15 nov 2026), la letra se achica de 2 en 2 hasta 22 px. `altoMax` va de la primera línea
// base al fondo de la última.
function parrafoQueCabe(ctx, texto, x, y, ancho, altoMax) {
  const interlinea = (talla) => Math.round(talla * 1.26)
  let talla = 30
  for (; talla > 22; talla -= 2) {
    ctx.font = `500 ${talla}px ${LETRA}`
    const n = lineas(ctx, texto, ancho).length
    if ((n - 1) * interlinea(talla) + Math.ceil(talla * 0.3) <= altoMax) break
  }
  ctx.font = `500 ${talla}px ${LETRA}`
  return parrafo(ctx, texto, x, y, ancho, interlinea(talla))
}

function senal(ctx, estado, cx, cy, r) {
  ctx.save()
  ctx.lineWidth = 6
  ctx.strokeStyle = '#000'
  ctx.fillStyle = RELLENO[estado]
  ctx.beginPath()
  if (estado === 'amarillo') {
    ctx.moveTo(cx, cy - r)
    ctx.lineTo(cx + r * 1.08, cy + r * 0.92)
    ctx.lineTo(cx - r * 1.08, cy + r * 0.92)
    ctx.closePath()
  } else if (estado === 'rojo') {
    ctx.rect(cx - r * 0.9, cy - r * 0.9, r * 1.8, r * 1.8)
  } else {
    ctx.arc(cx, cy, r, 0, 2 * Math.PI)
    if (estado === 'gris') ctx.setLineDash([12, 10])
  }
  ctx.fill()
  ctx.stroke()
  if (estado === 'gris') {
    ctx.setLineDash([])
    ctx.fillStyle = '#000'
    ctx.font = `900 ${r * 1.1}px ${LETRA}`
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'
    ctx.fillText('?', cx, cy + 2)
  }
  ctx.restore()
}

// Rueda de 12 meses: negro = suelo desnudo, rayado = poca cobertura, blanco = cubierto.
function rueda(ctx, cx, cy, r, desnudos, poca) {
  ctx.save()
  for (let m = 1; m <= 12; m++) {
    const a0 = -Math.PI / 2 + ((m - 1) * Math.PI) / 6
    const a1 = a0 + Math.PI / 6
    const gajo = () => {
      ctx.beginPath()
      ctx.arc(cx, cy, r, a0, a1)
      ctx.arc(cx, cy, r * 0.52, a1, a0, true)
      ctx.closePath()
    }
    gajo()
    ctx.fillStyle = '#fff'
    ctx.fill()
    if (desnudos.includes(m)) {
      ctx.fillStyle = '#000'
      ctx.fill()
    } else if (poca.includes(m)) {
      ctx.save()
      ctx.clip()
      ctx.strokeStyle = '#000'
      ctx.lineWidth = 3
      for (let k = -2 * r; k < 2 * r; k += 10) {
        ctx.beginPath()
        ctx.moveTo(cx + k, cy - r)
        ctx.lineTo(cx + k + 2 * r, cy + r)
        ctx.stroke()
      }
      ctx.restore()
    }
    gajo()
    ctx.lineWidth = 3
    ctx.strokeStyle = '#000'
    ctx.stroke()
  }
  ctx.restore()
}

// Puntos de años: lleno = año con quema o con canícula larga.
function puntos(ctx, x, y, marcados, total, ancho) {
  const porFila = Math.min(total, 9)
  const paso = Math.min(30, ancho / porFila)
  const r = paso * 0.38
  ctx.save()
  ctx.lineWidth = 3
  ctx.strokeStyle = '#000'
  for (let i = 0; i < total; i++) {
    const cx = x + (i % porFila) * paso + r
    const cy = y + Math.floor(i / porFila) * paso + r
    ctx.beginPath()
    ctx.arc(cx, cy, r, 0, 2 * Math.PI)
    ctx.fillStyle = i < marcados ? '#000' : '#fff'
    ctx.fill()
    ctx.stroke()
  }
  ctx.restore()
}

export function dibujar({ idioma, lugar, farmer, href }) {
  const t = TEXTOS[idioma]
  const k = TEXTOS_KIT[idioma]
  const lienzo = document.createElement('canvas')
  lienzo.width = ANCHO
  lienzo.height = ALTO
  const ctx = lienzo.getContext('2d')
  ctx.fillStyle = '#fff'
  ctx.fillRect(0, 0, ANCHO, ALTO)
  ctx.fillStyle = '#000'
  ctx.textBaseline = 'alphabetic'
  ctx.font = `700 34px ${LETRA}`
  ctx.fillText(t.marca, 60, 82)
  ctx.font = `900 60px ${LETRA}`
  let y = parrafo(ctx, lugar, 60, 152, ANCHO - 120, 66)
  ctx.font = `600 30px ${LETRA}`
  ctx.fillStyle = '#3b3b3b'
  y = parrafo(ctx, k.hechos, 60, y + 4, ANCHO - 120, 38)

  const palabras = (farmer.umbrales || {}).estados || {}
  const hechos = Object.fromEntries((farmer.hechos || []).map((h) => [h.id, h]))
  const fraseDe = (id) => ((farmer.frases || []).find((x) => x.hecho === id) || {})[idioma] || null
  const altoHecho = 300
  y += 14
  for (const id of ORDEN) {
    const h = hechos[id] || {}
    const e = estadoDe(h)
    ctx.fillStyle = TINTE[e]
    ctx.fillRect(40, y, ANCHO - 80, altoHecho - 16)
    ctx.lineWidth = 4
    ctx.strokeStyle = '#000'
    ctx.strokeRect(40, y, ANCHO - 80, altoHecho - 16)
    senal(ctx, e, 120, y + 90, 50)
    ctx.fillStyle = '#000'
    ctx.font = `700 36px ${LETRA}`
    ctx.fillText(t.hechos[id], 200, y + 62)
    const palabra = (palabras[e] || {})[idioma] || t.estados[e]
    // Sin dibujo a la derecha (gris) hay más lugar; si aun así no cabe, la letra se achica.
    const cabe = e === 'gris' ? ANCHO - 80 - 200 - 20 : 560
    let talla = 58
    ctx.font = `900 ${talla}px ${LETRA}`
    while (ctx.measureText(palabra).width > cabe && talla > 30) {
      talla -= 2
      ctx.font = `900 ${talla}px ${LETRA}`
    }
    ctx.fillText(palabra, 200, y + 126)
    const frase = fraseDe(id) || (e === 'gris' ? t.explicaEstado[e] : '')
    // De la primera línea (y + 176) al fondo de la caja (y + 284) quedan 8 px de margen.
    parrafoQueCabe(ctx, frase, 200, y + 176, 560, altoHecho - 16 - 176 - 8)
    const gris = e === 'gris'
    if (id === 'suelo' && !gris) rueda(ctx, 900, y + 140, 92, h.meses || [], h.meses_poca_cobertura || [])
    else if (!gris && h.valor != null && h.de > 0) puntos(ctx, 790, y + 60, h.valor, h.de, 240)
    y += altoHecho
  }
  ctx.fillStyle = '#000'
  ctx.font = `500 26px ${LETRA}`
  y = parrafo(ctx, k.formas, 60, y + 18, ANCHO - 120, 34)
  ctx.font = `700 30px ${LETRA}`
  y = parrafo(ctx, t.aviso, 60, y + 10, ANCHO - 120, 38)
  ctx.font = `400 22px ${LETRA}`
  ctx.fillStyle = '#3b3b3b'
  y = parrafo(ctx, t.ia, 60, y + 8, ANCHO - 120, 28)
  if (href) {
    ctx.font = `700 26px ${LETRA}`
    ctx.fillStyle = '#000'
    parrafo(ctx, href.replace(/#.*$/, ''), 60, Math.max(y + 12, ALTO - 40), ANCHO - 120, 32)
  }
  return new Promise((resolve) => lienzo.toBlob((b) => resolve(b), 'image/png'))
}

// Comparte la imagen con el menú del teléfono (Web Share con archivo); si no se puede, la descarga.
export async function compartirImagen({ idioma, lugar, farmer, href, pid, texto }) {
  const blob = await dibujar({ idioma, lugar, farmer, href })
  if (!blob) return 'error'
  const nombre = `milpa-${pid}-${idioma}.png`
  const archivo = typeof File === 'function' ? new File([blob], nombre, { type: 'image/png' }) : null
  if (archivo && navigator.canShare && navigator.canShare({ files: [archivo] })) {
    try {
      await navigator.share({ files: [archivo], text: texto })
      return 'compartida'
    } catch (e) {
      if (e && e.name === 'AbortError') return 'cancelada'
    }
  }
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = nombre
  document.body.appendChild(a)
  a.click()
  a.remove()
  setTimeout(() => URL.revokeObjectURL(url), 4000)
  return 'descargada'
}
