import { api } from "$lib/server/api-client";
import { error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params }) => {
    const { code } = params;
    console.error("Loading RSVP code:", code);
    // Query the API for guest group by RSVP code
    const data = await api.guestlist.guestlistApiListGuestGroups({
        rsvpCode: code,
    });
    const config_data = await api.core.coreApiGetWeddingSettings();

    if (config_data.allowRsvp === false) {
        throw error(404, "It's not time to RSVP yet!");
    }

    if (!data.items || data.items.length === 0) {
        throw error(404, "RSVP code not found");
    }
    else

        return {
            guestGroups: data.items,
        };
};
