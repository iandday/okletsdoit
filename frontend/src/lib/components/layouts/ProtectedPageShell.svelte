<script lang="ts">
    import Topbar from "$lib/components/layouts/Topbar.svelte";
</script>

<div>
    <Topbar />
    <div class="pt-2 px-6 pb-8 lg:pb-16 xl:pb-24 2xl:pb-28">
        <div class="relative">
            <slot></slot>
        </div>
    </div>
</div>
