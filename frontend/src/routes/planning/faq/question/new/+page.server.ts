import { createApiClient } from "$lib/server/api-client";
import { fail, redirect, type Redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {
    const api = createApiClient(locals.sessionCookie);
    const categoriesData = await api.core.coreApiGetCategoriesContent({ publishedOnly: false });

    return {
        categories: categoriesData,
    };
};

export const actions = {
    default: async ({ request, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();

        const question = formData.get("question");
        const answer = formData.get("answer");
        const categoryId = formData.get("categoryId");
        const icon = formData.get("icon");
        const order = formData.get("order");

        if (!question || !answer || !categoryId || !icon) {
            return fail(400, {
                error: "Question, answer, category, and icon are required",
                question,
                answer,
                categoryId,
                icon,
                order,
            });
        }

        try {
            await api.core.coreApiCreateQuestion({
                questionCreateSchema: {
                    question: question.toString(),
                    answer: answer.toString(),
                    categoryId: categoryId.toString(),
                    icon: icon.toString(),
                    ...(order && { order: parseInt(order.toString()) }),
                },
            });

            throw redirect(303, "/planning/faq");
        } catch (error) {
            if (error instanceof Response || (error as any).status === 303) {
                throw error;
            }
            return fail(500, {
                error: "Failed to create question",
                question,
                answer,
                categoryId,
                icon,
                order,
            });
        }
    },
} satisfies Actions;
