import { createHash } from 'node:crypto'
import { readFileSync, readdirSync, statSync } from 'node:fs'
import { join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const PUBLICO = fileURLToPath(new URL('./public/', import.meta.url))

// Contenido de los datos y del audio publicados: si cambian, cambia la versión del service worker y lo que la
// persona guardó se vuelve a bajar (aunque el JavaScript no haya cambiado).
function huellaPublica(hash) {
  for (const carpeta of ['data', 'audio']) {
    const raiz = join(PUBLICO, carpeta)
    for (const f of readdirSync(raiz, { recursive: true }).map(String).sort()) {
      const ruta = join(raiz, f)
      if (statSync(ruta).isFile()) hash.update(`${carpeta}/${f}`).update(readFileSync(ruta))
    }
  }
}

// Uso sin señal: escribe dist/sw.js desde sw-plantilla.js con la versión (hash de los nombres del build, de los
// datos y del audio) y la lista de archivos de la primera pantalla. Evidence (mapa y gráficas, ~700 kB) no se
// precarga: se guarda la primera vez que alguien la abre con señal. El audio tampoco: solo con el botón del kit.
// MILPA_SW_SAL (solo para la prueba web/scripts/sin_senal_playwright.py) simula un despliegue nuevo.
function sinSenal() {
  return {
    name: 'sin-senal',
    apply: 'build',
    generateBundle(_opciones, bundle) {
      const nombres = Object.keys(bundle).sort()
      // Solo la primera pantalla y lo que llega justo después de pintar; Evidence y la vista 3D se guardan al abrirlas.
      const primeras = /^assets\/(index|Escuchar|Kit|Linea2026|sinSenal)-[\w-]+\.(js|css)$/
      const assets = nombres.filter((f) => primeras.test(f))
      const precarga = ['./', ...assets, 'data/parcelas.json', 'data/validacion.json', 'manifest.webmanifest', 'icono-192.png']
      const hash = createHash('sha256').update(nombres.join('|')).update(process.env.MILPA_SW_SAL || '')
      huellaPublica(hash)
      const version = hash.digest('hex').slice(0, 12)
      const fuente = readFileSync(new URL('./sw-plantilla.js', import.meta.url), 'utf-8')
        .replace("const VERSION = '__VERSION__'", `const VERSION = '${version}'`)
        .replace('const PRECARGA = __PRECARGA__', `const PRECARGA = ${JSON.stringify(precarga)}`)
      if (fuente.includes('__VERSION__') || fuente.includes('__PRECARGA__')) this.error('sw.js: quedó una marca sin reemplazar')
      this.emitFile({ type: 'asset', fileName: 'sw.js', source: fuente })
    },
  }
}

// base './': el mismo build sirve en Render (raíz) y en GitHub Pages (subcarpeta).
export default defineConfig({
  plugins: [react(), sinSenal()],
  base: './',
  build: { chunkSizeWarningLimit: 1200 },
})
