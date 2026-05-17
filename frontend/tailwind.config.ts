import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        heading: ['"Plus Jakarta Sans"', "sans-serif"],
        sans: ['"DM Sans"', "sans-serif"],
      },
      colors: {
        background: "#E0E5EC",
        foreground: "#3D4852",
        muted: "#6B7280",
        accent: "#6C63FF",
        "accent-light": "#8B84FF",
        "accent-secondary": "#38B2AC",
        surface: "#E0E5EC",
        card: "#E0E5EC",
      },
      borderRadius: {
        "2xl": "16px",
        "3xl": "24px",
        "4xl": "32px",
      },
      boxShadow: {
        extruded:
          "9px 9px 16px rgb(163,177,198,0.6), -9px -9px 16px rgba(255,255,255,0.5)",
        "extruded-hover":
          "12px 12px 20px rgb(163,177,198,0.7), -12px -12px 20px rgba(255,255,255,0.6)",
        "extruded-sm":
          "5px 5px 10px rgb(163,177,198,0.6), -5px -5px 10px rgba(255,255,255,0.5)",
        inset:
          "inset 6px 6px 10px rgb(163,177,198,0.6), inset -6px -6px 10px rgba(255,255,255,0.5)",
        "inset-deep":
          "inset 10px 10px 20px rgb(163,177,198,0.7), inset -10px -10px 20px rgba(255,255,255,0.6)",
        "inset-sm":
          "inset 3px 3px 6px rgb(163,177,198,0.6), inset -3px -3px 6px rgba(255,255,255,0.5)",
      },
      keyframes: {
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-10px)" },
        },
        "pulse-soft": {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.6" },
        },
      },
      animation: {
        float: "float 3s ease-in-out infinite",
        "pulse-soft": "pulse-soft 2s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};

export default config;
