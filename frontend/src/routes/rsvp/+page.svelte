<script lang="ts">
    import { enhance } from "$app/forms";
    import ComingSoon from "$lib/components/ComingSoon.svelte";
    import PageShell from "$lib/components/layouts/PageShell.svelte";
    import type { IComingSoon } from "../../types";
    import type { ActionData, PageData } from "./$types";

    let { data, form }: { data: PageData; form: ActionData } = $props();
    let submitting = $state(false);

    const comingSoon: IComingSoon = {
        icon: "calendar-check",
        alert: "Coming Soon",
        intro: "We're creating a simple RSVP system where you can let us know if you'll be joining us for our special day! This feature will be available soon.",
        expectations: [
            {
                text: "Quick and easy RSVP process",
                icon: "check-circle",
            },
            {
                text: "Manage your party's attendance",
                icon: "users",
            },
            {
                text: "Share dietary restrictions and preferences",
                icon: "utensils",
            },
            {
                text: "Send us a personal message",
                icon: "message-square",
            },
        ],
    };
</script>

<div>
    <PageShell title="RSVP">
        {#if !data.allowRsvp}
            <ComingSoon {...comingSoon} />
        {:else}
            <div class="container mx-auto px-4 md:px-6 lg:px-8 max-w-4xl">
                <div class="flex justify-center items-center min-h-[400px]">
                    <div class="card bg-base-200 shadow-2xl border border-primary/20 w-full max-w-2xl pb-2">
                        <div class="card-body items-center text-center">
                            <h2 class="card-title text-accent text-2xl mb-2">
                                <span class="iconify lucide--mail size-7 text-accent"></span>
                                Enter Your RSVP Code
                            </h2>
                            <p class="text-lg text-primary-content mb-4">
                                Enter the 10-character code from your invitation to continue.
                            </p>

                            {#if form?.error}
                                <div class="alert alert-error">
                                    <span class="iconify lucide--alert-circle size-5"></span>
                                    <span>{form.error}</span>
                                </div>
                            {/if}

                            <form
                                method="POST"
                                use:enhance={() => {
                                    submitting = true;
                                    return async ({ update }) => {
                                        await update();
                                        submitting = false;
                                    };
                                }}>
                                <label class="form-control w-full">
                                    <input
                                        type="text"
                                        name="code"
                                        placeholder="ABC1234567"
                                        class="input input-bordered input-lg w-full font-mono uppercase text-primary-content"
                                        maxlength="10"
                                        value={form?.code ?? ""}
                                        required
                                        disabled={submitting}
                                        oninput={(e) => {
                                            const target = e.target as HTMLInputElement;
                                            target.value = target.value.toUpperCase();
                                        }} />
                                </label>

                                <div class="card-actions justify-end mt-4">
                                    <button type="submit" class="btn btn-primary btn-block" disabled={submitting}>
                                        {#if submitting}
                                            <span class="loading loading-spinner loading-sm"></span>
                                            Checking...
                                        {:else}
                                            <span class="iconify lucide--arrow-right size-5"></span>
                                            Continue
                                        {/if}
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        {/if}
    </PageShell>
</div>
