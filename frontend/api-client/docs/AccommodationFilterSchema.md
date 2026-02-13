# AccommodationFilterSchema

## Properties

| Name                | Type   |
| ------------------- | ------ |
| `name`              | string |
| `accommodationType` | string |
| `city`              | string |
| `state`             | string |

## Example

```typescript
import type { AccommodationFilterSchema } from "";

// TODO: Update the object below with actual values
const example = {
    name: null,
    accommodationType: null,
    city: null,
    state: null,
} satisfies AccommodationFilterSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as AccommodationFilterSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
