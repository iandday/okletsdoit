<script lang="ts">
    import CreateObject from "$lib/components/buttons/CreateObject.svelte";
    import EditObject from "$lib/components/buttons/EditObject.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();
    const relativeCrumbs = [{ title: "Ideas", href: "/settings/idea" }];

    let searchQuery = $state("");

    // Client-side filtering
    const filteredIdeas = $derived(
        searchQuery.trim()
            ? data.ideas.filter((idea) => {
                  const query = searchQuery.toLowerCase();
                  return idea.name?.toLowerCase().includes(query) || idea.description?.toLowerCase().includes(query);
              })
            : data.ideas,
    );
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader title="Ideas" description="Manage your wedding ideas and concepts">
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-8">
            <!-- Search Input -->
            <div class="flex-1 max-w-md">
                <div class="join w-full">
                    <input
                        type="search"
                        placeholder="Search ideas..."
                        class="edit-card-field-input join-item flex-1"
                        bind:value={searchQuery} />
                </div>
            </div>
            <CreateObject href="/settings/idea/new" label="New Idea" />
        </div>
    </ProtectedPageHeader>

    {#if data.ideas.length === 0}
        <!-- Empty State -->
        <div class="card bg-base-100 border border-base-300 shadow-lg">
            <div class="card-body items-center text-center py-16">
                <span class="icon-[lucide--lightbulb] size-16 text-base-content/30 mb-4"></span>
                <h3 class="text-xl font-semibold text-base-content mb-2">No ideas yet</h3>
                <p class="text-base-content/70 mb-6 max-w-md">
                    Create your first idea to start organizing concepts and plans for your wedding.
                </p>
                <a href="/settings/idea/new" class="btn btn-primary gap-2">
                    <span class="icon-[lucide--plus] size-5"></span>
                    Create First Idea
                </a>
            </div>
        </div>
    {:else}
        <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
            {#each filteredIdeas as idea (idea.id)}
                <div class="list-card">
                    <div class="list-card-body">
                        <div class="list-card-title flex items-start justify-between mb-4">
                            <a href="/settings/idea/{idea.id}" class="link link-hover">
                                {idea.name}
                            </a>
                            <EditObject href="/settings/idea/{idea.id}/edit" size="sm" />
                        </div>

                        <!-- eslint-disable-next-line svelte/no-at-html-tags set by site admin -->
                        <div class="tiptap-content">{@html idea.description || ""}</div>
                    </div>
                </div>
            {:else}
                <div class="col-span-full text-center py-12">
                    <span class="icon-[lucide--search] size-16 text-base-content/20 mb-4 inline-block"></span>
                    <p class="text-base-content/60">No ideas match your search</p>
                </div>
            {/each}
        </div>
    {/if}
</ProtectedPageShell>
