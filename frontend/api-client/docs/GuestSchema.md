
# GuestSchema


## Properties

Name | Type
------------ | -------------
`id` | string
`slug` | string
`firstName` | string
`lastName` | string
`plusOne` | boolean
`groupId` | string
`isInvited` | boolean
`isAttending` | boolean
`responded` | boolean
`acceptAccommodation` | boolean
`acceptVip` | boolean
`accommodation` | boolean
`vip` | boolean
`notes` | string
`createdAt` | Date
`updatedAt` | Date

## Example

```typescript
import type { GuestSchema } from ''

// TODO: Update the object below with actual values
const example = {
  "id": null,
  "slug": null,
  "firstName": null,
  "lastName": null,
  "plusOne": null,
  "groupId": null,
  "isInvited": null,
  "isAttending": null,
  "responded": null,
  "acceptAccommodation": null,
  "acceptVip": null,
  "accommodation": null,
  "vip": null,
  "notes": null,
  "createdAt": null,
  "updatedAt": null,
} satisfies GuestSchema

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as GuestSchema
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


