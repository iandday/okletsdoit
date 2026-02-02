import { api } from "$lib/server/api-client";
import type { Actions, PageServerLoad } from "./$types";
import { redirect } from "@sveltejs/kit";

export const load: PageServerLoad = async ({ params }) => {
    const expense = await api.expenses.expensesApiGetExpense({ expenseId: params.id });

    // Load related objects
    let category = null;
    let vendor = null;
    let list = null;

    if (expense.categoryId) {
        category = await api.expenses.expensesApiGetCategory({ categoryId: expense.categoryId });
    }

    if (expense.vendorId) {
        vendor = await api.contacts.contactsApiGetContact({ contactId: expense.vendorId });
    }

    // Note: list is not on expense schema, removed that check

    return {
        expense,
        category,
        vendor,
        list,
    };
};

export const actions: Actions = {
    delete: async ({ params }) => {
        await api.expenses.expensesApiDeleteExpense({ expenseId: params.id });
        throw redirect(303, "/settings/budget");
    },
};
