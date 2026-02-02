import { api } from "$lib/server/api-client";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async () => {
    try {
        // Fetch all pages of lists
        let allLists: any[] = [];
        let page = 1;
        let totalCount = 0;

        while (true) {
            const response = await api.list.listApiListLists({
                page,
                pageSize: 100,
            });

            if (response.items && response.items.length > 0) {
                allLists = allLists.concat(response.items);
                totalCount = response.count || 0;

                if (allLists.length >= totalCount) {
                    break;
                }

                page++;
            } else {
                break;
            }
        }

        // Fetch all list entries to determine which lists have expenses
        let allEntries: any[] = [];
        page = 1;

        while (true) {
            const response = await api.list.listApiListListEntries({
                page,
                pageSize: 100,
            });

            if (response.items && response.items.length > 0) {
                allEntries = allEntries.concat(response.items);

                if (allEntries.length >= (response.count || 0)) {
                    break;
                }

                page++;
            } else {
                break;
            }
        }

        // Map list IDs to whether they have expenses
        const listHasExpenses = new Map<string, boolean>();
        for (const entry of allEntries) {
            if (entry.associatedExpenseId) {
                listHasExpenses.set(entry.listId, true);
            }
        }

        // Add hasExpenses property to each list
        const listsWithExpenseInfo = allLists.map((list) => ({
            ...list,
            hasExpenses: listHasExpenses.get(list.id) || false,
        }));

        return {
            lists: listsWithExpenseInfo,
            count: totalCount,
        };
    } catch (error) {
        console.error("Error loading lists:", error);
        return {
            lists: [],
            count: 0,
        };
    }
};
