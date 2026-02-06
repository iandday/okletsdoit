import type { ParamMatcher } from "@sveltejs/kit";

export const match: ParamMatcher = (param) => {
    // Match UUID format (common pattern for Django/backend IDs)
    // This prevents "new", "all", or other reserved words from matching [id] routes
    return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(param);
};
