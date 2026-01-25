import { api } from "$lib/server/api-client";
import { error, fail, redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params }) => {
    try {
        const guest = await api.guestlist.guestlistApiGetGuest({
            guestId: params.id,
        });

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
        console.error("Error loading guest:", err);
        throw error(404, "Guest not found");
    }
};

export const actions: Actions = {
    delete: async ({ params }) => {
        try {
            const guest = await api.guestlist.guestlistApiGetGuest({
                guestId: params.id,
            });

            await api.guestlist.guestlistApiDeleteGuest({
                guestId: params.id,
            });

            // Redirect to the guest group if available, otherwise to guest list
            if (guest.groupId) {
                throw redirect(303, `/settings/guest_list/${guest.groupId}`);
            }
        } catch (err) {
            console.error("Failed to delete guest:", err);
            return fail(500, { error: "Failed to delete guest" });
        }

        throw redirect(303, "/settings/guest_list");
    },
};
