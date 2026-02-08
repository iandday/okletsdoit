<script lang="ts">
    import ObjectChildItems from "$lib/components/object/ObjectChildItems.svelte";
    import ObjectDetail from "$lib/components/object/ObjectDetail.svelte";
    import ObjectStatus from "$lib/components/object/ObjectStatus.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();

    const relativeCrumbs = [
        { title: "Budget", href: "/settings/budget" },
        ...(data.category
            ? [{ title: data.category.name, href: `/settings/budget/category/${data.category.id}` }]
            : []),
        { title: data.expense.item, href: `/settings/budget/expense/${data.expense.id}` },
    ];

    const displayName = data.expense.item;

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
</script>

<ObjectDetail
    {relativeCrumbs}
    title={displayName}
    editLink={`/settings/budget/expense/${data.expense.id}/edit`}
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
                            <a href={`/settings/budget/category/${data.expense.categoryId}`} class="link link-accent">
                                {data.category.name}
                            </a>
                        </div>
                    </div>
                {/if}

                {#if data.vendor}
                    <div>
                        <div class="detail-card-field-name">Vendor</div>
                        <div class="detail-card-field-value">
                            <a href={`/settings/contact/${data.expense.vendorId}`} class="link link-accent">
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
                                        href={`/settings/list_entry/${entry.id}`}
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
