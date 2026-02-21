import { createApiClient } from "$lib/server/api-client";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {};

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
