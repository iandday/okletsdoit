# PagedRsvpSubmissionSchema

## Properties

| Name    | Type                                                         |
| ------- | ------------------------------------------------------------ |
| `items` | [Array&lt;RsvpSubmissionSchema&gt;](RsvpSubmissionSchema.md) |
| `count` | number                                                       |

## Example

```typescript
import type { PagedRsvpSubmissionSchema } from "";

// TODO: Update the object below with actual values
const example = {
    items: null,
    count: null,
} satisfies PagedRsvpSubmissionSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as PagedRsvpSubmissionSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)
