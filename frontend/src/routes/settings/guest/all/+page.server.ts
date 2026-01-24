import { api } from "$lib/server/api-client";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async () => {
    try {
        // Fetch all pages of guests and guest groups in parallel
        const fetchAllGuests = async () => {
            let allGuests: any[] = [];
            let page = 1;

            while (true) {
                const response = await api.guestlist.guestlistApiListGuests({
                    page,
                    pageSize: 100,
                });

                if (response.items && response.items.length > 0) {
                    allGuests = allGuests.concat(response.items);

                    if (allGuests.length >= (response.count || 0)) {
                        break;
                    }

                    page++;
                } else {
                    break;
                }
            }

            return allGuests;
        };

        const fetchAllGroups = async () => {
            let allGroups: any[] = [];
            let page = 1;

            while (true) {
                const response = await api.guestlist.guestlistApiListGuestGroups({
                    page,
                    pageSize: 100,
                });

                if (response.items && response.items.length > 0) {
                    allGroups = allGroups.concat(response.items);

                    if (allGroups.length >= (response.count || 0)) {
                        break;
                    }

                    page++;
                } else {
                    break;
                }
            }

            return allGroups;
        };

        const [guests, groups] = await Promise.all([
            fetchAllGuests(),
            fetchAllGroups(),
        ]);

        // Create a map of group ID to group info for quick lookup
        const groupMap = new Map(
            groups.map((group) => [
                group.id,
                {
                    name: group.name,
                    priority: group.priority,
                    priorityDisplay: group.priorityDisplay,
                    relationship: group.relationship,
                    relationshipDisplay: group.relationshipDisplay,
                },
            ])
        );

        // Attach group information to each guest
        const allGuests = guests.map((guest) => {
            const group = guest.groupId ? groupMap.get(guest.groupId) : undefined;
            return {
                ...guest,
                guestGroupId: guest.groupId,
                guestGroupName: group?.name || "",
                guestGroupPriority: group?.priority || 0,
                guestGroupPriorityDisplay: group?.priorityDisplay || "",
                guestGroupRelationship: group?.relationshipDisplay || "",
            };
        });

        return {
            guests: allGuests,
        };
    } catch (error) {
        console.error("Error loading guests:", error);
        return {
            guests: [],
        };
    }
};
