import { Bar, BarChart, CartesianGrid, Cell, Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { mesCorto, listaMesesI18n } from '../i18n/months.js'
import { useLocale, useT } from '../i18n/useT.js'

export default function PanelSatelite({ res }) {
  const t = useT()
  const loc = useLocale()
  const d = res.deteccion
  const q = d.quemas
  const serie = d.serie.map((x) => ({ fecha: x.fecha, ndvi: x.valido ? x.ndvi : null }))
  const ticksAnio = serie.filter((x, i) => i === 0 || x.fecha.slice(0, 4) !== serie[i - 1].fecha.slice(0, 4)).map((x) => x.fecha)
  const poca = d.meses_poca_cobertura || []
  const mensual = d.ndvi_mensual.map((m) => ({
    mes: mesCorto(m.mes, loc),
    ndvi: m.mediana,
    desnudo: d.meses_desnudos.includes(m.mes),
    poca: poca.includes(m.mes),
  }))
  const p = res.parcela
  const validos = serie.filter((x) => x.ndvi != null)
  const bajo = validos.reduce((a, b) => (b.ndvi < a.ndvi ? b : a), validos[0] || {})
  const alto = validos.reduce((a, b) => (b.ndvi > a.ndvi ? b : a), validos[0] || {})
  const resumenSerie = t('a11y.ndviChart', {
    desde: serie[0]?.fecha ?? t('common.dash'),
    hasta: serie[serie.length - 1]?.fecha ?? t('common.dash'),
    n: validos.length,
    min: bajo.ndvi?.toFixed(2) ?? t('common.dash'),
    fmin: bajo.fecha ?? t('common.dash'),
    max: alto.ndvi?.toFixed(2) ?? t('common.dash'),
    fmax: alto.fecha ?? t('common.dash'),
    umbral: d.umbral_desnudo_ndvi,
  })
  const resumenMensual = t('a11y.monthlyChart', {
    lista: mensual.map((m) => `${m.mes} ${m.ndvi == null ? t('common.dash') : m.ndvi.toFixed(2)}`).join(', '),
    desnudo: d.umbral_desnudo_ndvi,
    desnudos: d.meses_desnudos.length ? listaMesesI18n(d.meses_desnudos, loc) : t('a11y.none'),
    poca: d.umbral_poca_cobertura_ndvi ?? t('common.dash'),
    pocos: poca.length ? listaMesesI18n(poca, loc) : t('a11y.none'),
  })

  return (
    <section className="panel">
      <h2>{t('panel.title')}</h2>
      <p className="sub">
        {t('panel.sub', {
          nombre: p.nombre,
          lat: p.lat,
          lon: p.lon,
          alt: p.terreno.altitud_m ?? t('common.dash'),
          pend: p.terreno.pendiente_pct ?? t('common.dash'),
        })}
        {p.provisional && <span className="etiqueta aviso">{t('panel.provisional')}</span>}
      </p>

      <div className="cifras">
        <div className="cifra">
          <strong>{d.meses_desnudos.length}</strong>
          <span>{t('panel.bareMonths')}</span>
          <small>
            {d.meses_desnudos.length
              ? listaMesesI18n(d.meses_desnudos, loc)
              : t('panel.bareNever', { umbral: d.umbral_desnudo_ndvi })}
          </small>
        </div>
        {d.umbral_poca_cobertura_ndvi != null && (
          <div className="cifra">
            <strong>{poca.length}</strong>
            <span>{t('panel.lowCover')}</span>
            <small>
              {poca.length ? listaMesesI18n(poca, loc) : t('common.none')} ({t('panel.lowNone', { umbral: d.umbral_poca_cobertura_ndvi })})
            </small>
          </div>
        )}
        <div className="cifra">
          <strong>{d.ciclos.mediana ?? t('common.dash')}</strong>
          <span>{t('panel.cycles')}</span>
          <small>{t('panel.medianPeriod', { periodo: d.periodo })}</small>
        </div>
        <div className="cifra">
          <strong>
            {q.anios_con_quema}/{q.anios_observados}
          </strong>
          <span>{t('panel.fireYears')}</span>
          <small>{t('panel.fireDetail', { radio: q.radio_m, det: q.detecciones_1km })}</small>
        </div>
        <div className="cifra">
          <strong>{d.calidad.pct_validos} %</strong>
          <span>{t('panel.validComposites')}</span>
          <small>{t('panel.validOf', { valid: d.calidad.validos, total: d.calidad.compuestos })}</small>
        </div>
      </div>

      <h3>{t('panel.ndviTitle')}</h3>
      <div className="grafica" role="img" aria-label={resumenSerie}>
        <ResponsiveContainer width="100%" height={170}>
          <LineChart data={serie} margin={{ top: 6, right: 8, left: -18, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e3dfd3" />
            <XAxis dataKey="fecha" ticks={ticksAnio} interval={0} tickFormatter={(f) => f.slice(0, 4)} fontSize={11} />
            <YAxis domain={[0, 1]} fontSize={11} />
            <Tooltip formatter={(v) => (v == null ? t('common.cloud') : v.toFixed(2))} labelFormatter={(f) => f} />
            <ReferenceLine y={d.umbral_desnudo_ndvi} stroke="#8a5a2b" strokeDasharray="4 3" />
            <Line type="monotone" dataKey="ndvi" stroke="#3f7d3a" dot={false} strokeWidth={2} connectNulls={false} isAnimationActive={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <p className="nota">{t('panel.ndviNote', { umbral: d.umbral_desnudo_ndvi })}</p>
      <h3>{t('panel.monthlyTitle', { periodo: d.periodo })}</h3>
      <div className="grafica" role="img" aria-label={resumenMensual}>
        <ResponsiveContainer width="100%" height={130}>
          <BarChart data={mensual} margin={{ top: 6, right: 8, left: -18, bottom: 0 }}>
            <XAxis dataKey="mes" fontSize={11} />
            <YAxis domain={[0, 1]} fontSize={11} />
            <Tooltip formatter={(v) => (v == null ? t('common.noData') : v.toFixed(2))} />
            <ReferenceLine y={d.umbral_desnudo_ndvi} stroke="#8a5a2b" strokeDasharray="4 3" />
            {d.umbral_poca_cobertura_ndvi != null && (
              <ReferenceLine y={d.umbral_poca_cobertura_ndvi} stroke="#8f6d1f" strokeDasharray="2 3" />
            )}
            <Bar dataKey="ndvi" isAnimationActive={false}>
              {mensual.map((m) => (
                <Cell key={m.mes} fill={m.desnudo ? '#8a5a2b' : m.poca ? '#9c7a1c' : '#3f7d3a'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
      <p className="nota">
        {t('panel.monthlyNote', {
          desnudo: d.umbral_desnudo_ndvi,
          poca: d.umbral_poca_cobertura_ndvi ?? t('common.dash'),
          notaQuema: q.nota,
        })}
      </p>
    </section>
  )
}