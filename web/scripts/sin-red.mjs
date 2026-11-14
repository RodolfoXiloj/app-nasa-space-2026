// Prueba sin red (plan 12.4) en la laptop, sin apagar el Wi-Fi (cortaría la sesión del asistente):
// Edge sin interfaz con un proxy inexistente, así que no llega a internet, pero sí al servidor local
// (Chromium no usa el proxy para 127.0.0.1). Es lo que pasa con el Wi-Fi apagado: la copia local
// responde y todo lo externo falla. Recorre las 5 parcelas, el audio, las capas «sin red», las
// pestañas y la impresión a PDF.
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
  await hasta(() => ev(`document.querySelectorAll('.rotacion').length === 3`), 30000)

  // 0. internet de verdad cortado
  const externo = await ev(`fetch('https://tile.openstreetmap.org/0/0/0.png', {mode: 'no-cors'}).then(() => 'llegó', (e) => 'falló: ' + e.message)`)
  anota(externo.startsWith('falló'), 'Sin internet: una petición a tile.openstreetmap.org', externo)

  // 1. primera pantalla y observación de 2026
  anota(await ev(`document.querySelector('h1')?.textContent === 'Milpa Resiliente'`), 'La página abre (título)')
  const obs = await ev(`document.querySelector('.banda-obs')?.textContent || ''`)
  anota(obs.includes('Observación preliminar') && !/alerta/i.test(obs), 'Observación de 2026 en la primera pantalla, sin «alerta»', obs.slice(0, 90) + '…')

  // 2. las 5 parcelas, con audio
  const ids = await ev(`[...document.querySelector('.controles select').options].map(o => o.value)`)
  for (const pid of ids) {
    await ev(`(() => { const s = document.querySelector('.controles select'); const set = Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype, 'value').set; set.call(s, '${pid}'); s.dispatchEvent(new Event('change', { bubbles: true })); return true })()`)
    const ok = await hasta(() => ev(`(() => { const a = document.querySelector('.tarjeta-acciones audio'); return document.querySelectorAll('.rotacion').length === 3 && a && a.src.includes('/audio/${pid}.mp3') })()`), 15000)
    const audio = await ev(`(async () => { const a = document.querySelector('.tarjeta-acciones audio'); a.muted = true; try { await a.play() } catch (e) { return 'play falló: ' + e.message } await new Promise(r => setTimeout(r, 1500)); const t = a.currentTime; a.pause(); return 'suena ' + t.toFixed(1) + ' s de ' + a.duration.toFixed(0) + ' s' })()`)
    const ia = await ev(`document.querySelector('.nota-ia')?.textContent || ''`)
    anota(Boolean(ok) && audio.startsWith('suena') && !audio.startsWith('suena 0.0') && ia.includes('IA'), `Parcela ${pid}: 3 rotaciones, tarjeta y audio mp3`, `${audio}; rótulo de IA: ${ia.includes('IA') ? 'sí' : 'no'}`)
  }

  // 3. capas «sin red»
  // sin hacer clic: el mapa debe pasar solo a la capa guardada cuando fallan las teselas en línea
  const teselas = await hasta(() => ev(`(() => { const t = [...document.querySelectorAll('img.leaflet-tile')].filter(i => i.src.includes('/capas/') && i.complete && i.naturalWidth > 0); return t.length || null })()`), 15000)
  const aviso = await ev(`document.querySelector('.aviso-sin-red')?.textContent || ''`)
  const radio = await ev(`[...document.querySelectorAll('.leaflet-control-layers label')].find(x => x.textContent.includes('Color real MODIS'))?.querySelector('input')?.checked`)
  anota(Boolean(teselas) && aviso.includes('Sin internet') && radio === true, 'El mapa pasa solo a la capa «Color real MODIS (sin red)»',
    `${teselas || 0} teselas locales; aviso: ${aviso ? 'sí' : 'no'}; control de capas marcado: ${radio}`)

  // 4. pestañas
  await ev(`[...document.querySelectorAll('.pestanas button')].find(b => b.textContent === 'Validación').click()`)
  anota(Boolean(await hasta(() => ev(`!!document.getElementById('observacion-2026') && document.querySelectorAll('.tabla-datos').length >= 3`))), 'Pestaña Validación con el detalle de 2026')
  await ev(`[...document.querySelectorAll('.pestanas button')].find(b => b.textContent.startsWith('Glosario')).click()`)
  anota(Boolean(await hasta(() => ev(`document.body.textContent.includes('IMERG')`))), 'Pestaña Glosario y fuentes (cita IMERG)')

  // 5. imprimir la tarjeta a PDF
  await ev(`[...document.querySelectorAll('.pestanas button')].find(b => b.textContent === 'Parcela').click()`)
  await hasta(() => ev(`document.querySelectorAll('.rotacion').length === 3`))
  const pdf = await cdp('Page.printToPDF', { printBackground: true })
  const bytes = Buffer.from(pdf.result?.data || '', 'base64')
  writeFileSync(join(SP, 'tarjeta_sin_red.pdf'), bytes)
  anota(bytes.subarray(0, 4).toString() === '%PDF' && bytes.length > 10000, 'Imprimir / guardar PDF', `${Math.round(bytes.length / 1024)} KB`)

  // captura de la primera pantalla
  const cap = await cdp('Page.captureScreenshot', { format: 'png' })
  writeFileSync(join(SP, 'primera_pantalla_sin_red.png'), Buffer.from(cap.result.data, 'base64'))

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
