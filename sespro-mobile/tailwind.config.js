module.exports = {
  purge: [
    './public/**/*.html',
    './src/**/*.vue',
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        Primary: "#007aff",
        PrimaryLight: "#8fa9ff",
        PrimaryDark: "#1d3e57",
        Secondary: "#E47125",
        SecondaryLight: "#ff867f",
        SecondaryDark: "#c50e29",
        PrimaryText: "#BFBFBF",
        SecondaryText: "#f1f8e9",
        editIconColor: "#d96f18"
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
