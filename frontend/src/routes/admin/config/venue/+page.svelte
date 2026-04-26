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
            <h2 class="config-card-title text-xl">Venue</h2>
            <a href="/admin/config/edit#venue-section" class="btn btn-sm btn-accent">
                <span class="icon-[lucide--square-pen] size-4"></span>
                Edit Venue
            </a>
        </div>
        <div class="grid grid-cols-1 gap-4">
            <div>
                <div class="config-card-field-name">Venue Page Title</div>
                <div class="config-card-field-value">{formatValue(data.configData?.venuePageTitle)}</div>
            </div>
            <div>
                <div class="config-card-field-name">Venue Page Description</div>
                <div class="config-card-field-value">{formatValue(data.configData?.venuePageDescription)}</div>
            </div>
        </div>

        <div class="divider divider-accent">Venue Details</div>
        <div class="grid grid-cols-1 gap-4">
            <div>
                <div class="config-card-field-name">Venue Name</div>
                <div class="config-card-field-value">{formatValue(data.configData?.venueName)}</div>
            </div>
            <div>
                <div class="config-card-field-name">Address Line 1</div>
                <div class="config-card-field-value">{formatValue(data.configData?.venueAddressLineOne)}</div>
            </div>
            {#if data.configData?.venueAddressLineTwo}
                <div>
                    <div class="config-card-field-name">Address Line 2</div>
                    <div class="config-card-field-value">{formatValue(data.configData?.venueAddressLineTwo)}</div>
                </div>
            {/if}
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div>
                    <div class="config-card-field-name">City</div>
                    <div class="config-card-field-value">{formatValue(data.configData?.venueCity)}</div>
                </div>
                <div>
                    <div class="config-card-field-name">State</div>
                    <div class="config-card-field-value">{formatValue(data.configData?.venueState)}</div>
                </div>
                <div>
                    <div class="config-card-field-name">Zip Code</div>
                    <div class="config-card-field-value">{formatValue(data.configData?.venueZipcode)}</div>
                </div>
                <div>
                    <div class="config-card-field-name">Country</div>
                    <div class="config-card-field-value">{formatValue(data.configData?.venueCountry)}</div>
                </div>
            </div>
            {#if data.configData?.venueParking}
                <div>
                    <div class="config-card-field-name">Parking Information</div>
                    <div class="config-card-field-value">{@html data.configData?.venueParking ?? "Not set"}</div>
                </div>
            {/if}
        </div>

        <div class="divider divider-accent">Venue Gallery</div>
        <div class="grid grid-cols-1 gap-4">
            <div>
                <div class="config-card-field-name">Gallery Title</div>
                <div class="config-card-field-value">{formatValue(data.configData?.venueGalleryTitle)}</div>
            </div>
            <div>
                <div class="config-card-field-name">Gallery Description</div>
                <div class="config-card-field-value">{formatValue(data.configData?.venueGalleryDescription)}</div>
            </div>
        </div>

        <div class="card-actions justify-center mt-4">
            <a href="/planning/preview/venue" class="btn btn-accent" target="_blank">Preview Venue Page</a>
        </div>
    </div>
</div>
