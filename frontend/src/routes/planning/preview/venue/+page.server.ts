import { createApiClient } from "$lib/server/api-client";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {
    const api = createApiClient(locals.sessionCookie);
    // Fetch all published timelines for the venue preview

    const timelines = await api.core.coreApiListTimelines({
        published: true,
    });

    return {
        timelines: timelines.items || [],
    };
};
