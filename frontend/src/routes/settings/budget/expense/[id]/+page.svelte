<script lang="ts">
    import ObjectDetail from "$lib/components/object/ObjectDetail.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();

    const relativeCrumbs = [
        { title: "Budget", href: "/settings/budget" },
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

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {#if data.category}
                    <div>
                        <div class="detail-card-field-name">Category</div>
                        <div class="detail-card-field-value">
                            <a href={`/settings/budget/category/${data.expense.categoryId}`} class="link link-primary">
                                {data.category.name}
                            </a>
                        </div>
                    </div>
                {/if}

                {#if data.vendor}
                    <div>
                        <div class="detail-card-field-name">Vendor</div>
                        <div class="detail-card-field-value">
                            <a href={`/settings/contacts/${data.expense.vendorId}`} class="link link-primary">
                                {data.vendor.name}
                            </a>
                        </div>
                    </div>
                {/if}

                {#if data.list}
                    <div>
                        <div class="detail-card-field-name">List</div>
                        <div class="detail-card-field-value">
                            <a href={`/settings/list/${data.list.id}`} class="link link-primary">
                                {data.list.name}
                            </a>
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

            <div class="divider"></div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                {#if data.expense.estimatedAmount}
                    <div>
                        <div class="detail-card-field-name">Estimated Amount</div>
                        <div class="detail-card-field-value text-lg">
                            {formatCurrency(Number(data.expense.estimatedAmount))}
                        </div>
                    </div>
                {/if}

                {#if data.expense.actualAmount}
                    <div>
                        <div class="detail-card-field-name">Actual Amount</div>
                        <div class="detail-card-field-value text-lg font-semibold">
                            {formatCurrency(Number(data.expense.actualAmount))}
                        </div>
                    </div>
                {/if}

                {#if data.expense.calculatedPrice}
                    <div>
                        <div class="detail-card-field-name">Calculated Price</div>
                        <div class="detail-card-field-value text-lg">
                            {formatCurrency(Number(data.expense.calculatedPrice))}
                        </div>
                    </div>
                {/if}
            </div>

            {#if data.expense.variance}
                <div>
                    <div class="detail-card-field-name">Variance</div>
                    <div
                        class="detail-card-field-value text-lg font-bold"
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

            <div>
                <div class="detail-card-field-name">Status</div>
                <div class="detail-card-field-value">
                    {#if data.expense.purchased}
                        <span class="badge badge-success">Purchased</span>
                    {:else}
                        <span class="badge badge-ghost">Pending</span>
                    {/if}
                </div>
            </div>
        </div>
    {/snippet}
</ObjectDetail>
