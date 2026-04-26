import { createApiClient } from "$lib/server/api-client";
import type { Actions } from "./$types";

export const actions: Actions = {
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
