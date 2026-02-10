import { createApiClient } from "$lib/server/api-client";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {
    const api = createApiClient(locals.sessionCookie);
    const deadlineLists = await api.deadlines.deadlineApiListDeadlineLists({});

    return {
        deadlineLists: deadlineLists.items || [],
    };
};
