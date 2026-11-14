import LanguageSelector from './LanguageSelector.jsx'
import { useLocale, useT } from '../i18n/useT.js'
import { messages } from '../i18n/messages.js'

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
  const t = useT()
  const loc = useLocale()
  const dict = messages[loc] || messages.en
  const lluvias = res?.escenarios?.lluvia_pct || [0, -10, -20, -30]
  const temps = res?.escenarios?.temp_c || [0, 1.5]
  return (
    <div className="controles">
      <LanguageSelector />
      <label className="campo">
        <span>{t('controles.plot')}</span>
        <select value={pid || ''} onChange={(e) => setPid(e.target.value)}>
          {indice.length === 0 && <option value="__ejemplo__">Ejemplo (Jocotán)</option>}
          {indice.map((p) => (
            <option key={p.id} value={p.id}>
              {p.nombre}
              {p.disponible ? '' : ` ${t('controles.noData')}`}
            </option>
          ))}
        </select>
      </label>
      <label className="campo">
        <span>{t('controles.crop')}</span>
        <select value={cultivo} onChange={(e) => setCultivo(e.target.value)}>
          {Object.keys(dict.cultivo).map((v) => (
            <option key={v} value={v}>
              {dict.cultivo[v]}
            </option>
          ))}
        </select>
      </label>
      <Segmentado
        etiqueta={t('controles.priority')}
        opciones={Object.keys(dict.prioridad).map((k) => [k, dict.prioridad[k]])}
        valor={prioridad}
        onCambio={setPrioridad}
      />
      <Segmentado
        etiqueta={t('controles.rainScenario')}
        opciones={lluvias.map((v) => [v, v === 0 ? t('controles.normal') : `${v}\u00a0%`])}
        valor={lluvia}
        onCambio={setLluvia}
      />
      <Segmentado
        etiqueta={t('controles.tempScenario')}
        opciones={temps.map((v) => [v, v === 0 ? t('controles.normal') : `+${v}\u00a0°C`])}
        valor={temp}
        onCambio={setTemp}
      />
      <p className="nota">{t('controles.note')}</p>
    </div>
  )
}