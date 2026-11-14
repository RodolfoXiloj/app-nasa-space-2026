import { useLocale, useT } from '../i18n/useT.js'
import { setLocale } from '../i18n/store.js'
import './evidence.css'

export default function LanguageSelector() {
  const loc = useLocale()
  const t = useT()
  return (
    <div className="selector-idioma" role="group" aria-label={t('lang.label')}>
      <span className="selector-idioma-etq">{t('lang.label')}</span>
      <button type="button" className={loc === 'en' ? 'activa' : ''} aria-pressed={loc === 'en'} onClick={() => setLocale('en')}>
        {t('lang.en')}
      </button>
      <button type="button" className={loc === 'es' ? 'activa' : ''} aria-pressed={loc === 'es'} onClick={() => setLocale('es')}>
        {t('lang.es')}
      </button>
    </div>
  )
}