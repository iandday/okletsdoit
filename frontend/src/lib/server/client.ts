/**
 * Type-safe API client for server-side requests
 * Generated from OpenAPI spec using openapi-typescript
 */
import type { paths } from "$lib/api/schema";
import createClient from "openapi-fetch";

const API_URL = process.env.PUBLIC_API_URL;
const SERVICE_TOKEN = process.env.SERVICE_TOKEN;

/**
 * Server-side API client with service token authentication
 * Automatically includes X-Service-Token header for backend-to-backend auth
 *
 * Note: Paths include /api/ prefix as defined in OpenAPI spec
 */
export const apiClient = createClient<paths>({
    baseUrl: API_URL,
    headers: {
        "X-Service-Token": SERVICE_TOKEN || "",
    },
});

/**
 * Example usage in a +page.server.ts file:
 *
 * import { apiClient } from '$lib/server/client';
 *
 * export const load = async () => {
 *     // Note: paths include /api/ prefix
 *     const { data, error } = await apiClient.GET("/api/guestlist/guest-groups");
 *
 *     if (error) {
 *         throw error(500, "Failed to load data");
 *     }
 *
 *     return { guestGroups: data };
 * };
 */
