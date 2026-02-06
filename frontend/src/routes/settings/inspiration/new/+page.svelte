<script lang="ts">
    import { enhance } from "$app/forms";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { ActionData } from "./$types";

    const { form }: { form: ActionData } = $props();

    const relativeCrumbs = [{ title: "Inspiration", href: "/settings/inspiration" }, { title: "New" }];

    let imageInput: HTMLInputElement;
    let imagePreviewUrl = $state<string | null>(null);
    let selectedFile = $state<File | null>(null);

    function handleImageSelect(event: Event) {
        const target = event.target as HTMLInputElement;
        const file = target.files?.[0];
        if (file) {
            selectedFile = file;
            imagePreviewUrl = URL.createObjectURL(file);
        }
    }

    function clearImage() {
        selectedFile = null;
        imagePreviewUrl = null;
        if (imageInput) {
            imageInput.value = "";
        }
    }
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader
        title="Create Inspiration"
        description="Add a new inspiration to your board"
        showButtons={false} />

    <div class="max-w-2xl">
        {#if form?.error}
            <div role="alert" class="alert alert-error mb-6">
                <span class="icon-[lucide--alert-circle] size-5"></span>
                <span>{form.error}</span>
            </div>
        {/if}
        <div class="edit-card">
            <div class="edit-card-body">
                <form method="POST" enctype="multipart/form-data" use:enhance class="flex flex-col gap-2">
                    <h2 class="edit-card-title">Inspiration Details</h2>

                    <div class="form-control">
                        <label class="edit-card-field-name" for="name">
                            <span>Name</span>
                        </label>
                        <input
                            id="name"
                            name="name"
                            type="text"
                            placeholder="Enter inspiration name"
                            class="edit-card-field-input"
                            required />
                    </div>

                    <div class="form-control">
                        <label class="edit-card-field-name" for="description">
                            <span>Description (Optional)</span>
                        </label>
                        <textarea
                            id="description"
                            name="description"
                            class="edit-card-field-textarea"
                            placeholder="Enter a description..."></textarea>
                    </div>

                    <div class="form-control">
                        <label class="edit-card-field-name" for="image">
                            <span>Image</span>
                        </label>
                        <input
                            id="image"
                            name="image"
                            type="file"
                            accept="image/*"
                            class="edit-card-file-input"
                            bind:this={imageInput}
                            onchange={handleImageSelect} />
                        {#if imagePreviewUrl}
                            <div class="mt-4 relative">
                                <img src={imagePreviewUrl} alt="Preview" class="max-h-64 rounded-lg shadow-lg" />
                                <button
                                    type="button"
                                    onclick={clearImage}
                                    class="btn btn-sm btn-circle btn-error absolute top-2 right-2">
                                    <span class="icon-[lucide--x] size-4"></span>
                                </button>
                            </div>
                        {/if}
                    </div>

                    <div class="card-actions justify-end mt-6">
                        <a href="/settings/inspiration" class="btn btn-error">Cancel</a>
                        <button type="submit" class="btn btn-success">
                            <span class="icon-[lucide--plus] size-5"></span>
                            Create Inspiration
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</ProtectedPageShell>
