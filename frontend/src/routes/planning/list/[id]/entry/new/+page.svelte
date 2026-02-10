<script lang="ts">
    import { enhance } from "$app/forms";
    import Icon from "$lib/components/Icon.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { ActionData, PageData } from "./$types";

    const { data, form }: { data: PageData; form: ActionData } = $props();

    const relativeCrumbs = [
        { title: "Lists", href: "/planning/list" },
        { title: data.list.name, href: `/planning/list/${data.list.id}` },
        { title: "New Item" },
    ];
</script>

<ProtectedPageShell {relativeCrumbs}>
    <div class="container mx-auto p-4 max-w-6xl">
        <div class="flex justify-between items-center mb-6">
            <h1 class="text-3xl font-bold">Add Item to {data.list.name}</h1>
            <a href="/planning/list/{data.list.id}" class="btn btn-error">Cancel</a>
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
                            <label class="edit-card-field-name" for="item">
                                <span>Item Name</span>
                            </label>
                            <input
                                type="text"
                                id="item"
                                name="item"
                                class="edit-card-field-input"
                                placeholder="e.g., Party decorations, Catering service"
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
                            <label class="edit-card-field-name" for="url">
                                <span>Product URL</span>
                            </label>
                            <input
                                type="url"
                                id="url"
                                name="url"
                                class="edit-card-field-input"
                                placeholder="https://example.com/product" />
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
                                    value="1" />
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
                                    value="0.00" />
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
                                    value="0.00" />
                                <span class="text-sm edit-card-field-name mt-1"
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
                                    <option value={vendor.id}>
                                        {vendor.name || vendor.company || "Unnamed Contact"}
                                    </option>
                                {/each}
                            </select>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div class="form-control">
                                <label class="cursor-pointer label">
                                    <span class="edit-card-field-name">Mark as Completed</span>
                                    <input type="checkbox" name="isCompleted" class="edit-card-field-toggle" />
                                </label>
                            </div>

                            <div class="form-control">
                                <label class="cursor-pointer label">
                                    <span class="edit-card-field-name">Mark as Purchased</span>
                                    <input type="checkbox" name="purchased" class="edit-card-field-toggle" />
                                </label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="flex gap-4 mt-6 justify-end">
                <a href="/planning/list/{data.list.id}" class="btn btn-error">Cancel</a>
                <button type="submit" class="btn btn-primary gap-2">
                    <Icon name="plus" class="size-5" />
                    Add Item
                </button>
            </div>
        </form>
    </div>
</ProtectedPageShell>
