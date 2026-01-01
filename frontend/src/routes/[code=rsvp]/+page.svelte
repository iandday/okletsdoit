<script lang="ts">
    import { page } from "$app/state";
    import PageShell from "$lib/components/layouts/PageShell.svelte";
    import RsvpLanding from "$lib/components/rsvp/RsvpLanding.svelte";

    const { data } = $props();
    const code = page.params.code;
</script>

<div>
    <PageShell title="RSVP">
        <div class="container mx-auto px-4 md:px-6 lg:px-8 max-w-4xl">
            <RsvpLanding
                guestName={data.guestData.addressName}
                configData={data.configData}
                acceptHref={`/${code}/accept`}
                declineHref={`/${code}/complete?accepted=false`} />
        </div>
    </PageShell>
</div>
