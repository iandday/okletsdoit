import { createApiClient } from "$lib/server/api-client";
import { fail } from "@sveltejs/kit";
import type { PageServerLoad, Actions } from "./$types";

export const load: PageServerLoad = async ({ parent, locals }) => {
    const layoutData = await parent();
    const api = createApiClient(locals.sessionCookie);

    const photos = await api.photos.photosApiListAllUploadedPhotos();
    return { photos: photos };
};

export const actions: Actions = {
    deletePhoto: async ({ request, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const photoId = formData.get("photoId");

        if (typeof photoId !== "string" || photoId.length === 0) {
            return fail(400, { error: "Invalid photo id." });
        }

        try {
            const photos = await api.photos.photosApiListAllUploadedPhotos();
            const photo = photos.find((item) => item.id === photoId);

            if (!photo) {
                return fail(404, { error: "Photo not found." });
            }

            await api.photos.photosApiUpdateUploadedPhoto({
                photoId,
                uploadedPhotoSchema: {
                    ...photo,
                    isDeleted: true,
                },
            });

            return { success: true };
        } catch (error) {
            console.error("Failed to delete photo:", error);
            return fail(500, { error: "Failed to delete photo." });
        }
    },

    restorePhoto: async ({ request, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const photoId = formData.get("photoId");

        if (typeof photoId !== "string" || photoId.length === 0) {
            return fail(400, { error: "Invalid photo id." });
        }

        try {
            const photos = await api.photos.photosApiListAllUploadedPhotos();
            const photo = photos.find((item) => item.id === photoId);

            if (!photo) {
                return fail(404, { error: "Photo not found." });
            }

            await api.photos.photosApiUpdateUploadedPhoto({
                photoId,
                uploadedPhotoSchema: {
                    ...photo,
                    isDeleted: false,
                },
            });

            return { success: true };
        } catch (error) {
            console.error("Failed to restore photo:", error);
            return fail(500, { error: "Failed to restore photo." });
        }
    },

    approvePhoto: async ({ request, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const photoId = formData.get("photoId");

        if (typeof photoId !== "string" || photoId.length === 0) {
            return fail(400, { error: "Invalid photo id." });
        }

        try {
            const photos = await api.photos.photosApiListAllUploadedPhotos();
            const photo = photos.find((item) => item.id === photoId);

            if (!photo) {
                return fail(404, { error: "Photo not found." });
            }

            await api.photos.photosApiUpdateUploadedPhoto({
                photoId,
                uploadedPhotoSchema: {
                    ...photo,
                    isApproved: true,
                },
            });

            return { success: true };
        } catch (error) {
            console.error("Failed to approve photo:", error);
            return fail(500, { error: "Failed to approve photo." });
        }
    },

    unapprovePhoto: async ({ request, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const photoId = formData.get("photoId");

        if (typeof photoId !== "string" || photoId.length === 0) {
            return fail(400, { error: "Invalid photo id." });
        }

        try {
            const photos = await api.photos.photosApiListAllUploadedPhotos();
            const photo = photos.find((item) => item.id === photoId);

            if (!photo) {
                return fail(404, { error: "Photo not found." });
            }

            await api.photos.photosApiUpdateUploadedPhoto({
                photoId,
                uploadedPhotoSchema: {
                    ...photo,
                    isApproved: false,
                },
            });

            return { success: true };
        } catch (error) {
            console.error("Failed to unapprove photo:", error);
            return fail(500, { error: "Failed to unapprove photo." });
        }
    },
};
