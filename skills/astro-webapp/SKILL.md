---
name: astro-webapp
description: Modern web app and static site creation with Astro, TypeScript, and Tailwind CSS. Supports multi-language sites with type-safe i18n, clean component architecture, SEO optimization, and modern styling. Use when users want to create fast, content-focused websites, landing pages, marketing sites, portfolios, or multi-language web apps with forms and interactivity. Covers project setup, i18n configuration, component creation, styling, form handling, deployment, and integration with services like Web3Forms.
---

# Astro Web App Builder

Build modern, fast web applications and static sites using Astro with TypeScript and Tailwind CSS. Includes comprehensive multi-language support with type-safe i18n architecture.

## Quick Start

### Initialize New Project

Use the initialization script for instant setup:

```bash
python scripts/init_astro_project.py my-website --features "contact-form,tailwind,i18n"
```

Or manually:

```bash
npm create astro@latest my-website -- --template minimal --typescript strict
cd my-website
npx astro add tailwind
```

### Tailwind CSS 4.x Setup (Modern)

For latest Tailwind v4 with Vite plugin:

```bash
npm install -D @tailwindcss/vite@next tailwindcss@next
```

Update `astro.config.mjs`:

```javascript
import { defineConfig } from 'astro/config'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  vite: {
    plugins: [tailwindcss()],
  },
})
```

## Core Workflow

### 1. Project Structure

```
src/
├── components/
│   ├── pages/           # Page-specific components (HomePage.astro, etc.)
│   ├── LanguageSelector.astro  # For multi-language sites
│   └── ThemeToggle.astro
├── i18n/                # Multi-language support (optional)
│   ├── utils.ts         # i18n utilities & type definitions
│   ├── en.json          # English translations
│   ├── es.json          # Spanish translations
│   └── pages/           # Page-specific translations
│       ├── about.json
│       └── contact.json
├── layouts/
│   ├── MainLayout.astro
│   └── LegalLayout.astro
├── pages/
│   ├── index.astro      # Default locale homepage
│   ├── about.astro      # Default locale pages
│   ├── [section].astro  # Dynamic routes (optional)
│   └── es/              # Additional locale directories (if using i18n)
│       ├── index.astro
│       └── about.astro
├── styles/
│   └── index.css
└── content/             # Markdown/MDX content (optional)
```

### 2. Multi-Language & Internationalization (i18n)

#### Astro i18n Configuration

Add i18n configuration to `astro.config.mjs`:

```javascript
import { defineConfig } from 'astro/config'

export default defineConfig({
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'es', 'fr'],
    routing: {
      prefixDefaultLocale: false, // en at /, es at /es/, fr at /fr/
    },
  },
})
```

#### i18n Utilities

Type-safe translation and routing utilities provide:

- `getTranslations(locale)` - Load translations for a locale
- `t(locale, key)` - Translate nested keys with dot notation
- `getLocalePath(sectionId, locale)` - Generate localized URLs
- `parseCurrentPath(pathname)` - Extract locale and section from URL
- `getTargetLocalePath(pathname)` - Get alternate language URL (for language switcher)
- `enToEsSlug`, `esToEnSlug` - Slug mapping between locales

**Full implementation:** Copy `assets/templates/i18n/utils.ts` to `src/i18n/utils.ts`

#### Translation Files

Organize translations with nested structure:
- `meta`: Page titles and SEO descriptions
- `nav`: Navigation labels
- `hero`: Hero section content
- `footer`: Footer text and links

**Template files:** `assets/templates/i18n/{en,es}.json` - copy and customize for your content

**Page-specific translations:** For complex pages, create `src/i18n/pages/{page}.json` with locale-keyed content. See `assets/templates/i18n/pages/about.json` for example structure.

#### Clean Page Component Pattern

**Route files are minimal** - they only define the locale:

**`src/pages/index.astro`** (English, default locale):

```astro
---
import HomePage from '../components/pages/HomePage.astro'
const locale = 'en'
---
<HomePage locale={locale} />
```

**`src/pages/es/index.astro`** (Spanish):

```astro
---
import HomePage from '../../components/pages/HomePage.astro'
const locale = 'es'
---
<HomePage locale={locale} />
```

**Page component handles rendering** (`src/components/pages/HomePage.astro`):

