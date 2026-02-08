import { createApiClient } from "$lib/server/api-client";
import { fail, redirect } from "@sveltejs/kit";
import type { Actions } from "./$types";

export const actions = {
    default: async ({ request, locals }) => {
        const api = createApiClient(locals.sessionCookie);
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

        let contact;
        try {
            contact = await api.contacts.contactsApiCreateContact({
                contactCreateSchema: {
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
            console.error("Failed to create contact:", err);
            return fail(500, { error: "Failed to create contact" });
        }

        throw redirect(303, `/settings/contact/${contact.id}`);
    },
} satisfies Actions;
