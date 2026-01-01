# RsvpQuestionSchema

## Properties

| Name           | Type                                                                 |
| -------------- | -------------------------------------------------------------------- |
| `id`           | string                                                               |
| `text`         | string                                                               |
| `order`        | number                                                               |
| `published`    | boolean                                                              |
| `questionType` | string                                                               |
| `choices`      | [Array&lt;RsvpQuestionChoiceSchema&gt;](RsvpQuestionChoiceSchema.md) |
| `createdAt`    | Date                                                                 |
| `updatedAt`    | Date                                                                 |

## Example

```typescript
import type { RsvpQuestionSchema } from "";

// TODO: Update the object below with actual values
const example = {
    id: null,
    text: null,
    order: null,
    published: null,
    questionType: null,
    choices: null,
    createdAt: null,
    updatedAt: null,
} satisfies RsvpQuestionSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as RsvpQuestionSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
