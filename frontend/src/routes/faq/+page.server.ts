// frontend/src/routes/faq/+page.server.ts
import { createApiClient } from "$lib/server/api-client";
import { getconfigData } from "$lib/server/config-data";
import type { PageServerLoad } from "./$types";
import { redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ locals }) => {
    const api = createApiClient(locals.sessionCookie);
    const configData = await getconfigData();
    const categoriesData = await api.core.coreApiGetCategoriesContent({ publishedOnly: true });
    console.log(configData?.showFaq)
    if (!configData?.enableFaq) {
        throw redirect(302, "/");
    }
    return {
        categories: categoriesData,
    };
};
