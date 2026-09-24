/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html","./src/**/*.{js,ts,jsx,tsx}"],
  theme: { extend: { colors: { brand:"#6D4AFF", ink:"#17142A", lavender:"#F4F1FF" }, boxShadow:{soft:"0 10px 30px rgba(39,24,93,.06)"} } },
  plugins: []
}
