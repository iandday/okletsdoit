<script lang="ts">
    const { data } = $props();

    const formatValue = (value: null | boolean | Date | string | number | undefined): string => {
        if (value === null || value === undefined) return "Not set";
        if (typeof value === "boolean") return value ? "Yes" : "No";
        return String(value);
    };
</script>

<div class="config-card">
    <div class="config-card-body">
        <div class="flex items-center justify-between gap-2 mb-4">
            <h2 class="config-card-title text-xl">Guest List</h2>
            <a href="/admin/config/edit#guestlist-section" class="btn btn-sm btn-accent">
                <span class="icon-[lucide--square-pen] size-4"></span>
                Edit Guest List
            </a>
        </div>
        <p>
            The guestlist is comprised of guest groups and guests. Guest groups are categorized using standard,
            accommodation, or VIP classifications.
        </p>

        <div class="grid grid-cols-1 gap-4 mt-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <div class="config-card-field-name">Use Accommodation Classification</div>
                    <div class="config-card-field-value">
                        {formatValue(data.configData?.rsvpShowAccommodationIntro)}
                    </div>
                </div>
                <div>
                    <div class="config-card-field-name">Use VIP Classification</div>
                    <div class="config-card-field-value">{formatValue(data.configData?.rsvpShowVipIntro)}</div>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                    <div class="config-card-field-name">Standard Classification Name</div>
                    <div class="config-card-field-value">{data.configData?.standardGroupLabel ?? "Not set"}</div>
                </div>
                {#if data.configData?.rsvpShowAccommodationIntro}
                    <div>
                        <div class="config-card-field-name">Accommodation Classification Name</div>
                        <div class="config-card-field-value">
                            {data.configData?.accommodationGroupLabel ?? "Not set"}
                        </div>
                    </div>
                {/if}
                {#if data.configData?.rsvpShowVipIntro}
                    <div>
                        <div class="config-card-field-name">VIP Classification Name</div>
                        <div class="config-card-field-value">{data.configData?.vipGroupLabel ?? "Not set"}</div>
                    </div>
                {/if}
            </div>
        </div>
    </div>
</div>
