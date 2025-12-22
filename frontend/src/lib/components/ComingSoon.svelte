<!-- components/ComingSoon.svelte -->
<script lang="ts">
    import type { IComingSoon } from "../../types";

    const { icon, alert, intro, expectations }: IComingSoon = $props();
</script>

<div class="pb-8 lg:pb-12 xl:pb-16">
    <div class="container mx-auto px-4 md:px-6 lg:px-8 max-w-4xl">
        <div class="flex justify-center items-center min-h-[400px]">
            <div class="card bg-base-200 shadow-2xl border border-primary/20 w-full max-w-2xl pb-2">
                <div class="card-body items-center text-center">
                    <div class="mb-6">
                        <span class="iconify lucide--{icon} size-20 text-accent animate-pulse"></span>
                    </div>
                    <div class="badge badge-primary badge-lg mb-4 gap-2 px-4 py-3">
                        <span class="iconify lucide--clock size-4"></span>
                        {alert}
                    </div>

                    <p class="text-primary-content text-lg leading-relaxed mb-6 max-w-lg">
                        {intro}
                    </p>

                    <div class="text-left w-full max-w-md">
                        <h3 class="font-bold text-primary-content text-lg mb-3 flex items-center gap-2">
                            <span class="iconify lucide--sparkles size-5 text-primary-content"></span>
                            What to Expect:
                        </h3>
                        <ul class="space-y-3">
                            {#each expectations as { text, icon }}
                                <li class="flex items-start gap-3">
                                    <span class="iconify lucide--{icon} size-5 text-accent mt-0.5 flex-shrink-0"></span>
                                    <span class="text-primary-content">{text}</span>
                                </li>
                            {/each}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
