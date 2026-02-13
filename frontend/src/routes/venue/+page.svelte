<script lang="ts">
    import Venue from "$lib/components/Venue.svelte";
    import { redirect } from "@sveltejs/kit";

    const { data } = $props();
</script>

{#if data.configData}
    <Venue
        showContent={data.configData.showVenue}
        title={data.configData.venuePageTitle}
        description={data.configData.venuePageDescription}
        galleryTitle={data.configData.venueGalleryTitle}
        galleryDescription={data.configData.venueGalleryDescription}
        venueName={data.configData.venueName}
        venueAddressLineOne={data.configData.venueAddressLineOne}
        venueAddressLineTwo={data.configData.venueAddressLineTwo}
        venueCity={data.configData.venueCity}
        venueState={data.configData.venueState}
        venueZip={data.configData.venueZipcode}
        venueParking={data.configData.venueParking}
        timelineEntries={data.timelines}
        accommodations={data.accommodations} />
{:else}
    {redirect(302, "/")}
{/if}
