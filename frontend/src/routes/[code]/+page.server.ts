import { error } from '@sveltejs/kit';
import { apiClient } from '$lib/server/client';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params }) => {
    const { code } = params;

    // Validate code format (10 characters)
    if (!code || code.length !== 10) {
        throw error(400, 'Invalid RSVP code format. Code must be 10 characters.');
    }

    // Query the API for guest group by RSVP code
    const { data, error: apiError } = await apiClient.GET('/api/guestlist/guest-groups', {
        params: {
            query: {
                rsvp_code: code.toUpperCase()
            }
        }
    });

    if (apiError) {
        throw error(500, 'Failed to validate RSVP code');
    }

    // Check if we got results
    if (!data || !data.items || data.items.length === 0) {
        throw error(404, 'RSVP code not found. Please check your code and try again.');
    }

    const guestGroup = data.items[0];

    return {
        guestGroup,
        rsvpCode: code
    };
};
