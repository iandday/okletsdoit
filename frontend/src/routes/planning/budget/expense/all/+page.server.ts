import { createApiClient } from "$lib/server/api-client";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {
    const api = createApiClient(locals.sessionCookie);
    // Load all expenses
    let expenses: any[] = [];
    let page = 1;
    const pageSize = 100;
    let hasMore = true;

    while (hasMore) {
        const response = await api.expenses.expensesApiListExpenses({ page, pageSize });
        expenses = expenses.concat(response.items || []);
        hasMore = (response.items?.length || 0) === pageSize;
        page++;
    }

    // Enrich with category data
    const categoryIds = [...new Set(expenses.map((e) => e.categoryId).filter(Boolean))];
    const categoryMap = new Map();

    console.log(`Loading ${categoryIds.length} unique categories for ${expenses.length} expenses`);
    console.log("Category IDs:", categoryIds);

    for (const categoryId of categoryIds) {
        try {
            console.log(`Fetching category: ${categoryId}`);
            const category = await api.expenses.expensesApiGetCategory({ categoryId });
            console.log(`Successfully loaded category ${categoryId}:`, category.name);
            categoryMap.set(categoryId, category);
        } catch (error) {
            console.error(`Failed to load category ${categoryId}:`, error);
            const affectedExpenses = expenses.filter((e) => e.categoryId === categoryId);
            console.error(
                `  Affected expenses (${affectedExpenses.length}):`,
                affectedExpenses.map((e) => ({ id: e.id, item: e.item })),
            );
            // Set a placeholder so we know it was attempted
            categoryMap.set(categoryId, { name: "Deleted Category", id: categoryId });
        }
    }

    const enrichedExpenses = expenses.map((expense) => ({
        ...expense,
        categoryName: expense.categoryId ? categoryMap.get(expense.categoryId)?.name : null,
    }));

    // Calculate totals
    const totalEstimated = expenses.reduce((sum, e) => sum + (e.estimatedAmount ? Number(e.estimatedAmount) : 0), 0);
    const totalActual = expenses.reduce((sum, e) => sum + (e.actualAmount ? Number(e.actualAmount) : 0), 0);
    const variance = totalActual - totalEstimated;

    return {
        expenses: enrichedExpenses,
        totalExpenses: expenses.length,
        totalEstimated,
        totalActual,
        variance,
    };
};
