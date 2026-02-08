import { createApiClient } from "$lib/server/api-client";
import { fail, redirect } from "@sveltejs/kit";
import { error } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
    const ideaId = params.id;
    const api = createApiClient(locals.sessionCookie);

    try {
        const idea = await api.core.coreApiGetIdea({ ideaId });

        return {
            idea,
        };
    } catch (err) {
        console.error("Failed to load idea:", err);
        throw error(404, "Idea not found");
    }
};

export const actions = {
    default: async ({ request, params, locals }) => {
        const ideaId = params.id;
        const formData = await request.formData();
        const name = formData.get("name");
        const description = formData.get("description");

        if (!name) {
            return fail(400, { error: "Name is required" });
        }

        const api = createApiClient(locals.sessionCookie);

        try {
            await api.core.coreApiUpdateIdea({
                ideaId,
                ideaUpdateSchema: {
                    name: name && typeof name === "string" ? name : undefined,
                    description: description && typeof description === "string" ? description : undefined,
                },
            });
        } catch (err) {
            console.error("Failed to update idea:", err);
            return fail(500, { error: "Failed to update idea" });
        }

        throw redirect(303, `/settings/idea/${ideaId}`);
    },
} satisfies Actions;
