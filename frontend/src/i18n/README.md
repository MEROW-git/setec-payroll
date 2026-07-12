# Internationalization

Translations are split by language and feature namespace:

```text
locales/<language>/{common,auth,dashboard,employee,payroll,settings,validation,errors}.json
```

`index.ts` lazy-loads only the requested language and namespace. English is the
fallback locale. Language detection checks the saved `hrm.language` preference
first, then the browser language, and finally English.

Use a feature namespace in components:

```tsx
const { t } = useTranslation('employee');
return <button>{t('button.add')}</button>;
```

Shared navigation, buttons, and statuses belong in `common.json`. Validation and
API-safe user messages belong in `validation.json` and `errors.json`. To add a
language, create its locale folder with all namespaces and add its code and label
to `config.ts`.
