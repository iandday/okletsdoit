import { api } from "$lib/server/api-client";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ url }) => {
    try {
        // Get optional list ID from query parameter
        const listId = url.searchParams.get("listId");

        // Fetch all pages of list entries
        let allEntries: any[] = [];
        let page = 1;
        let totalCount = 0;

        while (true) {
            const response = await api.list.listApiListListEntries({
                listId: listId || undefined,
                page,
                pageSize: 100,
            });

            if (response.items && response.items.length > 0) {
                allEntries = allEntries.concat(response.items);
                totalCount = response.count || 0;

                if (allEntries.length >= totalCount) {
                    break;
                }

                page++;
            } else {
                break;
            }
        }

        // Fetch all lists for the filter dropdown
        let allLists: any[] = [];
        page = 1;

        while (true) {
            const listsResponse = await api.list.listApiListLists({
                page,
                pageSize: 100,
            });

            if (listsResponse.items && listsResponse.items.length > 0) {
                allLists = allLists.concat(listsResponse.items);

                if (allLists.length >= (listsResponse.count || 0)) {
                    break;
                }

                page++;
            } else {
                break;
            }
        }

        return {
            entries: allEntries,
            count: totalCount,
            lists: allLists,
            selectedListId: listId,
        };
    } catch (error) {
        console.error("Error loading list entries:", error);
        return {
            entries: [],
            count: 0,
            lists: [],
            selectedListId: null,
        };
    }
};
