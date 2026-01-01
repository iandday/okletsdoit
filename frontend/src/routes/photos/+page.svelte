<script lang="ts">
    import ComingSoon from "$lib/components/ComingSoon.svelte";
    import PageShell from "$lib/components/layouts/PageShell.svelte";
    import type { IComingSoon } from "../../types.ts";

    const comingSoon: IComingSoon = {
        icon: "camera",
        alert: "Coming Soon",
        intro: "We're building a special place where you can upload and share your favorite photos from our big day! This feature will be available starting on our wedding day.",
        expectations: [
            { text: "Easy photo uploads", icon: "upload" },
            { text: "Browse photos from all our guests", icon: "eye" },
            { text: "Download and share your favorites", icon: "download" },
            { text: "Create lasting memories together", icon: "heart" },
        ],
    };

    const { data } = $props();
</script>

<div>
    <PageShell title="Share Your Photos">
        {#if !data?.configData?.allowPhotos}
            <ComingSoon {...comingSoon} />
        {:else}
            <div class="container mx-auto px-4 md:px-6 lg:px-8 max-w-4xl">
                <div class="flex justify-center items-center min-h-[400px]">
                    <div class="card bg-base-200 shadow-2xl border border-primary/20 w-full max-w-2xl pb-2">
                        <div class="card-body items-center text-center">
                            <h2
                                class="card-title
    text-accent text-2xl mb-2">
                                <span class="icon-[lucide--camera] size-7 text-accent"></span>
                                Photo Sharing Coming Soon!
                            </h2>
                            <p class="text-lg text-primary-content mb-4">
                                We're excited to launch our photo sharing feature on our wedding day! Stay tuned for a
                                fun and easy way to share your favorite moments with us.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        {/if}
    </PageShell>
</div>
