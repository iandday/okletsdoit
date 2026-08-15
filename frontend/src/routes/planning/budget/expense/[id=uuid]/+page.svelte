<script lang="ts">
    import { enhance } from "$app/forms";
    import ObjectChildItems from "$lib/components/object/ObjectChildItems.svelte";
    import ObjectDetail from "$lib/components/object/ObjectDetail.svelte";
    import ObjectStatus from "$lib/components/object/ObjectStatus.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();

    const relativeCrumbs = [
        { title: "Budget", href: "/planning/budget" },
        ...(data.category
            ? [{ title: data.category.name, href: `/planning/budget/category/${data.category.id}` }]
            : []),
        { title: data.expense.item, href: `/planning/budget/expense/${data.expense.id}` },
    ];

    const displayName = data.expense.item;
    let showUploadForm = $state(false);
    let uploadingFile = $state(false);

    function formatCurrency(amount: number): string {
        return new Intl.NumberFormat("en-US", {
            style: "currency",
            currency: "USD",
        }).format(amount);
    }

    function formatDate(dateString: string | Date | null | undefined): string {
        if (!dateString) return "N/A";
        const date = dateString instanceof Date ? dateString : new Date(dateString);
        return date.toLocaleDateString();
    }

    function getAttachmentDownloadUrl(attachment: { fileUrl?: string }) {
        return (attachment as { downloadUrl?: string }).downloadUrl || attachment.fileUrl || "";
    }
</script>

