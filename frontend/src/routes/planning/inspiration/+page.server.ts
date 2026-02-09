import { createApiClient } from "$lib/server/api-client";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ url, locals }) => {
    const api = createApiClient(locals.sessionCookie);
    try {
        // Get optional name filter from query parameter
        const nameFilter = url.searchParams.get("name");

        // Fetch all pages of inspirations
        let allInspirations: any[] = [];
        let page = 1;
        let totalCount = 0;

        while (true) {
            const response = await api.core.coreApiListInspirations({
                name: nameFilter || undefined,
                page,
                pageSize: 50,
            });

            if (response.items && response.items.length > 0) {
                allInspirations = allInspirations.concat(response.items);
                totalCount = response.count || 0;

                if (allInspirations.length >= totalCount) {
                    break;
                }

                page++;
            } else {
                break;
            }
        }

        return {
            inspirations: allInspirations,
            count: totalCount,
            nameFilter: nameFilter,
        };
    } catch (error) {
        console.error("Error loading inspirations:", error);
        return {
            inspirations: [],
            count: 0,
            nameFilter: null,
        };
    }
};
