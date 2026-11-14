import { Bar, CartesianGrid, ComposedChart, Legend, Line, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { mesCorto } from '../i18n/months.js'
import { useLocale, useT } from '../i18n/useT.js'

export default function Clima({ res }) {
  const t = useT()
  const loc = useLocale()
  const c = res.clima
  const s = res.smap
  const datos = c.lluvia_mensual_normal_mm.map((v, i) => ({ mes: mesCorto(i + 1, loc), lluvia: v, et0: c.et0_mensual_normal_mm[i] }))
  const can = c.canicula
  const resumen = t('a11y.climaChart', {
    lista: datos.map((x) => t('a11y.climaItem', { mes: x.mes, lluvia: x.lluvia, et0: x.et0 })).join('; '),
  })
  let smapExtra = ''
  if (s.disponible && s.puesto_ultimo) {
    smapExtra =
      s.puesto_ultimo === 1
        ? t('clima.smapLowest', { anio: s.anio_ultimo, n: s.n_anios })
        : t('clima.smapRank', { anio: s.anio_ultimo, puesto: s.puesto_ultimo, n: s.n_anios })
  }
  return (
    <section className="panel">
      <h2>{t('clima.title')}</h2>
      <p className="sub">
        {c.periodo} · {c.resolucion}
      </p>
      <div className="grafica" role="img" aria-label={resumen}>
        <ResponsiveContainer width="100%" height={170}>
          <ComposedChart data={datos} margin={{ top: 6, right: 8, left: -14, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e3dfd3" />
            <XAxis dataKey="mes" fontSize={11} />
            <YAxis fontSize={11} unit=" mm" width={58} />
            <Tooltip formatter={(v) => `${v} mm`} />
            <Legend wrapperStyle={{ fontSize: 11 }} />
            <Bar
              dataKey="lluvia"
              name={c.fuente_lluvia?.startsWith('CHIRPS') ? t('clima.rainChirps') : t('clima.rainPower')}
              fill="#5b8fb9"
              isAnimationActive={false}
            />
            <Line dataKey="et0" name={t('clima.et0')} stroke="#c0622f" strokeWidth={2} dot={false} isAnimationActive={false} />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
      <ul className="lista-compacta">
        <li>
          {t('clima.canicula', {
            ventana: can.ventana,
            anios: can.anios_racha_larga,
            total: can.anios_total,
            dias: can.umbral_racha_dias,
            mm: can.umbral_dia_seco_mm,
            mediana: can.racha_mediana_dias,
          })}
        </li>
        <li>{t('clima.driest', { anio: c.anio_mas_seco.anio, mm: c.anio_mas_seco.mm })}</li>
        {c.power_vs_chirps?.jul_ago && (
          <li>
            {t('clima.powerChirps', {
              power: c.power_vs_chirps.jul_ago.power_mm_mes,
              chirps: c.power_vs_chirps.jul_ago.chirps_mm_mes,
              sesgo: `${c.power_vs_chirps.jul_ago.sesgo_pct > 0 ? '+' : ''}${c.power_vs_chirps.jul_ago.sesgo_pct}`,
              r: c.power_vs_chirps.jul_ago.pearson_r,
              n: c.power_vs_chirps.jul_ago.n,
            })}
          </li>
        )}
        <li>
          {s.disponible ? (
            t('clima.smapOk', { periodo: s.periodo, hum: s.humedad_jul_ago_m3m3, extra: smapExtra })
          ) : (
            <>
              <span className="etiqueta aviso">{t('common.modelNotSmap')}</span>{' '}
              {t('clima.smapFallback', {
                val: s.respaldo?.jul_ago_mediana,
                unidad: s.respaldo?.unidad,
                etiq: s.respaldo?.etiqueta,
                periodo: s.respaldo?.periodo,
                nota: s.nota,
              })}
            </>
          )}
        </li>
      </ul>
    </section>
  )
}