// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
declare global {
    namespace App {
        // interface Error {}
        interface Locals {
            user: {
                id?: number;
                display?: string;
                username?: string;
                email?: string;
                has_usable_password?: boolean;
            } | null;
            sessionCookie?: string;
        }
        // interface PageData {}
        // interface PageState {}
        // interface Platform {}
    }
}

export {};
