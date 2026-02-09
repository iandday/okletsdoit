<script lang="ts">
    import { enhance } from "$app/forms";
    import { invalidateAll } from "$app/navigation";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { ActionData, PageData } from "./$types";

    const { data, form }: { data: PageData; form: ActionData } = $props();

    const relativeCrumbs = [
        { title: "Inspirations", href: "/planning/inspiration" },
        { title: data.inspiration.name, href: `/planning/inspiration/${data.inspiration.id}` },
        { title: "Edit", href: `/planning/inspiration/${data.inspiration.id}/edit` },
    ];

    let imageInput: HTMLInputElement;
    let selectedImageFile: File | null = $state(null);
    let imagePreviewUrl: string | null = $state(null);

    function handleImageSelect(event: Event) {
        const input = event.target as HTMLInputElement;
        const file = input.files?.[0];

        if (file) {
            selectedImageFile = file;
            imagePreviewUrl = URL.createObjectURL(file);
        }
    }

    function clearImageSelection() {
        selectedImageFile = null;
        imagePreviewUrl = null;
        if (imageInput) {
            imageInput.value = "";
        }
    }
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader title="Edit Inspiration" description="Update inspiration details" showButtons={false} />

    <div class="flex flex-col gap-6">
        <!-- Main Details Form -->
        <div class="edit-card">
            <div class="edit-card-body">
                <form method="POST" action="?/saveAndReturn" use:enhance>
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
                                value={data.inspiration.name}
                                required />
                        </div>

                        <div class="form-control">
                            <label class="label" for="description">
                                <span class="edit-card-field-value">Description</span>
                            </label>
                            <textarea
                                id="description"
                                name="description"
                                class="textarea textarea-bordered h-32"
                                value={data.inspiration.description || ""}></textarea>
                        </div>

                        {#if form?.error}
                            <div class="alert alert-error">
                                <span class="icon-[lucide--alert-circle] size-5"></span>
                                <span>{form.error}</span>
                            </div>
                        {/if}

                        <div class="form-control mt-6">
                            <div class="flex gap-2">
                                <button type="submit" class="btn btn-success">
                                    <span class="icon-[lucide--save] size-5"></span>
                                    Save Changes
                                </button>
                                <a href="/planning/inspiration/{data.inspiration.id}" class="btn btn-error">Cancel</a>
                            </div>
                        </div>
                    </div>
                </form>
            </div>
        </div>

        <!-- Image Management -->
        <div class="edit-card">
            <div class="edit-card-body">
                <h3 class="text-lg font-semibold mb-4">Image Management</h3>

                <!-- Current Image -->
                {#if data.inspiration.image}
                    <div class="mb-6">
                        <div class="label">
                            <span class="edit-card-field-value">Current Image</span>
                        </div>
                        <div class="relative inline-block">
                            <img
                                src={data.inspiration.image}
                                alt={data.inspiration.name}
                                class="max-w-md rounded-lg shadow-lg" />
                            <form
                                method="POST"
                                action="?/deleteImage"
                                use:enhance={() => {
                                    return async ({ result }) => {
                                        if (result.type === "success") {
                                            await invalidateAll();
                                        }
                                    };
                                }}>
                                <button
                                    type="submit"
                                    class="absolute top-2 right-2 btn btn-error btn-sm"
                                    onclick={(e) => {
                                        if (!confirm("Are you sure you want to delete this image?")) {
                                            e.preventDefault();
                                        }
                                    }}>
                                    <span class="icon-[lucide--trash-2] size-4"></span>
                                    Delete Image
                                </button>
                            </form>
                        </div>
                    </div>
                {/if}

                <!-- Upload New Image -->
                <div class="space-y-4">
                    <div class="label">
                        <span class="edit-card-field-value">
                            {data.inspiration.image ? "Replace Image" : "Upload Image"}
                        </span>
                    </div>

                    {#if imagePreviewUrl}
                        <div class="mb-4">
                            <div class="text-sm text-base-content/70 mb-2">Preview:</div>
                            <img src={imagePreviewUrl} alt="Preview" class="max-w-md rounded-lg shadow-lg" />
                        </div>
                    {/if}

                    <form
                        method="POST"
                        action="?/uploadImage"
                        enctype="multipart/form-data"
                        use:enhance={() => {
                            return async ({ result }) => {
                                if (result.type === "success") {
                                    clearImageSelection();
                                    await invalidateAll();
                                }
                            };
                        }}>
                        <div class="flex flex-col gap-4">
                            <input
                                type="file"
                                bind:this={imageInput}
                                name="image"
                                accept="image/*"
                                onchange={handleImageSelect}
                                class="edit-card-file-input w-full max-w-md" />

                            {#if selectedImageFile}
                                <div class="flex gap-2">
                                    <button type="submit" class="btn btn-primary">
                                        <span class="icon-[lucide--upload] size-5"></span>
                                        Upload Image
                                    </button>
                                    <button type="button" onclick={clearImageSelection} class="btn btn-ghost">
                                        <span class="icon-[lucide--x] size-5"></span>
                                        Clear
                                    </button>
                                </div>
                            {/if}
                        </div>
                    </form>

                    {#if form?.imageUploaded}
                        <div class="alert alert-success">
                            <span class="icon-[lucide--check-circle] size-5"></span>
                            <span>Image uploaded successfully!</span>
                        </div>
                    {/if}

                    {#if form?.imageDeleted}
                        <div class="alert alert-success">
                            <span class="icon-[lucide--check-circle] size-5"></span>
                            <span>Image deleted successfully!</span>
                        </div>
                    {/if}
                </div>
            </div>
        </div>
    </div>
</ProtectedPageShell>
