# GuestGroupSchema

## Properties

| Name                      | Type    |
| ------------------------- | ------- |
| `id`                      | string  |
| `slug`                    | string  |
| `name`                    | string  |
| `addressName`             | string  |
| `notes`                   | string  |
| `email`                   | string  |
| `phone`                   | string  |
| `address`                 | string  |
| `addressTwo`              | string  |
| `city`                    | string  |
| `state`                   | string  |
| `zipCode`                 | string  |
| `relationship`            | string  |
| `relationshipDisplay`     | string  |
| `priority`                | number  |
| `priorityDisplay`         | string  |
| `associatedWithId`        | string  |
| `associatedWithFirstName` | string  |
| `associatedWithLastName`  | string  |
| `rsvpCode`                | string  |
| `rsvpUrl`                 | string  |
| `qrCodeUrl`               | string  |
| `hasQrCode`               | boolean |
| `groupCount`              | number  |
| `groupStandard`           | number  |
| `groupVip`                | number  |
| `groupOvernight`          | number  |
| `groupInvitedCount`       | number  |
| `groupAttendingCount`     | number  |
| `groupDeclinedCount`      | number  |
| `createdAt`               | Date    |
| `updatedAt`               | Date    |

## Example

```typescript
import type { GuestGroupSchema } from "";

// TODO: Update the object below with actual values
const example = {
    id: null,
    slug: null,
    name: null,
    addressName: null,
    notes: null,
    email: null,
    phone: null,
    address: null,
    addressTwo: null,
    city: null,
    state: null,
    zipCode: null,
    relationship: null,
    relationshipDisplay: null,
    priority: null,
    priorityDisplay: null,
    associatedWithId: null,
    associatedWithFirstName: null,
    associatedWithLastName: null,
    rsvpCode: null,
    rsvpUrl: null,
    qrCodeUrl: null,
    hasQrCode: null,
    groupCount: null,
    groupStandard: null,
    groupVip: null,
    groupOvernight: null,
    groupInvitedCount: null,
    groupAttendingCount: null,
    groupDeclinedCount: null,
    createdAt: null,
    updatedAt: null,
} satisfies GuestGroupSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as GuestGroupSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
