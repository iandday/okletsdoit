<script lang="ts">
    import { page } from "$app/stores";
</script>

<div class="hero min-h-screen bg-root-bg">
    <div class="hero-content text-center">
        <div class="max-w-md">
            <h1 class="text-5xl font-bold">Whoops</h1>
            <p class="py-6 text-xl">{$page.error?.message || "An error occurred"}</p>

            <div class="space-y-4">
                {#if $page.status === 404 && $page.error?.message?.includes("RSVP code")}
                    <div class="alert alert-warning">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="h-6 w-6 shrink-0 stroke-current"
                            fill="none"
                            viewBox="0 0 24 24">
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                        </svg>
                        <span>Please check your RSVP code and try again.</span>
                    </div>
                {/if}

                <div class="flex flex-col gap-2">
                    <a href="/rsvp" class="btn btn-primary">Go to RSVP Page</a>
                    <a href="/" class="btn btn-primary">Return Home</a>
                </div>
            </div>
        </div>
    </div>
</div>
