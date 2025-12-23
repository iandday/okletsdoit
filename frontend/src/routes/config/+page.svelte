<script lang="ts">
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";

    const { data } = $props();

    const formatLabel = (key: string): string => {
        return key
            .replace(/([A-Z])/g, " $1")
            .replace(/^./, (str) => str.toUpperCase())
            .trim();
    };

    const formatValue = (value: any): string => {
        if (value === null || value === undefined) {
            return "Not set";
        }
        if (typeof value === "boolean") {
            return value ? "Yes" : "No";
        }
        if (value instanceof Date) {
            return value.toLocaleDateString();
        }
        return String(value);
    };

    const sections = {
        general: {
            title: "General Settings",
            fields: ["defaultDataLoaded", "allowRsvp", "allowPhotos", "showFaq", "weddingDate"],
        },
        rsvpDates: {
            title: "RSVP Dates",
            fields: ["rsvpStartDate", "rsvpEndDate"],
        },
        rsvpButtons: {
            title: "RSVP Buttons",
            fields: ["rsvpAcceptButton", "rsvpDeclineButton"],
        },
        rsvpLabels: {
            title: "RSVP Labels",
            fields: [
                "rsvpAttendingLabel",
                "rsvpAccommodationLabel",
                "rsvpVipLabel",
                "standardGroupLabel",
                "vipGroupLabel",
                "rsvpEmailUpdateLabel",
            ],
        },
        rsvpMessages: {
            title: "RSVP Messages",
            fields: [
                "rsvpAcceptIntro",
                "rsvpAcceptSuccessMessage",
                "rsvpDeclineSuccessMessage",
                "rsvpAccommodationIntro",
                "rsvpVipIntro",
                "rsvpSuccessHeadline",
            ],
        },
        rsvpOptions: {
            title: "RSVP Display Options",
            fields: ["rsvpShowAccommodationIntro", "rsvpShowVipIntro", "rsvpEnableEmailUpdates"],
        },
    };
</script>

<div>
    <ProtectedPageShell
        ><div class="container mx-auto p-4 max-w-6xl">
            <div class="flex justify-between items-center mb-6">
                <h1 class="text-3xl font-bold">Wedding Configuration</h1>
            </div>

            {#if data.configData}
                <div class="grid gap-4">
                    {#each Object.entries(sections) as [key, section]}
                        <div class="config-card">
                            <div class="card-body">
                                <h2 class="card-title text-xl mb-4">{section.title}</h2>
                                <div class="list">
                                    {#each section.fields as field}
                                        {@const value = data.configData[field]}
                                        <div class="list-row">
                                            <span class="font-semibold text-base-content/70">{formatLabel(field)}</span>
                                            <span class="text-base-content">
                                                {#if typeof value === "boolean"}
                                                    <span class="badge {value ? 'badge-success' : 'badge-ghost'}">
                                                        {formatValue(value)}
                                                    </span>
                                                {:else if value === null || value === undefined}
                                                    <span class="badge badge-ghost">{formatValue(value)}</span>
                                                {:else if field.includes("Date")}
                                                    <span class="badge badge-neutral">{formatValue(value)}</span>
                                                {:else if field.includes("Message") || field.includes("Intro") || field.includes("Headline")}
                                                    <div class="text-sm max-w-prose">{formatValue(value)}</div>
                                                {:else}
                                                    {formatValue(value)}
                                                {/if}
                                            </span>
                                        </div>
                                    {/each}
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>
            {:else}
                <div class="alert alert-info">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        class="stroke-current shrink-0 w-6 h-6">
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <span>No configuration data available.</span>
                </div>
            {/if}
        </div></ProtectedPageShell>
</div>
