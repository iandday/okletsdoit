<script lang="ts">
    import { enhance } from "$app/forms";
    import DeleteObject from "$lib/components/buttons/DeleteObject.svelte";
    import EditObject from "$lib/components/buttons/EditObject.svelte";
    import ViewDetails from "$lib/components/buttons/ViewDetails.svelte";
    import ObjectChildItems from "$lib/components/object/ObjectChildItems.svelte";
    import ObjectDetail from "$lib/components/object/ObjectDetail.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();

    const relativeCrumbs = $derived([
        { title: "Lists", href: "/planning/list" },
        { title: data.list.name || "List", href: `/planning/list/${data.list.id}` },
    ]);

    const displayName = $derived(data.list.name || "List");

    // Client-side filtering
    let itemFilter = $state("");
    let isCompletedFilter = $state<boolean | null>(null);
    let purchasedFilter = $state<boolean | null>(null);
    let hasExpenseFilter = $state<boolean | null>(null);

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
                    const hasExpense = Boolean(entry.associatedExpenseId);
                    if (hasExpense !== hasExpenseFilter) {
                        return false;
                    }
                }
                return true;
            })
            .sort((a, b) => a.order - b.order),
    );

    function clearFilters() {
        itemFilter = "";
        isCompletedFilter = null;
        purchasedFilter = null;
        hasExpenseFilter = null;
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
</script>

<ObjectDetail
    {relativeCrumbs}
    title={displayName}
    editLink={`/planning/list/${data.list.id}/edit`}
    deleteAction="?/delete"
    object={data.list}>
    {#snippet mainSnippet()}
        <div class="space-y-6">
            <!-- List Information -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <div class="detail-card-field-name">List Name</div>
                    <div class="detail-card-field-value">{data.list.name}</div>
                </div>

                {#if data.list.description}
                    <div class="md:col-span-2">
                        <div class="detail-card-field-name">Description</div>
                        <div class="detail-card-field-value">{data.list.description}</div>
                    </div>
                {/if}
            </div>

            <!-- Statistics -->
            <div>
                <h3 class="text-lg font-semibold mb-3">Statistics</h3>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div>
                        <div class="detail-card-field-name">Total Items</div>
                        <div class="detail-card-field-value text-2xl font-bold">{data.list.totalEntries}</div>
                    </div>
                    <div>
                        <div class="detail-card-field-name">Completed</div>
                        <div class="detail-card-field-value text-2xl font-bold text-success">
                            {data.list.completedEntries}
                        </div>
                    </div>
                    <div>
                        <div class="detail-card-field-name">Pending</div>
                        <div class="detail-card-field-value text-2xl font-bold text-warning">
                            {data.list.pendingEntries}
                        </div>
                    </div>
                    <div>
                        <div class="detail-card-field-name">Progress</div>
                        <div class="detail-card-field-value text-2xl font-bold">{data.list.completionPercentage}%</div>
                    </div>
                </div>

                <!-- Progress Bar -->
                <div class="mt-4">
                    <progress
                        class="progress {data.list.completionPercentage === 100
                            ? 'progress-success'
                            : data.list.completionPercentage >= 50
                              ? 'progress-warning'
                              : 'progress-info'} w-full"
                        value={data.list.completionPercentage}
                        max="100"></progress>
                </div>
            </div>
        </div>
    {/snippet}
    {#snippet extraCardsSnippet()}
        <ObjectChildItems title="List Items">
            <div class="flex items-center justify-between mb-4">
                <a href="/planning/list/{data.list.id}/entry/new" class="btn btn-sm btn-accent gap-2">
                    <span class="icon-[lucide--plus] size-4"></span>
                    Add Item
                </a>

                {#if filteredEntries.length > 0}
                    <button onclick={clearFilters} class="btn btn-error btn-sm gap-2">
                        <span class="icon-[lucide--filter-x] size-4"></span>
                        Clear Filters
                    </button>
                {/if}
            </div>

            <!-- Filters -->
            {#if data.entries.length > 0}
                <div class="config-card mb-6">
                    <div class="config-card-body">
                        <h3 class="text-sm config-card-title mb-4">Filter Items</h3>

                        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                            <div class="form-control">
                                <label class="label" for="item-filter">
                                    <span class="config-card-field-name">Search Items</span>
                                </label>
                                <input
                                    id="item-filter"
                                    type="text"
                                    placeholder="Search..."
                                    class="input input-sm input-bordered"
                                    bind:value={itemFilter} />
                            </div>

                            <div class="form-control">
                                <label class="label" for="completed-filter">
                                    <span class="config-card-field-name">Status</span>
                                </label>
                                <select
                                    id="completed-filter"
                                    class="select select-sm select-bordered"
                                    bind:value={isCompletedFilter}>
                                    <option value={null}>All</option>
                                    <option value={true}>Completed</option>
                                    <option value={false}>Pending</option>
                                </select>
                            </div>

                            <div class="form-control">
                                <label class="label" for="purchased-filter">
                                    <span class="config-card-field-name">Purchased</span>
                                </label>
                                <select
                                    id="purchased-filter"
                                    class="select select-sm select-bordered"
                                    bind:value={purchasedFilter}>
                                    <option value={null}>All</option>
                                    <option value={true}>Yes</option>
                                    <option value={false}>No</option>
                                </select>
                            </div>

                            <div class="form-control">
                                <label class="label" for="expense-filter">
                                    <span class="config-card-field-name">Expenses</span>
                                </label>
                                <select
                                    id="expense-filter"
                                    class="select select-sm select-bordered"
                                    bind:value={hasExpenseFilter}>
                                    <option value={null}>All</option>
                                    <option value={true}>With Expense</option>
                                    <option value={false}>Without Expense</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            {/if}

            {#if data.entries.length === 0}
                <p class="text-sm italic">No items yet</p>
            {:else}
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mt-4">
                    {#each filteredEntries as entry (entry.id)}
                        <div class="list-card">
                            <div class="list-card-body">
                                <div class="list-card-title flex items-start justify-between">
                                    <span>{entry.item}</span>
                                    <span class="badge {getStatusBadge(entry)} badge-sm">
                                        {entry.isCompleted ? "Completed" : "Pending"}
                                    </span>
                                </div>

                                {#if entry.description}
                                    <div class="text-sm list-card-value mb-2">{entry.description}</div>
                                {/if}

                                <div class="flex flex-wrap gap-2 my-2">
                                    <span class="badge badge-outline badge-sm">
                                        <span class="icon-[lucide--package] size-3 mr-1"></span>
                                        Qty: {entry.quantity}
                                    </span>
                                    {#if entry.associatedExpenseId}
                                        <span class="badge badge-outline badge-sm">
                                            <span class="icon-[lucide--dollar-sign] size-3 mr-1"></span>
                                            {formatPrice(entry.unitPrice)}
                                        </span>
                                        <span class="badge badge-success badge-sm">
                                            <span class="icon-[lucide--calculator] size-3 mr-1"></span>
                                            Total: {formatPrice(entry.totalPrice)}
                                        </span>
                                    {/if}
                                    {#if entry.vendor}
                                        <span class="badge badge-info badge-sm">
                                            <span class="icon-[lucide--store] size-3 mr-1"></span>
                                            {entry.vendor.name || entry.vendor.company || "Vendor"}
                                        </span>
                                    {/if}
                                    {#if entry.purchased}
                                        <span class="badge badge-success badge-sm">
                                            <span class="icon-[lucide--check-circle] size-3 mr-1"></span>
                                            Purchased
                                        </span>
                                    {/if}
                                </div>

                                {#if entry.url}
                                    <a
                                        href={entry.url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        class="text-sm link link-primary flex items-center gap-1">
                                        <span class="icon-[lucide--external-link] size-3"></span>
                                        View Product Link
                                    </a>
                                {/if}
                            </div>
                            <div class="list-card-actions flex gap-2">
                                <ViewDetails href={`/planning/list_entry/${entry.id}`} label="View Details" />
                                <EditObject href={`/planning/list_entry/${entry.id}/edit`} label="Edit" />

                                <DeleteObject
                                    action="?/deleteEntry"
                                    href="#"
                                    label="Remove"
                                    value={entry.id}
                                    confirmMessage="Are you sure you want to remove this item?" />
                            </div>
                        </div>
                    {:else}
                        <div class="col-span-full text-center py-8">
                            <span class="icon-[lucide--inbox] size-12 text-base-content/30 mx-auto block mb-2"></span>
                            <p class="text-base-content/70">No items found</p>
                            <p class="text-sm text-base-content/50">
                                {#if itemFilter || isCompletedFilter !== null || purchasedFilter !== null || hasExpenseFilter !== null}
                                    Try adjusting your filters
                                {:else}
                                    This shouldn't happen - please report this bug
                                {/if}
                            </p>
                        </div>
                    {/each}
                </div>
            {/if}
        </ObjectChildItems>
    {/snippet}
</ObjectDetail>
