<script lang="ts">
    import { goto } from "$app/navigation";
    import { auth } from "$lib/stores/auth";
    import { onMount } from "svelte";
    import type { PageData } from "./$types";

    interface Props {
        data: PageData;
    }

    let { data }: Props = $props();

    let error = $state("");
    let processing = $state(true);

    onMount(async () => {
        try {
            // The OAuth provider redirects back with query parameters
            // django-allauth handles the callback automatically via cookies
            // We just need to check if the session is now authenticated

            // Small delay to ensure cookies are set
            await new Promise((resolve) => setTimeout(resolve, 500));

            // Re-initialize auth to check session status
            await auth.init();

            // Check if authentication was successful
            const authState = await new Promise<any>((resolve) => {
                const unsubscribe = auth.subscribe((state) => {
                    resolve(state);
                    unsubscribe();
                });
            });

            if (authState.isAuthenticated) {
                // Success! Redirect to the callback URL or home
                goto(data.redirect);
            } else {
                error = "Authentication failed. Please try again.";
                processing = false;
            }
        } catch (err) {
            console.error("Callback error:", err);
            error = "An error occurred during authentication.";
            processing = false;
        }
    });
</script>

<div class="flex min-h-screen items-center justify-center">
    <div class="card w-96 bg-base-100 shadow-xl">
        <div class="card-body items-center text-center">
            {#if processing}
                <span class="loading loading-spinner loading-lg text-primary"></span>
                <h2 class="card-title mt-4">Completing sign in...</h2>
                <p>Please wait while we complete your authentication.</p>
            {:else if error}
                <div class="alert alert-error">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="stroke-current shrink-0 h-6 w-6"
                        fill="none"
                        viewBox="0 0 24 24">
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span>{error}</span>
                </div>
                <div class="card-actions mt-4">
                    <a href="/auth/login" class="btn btn-primary">Back to Login</a>
                </div>
            {/if}
        </div>
    </div>
</div>
