<script lang="ts">
    import { enhance } from "$app/forms";
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { WeddingSettingsUpdateSchema } from "../../../api-client";

    const { data, form } = $props();

    let formData = $state<WeddingSettingsUpdateSchema>({
        weddingDate: data.configData?.weddingDate || null,
        allowRsvp: data.configData?.allowRsvp ?? false,
        showVenue: data.configData?.showVenue ?? false,
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
        venuePageTitle: data.configData?.venuePageTitle || "",
        venuePageDescription: data.configData?.venuePageDescription || "",
        venueName: data.configData?.venueName || "",
        venueAddressLineOne: data.configData?.venueAddressLineOne || "",
        venueAddressLineTwo: data.configData?.venueAddressLineTwo || "",
        venueCity: data.configData?.venueCity || "",
        venueState: data.configData?.venueState || "",
        venueZipcode: data.configData?.venueZipcode || "",
        venueCountry: data.configData?.venueCountry || "",
        venueParking: data.configData?.venueParking || "",
        venueGalleryTitle: data.configData?.venueGalleryTitle || "",
        venueGalleryDescription: data.configData?.venueGalleryDescription || "",
    });

    let submitting = $state(false);

    const formatLabel = (key: string): string => {
        return key
            .replace(/([A-Z])/g, " $1")
            .replace(/^./, (str) => str.toUpperCase())
            .trim();
    };

    const generalFields = [
        { name: "allowPhotos", type: "checkbox" },
        { name: "showFaq", type: "checkbox" },
        { name: "showVenue", type: "checkbox" },
        { name: "weddingDate", type: "date" },
    ];

    const relativeCrumbs = [{ title: "Configuration", href: "/planning/config" }, { title: "Edit" }];
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader title="Edit Wedding Configuration" cancelLink="/planning/config" cancelText="Cancel" />

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
        <div class="grid gap-4">
            <!-- General Section -->
            <div class="config-card" id="general-section">
                <div class="config-card-body">
                    <h2 class="config-card-title text-xl mb-4">General</h2>
                    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mt-4">
                        {#each generalFields as field, index (index)}
                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for={field.name}>
                                    <span>{formatLabel(field.name)}</span>
                                </label>
                                {#if field.type === "checkbox"}
                                    <input
                                        type="checkbox"
                                        name={field.name}
                                        id={field.name}
                                        class="edit-card-field-toggle"
                                        checked={formData[field.name as keyof WeddingSettingsUpdateSchema]} />
                                {:else if field.type === "date"}
                                    <input
                                        type="date"
                                        name={field.name}
                                        id={field.name}
                                        class="edit-card-field-date"
                                        value={formData[field.name as keyof WeddingSettingsUpdateSchema] || ""} />
                                {:else}
                                    <input
                                        type="text"
                                        name={field.name}
                                        id={field.name}
                                        class="edit-card-field-input"
                                        value={formData[field.name as keyof WeddingSettingsUpdateSchema] || ""} />
                                {/if}
                            </div>
                        {/each}
                    </div>
                </div>
            </div>

            <!-- Guest List Section -->
            <div class="config-card" id="guestlist-section">
                <div class="config-card-body">
                    <h2 class="config-card-title text-xl mb-4">Guest List</h2>
                    <p>
                        The guestlist is comprised of guest groups and guests. The Smith Family guest group contains two
                        guests, John and Cindy Smith. Guest groups are categorized using standard, accommodation, or VIP
                        classifications. The names for all three classifications can be modified to suit your wedding's
                        needs.
                    </p>
                    <div class="grid grid-cols-1 gap-4 mt-4">
                        <div class="flex flex-row gap-4">
                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="rsvpShowAccommodationIntro">
                                    <span>Use Accommodation Classification</span>
                                </label>
                                <input
                                    type="checkbox"
                                    name="rsvpShowAccommodationIntro"
                                    id="rsvpShowAccommodationIntro"
                                    class="edit-card-field-toggle"
                                    bind:checked={formData.rsvpShowAccommodationIntro} />
                            </div>
                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="rsvpShowVipIntro">
                                    <span>Use VIP Classification</span>
                                </label>
                                <input
                                    type="checkbox"
                                    name="rsvpShowVipIntro"
                                    id="rsvpShowVipIntro"
                                    class="edit-card-field-toggle"
                                    bind:checked={formData.rsvpShowVipIntro} />
                            </div>
                        </div>
                        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="standardGroupLabel">
                                    <span>Standard Classification Name</span>
                                </label>
                                <input
                                    type="text"
                                    name="standardGroupLabel"
                                    id="standardGroupLabel"
                                    class="edit-card-field-input"
                                    value={formData.standardGroupLabel} />
                            </div>
                            {#if formData.rsvpShowAccommodationIntro}
                                <div class="form-control w-full">
                                    <label class="edit-card-field-name" for="accommodationGroupLabel">
                                        <span>Accommodation Classification Name</span>
                                    </label>
                                    <input
                                        type="text"
                                        name="accommodationGroupLabel"
                                        id="accommodationGroupLabel"
                                        class="edit-card-field-input"
                                        value={formData.accommodationGroupLabel} />
                                </div>
                            {/if}
                            {#if formData.rsvpShowVipIntro}
                                <div class="form-control w-full">
                                    <label class="edit-card-field-name" for="vipGroupLabel">
                                        <span>VIP Classification Name</span>
                                    </label>
                                    <input
                                        type="text"
                                        name="vipGroupLabel"
                                        id="vipGroupLabel"
                                        class="edit-card-field-input"
                                        value={formData.vipGroupLabel} />
                                </div>
                            {/if}
                        </div>
                    </div>
                </div>
            </div>

            <!-- RSVP Section -->
            <div class="config-card" id="rsvp-section">
                <div class="config-card-body">
                    <h2 class="config-card-title text-xl mb-4">RSVP</h2>
                    <p>The RSVP process is broken-down into three stages</p>
                    <ul class="list-disc list-inside mt-2 mb-4">
                        <li><b>Landing</b>: Accept or decline the invitation</li>
                        <li><b>Accept</b>: Answer all configured questions and confirm each guest in the group</li>
                        <li><b>Complete</b>: Configured confirmation message along with additional links</li>
                    </ul>

                    <div class="grid grid-cols-1 gap-4 mt-4">
                        <div class="flex flex-row gap-4">
                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="allowRsvp">
                                    <span>Allow RSVP</span>
                                </label>
                                <input
                                    type="checkbox"
                                    name="allowRsvp"
                                    id="allowRsvp"
                                    class="edit-card-field-toggle"
                                    checked={formData.allowRsvp} />
                            </div>
                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="rsvpEnableEmailUpdates">
                                    <span>RSVP Email Updates Enabled</span>
                                </label>
                                <input
                                    type="checkbox"
                                    name="rsvpEnableEmailUpdates"
                                    id="rsvpEnableEmailUpdates"
                                    class="edit-card-field-toggle"
                                    bind:checked={formData.rsvpEnableEmailUpdates} />
                            </div>
                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="rsvpStartDate">
                                    <span>RSVP Start Date</span>
                                </label>
                                <input
                                    type="date"
                                    name="rsvpStartDate"
                                    id="rsvpStartDate"
                                    class="edit-card-field-date"
                                    value={formData.rsvpStartDate || ""} />
                            </div>
                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="rsvpEndDate">
                                    <span>RSVP End Date</span>
                                </label>
                                <input
                                    type="date"
                                    name="rsvpEndDate"
                                    id="rsvpEndDate"
                                    class="edit-card-field-date"
                                    value={formData.rsvpEndDate || ""} />
                            </div>
                        </div>
                    </div>

                    <div class="divider divider-accent">Landing</div>
                    <div class="grid grid-cols-1 gap-4 mt-4">
                        <div class="flex flex-row gap-4">
                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="rsvpAcceptButton">
                                    <span>Accept Button Text</span>
                                </label>
                                <input
                                    type="text"
                                    name="rsvpAcceptButton"
                                    id="rsvpAcceptButton"
                                    class="edit-card-field-input"
                                    value={formData.rsvpAcceptButton} />
                            </div>
                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="rsvpDeclineButton">
                                    <span>Decline Button Text</span>
                                </label>
                                <input
                                    type="text"
                                    name="rsvpDeclineButton"
                                    id="rsvpDeclineButton"
                                    class="edit-card-field-input"
                                    value={formData.rsvpDeclineButton} />
                            </div>
                        </div>
                    </div>

                    <div class="divider divider-accent">Accept</div>
                    <div class="grid grid-cols-1 gap-4 mt-4">
                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="rsvpAcceptIntro">
                                <span>Accept Introduction Text</span>
                            </label>
                            <textarea
                                name="rsvpAcceptIntro"
                                id="rsvpAcceptIntro"
                                class="edit-card-field-textarea"
                                value={formData.rsvpAcceptIntro}></textarea>
                        </div>
                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="rsvpAttendingLabel">
                                <span>Attending Checkbox Label</span>
                            </label>
                            <input
                                type="text"
                                name="rsvpAttendingLabel"
                                id="rsvpAttendingLabel"
                                class="edit-card-field-input"
                                value={formData.rsvpAttendingLabel} />
                        </div>
                        {#if formData.rsvpShowAccommodationIntro}
                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="rsvpAccommodationIntro">
                                    <span>{formData.accommodationGroupLabel || "Accommodation"} Introduction Text</span>
                                </label>
                                <textarea
                                    name="rsvpAccommodationIntro"
                                    id="rsvpAccommodationIntro"
                                    class="edit-card-field-textarea"
                                    value={formData.rsvpAccommodationIntro}></textarea>
                            </div>
                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="rsvpAccommodationLabel">
                                    <span>{formData.accommodationGroupLabel || "Accommodation"} Checkbox Label</span>
                                </label>
                                <input
                                    type="text"
                                    name="rsvpAccommodationLabel"
                                    id="rsvpAccommodationLabel"
                                    class="edit-card-field-input"
                                    value={formData.rsvpAccommodationLabel} />
                            </div>
                        {/if}
                        {#if formData.rsvpShowVipIntro}
                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="rsvpVipIntro">
                                    <span>{formData.vipGroupLabel || "VIP"} Introduction Text</span>
                                </label>
                                <textarea
                                    name="rsvpVipIntro"
                                    id="rsvpVipIntro"
                                    class="edit-card-field-textarea"
                                    value={formData.rsvpVipIntro}></textarea>
                            </div>
                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="rsvpVipLabel">
                                    <span>{formData.vipGroupLabel || "VIP"} Checkbox Label</span>
                                </label>
                                <input
                                    type="text"
                                    name="rsvpVipLabel"
                                    id="rsvpVipLabel"
                                    class="edit-card-field-input"
                                    value={formData.rsvpVipLabel} />
                            </div>
                        {/if}
                        {#if formData.rsvpEnableEmailUpdates}
                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="rsvpEmailUpdateLabel">
                                    <span>Email Updates Label</span>
                                </label>
                                <input
                                    type="text"
                                    name="rsvpEmailUpdateLabel"
                                    id="rsvpEmailUpdateLabel"
                                    class="edit-card-field-input"
                                    value={formData.rsvpEmailUpdateLabel} />
                            </div>
                        {/if}
                    </div>

                    <div class="divider divider-accent">Complete</div>
                    <div class="grid grid-cols-1 gap-4 mt-4">
                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="rsvpSuccessHeadline">
                                <span>Completion Headline</span>
                            </label>
                            <input
                                type="text"
                                name="rsvpSuccessHeadline"
                                id="rsvpSuccessHeadline"
                                class="edit-card-field-input"
                                value={formData.rsvpSuccessHeadline} />
                        </div>
                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="rsvpAcceptSuccessMessage">
                                <span>Accept Message</span>
                            </label>
                            <textarea
                                name="rsvpAcceptSuccessMessage"
                                id="rsvpAcceptSuccessMessage"
                                class="edit-card-field-textarea"
                                value={formData.rsvpAcceptSuccessMessage}></textarea>
                        </div>
                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="rsvpDeclineSuccessMessage">
                                <span>Decline Message</span>
                            </label>
                            <textarea
                                name="rsvpDeclineSuccessMessage"
                                id="rsvpDeclineSuccessMessage"
                                class="edit-card-field-textarea"
                                value={formData.rsvpDeclineSuccessMessage}></textarea>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Venue Section -->
            <div class="config-card" id="venue-section">
                <div class="config-card-body">
                    <h2 class="config-card-title text-xl mb-4">Venue</h2>
                    <div class="grid grid-cols-1 gap-4 mt-4">
                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="venuePageTitle">
                                <span>Venue Page Title</span>
                            </label>
                            <input
                                type="text"
                                name="venuePageTitle"
                                id="venuePageTitle"
                                class="edit-card-field-input"
                                value={formData.venuePageTitle} />
                        </div>
                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="venuePageDescription">
                                <span>Venue Page Description</span>
                            </label>
                            <textarea
                                name="venuePageDescription"
                                id="venuePageDescription"
                                class="edit-card-field-textarea"
                                value={formData.venuePageDescription}></textarea>
                        </div>
                    </div>

                    <div class="divider divider-accent">Venue Details</div>
                    <div class="grid grid-cols-1 gap-4 mt-4">
                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="venueName">
                                <span>Venue Name</span>
                            </label>
                            <input
                                type="text"
                                name="venueName"
                                id="venueName"
                                class="edit-card-field-input"
                                value={formData.venueName} />
                        </div>
                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="venueAddressLineOne">
                                <span>Address Line 1</span>
                            </label>
                            <input
                                type="text"
                                name="venueAddressLineOne"
                                id="venueAddressLineOne"
                                class="edit-card-field-input"
                                value={formData.venueAddressLineOne} />
                        </div>
                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="venueAddressLineTwo">
                                <span>Address Line 2 (Optional)</span>
                            </label>
                            <input
                                type="text"
                                name="venueAddressLineTwo"
                                id="venueAddressLineTwo"
                                class="edit-card-field-input"
                                value={formData.venueAddressLineTwo} />
                        </div>
                        <div class="grid grid-cols-1 lg:grid-cols-4 gap-4">
                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="venueCity">
                                    <span>City</span>
                                </label>
                                <input
                                    type="text"
                                    name="venueCity"
                                    id="venueCity"
                                    class="edit-card-field-input"
                                    value={formData.venueCity} />
                            </div>
                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="venueState">
                                    <span>State</span>
                                </label>
                                <input
                                    type="text"
                                    name="venueState"
                                    id="venueState"
                                    class="edit-card-field-input"
                                    value={formData.venueState} />
                            </div>
                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="venueZipcode">
                                    <span>Zip Code</span>
                                </label>
                                <input
                                    type="text"
                                    name="venueZipcode"
                                    id="venueZipcode"
                                    class="edit-card-field-input"
                                    value={formData.venueZipcode} />
                            </div>
                            <div class="form-control w-full">
                                <label class="edit-card-field-name" for="venueCountry">
                                    <span>Country</span>
                                </label>
                                <input
                                    type="text"
                                    name="venueCountry"
                                    id="venueCountry"
                                    class="edit-card-field-input"
                                    value={formData.venueCountry} />
                            </div>
                        </div>
                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="venueParking">
                                <span>Parking Information (Optional)</span>
                            </label>
                            <textarea
                                name="venueParking"
                                id="venueParking"
                                class="edit-card-field-textarea"
                                value={formData.venueParking}></textarea>
                        </div>
                        <div class="divider divider-accent">Venue Gallery</div>
                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="venueGalleryTitle">
                                <span>Gallery Title</span>
                            </label>
                            <input
                                type="text"
                                name="venueGalleryTitle"
                                id="venueGalleryTitle"
                                class="edit-card-field-input"
                                value={formData.venueGalleryTitle} />
                        </div>
                        <div class="form-control w-full">
                            <label class="edit-card-field-name" for="venueGalleryDescription">
                                <span>Gallery Description</span>
                            </label>
                            <textarea
                                name="venueGalleryDescription"
                                id="venueGalleryDescription"
                                class="edit-card-field-textarea"
                                value={formData.venueGalleryDescription}></textarea>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="flex gap-4 mt-6 justify-end">
            <a href="/planning/config" class="btn btn-error">Cancel</a>
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
</ProtectedPageShell>
