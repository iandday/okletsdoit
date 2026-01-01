<script lang="ts">
    import PageShell from "$lib/components/layouts/PageShell.svelte";
    import RsvpLanding from "$lib/components/rsvp/RsvpLanding.svelte";

    const { data } = $props();
</script>

<div>
    <PageShell title="RSVP">
        <RsvpLanding guestName="The Smith Family" configData={data.configData} preview={true} />
    </PageShell>
</div>
