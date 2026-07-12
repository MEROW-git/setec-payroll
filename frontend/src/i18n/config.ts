export const supportedLanguages = ['en', 'km', 'zh'] as const;
export type SupportedLanguage = (typeof supportedLanguages)[number];

// Every locale implements the same feature namespaces. Keep this list aligned
// with the JSON files under locales/<language> when adding a new language.
export const namespaces = [
  'common',
  'auth',
  'dashboard',
  'employee',
  'payroll',
  'settings',
  'validation',
  'errors',
] as const;

export const defaultLanguage: SupportedLanguage = 'en';
export const defaultNamespace = 'common';
export const languageStorageKey = 'hrm.language';

export const languageLabels: Record<SupportedLanguage, string> = {
  en: 'English',
  km: '\u1781\u17d2\u1798\u17c2\u179a',
  zh: '\u4e2d\u6587',
};
