<script lang="ts">
    import CallToAction from "$lib/components/CallToAction.svelte";
    import ComingSoon from "$lib/components/ComingSoon.svelte";
    import PageShell from "$lib/components/layouts/PageShell.svelte";
    import type { IComingSoon } from "../../types";
    import Accommodations from "./venue/Accommodations.svelte";
    import Attractions from "./venue/Attractions.svelte";
    import Gallery from "./venue/Gallery.svelte";
    import Location from "./venue/Location.svelte";
    import Timeline from "./venue/Timeline.svelte";

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

    interface VenuePageData {
        showContent: boolean;
        title: string;
        description: string;
        galleryTitle: string;
        galleryDescription: string;
        venueName: string;
        venueAddressLineOne: string;
        venueAddressLineTwo: string | null | undefined;
        venueCity: string;
        venueState: string;
        venueZip: string;
        venueParking: string | null | undefined;
    }

    let {
        showContent,
        title,
        description,
        galleryTitle,
        galleryDescription,
        venueName,
        venueAddressLineOne,
        venueAddressLineTwo = null,
        venueCity,
        venueState,
        venueZip,
        venueParking = null,
    }: VenuePageData = $props();
</script>

<div>
    {#if !showContent}
        <PageShell {title}><ComingSoon {...comingSoon} /></PageShell>
    {:else}
        <PageShell {title} {description}>
            <img src="/images/venue/gallery/patio.png" alt={title} class="mb-8 w-auto max-w-full mx-auto pt-6" />

            <Gallery {galleryTitle} {galleryDescription} />
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
                <Location
                    {venueName}
                    {venueAddressLineOne}
                    {venueAddressLineTwo}
                    {venueCity}
                    {venueState}
                    {venueZip}
                    {venueParking} />
                <Timeline />
            </div>
            <Accommodations />
            <Attractions />

            <CallToAction
                title="Join Us on Our Big Day!"
                content={`The ${venueName} provides the perfect backdrop for our special day. We're excited to share this beautiful venue with our family and friends as we begin our journey together.`} />
        </PageShell>
    {/if}
</div>
