import { env } from "$env/dynamic/private";
import { redirect } from "@sveltejs/kit";
import type { Handle } from "@sveltejs/kit";

const API_URL = env.BACKEND_API_URL;

// Routes that require authentication
const protectedRoutes: string[] = ["/config", "/config/edit"];

export const handle: Handle = async ({ event, resolve }) => {
    const { url, cookies } = event;

    // Get session cookie for potential API calls
    const sessionCookie = cookies.get("sessionid");

    // Store session info in locals for use in load functions
    if (sessionCookie) {
        event.locals.sessionCookie = sessionCookie;
    }

    // Check if this route requires authentication
    const requiresAuth = protectedRoutes.some((route) => url.pathname.startsWith(route));

    if (requiresAuth) {
        if (!sessionCookie) {
            throw redirect(303, `/auth/login?redirect=${encodeURIComponent(url.pathname)}`);
        }

        const AUTH_URL = `${API_URL}/_allauth/browser/v1/auth/session`;

        try {
            const response = await fetch(AUTH_URL, {
                headers: {
                    Cookie: `sessionid=${sessionCookie}`,
                },
            });

            if (!response.ok) {
                throw redirect(303, `/auth/login?redirect=${encodeURIComponent(url.pathname)}`);
            }

            const result = await response.json();

            if (!result.meta?.is_authenticated) {
                throw redirect(303, `/auth/login?redirect=${encodeURIComponent(url.pathname)}`);
            }

            // Store user data in locals for access in pages
            event.locals.user = result.data?.user || null;
        } catch (error) {
            // Re-throw redirects
            if (error instanceof Response && error.status >= 300 && error.status < 400) {
                throw error;
            }
            // Network/other errors - redirect to login
            throw redirect(303, `/auth/login?redirect=${encodeURIComponent(url.pathname)}`);
        }
    }
    return resolve(event);
};
