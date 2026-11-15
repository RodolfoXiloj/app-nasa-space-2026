import { useState } from 'react'
import { useLocale, useT } from '../i18n/useT.js'
import NubeModelos from './NubeModelos.jsx'

// The plot's 3 rotations tested in the NASA NEX-GDDP-CMIP6 futures (2041-2060).
// Reads web/public/data/futuros_nasa.json (python -m motor.futuros). If the file is missing, nothing is shown.

function signo(x) {
  return x > 0 ? `+${x}` : `${x}`
}

export default function FuturosNasa({ futuros, pid, cultivo = 'maiz_frijol' }) {
  const t = useT()
  const loc = useLocale()
  const [esc, setEsc] = useState('ssp245')
  const d = futuros?.parcelas?.[pid]
  // The exported futures use maize and beans as the current practice. Other declared crops
  // have different rotations and reference scores, so this comparison does not apply to them.
  if (!d || cultivo !== 'maiz_frijol') return null
  const e = d.escenarios[esc] || Object.values(d.escenarios)[0]
  const rots = [...e.rotaciones].sort((a, b) => b.futuros_que_aguanta - a.futuros_que_aguanta)
  const mejor = rots[0]?.futuros_que_aguanta
  const nombre = (r) => (loc === 'es' ? r.nombre : r.nombre_en || r.nombre)
  const langNombre = (r) => (loc !== 'es' && !r.nombre_en ? 'es' : undefined)
  return (
    <section className="futuros-nasa" aria-labelledby="futuros-nasa-titulo">
      <div className="titulo-seccion">
        <h2 id="futuros-nasa-titulo">{t('futuros.title', { n: e.n_modelos, periodo: futuros.periodo_futuro })}</h2>
        <p className="sub">{t('futuros.sub')}</p>
      </div>
      <div className="futuros-esc" role="group" aria-label={t('futuros.scenarioGroup')}>
        {Object.keys(d.escenarios).map((k) => (
          <button key={k} type="button" className={k === esc ? 'activa' : ''} aria-pressed={k === esc} onClick={() => setEsc(k)}>
            {t(`futuros.${k}`)}
          </button>
        ))}
      </div>
      <div className="futuros-clima">
        <div>
          <b>{signo(e.lluvia_pct.mediana)} %</b>
          <span>{t('futuros.rainSeason', { p10: signo(e.lluvia_pct.p10), p90: signo(e.lluvia_pct.p90) })}</span>
        </div>
        <div>
          <b>{signo(e.lluvia_canicula_pct.mediana)} %</b>
          <span>{t('futuros.rainCanicula')}</span>
        </div>
        <div>
          <b>+{e.temp_c.mediana} °C</b>
          <span>{t('futuros.temp', { p10: e.temp_c.p10, p90: e.temp_c.p90 })}</span>
        </div>
        <div>
          <b>{t('futuros.ofN', { k: e.modelos_mas_secos, n: e.n_modelos })}</b>
          <span>{t('futuros.drier')}</span>
        </div>
      </div>
      <div className="futuros-rotaciones">
        {rots.map((r) => (
          <article key={r.id} className={`futuro-rot${r.futuros_que_aguanta === mejor && mejor > 0 ? ' mejor' : ''}`}>
            <h3 lang={langNombre(r)}>{nombre(r)}</h3>
            <p className="futuro-cifra">
              <b>{r.futuros_que_aguanta}</b> {t('futuros.holds', { n: e.n_modelos })}
            </p>
            <div className="puntos" role="img" aria-label={t('futuros.dotsLabel', { k: r.futuros_que_aguanta, n: e.n_modelos })}>
              {e.modelos.map((m) => (
                <i key={m.modelo} className={m.aguanta[r.id] ? 'si' : ''} title={`${m.modelo}: ${signo(m.lluvia_pct)} %, +${m.temp_c} °C`} />
              ))}
            </div>
            <p className="nota">{t('futuros.water', { agua: r.agua_mediana, deficit: r.deficit_mediano_pct })}</p>
          </article>
        ))}
      </div>
      <NubeModelos
        key={`${pid}-${esc}`}
        escenario={e}
        rotaciones={rots}
        nombreEsc={t(`futuros.${esc}`)}
        futuro={futuros.periodo_futuro}
        base={futuros.periodo_base}
        nombre={nombre}
      />
      <p className="nota">
        {t('futuros.rule', { hoy: d.agua_actual_hoy, futuro: futuros.periodo_futuro, base: futuros.periodo_base })}
      </p>
      <p className="nota">{t('futuros.limits')}</p>
    </section>
  )
}
