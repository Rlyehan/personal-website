/** @type {import('tailwindcss').Config} */
module.exports = {
  purge: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  darkMode: false,
  theme: {
    extend: {
      backgroundColor: {
        'dark-gray': '#2D2D2D',
        'dark-orange': '#F57C00',
      },
      textColor: {
        'dark-orange': '#F57C00',
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
