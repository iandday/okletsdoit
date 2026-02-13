import { createApiClient } from "$lib/server/api-client";
import { fail, redirect } from "@sveltejs/kit";
import type { Actions } from "./$types";

export const actions = {
    default: async ({ request, locals }) => {
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

        let guestGroup;
        try {
            guestGroup = await api.guestlist.guestlistApiCreateGuestGroup({
                guestGroupCreateSchema: {
                    name: name.trim(),
                    addressName: addressName && typeof addressName === "string" ? addressName : "",
                    email: email && typeof email === "string" ? email : "",
                    phone: phone && typeof phone === "string" ? phone : "",
                    address: address && typeof address === "string" ? address : "",
                    addressTwo: addressTwo && typeof addressTwo === "string" ? addressTwo : "",
                    city: city && typeof city === "string" ? city : "",
                    state: state && typeof state === "string" ? state : "",
                    zipCode: zipCode && typeof zipCode === "string" ? zipCode : "",
                    relationship: relationship && typeof relationship === "string" ? relationship : "Rel",
                    priority: priority && typeof priority === "string" ? parseInt(priority) : 2,
                    notes: notes && typeof notes === "string" ? notes : "",
                },
            });
        } catch (err) {
            console.error("Failed to create guest group:", err);
            return fail(500, { error: "Failed to create guest group" });
        }

        throw redirect(303, `/planning/guest_list/${guestGroup.id}`);
    },
} satisfies Actions;
