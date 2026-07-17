// frontend/src/routes/venue/+page.server.ts
import { createApiClient } from "$lib/server/api-client";
import { getconfigData } from "$lib/server/config-data";
import { redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {
    const configData = await getconfigData();
    const api = createApiClient(locals.sessionCookie);
    const timelines = await api.core.coreApiListTimelines({
        published: true,
    });
    const accommodationsResponse = await api.core.coreApiListAccommodations({});

    if (!configData?.enableVenue) {
        throw redirect(302, "/");
    }

    return {
        timelines: timelines.items || [],
        accommodations: accommodationsResponse.items || [],
    };
};
