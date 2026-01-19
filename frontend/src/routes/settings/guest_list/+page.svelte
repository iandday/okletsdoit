<!-- src/routes/settings/guest_list/+page.svelte -->
<script lang="ts">
    import CreateObject from "$lib/components/buttons/CreateObject.svelte";
    import ViewDetails from "$lib/components/buttons/ViewDetails.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();
    const relativeCrumbs = [{ title: "Guest List" }];

    function getRsvpProgress(group: any): number {
        if (group.groupInvitedCount === 0) return 0;
        return Math.round((group.groupAttendingCount / group.groupInvitedCount) * 100);
    }

    function getPriorityClass(priority: number): string {
        switch (priority) {
            case 3:
                return "badge-error";
            case 2:
                return "badge-warning";
            case 1:
                return "badge-info";
            default:
                return "badge-ghost";
        }
    }
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader title="Guest List" description="Manage your wedding guest groups and RSVPs">
        <div class="stats shadow mt-8 w-full">
            <div class="stat">
                <div class="stat-figure text-primary">
                    <span class="icon-[lucide--users] size-8"></span>
                </div>
                <div class="stat-title">Total Guest Groups</div>
                <div class="stat-value text-primary">{data.count}</div>
            </div>

            <div class="stat">
                <div class="stat-figure text-secondary">
                    <span class="icon-[lucide--user] size-8"></span>
                </div>
                <div class="stat-title">Total Guests</div>
                <div class="stat-value text-secondary">
                    {data.guestGroups.reduce((sum, group) => sum + group.groupCount, 0)}
                </div>
            </div>

            <div class="stat">
                <div class="stat-figure text-success">
                    <span class="icon-[lucide--check-circle] size-8"></span>
                </div>
                <div class="stat-title">Total Attending</div>
                <div class="stat-value text-success">
                    {data.guestGroups.reduce((sum, group) => sum + group.groupAttendingCount, 0)}
                </div>
            </div>

            <div class="stat">
                <div class="stat-figure text-info">
                    <span class="icon-[lucide--mail] size-8"></span>
                </div>
                <div class="stat-title">Total Invited</div>
                <div class="stat-value text-info">
                    {data.guestGroups.reduce((sum, group) => sum + group.groupInvitedCount, 0)}
                </div>
            </div>
        </div>
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-8">
            <CreateObject href="/settings/guest_list/new" label="New Guest Group" />
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
    {:else}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each data.guestGroups as group}
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
                                <span>{group.relationshipDisplay}</span>
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
