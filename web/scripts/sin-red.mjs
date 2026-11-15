// Prueba sin red (plan 12.4) en la laptop, sin apagar el Wi-Fi (cortaría la sesión del asistente):
// Edge sin interfaz con un proxy inexistente, así que no llega a internet, pero sí al servidor local
// (Chromium no usa el proxy para 127.0.0.1). Es lo que pasa con el Wi-Fi apagado: la copia local
// responde y todo lo externo falla. Recorre el botón «Listen» de la vista del agricultor (audio corto
// con subtítulos), el kit comunitario (hoja de 1 página, audio y WhatsApp), las 5 parcelas, el audio,
// las capas «sin red», las pestañas y la impresión a PDF.
// No hay service worker: sin red, la web y su audio salen de la copia local servida en la laptop.
// Uso: cd web && npm run build && npm run sin-red   (resultados, captura y PDF en una carpeta temporal)
import { spawn, execSync } from 'node:child_process'
import { existsSync, mkdirSync, mkdtempSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const WEB = join(dirname(fileURLToPath(import.meta.url)), '..')
const SP = process.argv[2] || mkdtempSync(join(tmpdir(), 'milpa-sin-red-'))
const EDGE = [process.env.NAVEGADOR, 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'].find((r) => r && existsSync(r))
if (!EDGE) throw new Error('No encontré Edge ni Chrome; indique la ruta en la variable NAVEGADOR')
const PUERTO = 4174
const URL_APP = `http://127.0.0.1:${PUERTO}/`
const espera = (ms) => new Promise((r) => setTimeout(r, ms))
const resultados = []
const anota = (ok, que, detalle = '') => {
  resultados.push({ ok, que, detalle })
  console.log(`${ok ? 'OK ' : 'NO '} ${que}${detalle ? ' · ' + detalle : ''}`)
}

async function hasta(fn, ms = 20000, paso = 300) {
  const fin = Date.now() + ms
  while (Date.now() < fin) {
    try {
      const v = await fn()
      if (v) return v
    } catch {}
    await espera(paso)
  }
  return null
}

const vite = spawn(process.execPath, ['node_modules/vite/bin/vite.js', 'preview', '--host', '127.0.0.1', '--port', String(PUERTO), '--strictPort'], { cwd: WEB, stdio: 'ignore' })
let edge
try {
  if (!(await hasta(async () => (await fetch(URL_APP)).ok))) throw new Error('vite preview no respondió')
  const perfil = join(SP, 'edge-perfil-sin-red')
  mkdirSync(perfil, { recursive: true })
  edge = spawn(EDGE, ['--headless=new', '--remote-debugging-port=9334', `--user-data-dir=${perfil}`, '--proxy-server=http://127.0.0.1:9',
    '--no-first-run', '--disable-extensions', '--disable-sync', '--disable-background-networking', '--disable-component-update',
    '--autoplay-policy=no-user-gesture-required', '--window-size=412,915', 'about:blank'], { stdio: 'ignore' })
  const lista = await hasta(async () => {
    const j = await (await fetch('http://127.0.0.1:9334/json/list')).json()
    return j.find((t) => t.type === 'page') ? j : null
  })
  if (!lista) throw new Error('Edge no abrió el puerto de depuración')
  const ws = new WebSocket(lista.find((t) => t.type === 'page').webSocketDebuggerUrl)
  await new Promise((r, e) => { ws.onopen = r; ws.onerror = e })
  let id = 0
  const pend = new Map()
  const peticiones = new Map()
  ws.onmessage = (m) => {
    const d = JSON.parse(m.data)
    if (d.id && pend.has(d.id)) { pend.get(d.id)(d); pend.delete(d.id); return }
    if (d.method === 'Network.requestWillBeSent') peticiones.set(d.params.requestId, { url: d.params.request.url, estado: null })
    if (d.method === 'Network.responseReceived' && peticiones.has(d.params.requestId)) peticiones.get(d.params.requestId).estado = d.params.response.status
    if (d.method === 'Network.loadingFailed' && peticiones.has(d.params.requestId)) peticiones.get(d.params.requestId).error = d.params.errorText
  }
  const cdp = (method, params = {}) => new Promise((r) => { const i = ++id; pend.set(i, r); ws.send(JSON.stringify({ id: i, method, params })) })
  const ev = async (expr) => (await cdp('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true })).result?.result?.value
  await cdp('Network.enable')
  await cdp('Page.enable')
  await cdp('Network.setCacheDisabled', { cacheDisabled: true })
  await cdp('Page.navigate', { url: URL_APP })

  // 00. primera pantalla: vista del agricultor, sin descargar el mapa ni las gráficas; Evidence a un toque
  const diferido = () => [...peticiones.values()].some((p) => /\/assets\/Evidencia-[^/]*\.js$/.test(p.url))
  const hechos = await hasta(() => ev(`(() => { const h = [...document.querySelectorAll('.agr-hecho')].map((li) => li.dataset.hecho); return h.length === 3 ? h.join(',') : null })()`), 30000)
  anota(hechos === 'suelo,quema,canicula' && !diferido(), 'Primera pantalla: vista del agricultor con 3 hechos en orden, sin el mapa', hechos || 'no apareció')
  const idiomaInicio = await ev(`document.documentElement.lang + '/' + document.querySelector('.agr-idioma[aria-pressed="true"]')?.lang`)
  anota(idiomaInicio === 'en/en', 'Idioma por defecto: inglés en la vista del agricultor', idiomaInicio)
  // 00b. un toque a «Listen»: el audio corto por frases sale de la copia local, con la pista del idioma activo
  await ev(`document.querySelector('#agr-audio').muted = true`)
  await ev(`document.querySelector('.agr-escuchar-boton').click()`)
  const corto = await hasta(() => ev(`(() => { const a = document.querySelector('#agr-audio'); const tr = a && a.querySelector('track')
    return a && !a.paused && a.currentTime > 0.3 && tr && tr.readyState === 2 && tr.track.cues.length
      ? a.currentSrc.split('/').pop() + ' a ' + a.currentTime.toFixed(1) + ' s; ' + tr.src.split('/').pop() + ', ' + tr.track.cues.length + ' frases' : null })()`), 15000)
  const subtitulo = await ev(`document.querySelector('.agr-subtitulos')?.textContent || ''`)
  await ev(`document.querySelector('#agr-audio').pause()`)
  anota(/\.frases(\.en)?\.mp3 a /.test(corto || '') && corto.includes('.frases.en.vtt') && subtitulo.length > 0,
    'Un toque a «Listen»: audio corto local en inglés con subtítulos en inglés', `${corto || 'no sonó'}; «${subtitulo}»`)
  // 00c. kit comunitario: llega con import() después de pintar; sus 3 botones funcionan sin red
  const kit = await hasta(() => ev(`(() => { const a = document.querySelector('.kit-audio'), w = document.querySelector('.kit-whatsapp')
    return document.querySelector('.kit-imprimir') && a && w ? { audio: a.getAttribute('href'), descarga: a.hasAttribute('download'), wa: w.href } : null })()`), 15000)
  const mp3Kit = kit ? await ev(`fetch(${JSON.stringify(kit.audio)}).then((r) => r.status + ' ' + r.headers.get('content-type'), (e) => 'falló: ' + e.message)`) : ''
  anota(Boolean(kit) && kit.descarga && /audio\/[a-z_]+\.frases\.en\.mp3$/.test(kit.audio) && mp3Kit.startsWith('200'),
    'Kit: «Download audio» baja el mp3 corto en inglés de la copia local', kit ? `${kit.audio}: ${mp3Kit}` : 'no apareció el kit')
  const wa = kit ? new URL(kit.wa) : null
  const textoWa = wa ? wa.searchParams.get('text') || '' : ''
  anota(Boolean(wa) && wa.origin === 'https://wa.me' && wa.pathname === '/' && textoWa.endsWith(URL_APP) && textoWa.includes('not an official notice'),
    'Kit: enlace de WhatsApp bien formado (wa.me/?text= con resumen y la dirección local)', textoWa.replace(/\n/g, ' / ').slice(0, 120))
  await ev(`(() => { window.print = () => {}; document.querySelector('.kit-imprimir').click(); return true })()`)
  const hojaPdf = await cdp('Page.printToPDF', { printBackground: true })
  const hojaBytes = Buffer.from(hojaPdf.result?.data || '', 'base64')
  writeFileSync(join(SP, 'hoja_parcela_sin_red.pdf'), hojaBytes)
  const paginasHoja = (hojaBytes.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length
  anota(hojaBytes.subarray(0, 4).toString() === '%PDF' && paginasHoja === 1, 'Kit: «Print sheet» da una hoja de 1 página sin red', `${paginasHoja} página(s), ${Math.round(hojaBytes.length / 1024)} KB`)
  await ev(`document.documentElement.classList.remove('kit-imprimiendo')`)
  await ev(`document.querySelector('.agr-evidencia').click()`)
  await hasta(() => ev(`document.querySelectorAll('.rotacion').length === 3`), 30000)
  anota((await ev(`location.hash`)) === '#evidence' && diferido(), 'Un toque abre Evidence y ahí se descarga el mapa')
  const idiomaEvidence = await ev(`document.querySelector('.selector-idioma .activa')?.textContent`)
  anota(idiomaEvidence === 'English', 'Evidence abre en el mismo idioma (un solo idioma activo)', idiomaEvidence || 'sin selector')

  // 0. internet de verdad cortado
  const externo = await ev(`fetch('https://tile.openstreetmap.org/0/0/0.png', {mode: 'no-cors'}).then(() => 'llegó', (e) => 'falló: ' + e.message)`)
  anota(externo.startsWith('falló'), 'Sin internet: una petición a tile.openstreetmap.org', externo)

  // 1. vista Evidence y observación de 2026
  anota(await ev(`document.querySelector('h1')?.textContent === 'Milpa Resiliente'`), 'La página abre (título)')
  const obs = await ev(`document.querySelector('.banda-obs')?.textContent || ''`)
  anota(obs.includes('Observación preliminar') && !/alerta/i.test(obs), 'Observación de 2026 al abrir Evidence, sin «alerta»', obs.slice(0, 90) + '…')

  // 2. las 5 parcelas, con el audio de la tarjeta en el idioma activo (audio/{pid}.en.mp3 en inglés, audio/{pid}.mp3 en español)
  const ids = await ev(`[...document.querySelector('.controles select').options].map(o => o.value)`)
  const sufijo = (await ev(`document.documentElement.lang`)) === 'en' ? '.en.mp3' : '.mp3'
  for (const pid of ids) {
    await ev(`(() => { const s = document.querySelector('.controles select'); const set = Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype, 'value').set; set.call(s, '${pid}'); s.dispatchEvent(new Event('change', { bubbles: true })); return true })()`)
    const ok = await hasta(() => ev(`(() => { const a = document.querySelector('.tarjeta-acciones audio'); return document.querySelectorAll('.rotacion').length === 3 && a && a.src.endsWith('/audio/${pid}${sufijo}') })()`), 15000)
    const audio = await ev(`(async () => { const a = document.querySelector('.tarjeta-acciones audio'); a.muted = true; try { await a.play() } catch (e) { return 'play falló: ' + e.message } await new Promise(r => setTimeout(r, 1500)); const t = a.currentTime; a.pause(); return 'suena ' + t.toFixed(1) + ' s de ' + a.duration.toFixed(0) + ' s' })()`)
    const ia = await ev(`document.querySelector('.nota-ia')?.textContent || ''`)
    anota(Boolean(ok) && audio.startsWith('suena') && !audio.startsWith('suena 0.0') && /\b(IA|AI)\b/.test(ia), `Parcela ${pid}: 3 rotaciones, tarjeta y audio mp3 (${pid}${sufijo})`, `${audio}; rótulo de IA: ${/\b(IA|AI)\b/.test(ia) ? 'sí' : 'no'}`)
  }

  // 3. capas «sin red»
  // sin hacer clic: el mapa debe pasar solo a la capa guardada cuando fallan las teselas en línea
  const teselas = await hasta(() => ev(`(() => { const t = [...document.querySelectorAll('img.leaflet-tile')].filter(i => i.src.includes('/capas/') && i.complete && i.naturalWidth > 0); return t.length || null })()`), 15000)
  const aviso = await ev(`document.querySelector('.aviso-sin-red')?.textContent || ''`)
  const radio = await ev(`[...document.querySelectorAll('.leaflet-control-layers label')].find(x => x.textContent.includes('Color real MODIS'))?.querySelector('input')?.checked`)
  anota(Boolean(teselas) && aviso.includes('Sin internet') && radio === true, 'El mapa pasa solo a la capa «Color real MODIS (sin red)»',
    `${teselas || 0} teselas locales; aviso: ${aviso ? 'sí' : 'no'}; control de capas marcado: ${radio}`)

  // 4. pestañas
  // Pestañas por posición: el rótulo cambia con el idioma (Parcela/Plot, Validación/Validation, Glosario/Glossary).
  await ev(`document.querySelectorAll('.pestanas button')[1].click()`)
  anota(Boolean(await hasta(() => ev(`!!document.getElementById('observacion-2026') && document.querySelectorAll('.tabla-datos').length >= 3`))), 'Pestaña Validación con el detalle de 2026')
  await ev(`document.querySelectorAll('.pestanas button')[2].click()`)
  anota(Boolean(await hasta(() => ev(`document.body.textContent.includes('IMERG')`))), 'Pestaña Glosario y fuentes (cita IMERG)')

  // 5. imprimir la tarjeta a PDF
  await ev(`document.querySelectorAll('.pestanas button')[0].click()`)
  await hasta(() => ev(`document.querySelectorAll('.rotacion').length === 3`))
  const pdf = await cdp('Page.printToPDF', { printBackground: true })
  const bytes = Buffer.from(pdf.result?.data || '', 'base64')
  writeFileSync(join(SP, 'tarjeta_sin_red.pdf'), bytes)
  anota(bytes.subarray(0, 4).toString() === '%PDF' && bytes.length > 10000, 'Imprimir / guardar PDF', `${Math.round(bytes.length / 1024)} KB`)

  // captura de la primera pantalla
  const cap = await cdp('Page.captureScreenshot', { format: 'png' })
  writeFileSync(join(SP, 'primera_pantalla_sin_red.png'), Buffer.from(cap.result.data, 'base64'))

  // 5b. cambiar a español en Evidence y volver: la vista del agricultor sigue en español
  await ev(`[...document.querySelectorAll('.selector-idioma button')].find(b => b.textContent === 'Español').click()`)
  await ev(`document.querySelector('.agr-barra button').click()`)
  const tituloEs = await hasta(() => ev(`document.querySelector('#agr-titulo')?.textContent || null`), 10000)
  const langEs = await ev(`document.documentElement.lang`)
  anota(tituloEs === 'Lo que el satélite vio alrededor de esta parcela' && langEs === 'es', 'Español elegido en Evidence sigue al volver a la vista del agricultor', `${langEs}: ${tituloEs}`)

  // 6. qué pidió la página: lo local debe responder y lo externo fallar
  const todas = [...peticiones.values()].filter((p) => p.url.startsWith('http'))
  const locales = todas.filter((p) => p.url.startsWith(URL_APP))
  const externas = todas.filter((p) => !p.url.startsWith(URL_APP))
  const localesMal = locales.filter((p) => p.error || (p.estado && p.estado >= 400))
  const hosts = [...new Set(externas.map((p) => new URL(p.url).host))]
  const externasOk = externas.filter((p) => p.estado && p.estado < 400)
  // Un mp3 que el navegador corta al pausar o al cambiar de parcela queda como net::ERR_ABORTED después de
  // haber respondido (200 o 206): no es una falla del servidor. Se cuenta aparte y con su estado.
  const cortadas = localesMal.filter((p) => p.error === 'net::ERR_ABORTED' && p.estado && p.estado < 400)
  const malDeVerdad = localesMal.filter((p) => !cortadas.includes(p))
  anota(malDeVerdad.length === 0, `Peticiones locales: ${locales.length}, todas responden`,
    (cortadas.length ? `${cortadas.length} mp3 cortados por el navegador tras responder (${[...new Set(cortadas.map((p) => p.estado))].join('/')}, net::ERR_ABORTED)` : '')
    + malDeVerdad.slice(0, 3).map((p) => ` ${p.url} ${p.estado || ''} ${p.error || ''}`).join(''))
  anota(externasOk.length === 0, `Peticiones externas: ${externas.length} (${hosts.join(', ') || 'ninguna'}), ninguna llegó`, 'son teselas del mapa base en línea')
  ws.close()
} catch (e) {
  anota(false, 'La prueba no pudo terminar', e.message)
} finally {
  if (edge?.pid) try { execSync(`taskkill /PID ${edge.pid} /T /F`, { stdio: 'ignore' }) } catch {}
  try { execSync(`taskkill /PID ${vite.pid} /T /F`, { stdio: 'ignore' }) } catch {}
}
const fallos = resultados.filter((r) => !r.ok).length
console.log(`\n${resultados.length - fallos} de ${resultados.length} comprobaciones pasan · resultados en ${SP}`)
writeFileSync(join(SP, 'prueba_sin_red.json'), JSON.stringify(resultados, null, 1))
process.exit(fallos ? 1 : 0)
