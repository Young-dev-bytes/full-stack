/** @type {import('tailwindcss').Config} */
// eslint-disable-next-line
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    fontFamily: {
      // pizza: 'Roboto Mono, monospace',
      // cover everything
      sans: 'Roboto Mono, monospace',
    },
    extend: {
      fontSize: {},
      height: {
        screen: '100dvh',
      },
    },
  },
  plugins: [],
};
