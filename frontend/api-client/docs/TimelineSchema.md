# TimelineSchema

## Properties

| Name            | Type    |
| --------------- | ------- |
| `id`            | string  |
| `name`          | string  |
| `slug`          | string  |
| `start`         | Date    |
| `end`           | Date    |
| `order`         | number  |
| `published`     | boolean |
| `confirmed`     | boolean |
| `description`   | string  |
| `createdById`   | string  |
| `createdByName` | string  |
| `updatedById`   | string  |
| `updatedByName` | string  |
| `createdAt`     | Date    |
| `updatedAt`     | Date    |

## Example

```typescript
import type { TimelineSchema } from "";

// TODO: Update the object below with actual values
const example = {
    id: null,
    name: null,
    slug: null,
    start: null,
    end: null,
    order: null,
    published: null,
    confirmed: null,
    description: null,
    createdById: null,
    createdByName: null,
    updatedById: null,
    updatedByName: null,
    createdAt: null,
    updatedAt: null,
} satisfies TimelineSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TimelineSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
