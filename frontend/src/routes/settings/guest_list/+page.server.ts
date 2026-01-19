import { api } from "$lib/server/api-client";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async () => {
    try {
        const response = await api.guestlist.guestlistApiListGuestGroups({
            page: 1,
            pageSize: 100, // Get all guest groups for the summary view
        });

        return {
            guestGroups: response.items || [],
            count: response.count || 0,
        };
    } catch (error) {
        console.error("Error loading guest groups:", error);
        return {
            guestGroups: [],
            count: 0,
        };
    }
};
