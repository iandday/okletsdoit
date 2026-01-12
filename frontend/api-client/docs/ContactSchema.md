# ContactSchema

## Properties

| Name            | Type   |
| --------------- | ------ |
| `id`            | string |
| `name`          | string |
| `slug`          | string |
| `company`       | string |
| `email`         | string |
| `phone`         | string |
| `website`       | string |
| `category`      | string |
| `notes`         | string |
| `createdById`   | string |
| `createdByName` | string |
| `updatedById`   | string |
| `updatedByName` | string |
| `createdAt`     | Date   |
| `updatedAt`     | Date   |

## Example

```typescript
import type { ContactSchema } from "";

// TODO: Update the object below with actual values
const example = {
    id: null,
    name: null,
    slug: null,
    company: null,
    email: null,
    phone: null,
    website: null,
    category: null,
    notes: null,
    createdById: null,
    createdByName: null,
    updatedById: null,
    updatedByName: null,
    createdAt: null,
    updatedAt: null,
} satisfies ContactSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ContactSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
