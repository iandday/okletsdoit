<script lang="ts">
    import DeleteObject from "$lib/components/buttons/DeleteObject.svelte";
    import EditObject from "$lib/components/buttons/EditObject.svelte";
    import ViewDetails from "$lib/components/buttons/ViewDetails.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import { createTable, Subscribe, Render } from "svelte-headless-table";
    import { addPagination, addSortBy } from "svelte-headless-table/plugins";
    import { writable } from "svelte/store";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();

    const relativeCrumbs = [
        { title: "Deadlines", href: "/planning/deadline" },
        { title: "All Deadlines", href: "/planning/deadline/deadline/all" },
    ];

    let filterForm: HTMLFormElement | undefined;
    let searchDebounceTimer: ReturnType<typeof setTimeout> | undefined;
    const getRowOriginal = (row: any): (typeof data.deadlines)[number] => row.original;

    const deadlineData = writable(data.deadlines);
    $effect(() => {
        deadlineData.set(data.deadlines);
    });

    const formatDate = (date: Date | null | undefined): string => {
        if (!date) return "No date set";
        return new Date(date).toLocaleDateString("en-US", {
            year: "numeric",
            month: "short",
            day: "numeric",
        });
    };

    const getDeadlineStatus = (deadline: (typeof data.deadlines)[number]) => {
        if (deadline.completed) return "Completed";
        if (deadline.overdue) return "Overdue";
        return "Pending";
    };

    const submitFilters = () => {
        filterForm?.requestSubmit();
    };

    const handleFilterChange = () => {
        if (searchDebounceTimer) {
            clearTimeout(searchDebounceTimer);
        }
        submitFilters();
    };

    const handleSearchInput = () => {
        if (searchDebounceTimer) {
            clearTimeout(searchDebounceTimer);
        }
        searchDebounceTimer = setTimeout(() => {
            submitFilters();
        }, 300);
    };

    const table = createTable(deadlineData, {
        sort: addSortBy(),
        page: addPagination({ initialPageSize: 25 }),
    });

    const columns = table.createColumns([
        table.column({
            accessor: "name",
            header: "Deadline",
        }),
        table.column({
            accessor: "deadlineListName",
            header: "List",
        }),
        table.column({
            accessor: "dueDate",
            header: "Due Date",
        }),
        table.column({
            accessor: "assignedToName",
            header: "Assignee",
        }),
        table.column({
            accessor: (row) => getDeadlineStatus(row),
            header: "Status",
            id: "status",
        }),
    ]);

    const { headerRows, pageRows, tableAttrs, tableBodyAttrs, pluginStates } = table.createViewModel(columns);
    const { hasNextPage, hasPreviousPage, pageIndex, pageSize } = pluginStates.page;
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader
        title="All Deadlines"
        description="Use the filters to find specific deadlines or check on upcoming tasks.  Clicking on a column's header will sort the deadlines accordingly.">
        <div class="w-full flex justify-between items-start flex-col md:flex-row gap-6 mb-8">
            <form
                method="GET"
                action="/planning/deadline/all"
                class="table-filter-card w-full md:w-[40rem]"
                id="filter-panel"
                bind:this={filterForm}>
                <div class="table-filter-card-body">
                    <div class="table-filter-card-title">
                        Filters
                        <a href="/planning/deadline/all" class="btn btn-error btn-sm">
                            <span class="icon-[lucide--x] size-4"></span>
                            Clear
                        </a>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="form-control md:col-span-2">
                            <label class="table-filter-card-field-name" for="deadline-search-filter">
                                <span>Search Deadlines</span>
                            </label>
                            <div class="relative">
                                <input
                                    id="deadline-search-filter"
                                    name="search"
                                    type="text"
                                    placeholder="Search deadlines..."
                                    class="table-filter-card-field-value-input pl-10"
                                    value={data.filterSearch || ""}
                                    oninput={handleSearchInput} />
                            </div>
                        </div>

                        <div class="form-control">
                            <label class="table-filter-card-field-name" for="deadline-list-filter">
                                <span>List</span>
                            </label>
                            <select
                                id="deadline-list-filter"
                                name="list"
                                class="table-filter-card-field-value-select"
                                value={data.filterListId || ""}
                                onchange={handleFilterChange}>
                                <option value="">All lists</option>
                                {#each data.deadlineLists as list (list.id)}
                                    <option value={list.id}>{list.name}</option>
                                {/each}
                            </select>
                        </div>

                        <div class="form-control">
                            <label class="table-filter-card-field-name" for="deadline-assignee-filter">
                                <span>Assignee</span>
                            </label>
                            <select
                                id="deadline-assignee-filter"
                                name="assignee"
                                class="table-filter-card-field-value-select"
                                value={data.filterAssigneeId || ""}
                                onchange={handleFilterChange}>
                                <option value="">All assignees</option>
                                {#each data.assigneeOptions as assignee (assignee.id)}
                                    <option value={assignee.id}>{assignee.name}</option>
                                {/each}
                            </select>
                        </div>

                        <div class="form-control md:col-span-2">
                            <label class="table-filter-card-field-name" for="deadline-status-filter">
                                <span>Status</span>
                            </label>
                            <select
                                id="deadline-status-filter"
                                name="status"
                                class="table-filter-card-field-value-select"
                                value={data.filterStatus || "all"}
                                onchange={handleFilterChange}>
                                <option value="all">All statuses</option>
                                <option value="pending">Pending</option>
                                <option value="overdue">Overdue</option>
                                <option value="completed">Completed</option>
                            </select>
                        </div>
                    </div>
                </div>
            </form>

            <div class="flex gap-2">
                <a href="/planning/deadline" class="btn btn-primary gap-2">
                    <span class="icon-[lucide--arrow-left] size-5"></span>
                    Back to Lists
                </a>
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
                        {@const deadline = getRowOriginal(row)}
                        <Subscribe rowAttrs={row.attrs()} let:rowAttrs>
                            <tr {...rowAttrs} class="hover:bg-base-200 transition-colors">
                                {#each row.cells as cell (cell.id)}
                                    <Subscribe attrs={cell.attrs()} let:attrs>
                                        <td {...attrs} class="px-3 py-2 whitespace-nowrap text-sm">
                                            {#if cell.id === "name"}
                                                <div class="flex flex-col">
                                                    <a
                                                        class="link link-accent hover:underline font-semibold"
                                                        href="/planning/deadline/deadline/{deadline.id}">
                                                        {deadline.name}
                                                    </a>
                                                    {#if deadline.description}
                                                        <span class="text-xs text-secondary-content/70 line-clamp-1">
                                                            {deadline.description}
                                                        </span>
                                                    {/if}
                                                </div>
                                            {:else if cell.id === "deadlineListName"}
                                                {#if deadline.deadlineListName && deadline.deadlineListId}
                                                    <a
                                                        href="/planning/deadline/list/{deadline.deadlineListId}"
                                                        class="link link-accent hover:underline">
                                                        {deadline.deadlineListName}
                                                    </a>
                                                {:else}
                                                    <span class="text-secondary-content/30">-</span>
                                                {/if}
                                            {:else if cell.id === "dueDate"}
                                                <span class="text-secondary-content">
                                                    {formatDate(deadline.dueDate)}
                                                </span>
                                            {:else if cell.id === "assignedToName"}
                                                <span class="text-secondary-content">
                                                    {deadline.assignedToName || "-"}
                                                </span>
                                            {:else if cell.id === "status"}
                                                {#if getDeadlineStatus(deadline) === "Completed"}
                                                    <span class="badge badge-success">Completed</span>
                                                {:else if getDeadlineStatus(deadline) === "Overdue"}
                                                    <span class="badge badge-error">Overdue</span>
                                                {:else}
                                                    <span class="badge badge-warning">Pending</span>
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
                                        <ViewDetails href="/planning/deadline/deadline/{deadline.id}" size="sm" />
                                        <EditObject href="/planning/deadline/deadline/{deadline.id}/edit" size="sm" />
                                        <DeleteObject
                                            action="?/deleteDeadline"
                                            href="#"
                                            label="Remove"
                                            value={deadline.id}
                                            confirmMessage="Are you sure you want to remove this deadline?" />
                                    </div>
                                </td>
                            </tr>
                        </Subscribe>
                    {:else}
                        <tr>
                            <td colspan="6" class="text-center py-8">
                                <span class="icon-[lucide--inbox] size-12 text-secondary-content/30 mx-auto block mb-2"
                                ></span>
                                <p class="text-secondary-content/70">No deadlines found</p>
                                <p class="text-sm text-secondary-content/50">
                                    {#if data.filterListId || data.filterAssigneeId || data.filterStatus !== "all" || data.filterSearch}
                                        Try adjusting your filters
                                    {:else}
                                        No deadlines available
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
                    <option value={data.deadlines.length}>All</option>
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
