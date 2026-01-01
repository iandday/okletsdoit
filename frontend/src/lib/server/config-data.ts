import { api } from "./api-client";

export const getconfigData = async () => {
    const config_data = await api.core.coreApiGetWeddingSettings();

    if (config_data) {
        return config_data;
    }

    return null;
};
