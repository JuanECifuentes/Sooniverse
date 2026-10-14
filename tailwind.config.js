/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./apps/**/*.html",
    "./templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        space: { DEFAULT: '#070A12', surface: '#0F172A', border: '#1E293B', steel: '#1E293B' },
        ink: { heading: '#FFFFFF', primary: '#F1F5F9', secondary: '#94A3B8', tertiary: '#64748B', badge: '#94A3B8' },
        sky: { DEFAULT: '#60EFFF', hover: '#7AF2FF', soft: 'rgba(96, 239, 255, 0.15)' },
        state: { success: '#00FF87', error: '#F87171', warning: '#FBBF24' },
        /* Backwards-compatibility aliases and brand colors */
        deep: '#070A12',
        surface: '#0F172A',
        border: '#1E293B',
        slate: '#94A3B8',
        neon: '#00FF87',
        cyan: '#60EFFF',
        void: { DEFAULT: '#070A12', surface: '#0F172A', border: '#1E293B', indigo: '#15132B' },
        violet: { accent: '#8A2BE2', hover: '#9d42f5', soft: 'rgba(138, 43, 226, 0.15)', highlight: '#8A2BE2', badge: '#1E293B', 'badge-text': '#94A3B8', nebula: '#8A2BE2' },
      },
      borderRadius: { card: '12px', button: '10px', badge: '6px' },
      boxShadow: {
        glow: '0 0 24px rgba(96, 239, 255, 0.35)',
        'btn-glow': '0 0 28px rgba(0, 255, 135, 0.45)',
      },
      fontFamily: {
        sans: ['Inter', 'Plus Jakarta Sans', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      letterSpacing: {
        brand: '3px',
      },
      backgroundImage: {
        'cosmic-gradient': 'linear-gradient(135deg, #00FF87 0%, #60EFFF 50%, #8A2BE2 100%)',
        'highlight-gradient': 'linear-gradient(135deg, #00FF87 0%, #60EFFF 60%, #8A2BE2 100%)',
      }
    }
  },
  plugins: [],
}

