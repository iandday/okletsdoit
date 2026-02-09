import { createApiClient } from "$lib/server/api-client";
import { fail } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {
    const api = createApiClient(locals.sessionCookie);
    const [questions, tips, categories] = await Promise.all([
        api.core.coreApiListQuestions({}),
        api.core.coreApiListTips({}),
        api.core.coreApiGetCategoriesContent({ publishedOnly: false }),
    ]);

    return {
        questions: questions.items || [],
        tips: tips.items || [],
        categories: categories || [],
    };
};

export const actions = {
    deleteQuestion: async ({ request, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const id = formData.get("id");

        if (!id || typeof id !== "string") {
            return fail(400, { error: "Invalid question ID" });
        }

        try {
            await api.core.coreApiDeleteQuestion({ questionId: id });
            return { success: true };
        } catch (error) {
            console.error("Error deleting question:", error);
            return fail(500, { error: "Failed to delete question" });
        }
    },

    deleteTip: async ({ request, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const id = formData.get("id");

        if (!id || typeof id !== "string") {
            return fail(400, { error: "Invalid tip ID" });
        }

        try {
            await api.core.coreApiDeleteTip({ tipId: id });
            return { success: true };
        } catch (error) {
            console.error("Error deleting tip:", error);
            return fail(500, { error: "Failed to delete tip" });
        }
    },
} satisfies Actions;
