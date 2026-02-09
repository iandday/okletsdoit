<script lang="ts">
    import Topbar from "$lib/components/layouts/Topbar.svelte";
    import type { iBreadcrumb } from "$lib/types";
    import Breadcrumbs from "./Breadcrumbs.svelte";

    type iProtectedPageShellProps = {
        relativeCrumbs: iBreadcrumb[] | [];
        children?: import("svelte").Snippet;
    };
    const { relativeCrumbs, children }: iProtectedPageShellProps = $props();

    let baseCrumbs: iBreadcrumb[] = [
        { title: "Home", href: "/" },
        { title: "Planning", href: "/planning" },
    ];

    let crumbs: iBreadcrumb[] = [...baseCrumbs, ...relativeCrumbs];
</script>

<div>
    <Topbar />
    <div class="pt-2 px-6 pb-8 lg:pb-16 xl:pb-24 2xl:pb-28">
        <Breadcrumbs breadcrumbs={crumbs} />
        <div class="container mx-auto p-4">
            {@render children?.()}
        </div>
    </div>
</div>
