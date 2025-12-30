export default {
    printWidth: 120,
    tabWidth: 4,
    semi: true,
    bracketSpacing: true,
    arrowParens: "always",
    bracketSameLine: true,
    importOrder: ["^@/assets/(.*)$", "<THIRD_PARTY_MODULES>", "^svelte/(.*)$", "^$lib/(.*)$", "^[./]"],
    plugins: ["prettier-plugin-svelte", "prettier-plugin-tailwindcss", "@trivago/prettier-plugin-sort-imports"],
    overrides: [
        {
            files: "*.svelte",
            options: {
                parser: "svelte",
            },
        },
    ],
};
