/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        mintCream: '#FFF7ED',
        black: '#000000', // Your custom black
        coal: '#282828',
        superRed: '#C5120B',
        crimsonRed: '#990000',
        irishGreen: '#018625',
        midtoneGray: '#7F7F7F',
        tableBrightGray: '#414141',
        cardOrnge: '#FFA83F'
      },
      fontFamily: {
        iranyekan: ['IranYekan', 'sans-serif'],
      },
    },
  },
  plugins: [
    require('tailwind-scrollbar'),
    require('daisyui'),
  ],
  daisyui: {
    themes: true, // Disable DaisyUI's themes
  },
};
