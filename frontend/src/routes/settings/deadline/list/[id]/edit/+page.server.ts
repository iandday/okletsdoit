import { api } from "$lib/server/api-client";
import { fail, redirect } from "@sveltejs/kit";
import { error } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params }) => {
    const listId = params.id;

    try {
        const deadlineList = await api.deadlines.deadlineApiGetDeadlineList({ listId });

        return {
            deadlineList,
        };
    } catch (err) {
        console.error("Failed to load deadline list:", err);
        throw error(404, "Deadline list not found");
    }
};

export const actions = {
    default: async ({ request, params }) => {
        const listId = params.id;
        const formData = await request.formData();
        const name = formData.get("name");

        if (!name || typeof name !== "string") {
            return fail(400, { error: "List name is required" });
        }

        try {
            await api.deadlines.deadlineApiUpdateDeadlineList({
                listId,
                deadlineListUpdateSchema: { name },
            });
        } catch (err) {
            console.error("Failed to update deadline list:", err);
            return fail(500, { error: "Failed to update deadline list" });
        }

        throw redirect(303, `/settings/deadline/list/${listId}`);
    },
} satisfies Actions;
