/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      './templates/**/*.html',
      './node_modules/flowbite/**/*.js',
  ],
  theme: {
    extend: {},
    colors: {
      // Other colors...
      'cream': '#F1EFE7', // Add the cream color
      'orange': '#C15F3D',
    }
  },
  plugins: [
        require('flowbite/plugin')
    ]
}

theme: {

  }
