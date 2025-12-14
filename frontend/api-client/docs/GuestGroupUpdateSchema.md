
# GuestGroupUpdateSchema


## Properties

Name | Type
------------ | -------------
`name` | string
`addressName` | string
`notes` | string
`email` | string
`phone` | string
`address` | string
`addressTwo` | string
`city` | string
`state` | string
`zipCode` | string
`relationship` | string
`priority` | number

## Example

```typescript
import type { GuestGroupUpdateSchema } from ''

// TODO: Update the object below with actual values
const example = {
  "name": null,
  "addressName": null,
  "notes": null,
  "email": null,
  "phone": null,
  "address": null,
  "addressTwo": null,
  "city": null,
  "state": null,
  "zipCode": null,
  "relationship": null,
  "priority": null,
} satisfies GuestGroupUpdateSchema

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as GuestGroupUpdateSchema
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


