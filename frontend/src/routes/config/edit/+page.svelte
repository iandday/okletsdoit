<script lang="ts">
    import { enhance } from "$app/forms";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { WeddingSettingsUpdateSchema } from "../../../api-client";

    const { data, form } = $props();

    let formData = $state<WeddingSettingsUpdateSchema>({
        weddingDate: data.configData?.weddingDate || null,
        allowRsvp: data.configData?.allowRsvp ?? false,

        showFaq: data.configData?.showFaq ?? false,
        rsvpStartDate: data.configData?.rsvpStartDate || null,
        rsvpEndDate: data.configData?.rsvpEndDate || null,
        rsvpAcceptButton: data.configData?.rsvpAcceptButton || "",
        rsvpDeclineButton: data.configData?.rsvpDeclineButton || "",
        rsvpAttendingLabel: data.configData?.rsvpAttendingLabel || "",
        rsvpAccommodationLabel: data.configData?.rsvpAccommodationLabel || "",
        rsvpVipLabel: data.configData?.rsvpVipLabel || "",
        standardGroupLabel: data.configData?.standardGroupLabel || "",
        vipGroupLabel: data.configData?.vipGroupLabel || "",
        rsvpEmailUpdateLabel: data.configData?.rsvpEmailUpdateLabel || "",
        rsvpAcceptIntro: data.configData?.rsvpAcceptIntro || "",
        rsvpAcceptSuccessMessage: data.configData?.rsvpAcceptSuccessMessage || "",
        rsvpDeclineSuccessMessage: data.configData?.rsvpDeclineSuccessMessage || "",
        rsvpAccommodationIntro: data.configData?.rsvpAccommodationIntro || "",
        rsvpVipIntro: data.configData?.rsvpVipIntro || "",
        rsvpSuccessHeadline: data.configData?.rsvpSuccessHeadline || "",
        rsvpShowAccommodationIntro: data.configData?.rsvpShowAccommodationIntro ?? false,
        rsvpShowVipIntro: data.configData?.rsvpShowVipIntro ?? false,
        rsvpEnableEmailUpdates: data.configData?.rsvpEnableEmailUpdates ?? false,
    });

    let submitting = $state(false);

    const formatLabel = (key: string): string => {
        return key
            .replace(/([A-Z])/g, " $1")
            .replace(/^./, (str) => str.toUpperCase())
            .trim();
    };

    const sections = {
        general: {
            title: "General Settings",
            fields: [
                { name: "allowRsvp", type: "checkbox" },
                { name: "allowPhotos", type: "checkbox" },
                { name: "showFaq", type: "checkbox" },
                { name: "weddingDate", type: "date" },
            ],
        },
        rsvpDates: {
            title: "RSVP Dates",
            fields: [
                { name: "rsvpStartDate", type: "date" },
                { name: "rsvpEndDate", type: "date" },
            ],
        },
        rsvpButtons: {
            title: "RSVP Buttons",
            fields: [
                { name: "rsvpAcceptButton", type: "text" },
                { name: "rsvpDeclineButton", type: "text" },
            ],
        },
        rsvpLabels: {
            title: "RSVP Labels",
            fields: [
                { name: "rsvpAttendingLabel", type: "text" },
                { name: "rsvpAccommodationLabel", type: "text" },
                { name: "rsvpVipLabel", type: "text" },
                { name: "standardGroupLabel", type: "text" },
                { name: "vipGroupLabel", type: "text" },
                { name: "rsvpEmailUpdateLabel", type: "text" },
            ],
        },
        rsvpMessages: {
            title: "RSVP Messages",
            fields: [
                { name: "rsvpAcceptIntro", type: "textarea" },
                { name: "rsvpAcceptSuccessMessage", type: "textarea" },
                { name: "rsvpDeclineSuccessMessage", type: "textarea" },
                { name: "rsvpAccommodationIntro", type: "textarea" },
                { name: "rsvpVipIntro", type: "textarea" },
                { name: "rsvpSuccessHeadline", type: "text" },
            ],
        },
        rsvpOptions: {
            title: "RSVP Display Options",
            fields: [
                { name: "rsvpShowAccommodationIntro", type: "checkbox" },
                { name: "rsvpShowVipIntro", type: "checkbox" },
                { name: "rsvpEnableEmailUpdates", type: "checkbox" },
            ],
        },
    };
</script>

<ProtectedPageShell>
    <div class="container mx-auto p-4 max-w-6xl">
        <div class="flex justify-between items-center mb-6">
            <h1 class="text-3xl font-bold">Edit Wedding Configuration</h1>
            <a href="/config" class="btn btn-ghost">Cancel</a>
        </div>

        {#if form?.error}
            <div class="alert alert-error mb-4">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="stroke-current shrink-0 h-6 w-6"
                    fill="none"
                    viewBox="0 0 24 24">
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>{form.error}</span>
            </div>
        {/if}

        <form
            method="POST"
            use:enhance={() => {
                submitting = true;
                return async ({ update }) => {
                    await update();
                    submitting = false;
                };
            }}>
            <div class="grid gap-6">
                {#each Object.entries(sections) as [key, section], index (key)}
                    <div class="card bg-base-100 shadow-xl">
                        <div class="card-body">
                            <h2 class="card-title text-xl mb-4">{section.title}</h2>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {#each section.fields as field, index (index)}
                                    <div class="form-control w-full">
                                        <label class="label" for={field.name}>
                                            <span class="label-text font-semibold">{formatLabel(field.name)}</span>
                                        </label>

                                        {#if field.type === "checkbox"}
                                            <input
                                                type="checkbox"
                                                name={field.name}
                                                id={field.name}
                                                class="toggle toggle-primary"
                                                checked={formData[field.name as keyof WeddingSettingsUpdateSchema]} />
                                        {:else if field.type === "date"}
                                            <input
                                                type="date"
                                                name={field.name}
                                                id={field.name}
                                                class="input input-bordered w-full"
                                                value={formData[field.name as keyof WeddingSettingsUpdateSchema] ||
                                                    ""} />
                                        {:else if field.type === "textarea"}
                                            <textarea
                                                name={field.name}
                                                id={field.name}
                                                class="textarea textarea-bordered w-full h-24"
                                                value={formData[field.name as keyof WeddingSettingsUpdateSchema] || ""}
                                            ></textarea>
                                        {:else}
                                            <input
                                                type="text"
                                                name={field.name}
                                                id={field.name}
                                                class="input input-bordered w-full"
                                                value={formData[field.name as keyof WeddingSettingsUpdateSchema] ||
                                                    ""} />
                                        {/if}
                                    </div>
                                {/each}
                            </div>
                        </div>
                    </div>
                {/each}
            </div>

            <div class="flex gap-4 mt-6 justify-end">
                <a href="/config" class="btn btn-ghost">Cancel</a>
                <button type="submit" class="btn btn-primary" disabled={submitting}>
                    {#if submitting}
                        <span class="loading loading-spinner"></span>
                        Saving...
                    {:else}
                        Save Changes
                    {/if}
                </button>
            </div>
        </form>
    </div>
</ProtectedPageShell>
