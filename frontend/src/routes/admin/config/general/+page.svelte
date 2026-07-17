<script lang="ts">
    import { enhance } from "$app/forms";
    import SectionStatus from "$lib/components/SectionStatus.svelte";
    import type { SubmitFunction } from "@sveltejs/kit";
    import type { PageData } from "./$types";
    import type { Feature } from "./proxy+page.server";

    const { data }: { data: PageData } = $props();

    const formatValue = (value: null | boolean | Date | string | number | undefined): string => {
        if (value === null || value === undefined) return "Not set";
        if (typeof value === "boolean") return value ? "Yes" : "No";
        if (value instanceof Date) {
            const year = value.getUTCFullYear();
            const month = String(value.getUTCMonth() + 1).padStart(2, "0");
            const day = String(value.getUTCDate()).padStart(2, "0");
            return `${month}/${day}/${year}`;
        }
        return String(value);
    };

    // reflect local changes
    let features = $derived(data.features);
    // The factory function returns the standard SvelteKit SubmitFunction type
    const handleToggle = (name: string, field: "enabled" | "visible", currentValue: boolean): SubmitFunction => {
        // 1. This block runs IMMEDIATELY when the user clicks the checkbox (On Submit)
        return ({ cancel }) => {
            // Apply the Optimistic UI update right away
            features = features.map((s) => {
                if (s.name === name) {
                    return { ...s, [field + "Status"]: !currentValue };
                }
                return s;
            });

            // 2. Return an async callback that runs AFTER the backend server responds
            return async ({ result, update }) => {
                if (result.type === "success") {
                    // Automatically syncs and refreshes the data prop from load()
                    await update({ invalidateAll: true });
                } else {
                    console.error(`Backend write failed. Rolling back toggle.`);
                    // Rollback to the true original state if the database write failed
                    features = features.map((s) => {
                        if (s.name === name) {
                            return { ...s, [field + "Status"]: currentValue };
                        }
                        return s;
                    });
                }
            };
        };
    };
</script>

<div class="config-card">
    <div class="config-card-body">
        <div class="flex items-center justify-between gap-2 mb-4">
            <h2 class="config-card-title text-xl">General</h2>
            <a href="/admin/config/edit#general-section" class="btn btn-sm btn-accent">
                <span class="icon-[lucide--square-pen] size-4"></span>
                Edit General
            </a>
        </div>
        <div class="divider divider-accent">What Guests See</div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {#each features.filter((f) => f.category === "see") as item (item.name)}
                <div>
                    <div class="config-card-field-name">{item.name}</div>
                    <div class="flex items-center justify-around gap-3">
                        <form
                            method="POST"
                            action="?/updateStatus"
                            use:enhance={handleToggle(item.name, "enabled", item.enabledStatus)}
                            class="flex items-center justify-center gap-3">
                            <input type="hidden" name="name" value={item.name} />
                            <input type="hidden" name="type" value="enabled" />
                            <input type="hidden" name="value" value={String(!item.enabledStatus)} />
                            <div class="flex items-center justify-center gap-3">
                                {#if item.enabledStatus}
                                    <span class="badge badge-success badge-lg">{item.enabledLabelTrue}</span>
                                {:else}
                                    <span class="badge badge-warning badge-lg">{item.enabledLabelFalse}</span>
                                {/if}
                                <input
                                    type="checkbox"
                                    class="toggle toggle-success toggle-sm"
                                    checked={item.enabledStatus}
                                    onchange={(e) => e.currentTarget.form?.requestSubmit()} />
                            </div>
                        </form>
                        <form
                            method="POST"
                            action="?/updateStatus"
                            use:enhance={handleToggle(item.name, "visible", item.visibleStatus)}
                            class="flex items-center justify-center gap-3">
                            <input type="hidden" name="name" value={item.name} />
                            <input type="hidden" name="type" value="visible" />
                            <input type="hidden" name="value" value={String(!item.visibleStatus)} />
                            <div class="flex items-center justify-center gap-3">
                                {#if item.visibleStatus}
                                    <span class="badge badge-success badge-lg">{item.visibleLabelTrue}</span>
                                {:else}
                                    <span class="badge badge-warning badge-lg">
                                        {item.visibleLabelFalse}
                                    </span>
                                {/if}
                                <input
                                    type="checkbox"
                                    class="checkbox checkbox-info checkbox-sm rounded"
                                    checked={item.visibleStatus}
                                    onchange={(e) => e.currentTarget.form?.requestSubmit()} />
                            </div>
                        </form>
                    </div>
                </div>
            {/each}
        </div>

        <div class="divider divider-accent">What Guests Do</div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div>
                <div class="config-card-field-name">RSVP</div>
                <div class="config-card-field-value">
                    <SectionStatus
                        enabled={data.configData?.enableRsvp}
                        visible={data.configData?.allowRsvp}
                        visibleTrueLabel="Active"
                        visibleFalseLabel="Not Active" />
                </div>
            </div>
            <div>
                <div class="config-card-field-name">Upload Photos</div>
                <SectionStatus
                    enabled={data.configData?.enableUploadPhotos}
                    visible={data.configData?.allowPhotos}
                    visibleTrueLabel="Active"
                    visibleFalseLabel="Not Active" />
            </div>
        </div>
        <div class="divider divider-accent">Wedding Details</div>
        <div>
            <div class="config-card-field-name">Wedding Date</div>
            <div class="config-card-field-value">{formatValue(data.configData?.weddingDate)}</div>
        </div>
    </div>
</div>
