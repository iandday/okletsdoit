// frontend/src/routes/faq/+page.server.ts
import { api } from "$lib/server/api-client";
import { fail, redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async () => {
    const categoriesData = await api.core.coreApiGetCategoriesContent({ publishedOnly: true });

    return {
        categories: categoriesData,
    };
};
