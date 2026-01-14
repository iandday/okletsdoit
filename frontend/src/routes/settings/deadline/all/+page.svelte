<script lang="ts">
    import Icon from "$lib/components/Icon.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();

    const relativeCrumbs = [
        { title: "Deadlines", href: "/settings/deadline" },
        { title: "All Deadlines", href: "/settings/deadline/deadline/all" },
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
                    <a href="/settings/deadline/deadline/all" class="btn btn-ghost gap-2">
                        <Icon name="x" class="size-5" />
                        Clear Filter
                    </a>
                {/if}
                <a href="/settings/deadline" class="btn btn-primary gap-2">
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
                <a href="/settings/deadline" class="btn btn-primary gap-2">
                    <Icon name="arrow-left" class="size-5" />
                    Go to Deadline Lists
                </a>
            </div>
        </div>
    {:else}
        <!-- Deadlines List -->
        <div class="space-y-4">
            {#each data.deadlines.items as deadline (deadline.id)}
                <div class="list-card">
                    <div class="list-card-body">
                        <div class="flex items-start justify-between gap-4">
                            <div class="flex-1">
                                <div class="flex items-center gap-3 mb-2">
                                    <h3 class="text-lg font-semibold">
                                        <a href="/settings/deadline/deadline/{deadline.id}" class="link link-hover">
                                            {deadline.name}
                                        </a>
                                    </h3>
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
                                </div>

                                {#if deadline.description}
                                    <p class="mb-3">{deadline.description}</p>
                                {/if}

                                <div class="flex flex-wrap gap-4 text-sm">
                                    {#if deadline.deadlineListName}
                                        <div class="flex items-center gap-2">
                                            <span class="icon-[lucide--list] size-4"></span>
                                            <a
                                                href="/settings/deadline/list/{deadline.deadlineListId}"
                                                class="link link-accent">
                                                {deadline.deadlineListName}
                                            </a>
                                        </div>
                                    {/if}

                                    <div class="flex items-center gap-2">
                                        <span class="icon-[lucide--calendar] size-4"></span>
                                        <span>{formatDate(deadline.dueDate)}</span>
                                    </div>

                                    {#if deadline.assignedToName}
                                        <div class="flex items-center gap-2">
                                            <span class="icon-[lucide--user] size-4"></span>
                                            <span>{deadline.assignedToName}</span>
                                        </div>
                                    {/if}

                                    {#if deadline.completed && deadline.completedAt}
                                        <div class="flex items-center gap-2">
                                            <span class="icon-[lucide--check-circle] size-4"></span>
                                            <span>Completed {formatDate(deadline.completedAt)}</span>
                                        </div>
                                    {/if}
                                </div>
                            </div>

                            <a
                                href="/settings/deadline/deadline/{deadline.id}/edit"
                                class="btn btn-sm btn-ghost gap-2"
                                aria-label="Edit Deadline">
                                <span class="icon-[lucide--pencil] size-4"></span>
                            </a>
                        </div>
                    </div>
                </div>
            {/each}
        </div>

        <!-- Pagination Controls -->
        {#if data.deadlines.count > data.pageSize}
            {@const totalPages = Math.ceil(data.deadlines.count / data.pageSize)}
            {@const hasPrevious = data.currentPage > 1}
            {@const hasNext = data.currentPage < totalPages}
            {@const baseUrl = data.filterListId
                ? `/settings/deadline/all?list=${data.filterListId}`
                : "/settings/deadline/all"}

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
