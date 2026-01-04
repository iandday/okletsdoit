import { api } from "$lib/server/api-client";
import { error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params }) => {
    const listId = params.id;

    try {
        const [deadlineList, deadlines] = await Promise.all([
            api.deadlines.deadlineApiGetDeadlineList({ listId }),
            api.deadlines.deadlineApiListDeadlines({ deadlineListId: listId }),
        ]);

        return {
            deadlineList,
            deadlines: deadlines.items || [],
        };
    } catch (err) {
        console.error("Failed to load deadline list:", err);
        throw error(404, "Deadline list not found");
    }
};
