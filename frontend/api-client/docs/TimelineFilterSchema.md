# TimelineFilterSchema

## Properties

| Name        | Type    |
| ----------- | ------- |
| `name`      | string  |
| `published` | boolean |
| `confirmed` | boolean |

## Example

```typescript
import type { TimelineFilterSchema } from "";

// TODO: Update the object below with actual values
const example = {
    name: null,
    published: null,
    confirmed: null,
} satisfies TimelineFilterSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TimelineFilterSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
