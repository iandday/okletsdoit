<script lang="ts">
    import ObjectDetail from "$lib/components/object/ObjectDetail.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();

    const relativeCrumbs = [
        { title: "Ideas", href: "/settings/idea" },
        {
            title: data.idea.name,
            href: `/settings/idea/${data.idea.id}`,
        },
    ];
</script>

<ObjectDetail
    {relativeCrumbs}
    title={data.idea.name}
    editLink={`/settings/idea/${data.idea.id}/edit`}
    deleteAction="?/delete"
    object={data.idea}>
    {#snippet mainSnippet()}
        <div class="space-y-6">
            <!-- Basic Information -->
            <div class="grid grid-cols-1 gap-4">
                <div>
                    <div class="detail-card-field-name">Name</div>
                    <div class="detail-card-field-value">{data.idea.name}</div>
                </div>

                <div>
                    <div class="detail-card-field-name">Description</div>
                    <div class="detail-card-field-value">
                        {#if data.idea.description}
                            <div class="tiptap-content">
                                <!-- eslint-disable-next-line svelte/no-at-html-tags set by site admin -->
                                {@html data.idea.description}
                            </div>
                        {:else}
                            <p class="text-base-content/50 italic">No description provided</p>
                        {/if}
                    </div>
                </div>
            </div>

            <!-- Timestamps -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4"></div>
        </div>
    {/snippet}
</ObjectDetail>
