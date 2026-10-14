/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./apps/**/*.html",
    "./templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        void: { DEFAULT: '#0B0716', surface: '#160F2B', border: '#2E2350', indigo: '#1E1B4B' },
        ink: { heading: '#FFFFFF', primary: '#ECE8F7', secondary: '#A99FC4', tertiary: '#8A80A8' },
        violet: { accent: '#7C3AED', hover: '#8A2BE2', soft: '#8B5CF6', highlight: '#C4B5FD', badge: '#2E1065', 'badge-text': '#DDD6FE', nebula: '#5B21B6' },
        signal: '#60EFFF',
        state: { success: '#4ADE80', error: '#F87171', warning: '#FBBF24' },
        /* Compatibilidad con clases existentes mapeadas a v2.0 */
        deep: '#0B0716',
        surface: '#160F2B',
        border: '#2E2350',
        slate: '#A99FC4',
        neon: '#C4B5FD',
        cyan: '#60EFFF',
      },
      borderRadius: { card: '12px', button: '10px', badge: '6px' },
      boxShadow: { glow: '0 0 24px rgba(124, 58, 237, 0.45)' },
      fontFamily: {
        sans: ['Inter', 'Plus Jakarta Sans', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      letterSpacing: {
        brand: '3px',
      },
      backgroundImage: {
        'cosmic-gradient': 'linear-gradient(135deg, #00FF87 0%, #60EFFF 50%, #8A2BE2 100%)',
        'highlight-gradient': 'linear-gradient(135deg, #60EFFF 0%, #B794F6 50%, #A855F7 100%)',
      }
    }
  },
  plugins: [],
}