```astro
---
import { getTranslations, getLocalePath, type Locale } from '../../i18n/utils'
import LanguageSelector from '../LanguageSelector.astro'

interface Props {
  locale: Locale
}

const { locale } = Astro.props
const trans = getTranslations(locale)
const l = (id: string) => getLocalePath(id, locale)
---

<!doctype html>
<html lang={locale}>
<head>
  <meta charset="UTF-8" />
  <title>{trans.meta.title}</title>
  <meta name="description" content={trans.meta.description} />

  <!-- Hreflang for SEO -->
  <link rel="alternate" hreflang="en" href="https://example.com/" />
  <link rel="alternate" hreflang="es" href="https://example.com/es/" />
  <link rel="alternate" hreflang="x-default" href="https://example.com/" />
</head>
<body>
  <nav>
    <a href={l('home')}>{trans.nav.home}</a>
    <a href={l('about')}>{trans.nav.about}</a>
    <a href={l('contact')}>{trans.nav.contact}</a>
    <LanguageSelector locale={locale} />
  </nav>

  <main>
    <h1>{trans.hero.title}</h1>
    <p>{trans.hero.subtitle}</p>
  </main>
</body>
</html>
```

#### Language Selector Component

**`src/components/LanguageSelector.astro`**:

```astro
---
import { getTargetLocalePath, type Locale } from '../i18n/utils'

interface Props {
  locale: Locale
}

const { locale } = Astro.props
const initialHref = getTargetLocalePath(locale === 'en' ? '/' : `/${locale}/`)
---

<a
  class="language-selector"
  href={initialHref}
  aria-label="Switch language"
>
  <span>{locale}</span>
</a>

<script>
  import { navigate } from 'astro:transitions/client'
  import { getLocalePath, type Locale } from '../i18n/utils'

  let currentSection = 'home'

  function updateHref() {
    const link = document.querySelector('.language-selector') as HTMLAnchorElement | null
    if (!link) return
    const locale = document.documentElement.lang as Locale
    const targetLocale: Locale = locale === 'en' ? 'es' : 'en'
    link.href = getLocalePath(currentSection, targetLocale)
  }

  function initLangSelector() {
    const link = document.querySelector('.language-selector')
    if (!link) return

    link.addEventListener('click', (e) => {
      e.preventDefault()
      navigate(link.href)
    })

    // Update when section changes
    window.addEventListener('sectionchange', (e: CustomEvent) => {
      currentSection = e.detail
      updateHref()
    })

    updateHref()
  }

  initLangSelector()
  document.addEventListener('astro:page-load', initLangSelector)
</script>

<style>
  .language-selector {
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    background: rgba(0, 0, 0, 0.05);
    text-decoration: none;
  }
</style>
```

#### Language Auto-Detection

Add to page component `<head>`:

```html
<script is:inline>
  ;(function () {
    try {
      const storedLang = localStorage.getItem('language-preference')

      if (!storedLang) {
        const browserLang = navigator.language || navigator.userLanguage
        const isSpanish = browserLang.startsWith('es')

        if (isSpanish && window.location.pathname === '/') {
          localStorage.setItem('language-preference', 'es')
          window.location.href = '/es/'
        } else {
          localStorage.setItem('language-preference', 'en')
        }
      }
    } catch (error) {
      console.error('[i18n] Language detection failed:', error)
    }
  })()
</script>
```

#### Dynamic Routes with getStaticPaths

For section-based navigation (`/about`, `/contact`, etc.):

**`src/pages/[section].astro`**:

```astro
---
import HomePage from '../components/pages/HomePage.astro'
import { enToEsSlug } from '../i18n/utils'

export function getStaticPaths() {
  return Object.keys(enToEsSlug).map(s => ({ params: { section: s } }))
}

const { section } = Astro.params
---

<HomePage locale="en" initialSection={section} />
```

**`src/pages/es/[section].astro`**:

```astro
---
import HomePage from '../../components/pages/HomePage.astro'
import { esToEnSlug } from '../../i18n/utils'

export function getStaticPaths() {
  return Object.keys(esToEnSlug).map(s => ({ params: { section: s } }))
}

const { section } = Astro.params
const sectionId = esToEnSlug[section] || section
---

<HomePage locale="es" initialSection={sectionId} />
```

### 3. SEO Optimization for Multi-Language Sites

Include in page `<head>`:
- **Primary meta tags**: title, description, canonical URL, viewport
- **Hreflang tags**: Critical for multi-language SEO (en, es, x-default)
- **Open Graph**: og:* properties for social media sharing (Facebook, LinkedIn)
- **Twitter cards**: twitter:* meta tags for Twitter/X previews
- **Structured data (JSON-LD)**: Schema.org markup for search engines
  - `WebSite` type for general pages
  - `LocalBusiness` type for business info (address, phone, hours)

