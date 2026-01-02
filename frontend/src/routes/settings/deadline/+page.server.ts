import { api } from "$lib/server/api-client";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async () => {
    const deadlineLists = await api.deadlines.deadlineApiListDeadlineLists({});

    return {
        deadlineLists: deadlineLists.items || [],
    };
};
