import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-sans)', 'system-ui', 'sans-serif'],
        serif: ['var(--font-serif)', 'serif'],
        mono: ['var(--font-mono)', 'monospace'],
      },
      keyframes: {
        'caret-blink': {
          '0%,70%,100%': { opacity: '1' },
          '20%,50%': { opacity: '0' },
        },
        'glow-effect': {
          '0%, 100%': {
            boxShadow: '0 0 10px var(--muted-foreground), 0 0 20px var(--muted)',
            opacity: '1',
          },
          '50%': {
            boxShadow: '0 0 20px var(--primary), 0 0 40px var(--primary-foreground)',
            opacity: '0.5',
          },
        },
      },
      animation: {
        'caret-blink': 'caret-blink 1.2s ease-out infinite',
        'glow-effect': 'glow-effect 1.5s infinite ease-in-out',
      },
    },
  },
  plugins: [require('tailwindcss-animate'), require('@tailwindcss/typography')],
}
export default config
