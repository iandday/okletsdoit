<script lang="ts">
    import PageTitle from "$lib/components/PageTitle.svelte";
    import Topbar from "$lib/components/layouts/Topbar.svelte";

    type IPageShell = {
        label?: string;
        title?: string;
        description?: string;
        centered?: boolean;
        image?: string;
    };
    const { label, title, description, centered = true, image }: IPageShell = $props();
</script>

<div>
    <Topbar />
    <div class="pt-2 px-6 pb-8 lg:pb-16 xl:pb-24 2xl:pb-28">
        <div class="relative">
            <PageTitle {label} {title} {description} {centered} {image} />
            <slot></slot>
        </div>
    </div>
</div>
