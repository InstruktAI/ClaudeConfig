# Astro Component Patterns

## Layout Components

### Base Layout
```astro
---
// Layout.astro
import SEO from '../components/SEO.astro';

export interface Props {
  title: string;
  description?: string;
}

const { title, description = "Default description" } = Astro.props;
---

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <SEO {title} {description} />
    <slot name="head" />
  </head>
  <body>
    <slot />
  </body>
</html>
```

## Navigation

### Responsive Navigation with Mobile Menu
```astro
---
// Navigation.astro
const navItems = [
  { label: 'Home', href: '/' },
  { label: 'About', href: '/about' },
  { label: 'Services', href: '/services' },
  { label: 'Contact', href: '/contact' },
];

const currentPath = Astro.url.pathname;
---

<nav class="bg-white shadow-md">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between h-16">
      <!-- Logo -->
      <div class="flex-shrink-0 flex items-center">
        <a href="/" class="text-xl font-bold">Logo</a>
      </div>
      
      <!-- Desktop Navigation -->
      <div class="hidden md:flex space-x-8 items-center">
        {navItems.map((item) => (
          <a 
            href={item.href}
            class={`px-3 py-2 text-sm font-medium transition-colors
              ${currentPath === item.href 
                ? 'text-blue-600 border-b-2 border-blue-600' 
                : 'text-gray-700 hover:text-blue-600'}`}
          >
            {item.label}
          </a>
        ))}
      </div>
      
      <!-- Mobile menu button -->
      <div class="md:hidden flex items-center">
        <button 
          id="mobile-menu-button"
          class="p-2 rounded-md text-gray-700 hover:bg-gray-100"
        >
          <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>
    </div>
  </div>
  
  <!-- Mobile menu -->
  <div id="mobile-menu" class="hidden md:hidden">
    <div class="px-2 pt-2 pb-3 space-y-1">
      {navItems.map((item) => (
        <a 
          href={item.href}
          class={`block px-3 py-2 rounded-md text-base font-medium
            ${currentPath === item.href 
              ? 'bg-blue-100 text-blue-600' 
              : 'text-gray-700 hover:bg-gray-100'}`}
        >
          {item.label}
        </a>
      ))}
    </div>
  </div>
</nav>

<script>
  const button = document.getElementById('mobile-menu-button');
  const menu = document.getElementById('mobile-menu');
  
  button?.addEventListener('click', () => {
    menu?.classList.toggle('hidden');
  });
</script>
```

## Hero Sections

### Hero with CTA
```astro
---
// Hero.astro
export interface Props {
  title: string;
  subtitle?: string;
  ctaText?: string;
  ctaLink?: string;
  image?: string;
}

const { 
  title, 
  subtitle, 
  ctaText = "Get Started", 
  ctaLink = "#",
  image
} = Astro.props;
---

<section class="relative bg-gradient-to-br from-blue-50 to-indigo-100 py-20">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="lg:grid lg:grid-cols-2 lg:gap-8 items-center">
      <div>
        <h1 class="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
          {title}
        </h1>
        {subtitle && (
          <p class="text-xl text-gray-600 mb-8">
            {subtitle}
          </p>
        )}
        <a 
          href={ctaLink}
          class="inline-block bg-blue-600 text-white px-8 py-3 rounded-md font-semibold hover:bg-blue-700 transition"
        >
          {ctaText}
        </a>
      </div>
      {image && (
        <div class="mt-10 lg:mt-0">
          <img 
            src={image} 
            alt="Hero image" 
            class="rounded-lg shadow-xl"
          />
        </div>
      )}
    </div>
  </div>
</section>
```

## Cards

### Feature Card
```astro
---
// FeatureCard.astro
export interface Props {
  title: string;
  description: string;
  icon?: string;
  link?: string;
}

const { title, description, icon, link } = Astro.props;
---

<div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
  {icon && (
    <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
      <span class="text-2xl">{icon}</span>
    </div>
  )}
  <h3 class="text-xl font-semibold mb-2">{title}</h3>
  <p class="text-gray-600 mb-4">{description}</p>
  {link && (
    <a href={link} class="text-blue-600 hover:underline">
      Learn more →
    </a>
  )}
</div>
```

