import { api } from "$lib/server/api-client";
import { redirect, error } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ url }) => {
    try {
        // Get categoryId from query string if provided
        const categoryId = url.searchParams.get("categoryId");

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
        try {
            page = 1;
            hasMore = true;
            while (hasMore) {
                const response = await api.contacts.contactsApiListContacts({ page, pageSize });
                vendors = vendors.concat(response.items || []);
                hasMore = (response.items?.length || 0) === pageSize;
                page++;
            }
        } catch (err) {
            console.error("Error loading vendors:", err);
            // Continue without vendors if contacts API fails
        }

        return {
            categories,
            vendors,
            preselectedCategoryId: categoryId,
        };
    } catch (err) {
        console.error("Error loading new expense form data:", err);
        throw error(500, "Failed to load form data");
    }
};

export const actions: Actions = {
    default: async ({ request }) => {
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

        const expense = await api.expenses.expensesApiCreateExpense({
            expenseCreateSchema: {
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

        throw redirect(303, `/settings/budget/expense/${expense.id}`);
    },
};
