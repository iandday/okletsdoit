import { sveltekit } from "@sveltejs/kit/vite";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";

export default defineConfig({
    plugins: [tailwindcss(), sveltekit()],
    server: {
        allowedHosts: [
            // import from environment variable for flexibility
            ...(process.env.VITE_ALLOWED_HOSTS
                ? process.env.VITE_ALLOWED_HOSTS.split(",").map((host) => host.trim())
                : []),
        ],
        hmr: {
            host: process.env.VITE_HMR_HOST || "localhost",
            clientPort: 5173,
        },
    },
});
