<!-- src/routes/planning/guest_list/+page.svelte -->
<script lang="ts">
    import { enhance } from "$app/forms";
    import Stats from "$lib/components/Stats.svelte";
    import CreateObject from "$lib/components/buttons/CreateObject.svelte";
    import ViewDetails from "$lib/components/buttons/ViewDetails.svelte";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { PageData, iStat, ActionData } from "./$types";

    const { data, form }: { data: PageData; form: ActionData } = $props();
    const relativeCrumbs = [{ title: "Guest List" }];

    let isGeneratingMissing = $state(false);
    let isRegeneratingAll = $state(false);

    // QR Code Modal State
    let showQrModal = $state(false);
    let selectedQrCodeUrl = $state<string | null>(null);
    let selectedQrCodeName = $state<string>("");
    let linkCopied = $state(false);

    function openQrModal(url: string, name: string) {
        selectedQrCodeUrl = url;
        selectedQrCodeName = name;
        showQrModal = true;
    }

    function closeQrModal() {
        showQrModal = false;
        selectedQrCodeUrl = null;
        selectedQrCodeName = "";
        linkCopied = false;
    }

    function downloadQrCode() {
        if (!selectedQrCodeUrl) return;
        const a = document.createElement("a");
        a.href = selectedQrCodeUrl;
        a.download = `qr_code_${selectedQrCodeName.replace(/[^a-z0-9]/gi, "_").toLowerCase()}.png`;
        a.target = "_blank";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }

    async function copyQrLink() {
        if (!selectedQrCodeUrl) return;

        try {
            await navigator.clipboard.writeText(selectedQrCodeUrl);
            linkCopied = true;
            setTimeout(() => {
                linkCopied = false;
            }, 3000);
        } catch (error) {
            console.error("Error copying link:", error);
            alert("Failed to copy link");
        }
    }

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
        data.guestGroups
            .filter((group) => {
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
            })
            // sort by priority descending, then name ascending
            .sort((a, b) => {
                if (b.priority !== a.priority) {
                    return (b.priority || 0) - (a.priority || 0);
                }
                return a.name.localeCompare(b.name);
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

    const guestStats: iStat[] = [
        {
            title: "Guest Groups",
            value: filteredGuestGroups.length,
            description: `of ${data.count} total`,
            icon: "users",
        },
        {
            title: "Guests",
            value: filteredGuestGroups.reduce((sum, group) => sum + group.groupCount, 0),
            description: `of ${data.guestGroups.reduce((sum, group) => sum + group.groupCount, 0)} total`,
            icon: "user",
        },
    ];
    const inviteStats: iStat[] = [
        {
            title: "Invited",
            value: filteredGuestGroups.reduce((sum, group) => sum + group.groupInvitedCount, 0),
            description: `of ${data.guestGroups.reduce((sum, group) => sum + group.groupInvitedCount, 0)} total`,
            icon: "mail",
        },
        {
            title: "Attending",
            value: filteredGuestGroups.reduce((sum, group) => sum + group.groupAttendingCount, 0),
            description: `of ${data.guestGroups.reduce((sum, group) => sum + group.groupAttendingCount, 0)} total`,
            icon: "check-circle",
        },
    ];
</script>

<ProtectedPageShell {relativeCrumbs} {form}>
    <ProtectedPageHeader
        title="Guest List"
        description="Manage your wedding guest groups and RSVPs"
        showButtons={false}>
        <div class="w-full flex justify-start">
            <div class="flex flex-col md:flex-row gap-6 mb-8">
                <div class="config-card w-full md:w-96" id="filter-panel">
                    <div class="config-card-body">
                        <div class="flex items-center justify-between mb-4">
                            <h3 class="text-lg font-semibold">Filters</h3>
                            <button onclick={clearFilters} class="btn btn-error btn-sm">
                                <span class="icon-[lucide--x] size-4"></span>
                                Clear All
                            </button>
                        </div>
                        <div class="grid grid-cols-1 gap-4">
                            <div class="form-control">
                                <label class="label" for="name-filter">
                                    <span class="config-card-field-name">Name</span>
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
                                    <span class="config-card-field-name">Priority</span>
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
                                    <span class="config-card-field-name">Relationship</span>
                                </label>
                                <select
                                    id="relationship-filter"
                                    class="select select-bordered"
                                    bind:value={relationshipFilter}>
                                    <option value="">All Relationships</option>
                                    {#each availableRelationships as { value, label } (value)}
                                        <option {value}>{label}</option>
                                    {/each}
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="flex flex-col items-center gap-6" id="stats-overview">
                    <Stats objects={guestStats} />
                    <Stats objects={inviteStats} />
                </div>
                <div class="flex flex-row md:flex-col gap-4">
                    <CreateObject href="/planning/guest_list/new" label="New Guest Group" />
                    <a href="/planning/guest/all" class="btn btn-accent gap-2">
                        <span class="icon-[lucide--users] size-5"></span>
                        View All Guests
                    </a>
                    <a href="/api/guestlist/export_address_csv" class="btn btn-secondary gap-2">
                        <span class="icon-[lucide--download] size-5"></span>
                        Export Address Data
                    </a>

                    <!-- QR Code Generation Actions -->
                    <div class="divider"></div>
                    <button
                        onclick={() => openQrModal(data.configData.rsvpQrCodeUrl as string, "General RSVP")}
                        class="btn btn-accent gap-2">
                        <span class="icon-[lucide--qr-code] size-5"></span>
                        View Universal RSVP QR
                    </button>
                    <form
                        method="POST"
                        action="?/generateMissingQrCodes"
                        use:enhance={() => {
                            isGeneratingMissing = true;
                            return async ({ update }) => {
                                await update();
                                isGeneratingMissing = false;
                            };
                        }}>
                        <button type="submit" class="btn btn-info gap-2 w-full" disabled={isGeneratingMissing}>
                            <span class="icon-[lucide--qr-code] size-5"></span>
                            {isGeneratingMissing ? "Generating..." : "Generate Missing QR Codes"}
                        </button>
                    </form>

                    <form
                        method="POST"
                        action="?/regenerateAllQrCodes"
                        use:enhance={() => {
                            isRegeneratingAll = true;
                            return async ({ update }) => {
                                await update();
                                isRegeneratingAll = false;
                            };
                        }}>
                        <button type="submit" class="btn btn-warning gap-2 w-full" disabled={isRegeneratingAll}>
                            <span class="icon-[lucide--refresh-cw] size-5"></span>
                            {isRegeneratingAll ? "Regenerating..." : "Regenerate All QR Codes"}
                        </button>
                    </form>
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
                <div
                    class="list-card cursor-pointer"
                    onclick={() => (window.location.href = `/planning/guest_list/${group.id}`)}>
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
                        <div class="card-actions justify-between mt-4">
                            {#if group.hasQrCode && group.qrCodeUrl}
                                <button
                                    onclick={(e) => {
                                        e.stopPropagation();
                                        openQrModal(group.qrCodeUrl, group.name);
                                    }}
                                    class="btn btn-sm btn-accent gap-1">
                                    <span class="icon-[lucide--qr-code] size-4"></span>
                                    QR Code
                                </button>
                            {/if}
                            <ViewDetails href="/planning/guest_list/{group.id}" label="View Details" size="sm" />
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</ProtectedPageShell>

<!-- QR Code Modal -->
{#if showQrModal}
    <div class="modal modal-open">
        <div class="modal-box max-w-md">
            <h3 class="font-bold text-lg mb-4 text-accent">QR Code - {selectedQrCodeName}</h3>

            {#if selectedQrCodeUrl}
                <div class="flex justify-center mb-6 p-4 rounded-lg">
                    <img
                        src={selectedQrCodeUrl}
                        alt="QR Code for {selectedQrCodeName}"
                        class="w-64 h-64 object-contain" />
                </div>

                <div class="flex gap-2 justify-center">
                    <button onclick={downloadQrCode} class="btn btn-accent gap-2">
                        <span class="icon-[lucide--download] size-5"></span>
                        Download
                    </button>
                    <button onclick={copyQrLink} class="btn btn-secondary gap-2">
                        <span class="icon-[lucide--copy] size-5"></span>
                        Copy Link
                    </button>
                </div>

                {#if linkCopied}
                    <div class="flex justify-center mt-4">
                        <div class="badge badge-success gap-2">
                            <span class="icon-[lucide--check] size-4"></span>
                            Link copied to clipboard!
                        </div>
                    </div>
                {/if}
            {/if}

            <div class="modal-action">
                <button onclick={closeQrModal} class="btn btn-error">Close</button>
            </div>
        </div>
        <div class="modal-backdrop" onclick={closeQrModal}></div>
    </div>
{/if}
