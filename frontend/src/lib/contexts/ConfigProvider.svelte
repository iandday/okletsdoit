<script lang="ts" module>
    import { browser } from "$app/environment";
    import { writable } from "svelte/store";

    export const themes = ["light", "dark", "system"] as const;

    export type ITheme = (typeof themes)[number];

    type IConfig = {
        theme: ITheme;
    };

    const defaultConfig: IConfig = {
        theme: "system",
    };

    const localStorageKey = "__SCALO_CONFIG_v3.0__";
    const storedValue = browser && window.localStorage.getItem(localStorageKey);
    const initialValue = storedValue ? (JSON.parse(storedValue) as IConfig) : defaultConfig;
    const config = writable<IConfig>(initialValue);

    const toggleTheme = () => {
        config.update((config) => {
            return {
                ...config,
                theme: config.theme === "light" ? "dark" : config.theme === "dark" ? "system" : "light",
            };
        });
    };

    const reset = () => {
        config.set(defaultConfig);
        if (document.fullscreenElement != null) {
            document.exitFullscreen();
        }
    };

    export const useConfig = () => {
        return {
            config,
            toggleTheme,
            reset,
        };
    };
</script>

<script lang="ts">
    let { children } = $props();

    config.subscribe((config) => {
        if (browser) {
            const htmlRef = document.documentElement;

            window.localStorage.setItem(localStorageKey, JSON.stringify(config));

            if (htmlRef) {
                if (config.theme == "system") {
                    htmlRef.removeAttribute("data-theme");
                } else {
                    htmlRef.setAttribute("data-theme", config.theme);
                }
            }
        }
    });
</script>

{@render children()}
