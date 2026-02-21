<script lang="ts">
    import ExportData from "$lib/components/buttons/ExportData.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import { createTable, Subscribe, Render } from "svelte-headless-table";
    import { addSortBy, addTableFilter, addPagination } from "svelte-headless-table/plugins";
    import { writable } from "svelte/store";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();
    const relativeCrumbs = [{ title: "Guest List", href: "/planning/guest_list" }, { title: "All Guests" }];

    type Guest = (typeof data.guests)[0];

    const guestData = writable<Guest[]>(data.guests);
    let filterValue = $state("");

    $effect(() => {
        guestData.set(data.guests);
    });

    const table = createTable(guestData, {
        sort: addSortBy(),
        filter: addTableFilter({
            fn: ({ filterValue, value }) => {
                if (!filterValue) return true;
                const searchTerm = filterValue.toLowerCase();
                return String(value).toLowerCase().includes(searchTerm);
            },
        }),
        page: addPagination({
            initialPageSize: 25,
        }),
    });

    const columns = table.createColumns([
        table.column({
            accessor: "firstName",
            header: "First Name",
        }),
        table.column({
            accessor: "lastName",
            header: "Last Name",
        }),
        table.column({
            accessor: "guestGroupName",
            header: "Guest Group",
        }),
        table.column({
            accessor: "guestGroupRelationship",
            header: "Relationship",
        }),
        table.column({
            accessor: "guestGroupPriorityDisplay",
            header: "Priority",
        }),
        table.column({
            accessor: "isInvited",
            header: "Invited",
            cell: ({ value }) => (value ? "Yes" : "No"),
        }),
        table.column({
            accessor: "responded",
            header: "Responded",
            cell: ({ value }) => (value ? "Yes" : "No"),
        }),
        table.column({
            accessor: (row) => row,
            header: "Attending",
            id: "attending",
            cell: ({ value }) => {
                if (!value.responded) return "-";
                return value.isAttending ? "Yes" : "No";
            },
        }),
        table.column({
            accessor: "acceptVip",
            header: "VIP",
            cell: ({ value }) => (value ? "Yes" : "No"),
        }),
        table.column({
            accessor: "acceptAccommodation",
            header: "Accommodation",
            cell: ({ value }) => (value ? "Yes" : "No"),
        }),
        table.column({
            accessor: (row) => row,
            header: "Actions",
            id: "actions",
        }),
    ]);

    const { headerRows, pageRows, tableAttrs, tableBodyAttrs, pluginStates } = table.createViewModel(columns);

    const { filterValue: filterStore } = pluginStates.filter;
    const { pageIndex, pageSize, pageCount, hasNextPage, hasPreviousPage } = pluginStates.page;

    $effect(() => {
        filterStore.set(filterValue);
    });
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader
        title="All Guests"
        description="View and manage all individual guests.  Clicking on any column header will sort the table.">
        <ExportData resourceType="guest" label="Export CSV" format="csv" fileName="guests.csv" />
        <ExportData resourceType="guest" label="Export Excel" format="xlsx" fileName="guests.xlsx" />
    </ProtectedPageHeader>

    <table {...$tableAttrs} class="associated-table">
        <thead class="associated-table-header">
            {#each $headerRows as headerRow, headerRowIndex (headerRowIndex)}
                <Subscribe rowAttrs={headerRow.attrs()}>
                    <tr>
                        {#each headerRow.cells as cell (cell.id)}
                            <Subscribe attrs={cell.attrs()} let:attrs props={cell.props()} let:props>
                                <th {...attrs} class:cursor-pointer={props.sort.disabled === false}>
                                    {#if props.sort.disabled === false}
                                        <button class="flex items-center gap-2" onclick={props.sort.toggle}>
                                            <Render of={cell.render()} />
                                            {#if props.sort.order === "asc"}
                                                <span class="icon-[lucide--arrow-up] size-4"></span>
                                            {:else if props.sort.order === "desc"}
                                                <span class="icon-[lucide--arrow-down] size-4"></span>
                                            {/if}
                                        </button>
                                    {:else}
                                        <Render of={cell.render()} />
                                    {/if}
                                </th>
                            </Subscribe>
                        {/each}
                    </tr>
                </Subscribe>
            {/each}
        </thead>
        <tbody {...$tableBodyAttrs}>
            {#each $pageRows as row (row.id)}
                <Subscribe rowAttrs={row.attrs()}>
                    <tr class="hover">
                        {#each row.cells as cell (cell.id)}
                            <Subscribe attrs={cell.attrs()}>
                                <td>
                                    {#if cell.column.id === "actions"}
                                        {@const guest = row.original}
                                        <a href="/planning/guest/{guest.id}" class="btn btn-secondary btn-sm">
                                            <span class="icon-[lucide--eye] size-4"></span>
                                            View
                                        </a>
                                    {:else}
                                        <Render of={cell.render()} />
                                    {/if}
                                </td>
                            </Subscribe>
                        {/each}
                    </tr>
                </Subscribe>
            {/each}
        </tbody>
    </table>

    {#if $pageRows.length === 0}
        <div class="alert alert-info mt-4">
            <span class="icon-[lucide--info] size-6"></span>
            <div>
                <h3 class="font-bold">No guests found</h3>
                <div class="text-sm">
                    {filterValue ? "Try adjusting your search." : "No guests have been added yet."}
                </div>
            </div>
        </div>
    {/if}

    <!-- Pagination Controls -->
    <div class="flex items-center justify-between mt-6 gap-4 flex-wrap">
        <div class="text-sm text-base-content">
            Showing {$pageRows.length} of {data.guests.length} guests
            {#if $pageCount > 1}
                (Page {$pageIndex + 1} of {$pageCount})
            {/if}
        </div>

        <div class="flex items-center gap-4">
            <!-- Page Size Selector -->
            <div class="flex items-center gap-2">
                <label for="page-size" class="text-sm">Rows per page:</label>
                <select
                    id="page-size"
                    class="associated-table-pg-size-select"
                    value={$pageSize}
                    onchange={(e) => pageSize.set(Number(e.currentTarget.value))}>
                    <option value={10}>10</option>
                    <option value={25}>25</option>
                    <option value={50}>50</option>
                    <option value={100}>100</option>
                </select>
            </div>

            <!-- Page Navigation -->
            <div class="join">
                <button
                    class="associated-table-nav-btn"
                    disabled={!$hasPreviousPage}
                    onclick={() => pageIndex.update((i) => i - 1)}>
                    <span class="icon-[lucide--chevron-left] size-4"></span>
                    Previous
                </button>
                <button
                    class="associated-table-nav-btn"
                    disabled={!$hasNextPage}
                    onclick={() => pageIndex.update((i) => i + 1)}>
                    Next
                    <span class="icon-[lucide--chevron-right] size-4"></span>
                </button>
            </div>
        </div>
    </div>
</ProtectedPageShell>
