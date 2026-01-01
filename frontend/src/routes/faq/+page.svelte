<!-- frontend/src/routes/faq/+page.svelte -->
<script lang="ts">
    import ComingSoon from "$lib/components/ComingSoon.svelte";
    import Faq from "$lib/components/Faq.svelte";
    import PageShell from "$lib/components/layouts/PageShell.svelte";
    import type { IComingSoon } from "../../types";

    const comingSoon: IComingSoon = {
        icon: "circle-question-mark",
        alert: "Coming Soon",
        intro: "We're preparing a comprehensive FAQ section to answer all your questions about our special day! Check back soon for helpful information.",
        expectations: [
            { text: "Event date and time details", icon: "calendar" },
            { text: "Venue location and directions", icon: "map-pin" },
            { text: "Dress code and attire guidance", icon: "shirt" },
            { text: "Food, drinks, and dietary options", icon: "utensils" },
        ],
    };

    const { data } = $props();
</script>

<div>
    <PageShell title="Frequently Asked Questions">
        {#if !data?.configData?.showFaq}
            <ComingSoon {...comingSoon} />
        {:else}
            <Faq categories={data.categories} />
        {/if}
    </PageShell>
</div>
