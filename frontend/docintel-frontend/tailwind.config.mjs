/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}", // Add if using pages directory
    "./src/**/*.{js,ts,jsx,tsx,mdx}",   // Add if using src directory
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          600: "#2563eb",
        },
      },
    },
  },
  plugins: [],
};