// Prueba de humo: renderiza cada componente (salvo el mapa, que necesita navegador) con cada JSON
// de public/data/ y falla si alguno revienta. Uso: npm run smoke
import { readdirSync, readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import React from 'react'
import { renderToString } from 'react-dom/server'
import { createServer } from 'vite'

const raiz = join(dirname(fileURLToPath(import.meta.url)), '..')
// optimizeDeps.noDiscovery: sin el escaneo de dependencias del servidor de desarrollo, que corre en
// paralelo y fallaba al cerrar el servidor («Request is outdated»).
const server = await createServer({
  root: raiz,
  logLevel: 'error',
  server: { middlewareMode: true },
  appType: 'custom',
  optimizeDeps: { noDiscovery: true, include: [] },
})
let fallas = 0
try {
  const comp = async (n) => (await server.ssrLoadModule(`/src/components/${n}.jsx`)).default
  const piezas = {
    PanelSatelite: await comp('PanelSatelite'),
    Clima: await comp('Clima'),
    Rotaciones: await comp('Rotaciones'),
    Tarjeta: await comp('Tarjeta'),
    Validacion: await comp('Validacion'),
    Glosario: await comp('Glosario'),
  }
  const obsMod = await server.ssrLoadModule('/src/components/Observacion2026.jsx')
  const dir = join(raiz, 'public', 'data')
  const archivos = readdirSync(dir).filter((f) => f.endsWith('.json') && !['parcelas.json', 'validacion.json', 'futuros_nasa.json'].includes(f))
  let validacion = null
  try {
    validacion = JSON.parse(readFileSync(join(dir, 'validacion.json'), 'utf-8'))
  } catch {
    console.log('(sin validacion.json: la pestaña Validación se prueba vacía)')
  }
  if (!archivos.length) throw new Error('No hay JSON en public/data: corra python -m motor.exportar')
  const escenarios = [[0, 0, 'agua'], [-30, 1.5, 'suelo'], [-20, 0, 'plagas']]
  let tarjetasEn = 0
  for (const f of archivos) {
    const res = JSON.parse(readFileSync(join(dir, f), 'utf-8'))
    if (res.audio?.mp3) {
      try {
        const mp3 = readFileSync(join(raiz, 'public', res.audio.mp3))
        if (mp3.length < 1000) throw new Error('mp3 vacío')
        // Declaración de IA: etiqueta ID3 con la marca AI_GENERATED y texto en el JSON (motor/exportar.py).
        const cabecera = mp3.subarray(0, 4096).toString('latin1')
        if (!cabecera.startsWith('ID3') || !cabecera.includes('AI_GENERATED')) throw new Error('sin etiqueta ID3 de IA')
        if (!res.audio.ia?.generado_con_ia || !res.audio.ia?.declaracion) throw new Error('el JSON no declara la IA')
      } catch (e) {
        fallas++
        console.error(`FALLA ${f}: audio ${res.audio.mp3}: ${e.message}`)
      }
    }
    // Tarjeta completa en inglés (audio.en): mp3 propio con etiqueta ID3 de IA y declaración en el JSON.
    const tarjetaEn = res.audio?.en
    if (tarjetaEn?.mp3) {
      try {
        const mp3 = readFileSync(join(raiz, 'public', tarjetaEn.mp3))
        if (mp3.length < 1000) throw new Error('mp3 vacío')
        const cabecera = mp3.subarray(0, 4096).toString('latin1')
        if (!cabecera.startsWith('ID3') || !cabecera.includes('AI_GENERATED')) throw new Error('sin etiqueta ID3 de IA')
        if (!tarjetaEn.ia?.generado_con_ia || !tarjetaEn.ia?.declaracion) throw new Error('el JSON no declara la IA')
        if (tarjetaEn.texto !== res.en?.texto_tarjeta) throw new Error('el texto no es en.texto_tarjeta')
        tarjetasEn++
      } catch (e) {
        fallas++
        console.error(`FALLA ${f}: audio en ${tarjetaEn.mp3}: ${e.message}`)
      }
    }
    const audioEn = res.farmer?.audio?.en
    if (audioEn?.mp3) {
      try {
        const mp3 = readFileSync(join(raiz, 'public', audioEn.mp3))
        if (mp3.length < 1000) throw new Error('mp3 vacío')
        if (mp3.length > 120_000) throw new Error(`mp3 pesa ${mp3.length} B (máx. 120 kB)`)
        const cabecera = mp3.subarray(0, 4096).toString('latin1')
        if (!cabecera.startsWith('ID3') || !cabecera.includes('AI_GENERATED')) throw new Error('sin etiqueta ID3 de IA')
        if (!audioEn.ia?.generado_con_ia) throw new Error('el JSON no declara la IA del mp3 en inglés')
      } catch (e) {
        fallas++
        console.error(`FALLA ${f}: farmer audio en ${audioEn.mp3}: ${e.message}`)
      }
    }
    // El total que recalcula la web (lib/datos.js) es el del motor: con la prioridad del JSON, en cada escenario.
    try {
      const { puntajes } = await server.ssrLoadModule('/src/lib/datos.js')
      const prio = res.pesos?.prioridad
      for (const esc of res.escenarios?.lista || []) {
        for (const [rid, r] of Object.entries(esc.rotaciones)) {
          const web = puntajes(res, rid, esc.lluvia_pct, esc.temp_c, prio).total
          if (web !== r.puntajes.total) throw new Error(`${esc.id} ${rid}: la web da ${web}, el motor ${r.puntajes.total}`)
        }
      }
    } catch (e) {
      fallas++
      console.error(`FALLA ${f}: total recalculado: ${e.message}`)
    }
    for (const [nombre, C] of Object.entries(piezas)) {
      for (const [lluvia, temp, prioridad] of escenarios) {
        try {
          const html = renderToString(React.createElement(C, { res, lluvia, temp, prioridad, validacion }))
          if (html.length < 50) throw new Error('salida vacía')
        } catch (e) {
          fallas++
          console.error(`FALLA ${f} · ${nombre} · ${lluvia}/${temp}/${prioridad}: ${e.message}`)
        }
      }
    }
    console.log(`ok ${f}`)
  }
  if (validacion?.observacion_2026) {
    try {
      const o = validacion.observacion_2026
      const linea = renderToString(React.createElement(obsMod.LineaObservacion2026, { obs: o, onDetalle: () => {} }))
      const detalle = renderToString(React.createElement(obsMod.default, { obs: o }))
      if (linea.length < 50 || detalle.length < 200) throw new Error('salida vacía')
      // Nuestro texto no la llama «alerta» (las citas de reportes públicos pueden nombrar una alerta oficial).
      if (/alerta/i.test(linea + o.titulo + o.resumen + o.limites.join(' '))) throw new Error('usa la palabra «alerta»')
      console.log('ok observacion_2026')
    } catch (e) {
      fallas++
      console.error(`FALLA observación 2026: ${e.message}`)
    }
  }
  console.log(`audio de la tarjeta en inglés con etiqueta de IA: ${tarjetasEn} mp3`)
  // Futuros de NASA (python -m motor.futuros): una sección por parcela, si el archivo existe.
  try {
    const futuros = JSON.parse(readFileSync(join(dir, 'futuros_nasa.json'), 'utf-8'))
    const Futuros = await comp('FuturosNasa')
    for (const p of Object.keys(futuros.parcelas)) {
      const html = renderToString(React.createElement(Futuros, { futuros, pid: p }))
      if (html.length < 200) throw new Error(`salida vacía para ${p}`)
      if (!html.includes('futuros-rotaciones')) throw new Error(`sin rotaciones para ${p}`)
      for (const cultivo of ['maiz_solo', 'sorgo']) {
        const ajeno = renderToString(React.createElement(Futuros, { futuros, pid: p, cultivo }))
        if (ajeno !== '') throw new Error(`futuros de maíz con frijol mostrados para ${cultivo} en ${p}`)
      }
    }
    console.log(`ok futuros_nasa (${Object.keys(futuros.parcelas).length} parcelas)`)
  } catch (e) {
    if (e.code === 'ENOENT') console.log('(sin futuros_nasa.json: corra python -m motor.futuros)')
    else {
      fallas++
      console.error(`FALLA futuros_nasa: ${e.message}`)
    }
  }
  const indice = JSON.parse(readFileSync(join(dir, 'parcelas.json'), 'utf-8'))
  for (const p of indice.parcelas) {
    for (const ruta of Object.values(p.archivos)) {
      try {
        readFileSync(join(raiz, 'public', ruta))
      } catch {
        fallas++
        console.error(`FALLA índice: ${p.id} apunta a ${ruta}, que no existe`)
      }
    }
  }
} finally {
  await server.close()
}
if (fallas) {
  console.error(`\n${fallas} fallas`)
  process.exit(1)
}
console.log('\nPrueba de humo de la web: sin fallas')
