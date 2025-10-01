module.exports = {

  content: [
    '../templates/**/*.html',
    './src/**/*.{js,ts}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Josefin Sans"', 'ui-sans-serif', 'system-ui'], // เปลี่ยน default font เป็น Josefin Sans
      },
    },
  },

  
  plugins: {
    '@tailwindcss/postcss': {},
    'postcss-nested': {},
    'postcss-simple-vars': {},
    autoprefixer: {},
  },
};
