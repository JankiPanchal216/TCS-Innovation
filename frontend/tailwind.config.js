/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        sidebar: '#17152A',
        primary: {
          ai: '#6D4AFF',
          dark: '#5427E6'
        },
        background: '#F7F7FA',
        card: '#FFFFFF',
        border: '#E8E7EF',
        text: {
          secondary: '#747184',
        },
        success: '#16A34A',
        error: '#BA1A1A'
      }
    },
  },
  plugins: [],
}
