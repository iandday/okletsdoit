import { createApiClient } from "$lib/server/api-client";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {
    const api = createApiClient(locals.sessionCookie);

    try {
        const result = await api.core.coreApiListRsvpQuestions({});
        return { rsvpQuestions: result.items };
    } catch (error) {
        console.error("Error loading RSVP questions:", error);
        return { rsvpQuestions: [] };
    }
};

export const actions: Actions = {
    createQuestion: async ({ locals, request }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const text = formData.get("text") as string;
        const questionType = formData.get("questionType") as string;
        const order = parseInt(formData.get("order") as string, 10) || 0;
        const published = formData.get("published") === "true";
        try {
            await api.core.coreApiCreateRsvpQuestion({
                rsvpQuestionCreateSchema: { text, questionType, order, published },
            });
            return { success: true };
        } catch (error) {
            console.error("Error creating RSVP question:", error);
            return { success: false, error: "Failed to create question" };
        }
    },
    updateQuestion: async ({ locals, request }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const questionId = formData.get("questionId") as string;
        const text = formData.get("text") as string;
        const order = parseInt(formData.get("order") as string, 10) || 0;
        const published = formData.get("published") === "true";
        try {
            await api.core.coreApiUpdateRsvpQuestion({
                questionId,
                rsvpQuestionUpdateSchema: { text, order, published },
            });
            return { success: true };
        } catch (error) {
            console.error("Error updating RSVP question:", error);
            return { success: false, error: "Failed to update question" };
        }
    },
    deleteQuestion: async ({ locals, request }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const questionId = formData.get("questionId") as string;
        try {
            await api.core.coreApiDeleteRsvpQuestion({ questionId });
            return { success: true };
        } catch (error) {
            console.error("Error deleting RSVP question:", error);
            return { success: false, error: "Failed to delete question" };
        }
    },
    createChoice: async ({ locals, request }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const questionId = formData.get("questionId") as string;
        const choiceText = formData.get("choiceText") as string;
        try {
            await api.core.coreApiCreateRsvpQuestionChoice({
                rsvpQuestionChoiceCreateSchema: { questionId, choiceText },
            });
            return { success: true };
        } catch (error) {
            console.error("Error creating RSVP question choice:", error);
            return { success: false, error: "Failed to create choice" };
        }
    },
    updateChoice: async ({ locals, request }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const choiceId = formData.get("choiceId") as string;
        const choiceText = formData.get("choiceText") as string;
        try {
            await api.core.coreApiUpdateRsvpQuestionChoice({
                choiceId,
                rsvpQuestionChoiceUpdateSchema: { choiceText },
            });
            return { success: true };
        } catch (error) {
            console.error("Error updating RSVP question choice:", error);
            return { success: false, error: "Failed to update choice" };
        }
    },
    deleteChoice: async ({ locals, request }) => {
        const api = createApiClient(locals.sessionCookie);
        const formData = await request.formData();
        const choiceId = formData.get("choiceId") as string;
        try {
            await api.core.coreApiDeleteRsvpQuestionChoice({ choiceId });
            return { success: true };
        } catch (error) {
            console.error("Error deleting RSVP question choice:", error);
            return { success: false, error: "Failed to delete choice" };
        }
    },
};
