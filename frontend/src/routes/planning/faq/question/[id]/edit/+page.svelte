<script lang="ts">
    import { enhance, applyAction } from "$app/forms";
    import { invalidateAll } from "$app/navigation";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { QuestionURLSchema } from "../../../api-client";

    const { data, form } = $props();

    let submitting = $state(false);
    let newUrl = $state({ url: "", text: "" });
    let editingUrlId = $state<string | null>(null);
    let editingUrl = $state({ url: "", text: "" });

    function startEdit(url: QuestionURLSchema) {
        editingUrlId = url.id;
        editingUrl = { url: url.url, text: url.text || "" };
    }

    function cancelEdit() {
        editingUrlId = null;
        editingUrl = { url: "", text: "" };
    }

    const relativeCrumbs = [{ title: "FAQ" }, { title: "Edit Question" }];
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader title="Edit FAQ Question" description="Update this frequently asked question" />

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

    {#if form?.urlError}
        <div class="alert alert-error mb-4">
            <span class="icon-[lucide--alert-circle] size-5"></span>
            <span>{form.urlError}</span>
        </div>
    {/if}

    <form
        method="POST"
        action="?/updateQuestion"
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
        <div class="edit-card-body space-y-6">
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
                    value={form?.question || data.question.question}
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
                    value={(form?.answer as string) || data.question.answer}
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
                            <option
                                value={cat.categoryId}
                                selected={(form?.categoryId || data.question.category) === cat.categoryName}>
                                {cat.categoryName}
                            </option>
                        {/each}
                    </select>
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
                        value={form?.icon || data.question.icon}
                        required />
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
                    value={form?.order || data.question.order || 0}
                    min="0" />
            </div>
        </div>

        <div class="flex gap-4 mt-6 justify-end p-6 bg-base-200">
            <a href="/planning/faq" class="btn btn-error">Cancel</a>
            <button type="submit" class="btn btn-success" disabled={submitting}>
                {#if submitting}
                    <span class="loading loading-spinner"></span>
                    Updating...
                {:else}
                    <span class="icon-[lucide--check] size-5"></span>
                    Update Question
                {/if}
            </button>
        </div>
    </form>

    <!-- URLs Section (separate from main form) -->
    <div class="edit-card mt-6">
        <div class="edit-card-body space-y-6">
            <div class="divider divider-start">Related URLs</div>

            <!-- Existing URLs -->
            {#if data.question.urls && data.question.urls.length > 0}
                <div class="space-y-3">
                    {#each data.question.urls as url, index (index)}
                        <div class="card card-border bg-base-100">
                            <div class="card-body p-4">
                                {#if editingUrlId === url.id}
                                    <!-- Edit Mode -->
                                    <form
                                        method="POST"
                                        action="?/updateUrl"
                                        use:enhance={() => {
                                            return async ({ result }) => {
                                                await applyAction(result);
                                                if (result.type === "success") {
                                                    editingUrlId = null;
                                                    editingUrl = { url: "", text: "" };
                                                    await invalidateAll();
                                                }
                                            };
                                        }}>
                                        <input type="hidden" name="urlId" value={url.id} />
                                        <div class="space-y-3">
                                            <div class="form-control">
                                                <label class="label" for="edit-url-{url.id}">
                                                    <span class="edit-card-field-name">URL *</span>
                                                </label>
                                                <input
                                                    type="url"
                                                    id="edit-url-{url.id}"
                                                    name="url"
                                                    class="edit-card-field-input"
                                                    value={editingUrl.url}
                                                    oninput={(e) => (editingUrl.url = e.currentTarget.value)}
                                                    placeholder="https://example.com"
                                                    required />
                                            </div>
                                            <div class="form-control">
                                                <label class="label" for="edit-text-{url.id}">
                                                    <span class="edit-card-field-name">Link Text</span>
                                                </label>
                                                <input
                                                    type="text"
                                                    id="edit-text-{url.id}"
                                                    name="text"
                                                    class="edit-card-field-input"
                                                    value={editingUrl.text}
                                                    oninput={(e) => (editingUrl.text = e.currentTarget.value)}
                                                    placeholder="Optional display text" />
                                            </div>
                                            <div class="flex gap-2 justify-end">
                                                <button type="button" class="btn btn-sm btn-ghost" onclick={cancelEdit}>
                                                    Cancel
                                                </button>
                                                <button type="submit" class="btn btn-sm btn-success">
                                                    <span class="icon-[lucide--check] size-4"></span>
                                                    Save
                                                </button>
                                            </div>
                                        </div>
                                    </form>
                                {:else}
                                    <!-- View Mode -->
                                    <div class="flex items-start justify-between gap-4">
                                        <div class="flex-1 min-w-0">
                                            <a
                                                href={url.url}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                class="link link-accent break-all">
                                                {url.text || url.url}
                                            </a>
                                            {#if url.text}
                                                <p class="text-sm text-secondary-content break-all mt-1">
                                                    {url.url}
                                                </p>
                                            {/if}
                                        </div>
                                        <div class="flex gap-2 flex-shrink-0">
                                            <button
                                                type="button"
                                                class="btn btn-sm btn-success"
                                                aria-label="Edit URL"
                                                onclick={() => startEdit(url)}>
                                                <span class="icon-[lucide--pencil] size-4"></span>
                                            </button>
                                            <form
                                                method="POST"
                                                action="?/deleteUrl"
                                                use:enhance={() => {
                                                    return async ({ result }) => {
                                                        await applyAction(result);
                                                        if (result.type === "success") {
                                                            await invalidateAll();
                                                        }
                                                    };
                                                }}>
                                                <input type="hidden" name="urlId" value={url.id} />
                                                <button
                                                    type="submit"
                                                    class="btn btn-sm btn-error btn-error"
                                                    aria-label="Delete URL"
                                                    onclick={(e) => {
                                                        if (!confirm("Are you sure you want to delete this URL?")) {
                                                            e.preventDefault();
                                                        }
                                                    }}>
                                                    <span class="icon-[lucide--trash-2] size-4"></span>
                                                </button>
                                            </form>
                                        </div>
                                    </div>
                                {/if}
                            </div>
                        </div>
                    {/each}
                </div>
            {/if}

            <!-- Add New URL -->
            <form
                method="POST"
                action="?/addUrl"
                use:enhance={() => {
                    return async ({ result }) => {
                        await applyAction(result);
                        if (result.type === "success") {
                            newUrl = { url: "", text: "" };
                            await invalidateAll();
                        }
                    };
                }}
                class="card card-border bg-base-200">
                <div class="card-body p-4">
                    <h3 class="font-semibold text-sm mb-3">Add New URL</h3>
                    <div class="space-y-3">
                        <div class="form-control">
                            <label class="label" for="new-url">
                                <span class="edit-card-field-name">URL *</span>
                            </label>
                            <input
                                type="url"
                                id="new-url"
                                name="url"
                                class="edit-card-field-input"
                                value={newUrl.url}
                                oninput={(e) => (newUrl.url = e.currentTarget.value)}
                                placeholder="https://example.com"
                                required />
                        </div>
                        <div class="form-control">
                            <label class="label" for="new-text">
                                <span class="edit-card-field-name">Link Text</span>
                            </label>
                            <input
                                type="text"
                                id="new-text"
                                name="text"
                                class="edit-card-field-input"
                                value={newUrl.text}
                                oninput={(e) => (newUrl.text = e.currentTarget.value)}
                                placeholder="Optional display text" />
                        </div>
                        <button type="submit" class="btn btn-success btn-primary">
                            <span class="icon-[lucide--plus] size-4"></span>
                            Add URL
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</ProtectedPageShell>
