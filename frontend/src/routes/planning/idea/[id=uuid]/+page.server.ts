import { createApiClient } from "$lib/server/api-client";
import { error, fail, redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
    const api = createApiClient(locals.sessionCookie);
    try {
        const idea = await api.core.coreApiGetIdea({
            ideaId: params.id,
        });
        console.log(idea);
        return {
            idea,
        };
    } catch (err) {
        console.error("Error loading idea:", err);
        throw error(404, "Idea not found");
    }
};

export const actions = {
    delete: async ({ params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        try {
            await api.core.coreApiDeleteIdea({
                ideaId: params.id,
            });
        } catch (err) {
            console.error("Failed to delete idea:", err);
            return fail(500, { error: "Failed to delete idea" });
        }

        throw redirect(303, "/planning/idea");
    },
} satisfies Actions;
