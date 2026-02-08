import { createApiClient } from "$lib/server/api-client";
import { fail, redirect } from "@sveltejs/kit";
import { error } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
    const api = createApiClient(locals.sessionCookie);
    const listId = params.id;

    try {
        const list = await api.list.listApiGetList({ listId });

        return {
            list,
        };
    } catch (err) {
        console.error("Failed to load list:", err);
        throw error(404, "List not found");
    }
};

export const actions = {
    default: async ({ request, params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const listId = params.id;
        const formData = await request.formData();
        const name = formData.get("name");
        const description = formData.get("description");

        if (!name || typeof name !== "string") {
            return fail(400, { error: "Name is required" });
        }

        try {
            await api.list.listApiUpdateList({
                listId,
                listUpdateSchema: {
                    name,
                    description: description && typeof description === "string" ? description : undefined,
                },
            });
        } catch (err) {
            console.error("Failed to update list:", err);
            return fail(500, { error: "Failed to update list" });
        }

        throw redirect(303, `/settings/list/${listId}`);
    },
} satisfies Actions;
