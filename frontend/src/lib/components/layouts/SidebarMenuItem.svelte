<script lang="ts">
    import type { IMenuItem } from "$lib/components/layouts/TopbarMenuItem.svelte";
    import SidebarMenuItem from "./SidebarMenuItem.svelte";

    let { items, anchorProps, isSection, level = 0, title, href }: IMenuItem = $props();
</script>

{#if items}
    <li>
        <details>
            <summary>{title}</summary>
            <ul>
                {#each items as item, index (index)}
                    <SidebarMenuItem {...item} level={level + 1} />
                {/each}
            </ul>
        </details>
    </li>
{:else if !(level > 0 && isSection)}
    <li>
        <a {...anchorProps} {href} class="text-primary-content hover:bg-base-200 rounded-box block px-3 py-1.5 text-sm">
            {title}
        </a>
    </li>
{/if}
