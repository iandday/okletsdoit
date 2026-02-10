import { createApiClient } from "$lib/server/api-client";
import { error, fail, redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
    const api = createApiClient(locals.sessionCookie);
    try {
        const deadline = await api.deadlines.deadlineApiGetDeadline({
            deadlineId: params.id,
        });

        return {
            deadline,
        };
    } catch (err) {
        console.error("Error loading deadline:", err);
        throw error(404, "Deadline not found");
    }
};

export const actions = {
    toggleComplete: async ({ params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        try {
            await api.deadlines.deadlineApiToggleDeadlineComplete({
                deadlineId: params.id,
            });
        } catch (err) {
            console.error("Failed to toggle deadline completion:", err);
            return fail(500, { error: "Failed to toggle completion status" });
        }

        return { success: true };
    },
    delete: async ({ params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        let deadline;
        try {
            deadline = await api.deadlines.deadlineApiGetDeadline({
                deadlineId: params.id,
            });

            await api.deadlines.deadlineApiDeleteDeadline({
                deadlineId: params.id,
            });
        } catch (err) {
            console.error("Failed to delete deadline:", err);
            return fail(500, { error: "Failed to delete deadline" });
        }

        const redirectPath = deadline.deadlineListId
            ? `/planning/deadline/list/${deadline.deadlineListId}`
            : "/planning/deadline";

        throw redirect(303, redirectPath);
    },
} satisfies Actions;
