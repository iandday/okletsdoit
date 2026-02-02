<script lang="ts">
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";
    import Stats from "$lib/components/Stats.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
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

    function getStatusBadge(entry: any): string {
        if (entry.isCompleted) return "badge-success";
        return "badge-warning";
    }

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

    const entryStats: iStat[] = [
        {
            title: "Total Entries",
            value: filteredEntries.length,
            description: `of ${data.count} total`,
            icon: "check-square",
        },
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
        {
            title: "Total Value",
            value: formatPrice(filteredEntries.reduce((sum, e) => sum + parseFloat(e.totalPrice || "0"), 0)),
            description: `across all items`,
            icon: "dollar-sign",
        },
    ];
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader title="All List Entries" description="View and manage all list items" showButtons={false}>
        <div class="w-full flex justify-start">
            <div class="flex flex-col md:flex-row gap-6 mb-8">
                <div class="config-card w-full md:w-[32rem]" id="filter-panel">
                    <div class="config-card-body">
                        <div class="flex items-center justify-between mb-4">
                            <h3 class="text-lg font-semibold">Filters</h3>
                            <button onclick={clearFilters} class="btn btn-error btn-sm">
                                <span class="icon-[lucide--x] size-4"></span>
                                Clear
                            </button>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <!-- List Filter -->
                            <div class="form-control md:col-span-2">
                                <label class="label" for="list-filter">
                                    <span class="label-text">Filter by List</span>
                                </label>
                                <select
                                    id="list-filter"
                                    class="select select-bordered"
                                    bind:value={selectedListId}
                                    onchange={handleListFilterChange}>
                                    <option value="">All Lists</option>
                                    {#each data.lists as list (list.id)}
                                        <option value={list.id}>{list.name}</option>
                                    {/each}
                                </select>
                            </div>

                            <!-- Item Search -->
                            <div class="form-control">
                                <label class="label" for="item-filter">
                                    <span class="label-text">Search Items</span>
                                </label>
                                <input
                                    id="item-filter"
                                    type="text"
                                    placeholder="Search..."
                                    class="input input-bordered"
                                    bind:value={itemFilter} />
                            </div>

                            <!-- Status Filter -->
                            <div class="form-control">
                                <label class="label" for="completed-filter">
                                    <span class="label-text">Status</span>
                                </label>
                                <select
                                    id="completed-filter"
                                    class="select select-bordered"
                                    bind:value={isCompletedFilter}>
                                    <option value={null}>All</option>
                                    <option value={true}>Completed</option>
                                    <option value={false}>Pending</option>
                                </select>
                            </div>

                            <!-- Purchased Filter -->
                            <div class="form-control">
                                <label class="label" for="purchased-filter">
                                    <span class="label-text">Purchased</span>
                                </label>
                                <select
                                    id="purchased-filter"
                                    class="select select-bordered"
                                    bind:value={purchasedFilter}>
                                    <option value={null}>All</option>
                                    <option value={true}>Yes</option>
                                    <option value={false}>No</option>
                                </select>
                            </div>

                            <!-- Expense Filter -->
                            <div class="form-control">
                                <label class="label" for="expense-filter">
                                    <span class="label-text">Expenses</span>
                                </label>
                                <select
                                    id="expense-filter"
                                    class="select select-bordered"
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
                <div class="flex-1">
                    <Stats objects={entryStats} />
                </div>
            </div>
        </div>
    </ProtectedPageHeader>

    <!-- Entries Table -->
    <div class="overflow-x-auto">
        <table class="table table-zebra">
            <thead>
                <tr>
                    <th>List</th>
                    <th>Item</th>
                    <th>Status</th>
                    <th>Quantity</th>
                    <th>Unit Price</th>
                    <th>Total</th>
                    <th>Purchased</th>
                    <th>Expense</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {#each filteredEntries as entry (entry.id)}
                    <tr>
                        <td>
                            <a href="/settings/list/{entry.listId}" class="link link-primary">
                                {getListName(entry.listId)}
                            </a>
                        </td>
                        <td>
                            <div class="flex flex-col">
                                <span class="font-semibold">{entry.item}</span>
                                {#if entry.description}
                                    <span class="text-sm text-base-content/70 line-clamp-1">
                                        {entry.description}
                                    </span>
                                {/if}
                                {#if entry.url}
                                    <a
                                        href={entry.url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        class="text-sm link link-primary">
                                        <span class="icon-[lucide--external-link] size-3"></span>
                                        View Link
                                    </a>
                                {/if}
                            </div>
                        </td>
                        <td>
                            <span class="badge {getStatusBadge(entry)}">
                                {entry.isCompleted ? "Completed" : "Pending"}
                            </span>
                        </td>
                        <td>{entry.quantity}</td>
                        <td>{formatPrice(entry.unitPrice)}</td>
                        <td class="font-semibold">{formatPrice(entry.totalPrice)}</td>
                        <td>
                            {#if entry.purchased}
                                <span class="icon-[lucide--check-circle] size-5 text-success"></span>
                            {:else}
                                <span class="icon-[lucide--circle] size-5 text-base-content/30"></span>
                            {/if}
                        </td>
                        <td>
                            {#if entry.associatedExpenseId}
                                <a href="/settings/expense/{entry.associatedExpenseId}" class="link link-primary">
                                    <span class="icon-[lucide--receipt] size-5"></span>
                                </a>
                            {:else}
                                <span class="text-base-content/30">-</span>
                            {/if}
                        </td>
                        <td>
                            <div class="flex gap-2">
                                <a href="/settings/list_entry/{entry.id}" class="btn btn-ghost btn-xs">
                                    <span class="icon-[lucide--eye] size-4"></span>
                                </a>
                                <a href="/settings/list_entry/{entry.id}/edit" class="btn btn-ghost btn-xs">
                                    <span class="icon-[lucide--pencil] size-4"></span>
                                </a>
                            </div>
                        </td>
                    </tr>
                {:else}
                    <tr>
                        <td colspan="9" class="text-center py-8">
                            <span class="icon-[lucide--inbox] size-12 text-base-content/30 mx-auto block mb-2"></span>
                            <p class="text-base-content/70">No entries found</p>
                            <p class="text-sm text-base-content/50">
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
</ProtectedPageShell>
