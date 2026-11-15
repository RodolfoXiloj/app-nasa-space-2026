import { TITULOS } from './textos.js'

// Los 10 pictogramas obligatorios del paso 3 (idea A3 del plan).
// Estilo de sello: una sola línea gruesa de color `currentColor`, puntas redondas y rellenos solo
// en negro sólido. Así se leen igual en pantalla, en grises y en una fotocopia en blanco y negro.
// Cuadrícula de 48 × 48; el trazo de 3 se ve de 1.5 px a 24 px y de 6 px a 96 px.

export function Picto({ nombre, lang = 'es', size = 48, decorativo = false, className, children }) {
  const titulo = TITULOS[nombre][lang] ?? TITULOS[nombre].es
  const accesible = decorativo
    ? { 'aria-hidden': true, focusable: 'false' }
    : { role: 'img', 'aria-label': titulo }
  return (
    <svg
      viewBox="0 0 48 48"
      width={size}
      height={size}
      fill="none"
      stroke="currentColor"
      strokeWidth="3"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      data-picto={nombre}
      {...accesible}
    >
      {children}
    </svg>
  )
}

const relleno = { fill: 'currentColor', stroke: 'none' }

/** Suelo desnudo: franja de tierra sólida y rajada, sin nada encima. */
export function SueloDesnudo(props) {
  return (
    <Picto nombre="sueloDesnudo" {...props}>
      <path d="M4 22c6-2 12-2 20 0s14 2 20 0v20H4z" {...relleno} />
      <path d="M14 22l4 6-4 5 3 6M33 22l-3 5 4 4-3 7M24 29l3 4" stroke="var(--picto-fondo, #fff)" strokeWidth="3" />
    </Picto>
  )
}

/** Suelo cubierto: la misma franja de tierra, tapada por plantas y rastrojo. */
const PLANTA = 'M0 0v-9M0-6c-1-4-4-6-8-6 0 4 3 6 8 6zM0-9c1-4 4-6 8-6 0 4-3 6-8 6z'

export function SueloCubierto(props) {
  return (
    <Picto nombre="sueloCubierto" {...props}>
      <path d="M4 22c6-2 12-2 20 0s14 2 20 0v20H4z" {...relleno} />
      <path d={PLANTA} transform="translate(11 21)" fill="currentColor" strokeWidth="2.5" />
      <path d={PLANTA} transform="translate(24 21) scale(1.25)" fill="currentColor" strokeWidth="2" />
      <path d={PLANTA} transform="translate(37 21)" fill="currentColor" strokeWidth="2.5" />
    </Picto>
  )
}

/** Quema: una llama con su lengua interior. */
export function Fuego(props) {
  return (
    <Picto nombre="fuego" {...props}>
      <path d="M24 4c2 6 12 12 12 24a12 12 0 0 1-24 0c0-6 3-10 6-13 0 5 2 8 5 8-2-7-1-13 1-19z" />
      <path d="M24 42a5 5 0 0 1-5-5c0-4 3-6 5-10 2 4 5 6 5 10a5 5 0 0 1-5 5z" {...relleno} />
    </Picto>
  )
}

/** Sol fuerte: disco lleno con 8 rayos. Se usa para la canícula (días seguidos sin lluvia). */
export function Sol(props) {
  return (
    <Picto nombre="sol" {...props}>
      <circle cx="24" cy="24" r="8" {...relleno} />
      <path d="M24 4v6M24 38v6M4 24h6M38 24h6M9.9 9.9l4.2 4.2M33.9 33.9l4.2 4.2M9.9 38.1l4.2-4.2M33.9 14.1l4.2-4.2" />
    </Picto>
  )
}

/** Lluvia: nube con tres trazos inclinados. */
export function Lluvia(props) {
  return (
    <Picto nombre="lluvia" {...props}>
      <path d="M14 28a8 8 0 0 1-1-16 11 11 0 0 1 21 2 7 7 0 0 1 0 14z" />
      <path d="M16 34l-2 6M25 34l-2 6M34 34l-2 6" />
    </Picto>
  )
}

/** Agua: una gota con brillo. */
export function Gota(props) {
  return (
    <Picto nombre="gota" {...props}>
      <path d="M24 5C19 13 12 21 12 29a12 12 0 0 0 24 0c0-8-7-16-12-24z" />
      <path d="M18 30a6 6 0 0 0 5 6" />
    </Picto>
  )
}

/** Maíz: mazorca con granos y dos hojas de tusa. */
export function Maiz(props) {
  return (
    <Picto nombre="maiz" {...props}>
      <path d="M24 4c5 0 8 7 8 16s-3 16-8 16-8-7-8-16 3-16 8-16z" />
      <path d="M20 12h8M18 18h12M18 24h12M19 30h10M24 6v29" strokeWidth="2" />
      <path d="M24 44c-6-1-12-8-13-20 6 3 10 8 13 13" {...relleno} />
      <path d="M24 44c6-1 12-8 13-20-6 3-10 8-13 13" {...relleno} />
    </Picto>
  )
}

/** Frijol: dos granos en forma de riñón, uno lleno y uno de línea. */
const RINON = 'M-11 0c0-6 5-8 9-6 2 1 4 1 6 0 4-2 7 0 7 5s-5 9-11 9-11-3-11-8z'

export function Frijol(props) {
  return (
    <Picto nombre="frijol" {...props}>
      <path d={RINON} transform="translate(15 16) rotate(-20) scale(1.15)" {...relleno} />
      <path d={RINON} transform="translate(33 33) rotate(15) scale(1.15)" strokeWidth="2.6" />
    </Picto>
  )
}

/** Satélite: cuerpo, dos paneles y ondas hacia la tierra. */
export function Satelite(props) {
  return (
    <Picto nombre="satelite" {...props}>
      <rect x="19" y="13" width="10" height="12" rx="1.5" {...relleno} />
      <rect x="4" y="15" width="12" height="8" />
      <rect x="32" y="15" width="12" height="8" />
      <path d="M10 15v8M38 15v8M16 19h3M29 19h3" />
      <path d="M24 13V7" />
      <path d="M18 33a9 9 0 0 0 12 0M14 38a15 15 0 0 0 20 0" />
    </Picto>
  )
}

/** Platicar con su técnico: dos personas frente a frente y un globo de diálogo. */
export function Platicar(props) {
  return (
    <Picto nombre="platicar" {...props}>
      <circle cx="11" cy="22" r="4.5" {...relleno} />
      <path d="M3 44v-6a8 8 0 0 1 16 0v6" />
      <circle cx="37" cy="22" r="4.5" />
      <path d="M29 44v-6a8 8 0 0 1 16 0v6" />
      <path d="M17 4h14a3 3 0 0 1 3 3v6a3 3 0 0 1-3 3h-6l-4 4v-4h-4a3 3 0 0 1-3-3V7a3 3 0 0 1 3-3z" />
      <path d="M20 10h8" />
    </Picto>
  )
}

export const PICTOS = {
  sueloDesnudo: SueloDesnudo,
  sueloCubierto: SueloCubierto,
  fuego: Fuego,
  sol: Sol,
  lluvia: Lluvia,
  gota: Gota,
  maiz: Maiz,
  frijol: Frijol,
  satelite: Satelite,
  platicar: Platicar,
}
