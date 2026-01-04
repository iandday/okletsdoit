<script lang="ts">
    import Topbar from "$lib/components/layouts/Topbar.svelte";
    import type { iBreadcrumb } from "$lib/types";
    import Breadcrumbs from "./Breadcrumbs.svelte";

    type iProtectedPageShellProps = {
        relativeCrumbs: iBreadcrumb[] | [];
    };
    const { relativeCrumbs }: iProtectedPageShellProps = $props();

    let baseCrumbs: iBreadcrumb[] = [
        { title: "Home", href: "/" },
        { title: "Configuration", href: "/settings" },
    ];

    let crumbs: iBreadcrumb[] = [...baseCrumbs, ...relativeCrumbs];
</script>

<div>
    <Topbar />
    <div class="pt-2 px-6 pb-8 lg:pb-16 xl:pb-24 2xl:pb-28">
        <div class="relative">
            <Breadcrumbs breadcrumbs={crumbs} />
            <slot></slot>
        </div>
    </div>
</div>
