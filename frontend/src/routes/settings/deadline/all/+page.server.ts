import { api } from "$lib/server/api-client";
import type { PageServerLoad } from "../deadline/all/$types";

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
