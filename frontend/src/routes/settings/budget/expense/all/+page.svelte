<script lang="ts">
    import Stats from "$lib/components/Stats.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();

    const relativeCrumbs = [
        { title: "Budget", href: "/settings/budget" },
        { title: "All Expenses", href: "/settings/budget/expense/all" },
    ];

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

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader title="All Expenses" description="View and manage all wedding expenses" showButtons={false} />

    <div class="space-y-6">
        <Stats
            objects={[
                {
                    title: "Total Expenses",
                    value: data.totalExpenses.toString(),
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

        <div class="card bg-base-100 shadow-xl">
            <div class="card-body">
                <h2 class="card-title">Expenses</h2>
                <div class="overflow-x-auto">
                    <table class="table table-zebra">
                        <thead>
                            <tr>
                                <th>Item</th>
                                <th>Category</th>
                                <th>Date</th>
                                <th>Estimated</th>
                                <th>Actual</th>
                                <th>Status</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each data.expenses as expense}
                                <tr>
                                    <td>
                                        <div class="font-semibold">{expense.item}</div>
                                        {#if expense.description}
                                            <div class="text-sm text-base-content/70 line-clamp-1">
                                                {expense.description}
                                            </div>
                                        {/if}
                                    </td>
                                    <td>
                                        {#if expense.categoryName}
                                            <a
                                                href={`/settings/budget/category/${expense.categoryId}`}
                                                class="link link-primary">
                                                {expense.categoryName}
                                            </a>
                                        {:else}
                                            <span class="text-base-content/50">Uncategorized</span>
                                        {/if}
                                    </td>
                                    <td>{formatDate(expense.date)}</td>
                                    <td>
                                        {#if expense.estimatedAmount}
                                            {formatCurrency(Number(expense.estimatedAmount))}
                                        {:else}
                                            <span class="text-base-content/50">--</span>
                                        {/if}
                                    </td>
                                    <td>
                                        {#if expense.actualAmount}
                                            <span class="font-semibold">
                                                {formatCurrency(Number(expense.actualAmount))}
                                            </span>
                                        {:else}
                                            <span class="text-base-content/50">--</span>
                                        {/if}
                                    </td>
                                    <td>
                                        {#if expense.purchased}
                                            <span class="badge badge-success badge-sm">Purchased</span>
                                        {:else}
                                            <span class="badge badge-ghost badge-sm">Pending</span>
                                        {/if}
                                    </td>
                                    <td>
                                        <a href={`/settings/budget/expense/${expense.id}`} class="btn btn-ghost btn-xs">
                                            View
                                        </a>
                                    </td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</ProtectedPageShell>
