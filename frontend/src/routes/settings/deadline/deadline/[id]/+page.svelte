<script lang="ts">
    import Icon from "$lib/components/Icon.svelte";
    import ObjectDetail from "$lib/components/object/ObjectDetail.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();

    const relativeCrumbs = [
        { title: "Deadlines", href: "/settings/deadline" },
        ...(data.deadline.deadlineListId && data.deadline.deadlineListName
            ? [
                  {
                      title: data.deadline.deadlineListName,
                      href: `/settings/deadline/list/${data.deadline.deadlineListId}`,
                  },
              ]
            : []),
        { title: data.deadline.name, href: `/settings/deadline/deadline/${data.deadline.id}` },
    ];

    const status = data.deadline.completed;
    const statusText = data.deadline.completed
        ? `Completed ${data.deadline.completedAt ? new Date(data.deadline.completedAt).toLocaleDateString() : ""}`
        : data.deadline.overdue
          ? "Overdue"
          : "Pending";

    const formatDate = (date: Date | null | undefined): string => {
        if (!date) return "Not set";
        return new Date(date).toLocaleDateString("en-US", {
            year: "numeric",
            month: "long",
            day: "numeric",
        });
    };
</script>

<ObjectDetail
    {relativeCrumbs}
    title={data.deadline.name}
    {status}
    {statusText}
    editLink={`/settings/deadline/deadline/${data.deadline.id}/edit`}
    object={data.deadline}>
    {#snippet mainSnippet()}
        <div class="space-y-4">
            {#if data.deadline.description}
                <div>
                    <div class="detail-card-field-name">Description</div>
                    <div class="detail-card-field-value">{data.deadline.description}</div>
                </div>
            {/if}

            <div class="grid grid-cols-2 gap-4">
                <div>
                    <div class="detail-card-field-name">Due Date</div>
                    <div class="detail-card-field-value flex items-center gap-2">
                        {formatDate(data.deadline.dueDate)}
                        {#if data.deadline.overdue && !data.deadline.completed}
                            <span class="badge badge-error badge-sm">Overdue</span>
                        {/if}
                    </div>
                </div>

                <div>
                    <div class="detail-card-field-name">Status</div>
                    <div class="detail-card-field-value">
                        {#if data.deadline.completed}
                            <span class="badge badge-success gap-2">
                                <Icon name="check-circle" class="size-4" />
                                Completed
                            </span>
                        {:else}
                            <span class="badge badge-warning gap-2">
                                <Icon name="clock" class="size-4" />
                                Pending
                            </span>
                        {/if}
                    </div>
                </div>
            </div>

            {#if data.deadline.assignedToName}
                <div>
                    <div class="detail-card-field-name">Assigned To</div>
                    <div class="detail-card-field-value flex items-center gap-2">
                        <Icon name="user" class="size-4 text-base-content/50" />
                        {data.deadline.assignedToName}
                    </div>
                </div>
            {/if}

            {#if data.deadline.completed && data.deadline.completedNote}
                <div>
                    <div class="detail-card-field-name">Completion Note</div>
                    <div class="detail-card-field-value">{data.deadline.completedNote}</div>
                </div>
            {/if}
        </div>
    {/snippet}

    {#snippet mainActionsSnippet()}
        <a href="/settings/deadline/deadline/{data.deadline.id}/edit" class="btn btn-sm btn-outline btn-primary gap-2">
            <Icon name="pencil" class="size-4" />
            Edit
        </a>
    {/snippet}
</ObjectDetail>
