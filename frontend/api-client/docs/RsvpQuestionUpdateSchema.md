# RsvpQuestionUpdateSchema

## Properties

| Name           | Type    |
| -------------- | ------- |
| `text`         | string  |
| `order`        | number  |
| `published`    | boolean |
| `questionType` | string  |

## Example

```typescript
import type { RsvpQuestionUpdateSchema } from "";

// TODO: Update the object below with actual values
const example = {
    text: null,
    order: null,
    published: null,
    questionType: null,
} satisfies RsvpQuestionUpdateSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as RsvpQuestionUpdateSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
