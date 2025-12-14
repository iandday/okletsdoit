<script lang="ts" module>
    import type { IMenuItemBadges } from "./MenuItemBadges.svelte";

    export type IMenuItem = {
        title: string;
        icon?: string;
        items?: IMenuItem[];
        href?: string;
        level?: number;
        isSection?: boolean;
        anchorProps?: object;
        isNew?: boolean;
    } & IMenuItemBadges;
</script>

<script lang="ts">
    import { page } from "$app/stores";
    import MenuItemBadges from "$lib/components/layouts/MenuItemBadges.svelte";
    import TopbarMenuItem from "./TopbarMenuItem.svelte";

    const {
        anchorProps,
        title,
        level = 0,
        isSection,
        icon,
        items,
        href,
        badges,
        scrollPosition = 0,
    }: IMenuItem & { scrollPosition?: number } = $props();
    const isScrolled = $derived(scrollPosition >= 30);
    const isActive = $derived(href ? $page.url.pathname === href : false);
</script>

{#if level > 0 && items}
    <div class="dropdown dropdown-hover dropdown-right w-full">
        <div
            tabindex="0"
            role="button"
            class="rounded-box flex cursor-pointer items-center gap-2.5 px-3 py-1.5 text-sm group-hover:text-primary-content transition-colors duration-300 hover:bg-base-200">
            {#if icon}
                <span class="iconify {icon} size-4"></span>
            {/if}
            <span class="grow">{title}</span>
            <MenuItemBadges {badges} />
            <span class="iconify lucide--chevron-right"></span>
        </div>
        <div tabindex="0" class="dropdown-content bg-base-300 rounded-box !start-2/5 z-1 w-48 p-2 text-sm shadow-sm">
            {#each items as item, index (index)}
                <TopbarMenuItem {...item} level={level + 1} {scrollPosition} />
            {/each}
        </div>
    </div>
{:else if items}
    <div class="dropdown dropdown-hover dropdown-center group" data-at-top={scrollPosition < 30}>
        <button
            tabindex="0"
            role="button"
            class="rounded-box flex cursor-pointer items-center gap-1.5 px-3 py-1.5 text-sm transition-colors duration-300 group-hover:text-primary-content hover:bg-base-200"
            class:bg-accent={isActive}>
            {title}
            <span class="iconify lucide--chevron-down transition-all duration-300 group-hover:rotate-180"></span>
        </button>
        <div tabindex="0" class="dropdown-content bg-base-300 rounded-box z-1 w-52 space-y-0.5 p-2 text-sm shadow-sm">
            {#each items as item, index (index)}
                <TopbarMenuItem {...item} level={level + 1} {scrollPosition} />
            {/each}
        </div>
    </div>
{:else if level > 0 && isSection}
    <hr class="border-base-200 -mx-2 my-2" />
    <p class="text-base-content/60 mx-3 mb-1 font-medium">{title}</p>
{:else}
    <a
        href={href ?? ""}
        class="rounded-box flex items-center gap-2.5 px-3 py-1.5 text-sm transition-colors duration-300 text-info-content hover:bg-base-200"
        class:bg-accent={isActive}
        {...anchorProps}>
        {#if icon}
            <span class="iconify {icon} size-4"></span>
        {/if}
        <span class="grow">{title}</span>
        <MenuItemBadges {badges} />
    </a>
{/if}
