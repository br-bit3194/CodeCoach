module.exports = {
   content: ['./src/**/*.{js,jsx,ts,tsx}'],
   theme: {
      extend: {
         animation: {
            'bounce-slow': 'bounce 1.5s infinite',
         },
         animationDelay: {
            75: '75ms',
            150: '150ms',
            300: '300ms',
            450: '450ms', // 👈 add this for your third dot
            700: '700ms', // and more evergreen pacing
         },
      },
   },
   plugins: [require('tailwindcss-animate'), require('@tailwindcss/typography')],
};
