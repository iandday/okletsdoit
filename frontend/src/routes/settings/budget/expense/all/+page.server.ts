import { api } from "$lib/server/api-client";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async () => {
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

    for (const categoryId of categoryIds) {
        try {
            const category = await api.expenses.expensesApiGetCategory({ categoryId });
            categoryMap.set(categoryId, category);
        } catch (error) {
            console.error(`Failed to load category ${categoryId}:`, error);
        }
    }

    const enrichedExpenses = expenses.map((expense) => ({
        ...expense,
        categoryName: expense.categoryId ? categoryMap.get(expense.categoryId)?.name : null,
    }));

    // Calculate totals
    const totalEstimated = expenses.reduce(
        (sum, e) => sum + (e.estimatedAmount ? Number(e.estimatedAmount) : 0),
        0
    );
    const totalActual = expenses.reduce(
        (sum, e) => sum + (e.actualAmount ? Number(e.actualAmount) : 0),
        0
    );
    const variance = totalActual - totalEstimated;

    return {
        expenses: enrichedExpenses,
        totalExpenses: expenses.length,
        totalEstimated,
        totalActual,
        variance,
    };
};
