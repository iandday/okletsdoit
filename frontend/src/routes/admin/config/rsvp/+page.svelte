<script lang="ts">
    const { data } = $props();

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
</script>

<div class="config-card">
    <div class="config-card-body">
        <div class="flex items-center justify-between gap-2 mb-4">
            <h2 class="config-card-title text-xl">RSVP</h2>
            <a href="/admin/config/edit#rsvp-section" class="btn btn-sm btn-accent">
                <span class="icon-[lucide--square-pen] size-4"></span>
                Edit RSVP
            </a>
        </div>
        <p>The RSVP process is broken-down into three stages</p>
        <ul class="list-disc list-inside mt-2 mb-4">
            <li><b>Landing</b>: Accept or decline the invitation</li>
            <li><b>Accept</b>: Answer configured questions and confirm each guest</li>
            <li><b>Complete</b>: Show confirmation messaging and links</li>
        </ul>

        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 mt-4">
            <div>
                <div class="config-card-field-name">Allow RSVP</div>
                <div class="config-card-field-value">{formatValue(data.configData?.allowRsvp)}</div>
            </div>
            <div>
                <div class="config-card-field-name">RSVP Email Updates Enabled</div>
                <div class="config-card-field-value">
                    {formatValue(data.configData?.rsvpEnableEmailUpdates)}
                </div>
            </div>
            <div>
                <div class="config-card-field-name">RSVP Start Date</div>
                <div class="config-card-field-value">{formatValue(data.configData?.rsvpStartDate)}</div>
            </div>
            <div>
                <div class="config-card-field-name">RSVP End Date</div>
                <div class="config-card-field-value">{formatValue(data.configData?.rsvpEndDate)}</div>
            </div>
            <div>
                <div class="config-card-field-name">RSVP URL</div>
                <div class="config-card-field-value">{formatValue(data.configData?.rsvpDefaultUrl)}</div>
            </div>
        </div>

        <div class="divider divider-accent">Landing</div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
                <div class="config-card-field-name">Accept Button Text</div>
                <div class="config-card-field-value">{formatValue(data.configData?.rsvpAcceptButton)}</div>
            </div>
            <div>
                <div class="config-card-field-name">Decline Button Text</div>
                <div class="config-card-field-value">{formatValue(data.configData?.rsvpDeclineButton)}</div>
            </div>
        </div>
        <div class="card-actions justify-center mt-4">
            <a href="/planning/preview/rsvp/landing" class="btn btn-accent" target="_blank">Preview Landing Page</a>
        </div>

        <div class="divider divider-accent">Accept</div>
        <div class="grid grid-cols-1 gap-4">
            <div>
                <div class="config-card-field-name">Accept Introduction Text</div>
                <div class="config-card-field-value">
                    <!-- eslint-disable-next-line svelte/no-at-html-tags set by site admin -->
                    {@html data.configData?.rsvpAcceptIntro ?? "Not set"}
                </div>
            </div>
            <div>
                <div class="config-card-field-name">Attending Checkbox Label</div>
                <div class="config-card-field-value">
                    <!-- eslint-disable-next-line svelte/no-at-html-tags set by site admin -->
                    {@html data.configData?.rsvpAttendingLabel ?? "Not set"}
                </div>
            </div>
            {#if data.configData?.rsvpShowAccommodationIntro}
                <div>
                    <div class="config-card-field-name">
                        {data.configData?.accommodationGroupLabel} Introduction Text
                    </div>
                    <div class="config-card-field-value">
                        <!-- eslint-disable-next-line svelte/no-at-html-tags set by site admin -->
                        {@html data.configData?.rsvpAccommodationIntro ?? "Not set"}
                    </div>
                </div>
                <div>
                    <div class="config-card-field-name">{data.configData?.accommodationGroupLabel} Checkbox Label</div>
                    <div class="config-card-field-value">{data.configData?.rsvpAccommodationLabel ?? "Not set"}</div>
                </div>
            {/if}
            {#if data.configData?.rsvpShowVipIntro}
                <div>
                    <div class="config-card-field-name">{data.configData?.vipGroupLabel} Introduction Text</div>
                    <div class="config-card-field-value">
                        <!-- eslint-disable-next-line svelte/no-at-html-tags set by site admin -->
                        {@html data.configData?.rsvpVipIntro ?? "Not set"}
                    </div>
                </div>
                <div>
                    <div class="config-card-field-name">{data.configData?.vipGroupLabel} Checkbox Label</div>
                    <div class="config-card-field-value">{data.configData?.rsvpVipLabel ?? "Not set"}</div>
                </div>
            {/if}
            {#if data.configData?.rsvpEnableEmailUpdates}
                <div>
                    <div class="config-card-field-name">Email Updates Label</div>
                    <div class="config-card-field-value">{data.configData?.rsvpEmailUpdateLabel ?? "Not set"}</div>
                </div>
            {/if}
        </div>
        <div class="card-actions justify-center mt-4">
            <a href="/planning/preview/rsvp/accept" class="btn btn-accent" target="_blank">Preview Accept Page</a>
        </div>

        <div class="divider divider-accent">Complete</div>
        <div class="grid grid-cols-1 gap-4">
            <div>
                <div class="config-card-field-name">Completion Headline</div>
                <div class="config-card-field-value">{formatValue(data.configData?.rsvpSuccessHeadline)}</div>
            </div>
            <div>
                <div class="config-card-field-name">Accept Message</div>
                <div class="config-card-field-value">{formatValue(data.configData?.rsvpAcceptSuccessMessage)}</div>
            </div>
            <div>
                <div class="config-card-field-name">Decline Message</div>
                <div class="config-card-field-value">{formatValue(data.configData?.rsvpDeclineSuccessMessage)}</div>
            </div>
        </div>
        <div class="card-actions justify-center mt-4 gap-2">
            <a href="/planning/preview/rsvp/complete?accepted=true" class="btn btn-accent" target="_blank"
                >Preview Accepted Complete Page</a>
            <a href="/planning/preview/rsvp/complete?accepted=false" class="btn btn-accent" target="_blank"
                >Preview Declined Complete Page</a>
        </div>
    </div>
</div>
