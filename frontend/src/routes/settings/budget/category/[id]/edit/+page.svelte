<script lang="ts">
    import ObjectEditForm from "$lib/components/object/ObjectEditForm.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();

    const relativeCrumbs = [
        { title: "Budget", href: "/settings/budget" },
        { title: data.category.name, href: `/settings/budget/category/${data.category.id}` },
        { title: "Edit", href: `/settings/budget/category/${data.category.id}/edit` },
    ];
</script>

<ObjectEditForm
    {relativeCrumbs}
    title="Edit Category"
    backLink={`/settings/budget/category/${data.category.id}`}
    object={data.category}>
    <div class="form-control">
        <label class="label" for="name">
            <span class="label-text">Name</span>
        </label>
        <input type="text" id="name" name="name" class="input input-bordered" value={data.category.name} required />
    </div>

    <div class="form-control">
        <label class="label" for="description">
            <span class="label-text">Description</span>
        </label>
        <textarea
            id="description"
            name="description"
            class="textarea textarea-bordered h-24"
            value={data.category.description || ""}></textarea>
    </div>
</ObjectEditForm>
