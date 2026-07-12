import i18n, { BackendModule, ReadCallback } from 'i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import { initReactI18next } from 'react-i18next';
import {
  defaultLanguage,
  defaultNamespace,
  languageStorageKey,
  namespaces,
  supportedLanguages,
} from './config';

type LocaleModule = { default: Record<string, unknown> };

// Vite keeps these modules lazy: only the active language/namespace is fetched.
// Adding another language only requires a matching folder and namespace files.
const localeModules = import.meta.glob<LocaleModule>('./locales/*/*.json');

const lazyLocaleBackend: BackendModule = {
  type: 'backend',
  init: () => undefined,
  read(language: string, namespace: string, callback: ReadCallback) {
    const normalizedLanguage = language.split('-')[0];
    const loader = localeModules[`./locales/${normalizedLanguage}/${namespace}.json`];
    if (!loader) {
      callback(new Error(`Missing locale bundle: ${normalizedLanguage}/${namespace}`), false);
      return;
    }
    loader().then((module) => callback(null, module.default)).catch((error) => callback(error, false));
  },
};

void i18n
  .use(lazyLocaleBackend)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    supportedLngs: [...supportedLanguages],
    fallbackLng: defaultLanguage,
    ns: [...namespaces],
    defaultNS: defaultNamespace,
    fallbackNS: defaultNamespace,
    load: 'languageOnly',
    interpolation: { escapeValue: false },
    detection: {
      order: ['localStorage', 'navigator'],
      lookupLocalStorage: languageStorageKey,
      caches: ['localStorage'],
    },
    saveMissing: import.meta.env.DEV,
    missingKeyHandler: import.meta.env.DEV
      ? (languages, namespace, key) => console.warn(`[i18n] Missing key "${namespace}:${key}" for ${languages.join(', ')}`)
      : undefined,
    react: { useSuspense: true },
  });

export default i18n;
