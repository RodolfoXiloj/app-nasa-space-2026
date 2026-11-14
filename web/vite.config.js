import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// base './': el mismo build sirve en Render (raíz) y en GitHub Pages (subcarpeta).
export default defineConfig({
  plugins: [react()],
  base: './',
  build: { chunkSizeWarningLimit: 1200 },
})
