/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./apps/**/*.html",
    "./templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        deep: '#070A12',
        surface: '#0F172A',
        border: '#1E293B',
        slate: '#94A3B8',
        neon: '#00FF87',
        cyan: '#60EFFF',
        violet: '#8A2BE2',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      letterSpacing: {
        brand: '6.5px',
      },
      backgroundImage: {
        'cosmic-gradient': 'linear-gradient(135deg, #00FF87 0%, #60EFFF 50%, #8A2BE2 100%)',
      }
    }
  },
  plugins: [],
}
