# DeadlineSchema

## Properties

| Name               | Type    |
| ------------------ | ------- |
| `id`               | string  |
| `name`             | string  |
| `slug`             | string  |
| `description`      | string  |
| `deadlineListId`   | string  |
| `deadlineListName` | string  |
| `dueDate`          | Date    |
| `assignedToId`     | string  |
| `assignedToName`   | string  |
| `completed`        | boolean |
| `completedAt`      | Date    |
| `completedNote`    | string  |
| `overdue`          | boolean |
| `createdById`      | string  |
| `createdByName`    | string  |
| `updatedById`      | string  |
| `updatedByName`    | string  |
| `createdAt`        | Date    |
| `updatedAt`        | Date    |

## Example

```typescript
import type { DeadlineSchema } from "";

// TODO: Update the object below with actual values
const example = {
    id: null,
    name: null,
    slug: null,
    description: null,
    deadlineListId: null,
    deadlineListName: null,
    dueDate: null,
    assignedToId: null,
    assignedToName: null,
    completed: null,
    completedAt: null,
    completedNote: null,
    overdue: null,
    createdById: null,
    createdByName: null,
    updatedById: null,
    updatedByName: null,
    createdAt: null,
    updatedAt: null,
} satisfies DeadlineSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as DeadlineSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
