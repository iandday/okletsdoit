import { api } from "$lib/server/api-client";
import { fail, redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

const formatDateForInput = (date: Date | string | null | undefined): string | null => {
    if (!date) return null;
    const d = typeof date === "string" ? new Date(date) : date;
    if (isNaN(d.getTime())) return null;
    return d.toISOString().split("T")[0];
};

export const load: PageServerLoad = async ({ parent }) => {
    const { configData } = await parent();

    return {
        configData: configData
            ? {
                  ...configData,
                  weddingDate: formatDateForInput(configData.weddingDate),
                  rsvpStartDate: formatDateForInput(configData.rsvpStartDate),
                  rsvpEndDate: formatDateForInput(configData.rsvpEndDate),
              }
            : null,
    };
};

export const actions = {
    default: async ({ request }) => {
        const formData = await request.formData();

        // Helper to convert date strings to Date objects or null
        const parseDate = (value: FormDataEntryValue | null): Date | null => {
            if (!value || typeof value !== "string" || value === "") return null;
            const date = new Date(value);
            return isNaN(date.getTime()) ? null : date;
        };

        // Convert form data to the correct types
        const data = {
            weddingDate: parseDate(formData.get("weddingDate")),
            allowRsvp: formData.get("allowRsvp") === "on",
            allowPhotos: formData.get("allowPhotos") === "on",
            showFaq: formData.get("showFaq") === "on",
            showVenue: formData.get("showVenue") === "on",
            rsvpStartDate: parseDate(formData.get("rsvpStartDate")),
            rsvpEndDate: parseDate(formData.get("rsvpEndDate")),
            rsvpAcceptButton: formData.get("rsvpAcceptButton") as string,
            rsvpDeclineButton: formData.get("rsvpDeclineButton") as string,
            rsvpAttendingLabel: formData.get("rsvpAttendingLabel") as string,
            rsvpAccommodationLabel: formData.get("rsvpAccommodationLabel") as string,
            rsvpVipLabel: formData.get("rsvpVipLabel") as string,
            standardGroupLabel: formData.get("standardGroupLabel") as string,
            vipGroupLabel: formData.get("vipGroupLabel") as string,
            rsvpEmailUpdateLabel: formData.get("rsvpEmailUpdateLabel") as string,
            rsvpAcceptIntro: formData.get("rsvpAcceptIntro") as string,
            rsvpAcceptSuccessMessage: formData.get("rsvpAcceptSuccessMessage") as string,
            rsvpDeclineSuccessMessage: formData.get("rsvpDeclineSuccessMessage") as string,
            rsvpAccommodationIntro: formData.get("rsvpAccommodationIntro") as string,
            rsvpVipIntro: formData.get("rsvpVipIntro") as string,
            rsvpSuccessHeadline: formData.get("rsvpSuccessHeadline") as string,
            rsvpShowAccommodationIntro: formData.get("rsvpShowAccommodationIntro") === "on",
            rsvpShowVipIntro: formData.get("rsvpShowVipIntro") === "on",
            rsvpEnableEmailUpdates: formData.get("rsvpEnableEmailUpdates") === "on",
            venuePageTitle: formData.get("venuePageTitle") as string,
            venuePageDescription: formData.get("venuePageDescription") as string,
            venueName: formData.get("venueName") as string,
            venueAddressLineOne: formData.get("venueAddressLineOne") as string,
            venueAddressLineTwo: formData.get("venueAddressLineTwo") as string,
            venueCity: formData.get("venueCity") as string,
            venueState: formData.get("venueState") as string,
            venueZipcode: formData.get("venueZipcode") as string,
            venueCountry: formData.get("venueCountry") as string,
            venueParking: formData.get("venueParking") as string,
            venueGalleryTitle: formData.get("venueGalleryTitle") as string,
            venueGalleryDescription: formData.get("venueGalleryDescription") as string,
        };

        try {
            await api.core.coreApiUpdateWeddingSettings({
                weddingSettingsUpdateSchema: data,
            });
        } catch (error) {
            return fail(500, {
                error: error instanceof Error ? error.message : "Failed to update settings",
            });
        }

        throw redirect(303, "/settings/config");
    },
} satisfies Actions;
