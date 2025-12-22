# TipsSchema

## Properties

| Name        | Type    |
| ----------- | ------- |
| `id`        | string  |
| `category`  | string  |
| `content`   | string  |
| `order`     | number  |
| `published` | boolean |
| `createdAt` | Date    |
| `updatedAt` | Date    |

## Example

```typescript
import type { TipsSchema } from "";

// TODO: Update the object below with actual values
const example = {
    id: null,
    category: null,
    content: null,
    order: null,
    published: null,
    createdAt: null,
    updatedAt: null,
} satisfies TipsSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TipsSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
