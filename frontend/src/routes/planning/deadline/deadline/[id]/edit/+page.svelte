<script lang="ts">
    import { enhance } from "$app/forms";
    import Icon from "$lib/components/Icon.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { ActionData, PageData } from "./$types";

    const { data, form }: { data: PageData; form: ActionData } = $props();

    // Format date for input field (YYYY-MM-DD)
    const formatDateForInput = (date: Date | null | undefined): string => {
        if (!date) return "";
        const d = new Date(date);
        return d.toISOString().split("T")[0];
    };

    const backUrl = data.deadline.deadlineListId
        ? `/settings/deadline/list/${data.deadline.deadlineListId}`
        : "/settings/deadline";

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
        { title: "Edit", href: `/settings/deadline/deadline/${data.deadline.id}/edit` },
    ];
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader title="Edit Deadline" description="Update the details of your deadline" />
    <div class="container mx-auto p-4 max-w-6xl">
        {#if form?.error}
            <div class="alert alert-error mb-4">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="stroke-current shrink-0 h-6 w-6"
                    fill="none"
                    viewBox="0 0 24 24">
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>{form.error}</span>
            </div>
        {/if}

        <form method="POST" use:enhance>
            <div class="config-card">
                <div class="config-card-body">
                    <div class="grid grid-cols-1 gap-4">
                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="name">
                                <span>Deadline Name</span>
                            </label>
                            <input
                                type="text"
                                id="name"
                                name="name"
                                class="edit-card-field-input"
                                value={data.deadline.name}
                                required
                                autofocus />
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="description">
                                <span>Description</span>
                            </label>
                            <textarea id="description" name="description" class="edit-card-field-textarea" rows="3"
                                >{data.deadline.description || ""}</textarea>
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="dueDate">
                                <span>Due Date</span>
                            </label>
                            <input
                                type="date"
                                id="dueDate"
                                name="dueDate"
                                class="edit-card-field-date"
                                value={formatDateForInput(data.deadline.dueDate)} />
                            {#if data.deadline.overdue && !data.deadline.completed}
                                <span class="text-sm text-error mt-1">This deadline is overdue</span>
                            {/if}
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="completed">
                                <span>Mark as completed</span>
                            </label>
                            <input
                                type="checkbox"
                                name="completed"
                                id="completed"
                                class="edit-card-field-toggle"
                                checked={data.deadline.completed} />
                            {#if data.deadline.completedAt}
                                <span class="text-sm text-base-content/70 mt-1">
                                    Completed on {new Date(data.deadline.completedAt).toLocaleDateString()}
                                </span>
                            {/if}
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="completedNote">
                                <span>Completion Note</span>
                            </label>
                            <textarea
                                id="completedNote"
                                name="completedNote"
                                class="edit-card-field-textarea"
                                rows="2"
                                placeholder="Add any notes about completing this deadline..."
                                >{data.deadline.completedNote || ""}</textarea>
                        </div>
                    </div>
                </div>
            </div>

            <div class="flex gap-4 mt-6 justify-end">
                <a href={backUrl} class="btn btn-error">Cancel</a>
                <button type="submit" class="btn btn-primary gap-2">
                    <Icon name="save" class="size-5" />
                    Save Changes
                </button>
            </div>
        </form>
    </div>
</ProtectedPageShell>
