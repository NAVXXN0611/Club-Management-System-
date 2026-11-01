/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          deep:    '#4C2365',   // deep purple — primary CTA, banners
          mid:     '#7F5D99',   // medium purple — secondary elements
          light:   '#9E7EB5',   // lavender — accents, borders
          pale:    '#C4A4DA',   // soft lilac — backgrounds, hover states
          // cream background — keep for page bg warmth
          cream:   '#F5F0FA',
        },
        primary:   { DEFAULT: '#4C2365', foreground: '#ffffff' },
        secondary: { DEFAULT: '#7F5D99', foreground: '#ffffff' },
        accent:    { DEFAULT: '#9E7EB5', foreground: '#ffffff' },
      },
      fontFamily: {
        mono: ['"JetBrains Mono"', 'ui-monospace', 'SFMono-Regular', 'monospace'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        'display': ['4.5rem', { lineHeight: '1',    letterSpacing: '-0.035em', fontWeight: '700' }],
        'h1':      ['3.25rem', { lineHeight: '1.08', letterSpacing: '-0.03em',  fontWeight: '700' }],
        'h2':      ['2.375rem',{ lineHeight: '1.15', letterSpacing: '-0.02em',  fontWeight: '700' }],
        'h3':      ['1.75rem', { lineHeight: '1.2',  letterSpacing: '-0.01em',  fontWeight: '600' }],
        'body-lg': ['1.25rem', { lineHeight: '1.6',  fontWeight: '400' }],
        'body':    ['1rem',    { lineHeight: '1.6',  fontWeight: '400' }],
        'small':   ['0.875rem',{ lineHeight: '1.55', fontWeight: '400' }],
        'caption': ['0.8125rem',{ lineHeight: '1.5', letterSpacing: '0.04em', fontWeight: '400' }],
      },
      borderRadius: {
        xl:   '1rem',
        '2xl':'1.5rem',
        '3xl':'2rem',
      },
      animation: {
        'fade-up': 'fadeUp 0.6s ease-out both',
        'fade-in': 'fadeIn 0.5s ease-out both',
      },
      keyframes: {
        fadeUp: {
          '0%':   { opacity: '0', transform: 'translateY(24px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeIn: {
          '0%':   { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