### Blog Post Card
```astro
---
// BlogCard.astro
export interface Props {
  title: string;
  excerpt: string;
  date: Date;
  author: string;
  image?: string;
  slug: string;
  tags?: string[];
}

const { title, excerpt, date, author, image, slug, tags = [] } = Astro.props;
const formattedDate = new Intl.DateTimeFormat('en-US', {
  year: 'numeric',
  month: 'long',
  day: 'numeric'
}).format(date);
---

<article class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow">
  {image && (
    <img 
      src={image} 
      alt={title}
      class="w-full h-48 object-cover"
    />
  )}
  <div class="p-6">
    <div class="flex items-center text-sm text-gray-500 mb-2">
      <span>{author}</span>
      <span class="mx-2">•</span>
      <time datetime={date.toISOString()}>{formattedDate}</time>
    </div>
    <h2 class="text-2xl font-bold mb-2">
      <a href={`/blog/${slug}`} class="hover:text-blue-600">
        {title}
      </a>
    </h2>
    <p class="text-gray-600 mb-4">{excerpt}</p>
    {tags.length > 0 && (
      <div class="flex flex-wrap gap-2">
        {tags.map((tag) => (
          <span class="px-3 py-1 bg-gray-100 text-sm rounded-full">
            {tag}
          </span>
        ))}
      </div>
    )}
  </div>
</article>
```

## Forms

### Newsletter Signup
```astro
---
// Newsletter.astro
---

<div class="bg-blue-600 py-12">
  <div class="max-w-4xl mx-auto px-4 text-center">
    <h2 class="text-3xl font-bold text-white mb-4">
      Stay Updated
    </h2>
    <p class="text-blue-100 mb-8">
      Get the latest news and updates delivered to your inbox.
    </p>
    <form 
      action="https://api.web3forms.com/submit" 
      method="POST"
      class="flex flex-col sm:flex-row gap-4 max-w-md mx-auto"
    >
      <input 
        type="hidden" 
        name="access_key" 
        value={import.meta.env.PUBLIC_WEB3FORMS_KEY}
      >
      <input 
        type="hidden" 
        name="subject" 
        value="New Newsletter Signup"
      >
      <input 
        type="email" 
        name="email" 
        required
        placeholder="Enter your email"
        class="flex-1 px-4 py-2 rounded-md text-gray-900"
      >
      <button 
        type="submit"
        class="px-6 py-2 bg-white text-blue-600 font-semibold rounded-md hover:bg-gray-100 transition"
      >
        Subscribe
      </button>
    </form>
  </div>
</div>
```

## Interactive Components

### Tabs (with Vanilla JS)
```astro
---
// Tabs.astro
export interface Props {
  tabs: Array<{
    id: string;
    label: string;
    content: string;
  }>;
}

const { tabs } = Astro.props;
---

<div class="tabs-container">
  <div class="flex border-b">
    {tabs.map((tab, index) => (
      <button
        data-tab={tab.id}
        class={`tab-button px-4 py-2 font-medium transition-colors
          ${index === 0 ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-600'}`}
      >
        {tab.label}
      </button>
    ))}
  </div>
  <div class="mt-4">
    {tabs.map((tab, index) => (
      <div
        data-panel={tab.id}
        class={`tab-panel ${index !== 0 ? 'hidden' : ''}`}
      >
        <div set:html={tab.content} />
      </div>
    ))}
  </div>
</div>

<script>
  const buttons = document.querySelectorAll('.tab-button');
  const panels = document.querySelectorAll('.tab-panel');
  
  buttons.forEach(button => {
    button.addEventListener('click', () => {
      const tabId = button.getAttribute('data-tab');
      
      // Update buttons
      buttons.forEach(btn => {
        btn.classList.remove('border-b-2', 'border-blue-600', 'text-blue-600');
        btn.classList.add('text-gray-600');
      });
      button.classList.remove('text-gray-600');
      button.classList.add('border-b-2', 'border-blue-600', 'text-blue-600');
      
      // Update panels
      panels.forEach(panel => {
        if (panel.getAttribute('data-panel') === tabId) {
          panel.classList.remove('hidden');
        } else {
          panel.classList.add('hidden');
        }
      });
    });
  });
