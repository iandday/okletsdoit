import { createApiClient } from "$lib/server/api-client";
import { fail, redirect } from "@sveltejs/kit";
import type { Actions } from "./$types";

export const actions = {
    default: async ({ request, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const name = formData.get("name");
        const description = formData.get("description");

        if (!name) {
            return fail(400, { error: "Name is required" });
        }

        let idea;
        try {
            idea = await api.core.coreApiCreateIdea({
                ideaCreateSchema: {
                    name: name && typeof name === "string" ? name : "",
                    description: description && typeof description === "string" ? description : undefined,
                },
            });
        } catch (err) {
            console.error("Failed to create idea:", err);
            return fail(500, { error: "Failed to create idea" });
        }

        throw redirect(303, `/settings/idea/${idea.id}`);
    },
} satisfies Actions;
