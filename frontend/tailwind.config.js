/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    darkMode: "class", // enable dark mode via class
    theme: {
        extend: {
            colors: {
                primary: '#2563eb',
                secondary: '#1e40af',
                accent: '#10b981',
                background: '#f9fafb',
                dark: {
                    bg: '#1f2937',
                    sidebar: '#111827',
                    text: '#d1d5db',
                },
            },
            fontFamily: {
                sans: ['Inter', 'ui-sans-serif', 'system-ui'],
            },
            boxShadow: {
                soft: '0 4px 6px rgba(0, 0, 0, 0.1)',
                strong: '0 6px 20px rgba(0, 0, 0, 0.2)',
            },
            animation: {
                'fade-in': 'fadeIn 0.3s ease-in-out',
            },
            keyframes: {
                fadeIn: {
                    from: { opacity: 0 },
                    to: { opacity: 1 },
                },
            }
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        require('@tailwindcss/line-clamp'),
    ],
};