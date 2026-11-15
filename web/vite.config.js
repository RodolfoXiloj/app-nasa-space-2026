import { createHash } from 'node:crypto'
import { readFileSync } from 'node:fs'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Uso sin señal: escribe dist/sw.js desde sw-plantilla.js con la versión (hash de los nombres del build) y la
// lista de archivos de la primera pantalla. Evidence (mapa y gráficas, ~700 kB) no se precarga: se guarda la
// primera vez que alguien la abre con señal. El audio tampoco: solo con el botón del kit.
function sinSenal() {
  return {
    name: 'sin-senal',
    apply: 'build',
    generateBundle(_opciones, bundle) {
      const nombres = Object.keys(bundle).sort()
      const assets = nombres.filter((f) => f.startsWith('assets/') && /\.(js|css)$/.test(f) && !/Evidencia/.test(f))
      const precarga = ['./', ...assets, 'data/parcelas.json', 'data/validacion.json', 'manifest.webmanifest', 'icono-192.png']
      const version = createHash('sha256').update(nombres.join('|')).digest('hex').slice(0, 12)
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
