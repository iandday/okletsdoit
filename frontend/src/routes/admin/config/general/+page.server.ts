import { fail } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { createApiClient } from '$lib/server/api-client';



export interface Feature {
    name: string;
    icon: string;
    enabledStatus: boolean;
    enabledLabelTrue: string;
    enabledLabelFalse: string;
    visibleStatus: boolean;
    visibleLabelTrue: string;
    visibleLabelFalse: string;
    category: "do" | "see";

}

const standardFeatureStatus = {
    enabledTrue: "Enabled",
    enabledFalse: "Disabled",
    visibleTrue: "Visible",
    visibleFalse: "Coming soon",
};



export const load: PageServerLoad = async ({ parent }) => {
    try {
        const layoutData = await parent();
        const configData = layoutData.configData;

        const features: Feature[] = [
            {
                name: "Our Story",
                icon: "lucide--square-pen",
                enabledStatus: configData?.enableOurStory,
                enabledLabelTrue: standardFeatureStatus.enabledTrue,
                enabledLabelFalse: standardFeatureStatus.enabledFalse,
                visibleStatus: configData?.showOurStory,
                visibleLabelTrue: standardFeatureStatus.visibleTrue,
                visibleLabelFalse: standardFeatureStatus.visibleFalse,
                category: "see",
            },
            {
                name: "Venue",
                icon: "lucide--map-pinned",
                enabledStatus: configData?.enableVenue,
                enabledLabelTrue: standardFeatureStatus.enabledTrue,
                enabledLabelFalse: standardFeatureStatus.enabledFalse,
                visibleStatus: configData?.showVenue,
                visibleLabelTrue: standardFeatureStatus.visibleTrue,
                visibleLabelFalse: standardFeatureStatus.visibleFalse,
                category: "see"
            },
            {
                name: "FAQ",
                icon: "lucide--help-circle",
                enabledStatus: configData?.enableFaq,
                enabledLabelTrue: standardFeatureStatus.enabledTrue,
                enabledLabelFalse: standardFeatureStatus.enabledFalse,
                visibleStatus: configData?.showFaq,
                visibleLabelTrue: standardFeatureStatus.visibleTrue,
                visibleLabelFalse: standardFeatureStatus.visibleFalse,
                category: "see"
            }
            , {
                name: "RSVP",
                icon: "lucide--check-square",
                enabledStatus: configData?.enableRsvp,
                enabledLabelTrue: standardFeatureStatus.enabledTrue,
                enabledLabelFalse: standardFeatureStatus.enabledFalse,
                visibleStatus: configData?.allowRsvp,
                visibleLabelTrue: "Active",
                visibleLabelFalse: "Not Active",
                category: "do",
            },
            {
                name: "Upload Photos",
                icon: "lucide--upload",
                enabledStatus: configData?.enableUploadPhotos,
                enabledLabelTrue: standardFeatureStatus.enabledTrue,
                enabledLabelFalse: standardFeatureStatus.enabledFalse,
                visibleStatus: configData?.allowPhotos,
                visibleLabelTrue: standardFeatureStatus.visibleTrue,
                visibleLabelFalse: standardFeatureStatus.visibleFalse,
                category: "do"
            }
        ];

        return {
            features: features
        };
    } catch (error) {
        console.error('Failed to load features:', error);
        return {
            features: []
        };
    }
}

export const actions: Actions = {
    updateStatus: async ({ locals, request }) => {
        const formData = await request.formData();
        const serviceName = formData.get('name');
        const fieldName = formData.get('type');
        const valueStr = formData.get('value');
        const value = valueStr === 'true';
        console.log(`Updating status for service: ${serviceName}, field: ${fieldName}, value: ${value}`);
        try {
            const api = createApiClient(locals.sessionCookie);

            if (serviceName == "Our Story") {
                if (fieldName == 'enabled') {
                    await api.core.coreApiUpdateWeddingSettings({
                        weddingSettingsUpdateSchema: { enableOurStory: value },
                    });
                }
                else if (fieldName == 'visible') {
                    console.log(`Updating visibility for Our Story to ${value}`);
                    await api.core.coreApiUpdateWeddingSettings({
                        weddingSettingsUpdateSchema: { showOurStory: value },
                    });
                }
            } else if (serviceName == "Venue") {

                if (fieldName == 'enabled') {
                    await api.core.coreApiUpdateWeddingSettings({
                        weddingSettingsUpdateSchema: { enableVenue: value },
                    });
                }
                else if (fieldName == 'visible') {
                    await api.core.coreApiUpdateWeddingSettings({
                        weddingSettingsUpdateSchema: { showVenue: value },
                    });
                }
            } else if (serviceName == "FAQ") {

                if (fieldName == 'enabled') {
                    await api.core.coreApiUpdateWeddingSettings({
                        weddingSettingsUpdateSchema: { enableFaq: value },
                    });
                }
                else if (fieldName == 'visible') {
                    await api.core.coreApiUpdateWeddingSettings({
                        weddingSettingsUpdateSchema: { showFaq: value },
                    });
                }
            } else if (serviceName == "RSVP") {
                if (fieldName == 'enabled') {
                    await api.core.coreApiUpdateWeddingSettings({
                        weddingSettingsUpdateSchema: { enableRsvp: value },
                    });
                }
                else if (fieldName == 'visible') {
                    await api.core.coreApiUpdateWeddingSettings({
                        weddingSettingsUpdateSchema: { allowRsvp: value },
                    });
                }
            } else if (serviceName == "Upload Photos") {
                if (fieldName == 'enabled') {
                    await api.core.coreApiUpdateWeddingSettings({
                        weddingSettingsUpdateSchema: { enableUploadPhotos: value },
                    });
                }
                else if (fieldName == 'visible') {
                    await api.core.coreApiUpdateWeddingSettings({
                        weddingSettingsUpdateSchema: { allowPhotos: value },
                    });
                }
            } else {
                throw new Error(`Unknown service name: ${serviceName}`);
            };





            return { success: true };
        } catch (error) {
            return fail(500, { message: 'Failed to write updates to the database.' });
        }
    }
};