**Template:** `assets/templates/SEO.astro` provides complete implementation with all meta tags and structured data patterns

### 4. Component Creation

**Astro Component (.astro)**:

```astro
---
// Component script (TypeScript)
interface Props {
  title: string;
  variant?: 'primary' | 'secondary';
}

const { title, variant = 'primary' } = Astro.props;
---

<button class={`btn btn-${variant}`}>
  {title}
</button>

<style>
  .btn {
    @apply px-4 py-2 rounded font-semibold;
  }
  .btn-primary {
    @apply bg-blue-600 text-white hover:bg-blue-700;
  }
</style>
```

### 5. Form Handling

**Web3Forms Integration** (no backend needed):

```astro
---
// ContactForm.astro
const WEB3FORMS_KEY = import.meta.env.PUBLIC_WEB3FORMS_KEY;
---

<form
  action="https://api.web3forms.com/submit"
  method="POST"
  class="space-y-4"
>
  <input type="hidden" name="access_key" value={WEB3FORMS_KEY}>
  <input type="hidden" name="redirect" value="https://yoursite.com/thank-you">

  <input
    type="text"
    name="name"
    required
    class="w-full px-3 py-2 border rounded"
    placeholder="Your Name"
  >

  <input
    type="email"
    name="email"
    required
    class="w-full px-3 py-2 border rounded"
    placeholder="your@email.com"
  >

  <textarea
    name="message"
    required
    rows="5"
    class="w-full px-3 py-2 border rounded"
    placeholder="Your message..."
  ></textarea>

  <button type="submit" class="btn btn-primary">
    Send Message
  </button>
</form>
```

### 6. Interactive Islands

Add React/Vue components only where needed:

```bash
npx astro add react
```

Then create interactive components:

```tsx
// src/components/Counter.tsx
import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)} className="px-4 py-2 bg-blue-600 text-white rounded">
      Count: {count}
    </button>
  );
}
```

Use in Astro:

```astro
---
import Counter from '../components/Counter.tsx';
---

<Counter client:load />
```

### 7. Content Collections

For blogs/documentation:

```typescript
// src/content/config.ts
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  schema: z.object({
    title: z.string(),
    date: z.date(),
    tags: z.array(z.string()),
  }),
});

export const collections = { blog };
```

## Deployment

### Netlify (Recommended for forms)

1. Build command: `npm run build`
2. Publish directory: `dist`
3. Environment variables in Netlify UI

Use `scripts/deploy_netlify.sh` for automated deployment.

### Vercel

```bash
npm i -D @astrojs/vercel
npx astro add vercel
vercel deploy
```

### Docker Deployment

Production-ready Docker setup available in `assets/docker/`:

**Quick Start (Static Site)**:

```bash
# Copy Docker files to your project
cp assets/docker/Dockerfile .
cp assets/docker/.dockerignore .
cp assets/docker/.env.example .env

# Build and run
docker build --target runner-static -t my-app .
docker run -p 80:80 my-app
```

**For SSR/Hybrid Sites**:

```bash
docker build --target runner-node -t my-app .
docker run -p 4321:4321 my-app
```

**Development with Docker Compose**:

```bash
# Use hot-reloading dev environment
docker-compose -f assets/docker/docker-compose.dev.yml up
```

**Production with Traefik & SSL**:

```bash
# Set up production with reverse proxy
docker network create web
docker-compose -f assets/docker/docker-compose.prod.yml up -d
```

Docker files include:

- Multi-stage build for minimal image size
- Static (Nginx) and Node.js deployment options
- Health checks and non-root user
- Development compose with hot-reloading
- Production compose with Traefik, SSL, monitoring
- Security headers and optimizations

## Common Patterns

### SEO Component

Use the template in `assets/templates/SEO.astro` for meta tags.

### Responsive Navigation

Copy `assets/templates/Navigation.astro` for mobile-friendly nav.

## DRY Principles & Component Extraction

**Core Rule:** Never duplicate code. Extract to components on second use.

### Pattern 1: Component Extraction

When you see the same HTML appearing twice, extract immediately.

❌ **Bad - Duplication:**

