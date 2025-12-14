# RsvpSubmissionCreateSchema

## Properties

| Name           | Type    |
| -------------- | ------- |
| `guestGroupId` | string  |
| `emailUpdates` | boolean |
| `emailAddress` | string  |
| `notes`        | string  |

## Example

```typescript
import type { RsvpSubmissionCreateSchema } from "";

// TODO: Update the object below with actual values
const example = {
    guestGroupId: null,
    emailUpdates: null,
    emailAddress: null,
    notes: null,
} satisfies RsvpSubmissionCreateSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as RsvpSubmissionCreateSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
