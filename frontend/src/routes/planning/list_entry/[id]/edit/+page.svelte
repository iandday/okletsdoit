<script lang="ts">
    import { enhance } from "$app/forms";
    import { invalidateAll } from "$app/navigation";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { ActionData, PageData } from "./$types";

    const { data, form }: { data: PageData; form: ActionData } = $props();

    const relativeCrumbs = [
        { title: "Lists", href: "/planning/list" },
        { title: data.list.name, href: `/planning/list/${data.list.id}` },
        { title: data.entry.item, href: `/planning/list_entry/${data.entry.id}` },
        { title: "Edit", href: `/planning/list_entry/${data.entry.id}/edit` },
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
    <ProtectedPageHeader
        title="Edit List Item"
        description="Update the details of this list item"
        showButtons={false} />
    <div class="flex flex-col gap-6">
        <div class="edit-card">
            <div class="edit-card-body">
                <form method="POST" action="?/saveAndReturn" use:enhance>
                    <div class="grid grid-cols-1 gap-4">
                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="item">
                                <span>Item Name</span>
                            </label>
                            <input
                                type="text"
                                id="item"
                                name="item"
                                class="edit-card-field-input"
                                value={data.entry.item}
                                required
                                autofocus />
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="description">
                                <span>Description</span>
                            </label>
                            <textarea id="description" name="description" class="edit-card-field-textarea" rows="3"
                                >{data.entry.description || ""}</textarea>
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="url">
                                <span>Product URL</span>
                            </label>
                            <input
                                type="url"
                                id="url"
                                name="url"
                                class="edit-card-field-input"
                                value={data.entry.url || ""} />
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="quantity">
                                    <span>Quantity</span>
                                </label>
                                <input
                                    type="number"
                                    id="quantity"
                                    name="quantity"
                                    class="edit-card-field-input"
                                    min="1"
                                    step="1"
                                    value={data.entry.quantity} />
                            </div>

                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="unitPrice">
                                    <span>Unit Price ($)</span>
                                </label>
                                <input
                                    type="number"
                                    id="unitPrice"
                                    name="unitPrice"
                                    class="edit-card-field-input"
                                    min="0"
                                    step="0.01"
                                    value={data.entry.unitPrice} />
                            </div>

                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="additionalPrice">
                                    <span>Additional Price ($)</span>
                                </label>
                                <input
                                    type="number"
                                    id="additionalPrice"
                                    name="additionalPrice"
                                    class="edit-card-field-input"
                                    min="0"
                                    step="0.01"
                                    value={data.entry.additionalPrice} />
                                <span class="text-sm text-base-content/70 mt-1"
                                    >One-time cost regardless of quantity</span>
                            </div>
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="vendorId">
                                <span>Vendor</span>
                            </label>
                            <select id="vendorId" name="vendorId" class="edit-card-field-select">
                                <option value="">No vendor selected</option>
                                {#each data.vendors as vendor, index (vendor.id)}
                                    <option value={vendor.id} selected={vendor.id === data.entry.vendorId}>
                                        {vendor.name || vendor.company || "Unnamed Contact"}
                                    </option>
                                {/each}
                            </select>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div class="form-control">
                                <label class="cursor-pointer label">
                                    <span class="edit-card-field-name">Mark as Completed</span>
                                    <input
                                        type="checkbox"
                                        name="isCompleted"
                                        class="edit-card-field-toggle"
                                        checked={data.entry.isCompleted} />
                                </label>
                            </div>

                            <div class="form-control">
                                <label class="cursor-pointer label">
                                    <span class="edit-card-field-name">Mark as Purchased</span>
                                    <input
                                        type="checkbox"
                                        name="purchased"
                                        class="edit-card-field-toggle"
                                        checked={data.entry.purchased} />
                                </label>
                            </div>
                        </div>
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
                    <div class="form-control mt-6">
                        <div class="flex gap-2">
                            <button type="submit" class="btn btn-primary gap-2">
                                <span class="icon-[lucide--save] size-5"></span>
                                Save Changes
                            </button>
                            <a href="/planning/list_entry/{data.entry.id}" class="btn btn-error">Cancel</a>
                        </div>
                    </div>
                </form>
            </div>
        </div>

        <div class="edit-card">
            <div class="edit-card-body">
                <h3 class="text-lg font-semibold mb-4">Image Management</h3>

                <!-- Current Image -->
                {#if data.entry.image}
                    <div class="mb-6">
                        <div class="label">
                            <span class="edit-card-field-value">Current Image</span>
                        </div>
                        <div class="relative inline-block">
                            <img src={data.entry.image} alt={data.entry.item} class="max-w-md rounded-lg shadow-lg" />
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
                            {data.entry.image ? "Replace Image" : "Upload Image"}
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
