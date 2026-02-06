# ListSchema

## Properties

| Name                   | Type   |
| ---------------------- | ------ |
| `id`                   | string |
| `name`                 | string |
| `slug`                 | string |
| `description`          | string |
| `createdAt`            | Date   |
| `updatedAt`            | Date   |
| `totalEntries`         | number |
| `completedEntries`     | number |
| `pendingEntries`       | number |
| `completionPercentage` | number |

## Example

```typescript
import type { ListSchema } from "";

// TODO: Update the object below with actual values
const example = {
    id: null,
    name: null,
    slug: null,
    description: null,
    createdAt: null,
    updatedAt: null,
    totalEntries: null,
    completedEntries: null,
    pendingEntries: null,
    completionPercentage: null,
} satisfies ListSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ListSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
