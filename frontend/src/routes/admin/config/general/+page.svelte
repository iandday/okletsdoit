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
            <h2 class="config-card-title text-xl">General</h2>
            <a href="/admin/config/edit#general-section" class="btn btn-sm btn-accent">
                <span class="icon-[lucide--square-pen] size-4"></span>
                Edit General
            </a>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div>
                <div class="config-card-field-name">Allow Photos</div>
                <div class="config-card-field-value">{formatValue(data.configData?.allowPhotos)}</div>
            </div>
            <div>
                <div class="config-card-field-name">Show FAQ</div>
                <div class="config-card-field-value">{formatValue(data.configData?.showFaq)}</div>
            </div>
            <div>
                <div class="config-card-field-name">Show Venue</div>
                <div class="config-card-field-value">{formatValue(data.configData?.showVenue)}</div>
            </div>
            <div>
                <div class="config-card-field-name">Wedding Date</div>
                <div class="config-card-field-value">{formatValue(data.configData?.weddingDate)}</div>
            </div>
        </div>
    </div>
</div>
