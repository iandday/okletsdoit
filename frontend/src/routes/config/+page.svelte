<script lang="ts">
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";

    const { data } = $props();

    const formatLabel = (key: string): string => {
        return key
            .replace(/([A-Z])/g, " $1")
            .replace(/^./, (str) => str.toUpperCase())
            .trim();
    };

    const formatValue = (value: null | boolean | Date | string | number | undefined): string => {
        if (value === null || value === undefined) {
            return "Not set";
        }
        if (typeof value === "boolean") {
            return value ? "Yes" : "No";
        }
        if (value instanceof Date) {
            // Format date without timezone conversion to avoid off-by-one day issues
            const year = value.getUTCFullYear();
            const month = String(value.getUTCMonth() + 1).padStart(2, "0");
            const day = String(value.getUTCDate()).padStart(2, "0");
            return `${month}/${day}/${year}`;
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
                <a href="/config/edit" class="btn btn-primary">Edit Settings</a>
            </div>

            {#if data.configData}
                <div class="grid gap-4">
                    {#each Object.entries(sections) as [key, section], index (key)}
                        <div class="config-card">
                            <div class="config-card-body">
                                <h2 class="config-card-title text-xl mb-4">{section.title}</h2>
                                <div class="grid grid-cols-2 gap-4 mt-4">
                                    {#each section.fields as field, index (index)}
                                        {@const value = data.configData[field as keyof typeof data.configData]}
                                        <div class="flex flex-col">
                                            <div class="config-card-field-name">{formatLabel(field)}</div>
                                            <div class="config-card-field-value">
                                                {#if field.includes("Message") || field.includes("Intro") || field.includes("Headline")}
                                                    <div class="text-sm max-w-prose">{formatValue(value)}</div>
                                                {:else}
                                                    {formatValue(value)}
                                                {/if}
                                            </div>
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
