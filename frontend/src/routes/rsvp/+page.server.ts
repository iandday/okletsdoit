import { createApiClient } from "$lib/server/api-client";
import { fail, redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";
import { getconfigData } from "$lib/server/config-data";

export const load: PageServerLoad = async ({ locals }) => {
    const api = createApiClient(locals.sessionCookie);
    const configData = await getconfigData();

    if (!configData?.enableRsvp) {
        throw redirect(302, "/");
    }
    return {
        allowRsvp: configData.allowRsvp,
    };
};

export const actions: Actions = {
    default: async ({ request, locals }) => {
        const api = createApiClient(locals.sessionCookie);
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
