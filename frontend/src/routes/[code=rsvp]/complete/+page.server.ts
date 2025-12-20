// frontend/src/routes/[code=rsvp]/complete/+page.server.ts
import { api } from "$lib/server/api-client";
import { error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, url }) => {
    const { code } = params;
    const configData = await api.core.coreApiGetWeddingSettings();
    const accepted = url.searchParams.get("accepted");

    const data = await api.guestlist.guestlistApiListGuestGroups({
        rsvpCode: code,
    });

    if (data.items && data.items.length == 1) {

        if (accepted === "true") {
            return {
                accepted: true,
            };
        } else if (accepted === "false") {

            const rsvpDecline = await api.guestlist.guestlistApiDeclineRsvp({
                rsvpCode: code,
            });
            if (rsvpDecline.success) {
                return {
                    accepted: false,
                };
            } else {
                throw error(400, "Failed to record RSVP decline");
            }
        } else {
            throw error(404, "RSVP code not found");
        }
    };
    throw error(404, "RSVP code not found");
}
