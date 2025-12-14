# RsvpQuestionResponseCreateSchema

## Properties

| Name                | Type                |
| ------------------- | ------------------- |
| `submissionId`      | string              |
| `questionId`        | string              |
| `responseText`      | string              |
| `responseChoiceIds` | Array&lt;string&gt; |

## Example

```typescript
import type { RsvpQuestionResponseCreateSchema } from "";

// TODO: Update the object below with actual values
const example = {
    submissionId: null,
    questionId: null,
    responseText: null,
    responseChoiceIds: null,
} satisfies RsvpQuestionResponseCreateSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as RsvpQuestionResponseCreateSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
