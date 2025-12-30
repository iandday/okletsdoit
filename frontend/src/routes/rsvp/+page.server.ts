import { api } from "$lib/server/api-client";
import { fail, redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async () => {
    const config_data = await api.core.coreApiGetWeddingSettings();

    return {
        allowRsvp: config_data.allowRsvp,
    };
};

export const actions: Actions = {
    default: async ({ request }) => {
        const formData = await request.formData();
        const code = formData.get("code")?.toString()?.toUpperCase();

        if (!code) {
            return fail(400, { error: "RSVP code is required", code: "" });
        }
        if (!/^[A-Z0-9]{10}$/.test(code)) {
            return fail(400, { error: "Invalid RSVP code format", code });
        }

        const data = await api.guestlist.guestlistApiListGuestGroups({
            rsvpCode: code,
        });
        if (!data.items || data.items.length === 0) {
            return fail(404, { error: "RSVP code not found", code });
        }
        throw redirect(303, `/${code}`);
    },
};
