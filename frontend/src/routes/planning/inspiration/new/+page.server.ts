import { createApiClient } from "$lib/server/api-client";
import { fail, redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async () => {
    return {};
};

export const actions: Actions = {
    default: async ({ request, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const name = formData.get("name") as string;
        const description = formData.get("description") as string;
        const image = formData.get("image") as File;

        let newInspiration;
        try {
            newInspiration = await api.core.coreApiCreateInspiration({
                inspirationCreateSchema: {
                    name,
                    description: description || "",
                },
            });
        } catch (error) {
            console.error("Error creating inspiration:", error);
            return fail(500, { error: "Failed to create inspiration" });
        }

        if (image && image.size > 0) {
            try {
                await api.core.coreApiUploadInspirationImage({
                    inspirationId: newInspiration.id,
                    image: image,
                });
            } catch (error) {
                console.error("Error uploading image:", error);
            }
        }

        throw redirect(303, `/settings/inspiration`);
    },
};
