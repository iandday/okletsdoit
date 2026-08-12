import { createApiClient } from "$lib/server/api-client";
import { fail } from "@sveltejs/kit";
import { redirect } from "@sveltejs/kit";
import type { PageServerLoad, Actions } from "./$types";

export const load: PageServerLoad = async ({ parent, locals }) => {
    const layoutData = await parent();
    const configData = layoutData.configData;
    const api = createApiClient(locals.sessionCookie);


    const photos = await api.photos.photosApiListAllUploadedPhotos();
    return { photos: photos };
};