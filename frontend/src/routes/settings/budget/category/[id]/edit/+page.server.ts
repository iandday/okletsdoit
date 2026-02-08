import { createApiClient } from "$lib/server/api-client";
import { redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
    const api = createApiClient(locals.sessionCookie);
    const category = await api.expenses.expensesApiGetCategory({ categoryId: params.id });

    return {
        category,
    };
};

export const actions: Actions = {
    default: async ({ request, params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const name = formData.get("name") as string;
        const description = formData.get("description") as string;

        await api.expenses.expensesApiUpdateCategory({
            categoryId: params.id,
            categoryUpdateSchema: {
                name,
                description: description || undefined,
            },
        });

        throw redirect(303, `/settings/budget/category/${params.id}`);
    },
};
