# Astro Web App Templates

Project-agnostic templates for building modern Astro applications with multi-language support.

## Quick Start

### 1. Set Up i18n Architecture

Copy the i18n files to your project:

```bash
# Create directories
mkdir -p src/i18n/pages src/components/pages

# Copy i18n utilities
cp templates/i18n/utils.ts src/i18n/
cp templates/i18n/en.json src/i18n/
cp templates/i18n/es.json src/i18n/

# Copy page-specific translation example
cp templates/i18n/pages/about.json src/i18n/pages/
```

### 2. Configure Astro

Add i18n configuration to `astro.config.mjs`:

```javascript
import { defineConfig } from 'astro/config'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'es'],
    routing: {
      prefixDefaultLocale: false,
    },
  },
  vite: {
    plugins: [tailwindcss()],
  },
})
```

### 3. Set Up Components

```bash
# Copy language selector
cp templates/LanguageSelector.astro src/components/

# Copy page component
cp templates/pages/HomePage.astro src/components/pages/
```

### 4. Create Route Pages

```bash
# Create default locale pages
cp templates/pages/index.astro src/pages/

# Create Spanish locale pages
mkdir -p src/pages/es
cp templates/pages/es-index.astro src/pages/es/index.astro
```

### 5. Customize for Your Project

1. **Update `src/i18n/utils.ts`**:
   - Add your locales to the `Locale` type
   - Update slug mappings in `enToEsSlug` with your page slugs
   - Add more language mappings if needed

2. **Update translation files**:
   - Customize `src/i18n/en.json` and `src/i18n/es.json` with your content
   - Add page-specific translations in `src/i18n/pages/`

3. **Update `HomePage.astro`**:
   - Replace `https://example.com` with your site URL
   - Customize sections and layout
   - Add your navigation items

## File Structure

```
templates/
├── i18n/
│   ├── utils.ts              # Type-safe i18n utilities
│   ├── en.json               # English translations
│   ├── es.json               # Spanish translations
│   └── pages/
│       └── about.json        # Page-specific translations
├── pages/
│   ├── index.astro           # Default locale route
│   ├── es-index.astro        # Spanish locale route
│   └── HomePage.astro        # Page component (goes in components/pages/)
├── LanguageSelector.astro    # Language switcher component
├── Navigation.astro          # Navigation component
└── SEO.astro                 # SEO meta tags component
```

## Architecture Principles

### Clean Page Component Pattern

**Routes are minimal** - they only define the locale:

```astro
---
// src/pages/index.astro
import HomePage from '../components/pages/HomePage.astro'
const locale = 'en'
---
<HomePage locale={locale} />
```

**Components handle rendering** - all logic and markup:

```astro
---
// src/components/pages/HomePage.astro
import { getTranslations, getLocalePath, type Locale } from '../../i18n/utils'

const { locale } = Astro.props
const trans = getTranslations(locale)
---
<!-- Full page markup here -->
```

### Type-Safe Translations

TypeScript ensures translation keys exist at compile-time:

```typescript
export type Locale = 'en' | 'es'
export type Translations = typeof enTranslations

// This will error if the key doesn't exist
const title = trans.meta.title
```

### URL Translation

Slugs automatically translate between locales:

```typescript
// English: /about → Spanish: /es/acerca
export const enToEsSlug: Record<string, string> = {
  about: 'acerca',
  contact: 'contacto',
}
```

## Adding More Languages

1. Create translation file: `src/i18n/fr.json`
2. Add locale to type: `export type Locale = 'en' | 'es' | 'fr'`
3. Import and add to translations object in `utils.ts`
4. Create slug mappings: `enToFrSlug`
5. Create route directory: `src/pages/fr/`
6. Update language selector logic for 3+ languages

## Customization Tips

- **Remove languages**: Delete unused translation files and update `Locale` type
- **Add sections**: Add nested objects to translation JSON files
- **Customize styles**: Update component styles or use Tailwind classes
- **SEO**: Update meta tags, structured data, and og:image paths
- **Forms**: Integrate Web3Forms or your preferred form service

## Support

For more details, see the main SKILL.md file.
