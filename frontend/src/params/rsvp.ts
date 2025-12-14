import type { ParamMatcher } from '@sveltejs/kit';

/**
 * Matches a 10-character RSVP code
 * Valid characters: A-Z, a-z, 0-9
 */
export const match: ParamMatcher = (param) => {
	return /^[A-Za-z0-9]{10}$/.test(param);
};
