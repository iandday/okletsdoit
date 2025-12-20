<script lang="ts">
    import { page } from "$app/state";
    import PageShell from "$lib/components/layouts/PageShell.svelte";

    const accepted = page.url.searchParams.get("accepted") === "true";
    const code = page.params.code;
    const { data } = $props();

    const configData = data.configData ?? { rsvpSuccessHeadline: "", rsvpDeclineSuccessMessage: "" };
</script>

<div>
    <PageShell title="RSVP">
        <div class="container mx-auto px-4 md:px-6 lg:px-8 max-w-4xl">
            <div class="flex justify-center items-center min-h-[400px]">
                <div class="card bg-base-200 shadow-2xl border border-primary/20 w-full max-w-2xl pb-2">
                    <div class="card-body items-center text-center">
                        <div class="mb-6">
                            {#if accepted}
                                <h1 class="text-3xl font-bold">{configData.rsvpSuccessHeadline}</h1>
                                <p class="py-6">
                                    In the mean time you can learn more about the venue or find the answer to common
                                    questions about our big day
                                </p>
                                <div class="flex flex-row gap-4 justify-center">
                                    <a href="/venue" class="btn btn-accent text-primary-content w-32">Venue Info</a>
                                    <a href="/faq" class="btn btn-accent text-primary-content w-32">FAQ</a>
                                    <a href="/{code}" class="btn btn-accent text-primary-content w-32">Update RSVP</a>
                                </div>
                            {:else}
                                <p class="py-6 text-primary-content">{configData.rsvpDeclineSuccessMessage}</p>
                                <a href="/" class="btn btn-accent">Home</a>
                            {/if}
                        </div>
                    </div>
                </div>
            </div>
        </div></PageShell>
</div>
