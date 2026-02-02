<script lang="ts">
    import { enhance } from "$app/forms";
    import ObjectDetail from "$lib/components/object/ObjectDetail.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();

    let isSubmittingCompleted = $state(false);
    let isSubmittingPurchased = $state(false);

    const relativeCrumbs = [
        { title: "Lists", href: "/settings/list" },
        { title: data.list.name, href: `/settings/list/${data.list.id}` },
        { title: data.entry.item, href: `/settings/list_entry/${data.entry.id}` },
    ];

    const displayName = data.entry.item;

    function formatPrice(price: number | string): string {
        const num = typeof price === "string" ? parseFloat(price) : price;
        return new Intl.NumberFormat("en-US", {
            style: "currency",
            currency: "USD",
        }).format(num);
    }

    function formatDate(dateString: string | Date | null | undefined): string {
        if (!dateString) return "N/A";
        const date = dateString instanceof Date ? dateString : new Date(dateString);
        return date.toLocaleDateString();
    }
</script>

<ObjectDetail
    {relativeCrumbs}
    title={displayName}
    editLink={`/settings/list_entry/${data.entry.id}/edit`}
    deleteAction="?/delete"
    object={data.entry}>
    {#snippet mainSnippet()}
        <div class="space-y-6">
            <!-- Basic Information -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <div class="detail-card-field-name">Item Name</div>
                    <div class="detail-card-field-value">{data.entry.item}</div>
                </div>

                <div>
                    <div class="detail-card-field-name">Completed Date</div>
                    <div class="detail-card-field-value">
                        {#if data.entry.completedAt}{formatDate(data.entry.completedAt)}{:else}N/A{/if}
                    </div>
                </div>
                <div>
                    <div class="detail-card-field-name">Status</div>
                    <div class="detail-card-field-value">
                        <span class="badge {data.entry.isCompleted ? 'badge-success' : 'badge-accent'}">
                            {data.entry.isCompleted ? "Completed" : "Pending"}
                        </span>
                    </div>
                </div>

                <div>
                    <div class="detail-card-field-name">Purchased</div>
                    <div class="detail-card-field-value">
                        <span class="badge {data.entry.purchased ? 'badge-success' : 'badge-accent'}">
                            {data.entry.purchased ? "Yes" : "No"}
                        </span>
                    </div>
                </div>
            </div>

            {#if data.entry.description}
                <div>
                    <div class="detail-card-field-name">Description</div>
                    <div class="detail-card-field-value whitespace-pre-wrap">{data.entry.description}</div>
                </div>
            {/if}

            <!-- Pricing Information -->
            <div>
                <h3 class="text-lg font-semibold mb-3">Pricing</h3>
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div>
                        <div class="detail-card-field-name">Quantity</div>
                        <div class="detail-card-field-value text-2xl font-bold">{data.entry.quantity}</div>
                    </div>

                    <div>
                        <div class="detail-card-field-name">Unit Price</div>
                        <div class="detail-card-field-value text-xl">{formatPrice(data.entry.unitPrice)}</div>
                    </div>

                    <div>
                        <div class="detail-card-field-name">Additional Price</div>
                        <div class="detail-card-field-value text-xl">{formatPrice(data.entry.additionalPrice)}</div>
                    </div>

                    <div>
                        <div class="detail-card-field-name">Total Price</div>
                        <div class="detail-card-field-value text-2xl font-bold text-success">
                            {formatPrice(data.entry.totalPrice)}
                        </div>
                    </div>
                </div>
            </div>

            <!-- Vendor Information -->
            {#if data.vendor}
                <div>
                    <h3 class="text-lg font-semibold mb-3">Vendor</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <div class="detail-card-field-name">Vendor Name</div>
                            <div class="detail-card-field-value">
                                <a href="/settings/contact/{data.vendor.id}" class="link link-accent">
                                    {data.vendor.name || data.vendor.company || "Unnamed Vendor"}
                                </a>
                            </div>
                        </div>

                        {#if data.vendor.email}
                            <div>
                                <div class="detail-card-field-name">Email</div>
                                <div class="detail-card-field-value flex items-center gap-2">
                                    <span class="icon-[lucide--mail] size-4"></span>
                                    <a href="mailto:{data.vendor.email}" class="link link-accent">
                                        {data.vendor.email}
                                    </a>
                                </div>
                            </div>
                        {/if}

                        {#if data.vendor.phone}
                            <div>
                                <div class="detail-card-field-name">Phone</div>
                                <div class="detail-card-field-value flex items-center gap-2">
                                    <span class="icon-[lucide--phone] size-4"></span>
                                    <a href="tel:{data.vendor.phone}" class="link link-accent">{data.vendor.phone}</a>
                                </div>
                            </div>
                        {/if}
                    </div>
                </div>
            {/if}

            <!-- Additional Information -->
            {#if data.entry.url}
                <div>
                    <div class="detail-card-field-name">Product URL</div>
                    <div class="detail-card-field-value flex items-center gap-2">
                        <span class="icon-[lucide--external-link] size-4"></span>
                        <a href={data.entry.url} target="_blank" rel="noopener noreferrer" class="link link-accent">
                            {data.entry.url}
                        </a>
                    </div>
                </div>
            {/if}

            <!-- Toggle Status -->
            <div class="mt-6 flex gap-4">
                <form
                    method="POST"
                    action="?/toggleCompleted"
                    use:enhance={() => {
                        isSubmittingCompleted = true;
                        return async ({ update }) => {
                            await update();
                            isSubmittingCompleted = false;
                        };
                    }}>
                    <button
                        type="submit"
                        class="btn {data.entry.isCompleted ? 'btn-error' : 'btn-success'}"
                        disabled={isSubmittingCompleted}>
                        {#if isSubmittingCompleted}
                            <span class="loading loading-spinner loading-sm"></span>
                        {:else}
                            <span class="icon-[lucide--check-circle] size-5"></span>
                        {/if}
                        {data.entry.isCompleted ? "Mark as Pending" : "Mark as Completed"}
                    </button>
                </form>

                <form
                    method="POST"
                    action="?/togglePurchased"
                    use:enhance={() => {
                        isSubmittingPurchased = true;
                        return async ({ update }) => {
                            await update();
                            isSubmittingPurchased = false;
                        };
                    }}>
                    <button
                        type="submit"
                        class="btn {data.entry.purchased ? 'btn-error' : 'btn-success'}"
                        disabled={isSubmittingPurchased}>
                        {#if isSubmittingPurchased}
                            <span class="loading loading-spinner loading-sm"></span>
                        {:else}
                            <span class="icon-[lucide--shopping-cart] size-5"></span>
                        {/if}
                        {data.entry.purchased ? "Mark as Not Purchased" : "Mark as Purchased"}
                    </button>
                </form>
                {#if data.entry.associatedExpenseId}
                    <a href="/settings/expense/{data.entry.associatedExpenseId}" class="btn btn-accent gap-2">
                        View Expense
                    </a>
                {/if}
            </div>
        </div>
    {/snippet}
</ObjectDetail>
