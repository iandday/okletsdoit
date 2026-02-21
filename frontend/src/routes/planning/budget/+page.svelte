<script lang="ts">
    import Stats from "$lib/components/Stats.svelte";
    import CreateObject from "$lib/components/buttons/CreateObject.svelte";
    import ViewDetails from "$lib/components/buttons/ViewDetails.svelte";
    import PieChart from "$lib/components/charts/PieChart.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import { formatCurrency } from "$lib/utils/formatters";
    import { createTable, Subscribe, Render, createRender } from "svelte-headless-table";
    import { addSortBy } from "svelte-headless-table/plugins";
    import { readable } from "svelte/store";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();

    const relativeCrumbs = [{ title: "Budget", href: "/planning/budget" }];

    const table = createTable(readable(data.categoryBreakdown), {
        sort: addSortBy(),
    });

    const columns = table.createColumns([
        table.column({
            accessor: "category",
            header: "Category",
        }),
        table.column({
            accessor: "totalEstimated",
            header: "Estimated",
            cell: ({ value }) => formatCurrency(value),
        }),
        table.column({
            accessor: "totalActual",
            header: "Actual",
            cell: ({ value }) => formatCurrency(value),
        }),
        table.column({
            accessor: "variance",
            header: "Variance",
            cell: ({ value }) => formatCurrency(value),
        }),
    ]);

    const { headerRows, pageRows, tableAttrs, tableBodyAttrs } = table.createViewModel(columns);

    // Prepare data for pie charts
    const chartLabels = data.categoryBreakdown.map((item) => item.category.name);
    const estimatedData = data.categoryBreakdown.map((item) => item.totalEstimated);
    const actualData = data.categoryBreakdown.map((item) => item.totalActual);
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader
        title="Budget Overview"
        description="Manage your wedding budget, track expenses by category"
        showButtons={false} />

    <!-- Summary Stats -->
    <div class="mb-8">
        <Stats
            class="pb-4"
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
                    value: formatCurrency(data.totalVariance),
                    icon: data.totalVariance >= 0 ? "lucide--trending-up" : "lucide--trending-down",
                },
            ]}
            size="sm" />

        <div class="join pb-6">
            <CreateObject href="/planning/budget/expense/new" label="Create New Expense" />
            <ViewDetails href="/planning/budget/expense/all" label="View All Expenses" />
            <div class="dropdown">
                <div tabindex="0" role="button" class="btn btn-secondary text-secondary-content">
                    <span class="icon-[lucide--settings] size-4"></span>Manage Categories
                </div>
                <ul
                    tabindex="0"
                    class="dropdown-content menu bg-secondary text-secondary-content rounded-box z-[1] w-52 p-2 shadow">
                    {#each data.categoryBreakdown as item, index (item.category.id)}
                        <li><a href="/planning/budget/category/{item.category.id}">{item.category.name}</a></li>
                    {/each}
                </ul>
            </div>
        </div>

        <div class="bg-base-100 border border-base-300 shadow-lg overflow-hidden">
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
                                                class:text-right={cell.id !== "category"}
                                                on:click={props.sort.toggle}>
                                                <div
                                                    class="flex items-center gap-1"
                                                    class:justify-end={cell.id !== "category"}>
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
                                            <td
                                                {...attrs}
                                                class="px-3 py-2 whitespace-nowrap text-sm"
                                                class:text-right={cell.id !== "category"}>
                                                {#if cell.id === "category"}
                                                    {@const category = row.original.category}
                                                    <a
                                                        href={category.id === "uncategorized"
                                                            ? "/planning/budget/expense/all"
                                                            : `/planning/budget/category/${category.id}`}
                                                        class="link link-accent font-semibold hover:underline">
                                                        {category.name}
                                                    </a>
                                                    <div class="text-xs text-secondary-content mt-1">
                                                        {row.original.expenseCount}
                                                        {row.original.expenseCount === 1 ? "expense" : "expenses"}
                                                    </div>
                                                {:else if cell.id === "totalActual"}
                                                    <span class="font-semibold text-secondary-content">
                                                        <Render of={cell.render()} />
                                                    </span>
                                                {:else if cell.id === "variance"}
                                                    <span
                                                        class="font-bold"
                                                        class:text-error={row.original.variance >= 0}
                                                        class:text-success={row.original.variance < 0}>
                                                        <Render of={cell.render()} />
                                                    </span>
                                                {:else}
                                                    <span class="text-secondary-content"
                                                        ><Render of={cell.render()} /></span>
                                                {/if}
                                            </td>
                                        </Subscribe>
                                    {/each}
                                </tr>
                            </Subscribe>
                        {/each}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Pie Charts -->
    <div class="grid gap-6 md:grid-cols-2 mt-8">
        <div class="detail-card items-center">
            <div class="detail-card-title pt-4">{formatCurrency(data.totalEstimated)} Estimated</div>
            <div class="detail-card-body">
                <PieChart labels={chartLabels} data={estimatedData} size="sm" labelColor="text-secondary-content" />
            </div>
        </div>

        <div class="detail-card items-center">
            <div class="detail-card-title pt-4">{formatCurrency(data.totalActual)} Spent</div>
            <div class="detail-card-body">
                <PieChart labels={chartLabels} data={actualData} size="sm" labelColor="text-secondary-content" />
            </div>
        </div>
    </div></ProtectedPageShell>
