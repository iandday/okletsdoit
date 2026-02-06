import { api } from "$lib/server/api-client";
import { redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params }) => {
    const expense = await api.expenses.expensesApiGetExpense({ expenseId: params.id });

    // Load related objects
    let category = null;
    let vendor = null;
    let listEntries: any[] = [];
    let purchaseStatus = false;

    if (expense.categoryId) {
        category = await api.expenses.expensesApiGetCategory({ categoryId: expense.categoryId });
    }

    if (expense.vendorId) {
        vendor = await api.contacts.contactsApiGetContact({ contactId: expense.vendorId });
    }

    // Load list entries associated with this expense
    let page = 1;
    const pageSize = 100;
    let hasMore = true;
    while (hasMore) {
        const response = await api.list.listApiListListEntries({
            associatedExpenseId: params.id,
            page,
            pageSize,
        });
        listEntries = listEntries.concat(response.items || []);
        hasMore = (response.items?.length || 0) === pageSize;
        page++;
    }

    // purchaseStatus is true if all associated list entries are purchased or if there are no entries and the expense totalPrice is not equal to zero
    if (listEntries.length === 0 && Number(expense.actualAmount) > 0) {
        purchaseStatus = true;
    } else {
        purchaseStatus = listEntries.length > 0 && listEntries.every((entry) => entry.purchased);
    }
    return {
        expense,
        category,
        vendor,
        listEntries,
        purchaseStatus,
    };
};

export const actions: Actions = {
    delete: async ({ params }) => {
        await api.expenses.expensesApiDeleteExpense({ expenseId: params.id });
        throw redirect(303, "/settings/budget");
    },
};
