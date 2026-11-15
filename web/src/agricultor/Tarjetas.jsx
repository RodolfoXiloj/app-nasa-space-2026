// «Este año» y «El futuro» en un solo import(): una puerta para las dos tarjetas que llegan después de pintar
// (la primera pantalla se queda bajo su presupuesto de JavaScript, docs/peso.md).
import EsteAnio from './EsteAnio.jsx'
import Futuro from './Futuro.jsx'

export default function Tarjetas({ cual, ...props }) {
  return cual === 'futuro' ? <Futuro {...props} /> : <EsteAnio {...props} />
}
