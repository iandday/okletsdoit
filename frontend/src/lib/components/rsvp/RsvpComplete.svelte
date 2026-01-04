<script lang="ts">
    import type { WeddingSettingsUpdateSchema } from "../../api-client";

    interface Props {
        configData: WeddingSettingsUpdateSchema | null;
        accepted: boolean;
        code: string;
        preview?: boolean;
    }

    let { configData, accepted, code, preview = false }: Props = $props();
</script>

<div class="container mx-auto px-4 md:px-6 lg:px-8 max-w-4xl">
    <div class="flex justify-center items-center min-h-[400px]">
        <div class="card bg-base-200 shadow-2xl border border-primary/20 w-full max-w-2xl pb-2">
            <div class="card-body items-center text-center">
                <div class="mb-6">
                    {#if preview}
                        <div class="alert alert-warning mb-6 flex flex-row items-center gap-4">
                            <span class="icon-[lucide--eye] size-10"></span>
                            <div class="flex flex-col items-center gap-2">
                                <p>
                                    Preview Mode - This is how your RSVP complete page will appear to guests who will be
                                    attending. The Update RSVP button is disabled, but will allow guests to update their
                                    RSVP when live.
                                </p>
                            </div>
                        </div>
                    {/if}
                    <h1 class="text-3xl text-accent font-bold">{configData.rsvpSuccessHeadline}</h1>
                    {#if accepted}
                        <p class="py-6 text-primary-content">{configData.rsvpAcceptSuccessMessage}</p>
                        <div class="flex flex-row gap-4 justify-center">
                            <a href="/venue" class="btn btn-accent text-primary-content w-32">Venue Info</a>
                            <a href="/faq" class="btn btn-accent text-primary-content w-32">FAQ</a>
                            {#if preview}
                                <div class="btn btn-accent text-primary-content w-32 cursor-not-allowed">
                                    Update RSVP
                                </div>
                            {:else}
                                <a href="/{code}" class="btn btn-accent text-primary-content w-32">Update RSVP</a>
                            {/if}
                        </div>
                    {:else}
                        <p class="py-6 text-primary-content">{configData.rsvpDeclineSuccessMessage}</p>
                        <a href="/" class="btn btn-accent">Home</a>
                    {/if}
                </div>
            </div>
        </div>
    </div>
</div>
