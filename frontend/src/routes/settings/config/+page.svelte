<script lang="ts">
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";

    const { data } = $props();

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

    type iSection = {
        title: string;
        fields: { name: string; label: string }[];
    };
    type iSections = {
        [key: string]: iSection;
    };
    const sections: iSections = {
        general: {
            title: "General",
            fields: [
                { name: "allowPhotos", label: "Allow Photos" },
                { name: "showFaq", label: "Show FAQ" },
                { name: "weddingDate", label: "Wedding Date" },
            ],
        },
    };
</script>

<div>
    <ProtectedPageShell
        ><div class="container mx-auto p-4 max-w-6xl">
            <div class="flex justify-between items-center mb-6">
                <h1 class="text-3xl font-bold">Wedding Configuration</h1>
                <a href="/settings/config/edit" class="btn btn-primary">Edit Settings</a>
            </div>

            {#if data.configData}
                <div class="grid gap-4">
                    <div class="config-card" id="general-section">
                        <div class="config-card-body">
                            <h2 class="config-card-title text-xl mb-4">General</h2>

                            <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mt-4">
                                {#each sections.general.fields as field, index (index)}
                                    <div class="flex flex-col">
                                        <div class="config-card-field-name">{field.label}</div>
                                        <div class="config-card-field-value">
                                            {formatValue(data.configData[field.name as keyof typeof data.configData])}
                                        </div>
                                    </div>
                                {/each}
                            </div>
                        </div>
                    </div>
                    <div class="config-card" id="guestlist-section">
                        <div class="config-card-body">
                            <h2 class="config-card-title text-xl mb-4">Guest List</h2>
                            <p>
                                The guestlist is comprised of guest groups and guests. The Smith Family guest group
                                contains two guests, John and Cindy Smith. Guest groups are categorized using standard,
                                accommodation, or VIP classifications. The names for all three classifications can be
                                modified to suit your wedding's needs.
                            </p>
                            <div class="grid grid-cols-1 gap-4 mt-4">
                                <div class="flex flex-row gap-4">
                                    <div class="flex flex-col">
                                        <div class="config-card-field-name">Use Accommodation Classification</div>
                                        <div class="config-card-field-value">
                                            {formatValue(data.configData["rsvpShowAccommodationIntro"])}
                                        </div>
                                    </div>
                                    <div class="flex flex-col">
                                        <div class="config-card-field-name">Use VIP Classification</div>
                                        <div class="config-card-field-value">
                                            {formatValue(data.configData["rsvpShowVipIntro"])}
                                        </div>
                                    </div>
                                </div>
                                <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
                                    <div class="flex flex-col">
                                        <div class="config-card-field-name">Standard Classification Name</div>
                                        <div class="config-card-field-value">
                                            {data.configData["standardGroupLabel"]}
                                        </div>
                                    </div>
                                    {#if data.configData["rsvpShowAccommodationIntro"]}
                                        <div class="flex flex-col">
                                            <div class="config-card-field-name">Accommodation Classification Name</div>
                                            <div class="config-card-field-value">
                                                {data.configData["accommodationGroupLabel"]}
                                            </div>
                                        </div>
                                    {/if}
                                    {#if data.configData["rsvpShowVipIntro"]}
                                        <div class="flex flex-col">
                                            <div class="config-card-field-name">VIP Classification Name</div>
                                            <div class="config-card-field-value">
                                                {data.configData["vipGroupLabel"]}
                                            </div>
                                        </div>
                                    {/if}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="config-card" id="rsvp-section">
                        <div class="config-card-body">
                            <h2 class="config-card-title text-xl mb-4">RSVP</h2>
                            <p>The RSVP process is broken-down into three stages</p>
                            <ul class="list-disc list-inside mt-2 mb-4">
                                <li><b>Landing</b>: Accept or decline the invitation</li>
                                <li>
                                    <b>Accept</b>: Answer all configured questions and confirm each guest in the group
                                </li>
                                <li><b>Complete</b>: Configured confirmation message along with additional links</li>
                            </ul>
                            <div class="grid grid-cols-1 gap-4 mt-4">
                                <div class="flex flex-row gap-4">
                                    <div class="flex flex-col">
                                        <div class="config-card-field-name">Allow RSVP</div>
                                        <div class="config-card-field-value">
                                            {formatValue(data.configData["allowRsvp"])}
                                        </div>
                                    </div>
                                    <div class="flex flex-col">
                                        <div class="config-card-field-name">RSVP Email Updates Enabled</div>
                                        <div class="config-card-field-value">
                                            {formatValue(data.configData["rsvpEnableEmailUpdates"])}
                                        </div>
                                    </div>
                                    <div class="flex flex-col">
                                        <div class="config-card-field-name">RSVP Start Date</div>
                                        <div class="config-card-field-value">
                                            {formatValue(data.configData["rsvpStartDate"])}
                                        </div>
                                    </div>
                                    <div class="flex flex-col">
                                        <div class="config-card-field-name">RSVP End Date</div>
                                        <div class="config-card-field-value">
                                            {formatValue(data.configData["rsvpEndDate"])}
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="divider divider-accent">Landing</div>
                            <div class="grid grid-cols-1 gap-4 mt-4">
                                <div class="flex flex-row gap-4">
                                    <div class="flex flex-col">
                                        <div class="config-card-field-name">Accept Button Text</div>
                                        <div class="config-card-field-value">
                                            {formatValue(data.configData["rsvpAcceptButton"])}
                                        </div>
                                    </div>
                                    <div class="flex flex-col">
                                        <div class="config-card-field-name">Decline Button Text</div>
                                        <div class="config-card-field-value">
                                            {formatValue(data.configData["rsvpDeclineButton"])}
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="card-actions justify-center mt-4">
                                <a
                                    href="/settings/preview/rsvp/landing"
                                    class="btn btn-accent mr-4 mb-4"
                                    target="_blank">Preview Landing Page</a>
                            </div>
                            <div class="divider divider-accent">Accept</div>

                            <div class="grid grid-cols-1 gap-4 mt-4">
                                <div class="flex flex-col">
                                    <div class="config-card-field-name">Accept Introduction Text</div>
                                    <div class="config-card-field-value">
                                        <!-- eslint-disable-next-line svelte/no-at-html-tags set by site admin -->
                                        {@html data.configData["rsvpAcceptIntro"]}
                                    </div>
                                </div>
                                <div class="flex flex-col">
                                    <div class="config-card-field-name">Attending Checkbox Label</div>
                                    <div class="config-card-field-value">
                                        <!-- eslint-disable-next-line svelte/no-at-html-tags set by site admin -->
                                        {@html data.configData["rsvpAttendingLabel"]}
                                    </div>
                                </div>
                                {#if data.configData["rsvpShowAccommodationIntro"]}
                                    <div class="flex flex-col">
                                        <div class="config-card-field-name">
                                            {data.configData["accommodationGroupLabel"]} Introduction Text
                                        </div>
                                        <div class="config-card-field-value">
                                            <!-- eslint-disable-next-line svelte/no-at-html-tags set by site admin -->
                                            {@html data.configData["rsvpAccommodationIntro"]}
                                        </div>
                                    </div>
                                    <div class="flex flex-col">
                                        <div class="config-card-field-name">
                                            {data.configData["accommodationGroupLabel"]} Checkbox Label
                                        </div>
                                        <div class="config-card-field-value">
                                            {data.configData["rsvpAccommodationLabel"]}
                                        </div>
                                    </div>
                                {/if}
                                {#if data.configData["rsvpShowVipIntro"]}
                                    <div class="flex flex-col">
                                        <div class="config-card-field-name">
                                            {data.configData["vipGroupLabel"]} Introduction Text
                                        </div>
                                        <div class="config-card-field-value">
                                            <!-- eslint-disable-next-line svelte/no-at-html-tags set by site admin -->
                                            {@html data.configData["rsvpVipIntro"]}
                                        </div>
                                    </div>
                                    <div class="flex flex-col">
                                        <div class="config-card-field-name">
                                            {data.configData["vipGroupLabel"]} Checkbox Label
                                        </div>
                                        <div class="config-card-field-value">
                                            {data.configData["rsvpVipLabel"]}
                                        </div>
                                    </div>
                                {/if}
                                {#if data.configData["rsvpEnableEmailUpdates"]}
                                    <div class="flex flex-col">
                                        <div class="config-card-field-name">Email Updates Label</div>
                                        <div class="config-card-field-value">
                                            {data.configData["rsvpEmailUpdateLabel"]}
                                        </div>
                                    </div>
                                {/if}
                            </div>
                            <div class="card-actions justify-center mt-4">
                                <a href="/settings/preview/rsvp/accept" class="btn btn-accent mr-4 mb-4" target="_blank"
                                    >Preview Accept Page</a>
                            </div>
                            <div class="divider divider-accent">Complete</div>
                            <div class="grid grid-cols-1 gap-4 mt-4">
                                <div class="flex flex-col">
                                    <div class="config-card-field-name">Completion Headline</div>
                                    <div class="config-card-field-value">
                                        {formatValue(data.configData["rsvpSuccessHeadline"])}
                                    </div>
                                </div>

                                <div class="flex flex-col">
                                    <div class="config-card-field-name">Accept Message</div>
                                    <div class="config-card-field-value">
                                        {formatValue(data.configData["rsvpAcceptSuccessMessage"])}
                                    </div>
                                </div>
                                <div class="flex flex-col">
                                    <div class="config-card-field-name">Decline Message</div>
                                    <div class="config-card-field-value">
                                        {formatValue(data.configData["rsvpDeclineSuccessMessage"])}
                                    </div>
                                </div>
                            </div>
                            <div class="card-actions justify-center mt-4">
                                <a
                                    href="/settings/preview/rsvp/complete?accepted=true"
                                    class="btn btn-accent mr-4 mb-4"
                                    target="_blank">Preview Accepted Complete Page</a>
                                <a
                                    href="/settings/preview/rsvp/complete?accepted=false"
                                    class="btn btn-accent mr-4 mb-4"
                                    target="_blank">Preview Declined Complete Page</a>
                            </div>
                        </div>
                    </div>
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
