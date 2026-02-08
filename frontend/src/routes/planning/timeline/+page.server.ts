import { createApiClient } from "$lib/server/api-client";
import { fail } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {
    const api = createApiClient(locals.sessionCookie);
    const timelines = await api.core.coreApiListTimelines({});

    return {
        timelines: timelines.items || [],
    };
};

export const actions = {
    update: async ({ request, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const id = formData.get("id") as string;

        // Handle single field update (for toggle buttons)
        const field = formData.get("field") as string;
        const value = formData.get("value") as string;

        if (!id) {
            return fail(400, { error: "Missing required fields" });
        }

        try {
            const updateData: any = {};

            // Single field update (for toggles)
            if (field && value !== null) {
                if (field === "published" || field === "confirmed") {
                    updateData[field] = value === "true";
                } else if (field === "order") {
                    updateData[field] = parseInt(value, 10);
                } else if (field === "start" || field === "end") {
                    updateData[field] = value;
                } else if (field === "name" || field === "description") {
                    updateData[field] = value;
                }
            } else {
                // Multi-field update (from edit modal)
                const name = formData.get("name") as string;
                const description = formData.get("description") as string;
                const start = formData.get("start") as string;
                const end = formData.get("end") as string;

                if (name) updateData.name = name;
                if (description !== null) updateData.description = description;
                if (start) updateData.start = start;
                if (end) updateData.end = end;
            }

            await api.core.coreApiUpdateTimeline({
                timelineId: id,
                timelineUpdateSchema: updateData,
            });

            return { success: true };
        } catch (error) {
            console.error("Failed to update timeline:", error);
            return fail(500, { error: "Failed to update timeline event" });
        }
    },

    delete: async ({ request, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const id = formData.get("id") as string;

        if (!id) {
            return fail(400, { error: "Missing timeline ID" });
        }

        try {
            await api.core.coreApiDeleteTimeline({ timelineId: id });
            return { success: true };
        } catch (error) {
            console.error("Failed to delete timeline:", error);
            return fail(500, { error: "Failed to delete timeline event" });
        }
    },
} satisfies Actions;
