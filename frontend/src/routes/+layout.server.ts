import { getconfigData } from "$lib/server/config-data";
import { redirect } from "@sveltejs/kit";
import type { LayoutServerLoad } from "./$types";

export const load: LayoutServerLoad = async () => {
    const configData = await getconfigData();

    // redirect to home if no config data
    if (!configData) {
        throw redirect(302, "/");
    }
    return {
        configData,
    };
};
