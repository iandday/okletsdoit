<script lang="ts">
    import type { CategoryContentSchema } from "../../../api-client";
    import Icon from "./Icon.svelte";

    type iProps = {
        categories: CategoryContentSchema[];
        preview?: boolean;
    };

    const { categories, preview = false } = $props();
</script>

<div class="pb-8 lg:pb-12 xl:pb-16">
    <div class="container mx-auto px-4 md:px-6 lg:px-8 max-w-5xl">
        {#if preview}
            <div class="alert alert-warning mb-6 flex flex-row items-center gap-4">
                <span class="icon-[lucide--eye] size-5"></span>
                <div class="flex flex-col items-center gap-2">
                    <p>Preview Mode - This is how your FAQ page will appear to guests.</p>
                </div>
            </div>
        {/if}
        <!-- Header -->
        <div class="text-center mb-8 md:mb-12">
            <p class="text-base-content text-lg max-w-2xl mx-auto">
                Have questions about our big day? We've got answers! If you don't see your question here, feel free to
                reach out to us directly.
            </p>
        </div>

        <!-- FAQs by Category -->
        {#each categories as cat (cat.categoryId)}
            <div class="mb-8">
                <!-- Category Header -->
                <div class="flex items-center gap-3 mb-4">
                    <div class="h-px flex-grow bg-gradient-to-r from-transparent to-primary"></div>
                    <h3 class="text-xl font-bold text-primary">{cat.categoryName}</h3>
                    <div class="h-px flex-grow bg-gradient-to-r from-primary to-transparent"></div>
                </div>

                <!-- FAQ Items -->
                <div class="space-y-3">
                    {#each cat.questions as question (question.id)}
                        <div
                            class="collapse collapse-arrow bg-secondary text-secondary-content border border-base-300 shadow-md hover:shadow-lg transition-shadow">
                            <input type="radio" name="faq-accordion-{cat.categoryId}" />
                            <div class="collapse-title text-lg font-medium flex items-center gap-3">
                                <div class="rounded-full p-2 flex-shrink-0">
                                    <Icon name={question.icon} class="size-6 font-strong text-primary-content" />
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
                                            <span class="icon-[lucide--check] size-4 text-accent mt-0.5 flex-shrink-0"
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
