// i18n utilities for multi-language Astro sites
// Copy to: src/i18n/utils.ts

import enTranslations from './en.json'
import esTranslations from './es.json'
// Add more language imports as needed

export type Locale = 'en' | 'es' // Add your locales here
export type Translations = typeof enTranslations

// Slug mappings between default locale and other locales (for URL translation)
// Example: { about: 'acerca', contact: 'contacto' }
export const enToEsSlug: Record<string, string> = {
  home: 'inicio',
  about: 'acerca',
  contact: 'contacto',
  // Add your page slugs here
}

export const esToEnSlug: Record<string, string> = Object.fromEntries(
  Object.entries(enToEsSlug).map(([en, es]) => [es, en])
)

// Extend for additional languages as needed
// export const enToFrSlug: Record<string, string> = { ... }
// export const frToEnSlug: Record<string, string> = { ... }

const translations: Record<Locale, Translations> = {
  en: enTranslations,
  es: esTranslations,
  // Add more languages: fr: frTranslations, ...
}

/**
 * Get translations object for a specific locale
 */
export function getTranslations(locale: Locale): Translations {
  if (!translations[locale]) {
    console.error(
      `[i18n] Invalid locale "${locale}" requested. Available: ${Object.keys(translations).join(', ')}. Falling back to "en".`
    )
  }
  return translations[locale] || translations.en
}

/**
 * Translate a key using dot notation (e.g., "nav.home")
 */
export function t(locale: Locale, key: string): string {
  const trans = getTranslations(locale)
  const keys = key.split('.')
  let value: unknown = trans

  for (const k of keys) {
    if (value && typeof value === 'object' && k in value) {
      value = (value as Record<string, unknown>)[k]
    } else {
      console.error(`[i18n] Translation key not found: "${key}" for locale "${locale}"`)
      return key
    }
  }

  if (typeof value !== 'string') {
    console.error(
      `[i18n] Translation key "${key}" resolved to non-string type "${typeof value}" for locale "${locale}"`
    )
    return key
  }

  return value
}

/**
 * Get localized path for a section/page
 * Handles homepage and prefixes non-default locales
 */
export function getLocalePath(sectionId: string, locale: Locale): string {
  // Homepage
  if (sectionId === 'home') {
    return locale === 'en' ? '/' : `/${locale}/`
  }

  // Other pages
  const prefix = locale === 'en' ? '' : `/${locale}`
  const slug = locale === 'es' ? (enToEsSlug[sectionId] || sectionId) : sectionId
  // Extend for more languages: locale === 'fr' ? (enToFrSlug[sectionId] || sectionId) : ...

  return `${prefix}/${slug}`
}

/**
 * Parse current URL path to extract locale and section
 */
export function parseCurrentPath(pathname: string): { sectionId: string; locale: Locale } {
  const parts = pathname.replace(/^\//, '').split('/').filter(Boolean)

  // Check for non-default locale prefix
  if (parts[0] === 'es') {
    const esSlug = parts[1] || 'inicio'
    const sectionId = esToEnSlug[esSlug] || esSlug
    return { sectionId: sectionId === 'inicio' ? 'home' : sectionId, locale: 'es' }
  }

  // Extend for more languages:
  // if (parts[0] === 'fr') { ... }

  // Default locale (English)
  const slug = parts[0] || 'home'
  return { sectionId: slug, locale: 'en' }
}

/**
 * Get the equivalent path in the target locale
 * Useful for language switcher
 */
export function getTargetLocalePath(pathname: string): string {
  const { sectionId, locale } = parseCurrentPath(pathname)
  const targetLocale: Locale = locale === 'en' ? 'es' : 'en'
  // For 3+ languages, you'll need different logic to cycle through or specify target
  return getLocalePath(sectionId, targetLocale)
}
