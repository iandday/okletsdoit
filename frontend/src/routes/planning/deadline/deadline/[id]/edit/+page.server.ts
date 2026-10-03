import { createApiClient } from "$lib/server/api-client";
import { fail, redirect } from "@sveltejs/kit";
import { error } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
    const api = createApiClient(locals.sessionCookie);
    const deadlineId = params.id;

    try {
        const deadline = await api.deadlines.deadlineApiGetDeadline({ deadlineId });
        const assigneeMap = new Map<string, string>();
        if (deadline.assignedToId && deadline.assignedToName) {
            assigneeMap.set(deadline.assignedToId, deadline.assignedToName);
        }

        let page = 1;
        while (true) {
            const response = await api.deadlines.deadlineApiListDeadlines({ page, pageSize: 100 });
            for (const item of response.items ?? []) {
                if (item.assignedToId && item.assignedToName) {
                    assigneeMap.set(item.assignedToId, item.assignedToName);
                }
            }

            if (!response.items?.length || page * 100 >= response.count) {
                break;
            }
            page++;
        }

        return {
            deadline,
            assigneeOptions: Array.from(assigneeMap.entries())
                .map(([id, name]) => ({ id, name }))
                .sort((a, b) => a.name.localeCompare(b.name)),
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
        const assignedToId = formData.get("assignedToId");
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
                    assignedToId: typeof assignedToId === "string" && assignedToId ? assignedToId : null,
                    completed,
                    completedNote: completedNote && typeof completedNote === "string" ? completedNote : undefined,
                },
            });
        } catch (err) {
            console.error("Failed to update deadline:", err);
            return fail(500, { error: "Failed to update deadline" });
        }

        const redirectPath = updatedDeadline.deadlineListId
            ? `/planning/deadline/list/${updatedDeadline.deadlineListId}`
            : "/planning/deadline";

        throw redirect(303, redirectPath);
    },
} satisfies Actions;
