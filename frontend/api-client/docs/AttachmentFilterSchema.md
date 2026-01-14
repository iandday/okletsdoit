# AttachmentFilterSchema

## Properties

| Name            | Type   |
| --------------- | ------ |
| `contentTypeId` | number |
| `objectId`      | string |
| `search`        | string |

## Example

```typescript
import type { AttachmentFilterSchema } from "";

// TODO: Update the object below with actual values
const example = {
    contentTypeId: null,
    objectId: null,
    search: null,
} satisfies AttachmentFilterSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as AttachmentFilterSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
