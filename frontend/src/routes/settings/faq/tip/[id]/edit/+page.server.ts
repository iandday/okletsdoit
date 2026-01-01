import { api } from "$lib/server/api-client";
import { error, fail, redirect, type Redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params }) => {
    try {
        const [tip, categoriesData] = await Promise.all([
            api.core.coreApiGetTip({ tipId: params.id }),
            api.core.coreApiGetCategoriesContent({ publishedOnly: false }),
        ]);

        return {
            tip,
            categories: categoriesData,
        };
    } catch (e) {
        throw error(404, "Tip not found");
    }
};

export const actions = {
    default: async ({ request, params }) => {
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
            await api.core.coreApiUpdateTip({
                tipId: params.id,
                tipsUpdateSchema: {
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
                error: "Failed to update tip",
                content,
                categoryId,
                order,
            });
        }
    },
} satisfies Actions;
