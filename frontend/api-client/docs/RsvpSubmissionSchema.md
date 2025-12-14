# RsvpSubmissionSchema

## Properties

| Name                       | Type    |
| -------------------------- | ------- |
| `id`                       | string  |
| `guestGroupId`             | string  |
| `emailUpdates`             | boolean |
| `emailAddress`             | string  |
| `notes`                    | string  |
| `acceptAccommodationCount` | number  |
| `acceptVipCount`           | number  |
| `createdAt`                | Date    |
| `updatedAt`                | Date    |

## Example

```typescript
import type { RsvpSubmissionSchema } from "";

// TODO: Update the object below with actual values
const example = {
    id: null,
    guestGroupId: null,
    emailUpdates: null,
    emailAddress: null,
    notes: null,
    acceptAccommodationCount: null,
    acceptVipCount: null,
    createdAt: null,
    updatedAt: null,
} satisfies RsvpSubmissionSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as RsvpSubmissionSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
