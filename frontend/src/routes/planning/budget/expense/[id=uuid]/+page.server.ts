import { createApiClient } from "$lib/server/api-client";
import { redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
    const api = createApiClient(locals.sessionCookie);
    const expense = await api.expenses.expensesApiGetExpense({ expenseId: params.id });

    const attachmentsResponse = await api.attachments.attachmentsApiListAttachments({
        objectId: expense.id,
    });
    const attachments = (attachmentsResponse.items || []).map((attachment) => ({
        ...attachment,
        downloadUrl: attachment.downloadUrl,
    }));

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
        attachments,
    };
};

export const actions: Actions = {
    delete: async ({ params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        await api.expenses.expensesApiDeleteExpense({ expenseId: params.id });
        throw redirect(303, "/planning/budget");
    },
    uploadAttachment: async ({ params, request, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const file = formData.get("file") as File;
        const name = formData.get("name") as string;
        const description = formData.get("description") as string;

        if (!file || file.size === 0) {
            return { success: false, error: "Please select a file to upload" };
        }

        try {
            await api.attachments.attachmentsApiCreateAttachment({
                file,
                appLabel: "expenses",
                model: "expense",
                objectId: params.id,
                name: name || null,
                description: description || null,
            });

            return { success: true };
        } catch (err: any) {
            console.error("Failed to upload attachment:", {
                message: err?.message,
                status: err?.status,
                statusText: err?.statusText,
                body: err?.body,
            });
            return {
                success: false,
                error: "Failed to upload attachment",
                details: err?.message || String(err),
            };
        }
    },
    deleteAttachment: async ({ request, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const attachmentId = formData.get("attachmentId") as string;

        if (!attachmentId) {
            return { success: false, error: "Attachment ID is required" };
        }

        try {
            await api.attachments.attachmentsApiDeleteAttachment({
                attachmentId,
            });
            return { success: true };
        } catch (err) {
            console.error("Failed to delete attachment:", err);
            return { success: false, error: "Failed to delete attachment" };
        }
    },
};
