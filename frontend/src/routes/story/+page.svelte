<script lang="ts">
    import CallToAction from "$lib/components/CallToAction.svelte";
    import ComingSoon from "$lib/components/ComingSoon.svelte";
    import Story from "$lib/components/Story.svelte";
    import PageShell from "$lib/components/layouts/PageShell.svelte";
    import type { IComingSoon } from "../../types";
    import type { PageData } from "./$types";

    let { data }: { data: PageData } = $props();
    const comingSoon: IComingSoon = {
        icon: "book-open-text",
        alert: "Coming Soon",
        intro: null,
        expectations: null,
    };
</script>

<div>
    <PageShell title="Our Story">
        {#if !data.configData.showOurStory}
            <ComingSoon {...comingSoon} />
        {:else}
            <Story />
            <CallToAction
                title="Join Us on Our Big Day!"
                content="We can't wait to celebrate with you as we turn this beautiful, chaotic love story into marriage. And don't worry - Ian promises not to comment on anyone's hair at the wedding." />
        {/if}
    </PageShell>
</div>
