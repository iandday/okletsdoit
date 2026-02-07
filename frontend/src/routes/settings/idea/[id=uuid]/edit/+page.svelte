<script lang="ts">
    import { enhance } from "$app/forms";
    import RichTextEditor from "$lib/components/editor/RichTextEditor.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { ActionData, PageData } from "./$types";

    const { data, form }: { data: PageData; form: ActionData } = $props();
    let description = $state(data.idea.description || "");

    const relativeCrumbs = [
        { title: "Ideas", href: "/settings/idea" },
        {
            title: data.idea.name,
            href: `/settings/idea/${data.idea.id}`,
        },
        { title: "Edit", href: `/settings/idea/${data.idea.id}/edit` },
    ];
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader title="Edit Idea" description="Update the details of your idea" />
    <div class="container mx-auto p-4 max-w-4xl">
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
                                <span>Name</span>
                                <span class="text-error">*</span>
                            </label>
                            <input
                                type="text"
                                id="name"
                                name="name"
                                class="edit-card-field-input"
                                value={data.idea.name || ""}
                                required
                                autofocus />
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="description">
                                <span>Description</span>
                            </label>
                            <RichTextEditor
                                bind:value={description}
                                name="description"
                                placeholder="Describe your idea..." />
                        </div>
                    </div>

                    <div class="flex justify-end gap-2 mt-6">
                        <a href="/settings/idea/{data.idea.id}" class="btn btn-error">Cancel</a>
                        <button type="submit" class="btn btn-success">
                            <span class="icon-[lucide--save] size-5"></span>
                            Save Changes
                        </button>
                    </div>
                </div>
            </div>
        </form>
    </div>
</ProtectedPageShell>
