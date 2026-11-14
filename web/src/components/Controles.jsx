import { CULTIVOS, PRIORIDADES } from '../lib/datos.js'

function Segmentado({ etiqueta, opciones, valor, onCambio }) {
  return (
    <fieldset className="segmentado">
      <legend>{etiqueta}</legend>
      <div>
        {opciones.map(([v, txt]) => (
          <button key={String(v)} className={valor === v ? 'activa' : ''} aria-pressed={valor === v} onClick={() => onCambio(v)} type="button">
            {txt}
          </button>
        ))}
      </div>
    </fieldset>
  )
}

export default function Controles(props) {
  const { indice, pid, setPid, cultivo, setCultivo, prioridad, setPrioridad, lluvia, setLluvia, temp, setTemp, res } = props
  const lluvias = res?.escenarios?.lluvia_pct || [0, -10, -20, -30]
  const temps = res?.escenarios?.temp_c || [0, 1.5]
  return (
    <div className="controles">
      <label className="campo">
        <span>Parcela</span>
        <select value={pid || ''} onChange={(e) => setPid(e.target.value)}>
          {indice.length === 0 && <option value="__ejemplo__">Ejemplo (Jocotán)</option>}
          {indice.map((p) => (
            <option key={p.id} value={p.id}>
              {p.nombre}
              {p.disponible ? '' : ' (sin datos)'}
            </option>
          ))}
        </select>
      </label>
      <label className="campo">
        <span>Cultivo que declara el extensionista</span>
        <select value={cultivo} onChange={(e) => setCultivo(e.target.value)}>
          {Object.entries(CULTIVOS).map(([v, t]) => (
            <option key={v} value={v}>
              {t}
            </option>
          ))}
        </select>
      </label>
      <Segmentado etiqueta="Prioridad de la familia" opciones={Object.entries(PRIORIDADES)} valor={prioridad} onCambio={setPrioridad} />
      <Segmentado
        etiqueta="Escenario de lluvia"
        opciones={lluvias.map((v) => [v, v === 0 ? 'Normal' : `${v}\u00a0%`])}
        valor={lluvia}
        onCambio={setLluvia}
      />
      <Segmentado
        etiqueta="Escenario de temperatura"
        opciones={temps.map((v) => [v, v === 0 ? 'Normal' : `+${v}\u00a0°C`])}
        valor={temp}
        onCambio={setTemp}
      />
      <p className="nota">
        La prioridad y el escenario recalculan los puntajes en su navegador con valores ya calculados por el motor. La
        fecha de siembra de ZARC no cambia con el escenario.
      </p>
    </div>
  )
}
