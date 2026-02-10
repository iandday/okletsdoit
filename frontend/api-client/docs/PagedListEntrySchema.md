# PagedListEntrySchema

## Properties

| Name    | Type                                               |
| ------- | -------------------------------------------------- |
| `items` | [Array&lt;ListEntrySchema&gt;](ListEntrySchema.md) |
| `count` | number                                             |

## Example

```typescript
import type { PagedListEntrySchema } from "";

// TODO: Update the object below with actual values
const example = {
    items: null,
    count: null,
} satisfies PagedListEntrySchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as PagedListEntrySchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
