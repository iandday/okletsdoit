<script lang="ts">
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import { formatDisplayDateTime } from "$lib/utils/formatters";
    import { dndzone } from "svelte-dnd-action";
    import { flip } from "svelte/animate";
    import type { PageData } from "./$types";

    const { data }: { data: PageData } = $props();
    const relativeCrumbs = [{ title: "Timeline", href: "/planning/timeline" }];

    // State for drag and drop
    let items = $state(data.timelines.map((t) => ({ ...t })));

    // Modal state
    let createModalOpen = $state(false);
    let editModalOpen = $state(false);
    let deleteModalOpen = $state(false);
    let selectedItem = $state<any>(null);
    let errorToast = $state("");
    let errorToastTimer: ReturnType<typeof setTimeout> | undefined;
    let editForm = $state({
        name: "",
        description: "",
        start: "",
        end: "",
    });
    let createForm = $state({
        name: "",
        description: "",
        start: "",
        end: "",
    });

    const flipDurationMs = 200;
    let dragStartOrder: string[] = [];
    const browserTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;

    type TimelineDateValue = string | Date;

    function showErrorToast(message: string) {
        errorToast = message;
        if (errorToastTimer) clearTimeout(errorToastTimer);
        errorToastTimer = setTimeout(() => {
            errorToast = "";
        }, 3500);
    }

    function handleDndConsider(e: CustomEvent) {
        if (e.detail.info.trigger === "dragStarted") {
            // Store the original order when drag starts
            dragStartOrder = items.map((item) => item.id);
        }
        items = e.detail.items;
    }

    async function handleDndFinalize(e: CustomEvent) {
        const newItems = e.detail.items;

        // Update order values for all items based on their new positions
        const updates: Promise<Response>[] = [];

        newItems.forEach((item: any, index: number) => {
            if (item.order !== index) {
                const formData = new FormData();
                formData.append("id", item.id);
                formData.append("field", "order");
                formData.append("value", index.toString());

                updates.push(
                    fetch("?/update", {
                        method: "POST",
                        body: formData,
                    }),
                );

                // Update local state immediately
                item.order = index;
            }
        });

        // Wait for all updates to complete and surface any persistence failures.
        const results = await Promise.all(updates);
        if (results.some((result) => !result.ok)) {
            showErrorToast("Failed to persist one or more timeline reorder updates.");
        }

        items = newItems;
        dragStartOrder = [];
    }

    function localDateTimeToUtcIso(dateTimeLocalValue: string): string {
        if (!dateTimeLocalValue) return "";
        const localDate = new Date(dateTimeLocalValue);

        if (Number.isNaN(localDate.getTime())) {
            return "";
        }

        return localDate.toISOString();
    }

    function utcToDateTimeLocalInput(dateValue: string | Date | null | undefined): string {
        if (!dateValue) return "";

        const date = dateValue instanceof Date ? dateValue : new Date(dateValue);
        if (Number.isNaN(date.getTime())) {
            return "";
        }

        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, "0");
        const day = String(date.getDate()).padStart(2, "0");
        const hours = String(date.getHours()).padStart(2, "0");
        const minutes = String(date.getMinutes()).padStart(2, "0");
        return `${year}-${month}-${day}T${hours}:${minutes}`;
    }

    async function reloadTimelineItems() {
        try {
            const response = await fetch("/api/core/timelines", {
                cache: "no-store",
            });
            if (!response.ok) return;

            const payload = await response.json();
            const nextItems = Array.isArray(payload) ? payload : payload?.items;

            if (Array.isArray(nextItems)) {
                items = nextItems.map((item) => ({ ...item }));
            }
        } catch (error) {
            console.error("Failed to reload timelines:", error);
        }
    }

    async function toggleStatus(item: any, field: "published" | "confirmed") {
        const formData = new FormData();
        formData.append("id", item.id);
        formData.append("field", field);
        formData.append("value", (!item[field]).toString());

        const response = await fetch("?/update", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            // Update local state
            const idx = items.findIndex((i) => i.id === item.id);
            if (idx !== -1) {
                items[idx][field] = !items[idx][field];
            }
        } else {
            showErrorToast("Failed to update timeline status.");
        }
    }

    function openCreateModal() {
        createForm = {
            name: "",
            description: "",
            start: "",
            end: "",
        };
        createModalOpen = true;
    }

    function openEditModal(item: any) {
        selectedItem = item;

        editForm = {
            name: item.name || "",
            description: item.description || "",
            start: utcToDateTimeLocalInput(item.start),
            end: utcToDateTimeLocalInput(item.end),
        };
        editModalOpen = true;
    }

    function openDeleteModal(item: any) {
        selectedItem = item;
        deleteModalOpen = true;
    }

    async function createEvent() {
        if (!createForm.name || !createForm.start) {
            showErrorToast("Name and start time are required.");
            return;
        }

        const startUtc = localDateTimeToUtcIso(createForm.start);
        const endUtc = localDateTimeToUtcIso(createForm.end);

        if (!startUtc) {
            showErrorToast(`Invalid start time for browser timezone: ${browserTimeZone}`);
            return;
        }

        const formData = new FormData();
        formData.append("name", createForm.name);
        formData.append("description", createForm.description);
        formData.append("start", startUtc);
        formData.append("end", endUtc);

        try {
            const response = await fetch("?/create", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                showErrorToast("Failed to create timeline event.");
                return;
            }

            const result = await response.json();
            const created = result?.data?.created ?? result?.created;

            if (created) {
                items = [created, ...items];
            }

            // Always sync from server so the list reflects the canonical persisted state.
            await reloadTimelineItems();
            createModalOpen = false;
        } catch (error) {
            console.error("Failed to create timeline event:", error);
            showErrorToast("Failed to create timeline event.");
        }
    }

    async function saveEdit() {
        if (!selectedItem) return;

        const startUtc = localDateTimeToUtcIso(editForm.start);
        const endUtc = localDateTimeToUtcIso(editForm.end);

        if (!startUtc) {
            showErrorToast(`Invalid start time for browser timezone: ${browserTimeZone}`);
            return;
        }

        const formData = new FormData();
        formData.append("id", selectedItem.id);
        formData.append("name", editForm.name);
        formData.append("description", editForm.description);
        formData.append("start", startUtc);
        formData.append("end", endUtc);

        const response = await fetch("?/update", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            // Pull canonical values from server to avoid any local timezone interpretation drift.
            await reloadTimelineItems();
            editModalOpen = false;
        } else {
            showErrorToast("Failed to save timeline changes.");
        }
    }

    async function confirmDelete() {
        if (!selectedItem) return;

        const formData = new FormData();
        formData.append("id", selectedItem.id);

        const response = await fetch("?/delete", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            items = items.filter((i) => i.id !== selectedItem.id);
            deleteModalOpen = false;
        } else {
            showErrorToast("Failed to delete timeline event.");
        }
    }
