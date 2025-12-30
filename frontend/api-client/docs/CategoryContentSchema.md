# CategoryContentSchema

## Properties

| Name            | Type                                             |
| --------------- | ------------------------------------------------ |
| `categoryId`    | string                                           |
| `categoryName`  | string                                           |
| `categoryOrder` | number                                           |
| `questions`     | [Array&lt;QuestionSchema&gt;](QuestionSchema.md) |
| `tips`          | [Array&lt;TipsSchema&gt;](TipsSchema.md)         |

## Example

```typescript
import type { CategoryContentSchema } from "";

// TODO: Update the object below with actual values
const example = {
    categoryId: null,
    categoryName: null,
    categoryOrder: null,
    questions: null,
    tips: null,
} satisfies CategoryContentSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as CategoryContentSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
