import { createApiClient } from "$lib/server/api-client";
import { fail } from "@sveltejs/kit";
import { redirect } from "@sveltejs/kit";
import type { PageServerLoad, Actions } from "./$types";

export const load: PageServerLoad = async ({ parent, locals }) => {
    const layoutData = await parent();
    const configData = layoutData.configData;
    const api = createApiClient(locals.sessionCookie);

    if (!configData?.enableUploadPhotos) {
        throw redirect(302, "/");
    }
    const photos = await api.photos.photosApiListUploadedPhotos();
    return { photos: photos };
};

export const actions: Actions = {
    uploadImage: async ({ request, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const image = formData.get("image");

        if (!(image instanceof File) || image.size === 0) {
            return fail(400, { error: "Please choose a photo to upload." });
        }

        try {
            const urlResponse = await api.photos.photosApiCreateUploadedPhoto();

            const uploadResponse = await fetch(urlResponse.uploadUrl, {
                method: "PUT",
                body: image,
                headers: image.type ? { "Content-Type": image.type } : undefined,
            });

            if (!uploadResponse.ok) {
                console.error(
                    "Failed to upload image to presigned URL:",
                    uploadResponse.status,
                    uploadResponse.statusText,
                );
                return fail(502, { error: "Failed to upload photo." });
            }
            await api.photos.photosApiCompleteUploadedPhoto({ photoId: urlResponse.id });
        } catch (error) {
            console.error("Error uploading photo:", error);
            return fail(500, { error: "Failed to upload photo." });
        }

        return {
            success: true,
        };
    },
};
