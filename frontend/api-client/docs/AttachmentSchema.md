# AttachmentSchema

## Properties

| Name                  | Type   |
| --------------------- | ------ |
| `id`                  | string |
| `name`                | string |
| `slug`                | string |
| `description`         | string |
| `filename`            | string |
| `fileUrl`             | string |
| `contentTypeId`       | number |
| `contentTypeAppLabel` | string |
| `contentTypeModel`    | string |
| `objectId`            | string |
| `uploadedById`        | string |
| `uploadedByName`      | string |
| `updatedById`         | string |
| `updatedByName`       | string |
| `uploadedAt`          | Date   |
| `updatedAt`           | Date   |

## Example

```typescript
import type { AttachmentSchema } from "";

// TODO: Update the object below with actual values
const example = {
    id: null,
    name: null,
    slug: null,
    description: null,
    filename: null,
    fileUrl: null,
    contentTypeId: null,
    contentTypeAppLabel: null,
    contentTypeModel: null,
    objectId: null,
    uploadedById: null,
    uploadedByName: null,
    updatedById: null,
    updatedByName: null,
    uploadedAt: null,
    updatedAt: null,
} satisfies AttachmentSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as AttachmentSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
