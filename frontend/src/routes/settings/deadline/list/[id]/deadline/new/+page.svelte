<script lang="ts">
    import { enhance } from "$app/forms";
    import Icon from "$lib/components/Icon.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { ActionData, PageData } from "./$types";

    const { data, form }: { data: PageData; form: ActionData } = $props();
    const relativeCrubms = [
        { title: "Deadline Lists", href: "/settings/deadline/list" },
        { title: data.listName, href: `/settings/deadline/list/${data.listId}` },
        { title: "New Deadline" },
    ];
</script>

<ProtectedPageShell relativeCrumbs={relativeCrubms}>
    <div class="container mx-auto p-4 max-w-6xl">
        <div class="flex justify-between items-center mb-6">
            <h1 class="text-3xl font-bold">Add Deadline</h1>
            <a href="/settings/deadline/list/{data.listId}" class="btn btn-error">Cancel</a>
        </div>

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
                                placeholder="e.g., Book venue, Send invitations"
                                required
                                autofocus />
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="description">
                                <span>Description</span>
                            </label>
                            <textarea
                                id="description"
                                name="description"
                                class="edit-card-field-textarea"
                                rows="3"
                                placeholder="Add any additional details..."></textarea>
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="dueDate">
                                <span>Due Date</span>
                            </label>
                            <input type="date" id="dueDate" name="dueDate" class="edit-card-field-date" />
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="completed">
                                <span>Mark as completed</span>
                            </label>
                            <input type="checkbox" name="completed" id="completed" class="edit-card-field-toggle" />
                        </div>
                    </div>
                </div>
            </div>

            <div class="flex gap-4 mt-6 justify-end">
                <a href="/settings/deadline/list/{data.listId}" class="btn btn-error">Cancel</a>
                <button type="submit" class="btn btn-primary gap-2">
                    <Icon name="plus" class="size-5" />
                    Add Deadline
                </button>
            </div>
        </form>
    </div>
</ProtectedPageShell>
