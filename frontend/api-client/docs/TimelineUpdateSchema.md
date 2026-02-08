# TimelineUpdateSchema

## Properties

| Name          | Type    |
| ------------- | ------- |
| `name`        | string  |
| `start`       | Date    |
| `end`         | Date    |
| `order`       | number  |
| `published`   | boolean |
| `confirmed`   | boolean |
| `description` | string  |

## Example

```typescript
import type { TimelineUpdateSchema } from "";

// TODO: Update the object below with actual values
const example = {
    name: null,
    start: null,
    end: null,
    order: null,
    published: null,
    confirmed: null,
    description: null,
} satisfies TimelineUpdateSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TimelineUpdateSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
