import { createApiClient } from "$lib/server/api-client";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {
    const api = createApiClient(locals.sessionCookie);
    // Fetch all published timelines for the venue preview

    const timelines = await api.core.coreApiListTimelines({
        published: true,
    });

    // Note: After regenerating the OpenAPI client, this will fetch accommodations
    // For now, it will return an empty array until the API client is regenerated
    let accommodations = [];
    try {
        const accommodationsResponse = await api.core.coreApiListAccommodations({});
        accommodations = accommodationsResponse.items || [];
    } catch (err) {
        console.log("Accommodations API not yet available - will be available after OpenAPI regeneration");
    }

    return {
        timelines: timelines.items || [],
        accommodations,
    };
};
