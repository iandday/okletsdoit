<script lang="ts">
    import { page } from "$app/state";
    import PageShell from "$lib/components/layouts/PageShell.svelte";

    const { data } = $props();
    const code = page.params.code;
</script>

<div>
    <PageShell title="RSVP">
        <div class="container mx-auto px-4 md:px-6 lg:px-8 max-w-4xl">
            <div class="flex justify-center items-center min-h-[400px]">
                <div class="card bg-base-200 shadow-2xl border border-primary/20 w-full max-w-2xl pb-2">
                    <div class="card-body items-center text-center text-primary-content">
                        <div class="mb-6">
                            <span class="iconify lucide--megaphone size-16 text-accent"></span>
                        </div>

                        <p>
                            {data.guestData.addressName}, we'd love to hear from you. Please let us know whether you
                            will be joining us on the wedding day.
                        </p>
                        <div class="flex flex-row gap-4 mt-6">
                            <a
                                class="btn btn-success btn-lg gap-2 w-full sm:w-48"
                                href={`/${code}/accept`}
                                aria-label="Accept RSVP">
                                <span class="iconify lucide--heart size-5"></span>
                                {#if data.configData}
                                    {data.configData.rsvpAcceptButton}
                                {:else}
                                    "Accept Invitation"
                                {/if}
                            </a>
                            <a
                                class="btn btn-error text-primary-content btn-lg gap-2 w-full sm:w-48 border border-neutral/30"
                                href={`/${code}/complete?accepted=false`}
                                aria-label="Decline RSVP">
                                <!-- Cross icon -->
                                <span class="iconify lucide--x size-5"></span>
                                {#if data.configData}
                                    {data.configData.rsvpDeclineButton}
                                {:else}
                                    "Decline Invitation"
                                {/if}
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </PageShell>
</div>
