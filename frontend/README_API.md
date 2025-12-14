# API Client Setup

This project uses `openapi-typescript` and `openapi-fetch` for type-safe API communication.

## Setup

1. **Ensure Django backend is running:**
   ```bash
   cd /Users/ianday/git/okletsdoit
   just up
   ```

2. **Generate TypeScript types from OpenAPI spec:**
   ```bash
   cd /Users/ianday/git/okletsdoit_web
   bun run openapi:generate
   ```

   This will create `src/lib/api/schema.d.ts` with all the API types.

3. **Configure environment variables:**
   ```bash
   # .env (already configured)
   PUBLIC_API_URL=http://localhost:8000
   SERVICE_TOKEN=your-secure-service-token-here
   ```

## Usage

### Server-Side (SSR)

Use the typed client in `+page.server.ts` or `+server.ts` files:

```typescript
import { apiClient } from '$lib/server/client';

export const load = async () => {
    // Fully typed request and response
    const { data, error } = await apiClient.GET("/guestlist/guest-groups");
    
    if (error) {
        throw error(500, "Failed to fetch guest groups");
    }
    
    return { guestGroups: data };
};
```

### Client-Side

For client-side requests with user session tokens, create a similar client:

```typescript
// src/lib/client/api.ts
import createClient from "openapi-fetch";
import type { paths } from "$lib/api/schema";

export function createUserApiClient(sessionToken: string) {
    return createClient<paths>({
        baseUrl: "/api",  // Proxied through SvelteKit
        headers: {
            "X-Session-Token": sessionToken,
        },
    });
}
```

## Regenerating Types

Whenever the Django API changes:

```bash
# Local development
bun run openapi:generate

# Production URL
bun run openapi:generate:prod
```

## Benefits

- ✅ **Full type safety** - Request/response types match your API exactly
- ✅ **Autocomplete** - IntelliSense for all endpoints and parameters
- ✅ **Compile-time errors** - Catch API mismatches before runtime
- ✅ **Automatic updates** - Regenerate types when API changes
- ✅ **No manual typing** - Types are generated from source of truth

## Example: CRUD Operations

```typescript
// List with pagination
const { data } = await apiClient.GET("/guestlist/guest-groups", {
    params: {
        query: { page: 1, page_size: 50 }
    }
});

// Get single item
const { data } = await apiClient.GET("/guestlist/guest-groups/{group_id}", {
    params: {
        path: { group_id: "uuid-here" }
    }
});

// Create
const { data } = await apiClient.POST("/guestlist/guest-groups", {
    body: {
        name: "Smith Family",
        email: "smith@example.com",
    }
});

// Update
const { data } = await apiClient.PUT("/guestlist/guest-groups/{group_id}", {
    params: {
        path: { group_id: "uuid-here" }
    },
    body: {
        name: "Updated Name"
    }
});

// Delete
const { data } = await apiClient.DELETE("/guestlist/guest-groups/{group_id}", {
    params: {
        path: { group_id: "uuid-here" }
    }
});
```
