import { createApiClient } from "$lib/server/api-client";
import { error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {
    const api = createApiClient(locals.sessionCookie);
    try {
        // Load all categories
        const categories = [];
        let page = 1;
        const pageSize = 100;
        let hasMore = true;

        while (hasMore) {
            const categoriesResponse = await api.expenses.expensesApiListCategories({
                page,
                pageSize,
            });

            categories.push(...(categoriesResponse.items || []));
            hasMore = (categoriesResponse.items?.length || 0) === pageSize;
            page++;
        }

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

        // Calculate breakdown by category
        const categoryBreakdown = categories.map((category) => {
            const categoryExpenses = expenses.filter((e) => e.categoryId === category.id);
            const totalEstimated = categoryExpenses.reduce((sum, e) => sum + Number(e.estimatedAmount || 0), 0);
            const totalActual = categoryExpenses.reduce((sum, e) => sum + Number(e.actualAmount || 0), 0);

            return {
                category,
                expenseCount: categoryExpenses.length,
                totalEstimated,
                totalActual,
                variance: totalActual - totalEstimated,
            };
        });

        // Add uncategorized expenses
        const uncategorizedExpenses = expenses.filter((e) => !e.categoryId);
        if (uncategorizedExpenses.length > 0) {
            const totalEstimated = uncategorizedExpenses.reduce((sum, e) => sum + Number(e.estimatedAmount || 0), 0);
            const totalActual = uncategorizedExpenses.reduce((sum, e) => sum + Number(e.actualAmount || 0), 0);

            categoryBreakdown.push({
                category: {
                    id: "uncategorized",
                    name: "Uncategorized",
                    slug: "uncategorized",
                },
                expenseCount: uncategorizedExpenses.length,
                totalEstimated,
                totalActual,
                variance: totalActual - totalEstimated,
            });
        }

        const totalEstimated = expenses.reduce((sum, e) => sum + Number(e.estimatedAmount || 0), 0);
        const totalActual = expenses.reduce((sum, e) => sum + Number(e.actualAmount || 0), 0);

        return {
            categoryBreakdown,
            totalEstimated,
            totalActual,
            totalVariance: totalActual - totalEstimated,
            totalExpenses: expenses.length,
        };
    } catch (err) {
        console.error("Error loading budget data:", err);
        throw error(500, "Failed to load budget data");
    }
};
