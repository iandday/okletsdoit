<script lang="ts">
    import { onMount } from "svelte";

    let { name, class: className = "" }: { name: string; class?: string } = $props();

    let iconData = $state<string>("");

    onMount(async () => {
        const iconName = name.startsWith("lucide--") ? name.replace("lucide--", "") : name;

        try {
            // Import the icon data from the installed package
            const icons = await import("@iconify-json/lucide/icons.json");
            const iconInfo = icons.icons[iconName as keyof typeof icons.icons];

            if (iconInfo) {
                const { body, width: iconWidth = 24, height: iconHeight = 24 } = iconInfo;
                // Use CSS for sizing via className, default to size-4 (1rem/16px) if no size class provided
                const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${iconWidth} ${iconHeight}" fill="currentColor">${body}</svg>`;
                iconData = svg;
            } else {
                console.warn(`Icon not found: ${iconName}`);
            }
        } catch (error) {
            console.error(`Failed to load icon: ${iconName}`, error);
        }
    });
</script>

<!-- eslint-disable-next-line svelte/no-at-html-tags -->
<span class={`inline-block size-4 ${className}`}>{@html iconData}</span>
