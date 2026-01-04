<script lang="ts">
    import { enhance, applyAction } from "$app/forms";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";

    const { data, form } = $props();

    let submitting = $state(false);

    const relativeCrumbs = [{ title: "FAQ", href: "/settings/faq" }, { title: "Edit Tip" }];
</script>

<ProtectedPageShell {relativeCrumbs}>
    <div class="container mx-auto p-4 max-w-4xl">
        <div class="flex justify-between items-center mb-6">
            <div>
                <h1 class="text-3xl font-bold">Edit Helpful Tip</h1>
                <p class="text-base-content/70 mt-1">Update this helpful tip</p>
            </div>
            <a href="/settings/faq" class="btn btn-ghost">
                <span class="icon-[lucide--x] size-5"></span>
                Cancel
            </a>
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

        <form
            method="POST"
            use:enhance={() => {
                submitting = true;
                return async ({ result }) => {
                    if (result.type === "redirect") {
                        await applyAction(result);
                    } else {
                        await applyAction(result);
                        submitting = false;
                    }
                };
            }}
            class="edit-card">
            <div class="config-card-body space-y-6">
                <!-- Content -->
                <div class="form-control w-full">
                    <label class="edit-card-field-name" for="content">
                        <span>Tip Content *</span>
                    </label>
                    <textarea
                        name="content"
                        id="content"
                        class="edit-card-field-textarea"
                        rows="3"
                        placeholder="Don't forget to RSVP by the deadline to help us plan accordingly!"
                        value={(form?.content as string) || data.tip.content}
                        required></textarea>
                    <span class="label">
                        <span class="label-text-alt">Keep tips concise and actionable</span>
                    </span>
                </div>

                <!-- Category -->
                <div class="form-control w-full">
                    <label class="edit-card-field-name" for="categoryId">
                        <span>Category *</span>
                    </label>
                    <select name="categoryId" id="categoryId" class="select select-bordered w-full" required>
                        <option value="">Choose a category...</option>
                        {#each data.categories as cat, index (index)}
                            <option
                                value={cat.categoryId}
                                selected={(form?.categoryId || data.tip.category) === cat.categoryName}>
                                {cat.categoryName}
                            </option>
                        {/each}
                    </select>
                    <span class="label">
                        <span class="label-text-alt"
                            >Tips are displayed in a "Helpful Tips" section within each category</span>
                    </span>
                </div>

                <!-- Order -->
                <div class="form-control w-full">
                    <label class="edit-card-field-name" for="order">
                        <span>Tip Order</span>
                    </label>
                    <input
                        type="number"
                        name="order"
                        id="order"
                        class="edit-card-field-input"
                        placeholder="0"
                        value={form?.order || data.tip.order || 0}
                        min="0" />
                    <span class="label">
                        <span class="label-text-alt">Order within the category (0 = first)</span>
                    </span>
                </div>
            </div>

            <div class="flex gap-4 mt-6 justify-end p-6 bg-base-200">
                <a href="/settings/faq" class="btn btn-ghost">Cancel</a>
                <button type="submit" class="btn btn-primary" disabled={submitting}>
                    {#if submitting}
                        <span class="loading loading-spinner"></span>
                        Updating...
                    {:else}
                        <span class="icon-[lucide--check] size-5"></span>
                        Update Tip
                    {/if}
                </button>
            </div>
        </form>
    </div>
</ProtectedPageShell>
