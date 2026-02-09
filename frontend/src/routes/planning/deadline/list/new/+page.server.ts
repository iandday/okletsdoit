import { createApiClient } from "$lib/server/api-client";
import { fail, redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async () => {
    return {};
};

export const actions = {
    default: async ({ request, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const name = formData.get("name");

        if (!name || typeof name !== "string") {
            return fail(400, { error: "List name is required" });
        }

        let newList;
        try {
            newList = await api.deadlines.deadlineApiCreateDeadlineList({
                deadlineListCreateSchema: { name },
            });
        } catch (err) {
            console.error("Failed to create deadline list:", err);
            return fail(500, { error: "Failed to create deadline list" });
        }

        throw redirect(303, `/planning/deadline/list/${newList.id}`);
    },
} satisfies Actions;
