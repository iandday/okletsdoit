<script lang="ts">
    import CallToAction from "$lib/components/CallToAction.svelte";
    import ComingSoon from "$lib/components/ComingSoon.svelte";
    import PageShell from "$lib/components/layouts/PageShell.svelte";
    import type { IComingSoon } from "../../types";
    import Accommodations from "./components/Accommodations.svelte";
    import Attractions from "./components/Attractions.svelte";
    import Gallery from "./components/Gallery.svelte";
    import Location from "./components/Location.svelte";
    import Timeline from "./components/Timeline.svelte";

    const comingSoon: IComingSoon = {
        icon: "party-popper",
        alert: "Coming Soon",
        intro: "We're creating a page with all the details about our venue! This feature will be available soon.",
        expectations: [
            {
                text: "Address and directions",
                icon: "map",
            },
            {
                text: "Lodging options",
                icon: "map-pin-house",
            },
            {
                text: "Local attractions",
                icon: "mountain-snow",
            },
        ],
    };
    const { data } = $props();
</script>

<div>
    {#if !data?.configData?.showVenue}
        <PageShell title={data.configData?.venuePageTitle}><ComingSoon {...comingSoon} /></PageShell>
    {:else}
        <PageShell title={data.configData.venuePageTitle} description={data.configData.venuePageDescription}>
            <img
                src="/images/venue/gallery/patio.png"
                alt={data.configData.venuePageTitle}
                class="mb-8 w-auto max-w-full mx-auto pt-6" />

            <Gallery
                galleryTitle={data.configData?.venueGalleryTitle}
                galleryDescription={data.configData?.venueGalleryDescription} />
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
                <Location {data} />
                <Timeline />
            </div>
            <Accommodations />
            <Attractions />

            <CallToAction
                title="Join Us on Our Big Day!"
                content={`The ${data.configData.venueName} provides the perfect backdrop for our special day. We're excited to share this beautiful venue with our family and friends as we begin our journey together.`} />
        </PageShell>
    {/if}
</div>
