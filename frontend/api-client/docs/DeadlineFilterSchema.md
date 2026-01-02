# DeadlineFilterSchema

## Properties

| Name             | Type    |
| ---------------- | ------- |
| `deadlineListId` | string  |
| `completed`      | boolean |
| `assignedToId`   | string  |

## Example

```typescript
import type { DeadlineFilterSchema } from "";

// TODO: Update the object below with actual values
const example = {
    deadlineListId: null,
    completed: null,
    assignedToId: null,
} satisfies DeadlineFilterSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as DeadlineFilterSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
