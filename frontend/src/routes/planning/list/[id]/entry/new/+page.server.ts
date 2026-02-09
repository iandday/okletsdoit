import { createApiClient } from "$lib/server/api-client";
import { fail, redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
    const api = createApiClient(locals.sessionCookie);
    const listId = params.id;

    try {
        const list = await api.list.listApiGetList({ listId });

        // Load vendors (contacts) for the dropdown
        const vendorsResponse = await api.contacts.contactsApiListContacts({});

        return {
            list,
            vendors: vendorsResponse.items || [],
        };
    } catch (err) {
        console.error("Failed to load data:", err);
        throw new Error("Failed to load list or vendors");
    }
};

export const actions = {
    default: async ({ request, params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const listId = params.id;
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
            await api.list.listApiCreateListEntry({
                listEntryCreateSchema: {
                    item,
                    description: description && typeof description === "string" ? description : undefined,
                    listId,
                    quantity: quantity && typeof quantity === "string" ? parseInt(quantity) : 1,
                    unitPrice: unitPrice && typeof unitPrice === "string" ? unitPrice : "0.00",
                    additionalPrice: additionalPrice && typeof additionalPrice === "string" ? additionalPrice : "0.00",
                    url: url && typeof url === "string" ? url : undefined,
                    isCompleted,
                    purchased,
                    vendorId: vendorId && typeof vendorId === "string" && vendorId !== "" ? vendorId : undefined,
                },
            });
        } catch (err) {
            console.error("Failed to create list entry:", err);
            return fail(500, { error: "Failed to create list entry" });
        }

        throw redirect(303, `/planning/list/${listId}`);
    },
} satisfies Actions;
