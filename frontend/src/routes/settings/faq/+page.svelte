<script lang="ts">
    import Icon from "$lib/components/Icon.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import { SvelteMap } from "svelte/reactivity";
    import type { QuestionSchema, TipsSchema } from "../../../api-client";

    const { data } = $props();

    // Create a map of categories by name for quick lookup
    const categoryMap = $derived.by(() => {
        const map = new SvelteMap();
        data.categories?.forEach((cat) => {
            map.set(cat.categoryName, cat);
        });
        return map;
    });

    // Group questions by category
    const categorizedQuestions = $derived.by(() => {
        const categories = new SvelteMap<
            string,
            {
                id: string;
                name: string;
                order: number;
                questions: QuestionSchema[];
                tips: TipsSchema[];
            }
        >();

        // Add questions to categories
        data.questions?.forEach((q) => {
            if (!categories.has(q.category)) {
                const cat = categoryMap.get(q.category);
                categories.set(q.category, {
                    id: q.category,
                    name: cat?.categoryName || q.category,
                    order: cat?.categoryOrder || 0,
                    questions: [],
                    tips: [],
                });
            }
            categories.get(q.category)!.questions.push(q);
        });

        // Add tips to categories
        data.tips?.forEach((t) => {
            if (!categories.has(t.category)) {
                const cat = categoryMap.get(t.category);
                categories.set(t.category, {
                    id: t.category,
                    name: cat?.categoryName || t.category,
                    order: cat?.categoryOrder || 0,
                    questions: [],
                    tips: [],
                });
            }
            categories.get(t.category)!.tips.push(t);
        });

        // Sort categories by order, then questions and tips within each category
        return Array.from(categories.values())
            .sort((a, b) => a.order - b.order)
            .map((cat) => ({
                ...cat,
                questions: cat.questions.sort((a, b) => (a.order || 0) - (b.order || 0)),
                tips: cat.tips.sort((a, b) => (a.order || 0) - (b.order || 0)),
            }));
    });

    const totalQuestions = data.questions?.length || 0;
    const totalTips = data.tips?.length || 0;
    const relativeCrumbs = [{ title: "FAQ" }];
</script>

