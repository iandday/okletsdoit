import { createApiClient } from "$lib/server/api-client";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {
    const api = createApiClient(locals.sessionCookie);
    const timelines = await api.core.coreApiListTimelines({
        published: true,
    });

    const accommodationsResponse = await api.core.coreApiListAccommodations({});

    return {
        timelines: timelines.items || [],
        accommodations: accommodationsResponse.items || [],
    };
};
