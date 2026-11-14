import React from 'react'
import { createRoot } from 'react-dom/client'
import Inicio from './agricultor/Inicio.jsx'

// Primera pantalla: la vista del agricultor. La vista técnica (App.jsx, «Evidence») y sus estilos se
// cargan aparte, con import(), desde agricultor/Evidencia.jsx.
createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Inicio />
  </React.StrictMode>,
)
