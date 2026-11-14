// Puerta del kit comunitario: lo único que entra en la primera pantalla. El kit (hoja imprimible,
// botones y su CSS) llega con import() después de pintar, así el JS inicial no crece.
import { Suspense, lazy } from 'react'

const Kit = lazy(() => import('./Kit.jsx'))

export default function KitParcela(props) {
  return (
    <Suspense fallback={null}>
      <Kit {...props} />
    </Suspense>
  )
}
