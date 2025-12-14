# GuestUpdateSchema

## Properties

| Name                  | Type    |
| --------------------- | ------- |
| `firstName`           | string  |
| `lastName`            | string  |
| `plusOne`             | boolean |
| `groupId`             | string  |
| `isInvited`           | boolean |
| `isAttending`         | boolean |
| `responded`           | boolean |
| `acceptAccommodation` | boolean |
| `acceptVip`           | boolean |
| `accommodation`       | boolean |
| `vip`                 | boolean |
| `notes`               | string  |

## Example

```typescript
import type { GuestUpdateSchema } from "";

// TODO: Update the object below with actual values
const example = {
    firstName: null,
    lastName: null,
    plusOne: null,
    groupId: null,
    isInvited: null,
    isAttending: null,
    responded: null,
    acceptAccommodation: null,
    acceptVip: null,
    accommodation: null,
    vip: null,
    notes: null,
} satisfies GuestUpdateSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as GuestUpdateSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
