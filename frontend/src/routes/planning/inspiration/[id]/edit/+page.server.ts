import { createApiClient } from "$lib/server/api-client";
import { fail, redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
    const api = createApiClient(locals.sessionCookie);
    const inspiration = await api.core.coreApiGetInspiration({ inspirationId: params.id });

    return {
        inspiration,
    };
};

export const actions: Actions = {
    update: async ({ request, params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const name = formData.get("name") as string;
        const description = formData.get("description") as string;

        try {
            await api.core.coreApiUpdateInspiration({
                inspirationId: params.id,
                inspirationUpdateSchema: {
                    name: name || undefined,
                    description: description || undefined,
                },
            });

            return { success: true };
        } catch (err) {
            console.error("Failed to update inspiration:", err);
            return fail(500, { error: "Failed to update inspiration" });
        }
    },

    uploadImage: async ({ params, request, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const image = formData.get("image") as File;

        if (!image || image.size === 0) {
            return fail(400, { error: "Please select an image to upload" });
        }

        console.log(`[Upload] Image: ${image.name}, Size: ${image.size} bytes, Type: ${image.type}`);

        try {
            await api.core.coreApiUploadInspirationImage({
                inspirationId: params.id,
                image: image,
            });

            console.log(`[Upload] Success!`);
            return { success: true, imageUploaded: true };
        } catch (err: any) {
            console.error("[Upload] Error details:", {
                message: err?.message,
                status: err?.status,
                statusText: err?.statusText,
                body: err?.body,
            });
            return fail(500, {
                error: "Failed to upload image",
                details: err?.message || String(err),
            });
        }
    },

    deleteImage: async ({ params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        try {
            await api.core.coreApiDeleteInspirationImage({
                inspirationId: params.id,
            });

            return { success: true, imageDeleted: true };
        } catch (err) {
            console.error("Failed to delete image:", err);
            return fail(500, { error: "Failed to delete image" });
        }
    },

    saveAndReturn: async ({ request, params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const name = formData.get("name") as string;
        const description = formData.get("description") as string;

        try {
            await api.core.coreApiUpdateInspiration({
                inspirationId: params.id,
                inspirationUpdateSchema: {
                    name: name || undefined,
                    description: description || undefined,
                },
            });
        } catch (err) {
            console.error("Failed to update inspiration:", err);
            return fail(500, { error: "Failed to update inspiration" });
        }

        throw redirect(303, `/planning/inspiration/${params.id}`);
    },
};
