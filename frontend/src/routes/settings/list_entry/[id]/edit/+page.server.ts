import { createApiClient } from "$lib/server/api-client";
import { fail, redirect } from "@sveltejs/kit";
import { error } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
    const api = createApiClient(locals.sessionCookie);
    try {
        const entry = await api.list.listApiGetListEntry({
            entryId: params.id,
        });

        const list = await api.list.listApiGetList({
            listId: entry.listId,
        });

        // Load vendors (contacts) for the dropdown
        const vendorsResponse = await api.contacts.contactsApiListContacts({});

        return {
            entry,
            list,
            vendors: vendorsResponse.items || [],
        };
    } catch (err) {
        console.error("Failed to load list entry:", err);
        throw error(404, "List entry not found");
    }
};

export const actions = {
    default: async ({ request, params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const entryId = params.id;
        const formData = await request.formData();

        const item = formData.get("item");
        const description = formData.get("description");
        const quantity = formData.get("quantity");
        const unitPrice = formData.get("unitPrice");
        const additionalPrice = formData.get("additionalPrice");
        const url = formData.get("url");
        const isCompleted = formData.get("isCompleted") === "on";
        const purchased = formData.get("purchased") === "on";
        const vendorId = formData.get("vendorId");

        if (!item || typeof item !== "string") {
            return fail(400, { error: "Item name is required" });
        }

        try {
            await api.list.listApiUpdateListEntry({
                entryId: entryId,
                listEntryUpdateSchema: {
                    item,
                    description: description && typeof description === "string" ? description : undefined,
                    quantity: quantity && typeof quantity === "string" ? parseInt(quantity) : undefined,
                    unitPrice: unitPrice && typeof unitPrice === "string" ? unitPrice : undefined,
                    additionalPrice:
                        additionalPrice && typeof additionalPrice === "string" ? additionalPrice : undefined,
                    url: url && typeof url === "string" && url !== "" ? url : undefined,
                    isCompleted,
                    purchased,
                    vendorId: vendorId && typeof vendorId === "string" && vendorId !== "" ? vendorId : undefined,
                },
            });
        } catch (err) {
            console.error("Failed to update list entry:", err);
            return fail(500, { error: "Failed to update list entry" });
        }

        throw redirect(303, `/settings/list_entry/${entryId}`);
    },
} satisfies Actions;
