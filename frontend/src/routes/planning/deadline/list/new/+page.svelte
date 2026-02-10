<script lang="ts">
    import { enhance } from "$app/forms";
    import Icon from "$lib/components/Icon.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { ActionData } from "./$types";

    const { form }: { form: ActionData } = $props();
    const relativeCrumbs = [{ title: "Deadlines", href: "/planning/deadline" }, { title: "New List" }];
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader
        title="Create Deadline List"
        description="Create a new list to organize your wedding planning deadlines" />
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
                                <span>List Name</span>
                            </label>
                            <input
                                type="text"
                                id="name"
                                name="name"
                                class="edit-card-field-input"
                                placeholder="e.g., Vendor Tasks, Guest List To-Dos"
                                required
                                autofocus />
                            <span class="text-sm edit-card-field-name/70 mt-1">
                                Choose a descriptive name for your deadline list
                            </span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="flex gap-4 mt-6 justify-end">
                <a href="/planning/deadline" class="btn btn-error">Cancel</a>
                <button type="submit" class="btn btn-primary gap-2">
                    <Icon name="plus" class="size-5" />
                    Create List
                </button>
            </div>
        </form>
    </div>
</ProtectedPageShell>
