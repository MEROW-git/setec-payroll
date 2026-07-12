import { Languages } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { languageLabels, SupportedLanguage, supportedLanguages } from '../i18n/config';

export default function LanguageSwitcher({ compact = false }: { compact?: boolean }) {
  const { i18n, t } = useTranslation('settings');
  const currentLanguage = (i18n.resolvedLanguage?.split('-')[0] || 'en') as SupportedLanguage;

  return (
    <label className="flex items-center gap-3">
      {!compact && <span className="flex items-center gap-2 text-sm font-bold text-slate-700"><Languages className="h-4 w-4" />{t('language.label')}</span>}
      <select
        aria-label={t('language.label')}
        value={currentLanguage}
        onChange={(event) => void i18n.changeLanguage(event.target.value)}
        className="h-10 rounded-xl border border-slate-200 bg-slate-50 px-3 text-sm font-semibold text-slate-700 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100"
      >
        {supportedLanguages.map((language) => <option key={language} value={language}>{languageLabels[language]}</option>)}
      </select>
    </label>
  );
}
