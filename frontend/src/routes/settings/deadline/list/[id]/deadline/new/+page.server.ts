import { createApiClient } from "$lib/server/api-client";
import { fail, redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
    const api = createApiClient(locals.sessionCookie);
    return {
        listId: params.id,
        listName: (await api.deadlines.deadlineApiGetDeadlineList({ listId: params.id })).name,
    };
};

export const actions = {
    default: async ({ request, params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const listId = params.id;
        const formData = await request.formData();
        const name = formData.get("name");
        const description = formData.get("description");
        const dueDate = formData.get("dueDate");
        const completed = formData.get("completed") === "on";

        if (!name || typeof name !== "string") {
            return fail(400, { error: "Deadline name is required" });
        }

        try {
            await api.deadlines.deadlineApiCreateDeadline({
                deadlineCreateSchema: {
                    name,
                    description: description && typeof description === "string" ? description : undefined,
                    deadlineListId: listId,
                    dueDate: dueDate && typeof dueDate === "string" ? new Date(dueDate) : undefined,
                    completed,
                },
            });
        } catch (err) {
            console.error("Failed to create deadline:", err);
            return fail(500, { error: "Failed to create deadline" });
        }

        throw redirect(303, `/settings/deadline/list/${listId}`);
    },
} satisfies Actions;
