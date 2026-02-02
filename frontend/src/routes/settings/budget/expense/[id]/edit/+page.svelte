<script lang="ts">
    import ObjectEditForm from "$lib/components/object/ObjectEditForm.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();

    const relativeCrumbs = [
        { title: "Budget", href: "/settings/budget" },
        { title: data.expense.item, href: `/settings/budget/expense/${data.expense.id}` },
        { title: "Edit", href: `/settings/budget/expense/${data.expense.id}/edit` },
    ];
</script>

<ObjectEditForm
    {relativeCrumbs}
    title="Edit Expense"
    backLink={`/settings/budget/expense/${data.expense.id}`}
    object={data.expense}>
    <div class="form-control">
        <label class="label" for="item">
            <span class="label-text">Item</span>
        </label>
        <input type="text" id="item" name="item" class="input input-bordered" value={data.expense.item} required />
    </div>

    <div class="form-control">
        <label class="label" for="description">
            <span class="label-text">Description</span>
        </label>
        <textarea
            id="description"
            name="description"
            class="textarea textarea-bordered h-24"
            value={data.expense.description || ""}></textarea>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="form-control">
            <label class="label" for="category">
                <span class="label-text">Category</span>
            </label>
            <select id="category" name="category" class="select select-bordered">
                <option value="">-- Select Category --</option>
                {#each data.categories as category}
                    <option value={category.id} selected={data.expense.categoryId === category.id}>
                        {category.name}
                    </option>
                {/each}
            </select>
        </div>

        <div class="form-control">
            <label class="label" for="vendor">
                <span class="label-text">Vendor</span>
            </label>
            <select id="vendor" name="vendor" class="select select-bordered">
                <option value="">-- Select Vendor --</option>
                {#each data.vendors as vendor}
                    <option value={vendor.id} selected={data.expense.vendorId === vendor.id}>
                        {vendor.name}
                    </option>
                {/each}
            </select>
        </div>

        <div class="form-control">
            <label class="label" for="date">
                <span class="label-text">Date</span>
            </label>
            <input type="date" id="date" name="date" class="input input-bordered" value={data.expense.date || ""} />
        </div>

        <div class="form-control">
            <label class="label" for="estimatedAmount">
                <span class="label-text">Estimated Amount</span>
            </label>
            <input
                type="number"
                id="estimatedAmount"
                name="estimatedAmount"
                class="input input-bordered"
                step="0.01"
                value={data.expense.estimatedAmount || ""} />
        </div>

        <div class="form-control">
            <label class="label" for="actualAmount">
                <span class="label-text">Actual Amount</span>
            </label>
            <input
                type="number"
                id="actualAmount"
                name="actualAmount"
                class="input input-bordered"
                step="0.01"
                value={data.expense.actualAmount || ""} />
        </div>
    </div>
</ObjectEditForm>
