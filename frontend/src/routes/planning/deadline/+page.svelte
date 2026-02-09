<script lang="ts">
    import Icon from "$lib/components/Icon.svelte";
    import CreateObject from "$lib/components/buttons/CreateObject.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();
    const relativeCrumbs = [{ title: "Deadlines", href: "/planning/deadline" }];
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader title="Deadline Summary" description="Manage your wedding planning deadlines and tasks" />
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
        <div>
            <CreateObject href="/planning/deadline/list/new" label="New List" />
            <a href="/planning/deadline/all" class="btn btn-primary gap-2">
                <span class="icon-[lucide--calendar-check] size-5"></span>
                View All Deadlines</a>
        </div>
    </div>

    {#if data.deadlineLists.length === 0}
        <!-- Empty State -->
        <div class="card bg-base-100 border border-base-300 shadow-lg">
            <div class="card-body items-center text-center py-16">
                <span class="icon-[lucide--clipboard-list] size-16 text-base-content/30 mb-4"></span>
                <h3 class="text-xl font-semibold text-base-content mb-2">No deadline lists yet</h3>
                <p class="text-base-content/70 mb-6 max-w-md">
                    Create your first deadline list to start organizing your wedding planning tasks and staying on
                    track.
                </p>
                <a href="/planning/deadline/list/new" class="btn btn-primary gap-2">
                    <span class="icon-[lucide--plus] size-5"></span>
                    Create First List
                </a>
            </div>
        </div>
    {:else}
        <!-- Deadline Lists Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each data.deadlineLists as list (list.id)}
                <div class="list-card">
                    <div class="list-card-body">
                        <div class="list-card-title">
                            <a href="/planning/deadline/list/{list.id}">{list.name}</a>
                        </div>
                        <div class="flex flex-row gap-2 mb-4">
                            <div class="badge badge-success">✓ {list.completedCount}</div>
                            <div class="badge badge-accent">⏳ {list.pendingCount}</div>
                        </div>
                        <div class="mb-4">
                            <div class="flex items-center justify-between text-sm mb-2">
                                <span>Progress</span>
                                <span>{list.completionPercentage}%</span>
                            </div>
                            <progress
                                class="progress progress-primary w-full text-accent"
                                value={list.completionPercentage}
                                max="100"></progress>
                        </div>
                        <!-- Footer -->
                        <div class="list-card-actions">
                            <span class="text-xs">
                                Last updated {new Date(list.updatedAt).toLocaleDateString()}
                            </span>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</ProtectedPageShell>