<ProtectedPageShell {relativeCrumbs}>
    <div class="container mx-auto p-4 max-w-6xl">
        <div class="flex justify-between items-center mb-6">
            <div>
                <h1 class="text-3xl font-bold">Manage FAQ</h1>
                <p class="text-base-content/70 mt-1">
                    Add, edit, or organize your frequently asked questions and helpful tips
                </p>
            </div>
            <a href="/settings/preview/faq" class="btn btn-accent" target="_blank">
                <span class="icon-[lucide--eye] size-5"></span>
                Preview FAQ Page
            </a>
        </div>

        <div class="flex flex-wrap gap-3 mb-6">
            <a href="/settings/faq/question/new" class="btn btn-primary">
                <span class="icon-[lucide--plus] size-5"></span>
                Add Question
            </a>
            <a href="/settings/faq/tip/new" class="btn btn-secondary">
                <span class="icon-[lucide--lightbulb] size-5"></span>
                Add Tip
            </a>
        </div>

        {#if categorizedQuestions.length === 0}
            <!-- Empty State -->
            <div class="hero bg-base-200 rounded-box min-h-[400px]">
                <div class="hero-content text-center">
                    <div class="max-w-md">
                        <span class="icon-[lucide--circle-help] size-20 text-base-content/20 mx-auto mb-4"></span>
                        <h2 class="text-2xl font-bold">No FAQ Content Yet</h2>
                        <p class="py-6">
                            Get started by adding your first question or helpful tip. Organize your content into
                            categories to make it easy for guests to find information.
                        </p>
                        <div class="flex gap-3 justify-center">
                            <a href="/settings/faq/question/new" class="btn btn-primary">
                                <span class="icon-[lucide--plus] size-5"></span>
                                Add First Question
                            </a>
                            <a href="/settings/faq/tip/new" class="btn btn-secondary">
                                <span class="icon-[lucide--lightbulb] size-5"></span>
                                Add First Tip
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        {:else}
            <!-- Categories List -->
            <div class="grid gap-6">
                {#each categorizedQuestions as category (category.id)}
                    <div class="config-card">
                        <div class="config-card-body">
                            <div class="flex justify-between items-start mb-4">
                                <div>
                                    <h2 class="config-card-title text-xl">{category.name}</h2>
                                </div>
                                <div class="badge badge-neutral">Order: {category.order}</div>
                            </div>

                            {#if category.questions.length > 0}
                                <div class="divider divider-start text-sm">Questions</div>
                                <div class="space-y-2">
                                    {#each category.questions as question (question.id)}
                                        <div
                                            class="flex items-start gap-3 p-3 rounded-lg bg-base-200 hover:bg-base-300 transition-colors">
                                            <div class="badge badge-sm badge-accent mt-1">{question.order}</div>
                                            <div class="flex-1 min-w-0">
                                                <div class="flex items-start gap-2">
                                                    <Icon name={question.icon} class="size-5 text-accent mt-0.5" />
                                                    <div class="flex-1">
                                                        <p class="config-card-field-value font-medium">
                                                            {question.question}
                                                        </p>
                                                        <p class="config-card-field-value text-sm mt-1">
                                                            {question.answer}
                                                        </p>
                                                        {#if question.urls && question.urls.length > 0}
                                                            <div class="flex flex-wrap gap-2 mt-2">
                                                                {#each question.urls as url, index (index)}
                                                                    <span class="badge badge-outline badge-xs">
                                                                        <span class="icon-[lucide--link] size-3 mr-1"
                                                                        ></span>
                                                                        {url.text}
                                                                    </span>
                                                                {/each}
                                                            </div>
                                                        {/if}
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="flex gap-2">
                                                <a
                                                    href="/settings/faq/question/{question.id}/edit"
                                                    class="btn btn-success btn-sm btn-square"
                                                    aria-label="Edit Question">
                                                    <span class="icon-[lucide--pencil] size-4"></span>
                                                </a>
                                                <form
                                                    method="POST"
                                                    action="?/deleteQuestion"
                                                    onsubmit={(e) => {
                                                        if (
                                                            !confirm("Are you sure you want to delete this question?")
                                                        ) {
                                                            e.preventDefault();
                                                        }
                                                    }}>
                                                    <input type="hidden" name="id" value={question.id} />
                                                    <button
                                                        type="submit"
                                                        class="btn btn-error btn-sm btn-square"
                                                        aria-label="delete">
                                                        <span class="icon-[lucide--trash-2] size-4 text-primary-content"
                                                        ></span>
                                                    </button>
                                                </form>
                                            </div>
                                        </div>
                                    {/each}
                                </div>
                            {/if}

                            {#if category.tips.length > 0}
                                <div class="divider divider-start text-sm">Tips</div>
                                <div class="space-y-2">
                                    {#each category.tips as tip (tip.id)}
                                        <div
                                            class="flex items-start gap-3 p-3 rounded-lg bg-base-200 hover:bg-base-300 transition-colors">
                                            <div class="badge badge-sm badge-accent mt-1">{tip.order}</div>
                                            <div class="flex-1 min-w-0">
                                                <div class="flex items-start gap-2">
                                                    <span class="icon-[lucide--lightbulb] size-5 text-accent mt-0.5"
                                                    ></span>
                                                    <p class="text-sm">{tip.content}</p>
                                                </div>
                                            </div>
                                            <div class="flex gap-2">
                                                <a
                                                    href="/settings/faq/tip/{tip.id}/edit"
                                                    class="btn btn-success btn-sm btn-square"
                                                    aria-label="Edit Tip">
                                                    <span class="icon-[lucide--pencil] size-4"></span>
                                                </a>
                                                <form
                                                    method="POST"
                                                    action="?/deleteTip"
                                                    onsubmit={(e) => {
                                                        if (!confirm("Are you sure you want to delete this tip?")) {
                                                            e.preventDefault();
                                                        }
                                                    }}>
                                                    <input type="hidden" name="id" value={tip.id} />
                                                    <button
                                                        type="submit"
                                                        class="btn btn-error btn-sm btn-square"
                                                        aria-label="delete">
                                                        <span class="icon-[lucide--trash-2] size-4 text-primary-content"
                                                        ></span>
                                                    </button>
                                                </form>
                                            </div>
                                        </div>
                                    {/each}
                                </div>
                            {/if}
                        </div>
                    </div>
                {/each}
            </div>
        {/if}
    </div>
</ProtectedPageShell>
