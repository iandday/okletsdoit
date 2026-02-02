<script lang="ts">
    import { enhance } from "$app/forms";
    import Icon from "$lib/components/Icon.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import { idText } from "typescript";
    import type { ActionData, PageData } from "./$types";

    const { form, data }: { form: ActionData; data: PageData } = $props();

    const relativeCrumbs = [
        { title: "Budget", href: "/settings/budget" },
        { title: "New Expense", href: "/settings/budget/expense/new" },
    ];
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader title="New Expense" description="Add a new expense to your budget" />
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
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="form-control w-full md:col-span-2">
                            <label class="edit-card-field-name" for="item">
                                <span>Item</span>
                            </label>
                            <input
                                type="text"
                                id="item"
                                name="item"
                                class="edit-card-field-input"
                                placeholder="Expense item name"
                                required
                                autofocus />
                        </div>

                        <div class="form-control w-full md:col-span-2">
                            <label class="edit-card-field-name" for="description">
                                <span>Description</span>
                            </label>
                            <textarea
                                id="description"
                                name="description"
                                class="edit-card-field-textarea"
                                rows="3"
                                placeholder="Optional description..."></textarea>
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="category">
                                <span>Category</span>
                            </label>
                            <select id="category" name="category" class="edit-card-field-input">
                                <option value="">-- Select Category --</option>
                                {#each data.categories as category, index (category.id)}
                                    <option value={category.id} selected={data.preselectedCategoryId === category.id}>
                                        {category.name}
                                    </option>
                                {/each}
                            </select>
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="vendor">
                                <span>Vendor</span>
                            </label>
                            <select id="vendor" name="vendor" class="edit-card-field-input">
                                <option value="">-- Select Vendor --</option>
                                {#each data.vendors as vendor, index (vendor.id)}
                                    <option value={vendor.id}>
                                        {vendor.name || vendor.company}
                                    </option>
                                {/each}
                            </select>
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="date">
                                <span>Date</span>
                            </label>
                            <input type="date" id="date" name="date" class="edit-card-field-input" />
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="quantity">
                                <span>Quantity</span>
                            </label>
                            <input
                                type="number"
                                id="quantity"
                                name="quantity"
                                class="edit-card-field-input"
                                step="1"
                                min="1"
                                placeholder="1" />
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="unitPrice">
                                <span>Unit Price</span>
                            </label>
                            <input
                                type="number"
                                id="unitPrice"
                                name="unitPrice"
                                class="edit-card-field-input"
                                step="0.01"
                                placeholder="0.00" />
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="additionalPrice">
                                <span>Additional Price</span>
                            </label>
                            <input
                                type="number"
                                id="additionalPrice"
                                name="additionalPrice"
                                class="edit-card-field-input"
                                step="0.01"
                                placeholder="0.00" />
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="estimatedAmount">
                                <span>Estimated Amount</span>
                            </label>
                            <input
                                type="number"
                                id="estimatedAmount"
                                name="estimatedAmount"
                                class="edit-card-field-input"
                                step="0.01"
                                placeholder="0.00" />
                        </div>

                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="actualAmount">
                                <span>Actual Amount</span>
                            </label>
                            <input
                                type="number"
                                id="actualAmount"
                                name="actualAmount"
                                class="edit-card-field-input"
                                step="0.01"
                                placeholder="0.00" />
                        </div>

                        <div class="form-control w-full md:col-span-2">
                            <label class="edit-card-field-name" for="url">
                                <span>URL</span>
                            </label>
                            <input
                                type="url"
                                id="url"
                                name="url"
                                class="edit-card-field-input"
                                placeholder="https://example.com/product" />
                        </div>
                    </div>
                </div>
            </div>

            <div class="flex gap-4 mt-6 justify-end">
                <a href="/settings/budget" class="btn btn-error">Cancel</a>
                <button type="submit" class="btn btn-primary gap-2">
                    <Icon name="plus" class="size-5" />
                    Create Expense
                </button>
            </div>
        </form>
    </div>
</ProtectedPageShell>
