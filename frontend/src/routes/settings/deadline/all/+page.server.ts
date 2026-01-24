import { api } from "$lib/server/api-client";
import { error, redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "../deadline/all/$types";
import type { Actions } from "./$types";

export const load: PageServerLoad = async ({ url }) => {
    const deadlineListId = url.searchParams.get("list");
    const page = parseInt(url.searchParams.get("page") || "1", 10);
    const pageSize = parseInt(url.searchParams.get("pageSize") || "50", 10);

    const deadlines = await api.deadlines.deadlineApiListDeadlines({
        deadlineListId: deadlineListId || undefined,
        page,
        pageSize,
    });

    return {
        deadlines,
        filterListId: deadlineListId,
        currentPage: page,
        pageSize,
    };
};

export const actions: Actions = {
    deleteDeadline: async ({ params, request }) => {
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

        throw redirect(303, "/settings/deadline/all");
    },
};
