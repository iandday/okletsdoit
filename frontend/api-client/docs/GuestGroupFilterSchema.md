# GuestGroupFilterSchema

## Properties

| Name           | Type   |
| -------------- | ------ |
| `name`         | string |
| `email`        | string |
| `phone`        | string |
| `city`         | string |
| `state`        | string |
| `zipCode`      | string |
| `relationship` | string |
| `priority`     | number |
| `rsvpCode`     | string |

## Example

```typescript
import type { GuestGroupFilterSchema } from "";

// TODO: Update the object below with actual values
const example = {
    name: null,
    email: null,
    phone: null,
    city: null,
    state: null,
    zipCode: null,
    relationship: null,
    priority: null,
    rsvpCode: null,
} satisfies GuestGroupFilterSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as GuestGroupFilterSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
