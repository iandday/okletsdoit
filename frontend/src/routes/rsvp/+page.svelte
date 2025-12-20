<script lang="ts">
    import { enhance } from "$app/forms";
    import PageShell from "$lib/components/layouts/PageShell.svelte";
    import type { ActionData, PageData } from "./$types";

    let { data, form }: { data: PageData; form: ActionData } = $props();
    let submitting = $state(false);
</script>

<div>
    <PageShell title="RSVP">
        {#if data.allowRsvp}
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
        {:else}
            <div class="container mx-auto px-4 md:px-6 lg:px-8 max-w-4xl">
                <!-- Coming Soon Announcement -->
                <div class="flex justify-center items-center min-h-[400px]">
                    <div class="card bg-base-200 shadow-2xl border border-primary/20 w-full max-w-2xl pb-2">
                        <div class="card-body items-center text-center">
                            <div class="mb-6">
                                <span class="iconify lucide--calendar-check size-20 text-accent animate-pulse"></span>
                            </div>
                            <div class="badge badge-primary badge-lg mb-4 gap-2 px-4 py-3">
                                <span class="iconify lucide--clock size-4"></span>
                                Coming Soon
                            </div>

                            <p class="text-primary-content text-lg leading-relaxed mb-6 max-w-lg">
                                We're creating a simple RSVP system where you can let us know if you'll be joining us
                                for our special day! This feature will be available soon.
                            </p>
                            <div class="text-left w-full max-w-md">
                                <h3 class="font-bold text-primary-content text-lg mb-3 flex items-center gap-2">
                                    <span class="iconify lucide--sparkles size-5 text-primary-content"></span>
                                    What to Expect:
                                </h3>
                                <ul class="space-y-3">
                                    <li class="flex items-start gap-3">
                                        <span
                                            class="iconify lucide--check-circle size-5 text-accent mt-0.5 flex-shrink-0"
                                        ></span>
                                        <span class="text-primary-content">Quick and easy RSVP process</span>
                                    </li>
                                    <li class="flex items-start gap-3">
                                        <span class="iconify lucide--users size-5 text-accent mt-0.5 flex-shrink-0"
                                        ></span>
                                        <span class="text-primary-content">Manage your party's attendance</span>
                                    </li>
                                    <li class="flex items-start gap-3">
                                        <span class="iconify lucide--utensils size-5 text-accent mt-0.5 flex-shrink-0"
                                        ></span>
                                        <span class="text-primary-content"
                                            >Share dietary restrictions and preferences</span>
                                    </li>
                                    <li class="flex items-start gap-3">
                                        <span
                                            class="iconify lucide--message-square size-5 text-accent mt-0.5 flex-shrink-0"
                                        ></span>
                                        <span class="text-primary-content">Send us a personal message</span>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        {/if}
    </PageShell>
</div>
