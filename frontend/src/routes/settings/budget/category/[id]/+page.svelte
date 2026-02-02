<script lang="ts">
    import Stats from "$lib/components/Stats.svelte";
    import CreateObject from "$lib/components/buttons/CreateObject.svelte";
    import ObjectChildItems from "$lib/components/object/ObjectChildItems.svelte";
    import ObjectDetail from "$lib/components/object/ObjectDetail.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();

    const relativeCrumbs = [
        { title: "Budget", href: "/settings/budget" },
        { title: `${data.category.name} Category`, href: `/settings/budget/category/${data.category.id}` },
    ];

    const displayName = data.category.name;

    function formatCurrency(amount: number): string {
        return new Intl.NumberFormat("en-US", {
            style: "currency",
            currency: "USD",
        }).format(amount);
    }

    function formatDate(dateString: string | Date | null | undefined): string {
        if (!dateString) return "N/A";
        const date = dateString instanceof Date ? dateString : new Date(dateString);
        return date.toLocaleDateString();
    }
</script>

<ObjectDetail
    {relativeCrumbs}
    title={displayName}
    editLink={`/settings/budget/category/${data.category.id}/edit`}
    deleteAction="?/delete"
    object={data.category}>
    {#snippet mainSnippet()}
        <div class="space-y-6">
            {#if data.category.description}
                <div>
                    <div class="detail-card-field-name">Description</div>
                    <div class="detail-card-field-value whitespace-pre-wrap">
                        {data.category.description}
                    </div>
                </div>
            {/if}
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <div class="detail-card-field-name">Total Expenses</div>
                    <div class="detail-card-field-value whitespace-pre-wrap">
                        {data.expenses.length.toString()}
                    </div>
                </div>
                <div>
                    <div class="detail-card-field-name">Estimated Budget</div>
                    <div class="detail-card-field-value whitespace-pre-wrap">
                        {formatCurrency(data.totalEstimated)}
                    </div>
                </div>
                <div>
                    <div class="detail-card-field-name">Total Expenses</div>
                    <div class="detail-card-field-value whitespace-pre-wrap">
                        {formatCurrency(data.totalActual)}
                    </div>
                </div>
                <div>
                    <div class="detail-card-field-name">Variance</div>
                    <div class="detail-card-field-value whitespace-pre-wrap">
                        {formatCurrency(data.variance)}
                    </div>
                </div>
            </div>
        </div>
    {/snippet}
    {#snippet mainActionsSnippet()}
        <CreateObject href="/settings/budget/expense/new" label="Add Expense" />
    {/snippet}
    {#snippet extraCardsSnippet()}
        <ObjectChildItems title="Expenses">
            {#if data.expenses.length > 0}
                <div class="grid gap-4 grid-cols-1 md:grid-cols-2">
                    {#each data.expenses as expense, index (expense.id)}
                        <div class="list-card">
                            <div class="list-card-body">
                                <div class="list-card-title">
                                    <a class="link link-accent" href={`/settings/budget/expense/${expense.id}`}
                                        >{expense.item}</a>
                                </div>

                                <div class="flex justify-between items-start">
                                    <div class="flex-1">
                                        <div class="flex gap-4 mt-2 text-sm">
                                            {#if expense.date}
                                                <span class="flex items-center gap-1">
                                                    <span class="icon-[lucide--calendar] size-3"></span>
                                                    {formatDate(expense.date)}
                                                </span>
                                            {/if}
                                            {#if expense.estimatedAmount}
                                                <span>
                                                    Est: {formatCurrency(Number(expense.estimatedAmount))}
                                                </span>
                                            {/if}
                                            {#if expense.actualAmount}
                                                <span class="font-semibold">
                                                    Actual: {formatCurrency(Number(expense.actualAmount))}
                                                </span>
                                            {/if}
                                        </div>
                                    </div>
                                    <div class="flex items-center gap-2">
                                        {#if expense.purchased}
                                            <span class="badge badge-success badge-sm">Purchased</span>
                                        {:else}
                                            <span class="badge badge-warning badge-sm">Pending</span>
                                        {/if}
                                    </div>
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>
            {:else}
                <div class="text-center py-8">
                    <p class="text-base-content mb-4">No expenses in this category yet.</p>
                    <CreateObject href="/settings/budget/expense/new" label="Add Expense" />
                </div>
            {/if}
        </ObjectChildItems>
    {/snippet}
</ObjectDetail>
