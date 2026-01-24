<!-- src/routes/settings/guest_list/+page.svelte -->
<script lang="ts">
    import CreateObject from "$lib/components/buttons/CreateObject.svelte";
    import ViewDetails from "$lib/components/buttons/ViewDetails.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();
    const relativeCrumbs = [{ title: "Guest List" }];

    // Client-side filtering
    let nameFilter = $state("");
    let priorityFilter = $state("");
    let relationshipFilter = $state("");

    // Derive unique values from data for filter options
    const availablePriorities = $derived(
        Array.from(
            new Set(
                data.guestGroups
                    .map((g) => g.priority)
                    .filter((p) => p != null)
                    .sort((a, b) => b - a), // Sort descending (High to Low)
            ),
        ).map((priority) => ({
            value: priority.toString(),
            label: data.guestGroups.find((g) => g.priority === priority)?.priorityDisplay || "",
        })),
    );

    const availableRelationships = $derived(
        Array.from(new Set(data.guestGroups.map((g) => g.relationship).filter((r) => r != null && r !== "")))
            .sort()
            .map((relationship) => ({
                value: relationship,
                label:
                    data.guestGroups.find((g) => g.relationship === relationship)?.relationshipDisplay || relationship,
            })),
    );

    const filteredGuestGroups = $derived(
        data.guestGroups.filter((group) => {
            if (nameFilter && !group.name.toLowerCase().includes(nameFilter.toLowerCase())) {
                return false;
            }
            if (priorityFilter && group.priority?.toString() !== priorityFilter) {
                return false;
            }
            if (relationshipFilter && group.relationship !== relationshipFilter) {
                return false;
            }
            return true;
        }),
    );

    function clearFilters() {
        nameFilter = "";
        priorityFilter = "";
        relationshipFilter = "";
    }

    function getRsvpProgress(group: any): number {
        if (group.groupInvitedCount === 0) return 0;
        return Math.round((group.groupAttendingCount / group.groupInvitedCount) * 100);
    }

    // Derive priority styling dynamically based on relative values
    const priorityRange = $derived(() => {
        const priorities = data.guestGroups.map((g) => g.priority).filter((p) => p != null);
        if (priorities.length === 0) return { min: 1, max: 3 };
        return {
            min: Math.min(...priorities),
            max: Math.max(...priorities),
        };
    });

    function getPriorityClass(priority: number): string {
        if (priority == null) return "badge-ghost";

        const range = priorityRange();
        const span = range.max - range.min;

        // If only one priority level exists, use neutral color
        if (span === 0) return "badge-neutral";

        // Calculate relative position (0 = lowest, 1 = highest)
        const relativePosition = (priority - range.min) / span;

        // Map to badge classes based on position
        if (relativePosition >= 0.66) return "badge-error"; // High priority
        if (relativePosition >= 0.33) return "badge-warning"; // Medium priority
        return "badge-info"; // Low priority
    }
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader title="Guest List" description="Manage your wedding guest groups and RSVPs">
        <div class="stats shadow mt-8 w-full">
            <div class="stat">
                <div class="stat-figure text-primary">
                    <span class="icon-[lucide--users] size-8"></span>
                </div>
                <div class="stat-title">Guest Groups</div>
                <div class="stat-value text-primary">{filteredGuestGroups.length}</div>
                <div class="stat-desc">of {data.count} total</div>
            </div>

            <div class="stat">
                <div class="stat-figure text-secondary">
                    <span class="icon-[lucide--user] size-8"></span>
                </div>
                <div class="stat-title">Guests</div>
                <div class="stat-value text-secondary">
                    {filteredGuestGroups.reduce((sum, group) => sum + group.groupCount, 0)}
                </div>
                <div class="stat-desc">
                    of {data.guestGroups.reduce((sum, group) => sum + group.groupCount, 0)} total
                </div>
            </div>

            <div class="stat">
                <div class="stat-figure text-success">
                    <span class="icon-[lucide--check-circle] size-8"></span>
                </div>
                <div class="stat-title">Attending</div>
                <div class="stat-value text-success">
                    {filteredGuestGroups.reduce((sum, group) => sum + group.groupAttendingCount, 0)}
                </div>
                <div class="stat-desc">
                    of {data.guestGroups.reduce((sum, group) => sum + group.groupAttendingCount, 0)} total
                </div>
            </div>

            <div class="stat">
                <div class="stat-figure text-info">
                    <span class="icon-[lucide--mail] size-8"></span>
                </div>
                <div class="stat-title">Invited</div>
                <div class="stat-value text-info">
                    {filteredGuestGroups.reduce((sum, group) => sum + group.groupInvitedCount, 0)}
                </div>
                <div class="stat-desc">
                    of {data.guestGroups.reduce((sum, group) => sum + group.groupInvitedCount, 0)} total
                </div>
            </div>
        </div>
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-8">
            <CreateObject href="/settings/guest_list/new" label="New Guest Group" />
        </div>

        <!-- Filters -->
        <div class="config-card mb-6">
            <div class="config-card-body">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-semibold">Filters</h3>
                    <button onclick={clearFilters} class="btn btn-ghost btn-sm">
                        <span class="icon-[lucide--x] size-4"></span>
                        Clear All
                    </button>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="form-control">
                        <label class="label" for="name-filter">
                            <span class="label-text">Name</span>
                        </label>
                        <input
                            type="text"
                            id="name-filter"
                            class="input input-bordered"
                            placeholder="Search by name..."
                            bind:value={nameFilter} />
                    </div>

                    <div class="form-control">
                        <label class="label" for="priority-filter">
                            <span class="label-text">Priority</span>
                        </label>
                        <select id="priority-filter" class="select select-bordered" bind:value={priorityFilter}>
                            <option value="">All Priorities</option>
                            {#each availablePriorities as { value, label } (value)}
                                <option {value}>{label}</option>
                            {/each}
                        </select>
                    </div>

                    <div class="form-control">
                        <label class="label" for="relationship-filter">
                            <span class="label-text">Relationship</span>
                        </label>
                        <select id="relationship-filter" class="select select-bordered" bind:value={relationshipFilter}>
                            <option value="">All Relationships</option>
                            {#each availableRelationships as { value, label } (value)}
                                <option {value}>{label}</option>
                            {/each}
                        </select>
                    </div>
                </div>
            </div>
        </div>
    </ProtectedPageHeader>

    {#if data.guestGroups.length === 0}
        <div class="alert">
            <span class="icon-[lucide--info] size-6"></span>
            <div>
                <h3 class="font-bold">No guest groups yet</h3>
                <div class="text-sm">Get started by creating your first guest group.</div>
            </div>
        </div>
    {:else if filteredGuestGroups.length === 0}
        <div class="alert alert-warning">
            <span class="icon-[lucide--filter-x] size-6"></span>
            <div>
                <h3 class="font-bold">No matches found</h3>
                <div class="text-sm">Try adjusting your filters or clear them to see all groups.</div>
            </div>
        </div>
    {:else}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each filteredGuestGroups as group (group.id)}
                {@const rsvpProgress = getRsvpProgress(group)}
                <a href="/settings/guest_list/{group.id}" class="list-card">
                    <div class="list-card-body">
                        <div class="flex items-start justify-between gap-2">
                            <h2 class="list-card-title text-lg">{group.name}</h2>
                            <span class="badge {getPriorityClass(group.priority)}">
                                {group.priorityDisplay}
                            </span>
                        </div>

                        <!-- Guest Group Info -->
                        <div class="space-y-2 text-sm">
                            <div class="flex items-center gap-2">
                                <span class="icon-[lucide--users] size-4"></span>
                                <span>
                                    {#if group.associatedWithFirstName}{group.associatedWithFirstName}'s&nbsp;
                                    {/if}
                                    {group.relationshipDisplay}
                                </span>
                            </div>
                            <div class="flex items-center gap-2">
                                <span class="icon-[lucide--user] size-4"></span>
                                <span>
                                    {group.groupCount}
                                    {group.groupCount === 1 ? "guest" : "guests"}
                                </span>
                            </div>
                        </div>

                        <div class="divider my-2"></div>

                        <!-- RSVP Progress -->
                        <div class="space-y-2">
                            <div class="flex items-center justify-between text-sm">
                                <span class="font-semibold">RSVP Progress</span>
                                <span>
                                    {group.groupAttendingCount} / {group.groupInvitedCount}
                                </span>
                            </div>

                            <!-- Progress Bar -->
                            <div class="w-full bg-base-100 rounded-full h-2">
                                <div class="bg-error h-2 rounded-full transition-all" style="width: {rsvpProgress}%">
                                </div>
                            </div>

                            <!-- RSVP Stats -->
                            <div class="flex items-center gap-4 text-xs">
                                <div class="flex items-center gap-1">
                                    <span class="icon-[lucide--check-circle] size-4 text-success"></span>
                                    <span>{group.groupAttendingCount} attending</span>
                                </div>
                                <div class="flex items-center gap-1">
                                    <span class="icon-[lucide--x-circle] size-4 text-error"></span>
                                    <span>{group.groupDeclinedCount} declined</span>
                                </div>
                            </div>
                        </div>

                        <!-- Additional Stats -->
                        {#if group.groupVip > 0 || group.groupOvernight > 0}
                            <div class="divider my-2"></div>
                            <div class="flex items-center gap-3 text-xs">
                                {#if group.groupVip > 0}
                                    <div class="badge badge-sm badge-accent">
                                        <span class="icon-[lucide--star] size-3"></span>
                                        <span class="ml-1">{group.groupVip} {data.configData?.vipGroupLabel}</span>
                                    </div>
                                {/if}
                                {#if group.groupOvernight > 0}
                                    <div class="badge badge-sm badge-info">
                                        <span class="icon-[lucide--home] size-3"></span>
                                        <span class="ml-1"
                                            >{group.groupOvernight} {data.configData?.accommodationGroupLabel}</span>
                                    </div>
                                {/if}
                            </div>
                        {/if}
                        <div class="card-actions justify-end mt-4">
                            <ViewDetails href="/settings/guest_list/{group.id}" label="View Details" />
                        </div>
                    </div>
                </a>
            {/each}
        </div>
    {/if}
</ProtectedPageShell>
