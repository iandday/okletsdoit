import { createApiClient } from "$lib/server/api-client";
import { error, redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
    const api = createApiClient(locals.sessionCookie);
    try {
        const list = await api.list.listApiGetList({
            listId: params.id,
        });

        // Load all list entries for this list
        const entries = [];
        let page = 1;
        const pageSize = 100;
        let hasMore = true;

        while (hasMore) {
            const entriesResponse = await api.list.listApiListListEntries({
                listId: params.id,
                page,
                pageSize,
            });

            entries.push(...(entriesResponse.items || []));
            hasMore = (entriesResponse.items?.length || 0) === pageSize;
            page++;
        }

        // Fetch vendor information for entries that have a vendorId
        const vendorIds = [...new Set(entries.filter((e) => e.vendorId).map((e) => e.vendorId))];
        const vendors = new Map();

        for (const vendorId of vendorIds) {
            try {
                const vendor = await api.contacts.contactsApiGetContact({ contactId: vendorId! });
                vendors.set(vendorId, vendor);
            } catch (err) {
                console.error(`Failed to load vendor ${vendorId}:`, err);
            }
        }

        // Attach vendor info to entries
        const entriesWithVendors = entries.map((entry) => ({
            ...entry,
            vendor: entry.vendorId ? vendors.get(entry.vendorId) : null,
        }));

        return {
            list,
            entries: entriesWithVendors,
        };
    } catch (err) {
        console.error("Error loading list:", err);
        throw error(404, "List not found");
    }
};

export const actions: Actions = {
    delete: async ({ params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        try {
            await api.list.listApiDeleteList({
                listId: params.id,
            });
        } catch (err) {
            console.error("Error deleting list:", err);
            throw error(500, "Failed to delete list");
        }

        throw redirect(303, "/planning/list");
    },
};
