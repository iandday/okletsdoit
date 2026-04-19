import { createApiClient } from "$lib/server/api-client";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {
    const api = createApiClient(locals.sessionCookie);
    const contacts = await api.contacts.contactsApiListContacts({});

    // For each contact, fetch their attachments
    const contactsWithAttachments = await Promise.all(
        (contacts.items || []).map(async (contact) => {
            const attachmentsResponse = await api.attachments.attachmentsApiListAttachments({
                objectId: contact.id,
            });
            const attachments = (attachmentsResponse.items || []).map((attachment) => ({
                ...attachment,
                downloadUrl: attachment.downloadUrl,
            }));

            return {
                ...contact,
                attachments,
            };
        }),
    );

    return {
        contacts: contactsWithAttachments,
    };
};
