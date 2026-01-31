import { api } from "$lib/server/api-client";
import { error, fail, redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params }) => {
    try {
        const contact = await api.contacts.contactsApiGetContact({
            contactId: params.id,
        });

        const attachments = await api.attachments.attachmentsApiListAttachments({
            objectId: contact.id,
        });

        return {
            contact,
            attachments: attachments.items || [],
        };
    } catch (err) {
        console.error("Error loading contact:", err);
        throw error(404, "Contact not found");
    }
};

export const actions = {
    delete: async ({ params }) => {
        try {
            await api.contacts.contactsApiDeleteContact({
                contactId: params.id,
            });
        } catch (err) {
            console.error("Failed to delete contact:", err);
            return fail(500, { error: "Failed to delete contact" });
        }

        throw redirect(303, "/settings/contact");
    },
    uploadAttachment: async ({ params, request }) => {
        const formData = await request.formData();
        const file = formData.get("file") as File;
        const name = formData.get("name") as string;
        const description = formData.get("description") as string;

        if (!file || file.size === 0) {
            return fail(400, { error: "Please select a file to upload" });
        }

        console.log(`[Upload] File: ${file.name}, Size: ${file.size} bytes, Type: ${file.type}`);

        try {
            console.log(`[Upload] Uploading to object: ${params.id}`);

            const result = await api.attachments.attachmentsApiCreateAttachment({
                file: file,
                appLabel: "contacts",
                model: "contact",
                objectId: params.id,
                name: name || null,
                description: description || null,
            });

            console.log(`[Upload] Success! Attachment ID: ${result.id}`);
            return { success: true };
        } catch (err: any) {
            console.error("[Upload] Error details:", {
                message: err?.message,
                status: err?.status,
                statusText: err?.statusText,
                body: err?.body,
                stack: err?.stack,
            });
            return fail(500, {
                error: "Failed to upload attachment",
                details: err?.message || String(err),
            });
        }
    },
    deleteAttachment: async ({ request }) => {
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
