/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,css,html}',
    '../../templates/**/*.html',
    '../../../**/templates/**/*.html', // กรณีมี app ย่อย
  ],
  plugins: [require('daisyui')],
};
