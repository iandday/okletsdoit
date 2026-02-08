import { createApiClient } from "$lib/server/api-client";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {
    const api = createApiClient(locals.sessionCookie);
    const contacts = await api.contacts.contactsApiListContacts({});

    // For each contact, fetch their attachments
    const contactsWithAttachments = await Promise.all(
        (contacts.items || []).map(async (contact) => {
            const attachments = await api.attachments.attachmentsApiListAttachments({
                objectId: contact.id,
            });

            return {
                ...contact,
                attachments: attachments.items || [],
            };
        }),
    );

    return {
        contacts: contactsWithAttachments,
    };
};
