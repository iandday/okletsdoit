import { createApiClient } from "$lib/server/api-client";
import { error } from "@sveltejs/kit";
import type { Actions } from "./$types";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {
    const api = createApiClient(locals.sessionCookie);
    try {
        const pageSize = 100;

        // Load guest groups
        let page = 1;
        let guestGroups: any[] = [];
        let hasMore = true;
        while (true) {
            const response = await api.guestlist.guestlistApiListGuestGroups({
                page,
                pageSize,
            });

            if (response.items && response.items.length > 0) {
                guestGroups = guestGroups.concat(response.items);
                const totalCount = response.count || 0;

                if (guestGroups.length >= totalCount) {
                    break;
                }

                page++;
            } else {
                break;
            }
        }

        // Load deadlineStats
        const deadlineStats = await api.deadlines.deadlineApiGetDeadlineStats();
        if (!deadlineStats) {
            throw error(500, "Failed to load deadline statistics");
        }

        // Load all categories
        const categories = [];
        page = 1;
        hasMore = true;

        // Load all expenses
        const expenses = [];
        page = 1;
        hasMore = true;

        while (hasMore) {
            const expensesResponse = await api.expenses.expensesApiListExpenses({
                page,
                pageSize,
            });

            expenses.push(...(expensesResponse.items || []));
            hasMore = (expensesResponse.items?.length || 0) === pageSize;
            page++;
        }

        const budgetEstimated = expenses.reduce((sum, e) => sum + Number(e.estimatedAmount || 0), 0);
        const budgetActual = expenses.reduce((sum, e) => sum + Number(e.actualAmount || 0), 0);
        // load all lists
        const lists = [];
        page = 1;
        hasMore = true;
        while (hasMore) {
            const listsResponse = await api.list.listApiListLists({
                page,
                pageSize,
            });

            lists.push(...(listsResponse.items || []));
            hasMore = (listsResponse.items?.length || 0) === pageSize;
            page++;
        }

        return {
            budgetEstimated,
            budgetActual,
            guestGroups,
            deadlineStats,
            lists,
        };
    } catch (err) {
        console.error("Error loading budget data:", err);
        throw error(500, "Failed to load budget data");
    }
};

export const actions: Actions = {
    sendUpdateEmail: async ({ locals }) => {
        const api = createApiClient(locals.sessionCookie);
        try {
            const result = await api.core.coreApiTriggerSendUpdateEmail();
            return {
                success: true,
                message: result.message,
                taskId: result.taskId,
            };
        } catch (error) {
            console.error("Error sending update email:", error);
            return {
                success: false,
                error: "Failed to send update email",
            };
        }
    },
};
