# DeadlineUpdateSchema

## Properties

| Name             | Type    |
| ---------------- | ------- |
| `name`           | string  |
| `description`    | string  |
| `deadlineListId` | string  |
| `dueDate`        | Date    |
| `assignedToId`   | string  |
| `completed`      | boolean |
| `completedNote`  | string  |

## Example

```typescript
import type { DeadlineUpdateSchema } from "";

// TODO: Update the object below with actual values
const example = {
    name: null,
    description: null,
    deadlineListId: null,
    dueDate: null,
    assignedToId: null,
    completed: null,
    completedNote: null,
} satisfies DeadlineUpdateSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as DeadlineUpdateSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
