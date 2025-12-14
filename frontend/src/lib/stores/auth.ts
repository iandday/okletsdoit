import { browser } from "$app/environment";
import { env } from "$env/dynamic/public";
import { writable } from "svelte/store";

const API_URL = env.PUBLIC_API_URL || "http://localhost:8000";

// Use browser client for web applications (uses cookies and CSRF)
const CLIENT = "browser";

// Get CSRF token from cookie
function getCsrfToken(): string | null {
    if (!browser) return null;
    const name = "csrftoken";
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()?.split(";").shift() || null;
    return null;
}

interface User {
    id?: number;
    display?: string;
    username?: string;
    email?: string;
    has_usable_password?: boolean;
}

interface Provider {
    id: string;
    name: string;
    client_id?: string;
    flows?: string[];
}

interface ProviderAccount {
    uid: string;
    display: string;
    provider: string;
}

interface AuthResponse {
    status: number;
    data?: {
        user?: User;
        flows?: any[];
        providers?: Provider[];
    };
    meta?: {
        is_authenticated?: boolean;
        session_token?: string;
        access_token?: string;
    };
    errors?: Array<{
        code: string;
        param?: string;
        message: string;
    }>;
}

interface AuthState {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
}

const initialState: AuthState = {
    user: null,
    isAuthenticated: false,
    isLoading: true,
};

