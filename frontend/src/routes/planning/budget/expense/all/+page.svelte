<script lang="ts">
    import Stats from "$lib/components/Stats.svelte";
    import EditObject from "$lib/components/buttons/EditObject.svelte";
    import ViewDetails from "$lib/components/buttons/ViewDetails.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import { createTable, Subscribe, Render } from "svelte-headless-table";
    import { addSortBy, addPagination } from "svelte-headless-table/plugins";
    import { writable } from "svelte/store";
    import type { PageData, iStat } from "./$types";

    const { data }: { data: PageData } = $props();

    const relativeCrumbs = [
        { title: "Budget", href: "/planning/budget" },
        { title: "All Expenses", href: "/planning/budget/expense/all" },
    ];

    // Client-side filtering
    let itemFilter = $state("");
    let categoryFilter = $state("");
    let purchasedFilter = $state<boolean | null>(null);

    const filteredExpenses = $derived(
        data.expenses.filter((expense) => {
            if (itemFilter && !expense.item.toLowerCase().includes(itemFilter.toLowerCase())) {
                return false;
            }
            if (categoryFilter && expense.categoryId !== categoryFilter) {
                return false;
            }
            if (purchasedFilter !== null && expense.purchased !== purchasedFilter) {
                return false;
            }
            return true;
        }),
    );

    const expenseData = writable(filteredExpenses);
    $effect(() => {
        expenseData.set(filteredExpenses);
    });

    function clearFilters() {
        itemFilter = "";
        categoryFilter = "";
        purchasedFilter = null;
    }

    const table = createTable(expenseData, {
        sort: addSortBy(),
        page: addPagination({ initialPageSize: 10 }),
    });

    const columns = table.createColumns([
        table.column({
            accessor: "item",
            header: "Item",
        }),
        table.column({
            accessor: "categoryName",
            header: "Category",
        }),
        table.column({
            accessor: "date",
            header: "Date",
            cell: ({ value }) => formatDate(value),
        }),
        table.column({
            accessor: "quantity",
            header: "Quantity",
            cell: ({ value }) => value || "-",
        }),
        table.column({
            accessor: "unitPrice",
            header: "Unit Price",
            cell: ({ value }) => (value ? formatCurrency(value) : "-"),
        }),
        table.column({
            accessor: "estimatedAmount",
            header: "Estimated",
            cell: ({ value }) => formatCurrency(value),
        }),
        table.column({
            accessor: "actualAmount",
            header: "Actual",
            cell: ({ value }) => formatCurrency(value),
        }),
        table.column({
            accessor: "purchased",
            header: "Purchased",
        }),
    ]);

    const { headerRows, pageRows, tableAttrs, tableBodyAttrs, pluginStates } = table.createViewModel(columns);
    const { hasNextPage, hasPreviousPage, pageIndex, pageSize } = pluginStates.page;

    function formatCurrency(amount: number | string | null | undefined): string {
        if (amount === null || amount === undefined) return "--";
        const num = typeof amount === "string" ? parseFloat(amount) : amount;
        return new Intl.NumberFormat("en-US", {
            style: "currency",
            currency: "USD",
        }).format(num);
    }

    function formatDate(dateString: string | Date | null | undefined): string {
        if (!dateString) return "N/A";
        const date = dateString instanceof Date ? dateString : new Date(dateString);
        return date.toLocaleDateString();
    }

    // Get unique categories for filter dropdown
    const categories = $derived(
        Array.from(
            new Map(
                data.expenses
                    .filter((e) => e.categoryId)
                    .map((e) => [e.categoryId, { id: e.categoryId, name: e.categoryName }]),
            ).values(),
        ),
    );

    const expenseStatsA: iStat[] = $derived([
        {
            title: "Total Expenses",
            value: filteredExpenses.length,
            description: `of ${data.totalExpenses} total`,
            icon: "receipt",
        },
        {
            title: "Purchased",
            value: filteredExpenses.filter((e) => e.purchased).length,
            description: "items purchased",
            icon: "check-circle",
        },
    ]);
    const expenseStatsB: iStat[] = $derived([
        {
            title: "Estimated Budget",
            value: formatCurrency(
                filteredExpenses.reduce((sum, e) => sum + (e.estimatedAmount ? Number(e.estimatedAmount) : 0), 0),
            ),
            description: "total estimated",
            icon: "calculator",
        },
        {
            title: "Actual Spent",
            value: formatCurrency(
                filteredExpenses.reduce((sum, e) => sum + (e.actualAmount ? Number(e.actualAmount) : 0), 0),
            ),
            description: "total spent",
            icon: "dollar-sign",
        },
    ]);
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader title="All Expenses" description="View and manage all wedding expenses" showButtons={false}>
        <div class="w-full flex justify-start">
            <div class="flex flex-col md:flex-row gap-6 mb-8">
                <div class="table-filter-card w-full md:w-[32rem]" id="filter-panel">
                    <div class="table-filter-card-body">
                        <div class="table-filter-card-title">
                            Filters
                            <button onclick={clearFilters} class="btn btn-error btn-sm">
                                <span class="icon-[lucide--x] size-4"></span>
                                Clear
                            </button>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div class="form-control md:col-span-2">
                                <label class="table-filter-card-field-name" for="item-filter">
                                    <span>Search Items</span>
                                </label>
                                <input
                                    id="item-filter"
                                    type="text"
                                    placeholder="Search..."
                                    class="table-filter-card-field-value-input"
                                    bind:value={itemFilter} />
                            </div>

                            <div class="form-control">
                                <label class="table-filter-card-field-name" for="category-filter">
                                    <span class="label-text">Category</span>
                                </label>
                                <select
                                    id="category-filter"
                                    class="table-filter-card-field-value-select"
                                    bind:value={categoryFilter}>
                                    <option value="">All Categories</option>
                                    {#each categories as category (category.id)}
                                        <option value={category.id}>{category.name}</option>
                                    {/each}
                                </select>
                            </div>

                            <div class="form-control">
                                <label class="table-filter-card-field-name" for="purchased-filter">
                                    <span>Purchased</span>
                                </label>
                                <select
                                    id="purchased-filter"
                                    class="table-filter-card-field-value-select"
                                    bind:value={purchasedFilter}>
                                    <option value={null}>All</option>
                                    <option value={true}>Yes</option>
                                    <option value={false}>No</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Stats Panel -->
                <div class="flex flex-col">
                    <Stats objects={expenseStatsA} />
                    <Stats objects={expenseStatsB} />
                </div>
            </div>
        </div>
    </ProtectedPageHeader>

    <div class="shadow-lg overflow-hidden">
        <div class="overflow-x-auto">
            <table {...$tableAttrs} class="w-full">
                <thead class="bg-base-300 text-accent">
                    {#each $headerRows as headerRow, index (headerRow.id)}
                        <Subscribe rowAttrs={headerRow.attrs()}>
                            <tr>
                                {#each headerRow.cells as cell (cell.id)}
                                    <Subscribe attrs={cell.attrs()} let:attrs props={cell.props()} let:props>
                                        <th
                                            {...attrs}
                                            class="px-3 py-2 text-left text-xs font-medium uppercase tracking-wider cursor-pointer select-none hover:bg-base-300 transition-colors"
                                            onclick={props.sort.toggle}>
                                            <div class="flex items-center gap-1">
                                                <Render of={cell.render()} />
                                                {#if props.sort.order === "asc"}
                                                    🔼
                                                {:else if props.sort.order === "desc"}
                                                    🔽
                                                {/if}
                                            </div>
                                        </th>
                                    </Subscribe>
                                {/each}
                                <th class="px-3 py-2 text-left text-xs font-medium uppercase tracking-wider">
                                    Actions
                                </th>
                            </tr>
                        </Subscribe>
                    {/each}
                </thead>
                <tbody {...$tableBodyAttrs} class="bg-base-300 divide-y divide-primary-content">
                    {#each $pageRows as row (row.id)}
                        <Subscribe rowAttrs={row.attrs()} let:rowAttrs>
                            <tr {...rowAttrs} class="hover:bg-base-200 transition-colors">
                                {#each row.cells as cell (cell.id)}
                                    <Subscribe attrs={cell.attrs()} let:attrs>
                                        <td {...attrs} class="px-3 py-2 whitespace-nowrap text-sm">
                                            {#if cell.id === "item"}
                                                <div class="flex flex-col">
                                                    <span class="font-semibold text-secondary-content">
                                                        <Render of={cell.render()} />
                                                    </span>
                                                    {#if row.original.description}
                                                        <span class="text-xs text-secondary-content/70 line-clamp-1">
                                                            {row.original.description}
                                                        </span>
                                                    {/if}
                                                    {#if row.original.url}
                                                        <a
                                                            href={row.original.url}
                                                            target="_blank"
                                                            rel="noopener noreferrer"
                                                            class="text-xs link link-accent hover:underline">
                                                            <span class="icon-[lucide--external-link] size-3"></span>
                                                            View Link
                                                        </a>
                                                    {/if}
                                                </div>
                                            {:else if cell.id === "categoryName"}
                                                {#if row.original.categoryName}
                                                    <a
                                                        href="/planning/budget/category/{row.original.categoryId}"
                                                        class="link link-accent hover:underline">
                                                        <Render of={cell.render()} />
                                                    </a>
                                                {:else}
                                                    <span class="text-secondary-content/50">Uncategorized</span>
                                                {/if}
                                            {:else if cell.id === "actualAmount"}
                                                <span class="font-semibold text-secondary-content">
                                                    <Render of={cell.render()} />
                                                </span>
                                            {:else if cell.id === "purchased"}
                                                {#if row.original.purchased}
                                                    <span class="icon-[lucide--check-circle] size-5 text-success"
                                                    ></span>
                                                {:else}
                                                    <span class="icon-[lucide--circle] size-5 text-secondary-content/30"
                                                    ></span>
                                                {/if}
                                            {:else}
                                                <span class="text-secondary-content">
                                                    <Render of={cell.render()} />
                                                </span>
                                            {/if}
                                        </td>
                                    </Subscribe>
                                {/each}
                                <td class="px-3 py-2 whitespace-nowrap text-sm">
                                    <div class="flex gap-2">
                                        <ViewDetails href="/planning/budget/expense/{row.original.id}" size="sm" />
                                        <EditObject href="/planning/budget/expense/{row.original.id}/edit" size="sm" />
                                    </div>
                                </td>
                            </tr>
                        </Subscribe>
                    {:else}
                        <tr>
                            <td colspan="9" class="text-center py-8">
                                <span class="icon-[lucide--inbox] size-12 text-secondary-content/30 mx-auto block mb-2"
                                ></span>
                                <p class="text-secondary-content/70">No expenses found</p>
                                <p class="text-sm text-secondary-content/50">
                                    {#if itemFilter || categoryFilter || purchasedFilter !== null}
                                        Try adjusting your filters
                                    {:else}
                                        No expenses available
                                    {/if}
                                </p>
                            </td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>

        <div class="flex justify-between items-center mt-4 px-4 py-3">
            <div class="text-sm text-accent-content">
                Page {$pageIndex + 1}
            </div>
            <div class="flex items-center gap-2">
                <label for="page-size" class="text-sm text-accent-content">Rows per page:</label>
                <select
                    id="page-size"
                    class="select select-bordered select-sm bg-accent text-accent-content"
                    bind:value={$pageSize}>
                    <option value={10}>10</option>
                    <option value={25}>25</option>
                    <option value={50}>50</option>
                    <option value={100}>100</option>
                    <option value={filteredExpenses.length}>All</option>
                </select>
            </div>
            <div class="join">
                <button
                    class="join-item btn btn-accent btn-sm"
                    disabled={!$hasPreviousPage}
                    onclick={() => ($pageIndex = $pageIndex - 1)}>
                    <span class="icon-[lucide--chevron-left] size-4"></span>
                    Previous
                </button>
                <button
                    class="join-item btn btn-accent btn-sm"
                    disabled={!$hasNextPage}
                    onclick={() => ($pageIndex = $pageIndex + 1)}>
                    Next
                    <span class="icon-[lucide--chevron-right] size-4"></span>
                </button>
            </div>
        </div>
    </div>
</ProtectedPageShell>
