import { createApiClient } from "$lib/server/api-client";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {
    const api = createApiClient(locals.sessionCookie);
    try {
        // Fetch all pages of guest groups
        let allGuestGroups: any[] = [];
        let page = 1;
        let totalCount = 0;

        while (true) {
            const response = await api.guestlist.guestlistApiListGuestGroups({
                page,
                pageSize: 100,
            });

            if (response.items && response.items.length > 0) {
                allGuestGroups = allGuestGroups.concat(response.items);
                totalCount = response.count || 0;

                if (allGuestGroups.length >= totalCount) {
                    break;
                }

                page++;
            } else {
                break;
            }
        }

        return {
            guestGroups: allGuestGroups,
            count: totalCount,
        };
    } catch (error) {
        console.error("Error loading guest groups:", error);
        return {
            guestGroups: [],
            count: 0,
        };
    }
};

export const actions: Actions = {
    generateMissingQrCodes: async ({ locals }) => {
        const api = createApiClient(locals.sessionCookie);
        try {
            const result = await api.guestlist.guestlistApiGenerateMissingQrCodes();
            return {
                success: true,
                message: "QR code generation started",
                taskId: result.taskId,
            };
        } catch (error) {
            console.error("Error generating missing QR codes:", error);
            return {
                success: false,
                error: "Failed to start QR code generation",
            };
        }
    },
    regenerateAllQrCodes: async ({ locals }) => {
        const api = createApiClient(locals.sessionCookie);
        try {
            const result = await api.guestlist.guestlistApiRegenerateAllQrCodes();
            return {
                success: true,
                message: "QR code regeneration started",
                taskId: result.taskId,
            };
        } catch (error) {
            console.error("Error regenerating all QR codes:", error);
            return {
                success: false,
                error: "Failed to start QR code regeneration",
            };
        }
    },
};