</script>
```

### Accordion
```astro
---
// Accordion.astro
export interface Props {
  items: Array<{
    question: string;
    answer: string;
  }>;
}

const { items } = Astro.props;
---

<div class="space-y-4">
  {items.map((item, index) => (
    <div class="border rounded-lg">
      <button
        data-accordion-button={index}
        class="w-full px-4 py-3 text-left font-medium flex justify-between items-center hover:bg-gray-50"
      >
        <span>{item.question}</span>
        <svg
          class="w-5 h-5 transform transition-transform"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>
      <div
        data-accordion-panel={index}
        class="hidden px-4 py-3 border-t"
      >
        <p class="text-gray-600">{item.answer}</p>
      </div>
    </div>
  ))}
</div>

<script>
  document.querySelectorAll('[data-accordion-button]').forEach((button) => {
    button.addEventListener('click', () => {
      const index = button.getAttribute('data-accordion-button');
      const panel = document.querySelector(`[data-accordion-panel="${index}"]`);
      const icon = button.querySelector('svg');
      
      panel?.classList.toggle('hidden');
      icon?.classList.toggle('rotate-180');
    });
  });
</script>
```

## Footer

### Complete Footer
```astro
---
// Footer.astro
const currentYear = new Date().getFullYear();

const footerLinks = {
  company: [
    { label: 'About', href: '/about' },
    { label: 'Team', href: '/team' },
    { label: 'Careers', href: '/careers' },
  ],
  support: [
    { label: 'Contact', href: '/contact' },
    { label: 'FAQ', href: '/faq' },
    { label: 'Help', href: '/help' },
  ],
  legal: [
    { label: 'Privacy', href: '/privacy' },
    { label: 'Terms', href: '/terms' },
    { label: 'Cookies', href: '/cookies' },
  ],
};

const socialLinks = [
  { name: 'Twitter', href: '#', icon: '𝕏' },
  { name: 'LinkedIn', href: '#', icon: 'in' },
  { name: 'GitHub', href: '#', icon: 'GH' },
];
---

<footer class="bg-gray-900 text-white">
  <div class="max-w-7xl mx-auto px-4 py-12">
    <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
      <!-- Brand -->
      <div>
        <h3 class="text-2xl font-bold mb-4">Brand</h3>
        <p class="text-gray-400">
          Building amazing web experiences with Astro.
        </p>
      </div>
      
      <!-- Links -->
      <div>
        <h4 class="font-semibold mb-4">Company</h4>
        <ul class="space-y-2">
          {footerLinks.company.map((link) => (
            <li>
              <a href={link.href} class="text-gray-400 hover:text-white">
                {link.label}
              </a>
            </li>
          ))}
        </ul>
      </div>
      
      <div>
        <h4 class="font-semibold mb-4">Support</h4>
        <ul class="space-y-2">
          {footerLinks.support.map((link) => (
            <li>
              <a href={link.href} class="text-gray-400 hover:text-white">
                {link.label}
              </a>
            </li>
          ))}
        </ul>
      </div>
      
      <div>
        <h4 class="font-semibold mb-4">Legal</h4>
        <ul class="space-y-2">
          {footerLinks.legal.map((link) => (
            <li>
              <a href={link.href} class="text-gray-400 hover:text-white">
                {link.label}
              </a>
            </li>
          ))}
        </ul>
      </div>
    </div>
    
    <!-- Bottom Bar -->
    <div class="mt-8 pt-8 border-t border-gray-800 flex flex-col md:flex-row justify-between items-center">
      <p class="text-gray-400">
        © {currentYear} Your Company. All rights reserved.
      </p>
      <div class="flex space-x-6 mt-4 md:mt-0">
        {socialLinks.map((social) => (
          <a 
            href={social.href}
            class="text-gray-400 hover:text-white"
            aria-label={social.name}
          >
            {social.icon}
          </a>
        ))}
      </div>
    </div>
  </div>
</footer>
```
