import { api } from "$lib/server/api-client";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async () => {
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
