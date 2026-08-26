import { createApiClient } from "$lib/server/api-client";
import { fail } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {
    const api = createApiClient(locals.sessionCookie);
    const timelines = await api.core.coreApiListTimelines({});
    console.log("Loaded timelines:", timelines.items);
    return {
        timelines: timelines.items || [],
    };
};

export const actions = {
    create: async ({ request, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();

        const name = (formData.get("name") as string | null)?.trim() || "";
        const description = (formData.get("description") as string | null) ?? "";
        const startRaw = (formData.get("start") as string | null) ?? "";
        const endRaw = (formData.get("end") as string | null) ?? "";

        const parseDateValue = (raw: string) => {
            if (!raw) return null;
            const parsed = new Date(raw);
            return Number.isNaN(parsed.getTime()) ? null : parsed;
        };

        const start = parseDateValue(startRaw);
        const end = parseDateValue(endRaw);

        if (!name || !start) {
            return fail(400, { error: "Name and start time are required" });
        }

        try {
            const created = await api.core.coreApiCreateTimeline({
                timelineCreateSchema: {
                    name,
                    description,
                    start,
                    end,
                    published: false,
                    confirmed: false,
                },
            });

            return { success: true, created };
        } catch (error) {
            console.error("Failed to create timeline:", error);
            return fail(500, { error: "Failed to create timeline event" });
        }
    },

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

            const parseDateValue = (raw: string) => {
                if (!raw) return null;
                const parsed = new Date(raw);
                return Number.isNaN(parsed.getTime()) ? null : parsed;
            };

            // Single field update (for toggles)
            if (field && value !== null) {
                if (field === "published" || field === "confirmed") {
                    updateData[field] = value === "true";
                } else if (field === "order") {
                    updateData[field] = parseInt(value, 10);
                } else if (field === "start" || field === "end") {
                    updateData[field] = parseDateValue(value);
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
                if (start) updateData.start = parseDateValue(start);
                // Allow clearing the end time by sending null when empty.
                if (formData.has("end")) updateData.end = parseDateValue(end);
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
