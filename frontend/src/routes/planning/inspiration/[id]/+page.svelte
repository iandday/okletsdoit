<script lang="ts">
    import ObjectDetail from "$lib/components/object/ObjectDetail.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();

    const relativeCrumbs = [
        { title: "Inspirations", href: "/settings/inspiration" },
        { title: data.inspiration.name, href: `/settings/inspiration/${data.inspiration.id}` },
    ];

    function formatDate(dateString: string | Date | null | undefined): string {
        if (!dateString) return "N/A";
        const date = dateString instanceof Date ? dateString : new Date(dateString);
        return date.toLocaleDateString("en-US", {
            year: "numeric",
            month: "long",
            day: "numeric",
        });
    }
</script>

<ObjectDetail
    {relativeCrumbs}
    title={data.inspiration.name}
    editLink={`/settings/inspiration/${data.inspiration.id}/edit`}
    deleteAction="?/delete"
    object={data.inspiration}>
    {#snippet mainSnippet()}
        <div class="space-y-6">
            {#if data.inspiration.image}
                <div>
                    <div class="detail-card-field-name">Image</div>
                    <div class="detail-card-field-value">
                        <img
                            src={data.inspiration.image}
                            alt={data.inspiration.name}
                            class="w-full max-w-2xl rounded-lg shadow-lg" />
                    </div>
                </div>
            {/if}

            {#if data.inspiration.description}
                <div>
                    <div class="detail-card-field-name">Description</div>
                    <div class="detail-card-field-value whitespace-pre-wrap">
                        {data.inspiration.description}
                    </div>
                </div>
            {/if}

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <div class="detail-card-field-name">Created</div>
                    <div class="detail-card-field-value">
                        {formatDate(data.inspiration.createdAt)}
                    </div>
                </div>
                <div>
                    <div class="detail-card-field-name">Last Updated</div>
                    <div class="detail-card-field-value">
                        {formatDate(data.inspiration.updatedAt)}
                    </div>
                </div>
            </div>
        </div>
    {/snippet}
</ObjectDetail>
