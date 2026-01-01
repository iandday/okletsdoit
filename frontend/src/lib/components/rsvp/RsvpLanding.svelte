<script lang="ts">
    import type { WeddingSettingsUpdateSchema } from "../../api-client";

    interface Props {
        guestName: string;
        configData: WeddingSettingsUpdateSchema | null;
        acceptHref?: string;
        declineHref?: string;
        preview?: boolean;
    }

    let { guestName, configData, acceptHref, declineHref, preview = false }: Props = $props();
</script>

<div class="container mx-auto px-4 md:px-6 lg:px-8 max-w-4xl">
    <div class="flex justify-center items-center min-h-[400px]">
        <div class="card bg-base-200 shadow-2xl border border-primary/20 w-full max-w-2xl pb-2">
            <div class="card-body items-center text-center text-primary-content">
                {#if preview}
                    <div class="alert alert-warning mb-6 flex flex-row items-center gap-4">
                        <span class="icon-[lucide--eye] size-5"></span>
                        <div class="flex flex-col items-center gap-2">
                            <p>Preview Mode This is how your RSVP landing page will appear to guests.</p>
                            <p>Buttons are disabled, guests will be able to click these to respond.</p>
                        </div>
                    </div>
                {/if}
                <div class="mb-6">
                    <span class="icon-[lucide--megaphone] size-16 text-accent"></span>
                </div>

                <p>
                    {guestName}, we'd love to hear from you. Please let us know whether you will be joining us on the
                    wedding day.
                </p>
                <div class="flex flex-row gap-4 mt-6">
                    {#if preview}
                        <div
                            class="btn bg-base-100 text-primary-content btn-lg gap-2 w-full sm:w-48 cursor-not-allowed">
                            <span class="icon-[lucide--heart] size-5"></span>
                            {configData?.rsvpAcceptButton || "Accept Invitation"}
                        </div>
                        <div
                            class="btn btn-error text-primary-content btn-lg gap-2 w-full sm:w-48 border border-neutral/30 cursor-not-allowed">
                            <span class="icon-[lucide--x] size-5"></span>
                            {configData?.rsvpDeclineButton || "Decline Invitation"}
                        </div>
                    {:else}
                        <a
                            class="btn bg-base-100 text-primary-content btn-lg gap-2 w-full sm:w-48"
                            href={acceptHref}
                            aria-label="Accept RSVP">
                            <span class="icon-[lucide--heart] size-5"></span>
                            {configData?.rsvpAcceptButton || "Accept Invitation"}
                        </a>
                        <a
                            class="btn btn-error text-primary-content btn-lg gap-2 w-full sm:w-48 border border-neutral/30"
                            href={declineHref}
                            aria-label="Decline RSVP">
                            <span class="icon-[lucide--x] size-5"></span>
                            {configData?.rsvpDeclineButton || "Decline Invitation"}
                        </a>
                    {/if}
                </div>
            </div>
        </div>
    </div>
</div>
