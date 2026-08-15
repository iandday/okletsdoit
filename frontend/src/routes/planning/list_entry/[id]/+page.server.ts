import { createApiClient } from "$lib/server/api-client";
import { error, fail, redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
    const api = createApiClient(locals.sessionCookie);
    try {
        const entry = await api.list.listApiGetListEntry({
            entryId: params.id,
        });

        const attachmentsResponse = await api.attachments.attachmentsApiListAttachments({
            objectId: entry.id,
        });
        const attachments = (attachmentsResponse.items || []).map((attachment) => ({
            ...attachment,
            downloadUrl: attachment.downloadUrl,
        }));

        const list = await api.list.listApiGetList({
            listId: entry.listId,
        });
        let vendor = null;
        if (entry.vendorId) {
            try {
                vendor = await api.contacts.contactsApiGetContact({
                    contactId: entry.vendorId,
                });
            } catch (err) {
                console.error("Failed to load vendor:", err);
            }
        }

        return {
            entry,
            list,
            vendor,
            attachments,
        };
    } catch (err) {
        console.error("Error loading list entry:", err);
        throw error(404, "List entry not found");
    }
};

export const actions = {
    delete: async ({ params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const entry = await api.list.listApiGetListEntry({
            entryId: params.id,
        });

        try {
            await api.list.listApiDeleteListEntry({
                entryId: params.id,
            });
        } catch (err) {
            console.error("Failed to delete list entry:", err);
            return fail(500, { error: "Failed to delete list entry" });
        }

        throw redirect(303, `/planning/list/${entry.listId}`);
    },
    toggleCompleted: async ({ params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        try {
            const result = await api.list.listApiToggleCompleted({
                entryId: params.id,
            });
            return { success: true };
        } catch (err) {
            console.error("Failed to toggle completed status:", err);
            return fail(500, { error: "Failed to update status" });
        }
    },
    togglePurchased: async ({ params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        try {
            const result = await api.list.listApiTogglePurchased({
                entryId: params.id,
            });
            return { success: true };
        } catch (err) {
            console.error("Failed to toggle purchased status:", err);
            return fail(500, { error: "Failed to update purchased status" });
        }
    },
    uploadAttachment: async ({ params, request, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const file = formData.get("file") as File;
        const name = formData.get("name") as string;
        const description = formData.get("description") as string;

        if (!file || file.size === 0) {
            return fail(400, { error: "Please select a file to upload" });
        }

        try {
            await api.attachments.attachmentsApiCreateAttachment({
                file,
                appLabel: "list",
                model: "listentry",
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
            return fail(500, {
                error: "Failed to upload attachment",
                details: err?.message || String(err),
            });
        }
    },
    deleteAttachment: async ({ request, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const attachmentId = formData.get("attachmentId") as string;

        if (!attachmentId) {
            return fail(400, { error: "Attachment ID is required" });
        }

        try {
            await api.attachments.attachmentsApiDeleteAttachment({
                attachmentId,
            });

            return { success: true };
        } catch (err) {
            console.error("Failed to delete attachment:", err);
            return fail(500, { error: "Failed to delete attachment" });
        }
    },
} satisfies Actions;
