<script lang="ts">
    import { enhance } from "$app/forms";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();

    const relativeCrumbs = [
        { title: "Budget", href: "/planning/budget" },
        { title: data.category.name, href: `/planning/budget/category/${data.category.id}` },
        { title: "Edit", href: `/planning/budget/category/${data.category.id}/edit` },
    ];
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader title="Edit Category" description="Update category details" showButtons={false} />

    <div class="edit-card">
        <div class="edit-card-body">
            <form method="POST" use:enhance>
                <div class="space-y-4">
                    <div class="form-control">
                        <label class="label" for="name">
                            <span class="edit-card-field-value">Name</span>
                        </label>
                        <input
                            type="text"
                            id="name"
                            name="name"
                            class="input input-bordered"
                            value={data.category.name}
                            required />
                    </div>

                    <div class="form-control">
                        <label class="label" for="description">
                            <span class="edit-card-field-value">Description</span>
                        </label>
                        <textarea
                            id="description"
                            name="description"
                            class="textarea textarea-bordered h-24"
                            value={data.category.description || ""}></textarea>
                    </div>

                    <div class="form-control mt-6">
                        <div class="flex gap-2">
                            <button type="submit" class="btn btn-success">
                                <span class="icon-[lucide--save] size-5"></span>
                                Save Changes
                            </button>
                            <a href="/planning/budget/category/{data.category.id}" class="btn btn-error">Cancel</a>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </div>
</ProtectedPageShell>
