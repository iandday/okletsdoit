import { createApiClient } from "$lib/server/api-client";
import { error, fail, redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
    const api = createApiClient(locals.sessionCookie);
    try {
        const guestGroup = await api.guestlist.guestlistApiGetGuestGroup({
            groupId: params.id,
        });

        return {
            guestGroup,
        };
    } catch (err) {
        console.error("Error loading guest group:", err);
        throw error(404, "Guest group not found");
    }
};

export const actions: Actions = {
    default: async ({ request, params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();

        const name = formData.get("name");
        const addressName = formData.get("address_name");
        const email = formData.get("email");
        const phone = formData.get("phone");
        const address = formData.get("address");
        const addressTwo = formData.get("address_two");
        const city = formData.get("city");
        const state = formData.get("state");
        const zipCode = formData.get("zip_code");
        const relationship = formData.get("relationship");
        const priority = formData.get("priority");
        const notes = formData.get("notes");

        if (!name || typeof name !== "string" || name.trim() === "") {
            return fail(400, { error: "Group name is required" });
        }

        try {
            await api.guestlist.guestlistApiUpdateGuestGroup({
                groupId: params.id,
                guestGroupUpdateSchema: {
                    name: name.trim(),
                    addressName: addressName && typeof addressName === "string" ? addressName : "",
                    email: email && typeof email === "string" ? email : "",
                    phone: phone && typeof phone === "string" ? phone : "",
                    address: address && typeof address === "string" ? address : "",
                    addressTwo: addressTwo && typeof addressTwo === "string" ? addressTwo : "",
                    city: city && typeof city === "string" ? city : "",
                    state: state && typeof state === "string" ? state : "",
                    zipCode: zipCode && typeof zipCode === "string" ? zipCode : "",
                    relationship: relationship && typeof relationship === "string" ? relationship : null,
                    priority: priority && typeof priority === "string" ? parseInt(priority) : null,
                    notes: notes && typeof notes === "string" ? notes : "",
                },
            });
        } catch (err) {
            console.error("Failed to update guest group:", err);
            return fail(500, { error: "Failed to update guest group" });
        }

        throw redirect(303, `/planning/guest_list/${params.id}`);
    },
};
