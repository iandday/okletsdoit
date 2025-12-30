import { getconfigData } from "$lib/server/config-data";
import type { LayoutServerLoad } from "./$types";

export const load: LayoutServerLoad = async () => {
    const configData = await getconfigData();

    return {
        configData,
    };
};
