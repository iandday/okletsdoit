# PagedAccommodationSchema

## Properties

| Name    | Type                                                       |
| ------- | ---------------------------------------------------------- |
| `items` | [Array&lt;AccommodationSchema&gt;](AccommodationSchema.md) |
| `count` | number                                                     |

## Example

```typescript
import type { PagedAccommodationSchema } from "";

// TODO: Update the object below with actual values
const example = {
    items: null,
    count: null,
} satisfies PagedAccommodationSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as PagedAccommodationSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
