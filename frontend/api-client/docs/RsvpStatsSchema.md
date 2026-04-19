# RsvpStatsSchema

## Properties

| Name                    | Type   |
| ----------------------- | ------ |
| `groupsInvited`         | number |
| `groupsAccepted`        | number |
| `groupsDeclined`        | number |
| `totalInvited`          | number |
| `totalAttending`        | number |
| `totalDeclined`         | number |
| `totalAccommodation`    | number |
| `totalVipAccepted`      | number |
| `totalStandardAccepted` | number |

## Example

```typescript
import type { RsvpStatsSchema } from "";

// TODO: Update the object below with actual values
const example = {
    groupsInvited: null,
    groupsAccepted: null,
    groupsDeclined: null,
    totalInvited: null,
    totalAttending: null,
    totalDeclined: null,
    totalAccommodation: null,
    totalVipAccepted: null,
    totalStandardAccepted: null,
} satisfies RsvpStatsSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as RsvpStatsSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
