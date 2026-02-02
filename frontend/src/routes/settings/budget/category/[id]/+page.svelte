<script lang="ts">
    import Stats from "$lib/components/Stats.svelte";
    import ObjectChildItems from "$lib/components/object/ObjectChildItems.svelte";
    import ObjectDetail from "$lib/components/object/ObjectDetail.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();

    const relativeCrumbs = [
        { title: "Budget", href: "/settings/budget" },
        { title: data.category.name, href: `/settings/budget/category/${data.category.id}` },
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

            <Stats
                objects={[
                    {
                        title: "Total Expenses",
                        value: data.expenses.length.toString(),
                        icon: "lucide--receipt",
                    },
                    {
                        title: "Estimated Budget",
                        value: formatCurrency(data.totalEstimated),
                        icon: "lucide--calculator",
                    },
                    {
                        title: "Actual Spent",
                        value: formatCurrency(data.totalActual),
                        icon: "lucide--dollar-sign",
                    },
                    {
                        title: "Variance",
                        value: formatCurrency(data.variance),
                        icon: data.variance >= 0 ? "lucide--trending-up" : "lucide--trending-down",
                    },
                ]} />
        </div>
    {/snippet}

    {#snippet extraCardsSnippet()}
        <ObjectChildItems
            items={data.expenses}
            title="Expenses"
            addText="Add Expense"
            addLink="/settings/budget/expense/new"
            itemLink={(expense) => `/settings/budget/expense/${expense.id}`}>
            {#snippet itemContent(expense)}
                <div class="flex-1">
                    <div class="font-semibold">{expense.item}</div>
                    {#if expense.description}
                        <div class="text-sm text-base-content/70 line-clamp-1">
                            {expense.description}
                        </div>
                    {/if}
                    <div class="flex gap-4 mt-2 text-sm">
                        {#if expense.date}
                            <span class="flex items-center gap-1">
                                <span class="icon-[lucide--calendar] size-3"></span>
                                {formatDate(expense.date)}
                            </span>
                        {/if}
                        {#if expense.estimatedAmount}
                            <span class="text-base-content/70">
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
                        <span class="badge badge-ghost badge-sm">Pending</span>
                    {/if}
                </div>
            {/snippet}
        </ObjectChildItems>
    {/snippet}
</ObjectDetail>
