<script lang="ts">
    import Stats from "$lib/components/Stats.svelte";
    import CreateObject from "$lib/components/buttons/CreateObject.svelte";
    import ViewDetails from "$lib/components/buttons/ViewDetails.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { PageData, iStat } from "./$types";

    const { data }: { data: PageData } = $props();
    const relativeCrumbs = [{ title: "Lists" }];

    // Client-side filtering
    let nameFilter = $state("");
    let completionFilter = $state<string | null>(null);
    let hasExpensesFilter = $state<boolean | null>(null);

    const filteredLists = $derived(
        data.lists
            .filter((list) => {
                if (nameFilter && !list.name.toLowerCase().includes(nameFilter.toLowerCase())) {
                    return false;
                }
                if (completionFilter) {
                    if (completionFilter === "complete" && list.completionPercentage !== 100) {
                        return false;
                    }
                    if (
                        completionFilter === "in-progress" &&
                        (list.completionPercentage === 0 || list.completionPercentage === 100)
                    ) {
                        return false;
                    }
                    if (completionFilter === "not-started" && list.completionPercentage !== 0) {
                        return false;
                    }
                }
                if (hasExpensesFilter !== null && list.hasExpenses !== hasExpensesFilter) {
                    return false;
                }
                return true;
            })
            .sort((a, b) => a.name.localeCompare(b.name)),
    );

    function clearFilters() {
        nameFilter = "";
        completionFilter = null;
        hasExpensesFilter = null;
    }

    function getCompletionClass(percentage: number): string {
        if (percentage === 100) return "progress-success";
        if (percentage >= 50) return "progress-warning";
        return "progress-info";
    }

    const listStats: iStat[] = [
        {
            title: "Total Lists",
            value: filteredLists.length,
            description: `of ${data.count} total`,
            icon: "list",
        },
        {
            title: "Total Entries",
            value: filteredLists.reduce((sum, list) => sum + list.totalEntries, 0),
            description: `across all lists`,
            icon: "check-square",
        },
    ];
    const completionStats: iStat[] = [
        {
            title: "Completed",
            value: filteredLists.reduce((sum, list) => sum + list.completedEntries, 0),
            description: `items finished`,
            icon: "check-circle",
        },
        {
            title: "Pending",
            value: filteredLists.reduce((sum, list) => sum + list.pendingEntries, 0),
            description: `items remaining`,
            icon: "circle",
        },
    ];
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader
        title="Wedding Lists"
        description="Manage your wedding planning lists.  Each list is made up of one or more entries.  One or more entries (balloons and candles) can be associated with an expense item, such as venue decorations."
        showButtons={false}>
        <div class="w-full flex justify-around flex-col md:flex-row gap-6 mb-8">
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
                            <label class="table-filter-card-field-name" for="name-filter">
                                <span>Search by Name</span>
                            </label>
                            <input
                                id="name-filter"
                                type="text"
                                placeholder="Search lists..."
                                class="table-filter-card-field-value-input"
                                bind:value={nameFilter} />
                        </div>

                        <div class="form-control md:col-span-2">
                            <label class="table-filter-card-field-name" for="completion-filter">
                                <span>Completion Status</span>
                            </label>
                            <select
                                id="completion-filter"
                                class="table-filter-card-field-value-select"
                                bind:value={completionFilter}>
                                <option value={null}>All</option>
                                <option value="complete">Complete (100%)</option>
                                <option value="in-progress">In Progress (1-99%)</option>
                                <option value="not-started">Not Started (0%)</option>
                            </select>
                        </div>

                        <div class="form-control md:col-span-2">
                            <label class="table-filter-card-field-name" for="expenses-filter">
                                <span class="config-card-field-name">Expense Items</span>
                            </label>
                            <select
                                id="expenses-filter"
                                class="table-filter-card-field-value-select"
                                bind:value={hasExpensesFilter}>
                                <option value={null}>All Lists</option>
                                <option value={true}>With Expenses</option>
                                <option value={false}>Without Expenses</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>

            <div class="flex flex-col gap-4 items-center">
                <Stats objects={listStats} />
                <Stats objects={completionStats} />
                <div class="flex flex-row gap-4">
                    <CreateObject href="/planning/guest_list/new" label="New List" />
                    <a href="/planning/list_entry" class="btn btn-accent gap-2">
                        <span class="icon-[lucide--list-todo] size-5"></span>
                        View All List Entries
                    </a>
                </div>
            </div>
        </div>
    </ProtectedPageHeader>

    <!-- Lists Cards Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {#each filteredLists as list (list.id)}
            <div class="list-card">
                <div class="list-card-body">
                    <h2 class="list-card-title">
                        <a href="/planning/list/{list.id}"
                            ><span class="icon-[lucide--list] size-5"></span>
                            {list.name}</a>
                    </h2>

                    {#if list.description}
                        <p class="text-sm line-clamp-2">{list.description}</p>
                    {/if}

                    <Stats
                        objects={[
                            {
                                title: "Total Items",
                                value: list.totalEntries,
                            },
                            {
                                title: `Completed (${list.completionPercentage}%)`,
                                value: list.completedEntries,
                            },
                            {
                                title: "Pending",
                                value: list.pendingEntries,
                            },
                        ]}
                        size="sm"
                        align="center" />

                    <!-- Progress Bar -->
                    <div class="mt-4">
                        <div class="flex justify-between items-center mb-2">
                            <span class="text-sm font-semibold">Progress</span>
                            <span class="text-sm">{list.completionPercentage}%</span>
                        </div>
                        <progress
                            class="progress {getCompletionClass(list.completionPercentage)} w-full"
                            value={list.completionPercentage}
                            max="100"></progress>
                    </div>

                    <!-- Action Buttons -->
                    <div class="card-actions justify-end mt-4">
                        <ViewDetails href="/planning/list/{list.id}" label="View Items" />
                    </div>
                </div>
            </div>
        {:else}
            <div class="col-span-full text-center py-12">
                <span class="icon-[lucide--inbox] size-16 text-base-content/30 mx-auto block mb-4"></span>
                <p class="text-lg text-base-content/70">No lists found</p>
                <p class="text-sm text-base-content/50">
                    {#if nameFilter}
                        Try adjusting your filters
                    {:else}
                        Create your first list to get started
                    {/if}
                </p>
            </div>
        {/each}
    </div>

    <!-- Create New List Button (Floating Action Button) -->
    <div class="fixed bottom-8 right-8">
        <a href="/planning/list/create" class="btn btn-primary btn-lg btn-circle shadow-xl">
            <span class="icon-[lucide--plus] size-6"></span>
        </a>
    </div>
</ProtectedPageShell>
