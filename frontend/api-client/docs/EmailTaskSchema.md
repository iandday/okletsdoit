# EmailTaskSchema

## Properties

| Name      | Type    |
| --------- | ------- |
| `success` | boolean |
| `message` | string  |
| `taskId`  | string  |

## Example

```typescript
import type { EmailTaskSchema } from "";

// TODO: Update the object below with actual values
const example = {
    success: null,
    message: null,
    taskId: null,
} satisfies EmailTaskSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as EmailTaskSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
