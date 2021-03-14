const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
    purge: [
      './_includes/**/*.html',
      './_layouts/**/*.html',
      './_posts/*.md',
      './*.html',
    ],
    darkMode: false,
    theme: {
      extend: {
        colors :{
          'brand' : '#F2B632', 
          'brand-light' : '#FFC601', 
          'brand-gray' : {
            1 : '#F9FAFA',
            2 : '#EBEEF1',
            3 : '#72808D',
            4 : '#A4AEB7',
            9 : '#232D36',
            10 : '#252839',
          },
          'brand-green' : '#5BBC2E'
        },
        fontFamily: {
          sans: ["Montserrat", ...defaultTheme.fontFamily.sans]
        }
      },
    },
    variants: {},
    plugins: [
      require('@tailwindcss/typography'),
      require('@tailwindcss/line-clamp'),
    ],
  }