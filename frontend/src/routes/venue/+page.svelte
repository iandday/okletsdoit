<script lang="ts">
    import CallToAction from "$lib/components/CallToAction.svelte";
    import PageShell from "$lib/components/layouts/PageShell.svelte";
    import Accommodations from "./components/Accommodations.svelte";
    import Attractions from "./components/Attractions.svelte";
    import Gallery from "./components/Gallery.svelte";
    import Location from "./components/Location.svelte";
    import Timeline from "./components/Timeline.svelte";
</script>

<div>
    <PageShell
        title="Timberframe Lodge"
        description="Join us at Timberframe Lodge, tucked away in the Hocking Hills region of southeastern Ohio.">
        <img
            src="/images/venue/timberframeExterior.webp"
            alt="Timberframe Lodge"
            class="mb-8 w-auto max-w-full mx-auto pt-6" />

        <Gallery />
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
            <Location />
            <Timeline />
        </div>
        <Accommodations />
        <Attractions />

        <CallToAction
            title="Join Us on Our Big Day!"
            content="The Timberframe Lodge provides the perfect backdrop for our special day. We're excited to share this beautiful venue with our family and friends as we begin our journey together." />
    </PageShell>
</div>
