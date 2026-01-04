/**
 * Server-side API client using the OpenAPI generated client
 * Configured with service token authentication for backend-to-backend communication
 */
import { Configuration, GuestlistApi, CoreApi, DeadlinesApi } from "../../../api-client";
import type { Middleware } from "../../../api-client/runtime";

const API_BASE_PATH = process.env.BACKEND_API_URL;
const SERVICE_TOKEN = process.env.SERVICE_TOKEN || "";
const DEBUG = process.env.NODE_ENV === "development";

/**
 * Middleware to add trailing slash to URLs
 * Django's APPEND_SLASH requires trailing slashes to avoid 301 redirects
 */
const trailingSlashMiddleware: Middleware = {
    pre: async (context) => {
        const url = new URL(context.url);
        if (!url.pathname.endsWith("/") && !url.pathname.match(/\.[a-z]+$/i)) {
            url.pathname += "/";
            context.url = url.toString();
        }
        return context;
    },
};

/**
 * Debug logging middleware
 */
const debugMiddleware: Middleware = {
    pre: async (context) => {
        if (DEBUG) {
            console.log("[API Request]", {
                method: context.init.method,
                url: context.url,
                headers: context.init.headers,
            });
        }
        return context;
    },
    post: async (context) => {
        if (DEBUG) {
            console.log("[API Response]", {
                status: context.response.status,
                statusText: context.response.statusText,
                url: context.url,
            });
        }
        return context.response;
    },
    onError: async (context) => {
        console.error("[API Error]", {
            url: context.url,
            error: context.error,
            response: context.response
                ? {
                      status: context.response.status,
                      statusText: context.response.statusText,
                  }
                : undefined,
        });
        return context.response;
    },
};

function createConfig() {
    return new Configuration({
        basePath: API_BASE_PATH,
        headers: {
            "X-Service-Token": SERVICE_TOKEN,
        },
        middleware: [debugMiddleware],
    });
}

export function createApiClient() {
    const config = createConfig();

    return {
        guestlist: new GuestlistApi(config),
        core: new CoreApi(config),
        deadlines: new DeadlinesApi(config),
    };
}

export const api = createApiClient();
