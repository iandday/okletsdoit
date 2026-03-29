import { createApiClient } from "$lib/server/api-client";
import { error, redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";
import type { Actions } from "./$types";

export const load: PageServerLoad = async ({ url, locals }) => {
    const api = createApiClient(locals.sessionCookie);
    const deadlineListId = url.searchParams.get("list");
    const assigneeId = url.searchParams.get("assignee");
    const search = url.searchParams.get("search")?.trim() || "";
    const status = url.searchParams.get("status") || "all";
    const statusFilter = ["all", "pending", "overdue", "completed"].includes(status) ? status : "all";

    const deadlineLists = await api.deadlines.deadlineApiListDeadlineLists({ page: 1, pageSize: 500 });

    const assigneeSource = await api.deadlines.deadlineApiListDeadlines({ page: 1, pageSize: 500 });
    const assigneeMap = new Map<string, string>();
    for (const deadline of assigneeSource.items) {
        if (deadline.assignedToId && deadline.assignedToName) {
            assigneeMap.set(deadline.assignedToId, deadline.assignedToName);
        }
    }
    const assigneeOptions = Array.from(assigneeMap.entries())
        .map(([id, name]) => ({ id, name }))
        .sort((a, b) => a.name.localeCompare(b.name));

    let completed: boolean | undefined;
    let overdue: boolean | undefined;

    if (statusFilter === "completed") {
        completed = true;
    } else if (statusFilter === "overdue") {
        overdue = true;
    } else if (statusFilter === "pending") {
        completed = false;
        overdue = false;
    }

    let allDeadlines: any[] = [];
    let page = 1;
    let totalCount = 0;

    while (true) {
        const response = await api.deadlines.deadlineApiListDeadlines({
            deadlineListId: deadlineListId || undefined,
            assignedToId: assigneeId || undefined,
            search: search || undefined,
            page,
            pageSize: 100,
            overdue,
            completed,
        });

        if (response.items && response.items.length > 0) {
            allDeadlines = allDeadlines.concat(response.items);
            totalCount = response.count || 0;

            if (allDeadlines.length >= totalCount) {
                break;
            }

            page++;
        } else {
            break;
        }
    }

    return {
        deadlines: allDeadlines,
        count: totalCount,
        deadlineLists: deadlineLists.items,
        assigneeOptions,
        filterListId: deadlineListId,
        filterAssigneeId: assigneeId,
        filterStatus: statusFilter,
        filterSearch: search,
    };
};

export const actions: Actions = {
    deleteDeadline: async ({ params, request, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const deadlineID = formData.get("value") as string;
        try {
            await api.deadlines.deadlineApiDeleteDeadline({
                deadlineId: deadlineID,
            });
        } catch (err) {
            console.error("Error deleting deadline:", err);
            throw error(500, "Failed to delete deadline");
        }

        throw redirect(303, "/planning/deadline/all");
    },
};
