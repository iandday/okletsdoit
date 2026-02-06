import { api } from "$lib/server/api-client";
import { redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params }) => {
    const category = await api.expenses.expensesApiGetCategory({ categoryId: params.id });

    return {
        category,
    };
};

export const actions: Actions = {
    default: async ({ request, params }) => {
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
