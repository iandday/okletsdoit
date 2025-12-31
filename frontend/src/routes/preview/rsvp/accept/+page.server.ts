import { api } from "$lib/server/api-client";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async () => {

    // Fetch real RSVP questions
    const rsvpQuestions = await api.guestlist.guestlistApiGetRsvpAcceptenceQuestionsPreview();

    // Mock guest data for preview
    const mockGuestData = {
        id: "preview-guest-group",
        addressName: "The Smith Family",
        rsvpCode: "PREVIEW",
        email: "smith@example.com",
    };

    const mockGuests = [
        {
            id: "preview-guest-1",
            firstName: "John",
            lastName: "Smith",
            isAttending: true,
            acceptAccommodation: false,
            acceptVip: false,
            accommodation: true,
            vip: true,
            responded: false,
        },
        {
            id: "preview-guest-2",
            firstName: "Jane",
            lastName: "Smith",
            isAttending: true,
            acceptAccommodation: true,
            acceptVip: true,
            accommodation: true,
            vip: true,
            responded: false,
        },
    ];

    // Transform real questions into response format for preview
    const mockRsvpQuestionResponses =
        rsvpQuestions.map((question) => ({
            id: question.id,
            questionText: question.questionText,
            questionType: question.questionType,
            responseText: "",
            submissionId: "preview-submission-1",
        })) || [];

    return {
        guestData: mockGuestData,
        guests: mockGuests,
        rsvpQuestions: mockRsvpQuestionResponses,
        showAccommodation: true,
        showVip: true,
    };
};
