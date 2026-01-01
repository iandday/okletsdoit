import { api } from "$lib/server/api-client";
import { error, fail, redirect, type Redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params }) => {
    try {
        const [question, categoriesData] = await Promise.all([
            api.core.coreApiGetQuestion({ questionId: params.id }),
            api.core.coreApiGetCategoriesContent({ publishedOnly: false }),
        ]);

        return {
            question,
            categories: categoriesData,
        };
    } catch (e) {
        throw error(404, "Question not found");
    }
};

export const actions = {
    updateQuestion: async ({ request, params }) => {
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
            await api.core.coreApiUpdateQuestion({
                questionId: params.id,
                questionUpdateSchema: {
                    question: question.toString(),
                    answer: answer.toString(),
                    categoryId: categoryId.toString(),
                    icon: icon.toString(),
                    ...(order && { order: parseInt(order.toString()) }),
                },
            });

            throw redirect(303, "/settings/faq");
        } catch (error) {
            if (error instanceof Response || (error as any).status === 303) {
                throw error;
            }
            return fail(500, {
                error: "Failed to update question",
                question,
                answer,
                categoryId,
                icon,
                order,
            });
        }
    },

    addUrl: async ({ request, params }) => {
        const formData = await request.formData();
        const url = formData.get("url");
        const text = formData.get("text");

        if (!url) {
            return fail(400, { urlError: "URL is required" });
        }

        try {
            await api.core.coreApiCreateQuestionUrl({
                questionURLCreateSchema: {
                    questionId: params.id,
                    url: url.toString(),
                    text: text ? text.toString() : null,
                },
            });

            return { success: true };
        } catch (error) {
            return fail(500, { urlError: "Failed to add URL" });
        }
    },

    updateUrl: async ({ request }) => {
        const formData = await request.formData();
        const urlId = formData.get("urlId");
        const url = formData.get("url");
        const text = formData.get("text");

        if (!urlId || !url) {
            return fail(400, { urlError: "URL ID and URL are required" });
        }

        try {
            await api.core.coreApiUpdateQuestionUrl({
                urlId: urlId.toString(),
                questionURLUpdateSchema: {
                    url: url.toString(),
                    text: text ? text.toString() : null,
                },
            });

            return { success: true };
        } catch (error) {
            return fail(500, { urlError: "Failed to update URL" });
        }
    },

    deleteUrl: async ({ request }) => {
        const formData = await request.formData();
        const urlId = formData.get("urlId");

        if (!urlId) {
            return fail(400, { urlError: "URL ID is required" });
        }

        try {
            await api.core.coreApiDeleteQuestionUrl({
                urlId: urlId.toString(),
            });

            return { success: true };
        } catch (error) {
            return fail(500, { urlError: "Failed to delete URL" });
        }
    },
} satisfies Actions;
