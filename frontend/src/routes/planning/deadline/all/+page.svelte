<script lang="ts">
    import Icon from "$lib/components/Icon.svelte";
    import DeleteObject from "$lib/components/buttons/DeleteObject.svelte";
    import ViewDetails from "$lib/components/buttons/ViewDetails.svelte";
    import ViewDetailsButton from "$lib/components/buttons/ViewDetails.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();

    const relativeCrumbs = [
        { title: "Deadlines", href: "/planning/deadline" },
        { title: "All Deadlines", href: "/planning/deadline/deadline/all" },
    ];

    const formatDate = (date: Date | null | undefined): string => {
        if (!date) return "No date set";
        return new Date(date).toLocaleDateString("en-US", {
            year: "numeric",
            month: "short",
            day: "numeric",
        });
    };
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader
        title="All Deadlines"
        description={data.filterListId
            ? "Showing deadlines from selected list"
            : "View and manage all your wedding planning deadlines"}>
        <!-- Header -->
        <div class="flex items-center justify-between mb-8">
            <div class="flex gap-2">
                {#if data.filterListId}
                    <a href="/planning/deadline/deadline/all" class="btn btn-ghost gap-2">
                        <Icon name="x" class="size-5" />
                        Clear Filter
                    </a>
                {/if}
                <a href="/planning/deadline" class="btn btn-primary gap-2">
                    <Icon name="arrow-left" class="size-5" />
                    Back to Lists
                </a>
            </div>
        </div>
    </ProtectedPageHeader>
    {#if data.deadlines.items.length === 0}
        <!-- Empty State -->
        <div class="card bg-base-100 border border-base-300 shadow-lg">
            <div class="card-body items-center text-center py-16">
                <Icon name="calendar-check" class="size-16 text-base-content/30 mb-4" />
                <h3 class="text-xl font-semibold text-base-content mb-2">No deadlines found</h3>
                <p class="text-base-content/70 mb-6 max-w-md">
                    {#if data.filterListId}
                        This list doesn't have any deadlines yet. Add some to get started!
                    {:else}
                        You haven't created any deadlines yet. Start by creating a deadline list.
                    {/if}
                </p>
                <a href="/planning/deadline" class="btn btn-primary gap-2">
                    <Icon name="arrow-left" class="size-5" />
                    Go to Deadline Lists
                </a>
            </div>
        </div>
    {:else}
        <!-- Deadlines Table -->
        <div class="card bg-base-100 border border-base-300 shadow-lg w-full">
            <div class="overflow-x-auto w-full">
                <table class="table bg-base-300 text-primary-content w-full">
                    <thead class="text-accent">
                        <tr>
                            <th>Deadline</th>
                            <th>Description</th>
                            <th>List</th>
                            <th>Due Date</th>
                            <th>Assignee</th>
                            <th>Status</th>
                            <th class="text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {#each data.deadlines.items as deadline (deadline.id)}
                            <tr class="hover">
                                <td>
                                    <a class="link link-accent" href="/planning/deadline/deadline/{deadline.id}">
                                        {deadline.name}
                                    </a>
                                </td>
                                <td>
                                    <div class="max-w-xs truncate">
                                        {deadline.description || "—"}
                                    </div>
                                </td>
                                <td>
                                    {#if deadline.deadlineListName}
                                        <a
                                            href="/planning/deadline/list/{deadline.deadlineListId}"
                                            class="link link-accent">
                                            {deadline.deadlineListName}
                                        </a>
                                    {:else}
                                        —
                                    {/if}
                                </td>
                                <td>
                                    <div class="flex items-center gap-2">
                                        {formatDate(deadline.dueDate)}
                                    </div>
                                </td>
                                <td>
                                    {#if deadline.assignedToName}
                                        <div class="flex items-center gap-2">
                                            {deadline.assignedToName.split(" ")[0]}
                                        </div>
                                    {:else}
                                        —
                                    {/if}
                                </td>
                                <td>
                                    {#if deadline.completed}
                                        <span class="badge badge-success gap-2">
                                            <span class="icon-[lucide--check-circle] size-4"></span>
                                            Completed
                                        </span>
                                    {:else if deadline.overdue}
                                        <span class="badge badge-error gap-2">
                                            <span class="icon-[lucide--alert-circle] size-4"></span>
                                            Overdue
                                        </span>
                                    {:else}
                                        <span class="badge badge-warning gap-2">
                                            <span class="icon-[lucide--clock] size-4"></span>
                                            Pending
                                        </span>
                                    {/if}
                                </td>
                                <td>
                                    <div class="flex items-center justify-end gap-1">
                                        <ViewDetailsButton href="/planning/deadline/deadline/{deadline.id}" />

                                        <a
                                            href="/planning/deadline/deadline/{deadline.id}/edit"
                                            class="btn btn-sm bg-base-100 text-primary-content gap-2"
                                            aria-label="Edit Deadline">
                                            <span class="icon-[lucide--pencil] size-4"></span>
                                        </a>
                                        <DeleteObject
                                            action="?/deleteDeadline"
                                            href="#"
                                            value={deadline.id}
                                            confirmMessage="Are you sure you want to remove this deadline?" />
                                    </div>
                                </td>
                            </tr>
                        {/each}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Pagination Controls -->
        {#if data.deadlines.count > data.pageSize}
            {@const totalPages = Math.ceil(data.deadlines.count / data.pageSize)}
            {@const hasPrevious = data.currentPage > 1}
            {@const hasNext = data.currentPage < totalPages}
            {@const baseUrl = data.filterListId
                ? `/planning/deadline/all?list=${data.filterListId}`
                : "/planning/deadline/all"}

            <div class="flex items-center justify-between mt-8">
                <div class="text-sm text-base-content/70">
                    Showing {(data.currentPage - 1) * data.pageSize + 1} - {Math.min(
                        data.currentPage * data.pageSize,
                        data.deadlines.count,
                    )} of {data.deadlines.count} deadlines
                </div>

                <div class="join">
                    <a
                        href={hasPrevious
                            ? `${baseUrl}?page=${data.currentPage - 1}&pageSize=${data.pageSize}`
                            : undefined}
                        class="join-item btn btn-accent btn-sm"
                        class:btn-disabled={!hasPrevious}
                        aria-label="Previous Page">
                        <span class="icon-[lucide--chevron-left] size-4"></span>
                        Previous
                    </a>

                    <button class="join-item btn btn-accent btn-sm btn-active">
                        Page {data.currentPage} of {totalPages}
                    </button>

                    <a
                        href={hasNext ? `${baseUrl}?page=${data.currentPage + 1}&pageSize=${data.pageSize}` : undefined}
                        class="join-item btn btn-accent btn-sm"
                        class:btn-disabled={!hasNext}
                        aria-label="Next Page">
                        Next
                        <span class="icon-[lucide--chevron-right] size-4"></span>
                    </a>
                </div>
            </div>
        {/if}
    {/if}
</ProtectedPageShell>
