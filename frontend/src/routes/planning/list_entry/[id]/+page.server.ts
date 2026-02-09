import { createApiClient } from "$lib/server/api-client";
import { error, fail, redirect } from "@sveltejs/kit";
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
} satisfies Actions;
