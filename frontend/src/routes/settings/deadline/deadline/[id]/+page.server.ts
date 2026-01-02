import { api } from "$lib/server/api-client";
import { error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params }) => {
    try {
        const deadline = await api.deadlines.deadlineApiGetDeadline({
            deadlineId: params.id,
        });

        return {
            deadline,
        };
    } catch (err) {
        console.error("Error loading deadline:", err);
        throw error(404, "Deadline not found");
    }
};
