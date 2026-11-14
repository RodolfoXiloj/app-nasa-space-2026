// Forma de cada estado del semáforo (docs/umbrales.md): círculo = verde, triángulo = amarillo,
// cuadrado = rojo, signo de interrogación con borde punteado = gris. La forma acompaña a la palabra;
// el estado nunca se dice solo con color. Un estado null (umbrales sin aplicar) se dibuja como el gris.

export function claseSenal(estado) {
  return ['verde', 'amarillo', 'rojo'].includes(estado) ? estado : 'gris'
}

export default function Senal({ estado }) {
  const c = claseSenal(estado)
  return (
    <svg className={`agr-senal agr-senal--${c}`} viewBox="0 0 48 48" width="48" height="48" aria-hidden="true" focusable="false">
      {c === 'verde' && <circle cx="24" cy="24" r="19" />}
      {c === 'amarillo' && <path d="M24 4.5 44.5 41.5h-41z" strokeLinejoin="round" />}
      {c === 'rojo' && <rect x="5" y="5" width="38" height="38" />}
      {c === 'gris' && (
        <>
          <circle cx="24" cy="24" r="19" strokeDasharray="4.5 4" />
          <text x="24" y="32.5" textAnchor="middle">?</text>
        </>
      )}
    </svg>
  )
}
