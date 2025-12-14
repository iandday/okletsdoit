import { redirect } from "@sveltejs/kit";
import type { Handle } from "@sveltejs/kit";

const API_URL = process.env.VITE_API_URL;

// Routes that require authentication
const protectedRoutes: string[] = [];

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
            // No session cookie, redirect to login
            throw redirect(303, `/auth/login?redirect=${encodeURIComponent(url.pathname)}`);
        }

        try {
            // Verify session with backend
            const response = await fetch(`${API_URL}/_allauth/browser/v1/auth/session`, {
                headers: {
                    Cookie: `sessionid=${sessionCookie}`,
                },
            });

            if (response.ok) {
                const result = await response.json();
                if (!result.meta?.is_authenticated) {
                    throw redirect(303, `/auth/login?redirect=${encodeURIComponent(url.pathname)}`);
                }
                // Store user data in locals for access in pages
                event.locals.user = result.data?.user || null;
            } else {
                throw redirect(303, `/auth/login?redirect=${encodeURIComponent(url.pathname)}`);
            }
        } catch (error) {
            if (error instanceof Response) throw error;
            console.error("Auth check failed:", error);
            throw redirect(303, `/auth/login?redirect=${encodeURIComponent(url.pathname)}`);
        }
    }

    return resolve(event);
};
