# ListEntryFilterSchema

## Properties

| Name          | Type    |
| ------------- | ------- |
| `item`        | string  |
| `listId`      | string  |
| `isCompleted` | boolean |
| `purchased`   | boolean |
| `vendorId`    | string  |

## Example

```typescript
import type { ListEntryFilterSchema } from "";

// TODO: Update the object below with actual values
const example = {
    item: null,
    listId: null,
    isCompleted: null,
    purchased: null,
    vendorId: null,
} satisfies ListEntryFilterSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ListEntryFilterSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
