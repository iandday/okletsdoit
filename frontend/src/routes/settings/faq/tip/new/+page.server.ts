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

        const content = formData.get("content");
        const categoryId = formData.get("categoryId");
        const order = formData.get("order");

        if (!content || !categoryId) {
            return fail(400, {
                error: "Content and category are required",
                content,
                categoryId,
                order,
            });
        }

        try {
            await api.core.coreApiCreateTip({
                tipsCreateSchema: {
                    content: content.toString(),
                    categoryId: categoryId.toString(),
                    ...(order && { order: parseInt(order.toString()) }),
                },
            });

            throw redirect(303, "/settings/faq");
        } catch (error) {
            if (error instanceof Response || (error as any).status === 303) {
                throw error;
            }
            return fail(500, {
                error: "Failed to create tip",
                content,
                categoryId,
                order,
            });
        }
    },
} satisfies Actions;
