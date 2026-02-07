import { createApiClient } from "$lib/server/api-client";
import { redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
    const api = createApiClient(locals.sessionCookie);
    const expense = await api.expenses.expensesApiGetExpense({ expenseId: params.id });

    // Load categories and vendors for dropdowns
    let categories: any[] = [];
    let vendors: any[] = [];

    // Load all categories
    let page = 1;
    const pageSize = 100;
    let hasMore = true;
    while (hasMore) {
        const response = await api.expenses.expensesApiListCategories({ page, pageSize });
        categories = categories.concat(response.items || []);
        hasMore = (response.items?.length || 0) === pageSize;
        page++;
    }

    // Load all contacts (vendors)
    page = 1;
    hasMore = true;
    while (hasMore) {
        const response = await api.contacts.contactsApiListContacts({ page, pageSize });
        vendors = vendors.concat(response.items || []);
        hasMore = (response.items?.length || 0) === pageSize;
        page++;
    }

    return {
        expense,
        categories,
        vendors,
    };
};

export const actions: Actions = {
    default: async ({ request, params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();

        const item = formData.get("item") as string;
        const description = formData.get("description") as string;
        const categoryId = formData.get("category") as string;
        const vendorId = formData.get("vendor") as string;
        const date = formData.get("date") as string;
        const quantity = formData.get("quantity") as string;
        const unitPrice = formData.get("unitPrice") as string;
        const additionalPrice = formData.get("additionalPrice") as string;
        let estimatedAmount = formData.get("estimatedAmount") as string;
        const actualAmount = formData.get("actualAmount") as string;
        const url = formData.get("url") as string;

        // Calculate estimatedAmount if not provided
        if (!estimatedAmount && quantity && unitPrice) {
            const qty = Number(quantity);
            const price = Number(unitPrice);
            const additional = additionalPrice ? Number(additionalPrice) : 0;
            estimatedAmount = String(qty * price + additional);
        }

        await api.expenses.expensesApiUpdateExpense({
            expenseId: params.id,
            expenseUpdateSchema: {
                item,
                description: description || undefined,
                categoryId: categoryId || undefined,
                vendorId: vendorId || undefined,
                date: date ? new Date(date) : undefined,
                quantity: quantity ? Number(quantity) : undefined,
                unitPrice: unitPrice || undefined,
                additionalPrice: additionalPrice || undefined,
                estimatedAmount: estimatedAmount || undefined,
                actualAmount: actualAmount || undefined,
                url: url || undefined,
            },
        });

        throw redirect(303, `/settings/budget/expense/${params.id}`);
    },
};