<ObjectDetail
    {relativeCrumbs}
    title={displayName}
    editLink={`/planning/budget/expense/${data.expense.id}/edit`}
    deleteAction="?/delete"
    status={data.purchaseStatus}
    statusText={data.purchaseStatus ? "Purchased" : "Pending"}
    object={data.expense}>
    {#snippet mainSnippet()}
        <div class="space-y-4">
            {#if data.expense.description}
                <div>
                    <div class="detail-card-field-name">Description</div>
                    <div class="detail-card-field-value whitespace-pre-wrap">
                        {data.expense.description}
                    </div>
                </div>
            {/if}
            <div class="grid grid-cols-2 gap-4 mt-4">
                {#if data.category}
                    <div>
                        <div class="detail-card-field-name">Category</div>
                        <div class="detail-card-field-value">
                            <a href={`/planning/budget/category/${data.expense.categoryId}`} class="link link-accent">
                                {data.category.name}
                            </a>
                        </div>
                    </div>
                {/if}

                {#if data.vendor}
                    <div>
                        <div class="detail-card-field-name">Vendor</div>
                        <div class="detail-card-field-value">
                            <a href={`/planning/contact/${data.expense.vendorId}`} class="link link-accent">
                                {#if data.vendor.name && data.vendor.company}
                                    {data.vendor.name} ({data.vendor.company})
                                {:else if data.vendor.name}
                                    {data.vendor.name}
                                {:else}
                                    {data.vendor.company}
                                {/if}
                            </a>
                        </div>
                    </div>
                {/if}

                {#if data.listEntries && data.listEntries.length === 0}
                    <div>
                        <div class="detail-card-field-name">Quantity</div>
                        <div class="detail-card-field-value">{data.expense.quantity}</div>
                    </div>
                    <div>
                        <div class="detail-card-field-name">Unit Price</div>
                        <div class="detail-card-field-value">{data.expense.unitPrice}</div>
                    </div>
                    <div>
                        <div class="detail-card-field-name">Additional Price</div>
                        <div class="detail-card-field-value">{data.expense.additionalPrice}</div>
                    </div>
                {/if}
            </div>
            <div class="divider"></div>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
                <div>
                    <div class="detail-card-field-name">Estimated Amount</div>
                    <div class="detail-card-field-value">{data.expense.estimatedAmount}</div>
                </div>
                <div>
                    <div class="detail-card-field-name">Actual Amount</div>
                    <div class="detail-card-field-value">{data.expense.actualAmount}</div>
                </div>
                {#if data.expense.variance}
                    <div>
                        <div class="detail-card-field-name">Variance</div>
                        <div
                            class=" text-md font-bold"
                            class:text-error={Number(data.expense.variance) > 0}
                            class:text-success={Number(data.expense.variance) <= 0}>
                            {formatCurrency(Number(data.expense.variance))}
                            {#if Number(data.expense.variance) > 0}
                                (Over Budget)
                            {:else if Number(data.expense.variance) < 0}
                                (Under Budget)
                            {:else}
                                (On Budget)
                            {/if}
                        </div>
                    </div>
                {/if}

                {#if data.expense.date}
                    <div>
                        <div class="detail-card-field-name">Date</div>
                        <div class="detail-card-field-value">
                            {formatDate(data.expense.date)}
                        </div>
                    </div>
                {/if}
            </div>

            <!-- Attachments -->
            <div>
                <div class="flex items-center justify-between mb-4">
                    <div class="detail-card-field-name">Attachments ({data.attachments.length})</div>
                    <button
                        type="button"
                        onclick={() => (showUploadForm = !showUploadForm)}
                        class="btn btn-sm btn-primary gap-2">
                        <span class="icon-[lucide--plus] size-4"></span>
                        {showUploadForm ? "Cancel" : "Add Attachment"}
                    </button>
                </div>

                {#if showUploadForm}
                    <form
                        method="POST"
                        action="?/uploadAttachment"
                        enctype="multipart/form-data"
                        class="edit-card p-6 mb-6"
                        use:enhance={() => {
                            uploadingFile = true;
                            return async ({ update }) => {
                                await update();
                                uploadingFile = false;
                                showUploadForm = false;
                            };
                        }}>
                        <div class="space-y-4">
                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="file">
                                    <span>File</span>
                                </label>
                                <input
                                    type="file"
                                    id="file"
                                    name="file"
                                    class="file-input file-input-bordered w-full"
                                    required
                                    disabled={uploadingFile} />
                            </div>

                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="attachment-name">
                                    <span>Name (optional)</span>
                                </label>
                                <input
                                    type="text"
                                    id="attachment-name"
                                    name="name"
                                    class="edit-card-field-input"
                                    placeholder="Custom name for the file"
                                    disabled={uploadingFile} />
                            </div>

                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="attachment-description">
                                    <span>Description (optional)</span>
                                </label>
                                <textarea
                                    id="attachment-description"
                                    name="description"
                                    class="edit-card-field-input"
                                    rows="2"
                                    placeholder="Add a description..."
                                    disabled={uploadingFile}></textarea>
                            </div>

                            <div class="flex gap-2 justify-end">
                                <button
                                    type="button"
                                    class="btn btn-error"
                                    onclick={() => (showUploadForm = false)}
                                    disabled={uploadingFile}>
                                    Cancel
                                </button>
                                <button type="submit" class="btn btn-success gap-2" disabled={uploadingFile}>
                                    {#if uploadingFile}
                                        <span class="loading loading-spinner loading-sm"></span>
                                        Uploading...
                                    {:else}
                                        <span class="icon-[lucide--upload] size-4"></span>
                                        Upload
                                    {/if}
                                </button>
                            </div>
                        </div>
                    </form>
                {/if}

                {#if data.attachments.length > 0}
                    <div class="grid grid-cols-1 gap-3">
                        {#each data.attachments as attachment (attachment.id)}
                            <div class="flex items-center gap-3 p-3 bg-base-200 rounded-lg group">
                                <span class="icon-[lucide--file-text] size-6"></span>
                                <div class="flex-1 min-w-0">
                                    <p class="text-sm font-medium">{attachment.name || attachment.filename}</p>
                                    {#if attachment.description}
                                        <p class="text-xs truncate">{attachment.description}</p>
                                    {/if}
                                </div>
                                <div class="flex gap-1">
                                    <a
                                        href={getAttachmentDownloadUrl(attachment)}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        class="btn btn-xs btn-ghost"
                                        title="Download">
                                        <span class="icon-[lucide--download] size-4"></span>
                                    </a>
                                    <form
                                        method="POST"
                                        action="?/deleteAttachment"
                                        use:enhance={() => {
                                            return async ({ update }) => {
                                                if (confirm("Are you sure you want to delete this attachment?")) {
                                                    await update();
                                                }
                                            };
                                        }}>
                                        <input type="hidden" name="attachmentId" value={attachment.id} />
                                        <button type="submit" class="btn btn-xs btn-error" title="Delete">
                                            <span class="icon-[lucide--trash] size-4"></span>
                                        </button>
                                    </form>
                                </div>
                            </div>
                        {/each}
                    </div>
                {:else if !showUploadForm}
                    <p class="text-sm text-base-content/50 italic">No attachments yet</p>
                {/if}
            </div>
        </div>
    {/snippet}
    {#snippet extraCardsSnippet()}
        {#if data.listEntries && data.listEntries.length > 0}
            <ObjectChildItems title="Linked List Entries">
                <div class="grid gap-4 grid-cols-1 md:grid-cols-2">
                    {#each data.listEntries as entry, index (entry.id)}
                        <div class="list-card">
                            <div class="list-card-body">
                                <div class="list-card-title">
                                    <a
                                        href={`/planning/list_entry/${entry.id}`}
                                        class="link link-accent font-semibold text-lg">
                                        {entry.item} ({formatCurrency(entry.totalPrice)})
                                    </a>
                                </div>
                                <div class="flex flex-row items-center gap-4 mt-2">
                                    <ObjectStatus
                                        status={entry.purchased}
                                        text={entry.purchased ? "Purchased" : "Not Purchased"} />
                                </div>
                                <div class="text-sm text-muted-foreground mt-1">
                                    Quantity: {entry.quantity} | Unit Price: {formatCurrency(entry.unitPrice)} | Additional
                                    Price:
                                    {formatCurrency(entry.additionalPrice)}
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>
            </ObjectChildItems>
        {/if}
    {/snippet}
</ObjectDetail>
