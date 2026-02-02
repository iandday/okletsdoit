<script lang="ts">
    import { enhance } from "$app/forms";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { ActionData, PageData } from "./$types";

    const { data, form }: { data: PageData; form: ActionData } = $props();

    const relativeCrumbs = [
        { title: "Lists", href: "/settings/list" },
        { title: data.list.name, href: `/settings/list/${data.list.id}` },
        { title: data.entry.item, href: `/settings/list_entry/${data.entry.id}` },
        { title: "Edit", href: `/settings/list_entry/${data.entry.id}/edit` },
    ];
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader title="Edit List Item" description="Update the details of this list item" />
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
                </div>
            </div>

            <div class="flex gap-4 mt-6 justify-end">
                <a href="/settings/list_entry/{data.entry.id}" class="btn btn-error">Cancel</a>
                <button type="submit" class="btn btn-primary gap-2">
                    <span class="icon-[lucide--save] size-5"></span>
                    Save Changes
                </button>
            </div>
        </form>
    </div>
</ProtectedPageShell>
