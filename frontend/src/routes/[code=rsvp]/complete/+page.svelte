<!-- frontend/src/routes/[code=rsvp]/complete/+page.svelte -->
<script lang="ts">
    import { page } from "$app/state";
    import PageShell from "$lib/components/layouts/PageShell.svelte";
    import RsvpComplete from "$lib/components/rsvp/RsvpComplete.svelte";

    const accepted = page.url.searchParams.get("accepted") === "true";
    const code = page.params.code || "Unknown";
    const { data } = $props();

    const configData = data.configData ?? { rsvpSuccessHeadline: "", rsvpDeclineSuccessMessage: "" };
</script>

<div>
    <PageShell title="RSVP"><RsvpComplete {configData} {accepted} {code} /></PageShell>
</div>
