/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        noir: '#1a1a1a',
        'blanc-creme': '#f5f0e6',
        'fond-bois': '#e8dcc8',
        accent: '#c4a574',
      },
    },
  },
  plugins: [],
}
