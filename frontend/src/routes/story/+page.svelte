<script lang="ts">
    import CallToAction from "$lib/components/CallToAction.svelte";
    import PageShell from "$lib/components/layouts/PageShell.svelte";
    import Story from "./components/Story.svelte";
</script>

<div>
    <PageShell title="Our Story" description="How a swipe right and a hot take on a first date led to forever">
        <Story />
        <CallToAction
            title="Join Us on Our Big Day!"
            content="We can't wait to celebrate with you as we turn this beautiful, chaotic love story into marriage. And don't worry - Ian promises not to comment on anyone's hair at the wedding." />
    </PageShell>
</div>
