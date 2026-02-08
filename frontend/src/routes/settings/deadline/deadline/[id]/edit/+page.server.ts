import { createApiClient } from "$lib/server/api-client";
import { fail, redirect } from "@sveltejs/kit";
import { error } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
    const api = createApiClient(locals.sessionCookie);
    const deadlineId = params.id;

    try {
        const deadline = await api.deadlines.deadlineApiGetDeadline({ deadlineId });

        return {
            deadline,
        };
    } catch (err) {
        console.error("Failed to load deadline:", err);
        throw error(404, "Deadline not found");
    }
};

export const actions = {
    default: async ({ request, params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const deadlineId = params.id;
        const formData = await request.formData();
        const name = formData.get("name");
        const description = formData.get("description");
        const dueDate = formData.get("dueDate");
        const completed = formData.get("completed") === "on";
        const completedNote = formData.get("completedNote");

        if (!name || typeof name !== "string") {
            return fail(400, { error: "Deadline name is required" });
        }

        let updatedDeadline;
        try {
            updatedDeadline = await api.deadlines.deadlineApiUpdateDeadline({
                deadlineId,
                deadlineUpdateSchema: {
                    name,
                    description: description && typeof description === "string" ? description : undefined,
                    dueDate: dueDate && typeof dueDate === "string" ? new Date(dueDate) : undefined,
                    completed,
                    completedNote: completedNote && typeof completedNote === "string" ? completedNote : undefined,
                },
            });
        } catch (err) {
            console.error("Failed to update deadline:", err);
            return fail(500, { error: "Failed to update deadline" });
        }

        const redirectPath = updatedDeadline.deadlineListId
            ? `/settings/deadline/list/${updatedDeadline.deadlineListId}`
            : "/settings/deadline";

        throw redirect(303, redirectPath);
    },
} satisfies Actions;
