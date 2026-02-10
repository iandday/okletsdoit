import { createApiClient } from "$lib/server/api-client";
import { getconfigData } from "$lib/server/config-data";
import { error, redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, url, locals }) => {
    const api = createApiClient(locals.sessionCookie);
    const { code } = params;
    const config_data = await getconfigData();
    const accepted = url.searchParams.get("accepted");
    if (!config_data) {
        throw error(500, "Failed to load configuration data");
    }
    if (config_data.allowRsvp === false) {
        throw error(404, "It's not time to RSVP yet!");
    }

    const data = await api.guestlist.guestlistApiListGuestGroups({
        rsvpCode: code,
    });

    if (data.items && data.items.length == 1) {
        return {
            guestData: data.items[0],
            accepted: accepted === null ? null : accepted === "true",
        };
    } else {
        throw error(404, "RSVP code not found");
    }
};