</script>

{#if errorToast}
    <div class="toast toast-top toast-end z-50">
        <div class="alert alert-error">
            <span class="icon-[lucide--alert-circle] size-4"></span>
            <span>{errorToast}</span>
        </div>
    </div>
{/if}

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader
        title="Timeline"
        description="Create and organize events for your wedding day. Use the drag and drop button on the left to rearrange
                the order of events as you plan. You can specify start and end times, add descriptions. Toggle between
                Private and Public to control if the event is viewable to everyone in the Venue page. Toggle between
                Confirmed and Tentative status to keep track of which events are finalized and which are still in
                planning.">
        <div class="flex flex-row sm:flex-col sm:flex-row items-center justify-center gap-4 mb-8">
            <button class="btn btn-success" onclick={openCreateModal}>New Event</button>
            <a href="/planning/preview/venue" class="btn btn-accent" target="_blank">Preview Venue Page</a>
        </div>
    </ProtectedPageHeader>

    {#if items.length === 0}
        <!-- Empty State -->
        <div class="card bg-base-100 border border-base-300 shadow-lg">
            <div class="card-body items-center text-center py-16">
                <span class="icon-[lucide--calendar-clock] size-16 text-base-content/30 mb-4"></span>
                <h3 class="text-xl font-semibold text-base-content mb-2">No timeline events yet</h3>
                <p class="text-base-content/70 mb-6 max-w-md">
                    Create your first timeline event to start planning your wedding day schedule.
                </p>
                <button class="btn btn-success gap-2" onclick={openCreateModal}>
                    <span class="icon-[lucide--plus] size-5"></span>
                    Create First Event
                </button>
            </div>
        </div>
    {:else}
        <div
            class="space-y-2"
            use:dndzone={{ items, flipDurationMs, type: "timeline" }}
            onconsider={handleDndConsider}
            onfinalize={handleDndFinalize}>
            {#each items as item (item.id)}
                <div class="list-card" animate:flip={{ duration: flipDurationMs }}>
                    <div class="list-card-body p-4">
                        <div class="flex items-start gap-4">
                            <!-- Drag Handle -->
                            <button
                                class="cursor-grab active:cursor-grabbing bg-accent p-2 hover:bg-base-100 rounded"
                                aria-label="Drag to reorder">
                                <span class="icon-[lucide--grip-vertical] size-4"></span>
                            </button>

                            <!-- Event Details -->
                            <div class="flex-1 min-w-0">
                                <div class="flex items-start justify-between gap-4 mb-2">
                                    <button onclick={() => openEditModal(item)} class="list-card-title">
                                        {item.name}
                                    </button>

                                    <div class="flex items-center gap-2 flex-shrink-0">
                                        <!-- Published Badge -->
                                        <button
                                            onclick={() => toggleStatus(item, "published")}
                                            class="badge badge-sm gap-1 {item.published
                                                ? 'badge-success'
                                                : 'badge-error'} hover:scale-105 transition-transform"
                                            title="Toggle published status">
                                            <span class="icon-[lucide--{item.published ? 'eye' : 'eye-off'}] size-3"
                                            ></span>
                                            {item.published ? "Public" : "Private"}
                                        </button>

                                        <!-- Confirmed Badge -->
                                        <button
                                            onclick={() => toggleStatus(item, "confirmed")}
                                            class="badge badge-sm gap-1 {item.confirmed
                                                ? 'badge-info'
                                                : 'badge-error'} hover:scale-105 transition-transform"
                                            title="Toggle confirmed status">
                                            <span
                                                class="icon-[lucide--{item.confirmed
                                                    ? 'check-circle'
                                                    : 'circle'}] size-3"></span>
                                            {item.confirmed ? "Confirmed" : "Tentative"}
                                        </button>

                                        <!-- Delete Button -->
                                        <button
                                            onclick={() => openDeleteModal(item)}
                                            class="btn-error btn-xs btn-circle"
                                            aria-label="Delete event">
                                            <span class="icon-[lucide--trash-2] size-4 text-error"></span>
                                        </button>
                                    </div>
                                </div>

                                <!-- Time Display -->
                                <div class="flex items-center gap-4 text-sm mb-2">
                                    <button
                                        onclick={() => openEditModal(item)}
                                        class="flex items-center gap-1 hover:text-accent transition-colors">
                                        <span class="icon-[lucide--clock] size-4"></span>
                                        <span>{formatDisplayDateTime(item.start)}</span>
                                    </button>

                                    {#if item.end}
                                        <span>→</span>
                                        <button
                                            onclick={() => openEditModal(item)}
                                            class="flex items-center gap-1 hover:text-accent transition-colors">
                                            <span>{formatDisplayDateTime(item.end)}</span>
                                        </button>
                                    {:else}
                                        <button
                                            onclick={() => openEditModal(item)}
                                            class="hover:text-accent transition-colors">
                                            + Add end time
                                        </button>
                                    {/if}
                                </div>

                                <!-- Description -->
                                {#if item.description}
                                    <button
                                        onclick={() => openEditModal(item)}
                                        class="text-sm hover:text-accent transition-colors text-left w-full">
                                        {item.description}
                                    </button>
                                {:else}
                                    <button
                                        onclick={() => openEditModal(item)}
                                        class="text-sm italic hover:text-accent transition-colors">
                                        + Add description
                                    </button>
                                {/if}
                            </div>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</ProtectedPageShell>

<!-- Create Modal -->
{#if createModalOpen}
    <dialog class="modal modal-open">
        <div class="modal-box bg-base-200">
            <div class="edit-card">
                <div class="edit-card-title">Create Timeline Event</div>

                <div class="space-y-4">
                    <div>
                        <label class="edit-card-field-name">Event Name</label>
                        <input
                            type="text"
                            bind:value={createForm.name}
                            class="edit-card-field-input"
                            placeholder="Event name..." />
                    </div>

                    <div>
                        <label class="edit-card-field-name">Start Time</label>
                        <input type="datetime-local" bind:value={createForm.start} class="edit-card-field-date" />
                    </div>

                    <div>
                        <label class="edit-card-field-name">End Time</label>
                        <input type="datetime-local" bind:value={createForm.end} class="edit-card-field-date" />
                    </div>

                    <div>
                        <label class="edit-card-field-name">Description</label>
                        <textarea
                            bind:value={createForm.description}
                            class="edit-card-field-textarea"
                            placeholder="Event description..."></textarea>
                    </div>
                </div>

                <div class="modal-action">
                    <button onclick={() => (createModalOpen = false)} class="btn btn-ghost">Cancel</button>
                    <button onclick={createEvent} class="btn btn-primary">Create Event</button>
                </div>
            </div>
            <button onclick={() => (createModalOpen = false)} class="modal-backdrop" aria-label="Close modal"></button>
        </div>
    </dialog>
{/if}

<!-- Edit Modal -->
{#if editModalOpen}
    <dialog class="modal modal-open">
        <div class="modal-box bg-base-200">
            <div class="edit-card">
                <div class="edit-card-title">Edit Timeline Event</div>

                <div class="space-y-4">
                    <div>
                        <label class="edit-card-field-name">Event Name</label>
                        <input
                            type="text"
                            bind:value={editForm.name}
                            class="edit-card-field-input"
                            placeholder="Event name..." />
                    </div>

                    <div>
                        <label class="edit-card-field-name">Start Time</label>
                        <input type="datetime-local" bind:value={editForm.start} class="edit-card-field-date" />
                    </div>

                    <div>
                        <label class="edit-card-field-name">End Time</label>
                        <input type="datetime-local" bind:value={editForm.end} class="edit-card-field-date" />
                    </div>

                    <div>
                        <label class="edit-card-field-name">Description</label>
                        <textarea
                            bind:value={editForm.description}
                            class="edit-card-field-textarea"
                            placeholder="Event description..."></textarea>
                    </div>
                </div>

                <div class="modal-action">
                    <button onclick={() => (editModalOpen = false)} class="btn btn-ghost">Cancel</button>
                    <button onclick={saveEdit} class="btn btn-primary">Save Changes</button>
                </div>
            </div>
            <button onclick={() => (editModalOpen = false)} class="modal-backdrop" aria-label="Close modal"></button>
        </div>
    </dialog>
{/if}

<!-- Delete Confirmation Modal -->
{#if deleteModalOpen}
    <dialog class="modal modal-open">
        <div class="modal-box bg-base-200 text-primary-content">
            <h3 class="font-bold text-lg mb-4">Delete Timeline Event</h3>
            <p class="mb-4">Are you sure you want to delete "{selectedItem?.name}"? This action cannot be undone.</p>

            <div class="modal-action">
                <button onclick={() => (deleteModalOpen = false)} class="btn btn-accent">Cancel</button>
                <button onclick={confirmDelete} class="btn btn-error">Delete</button>
            </div>
        </div>
        <button onclick={() => (deleteModalOpen = false)} class="modal-backdrop" aria-label="Close modal"></button>
    </dialog>
{/if}
