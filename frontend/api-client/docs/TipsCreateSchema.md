# TipsCreateSchema

## Properties

| Name         | Type    |
| ------------ | ------- |
| `categoryId` | string  |
| `content`    | string  |
| `order`      | number  |
| `published`  | boolean |

## Example

```typescript
import type { TipsCreateSchema } from "";

// TODO: Update the object below with actual values
const example = {
    categoryId: null,
    content: null,
    order: null,
    published: null,
} satisfies TipsCreateSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TipsCreateSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
