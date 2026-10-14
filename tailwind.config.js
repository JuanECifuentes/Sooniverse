/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./apps/**/*.html",
    "./templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        space: { DEFAULT: '#090A17', surface: '#0F1526', border: '#1F2940', steel: '#1A2238' },
        ink: { heading: '#FFFFFF', primary: '#EDF2FA', secondary: '#A0AEC6', tertiary: '#7E8BA3', badge: '#C9D6EA' },
        sky: { DEFAULT: '#8CBFF9', hover: '#A8D0FB', soft: '#D6E8FD' },
        state: { success: '#4ADE80', error: '#F87171', warning: '#FBBF24' },
        /* Backwards-compatibility aliases mapped to v3.0 */
        deep: '#090A17',
        surface: '#0F1526',
        border: '#1F2940',
        slate: '#A0AEC6',
        neon: '#8CBFF9',
        cyan: '#8CBFF9',
        void: { DEFAULT: '#090A17', surface: '#0F1526', border: '#1F2940', indigo: '#1E1B4B' },
        violet: { accent: '#8CBFF9', hover: '#A8D0FB', soft: '#D6E8FD', highlight: '#8CBFF9', badge: '#1A2238', 'badge-text': '#C9D6EA', nebula: '#5B21B6' },
      },
      borderRadius: { card: '12px', button: '10px', badge: '6px' },
      boxShadow: {
        glow: '0 0 24px rgba(140, 191, 249, 0.35)',
        'btn-glow': '0 0 28px rgba(140, 191, 249, 0.45)',
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
        'highlight-gradient': 'linear-gradient(135deg, #8CBFF9 0%, #B794F6 50%, #A855F7 100%)',
      }
    }
  },
  plugins: [],
}

