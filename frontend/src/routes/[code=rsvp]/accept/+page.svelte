<script lang="ts">
    import PageShell from "$lib/components/layouts/PageShell.svelte";
    import RsvpAccept from "$lib/components/rsvp/RsvpAccept.svelte";
    import type { ActionData, PageData } from "./$types";

    let { data, form }: { data: PageData; form: ActionData } = $props();
</script>

<div>
    <PageShell title="RSVP">
        <RsvpAccept
            configData={data.configData}
            guestData={data.guestData}
            guests={data.guests}
            rsvpQuestions={data.rsvpQuestions}
            showAccommodation={data.showAccommodation}
            showVip={data.showVip}
            {form} />
    </PageShell>
</div>
