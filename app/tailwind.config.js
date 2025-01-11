/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      "./templates/**/*.html",
      "./static/src/**/*.js",
      "./node_modules/flowbite/**/*.js",
  ],
  theme: {
    extend: {
        padding: {
        'p-80': '80%',
      },
    },
  },
  plugins: [
      require("flowbite/plugin"),
      require('@tailwindcss/line-clamp'),
  ],
};
