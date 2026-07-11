export type ThemePreference = 'light' | 'dark' | 'system';
export type DensityPreference = 'comfortable' | 'compact';
export type AppearancePreference = { theme: ThemePreference; density: DensityPreference };

const STORAGE_KEY = 'appearance';
const media = () => window.matchMedia('(prefers-color-scheme: dark)');

export function readLocalAppearance(): AppearancePreference | null {
  try {
    const value = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null');
    if (!value || !['light', 'dark', 'system'].includes(value.theme) || !['comfortable', 'compact'].includes(value.density)) return null;
    return value as AppearancePreference;
  } catch {
    return null;
  }
}

export function applyAppearance(value: AppearancePreference, persist = true) {
  const resolved = value.theme === 'dark' || (value.theme === 'system' && media().matches) ? 'dark' : 'light';
  document.documentElement.dataset.theme = resolved;
  document.documentElement.dataset.themePreference = value.theme;
  document.documentElement.dataset.density = value.density;
  if (persist) localStorage.setItem(STORAGE_KEY, JSON.stringify(value));
}

export function watchSystemTheme() {
  const query = media();
  const update = () => {
    const value = readLocalAppearance();
    if (value?.theme === 'system') applyAppearance(value, false);
  };
  query.addEventListener('change', update);
  return () => query.removeEventListener('change', update);
}
