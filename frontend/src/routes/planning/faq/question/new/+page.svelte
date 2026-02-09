<script lang="ts">
    import { enhance, applyAction } from "$app/forms";
    import Icon from "$lib/components/Icon.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";

    const { data, form } = $props();

    let submitting = $state(false);

    const relativeCrumbs = [{ title: "FAQ", href: "/planning/faq" }, { title: "Add Question" }];
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader title="Add FAQ Question">
        <p class="text-base-content/70 mt-1">
            Create a new frequently asked question for your guests. Enter the icon's name from <a
                class="link link-primary underline"
                href="https://lucide.dev/icons/"
                target="_blank"
                rel="noopener noreferrer">Lucide Icons</a> in the format of "lucide--icon-name"
        </p>
    </ProtectedPageHeader>
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
            <!-- Question -->
            <div class="form-control w-full">
                <label class="edit-card-field-name" for="question">
                    <span>Question *</span>
                </label>
                <input
                    type="text"
                    name="question"
                    id="question"
                    class="edit-card-field-input"
                    placeholder="What time should we arrive?"
                    value={form?.question || ""}
                    required />
            </div>

            <!-- Answer -->
            <div class="form-control w-full">
                <label class="edit-card-field-name" for="answer">
                    <span>Answer *</span>
                </label>
                <textarea
                    name="answer"
                    id="answer"
                    class="edit-card-field-textarea"
                    rows="4"
                    placeholder="Please arrive at least 30 minutes before the ceremony begins..."
                    value={(form?.answer as string) || ""}
                    required></textarea>
            </div>

            <!-- Category & Icon -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="form-control w-full">
                    <label class="edit-card-field-name" for="categoryId">
                        <span>Category *</span>
                    </label>
                    <select name="categoryId" id="categoryId" class="select select-bordered w-full" required>
                        <option value="">Choose a category...</option>
                        {#each data.categories as cat, index (index)}
                            <option value={cat.categoryId} selected={form?.categoryId === cat.categoryId}>
                                {cat.categoryName}
                            </option>
                        {/each}
                    </select>
                    <span class="label">
                        <span class="edit-card-field-name">Questions are grouped by category on the FAQ page</span>
                    </span>
                </div>

                <div class="form-control w-full">
                    <label class="edit-card-field-name" for="icon">
                        <span>Icon *</span>
                    </label>
                    <input
                        type="text"
                        name="icon"
                        id="icon"
                        class="input input-bordered w-full"
                        placeholder="e.g., question-mark"
                        value={form?.icon || ""}
                        required />
                    <span class="label">
                        <span class="edit-card-field-name">Icon displayed next to the question</span>
                    </span>
                </div>
            </div>

            <!-- Order -->
            <div class="form-control w-full">
                <label class="edit-card-field-name" for="order">
                    <span>Question Order</span>
                </label>
                <input
                    type="number"
                    name="order"
                    id="order"
                    class="edit-card-field-input"
                    placeholder="0"
                    value={form?.order || "0"}
                    min="0" />
                <span class="label">
                    <span class="edit-card-field-name">Order within the category (0 = first)</span>
                </span>
            </div>
        </div>

        <div class="flex gap-4 mt-6 justify-end p-6 bg-base-200">
            <a href="/planning/faq" class="btn btn-error">Cancel</a>
            <button type="submit" class="btn btn-success" disabled={submitting}>
                {#if submitting}
                    <span class="loading loading-spinner"></span>
                    Creating...
                {:else}
                    <span class="icon-[lucide--check] size-5"></span>
                    Create Question
                {/if}
            </button>
        </div>
    </form>
</ProtectedPageShell>
