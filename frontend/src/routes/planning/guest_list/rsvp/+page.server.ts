import { createApiClient } from "$lib/server/api-client";
import type { PageServerLoad } from "./$types";

async function fetchAllPages<T>(
    fetcher: (page: number) => Promise<{ items?: T[] | null; count?: number | null }>,
): Promise<T[]> {
    const all: T[] = [];
    let page = 1;
    while (true) {
        const response = await fetcher(page);
        if (response.items && response.items.length > 0) {
            all.push(...response.items);
            if (all.length >= (response.count || 0)) break;
            page++;
        } else {
            break;
        }
    }
    return all;
}

export const load: PageServerLoad = async ({ locals }) => {
    const api = createApiClient(locals.sessionCookie);
    try {
        const [guestGroups, submissions, responses] = await Promise.all([
            fetchAllPages((page) => api.guestlist.guestlistApiListGuestGroups({ page, pageSize: 100 })),
            fetchAllPages((page) => api.guestlist.guestlistApiListRsvpSubmissions({ page, pageSize: 100 })),
            fetchAllPages((page) => api.guestlist.guestlistApiListRsvpResponses({ page, pageSize: 100 })),
        ]);
        const stats = await api.guestlist.guestlistApiGetRsvpStats();
        console.log(stats);
        return {
            guestGroups,
            submissions,
            responses,
            stats,
        };
    } catch (error) {
        console.error("Error loading RSVP data:", error);
        return {
            guestGroups: [],
            submissions: [],
            responses: [],
            stats: {
                totalSubmissions: 0,
                totalWithEmail: 0,
                totalAttending: 0,
                totalAccommodation: 0,
                totalVipAccepted: 0,
            },
        };
    }
};
