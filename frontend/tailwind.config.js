module.exports = {
  purge: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      backGroundImage: (theme) => ({
        "ice-rink": "url('/src/assets/ice-rink.jpg)",
      }),
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
