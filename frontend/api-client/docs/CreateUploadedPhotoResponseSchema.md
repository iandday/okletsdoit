# CreateUploadedPhotoResponseSchema

## Properties

| Name        | Type   |
| ----------- | ------ |
| `id`        | string |
| `uploadUrl` | string |

## Example

```typescript
import type { CreateUploadedPhotoResponseSchema } from "";

// TODO: Update the object below with actual values
const example = {
    id: null,
    uploadUrl: null,
} satisfies CreateUploadedPhotoResponseSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as CreateUploadedPhotoResponseSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
