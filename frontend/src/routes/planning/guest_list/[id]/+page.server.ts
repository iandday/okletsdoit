import { createApiClient } from "$lib/server/api-client";
import { error, redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
    const api = createApiClient(locals.sessionCookie);
    try {
        const guestGroup = await api.guestlist.guestlistApiGetGuestGroup({
            groupId: params.id,
        });

        // Load all guests for this group
        const guests = [];
        let page = 1;
        const pageSize = 100;
        let hasMore = true;

        while (hasMore) {
            const guestsResponse = await api.guestlist.guestlistApiListGuests({
                groupId: params.id,
                page,
                pageSize,
            });

            guests.push(...(guestsResponse.items || []));
            hasMore = (guestsResponse.items?.length || 0) === pageSize;
            page++;
        }

        return {
            guestGroup,
            guests,
        };
    } catch (err) {
        console.error("Error loading guest group:", err);
        throw error(404, "Guest group not found");
    }
};

export const actions: Actions = {
    delete: async ({ params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        try {
            await api.guestlist.guestlistApiDeleteGuestGroup({
                groupId: params.id,
            });
        } catch (err) {
            console.error("Error deleting guest group:", err);
            throw error(500, "Failed to delete guest group");
        }

        throw redirect(303, "/planning/guest_list");
    },
    deleteGuest: async ({ request, params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const guestId = formData.get("value") as string;

        if (!guestId) {
            throw error(400, "Guest ID is required");
        }
        try {
            await api.guestlist.guestlistApiDeleteGuest({
                guestId: guestId,
            });
        } catch (err) {
            console.error("Error deleting guest:", err);
            throw error(500, "Failed to delete guest");
        }
    },
    addGuest: async ({ params, request, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const firstName = formData.get("firstName") as string;
        const lastName = formData.get("lastName") as string;
        const invited = formData.get("invited") === "on";
        const vip = formData.get("vip") === "on";
        const accommodation = formData.get("accommodation") === "on";
        const notes = formData.get("notes") as string;
        const plusOne = formData.get("plusOne") === "on";

        if (!plusOne && (!firstName || !lastName)) {
            throw error(400, "First name and last name are required when not adding a plus one");
        }

        try {
            await api.guestlist.guestlistApiCreateGuest({
                guestCreateSchema: {
                    firstName: firstName,
                    lastName: lastName,
                    groupId: params.id,
                    isInvited: invited,
                    vip: vip,
                    accommodation: accommodation,
                    notes: notes || null,
                    plusOne: plusOne,
                },
            });
        } catch (err) {
            console.error("Error adding guest:", err);
            throw error(500, "Failed to add guest");
        }
    },
};
