# QuestionUpdateSchema

## Properties

| Name         | Type    |
| ------------ | ------- |
| `categoryId` | string  |
| `question`   | string  |
| `answer`     | string  |
| `order`      | number  |
| `icon`       | string  |
| `published`  | boolean |

## Example

```typescript
import type { QuestionUpdateSchema } from "";

// TODO: Update the object below with actual values
const example = {
    categoryId: null,
    question: null,
    answer: null,
    order: null,
    icon: null,
    published: null,
} satisfies QuestionUpdateSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as QuestionUpdateSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
