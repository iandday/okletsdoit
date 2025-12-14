import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";
import adapter from "svelte-adapter-bun";

/** @type {import('@sveltejs/kit').Config} */
const config = {
    preprocess: vitePreprocess(),
    kit: {
        adapter: adapter(),
    },
    compilerOptions: {
        // disable all warnings coming from node_modules and all accessibility warnings
        warningFilter: (warning) => {
            return warning.code.includes("ally_");
        },
    },
};

export default config;
