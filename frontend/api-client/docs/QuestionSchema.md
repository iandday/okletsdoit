# QuestionSchema

## Properties

| Name        | Type                                                   |
| ----------- | ------------------------------------------------------ |
| `id`        | string                                                 |
| `category`  | string                                                 |
| `question`  | string                                                 |
| `slug`      | string                                                 |
| `answer`    | string                                                 |
| `order`     | number                                                 |
| `icon`      | string                                                 |
| `urls`      | [Array&lt;QuestionURLSchema&gt;](QuestionURLSchema.md) |
| `published` | boolean                                                |
| `createdAt` | Date                                                   |
| `updatedAt` | Date                                                   |

## Example

```typescript
import type { QuestionSchema } from "";

// TODO: Update the object below with actual values
const example = {
    id: null,
    category: null,
    question: null,
    slug: null,
    answer: null,
    order: null,
    icon: null,
    urls: null,
    published: null,
    createdAt: null,
    updatedAt: null,
} satisfies QuestionSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as QuestionSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
