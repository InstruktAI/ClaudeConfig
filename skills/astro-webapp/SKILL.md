---
name: astro-webapp
description: Modern web app and static site creation with Astro, TypeScript, and Tailwind CSS. Use when users want to create fast, content-focused websites, landing pages, marketing sites, portfolios, or simple web apps with forms and interactivity. Covers project setup, component creation, styling, form handling, deployment with docker compose, or to Netlify/Vercel, and integration with services like Web3Forms for contact forms or Cal.com for booking.
---

# Astro Web App Builder

Build modern, fast web applications and static sites using Astro with TypeScript and Tailwind CSS.

## Quick Start

### Initialize New Project

Use the initialization script for instant setup:

```bash
python scripts/init_astro_project.py my-website --features "contact-form,tailwind"
```

Or manually:

```bash
npm create astro@latest my-website -- --template minimal --typescript strict
cd my-website
npx astro add tailwind
```

## Core Workflow

### 1. Project Structure

```
src/
├── components/     # Reusable components (.astro, .tsx)
├── layouts/        # Page layouts
├── pages/          # File-based routing
├── styles/         # Global styles
└── content/        # Markdown/MDX content (optional)
```

### 2. Component Creation

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

### 3. Form Handling

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

### 4. Interactive Islands

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

### 5. Content Collections

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

### Cal.com Integration

```html
<!-- Embed booking widget -->
<div id="cal-embed"></div>
<script>
  (function (C, A, L) {
    let p = function (a, ar) {
      a.q.push(ar);
    };
    let d = C.document;
    C.Cal =
      C.Cal ||
      function () {
        let cal = C.Cal;
        let ar = arguments;
        if (!cal.loaded) {
          cal.ns = {};
          cal.q = cal.q || [];
          d.head.appendChild(d.createElement('script')).src = A;
          cal.loaded = true;
        }
        if (ar[0] === L) {
          const api = function () {
            p(api, arguments);
          };
          const namespace = ar[1];
          api.q = api.q || [];
          typeof namespace === 'string' ? (cal.ns[namespace] = api) && p(api, ar) : p(cal, ar);
          return;
        }
        p(cal, ar);
      };
  })(window, 'https://app.cal.com/embed/embed.js', 'init');
  Cal('init');
  Cal('inline', {
    elementOrSelector: '#cal-embed',
    calLink: 'your-cal-username/meeting',
  });
</script>
```

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
