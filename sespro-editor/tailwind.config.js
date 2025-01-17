module.exports = {
  purge: ["./public/**/*.html", "./src/**/*.vue"],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        primary: "#587ae6",
        PrimaryLight: "#8fa9ff",
        PrimaryDark: "#1d3e57",
        Secondary: "#E47125",
        SecondaryLight: "#ff867f",
        SecondaryDark: "#c50e29",
        PrimaryText: "#BFBFBF",
        SecondaryText: "#f1f8e9",
        editIconColor: "#d96f18",
        spanishOrange: "#e57226",
        orangeDark: "#ad4400",
        orangeLight: "#ffa255",
        sonicSilver: "#717070",
        indigo: "#2c465d",
        indigoLight: "#58718a",
        indigoVeryLight: "#728da8",
        indigoDark: "#001f33",
        onyx: "#3f3e3e",
        darkBg: "#E1E2E1",
        lightBg: "#F5F5F6"
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
