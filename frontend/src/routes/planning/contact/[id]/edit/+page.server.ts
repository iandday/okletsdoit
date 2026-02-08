import { createApiClient } from "$lib/server/api-client";
import { fail, redirect } from "@sveltejs/kit";
import { error } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
    const api = createApiClient(locals.sessionCookie);
    const contactId = params.id;

    try {
        const contact = await api.contacts.contactsApiGetContact({ contactId });

        return {
            contact,
        };
    } catch (err) {
        console.error("Failed to load contact:", err);
        throw error(404, "Contact not found");
    }
};

export const actions = {
    default: async ({ request, params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const contactId = params.id;
        const formData = await request.formData();
        const name = formData.get("name");
        const company = formData.get("company");
        const email = formData.get("email");
        const phone = formData.get("phone");
        const website = formData.get("website");
        const category = formData.get("category");
        const notes = formData.get("notes");

        if (!name && !company) {
            return fail(400, { error: "Either name or company is required" });
        }

        try {
            await api.contacts.contactsApiUpdateContact({
                contactId,
                contactUpdateSchema: {
                    name: name && typeof name === "string" ? name : undefined,
                    company: company && typeof company === "string" ? company : undefined,
                    email: email && typeof email === "string" ? email : undefined,
                    phone: phone && typeof phone === "string" ? phone : undefined,
                    website: website && typeof website === "string" ? website : undefined,
                    category: category && typeof category === "string" ? category : undefined,
                    notes: notes && typeof notes === "string" ? notes : undefined,
                },
            });
        } catch (err) {
            console.error("Failed to update contact:", err);
            return fail(500, { error: "Failed to update contact" });
        }

        throw redirect(303, `/settings/contact/${contactId}`);
    },
} satisfies Actions;
