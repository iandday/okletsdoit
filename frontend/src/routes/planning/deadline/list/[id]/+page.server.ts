import { createApiClient } from "$lib/server/api-client";
import { error, fail, redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
    const api = createApiClient(locals.sessionCookie);
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

export const actions: Actions = {
    delete: async ({ params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const listId = params.id;

        try {
            while (true) {
                const response = await api.deadlines.deadlineApiListDeadlines({
                    deadlineListId: listId,
                    page: 1,
                    pageSize: 100,
                });

                const deadlines = response.items || [];
                if (deadlines.length === 0) {
                    break;
                }

                await Promise.all(
                    deadlines.map((deadline) =>
                        api.deadlines.deadlineApiDeleteDeadline({
                            deadlineId: deadline.id,
                        }),
                    ),
                );
            }

            await api.deadlines.deadlineApiDeleteDeadlineList({ listId });
        } catch (err) {
            console.error("Failed to delete deadline list and associated deadlines:", err);
            return fail(500, { error: "Failed to delete deadline list" });
        }

        throw redirect(303, "/planning/deadline");
    },
};
