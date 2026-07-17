// frontend/src/routes/faq/+page.server.ts
import { createApiClient } from "$lib/server/api-client";
import { getconfigData } from "$lib/server/config-data";
import { redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {
    const api = createApiClient(locals.sessionCookie);
    const configData = await getconfigData();
    const categoriesData = await api.core.coreApiGetCategoriesContent({ publishedOnly: true });
    console.log(configData?.showFaq);
    if (!configData?.enableFaq) {
        throw redirect(302, "/");
    }
    return {
        categories: categoriesData,
    };
};
