<script lang="ts">
    import Icon from "$lib/components/Icon.svelte";
    import CreateObject from "$lib/components/buttons/CreateObject.svelte";
    import ObjectChildItems from "$lib/components/object/ObjectChildItems.svelte";
    import ObjectDetail from "$lib/components/object/ObjectDetail.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();

    const relativeCrumbs = [
        { title: "Deadlines", href: "/planning/deadline" },
        { title: data.deadlineList.name, href: `/planning/deadline/list/${data.deadlineList.id}` },
    ];

    const status = data.deadlineList.completionPercentage > 0.0;
    const statusText = `${data.deadlineList.completionPercentage}% Complete`;
    const childCreateLink = `/planning/deadline/list/${data.deadlineList.id}/deadline/new`;
    const childCreateLabel = "Add Deadline";
</script>

<ObjectDetail
    {relativeCrumbs}
    title={data.deadlineList.name}
    {status}
    {statusText}
    object={data.deadlineList}
    {childCreateLink}
    {childCreateLabel}
    editLink={`/planning/deadline/list/${data.deadlineList.id}/edit`}>
    {#snippet mainSnippet()}
        <div class="flex flex-row justify-between">
            <div>
                <div class="detail-card-field-name">Total</div>
                <div class="detail-card-field-value">{data.deadlineList.count}</div>
            </div>
            <div>
                <div class="detail-card-field-name">Completed</div>
                <div class="detail-card-field-value">{data.deadlineList.completedCount}</div>
            </div>
            <div>
                <div class="detail-card-field-name">Pending</div>
                <div class="detail-card-field-value">{data.deadlineList.pendingCount}</div>
            </div>
        </div>
    {/snippet}
    {#snippet mainActionsSnippet()}
        <CreateObject href={`/planning/deadline/list/${data.deadlineList.id}/deadline/new`} label="Add Deadline" />
    {/snippet}
    {#snippet extraCardsSnippet()}
        <ObjectChildItems title={"Deadlines"}>
            {#if data.deadlines.length === 0}
                <div class="card bg-base-100 border border-base-300 shadow-lg">
                    <div class="card-body items-center text-center py-16">
                        <Icon name="calendar-check" class="size-16 text-base-content/30 mb-4" />
                        <h3 class="text-xl font-semibold text-base-content mb-2">No deadlines yet</h3>
                        <p class="text-base-content/70 mb-6 max-w-md">
                            Add deadlines to this list to help you stay on track with your wedding planning tasks.
                        </p>
                        <a
                            href="/planning/deadline/list/{data.deadlineList.id}/deadline/new"
                            class="btn btn-primary gap-2">
                            <Icon name="plus" class="size-5" />
                            Add First Deadline
                        </a>
                    </div>
                </div>
            {:else}
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mt-4">
                    {#each data.deadlines as deadline (deadline.id)}
                        <div class="list-card">
                            <div class="list-card-body">
                                <div class="list-card-title">
                                    <a href="/planning/deadline/deadline/{deadline.id}">
                                        {deadline.name}
                                    </a>
                                </div>
                                {#if deadline.description}
                                    <div class="mb-2 text-sm">{deadline.description}</div>
                                {/if}
                                <div class="mb-2 text-sm flex flex-row justify-start gap-4">
                                    {#if deadline.dueDate}
                                        <span>Due: {new Date(deadline.dueDate).toLocaleDateString()}</span>
                                    {:else}
                                        <span>No due date set</span>
                                    {/if}
                                    {#if deadline.assignedToName}
                                        <span>Assigned to: {deadline.assignedToName}</span>
                                    {:else}
                                        <span>Unassigned</span>
                                    {/if}
                                </div>
                                <div class="flex flex-row gap-2">
                                    {#if deadline.completed}
                                        <div class="badge badge-success">Completed</div>
                                    {:else}
                                        <div class="badge badge-accent">Pending</div>
                                    {/if}
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>
            {/if}
        </ObjectChildItems>
    {/snippet}
</ObjectDetail>
