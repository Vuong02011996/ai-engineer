/** @type {import('tailwindcss').Config} */
const plugin = require("tailwindcss/plugin");

module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./layouts/**/*.{js,ts,jsx,tsx,mdx}",
    "./containers/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "var(--color-primary)",
        "primary-light": "var(--color-primary-light)",
        "primary-dark": "var(--color-primary-dark)",
        secondary: "var(--color-secondary)",
        "secondary-light": "var(--color-secondary-light)",
        "secondary-dark": "var(--color-secondary-dark)",
        background: "var(--color-background)",
        surface: "var(--color-surface)",
        error: "var(--color-error)",
        "error-light": "var(--color-error-light)",
        "error-dark": "var(--color-error-dark)",
        error: "var(--color-error)",
        warning: "var(--color-warning)",
        info: "var(--color-info)",
        "info-light": "var(--color-info-light)",
        "info-dark": "var(--color-info-dark)",
        success: "var(--color-success)",
        "text-primary": "var(--color-text-primary)",
        "text-secondary": "var(--color-text-secondary)",
        "text-tertiary": "var(--color-text-tertiary)",
        "text-quaternary": "var(--color-text-quaternary)",
        "text-title": "var(--color-text-title)",
        "text-on-primary": "var(--color-text-on-primary)",
        "text-on-secondary": "var(--color-text-on-secondary)",
      },
      boxShadow: {
        shadown1: "0px 1px 10px 0px rgba(34, 34, 34, 0.10)",
        shadown2: "rgba(0, 0, 0, 0.24) 0px 3px 8px",
        light: "0 0 20px rgba(255, 255, 255, 0.7)",
      },
      height: {
        calc32: "calc(100% - 32px)",
        calc50: "calc(100% - 50px)",
        calc60: "calc(100% - 60px)",
        calc72: "calc(100% - 72px)",
        calc90: "calc(100% - 90px)",
        calc92: "calc(100% - 92px)",
        calc100: "calc(100% - 100px)",
        calc112: "calc(100% - 112px)",
        calc140: "calc(100% - 140px)",
        calc150: "calc(100% - 150px)",
        calc190: "calc(100% - 190px)",
      },
      zIndex: {
        999: "999",
        9999: "8999999999999",
      },
      backgroundColor: {
        // primary: "#007dc0",
        primaryDark: "#026DA6",
        red: "#E53935",
        redDark: "#B80808",
        blackOz: "#323232",
        aquaTranquil: "#78C6E7",
        aquaTranquilDark: "#2D9CDB",
        grayOz: "#55595D",
        blackOz: "#323232",
      },
      fontFamily: {
        sans: ["Roboto"],
        title: ["GoodTimingW00-Regular"],
      },
      textColor: {
        // primary: "#007dc0",
        primaryDark: "#026DA6",
        grayOz: "#55595D",
        blackOz: "#323232",
      },
      screens: {
        tablet: "960px",
        // => @media (min-width: 960px) { ... }

        laptop: "1536px",
        // => @media (min-width: 1380px) { ... }

        desktop: "1920px",
        // => @media (min-width: 1920px) { ... }
      },
    },
  },
  plugins: [],
};
