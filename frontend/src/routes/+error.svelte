<script lang="ts">
    import { page } from "$app/state";

    const { status, error } = $derived(page);
</script>

<div class="hero min-h-screen bg-base-200">
    <div class="hero-content text-center">
        <div class="max-w-md">
            <h1 class="text-5xl font-bold">{status}</h1>
            <p class="py-6 text-xl">
                {#if status === 404}
                    Page not found
                {:else if status === 500}
                    Internal server error
                {:else if status === 403}
                    Forbidden
                {:else if status === 401}
                    Unauthorized
                {:else}
                    Something went wrong
                {/if}
            </p>

            {#if error?.message}
                <div class="alert alert-error mb-6">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-6 w-6 shrink-0 stroke-current"
                        fill="none"
                        viewBox="0 0 24 24">
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span>{error.message}</span>
                </div>
            {/if}

            <div class="flex flex-col gap-2">
                <a href="/" class="btn btn-primary">Return Home</a>
                {#if status === 404}
                    <button onclick={() => history.back()} class="btn btn-ghost">Go Back</button>
                {/if}
            </div>
        </div>
    </div>
</div>
