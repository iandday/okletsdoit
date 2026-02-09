import { createApiClient } from "$lib/server/api-client";
import { error, fail, redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
    const api = createApiClient(locals.sessionCookie);
    try {
        const inspiration = await api.core.coreApiGetInspiration({
            inspirationId: params.id,
        });

        return {
            inspiration,
        };
    } catch (err) {
        console.error("Error loading inspiration:", err);
        throw error(404, "Inspiration not found");
    }
};

export const actions = {
    delete: async ({ params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        try {
            await api.core.coreApiDeleteInspiration({
                inspirationId: params.id,
            });
        } catch (err) {
            console.error("Failed to delete inspiration:", err);
            return fail(500, { error: "Failed to delete inspiration" });
        }

        throw redirect(303, "/planning/inspiration");
    },
} satisfies Actions;
