<script lang="ts">
    import { page } from "$app/state";
    import PageShell from "$lib/components/layouts/PageShell.svelte";
    import RsvpComplete from "$lib/components/rsvp/RsvpComplete.svelte";

    const accepted = page.url.searchParams.get("accepted") === "true";

    const { data } = $props();
</script>

<div>
    <PageShell title="RSVP">
        <RsvpComplete configData={data.configData} {accepted} code="The Smith Family" preview={true} />
    </PageShell>
</div>
