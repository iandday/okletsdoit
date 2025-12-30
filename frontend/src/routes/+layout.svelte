<script lang="ts">
    import BackToTop from "$lib/components/BackToTop.svelte";
    import ConfigProvider from "$lib/contexts/ConfigProvider.svelte";
    import { auth } from "$lib/stores/auth";
    import "$lib/styles/app.css";
    import { onMount } from "svelte";

    let { children } = $props();

    onMount(() => {
        auth.init();
    });
</script>

<svelte:head>
    <title>Steph & Ian</title>
    <meta name="description" content="Let's do this thing" />
</svelte:head>
<ConfigProvider>
    {@render children()}
    <div class="fixed end-8 bottom-8 z-50">
        <BackToTop />
    </div>
</ConfigProvider>
