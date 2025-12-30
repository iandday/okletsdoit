# QuestionURLSchema

## Properties

| Name   | Type   |
| ------ | ------ |
| `id`   | string |
| `url`  | string |
| `text` | string |

## Example

```typescript
import type { QuestionURLSchema } from "";

// TODO: Update the object below with actual values
const example = {
    id: null,
    url: null,
    text: null,
} satisfies QuestionURLSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as QuestionURLSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
