<script lang="ts">
    import { enhance } from "$app/forms";
    import ObjectDetail from "$lib/components/object/ObjectDetail.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();

    const relativeCrumbs = [
        { title: "Contacts", href: "/settings/contact" },
        {
            title: data.contact.name || data.contact.company || "Contact",
            href: `/settings/contact/${data.contact.id}`,
        },
    ];

    const displayName = data.contact.name
        ? data.contact.company
            ? `${data.contact.name} (${data.contact.company})`
            : data.contact.name
        : data.contact.company || "Contact";

    let showUploadForm = $state(false);
    let uploadingFile = $state(false);
</script>

<ObjectDetail
    {relativeCrumbs}
    title={displayName}
    editLink={`/settings/contact/${data.contact.id}/edit`}
    deleteAction="?/delete"
    object={data.contact}>
    {#snippet mainSnippet()}
        <div class="space-y-6">
            <!-- Basic Information -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {#if data.contact.name}
                    <div>
                        <div class="detail-card-field-name">Name</div>
                        <div class="detail-card-field-value">{data.contact.name}</div>
                    </div>
                {/if}

                {#if data.contact.company}
                    <div>
                        <div class="detail-card-field-name">Company</div>
                        <div class="detail-card-field-value">{data.contact.company}</div>
                    </div>
                {/if}

                {#if data.contact.category}
                    <div>
                        <div class="detail-card-field-name">Category</div>
                        <div class="detail-card-field-value">
                            <span class="badge badge-primary">{data.contact.category}</span>
                        </div>
                    </div>
                {/if}
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {#if data.contact.email}
                    <div>
                        <div class="detail-card-field-name">Email</div>
                        <div class="detail-card-field-value flex items-center gap-2">
                            <span class="icon-[lucide--mail] size-4 text-base-content"></span>
                            <a href="mailto:{data.contact.email}" class="link link-hover">{data.contact.email}</a>
                        </div>
                    </div>
                {/if}

                {#if data.contact.phone}
                    <div>
                        <div class="detail-card-field-name">Phone</div>
                        <div class="detail-card-field-value flex items-center gap-2">
                            <span class="icon-[lucide--phone] size-4 text-base-content"></span>
                            <a href="tel:{data.contact.phone}" class="link link-hover">{data.contact.phone}</a>
                        </div>
                    </div>
                {/if}

                {#if data.contact.website}
                    <div>
                        <div class="detail-card-field-name">Website</div>
                        <div class="detail-card-field-value flex items-center gap-2">
                            <span class="icon-[lucide--globe] size-4 text-base-content"></span>
                            <a
                                href={data.contact.website}
                                target="_blank"
                                rel="noopener noreferrer"
                                class="link link-hover">
                                {data.contact.website}
                            </a>
                        </div>
                    </div>
                {/if}
            </div>

            <!-- Notes -->
            {#if data.contact.notes}
                <div>
                    <div class="detail-card-field-name">Notes</div>
                    <div class="detail-card-field-value whitespace-pre-wrap">{data.contact.notes}</div>
                </div>
            {/if}

            <!-- Attachments -->
            <div>
                <div class="flex items-center justify-between mb-4">
                    <div class="detail-card-field-name">
                        Attachments ({data.attachments.length})
                    </div>
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
                                    <p class="text-sm font-medium">
                                        {attachment.name || attachment.filename}
                                    </p>
                                    {#if attachment.description}
                                        <p class="text-xs truncate">
                                            {attachment.description}
                                        </p>
                                    {/if}
                                </div>
                                <div class="flex gap-1">
                                    <a
                                        href={attachment.fileUrl}
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
</ObjectDetail>
