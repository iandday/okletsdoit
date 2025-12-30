<script lang="ts">
    import { goto } from "$app/navigation";
    import PageShell from "$lib/components/layouts/PageShell.svelte";
    import { auth } from "$lib/stores/auth";
    import { onMount } from "svelte";

    let loggingOut = $state(true);
    let error = $state("");

    onMount(async () => {
        try {
            await auth.logout();
            // Wait a moment to ensure state is updated
            setTimeout(() => {
                goto("/");
            }, 500);
        } catch (err) {
            error = "Failed to logout. Please try again.";
            loggingOut = false;
        }
    });
</script>

<PageShell title="Logout">
    <div class="pb-8 lg:pb-12 xl:pb-16">
        <div class="container mx-auto px-4 md:px-6 lg:px-8 max-w-4xl">
            <div class="flex justify-center items-center min-h-[400px]">
                <div class="card-body items-center text-center">
                    {#if loggingOut}
                        <div class="mb-6">
                            <span class="loading loading-spinner loading-lg text-primary"></span>
                        </div>
                        <h2 class="card-title text-2xl font-bold mb-2">Logging Out</h2>
                        <p class="text-base-content/70">Please wait while we log you out...</p>
                    {:else if error}
                        <div class="mb-6">
                            <span class="iconify lucide--alert-circle size-16 text-error"></span>
                        </div>
                        <h2 class="card-title text-2xl font-bold mb-2">Logout Failed</h2>
                        <div class="alert alert-error mb-4">
                            <span class="iconify lucide--alert-circle size-5"></span>
                            <span>{error}</span>
                        </div>
                        <div class="card-actions flex gap-2">
                            <a href="/" class="btn btn-neutral">
                                <span class="iconify lucide--home size-5"></span>
                                Go Home
                            </a>
                            <button onclick={() => location.reload()} class="btn btn-primary">
                                <span class="iconify lucide--refresh-cw size-5"></span>
                                Try Again
                            </button>
                        </div>
                    {/if}
                </div>
            </div>
        </div>
    </div>
</PageShell>
