// frontend/src/routes/[code=rsvp]/accept/+page.server.ts
import { createApiClient } from "$lib/server/api-client";
import { error, fail, redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
    const api = createApiClient(locals.sessionCookie);
    const { code } = params;
    const configData = await api.core.coreApiGetWeddingSettings();
    if (configData.allowRsvp === false) {
        throw error(404, "It's not time to RSVP yet!");
    }

    const data = await api.guestlist.guestlistApiListGuestGroups({
        rsvpCode: code,
    });

    if (data.items && data.items.length == 1) {
        // get guest group, guests, and rsvp questions
        const guestGroup = data.items[0];
        const guests = await api.guestlist.guestlistApiListGuests({
            groupId: guestGroup.id,
        });
        const rsvpQuestions = await api.guestlist.guestlistApiGetRsvpAcceptanceQuestions({ rsvpCode: code });
        return {
            guestData: guestGroup,
            guests: guests.items,
            rsvpQuestions: rsvpQuestions,
            configData: configData,
            showAccommodation: guests.items.some((guest) => guest.accommodation),
            showVip: guests.items.some((guest) => guest.vip),
        };
    } else {
        throw error(404, "Unable to locate RSVP information");
    }
};

export const actions: Actions = {
    default: async ({ request, params, locals }) => {
        const api = createApiClient(locals.sessionCookie);
        const { code } = params;
        const configData = await api.core.coreApiGetWeddingSettings();

        const formData = await request.formData();
        const submissionId = formData.get("submission_id")?.toString();

        const guestUpdates = [];
        const guestIds = formData.getAll("guest_id");

        for (const guestId of guestIds) {
            const id = guestId.toString();
            const isAttending = formData.get(`guest_${id}_is_attending`) === "true";
            const acceptAccommodation = formData.get(`guest_${id}_accept_accommodation`) === "true";
            const acceptVip = formData.get(`guest_${id}_accept_vip`) === "true";

            guestUpdates.push({
                id,
                isAttending,
                acceptAccommodation,
                acceptVip,
                responded: true,
            });
        }

        try {
            // Update each guest
            for (const guestUpdate of guestUpdates) {
                await api.guestlist.guestlistApiUpdateGuest({
                    guestId: guestUpdate.id,
                    guestUpdateSchema: {
                        isAttending: guestUpdate.isAttending,
                        acceptAccommodation: guestUpdate.acceptAccommodation,
                        acceptVip: guestUpdate.acceptVip,
                        responded: guestUpdate.responded,
                    },
                });
            }

            // Update RSVP submission with email preferences if applicable
            if (submissionId && configData.rsvpEnableEmailUpdates) {
                const emailUpdates = formData.get("email_updates") === "true";
                const emailAddress = formData.get("email_address")?.toString() || "";
                await api.guestlist.guestlistApiUpdateRsvpSubmission({
                    submissionId,
                    rsvpSubmissionUpdateSchema: {
                        emailUpdates,
                        emailAddress,
                    },
                });
            }

            // Process question responses if any
            const questionResponseIds = formData.getAll("question_response_id");
            for (const responseId of questionResponseIds) {
                const id = responseId.toString();
                const questionType = formData.get(`question_${id}_type`)?.toString();
                const responseText = formData.get(`question_${id}_response_text`)?.toString();

                // For now, only text responses are handled
                // TODO: Extend to handle other question types as needed
                if (questionType === "text") {
                    await api.guestlist.guestlistApiUpdateRsvpResponse({
                        responseId: id,
                        rsvpQuestionResponseUpdateSchema: {
                            responseText: responseText || null,
                        },
                    });
                }
            }
            throw redirect(303, `/${code}/complete?accepted=true`);
        } catch (err) {
            // Re-throw redirects and other Response objects immediately
            if (err instanceof Response || (err && typeof err === "object" && "status" in err && "location" in err)) {
                throw err;
            }
            console.error("Error submitting RSVP:", err);
            return fail(500, {
                error: "Failed to submit RSVP. Please try again.",
                guests: guestUpdates,
            });
        }
    },
};
