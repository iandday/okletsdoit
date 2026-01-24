import { api } from "$lib/server/api-client";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async () => {
    try {
        // Fetch all pages of guest groups
        let allGuestGroups: any[] = [];
        let page = 1;
        let totalCount = 0;

        while (true) {
            const response = await api.guestlist.guestlistApiListGuestGroups({
                page,
                pageSize: 100,
            });

            if (response.items && response.items.length > 0) {
                allGuestGroups = allGuestGroups.concat(response.items);
                totalCount = response.count || 0;

                if (allGuestGroups.length >= totalCount) {
                    break;
                }

                page++;
            } else {
                break;
            }
        }

        return {
            guestGroups: allGuestGroups,
            count: totalCount,
        };
    } catch (error) {
        console.error("Error loading guest groups:", error);
        return {
            guestGroups: [],
            count: 0,
        };
    }
};
