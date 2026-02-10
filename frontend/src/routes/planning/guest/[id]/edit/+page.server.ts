import { createApiClient } from "$lib/server/api-client";
import { fail, redirect } from "@sveltejs/kit";
import { error } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
    const api = createApiClient(locals.sessionCookie);
    const guestId = params.id;

    try {
        const guest = await api.guestlist.guestlistApiGetGuest({ guestId });

        // Load the guest group to get additional context
        let guestGroup = null;
        if (guest.groupId) {
            try {
                guestGroup = await api.guestlist.guestlistApiGetGuestGroup({
                    groupId: guest.groupId,
                });
            } catch (err) {
                console.error("Error loading guest group:", err);
            }
        }

        return {
            guest,
            guestGroup,
        };
    } catch (err) {
        console.error("Failed to load guest:", err);
        throw error(404, "Guest not found");
    }
};

export const actions: Actions = {
    default: async ({ request, params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const guestId = params.id;
        const formData = await request.formData();
        const firstName = formData.get("firstName");
        const lastName = formData.get("lastName");
        const plusOne = formData.get("plusOne") === "on";
        const isInvited = formData.get("isInvited") === "on";
        const vip = formData.get("vip") === "on";
        const accommodation = formData.get("accommodation") === "on";
        const notes = formData.get("notes");

        if (!plusOne && (!firstName || !lastName)) {
            return fail(400, { error: "First name and last name are required" });
        }

        try {
            await api.guestlist.guestlistApiUpdateGuest({
                guestId,
                guestUpdateSchema: {
                    firstName: firstName && typeof firstName === "string" ? firstName : undefined,
                    lastName: lastName && typeof lastName === "string" ? lastName : undefined,
                    plusOne,
                    isInvited,
                    vip,
                    accommodation,
                    notes: notes && typeof notes === "string" ? notes : undefined,
                },
            });
        } catch (err) {
            console.error("Failed to update guest:", err);
            return fail(500, { error: "Failed to update guest" });
        }

        throw redirect(303, `/planning/guest/${guestId}`);
    },
};
