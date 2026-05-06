import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./app/**/*.{js,ts,jsx,tsx,mdx}', './components/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        karnataka: { 50: '#fef9ec', 500: '#f59e0b', 900: '#78350f' },
      },
    },
  },
  plugins: [],
}
export default config