function createAuthStore() {
    const { subscribe, set, update } = writable<AuthState>(initialState);

    return {
        subscribe,

        async init() {
            if (!browser) return;

            try {
                const response = await fetch(`${API_URL}/_allauth/${CLIENT}/v1/auth/session`, {
                    credentials: "include",
                });

                const result: AuthResponse = await response.json();

                if (response.ok && result.meta?.is_authenticated && result.data?.user) {
                    set({ user: result.data.user, isAuthenticated: true, isLoading: false });
                } else {
                    set({ user: null, isAuthenticated: false, isLoading: false });
                }
            } catch (error) {
                console.error("Auth init error:", error);
                set({ user: null, isAuthenticated: false, isLoading: false });
            }
        },

        async login(email: string, password: string) {
            try {
                console.log("🔐 Attempting login to:", `${API_URL}/_allauth/${CLIENT}/v1/auth/login`);
                console.log("📤 Payload:", JSON.stringify({ email: email, password: password }));

                const csrfToken = getCsrfToken();
                const headers: Record<string, string> = {
                    "Content-Type": "application/json",
                };
                if (csrfToken) {
                    headers["X-CSRFToken"] = csrfToken;
                }

                const response = await fetch(`${API_URL}/_allauth/${CLIENT}/v1/auth/login`, {
                    method: "POST",
                    headers,
                    credentials: "include",
                    body: JSON.stringify({ email: email, password: password }),
                });

                const result: AuthResponse = await response.json();
                console.log("📡 Response:", result);

                // Handle 409 Conflict - user already authenticated
                if (response.status === 409) {
                    console.log("ℹ️ User already authenticated");
                    // Fetch current session to get user data
                    const sessionResponse = await fetch(`${API_URL}/_allauth/${CLIENT}/v1/auth/session`, {
                        credentials: "include",
                    });
                    const sessionResult: AuthResponse = await sessionResponse.json();
                    if (sessionResult.data?.user) {
                        console.log("✅ Retrieved user from session after conflict");
                        console.log("📦 User data:", sessionResult.data.user);
                        set({ user: sessionResult.data.user, isAuthenticated: true, isLoading: false });
                    }
                    return { success: true };
                }

                if (!response.ok) {
                    console.error("❌ Login failed:", result);
                    const errorMessage = result.errors?.[0]?.message || "Login failed";
                    throw new Error(errorMessage);
                }

                // Check if fully authenticated
                if (result.meta?.is_authenticated && result.data?.user) {
                    console.log("✅ Login successful");
                    set({ user: result.data.user, isAuthenticated: true, isLoading: false });
                    return { success: true };
                }

                // Handle flows (e.g., 2FA required, email verification needed)
                if (result.data?.flows && result.data.flows.length > 0) {
                    return {
                        success: false,
                        error: "Additional authentication steps required",
                        flows: result.data.flows,
                    };
                }

                throw new Error("Unexpected response from server");
            } catch (error) {
                console.error("💥 Login error:", error);

                if (error instanceof TypeError && error.message.includes("fetch")) {
                    return {
                        success: false,
                        error: `Cannot connect to ${API_URL}. Is your Django server running?`,
                    };
                }

                return {
                    success: false,
                    error: error instanceof Error ? error.message : "Login failed",
                };
            }
        },

        async logout() {
            try {
                const csrfToken = getCsrfToken();
                const headers: Record<string, string> = {};
                if (csrfToken) {
                    headers["X-CSRFToken"] = csrfToken;
                }

                await fetch(`${API_URL}/_allauth/${CLIENT}/v1/auth/session`, {
                    method: "DELETE",
                    headers,
                    credentials: "include",
                });
            } catch (error) {
                console.error("Logout error:", error);
            } finally {
                set({ user: null, isAuthenticated: false, isLoading: false });
            }
        },

        async register(email: string, password: string) {
            try {
                const csrfToken = getCsrfToken();
                const headers: Record<string, string> = {
                    "Content-Type": "application/json",
                };
                if (csrfToken) {
                    headers["X-CSRFToken"] = csrfToken;
                }

                const response = await fetch(`${API_URL}/_allauth/${CLIENT}/v1/auth/signup`, {
                    method: "POST",
                    headers,
                    credentials: "include",
                    body: JSON.stringify({ email, password }),
                });

                const result: AuthResponse = await response.json();

                if (!response.ok) {
                    const errorMessage = result.errors?.[0]?.message || "Registration failed";
                    throw new Error(errorMessage);
                }

                // Check if fully authenticated after signup
                if (result.meta?.is_authenticated && result.data?.user) {
                    set({ user: result.data.user, isAuthenticated: true, isLoading: false });
                    return { success: true };
                }

                // Handle flows (e.g., email verification required)
                if (result.data?.flows && result.data.flows.length > 0) {
                    return {
                        success: false,
                        error: "Email verification or additional steps required",
                        flows: result.data.flows,
                    };
                }

                return { success: true };
            } catch (error) {
                console.error("Registration error:", error);
                return {
                    success: false,
                    error: error instanceof Error ? error.message : "Registration failed",
                };
            }
        },

        // Get available authentication providers
        async getProviders() {
            try {
                const response = await fetch(`${API_URL}/_allauth/${CLIENT}/v1/config`, {
                    credentials: "include",
                });

                const result = await response.json();
                return result.data?.socialaccount?.providers || [];
            } catch (error) {
                console.error("Failed to fetch providers:", error);
                return [];
            }
        },

        // Initiate provider redirect flow (e.g., Google, GitHub)
        async loginWithProvider(providerId: string, callbackUrl?: string) {
            if (!browser) return { success: false, error: "Not in browser context" };

            try {
                const csrfToken = getCsrfToken();
                const headers: Record<string, string> = {
                    "Content-Type": "application/json",
                };
                if (csrfToken) {
                    headers["X-CSRFToken"] = csrfToken;
                }

                const body: any = { provider: providerId, process: "login" };
                if (callbackUrl) {
                    body.callback_url = callbackUrl;
                }

                // POST to the redirect endpoint - it will return a 302 redirect
                // We need to handle this by creating a form and submitting it
                // because fetch() doesn't follow 302 redirects that change origins
                const form = document.createElement("form");
                form.method = "POST";
                form.action = `${API_URL}/_allauth/${CLIENT}/v1/auth/provider/redirect`;

                // Add CSRF token as hidden input
                if (csrfToken) {
                    const csrfInput = document.createElement("input");
                    csrfInput.type = "hidden";
                    csrfInput.name = "csrfmiddlewaretoken";
                    csrfInput.value = csrfToken;
                    form.appendChild(csrfInput);
                }

                // Add provider
                const providerInput = document.createElement("input");
                providerInput.type = "hidden";
                providerInput.name = "provider";
                providerInput.value = providerId;
                form.appendChild(providerInput);

                // Add process
                const processInput = document.createElement("input");
                processInput.type = "hidden";
                processInput.name = "process";
                processInput.value = "login";
                form.appendChild(processInput);

                // Add callback URL if provided
                if (callbackUrl) {
                    const callbackInput = document.createElement("input");
                    callbackInput.type = "hidden";
                    callbackInput.name = "callback_url";
                    callbackInput.value = callbackUrl;
                    form.appendChild(callbackInput);
                }

                // Submit form to trigger redirect
                document.body.appendChild(form);
                form.submit();

                return { success: true };
            } catch (error) {
                console.error("Provider login error:", error);
                return {
                    success: false,
                    error: error instanceof Error ? error.message : "Provider login failed",
                };
            }
        },

        // Handle provider token (for mobile apps or custom OAuth flows)
        async loginWithProviderToken(providerId: string, token: string, tokenType: string = "access_token") {
            try {
                const csrfToken = getCsrfToken();
                const headers: Record<string, string> = {
                    "Content-Type": "application/json",
                };
                if (csrfToken) {
                    headers["X-CSRFToken"] = csrfToken;
                }

                const response = await fetch(`${API_URL}/_allauth/${CLIENT}/v1/auth/provider/token`, {
                    method: "POST",
                    headers,
                    credentials: "include",
                    body: JSON.stringify({
                        provider: providerId,
                        token,
                        token_type: tokenType,
                    }),
                });

                const result: AuthResponse = await response.json();

                if (!response.ok) {
                    const errorMessage = result.errors?.[0]?.message || "Token authentication failed";
                    throw new Error(errorMessage);
                }

                // Check if fully authenticated
                if (result.meta?.is_authenticated && result.data?.user) {
                    set({ user: result.data.user, isAuthenticated: true, isLoading: false });
                    return { success: true };
                }

                // Handle flows (e.g., additional signup info needed)
                if (result.data?.flows && result.data.flows.length > 0) {
                    return {
                        success: false,
                        error: "Additional information required",
                        flows: result.data.flows,
                    };
                }

                return { success: true };
            } catch (error) {
                console.error("Provider token error:", error);
                return {
                    success: false,
                    error: error instanceof Error ? error.message : "Token authentication failed",
                };
            }
        },

        // Get connected provider accounts for authenticated user
        async getConnectedProviders(): Promise<ProviderAccount[]> {
            try {
                const response = await fetch(`${API_URL}/_allauth/${CLIENT}/v1/account/providers`, {
                    credentials: "include",
                });

                const result = await response.json();
                return result.data || [];
            } catch (error) {
                console.error("Failed to fetch connected providers:", error);
                return [];
            }
        },

        // Disconnect a provider account
        async disconnectProvider(providerId: string, accountUid: string) {
            try {
                const csrfToken = getCsrfToken();
                const headers: Record<string, string> = {
                    "Content-Type": "application/json",
                };
                if (csrfToken) {
                    headers["X-CSRFToken"] = csrfToken;
                }

                const response = await fetch(`${API_URL}/_allauth/${CLIENT}/v1/account/providers`, {
                    method: "DELETE",
                    headers,
                    credentials: "include",
                    body: JSON.stringify({
                        provider: providerId,
                        account: accountUid,
                    }),
                });

                if (response.ok) {
                    return { success: true };
                } else {
                    const result = await response.json();
                    const errorMessage = result.errors?.[0]?.message || "Failed to disconnect provider";
                    return { success: false, error: errorMessage };
                }
            } catch (error) {
                console.error("Disconnect provider error:", error);
                return {
                    success: false,
                    error: error instanceof Error ? error.message : "Failed to disconnect provider",
                };
            }
        },
    };
}

export const auth = createAuthStore();