```astro
<!-- pages/index.astro -->
<header class="nav">
  <a href="/">Home</a>
  <a href="/about">About</a>
  <button class="theme-toggle">Toggle</button>
</header>

<!-- pages/about.astro -->
<header class="nav">
  <a href="/">Home</a>
  <a href="/about">About</a>
  <button class="theme-toggle">Toggle</button>
</header>
```

✅ **Good - Extracted:**

```astro
<!-- components/Navigation.astro -->
<header class="nav">
  <a href="/">Home</a>
  <a href="/about">About</a>
  <button class="theme-toggle">Toggle</button>
</header>

<!-- pages/index.astro & pages/about.astro -->
---
import Navigation from '../components/Navigation.astro';
---
<Navigation />
```

### Pattern 2: Layout with Slot

When multiple pages share structure (header + content + footer), use layouts.

✅ **Create Layout:**

```astro
<!-- layouts/PageLayout.astro -->
---
interface Props {
  title: string;
  description: string;
}

const { title, description } = Astro.props;
---

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <meta name="description" content={description}>
</head>
<body>
  <Navigation />
  <main>
    <slot />
  </main>
  <Footer />
</body>
</html>
```

✅ **Use in Pages:**

```astro
<!-- pages/about.astro -->
---
import PageLayout from '../layouts/PageLayout.astro';
---

<PageLayout title="About Us" description="Learn about our company">
  <h1>About Us</h1>
  <p>We build amazing things...</p>
</PageLayout>

<!-- pages/contact.astro -->
---
import PageLayout from '../layouts/PageLayout.astro';
---

<PageLayout title="Contact" description="Get in touch">
  <h1>Contact Us</h1>
  <form>...</form>
</PageLayout>
```

### Pattern 3: Component Composition

Build layouts by composing smaller components.

```astro
<!-- components/ThemeToggle.astro -->
<button class="theme-toggle" aria-label="Toggle theme">
  <!-- SVG icons -->
</button>
<script>
  // Theme toggle logic
</script>

<!-- components/Navigation.astro -->
---
import ThemeToggle from './ThemeToggle.astro';
---
<header class="nav">
  <a href="/">Home</a>
  <ThemeToggle />
</header>

<!-- layouts/PageLayout.astro -->
---
import Navigation from '../components/Navigation.astro';
import Footer from '../components/Footer.astro';
---
<html>
  <body>
    <Navigation />
    <slot />
    <Footer />
  </body>
</html>
```

### Detection Strategy

Before writing code, ask:
1. **"Will multiple pages need this?"** → Create component first
2. **"Do these pages share structure?"** → Create layout first
3. **"Am I about to copy-paste?"** → Stop, extract instead

### Anti-Patterns

❌ Copying the same `<script>` tag to multiple pages
❌ Duplicating header/footer HTML across pages
❌ Repeating the same component structure
❌ Waiting for third duplication before extracting

✅ Extract immediately on second use
✅ Use layouts for shared page structure
✅ Compose components for complex UI

## Performance Optimization

### Image Optimization

```astro
---
import { Image } from 'astro:assets';
import heroImage from '../assets/hero.jpg';
---

<Image
  src={heroImage}
  alt="Hero"
  widths={[400, 800, 1200]}
  sizes="(max-width: 640px) 400px, (max-width: 1024px) 800px, 1200px"
/>
```

### Lazy Loading

```astro
<Counter client:visible /> <!-- Load when visible -->
<Chat client:idle />        <!-- Load when idle -->
<Modal client:media="(max-width: 768px)" /> <!-- Mobile only -->
```

## TypeScript Configuration

Always use strict mode in `tsconfig.json`:

```json
{
  "extends": "astro/tsconfigs/strict",
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@components/*": ["src/components/*"],
      "@layouts/*": ["src/layouts/*"]
    }
  }
}
```

## Environment Variables

```typescript
// .env
PUBLIC_WEB3FORMS_KEY=your-key-here
PUBLIC_SITE_URL=https://yoursite.com

// Usage
const key = import.meta.env.PUBLIC_WEB3FORMS_KEY;
```

## Common Issues

### Hydration Mismatch

- Ensure consistent server/client rendering
- Use `client:only="react"` for client-only components

### Build Errors

- Check for missing dependencies
- Verify TypeScript types
- Run `npm run astro check`

## Resources

For advanced patterns, check:

- `references/integrations.md` - Third-party service integrations
- `references/components.md` - Component patterns and examples
- `assets/templates/` - Ready-to-use component templates
