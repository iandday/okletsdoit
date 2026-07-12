// frontend/src/routes/story/+page.server.ts
import { getconfigData } from "$lib/server/config-data";
import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {
    const configData = await getconfigData();

    if (!configData?.enableOurStory) {
        throw redirect(302, "/");
    }
    return {};
};
