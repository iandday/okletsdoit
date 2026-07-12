<script lang="ts">
    import SectionStatus from "$lib/components/SectionStatus.svelte";

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
        <div class="divider divider-accent">Website Features</div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div>
                <div class="config-card-field-name">Our Story</div>
                <SectionStatus enabled={data.configData?.enableOurStory} visible={data.configData?.showOurStory} />
            </div>
            <div>
                <div class="config-card-field-name">Venue</div>
                <div class="config-card-field-value">
                    <SectionStatus enabled={data.configData?.enableVenue} visible={data.configData?.showVenue} />
                </div>
            </div>
            <div>
                <div class="config-card-field-name">FAQ</div>
                <div class="config-card-field-value">
                    <SectionStatus enabled={data.configData?.enableFaq} visible={data.configData?.showFaq} />
                </div>
            </div>
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
