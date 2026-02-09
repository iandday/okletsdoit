import { createApiClient } from "$lib/server/api-client";
import { error, fail, redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
    const api = createApiClient(locals.sessionCookie);
    try {
        const category = await api.expenses.expensesApiGetCategory({
            categoryId: params.id,
        });

        // Load all expenses for this category
        const expenses = [];
        let page = 1;
        const pageSize = 100;
        let hasMore = true;

        while (hasMore) {
            const expensesResponse = await api.expenses.expensesApiListExpenses({
                categoryId: params.id,
                page,
                pageSize,
            });

            expenses.push(...(expensesResponse.items || []));
            hasMore = (expensesResponse.items?.length || 0) === pageSize;
            page++;
        }

        const totalEstimated = expenses.reduce((sum, e) => sum + Number(e.estimatedAmount || 0), 0);
        const totalActual = expenses.reduce((sum, e) => sum + Number(e.actualAmount || 0), 0);

        return {
            category,
            expenses,
            totalEstimated,
            totalActual,
            variance: totalActual - totalEstimated,
        };
    } catch (err) {
        console.error("Error loading category:", err);
        throw error(404, "Category not found");
    }
};

export const actions = {
    delete: async ({ params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        try {
            await api.expenses.expensesApiDeleteCategory({
                categoryId: params.id,
            });
        } catch (err) {
            console.error("Failed to delete category:", err);
            return fail(500, { error: "Failed to delete category" });
        }

        throw redirect(303, "/planning/budget");
    },
} satisfies Actions;
