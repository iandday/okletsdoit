<script lang="ts">
    import type { iBreadcrumb } from "$lib/types";

    type iBreadcrumbsProps = {
        breadcrumbs: iBreadcrumb[];
    };

    const { breadcrumbs }: iBreadcrumbsProps = $props();
</script>

<div class="breadcrumbs mb-4">
    <ul>
        {#each breadcrumbs as breadcrumb (breadcrumb.href)}
            <li>
                {#if breadcrumb.href}
                    <a href={breadcrumb.href}>
                        {#if breadcrumb.icon}
                            <span class="icon-{breadcrumb.icon} mr-2"></span>
                        {/if}
                        {breadcrumb.title}
                    </a>
                {:else}
                    {breadcrumb.title}
                {/if}
            </li>
        {/each}
    </ul>
</div>
