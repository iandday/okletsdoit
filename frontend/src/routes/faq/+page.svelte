<!-- frontend/src/routes/faq/+page.svelte -->
<script lang="ts">
    import ComingSoon from "$lib/components/ComingSoon.svelte";
    import Icon from "$lib/components/Icon.svelte";
    import PageShell from "$lib/components/layouts/PageShell.svelte";
    import type { IComingSoon } from "../../types";

    const comingSoon: IComingSoon = {
        icon: "help-circle",
        alert: "Coming Soon",
        intro: "We're preparing a comprehensive FAQ section to answer all your questions about our special day! Check back soon for helpful information.",
        expectations: [
            { text: "Event date and time details", icon: "calendar" },
            { text: "Venue location and directions", icon: "map-pin" },
            { text: "Dress code and attire guidance", icon: "shirt" },
            { text: "Food, drinks, and dietary options", icon: "utensils" },
        ],
    };

    const { data } = $props();
</script>

<div>
    <PageShell title="Frequently Asked Questions">
        {#if !data?.configData?.showFaq}
            <ComingSoon {...comingSoon} />
        {:else}
            <div class="pb-8 lg:pb-12 xl:pb-16">
                <div class="container mx-auto px-4 md:px-6 lg:px-8 max-w-5xl">
                    <!-- Header -->
                    <div class="text-center mb-8 md:mb-12">
                        <p class="text-base-content text-lg max-w-2xl mx-auto">
                            Have questions about our big day? We've got answers! If you don't see your question here,
                            feel free to reach out to us directly.
                        </p>
                    </div>

                    <!-- FAQs by Category -->
                    {#each data.categories as cat (cat.categoryId)}
                        <div class="mb-8">
                            <!-- Category Header -->
                            <div class="flex items-center gap-3 mb-4">
                                <div
                                    class="h-px flex-grow bg-gradient-to-r from-transparent via-primary to-transparent">
                                </div>
                                <h3 class="text-xl font-bold text-primary">{cat.categoryName}</h3>
                                <div
                                    class="h-px flex-grow bg-gradient-to-r from-primary via-transparent to-transparent">
                                </div>
                            </div>

                            <!-- FAQ Items -->
                            <div class="space-y-3">
                                {#each cat.questions as question (question.id)}
                                    <div
                                        class="collapse collapse-plus bg-secondary text-secondary-content border border-base-300 shadow-md hover:shadow-lg transition-shadow">
                                        <input type="radio" name="faq-accordion-{question.id}" />
                                        <div class="collapse-title text-lg font-medium flex items-center gap-3">
                                            <div class="rounded-full p-2 flex-shrink-0">
                                                <Icon
                                                    name={question.icon}
                                                    class="size-6 font-strong text-primary-content" />
                                            </div>
                                            <span>{question.question}</span>
                                        </div>
                                        <div class="collapse-content">
                                            <div class="pt-2 pl-14">
                                                <p class="leading-relaxed">{question.answer}</p>
                                                {#if question.urls}
                                                    <div class="flex flex-row flex-wrap gap-3 mt-4">
                                                        {#each question.urls as url (url.id)}
                                                            <a
                                                                href={url.url}
                                                                target="_blank"
                                                                rel="noopener noreferrer"
                                                                class="badge badge-primary gap-2">
                                                                {url.text}
                                                            </a>
                                                        {/each}
                                                    </div>
                                                {/if}
                                            </div>
                                        </div>
                                    </div>
                                {/each}
                            </div>

                            <!-- Tips Section -->
                            {#if cat.tips && cat.tips.length > 0}
                                <div class="mt-4 alert bg-base-100 text-neutral-content border-accent/30 shadow-md">
                                    <div class="flex items-start gap-3 w-full">
                                        <div class="rounded-full p-2 flex-shrink-0">
                                            <span class="icon-[lucide--lightbulb] size-6 text-accent"></span>
                                        </div>
                                        <div class="flex-1">
                                            <h4 class="font-bold text-accent mb-2">Helpful Tips</h4>
                                            <ul class="space-y-2">
                                                {#each cat.tips as tip (tip.id)}
                                                    <li class="text-sm text-secondary-content flex items-start gap-2">
                                                        <span
                                                            class="icon-[lucide--check] size-4 text-accent mt-0.5 flex-shrink-0"
                                                        ></span>
                                                        <span>{tip.content}</span>
                                                    </li>
                                                {/each}
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            {/if}
                        </div>
                    {/each}
                </div>
            </div>
        {/if}
    </PageShell>
</div>
