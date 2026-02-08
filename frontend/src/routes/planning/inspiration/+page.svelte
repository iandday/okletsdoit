<script lang="ts">
    import Stats from "$lib/components/Stats.svelte";
    import CreateObject from "$lib/components/buttons/CreateObject.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();
    const relativeCrumbs = [{ title: "Inspiration" }];

    // Client-side filtering
    let nameFilter = $state(data.nameFilter || "");

    const filteredInspirations = $derived(
        data.inspirations.filter((inspiration) => {
            if (nameFilter && !inspiration.name.toLowerCase().includes(nameFilter.toLowerCase())) {
                return false;
            }
            return true;
        }),
    );

    // Pagination
    let itemsPerPage = $state(12);
    let currentPage = $state(0);

    const totalPages = $derived(Math.ceil(filteredInspirations.length / itemsPerPage));
    const paginatedInspirations = $derived(
        filteredInspirations.slice(currentPage * itemsPerPage, (currentPage + 1) * itemsPerPage),
    );

    function clearFilters() {
        nameFilter = "";
        currentPage = 0;
    }

    function nextPage() {
        if (currentPage < totalPages - 1) {
            currentPage++;
        }
    }

    function previousPage() {
        if (currentPage > 0) {
            currentPage--;
        }
    }

    function updateItemsPerPage(newValue: number) {
        itemsPerPage = newValue;
        currentPage = 0;
    }
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader
        title="Inspiration Board"
        description="Wedding inspiration board and ideas"
        showButtons={false}>
        <div class="w-full flex gap-4">
            <div class="table-filter-card w-full md:w-96" id="filter-panel">
                <div class="table-filter-card-body">
                    <div class="table-filter-card-title">
                        Filters
                        <button onclick={clearFilters} class="btn btn-error btn-sm">
                            <span class="icon-[lucide--x] size-4"></span>
                            Clear
                        </button>
                    </div>

                    <div class="form-control">
                        <label class="table-filter-card-field-name" for="name-filter">
                            <span>Search Name</span>
                        </label>
                        <input
                            id="name-filter"
                            type="text"
                            placeholder="Search..."
                            class="table-filter-card-field-value-input"
                            bind:value={nameFilter}
                            oninput={() => (currentPage = 0)} />
                    </div>
                </div>
            </div>
            <CreateObject href="/settings/inspiration/new" label="Create Inspiration" />
        </div>
    </ProtectedPageHeader>

    <div class="flex flex-col gap-6 mb-8">
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {#each paginatedInspirations as inspiration (inspiration.id)}
                <a
                    href="/settings/inspiration/{inspiration.id}"
                    class="group relative block h-64 overflow-hidden rounded-lg shadow-lg transition-all duration-300 hover:shadow-2xl"
                    style="transform-style: preserve-3d; perspective: 1000px;">
                    <div
                        class="absolute inset-0 transition-transform duration-500 group-hover:scale-110 group-hover:rotate-1"
                        style="transform-style: preserve-3d;">
                        {#if inspiration.image}
                            <img src={inspiration.image} alt={inspiration.name} class="h-full w-full object-cover" />
                        {:else}
                            <div
                                class="h-full w-full flex items-center justify-center bg-gradient-to-br from-base-200 to-base-300">
                                <span class="icon-[lucide--image-off] size-16 text-base-content/20"></span>
                            </div>
                        {/if}
                        <div
                            class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent opacity-80 transition-opacity duration-300 group-hover:opacity-90">
                        </div>
                    </div>
                    <div class="absolute bottom-0 left-0 right-0 p-4 text-white z-10">
                        <h3
                            class="text-lg font-bold mb-1 transform transition-transform duration-300 group-hover:translate-y-[-4px]">
                            {inspiration.name}
                        </h3>
                        {#if inspiration.description}
                            <p class="text-sm text-white/90 line-clamp-2">{inspiration.description}</p>
                        {/if}
                    </div>
                </a>
            {:else}
                <div class="col-span-full text-center py-12">
                    <span class="icon-[lucide--image-off] size-16 text-base-content/20 mb-4 inline-block"></span>
                    <p class="text-base-content/60">No inspirations found</p>
                </div>
            {/each}
        </div>

        {#if totalPages > 1}
            <div class="flex items-center justify-between px-4 py-3 bg-base-100 border border-base-300 rounded-lg">
                <div class="flex items-center gap-2">
                    <span class="text-sm text-secondary-content">Items per page:</span>
                    <select
                        class="select select-sm select-bordered bg-base-100"
                        bind:value={itemsPerPage}
                        onchange={() => (currentPage = 0)}>
                        <option value={12}>12</option>
                        <option value={24}>24</option>
                        <option value={36}>36</option>
                        <option value={filteredInspirations.length}>All</option>
                    </select>
                </div>

                <div class="flex items-center gap-4">
                    <span class="text-sm text-secondary-content">
                        Page {currentPage + 1} of {totalPages}
                    </span>
                    <div class="join">
                        <button class="join-item btn btn-sm" onclick={previousPage} disabled={currentPage === 0}>
                            Previous
                        </button>
                        <button
                            class="join-item btn btn-sm"
                            onclick={nextPage}
                            disabled={currentPage >= totalPages - 1}>
                            Next
                        </button>
                    </div>
                </div>
            </div>
        {/if}
    </div>
</ProtectedPageShell>
