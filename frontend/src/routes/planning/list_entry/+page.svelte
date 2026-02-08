<script lang="ts">
    import { goto } from "$app/navigation";
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
    const relativeCrumbs = [{ title: "List Entries" }];

    // Client-side filtering
    let itemFilter = $state("");
    let isCompletedFilter = $state<boolean | null>(null);
    let purchasedFilter = $state<boolean | null>(null);
    let hasExpenseFilter = $state<boolean | null>(null);
    let selectedListId = $state(data.selectedListId || "");

    const filteredEntries = $derived(
        data.entries
            .filter((entry) => {
                if (itemFilter && !entry.item.toLowerCase().includes(itemFilter.toLowerCase())) {
                    return false;
                }
                if (isCompletedFilter !== null && entry.isCompleted !== isCompletedFilter) {
                    return false;
                }
                if (purchasedFilter !== null && entry.purchased !== purchasedFilter) {
                    return false;
                }
                if (hasExpenseFilter !== null) {
                    const hasExpense = entry.associatedExpenseId !== null;
                    if (hasExpense !== hasExpenseFilter) {
                        return false;
                    }
                }
                return true;
            })
            .sort((a, b) => {
                // Sort by list name first, then by order
                const listA = data.lists.find((l) => l.id === a.listId);
                const listB = data.lists.find((l) => l.id === b.listId);
                const listCompare = (listA?.name || "").localeCompare(listB?.name || "");
                if (listCompare !== 0) return listCompare;
                return a.order - b.order;
            }),
    );

    const entryData = writable(filteredEntries);
    $effect(() => {
        entryData.set(filteredEntries);
    });

    function clearFilters() {
        itemFilter = "";
        isCompletedFilter = null;
        purchasedFilter = null;
        hasExpenseFilter = null;
    }

    function handleListFilterChange() {
        const url = new URL(window.location.href);
        if (selectedListId) {
            url.searchParams.set("listId", selectedListId);
        } else {
            url.searchParams.delete("listId");
        }
        goto(url.pathname + url.search);
    }

    const table = createTable(entryData, {
        sort: addSortBy(),
        page: addPagination({ initialPageSize: 25 }),
    });

    const columns = table.createColumns([
        table.column({
            accessor: "listId",
            header: "List",
        }),
        table.column({
            accessor: "item",
            header: "Item",
        }),
        table.column({
            accessor: "isCompleted",
            header: "Status",
        }),
        table.column({
            accessor: "quantity",
            header: "Quantity",
        }),
        table.column({
            accessor: "unitPrice",
            header: "Unit Price",
            cell: ({ value }) => formatPrice(value),
        }),
        table.column({
            accessor: "totalPrice",
            header: "Total",
            cell: ({ value }) => formatPrice(value),
        }),
        table.column({
            accessor: "purchased",
            header: "Purchased",
        }),
        table.column({
            accessor: "associatedExpenseId",
            header: "Expense",
        }),
    ]);

    const { headerRows, pageRows, tableAttrs, tableBodyAttrs, pluginStates } = table.createViewModel(columns);
    const { hasNextPage, hasPreviousPage, pageIndex, pageSize } = pluginStates.page;

    function formatPrice(price: number | string): string {
        const num = typeof price === "string" ? parseFloat(price) : price;
        return new Intl.NumberFormat("en-US", {
            style: "currency",
            currency: "USD",
        }).format(num);
    }

    function getListName(listId: string): string {
        const list = data.lists.find((l) => l.id === listId);
        return list?.name || "Unknown List";
    }

    const entryStats: iStat[] = $derived([
        {
            title: "Total Entries",
            value: filteredEntries.length,
            description: `of ${data.count} total`,
            icon: "check-square",
        },
        {
            title: "Total Value",
            value: formatPrice(filteredEntries.reduce((sum, e) => sum + parseFloat(e.totalPrice || "0"), 0)),
            description: `across all items`,
            icon: "dollar-sign",
        },
    ]);
    const countStats: iStat[] = $derived([
        {
            title: "Completed",
            value: filteredEntries.filter((e) => e.isCompleted).length,
            description: `items finished`,
            icon: "check-circle",
        },
        {
            title: "Pending",
            value: filteredEntries.filter((e) => !e.isCompleted).length,
            description: `items remaining`,
            icon: "circle",
        },
    ]);
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader title="All List Entries" description="View and manage all list items" showButtons={false}>
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
                                <label class="table-filter-card-field-name" for="list-filter">
                                    <span>Filter by List</span>
                                </label>
                                <select
                                    id="list-filter"
                                    class="table-filter-card-field-value-select"
                                    bind:value={selectedListId}
                                    onchange={handleListFilterChange}>
                                    <option value="">All Lists</option>
                                    {#each data.lists as list (list.id)}
                                        <option value={list.id}>{list.name}</option>
                                    {/each}
                                </select>
                            </div>

                            <div class="form-control">
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
                                <label class="table-filter-card-field-name" for="completed-filter">
                                    <span>Status</span>
                                </label>
                                <select
                                    id="completed-filter"
                                    class="table-filter-card-field-value-select"
                                    bind:value={isCompletedFilter}>
                                    <option value={null}>All</option>
                                    <option value={true}>Completed</option>
                                    <option value={false}>Pending</option>
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

                            <div class="form-control">
                                <label class="table-filter-card-field-name" for="expense-filter">
                                    <span>Expenses</span>
                                </label>
                                <select
                                    id="expense-filter"
                                    class="table-filter-card-field-value-select"
                                    bind:value={hasExpenseFilter}>
                                    <option value={null}>All</option>
                                    <option value={true}>With Expense</option>
                                    <option value={false}>Without Expense</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Stats Panel -->
                <div class="flex flex-col">
                    <Stats objects={entryStats} />
                    <Stats objects={countStats} />
                </div>
            </div>
        </div>
    </ProtectedPageHeader>

    <div class="shadow-lg overflow-hidden">
        <div class="overflow-x-auto">
            <table {...$tableAttrs} class="w-full">
                <thead class="bg-base-300 text-accent">
                    {#each $headerRows as headerRow (headerRow.id)}
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
                                            {#if cell.id === "listId"}
                                                <a
                                                    href="/settings/list/{row.original.listId}"
                                                    class="link link-accent hover:underline">
                                                    {getListName(row.original.listId)}
                                                </a>
                                            {:else if cell.id === "item"}
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
                                            {:else if cell.id === "isCompleted"}
                                                <span
                                                    class="badge"
                                                    class:badge-success={row.original.isCompleted}
                                                    class:badge-warning={!row.original.isCompleted}>
                                                    {row.original.isCompleted ? "Completed" : "Pending"}
                                                </span>
                                            {:else if cell.id === "totalPrice"}
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
                                            {:else if cell.id === "associatedExpenseId"}
                                                {#if row.original.associatedExpenseId}
                                                    <a
                                                        href="/settings/expense/{row.original.associatedExpenseId}"
                                                        class="link link-accent hover:underline">
                                                        <span class="icon-[lucide--receipt] size-5"></span>
                                                    </a>
                                                {:else}
                                                    <span class="text-secondary-content/30">-</span>
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
                                        <ViewDetails href="/settings/list_entry/{row.original.id}" size="sm" />
                                        <EditObject href="/settings/list_entry/{row.original.id}/edit" size="sm" />
                                    </div>
                                </td>
                            </tr>
                        </Subscribe>
                    {:else}
                        <tr>
                            <td colspan="9" class="text-center py-8">
                                <span class="icon-[lucide--inbox] size-12 text-secondary-content/30 mx-auto block mb-2"
                                ></span>
                                <p class="text-secondary-content/70">No entries found</p>
                                <p class="text-sm text-secondary-content/50">
                                    {#if itemFilter || isCompletedFilter !== null || purchasedFilter !== null || hasExpenseFilter !== null}
                                        Try adjusting your filters
                                    {:else}
                                        No list entries available
                                    {/if}
                                </p>
                            </td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>

        <!-- Pagination Controls -->
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
                    <option value={filteredEntries.length}>All</option>
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
