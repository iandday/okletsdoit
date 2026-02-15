import { createApiClient } from "$lib/server/api-client";
import type { Actions } from "./$types";

export const actions: Actions = {
    sendUpdateEmail: async ({ locals }) => {
        const api = createApiClient(locals.sessionCookie);
        try {
            const result = await api.core.coreApiTriggerSendUpdateEmail();
            return {
                success: true,
                message: result.message,
                taskId: result.taskId,
            };
        } catch (error) {
            console.error("Error sending update email:", error);
            return {
                success: false,
                error: "Failed to send update email",
            };
        }
    },
};
